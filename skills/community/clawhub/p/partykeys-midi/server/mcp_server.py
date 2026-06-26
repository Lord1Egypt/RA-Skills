"""
PartyKeys MCP Server
通过 WebSocket（端口 18790）控制音乐硬件 - 支持手机 App 和浏览器页面连接
"""
import asyncio
import json
import subprocess
import os
from typing import Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
import aiohttp
from aiohttp import web
from script_ble_client import ScriptBLEClient

WS_PORT = 18790

class MobileBridge:
    """
    WebSocket server that accepts connections from mobile app and web browser.
    统一架构：手机 App 和 浏览器页面都连接同一个 WebSocket 端口
    """

    def __init__(self):
        self._clients: set = set()  # 所有 WebSocket 客户端
        self._app: Optional[web.Application] = None
        self._runner: Optional[web.AppRunner] = None
        self._pending: dict[str, web.WebSocketResponse] = {}  # cmd_id -> requester_ws
        self._cmd_id = 0

    async def start(self, port: int = WS_PORT) -> dict:
        self._app = web.Application()
        self._app.router.add_get('/ws', self._handle_ws)
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, '0.0.0.0', port)
        await site.start()
        return {"success": True, "port": port}

    async def stop(self):
        for client in self._clients:
            if not client.closed:
                await client.close()
        if self._runner:
            await self._runner.cleanup()
        self._clients.clear()

    @property
    def is_connected(self) -> bool:
        return len(self._clients) > 0

    @property
    def client_count(self) -> int:
        return len(self._clients)

    async def _handle_ws(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._clients.add(ws)

        client_info = f"新客户端 (现有 {len(self._clients)} 个客户端)"
        print(f"[WS] {client_info}")

        try:
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    msg_type = data.get('type', '')

                    if msg_type == 'status':
                        # 客户端发送状态更新
                        ble = data.get('data', {}).get('bleConnected', False)
                        bridge = data.get('data', {}).get('bridge', 'unknown')
                        print(f"[WS] 状态更新：BLE={ble}, bridge={bridge}")
                        # 更新 BLE 连接状态
                        gateway.ble_connected = ble
                        if ble:
                            gateway.mode = gateway.mode or "web"  # 自动设置为 web 模式

                    elif msg_type == 'command':
                        # 转发命令给所有其他客户端（广播）
                        cmd_id = data.get('id', '')
                        self._pending[cmd_id] = ws  # 记录请求者
                        print(f"[WS] 收到命令：{data.get('command', {})}")

                        # 广播给所有其他客户端
                        for client in self._clients:
                            if client != ws and not client.closed:
                                await client.send_json(data)
                                print(f"[WS] 转发命令到客户端")

                    elif msg_type == 'result':
                        # 转发结果给请求者
                        fid = data.get('id', '')
                        requester_ws = self._pending.pop(fid, None)
                        if requester_ws and not requester_ws.closed:
                            await requester_ws.send_json(data)
                            print(f"[WS] 转发结果给请求者")

                    elif msg_type == 'ping':
                        await ws.send_json({'type': 'pong'})

                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break

        except Exception as e:
            print(f"[WS] 异常：{e}")
        finally:
            self._clients.discard(ws)
            self._pending = {k: v for k, v in self._pending.items() if v != ws}
            print(f"[WS] 客户端断开 (剩余 {len(self._clients)} 个客户端)")

        return ws

    async def send_command(self, command: str, params: dict, timeout: float = 30) -> dict:
        """从 MCP 发送命令到所有客户端"""
        if not self.is_connected:
            return {"success": False, "error": "没有客户端连接"}

        self._cmd_id += 1
        cmd_id = str(self._cmd_id)

        msg = {
            'type': 'command',
            'id': cmd_id,
            'command': {'command': command, 'params': params},
        }

        # 广播给所有客户端
        sent_count = 0
        for client in self._clients:
            if not client.closed:
                await client.send_json(msg)
                sent_count += 1

        print(f"[WS] 发送命令到 {sent_count} 个客户端：{command}")
        return {"success": True, "note": f"命令已发送到 {sent_count} 个客户端"}


class GatewayManager:
    """
    统一网关管理器 - 只支持 WebSocket 模式（端口 18790）
    手机 App 和浏览器页面都通过 WebSocket 连接
    """
    def __init__(self):
        self.connected = False
        self.script_client: Optional[ScriptBLEClient] = None
        self.mobile_bridge: Optional[MobileBridge] = None
        self.mode: Optional[str] = None
        self.ble_connected: bool = False  # 跟踪 BLE 连接状态

    async def send_command(self, command: str, params: dict) -> dict:
        """通过 mobile_bridge 发送命令到 WebSocket 客户端"""
        if self.mobile_bridge:
            return await self.mobile_bridge.send_command(command, params)
        return {"error": "WebSocket service not started"}

# 全局实例
gateway = GatewayManager()
app = Server("partykeys")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """定义 MCP Tools"""
    return [
        Tool(
            name="music_connect",
            description="连接音乐硬件设备",
            inputSchema={
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": ["script", "mobile", "web"],
                        "description": "连接模式：script(脚本直接 BLE，需蓝牙硬件), mobile(手机 App 中转，推荐云端/远程使用), web(浏览器 Web Bluetooth)。注意：Web Bluetooth 仅在浏览器安全上下文中可用（https 或本机 localhost/127.0.0.1）；MCP 部署在云端或用 http://局域网 IP 打开控制页时无法调起蓝牙，请改用 mobile 或在前端自行配置 HTTPS 反向代理。",
                        "default": "mobile"
                    },
                    "address": {
                        "type": "string",
                        "description": "设备地址（script 模式下可选，用于直接连接指定设备）"
                    }
                },
            }
        ),
        Tool(
            name="music_disconnect",
            description="断开音乐硬件连接",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="music_light_keys",
            description="点亮指定按键的 LED 灯",
            inputSchema={
                "type": "object",
                "properties": {
                    "keys": {
                        "oneOf": [
                            {"type": "array", "items": {"type": "string"}},
                            {"type": "string"}
                        ],
                        "description": "音符列表，如 ['C4', 'E4', 'G4'] 或 'C4,E4,G4' 或 '31'"
                    },
                    "colors": {
                        "oneOf": [
                            {"type": "array", "items": {"type": ["string", "number"]}},
                            {"type": "string"},
                            {"type": "number"}
                        ],
                        "description": "颜色数组（每个键不同颜色）或单个颜色值，如 ['red', 'green', 'blue'] 或 'red' 或 1",
                        "default": "blue"
                    },
                    "color": {
                        "type": "string",
                        "description": "颜色（已废弃，使用 colors 代替），如 'red', 'green', 'blue'",
                        "default": "blue"
                    },
                    "brightness": {
                        "type": "number",
                        "description": "亮度 0-100",
                        "default": 100
                    }
                },
                "required": ["keys"]
            }
        ),
        Tool(
            name="music_listen",
            description="监听用户弹奏输入",
            inputSchema={
                "type": "object",
                "properties": {
                    "timeout": {
                        "type": "number",
                        "description": "超时时间（毫秒）",
                        "default": 5000
                    },
                    "mode": {
                        "type": "string",
                        "description": "监听模式：single(单音符) 或 continuous(持续)",
                        "default": "single"
                    }
                }
            }
        ),
        Tool(
            name="music_play_sequence",
            description="播放音符序列（用于曲谱实时点亮）",
            inputSchema={
                "type": "object",
                "properties": {
                    "sequence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "keys": {"type": "array", "items": {"type": "string"}},
                                "delay": {"type": "number", "description": "延迟时间（毫秒）"}
                            }
                        },
                        "description": "音符序列，每个元素包含 keys 和 delay"
                    }
                }
            }
        ),
        Tool(
            name="music_follow_mode",
            description="跟弹模式 - 点亮音符并等待用户弹奏正确后继续",
            inputSchema={
                "type": "object",
                "properties": {
                    "notes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "音符序列（按顺序）"
                    },
                    "timeout": {
                        "type": "number",
                        "description": "每个音符的超时时间（毫秒）",
                        "default": 30000
                    }
                },
                "required": ["notes"]
            }
        ),
        Tool(
            name="music_status",
            description="获取硬件连接状态",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        Tool(
            name="music_set_mode",
            description="切换键盘/设备工作模式",
            inputSchema={
                "type": "object",
                "properties": {
                    "mode": {
                        "type": "string",
                        "enum": [
                            "skin",
                            "free",
                            "game",
                            "skin_config",
                            "drum",
                            "free_light",
                            "singing",
                            "singing_advanced",
                            "app_connect"
                        ],
                        "description": (
                            "模式名称：\n"
                            "  skin         - 皮肤模式（键盘皮肤，音响弹奏）0x00\n"
                            "  free         - 自由模式（键盘弹奏，音响弹奏）0x01\n"
                            "  game         - 游戏模式 0x02\n"
                            "  skin_config  - 皮肤配置/录课模式 0x03\n"
                            "  drum         - 鼓机模式 0x04\n"
                            "  free_light   - 自由模式+音符亮灯 0x05\n"
                            "  singing      - 弹唱模式 0x0E\n"
                            "  singing_advanced - 弹唱高级模式 0x0D\n"
                            "  app_connect  - App连接模式 0x7F"
                        )
                    }
                },
                "required": ["mode"]
            }
        ),
        Tool(
            name="music_set_octave",
            description="设置键盘音区（8度偏移）",
            inputSchema={
                "type": "object",
                "properties": {
                    "octave": {
                        "type": "integer",
                        "minimum": -3,
                        "maximum": 3,
                        "description": "8度偏移量：-3~-1 降低，0 默认，1~3 升高"
                    }
                },
                "required": ["octave"]
            }
        ),
        Tool(
            name="music_set_bpm",
            description="设置节拍速度（BPM）",
            inputSchema={
                "type": "object",
                "properties": {
                    "bpm": {
                        "type": "integer",
                        "minimum": 20,
                        "maximum": 300,
                        "description": "BPM 速度值，范围 20~300"
                    }
                },
                "required": ["bpm"]
            }
        ),
        Tool(
            name="music_chord_light",
            description="根据和弦名称点亮键盘对应按键（教学用）",
            inputSchema={
                "type": "object",
                "properties": {
                    "chord": {
                        "type": "string",
                        "description": (
                            "和弦名称，格式：根音+和弦类型，如 C、Dm、G7、FMaj7、Am7。\n"
                            "根音：C C# D D# E F F# G G# A A# B\n"
                            "和弦类型：Maj(默认大三和弦) Min m7 Maj7 7 Sus4 add9 m7b5 Aug Dim"
                        )
                    },
                    "position": {
                        "type": "integer",
                        "description": "把位偏移，0 为默认把位，正数升高，负数降低",
                        "default": 0
                    }
                },
                "required": ["chord"]
            }
        ),
        Tool(
            name="music_query_version",
            description="查询设备固件版本信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "target": {
                        "type": "string",
                        "enum": ["all", "box", "keyboard"],
                        "description": "查询目标：all=广播查所有设备, box=仅盒子, keyboard=仅键盘",
                        "default": "all"
                    }
                }
            }
        ),
        Tool(
            name="music_set_beat_type",
            description="设置节拍类型（拍号）",
            inputSchema={
                "type": "object",
                "properties": {
                    "beat": {
                        "type": "string",
                        "enum": ["4/4", "4/3", "8/6"],
                        "description": "拍号：4/4(0x00, 默认), 4/3(0x01), 8/6(0x02)"
                    }
                },
                "required": ["beat"]
            }
        ),
        Tool(
            name="music_set_skin",
            description="设置键盘/设备皮肤（色盘）",
            inputSchema={
                "type": "object",
                "properties": {
                    "skin_id": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 127,
                        "description": "色盘编号，0 为默认皮肤"
                    },
                    "query": {
                        "type": "boolean",
                        "description": "若为 true，则仅查询当前已有皮肤列表，不下发设置",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="music_query_device",
            description="查询设备在线状态，获取当前已连接的设备列表",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """处理工具调用"""

    if name == "music_connect":
        mode = arguments.get("mode")

        # 启动 WebSocket 服务
        gateway.mobile_bridge = MobileBridge()
        bridge_result = await gateway.mobile_bridge.start(WS_PORT)

        if not bridge_result.get("success"):
            return [TextContent(
                type="text",
                text=json.dumps(bridge_result, ensure_ascii=False)
            )]

        gateway.connected = True

        # 如果用户指定了模式，直接设置；否则等待用户选择
        if mode:
            gateway.mode = mode

        if mode == "script":
            gateway.script_client = ScriptBLEClient()
            address = arguments.get("address")
            result = await gateway.script_client.connect(address)
            if result.get("success"):
                gateway.mode = "script"
                gateway.connected = True
                result["message"] = f"已通过脚本连接设备：{result['address']}"
        else:
            # 未指定模式或指定 mobile/web 时，返回统一的连接提示
            local_ip = subprocess.run(
                "ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -1",
                shell=True, capture_output=True, text=True
            ).stdout.strip() or "<本机 IP>"

            result = {
                "success": True,
                "services_started": True,
                "ws_port": WS_PORT,
                "local_ip": local_ip,
                "message": f"""✅ WebSocket 服务已启动！

【连接方式 1】📱 手机 App 中转
  1. 在手机打开 PartyKeys Bridge App
  2. 输入服务器地址：ws://{local_ip}:18790/ws
  3. 在 App 中扫描并连接 MIDI 键盘

【连接方式 2】🌐 独立网页版
  1. 打开网页文件：partykeys-bridge-web/standalone.html
  2. 输入 WebSocket 地址：ws://{local_ip}:18790/ws
  3. 点击「连接服务器」，然后点击「连接设备」

【连接方式 3】🌐 部署网页到 GitHub Pages / Vercel
  1. 将 standalone.html 部署到任意 HTTPS 服务
  2. 打开网页，输入 WebSocket 地址：ws://{local_ip}:9528/ws
  3. 连接服务器并连接设备

注意：所有连接方式都使用同一个 WebSocket 端口 18790，可任选其一。"""
            }

        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False)
        )]

    elif name == "music_disconnect":
        if gateway.mode == "script":
            result = await gateway.script_client.disconnect()
            gateway.script_client = None
        elif gateway.mode == "mobile" or gateway.mode == "web":
            result = await gateway.send_command("disconnect", {})
            await gateway.mobile_bridge.stop()
            gateway.mobile_bridge = None

        gateway.connected = False
        gateway.mode = None

        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False)
        )]

    elif name == "music_light_keys":
        # 支持多种 keys 格式：数组 ["31"] 或 字符串 "31" 或 "31,32,33"
        keys_arg = arguments.get("keys", [])
        if isinstance(keys_arg, str):
            keys = [k.strip() for k in keys_arg.split(",")]
        elif isinstance(keys_arg, list):
            keys = keys_arg
        else:
            keys = [str(keys_arg)]

        # 特殊处理：空数组表示关闭所有灯光，直接发送简化的参数
        if len(keys) == 0:
            light_args = {"keys": [], "brightness": 100}
            result = await gateway.send_command("light_keys", light_args)
            return [TextContent(
                type="text",
                text=json.dumps(result, ensure_ascii=False)
            )]

        # 支持 colors 数组或单个 color 值
        colors_arg = arguments.get("colors", arguments.get("color", 1))
        if isinstance(colors_arg, list):
            colors = colors_arg
        else:
            colors = [colors_arg] * len(keys)  # 单个颜色应用到所有键

        if gateway.mode == "script":
            result = await gateway.script_client.light_keys(keys, colors[0], arguments.get("brightness", 100))
        else:
            # 构建参数：支持每个键不同颜色
            light_args = {
                "keys": keys,
                "colors": colors,  # 新增 colors 数组
                "brightness": arguments.get("brightness", 100)
            }
            result = await gateway.send_command("light_keys", light_args)

        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False)
        )]

    elif name == "music_play_sequence":
        if gateway.mode == "script":
            result = await gateway.script_client.play_sequence(arguments["sequence"])
        elif gateway.mode == "mobile":
            result = await gateway.send_command("play_sequence", arguments)
        else:
            result = {"success": False, "error": "Web 模式暂不支持序列播放"}

        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False)
        )]

    elif name == "music_follow_mode":
        if gateway.mode == "script":
            result = await gateway.script_client.follow_mode(arguments["notes"], arguments.get("timeout", 30000))
        elif gateway.mode == "mobile":
            result = await gateway.send_command("follow_mode", arguments)
        else:
            result = {"success": False, "error": "Web 模式暂不支持跟弹模式"}

        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False)
        )]

    elif name == "music_listen":
        result = await gateway.send_command("listen", arguments)

        return [TextContent(
            type="text",
            text=json.dumps(result, ensure_ascii=False)
        )]

    elif name == "music_status":
        status = {
            "connected": gateway.connected,
            "mode": gateway.mode,
            "gateway_url": gateway.gateway_url,
            "ble_connected": gateway.ble_connected,  # 新增：BLE 连接状态
        }
        if gateway.mode == "mobile" and gateway.mobile_bridge:
            status["mobile_bridge_connected"] = gateway.mobile_bridge.is_connected
            status["ws_port"] = WS_PORT
        if gateway.mode == "web" and gateway.mobile_bridge:
            status["mobile_bridge_connected"] = gateway.mobile_bridge.is_connected
            status["ws_port"] = WS_PORT

        return [TextContent(
            type="text",
            text=json.dumps(status, ensure_ascii=False)
        )]

    elif name == "music_set_mode":
        MODE_MAP = {
            "skin":              0x00,
            "free":              0x01,
            "game":              0x02,
            "skin_config":       0x03,
            "drum":              0x04,
            "free_light":        0x05,
            "singing_advanced":  0x0D,
            "singing":           0x0E,
            "factory_test":      0x0F,
            "app_connect":       0x7F,
        }
        mode_name = arguments.get("mode")
        mode_val = MODE_MAP.get(mode_name)
        if mode_val is None:
            return [TextContent(type="text", text=json.dumps({"error": f"未知模式: {mode_name}"}, ensure_ascii=False))]
        result = await gateway.send_command("set_mode", {"mode": mode_val, "mode_name": mode_name})
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    elif name == "music_set_octave":
        octave = arguments.get("octave", 0)
        # 协议编码：-3=0x7D -2=0x7E -1=0x7F 0=0x00 1=0x01 2=0x02 3=0x03
        if octave < 0:
            octave_val = 0x80 + octave  # -1->0x7F, -2->0x7E, -3->0x7D
        else:
            octave_val = octave
        result = await gateway.send_command("set_octave", {"octave": octave, "octave_val": octave_val})
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    elif name == "music_set_bpm":
        bpm = arguments.get("bpm", 120)
        bpm = max(20, min(300, int(bpm)))
        # 协议：两字节合并，低7位在前，高7位在后
        low7  = bpm & 0x7F
        high7 = (bpm >> 7) & 0x7F
        result = await gateway.send_command("set_bpm", {"bpm": bpm, "low7": low7, "high7": high7})
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    elif name == "music_chord_light":
        chord_str = arguments.get("chord", "C")
        position  = arguments.get("position", 0)

        # 根音映射 -> 级别索引 (0x00~0x0B)
        ROOT_MAP = {
            "C": 0x00, "C#": 0x01, "Db": 0x01,
            "D": 0x02, "D#": 0x03, "Eb": 0x03,
            "E": 0x04,
            "F": 0x05, "F#": 0x06, "Gb": 0x06,
            "G": 0x07, "G#": 0x08, "Ab": 0x08,
            "A": 0x09, "A#": 0x0A, "Bb": 0x0A,
            "B": 0x0B,
        }
        # 和弦类型映射 -> 和弦尾序号
        SUFFIX_MAP = {
            "Maj": 0x00, "":    0x00,
            "Min": 0x01, "m":   0x01,
            "Maj7": 0x02,
            "m7":  0x03, "Min7": 0x03, "min7": 0x03,
            "7":   0x04,
            "Sus4": 0x05, "sus4": 0x05,
            "add9": 0x06, "Maj-add9": 0x06,
            "m7b5": 0x07, "m7-5": 0x07, "Min7b5": 0x07,
            "Aug":  0x08, "aug":  0x08,
            "Dim":  0x09, "dim":  0x09,
        }

        # 解析根音：先尝试2字符（C#/Db），再1字符
        root_str = ""
        suffix_str = ""
        for length in (2, 1):
            candidate = chord_str[:length]
            if candidate in ROOT_MAP:
                root_str   = candidate
                suffix_str = chord_str[length:]
                break

        if not root_str:
            return [TextContent(type="text", text=json.dumps(
                {"error": f"无法解析和弦根音: {chord_str}"}, ensure_ascii=False))]

        level_idx  = ROOT_MAP[root_str]
        suffix_idx = SUFFIX_MAP.get(suffix_str, 0x00)

        # 把位编码：默认64(0x40)，每级+/-1
        position_val = max(0, min(0x7F, 0x40 + position))

        # 和弦索引（键盘位置index）：使用根音对应的白键/黑键序号
        # 白键 C D E F G A B -> 0~6; 黑键用其前一个白键+1偏移，这里简化为level_idx
        chord_index = level_idx

        result = await gateway.send_command("chord_light", {
            "chord":        chord_str,
            "level_idx":    level_idx,
            "suffix_idx":   suffix_idx,
            "chord_index":  chord_index,
            "position_val": position_val,
        })
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    elif name == "music_query_version":
        # 协议 0x06：App -> 设备 询问版本，模版 F0 10 30 7F 7F 20 00 06 F7
        target = arguments.get("target", "all")
        # 映射 target 到设备类型/通道，前端根据此参数组装 SysEx
        TARGET_MAP = {
            "all":      {"device_type": 0x7F, "channel": 0x7F},  # 广播
            "box":      {"device_type": 0x10, "channel": 0x10},  # 音乐盒子
            "keyboard": {"device_type": 0x05, "channel": 0x7F},  # 36键广播
        }
        target_params = TARGET_MAP.get(target, TARGET_MAP["all"])
        result = await gateway.send_command("query_version", {
            "target": target,
            **target_params,
        })
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    elif name == "music_set_beat_type":
        BEAT_MAP = {"4/4": 0x00, "4/3": 0x01, "8/6": 0x02}
        beat = arguments.get("beat", "4/4")
        beat_val = BEAT_MAP.get(beat)
        if beat_val is None:
            return [TextContent(type="text", text=json.dumps(
                {"error": f"不支持的拍号: {beat}"}, ensure_ascii=False))]
        # 协议 0x20：盒子 -> 设备 下发拍型
        result = await gateway.send_command("set_beat_type", {"beat": beat, "beat_val": beat_val})
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    elif name == "music_set_skin":
        query = arguments.get("query", False)
        if query:
            # 协议 0x1A：查询已有皮肤
            result = await gateway.send_command("query_skin", {})
        else:
            skin_id = arguments.get("skin_id", 0)
            skin_id = max(0, min(127, int(skin_id)))
            # 协议 0x1C：皮肤设置，下发色盘号
            result = await gateway.send_command("set_skin", {"skin_id": skin_id})
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    elif name == "music_query_device":
        # 协议 0x01：主机 -> 设备 询问在线状态，模版 F0 7F 30 7F 7F 20 00 01 F7
        result = await gateway.send_command("query_device", {})
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    else:
        return [TextContent(
            type="text",
            text=json.dumps({"error": f"Unknown tool: {name}"})
        )]

async def main():
    """启动 MCP Server"""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
