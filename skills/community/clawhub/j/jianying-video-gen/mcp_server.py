#!/usr/bin/env python3
"""
MCP Server for Jianying Video Generation
封装剪映 Seedance 2.0 视频生成功能
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

# MCP 协议常量
JSONRPC_VERSION = "2.0"

class JianyingMCPServer:
    def __init__(self):
        self.server_info = {
            "name": "jianying-video-gen",
            "version": "1.0.0"
        }
        
    def send_message(self, message: dict):
        """发送 JSON-RPC 消息"""
        json_str = json.dumps(message, ensure_ascii=False)
        print(json_str, flush=True)
        
    def send_error(self, id, code: int, message: str):
        """发送错误响应"""
        self.send_message({
            "jsonrpc": JSONRPC_VERSION,
            "id": id,
            "error": {
                "code": code,
                "message": message
            }
        })
        
    def send_result(self, id, result: dict):
        """发送成功响应"""
        self.send_message({
            "jsonrpc": JSONRPC_VERSION,
            "id": id,
            "result": result
        })
        
    def handle_initialize(self, id: int, params: dict):
        """处理初始化请求"""
        self.send_result(id, {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": self.server_info
        })
        
    def handle_tools_list(self, id: int):
        """返回可用工具列表"""
        tools = [
            {
                "name": "text_to_video",
                "description": "文生视频：根据文本描述生成AI视频",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "视频描述提示词"
                        },
                        "duration": {
                            "type": "string",
                            "enum": ["5s", "10s", "15s"],
                            "default": "10s",
                            "description": "视频时长"
                        },
                        "ratio": {
                            "type": "string",
                            "enum": ["横屏", "竖屏", "方屏"],
                            "default": "横屏",
                            "description": "画面比例"
                        },
                        "model": {
                            "type": "string",
                            "enum": ["Seedance 2.0", "Seedance 2.0 Fast"],
                            "default": "Seedance 2.0",
                            "description": "模型选择"
                        },
                        "output_dir": {
                            "type": "string",
                            "default": ".",
                            "description": "输出目录"
                        }
                    },
                    "required": ["prompt"]
                }
            },
            {
                "name": "image_to_video",
                "description": "图生视频：根据参考图片生成动画视频",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "image_path": {
                            "type": "string",
                            "description": "参考图片路径"
                        },
                        "prompt": {
                            "type": "string",
                            "description": "动画描述提示词"
                        },
                        "duration": {
                            "type": "string",
                            "enum": ["5s", "10s", "15s"],
                            "default": "10s"
                        },
                        "ratio": {
                            "type": "string",
                            "enum": ["横屏", "竖屏", "方屏"],
                            "default": "横屏"
                        },
                        "model": {
                            "type": "string",
                            "enum": ["Seedance 2.0", "Seedance 2.0 Fast"],
                            "default": "Seedance 2.0"
                        },
                        "output_dir": {
                            "type": "string",
                            "default": "."
                        }
                    },
                    "required": ["image_path", "prompt"]
                }
            },
            {
                "name": "video_to_video",
                "description": "参考视频生成：基于参考视频进行风格转换",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "video_path": {
                            "type": "string",
                            "description": "参考视频路径"
                        },
                        "prompt": {
                            "type": "string",
                            "description": "风格转换提示词"
                        },
                        "duration": {
                            "type": "string",
                            "enum": ["5s", "10s", "15s"],
                            "default": "10s"
                        },
                        "ratio": {
                            "type": "string",
                            "enum": ["横屏", "竖屏", "方屏"],
                            "default": "横屏"
                        },
                        "model": {
                            "type": "string",
                            "enum": ["Seedance 2.0", "Seedance 2.0 Fast"],
                            "default": "Seedance 2.0"
                        },
                        "output_dir": {
                            "type": "string",
                            "default": "."
                        }
                    },
                    "required": ["video_path", "prompt"]
                }
            },
            {
                "name": "get_credits_info",
                "description": "获取积分消耗信息",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        self.send_result(id, {"tools": tools})
        
    async def handle_tool_call(self, id: int, name: str, arguments: dict):
        """处理工具调用"""
        skill_dir = Path(__file__).parent
        cookies_path = skill_dir / "cookies.json"
        
        if not cookies_path.exists():
            self.send_error(id, -32600, f"未找到 cookies.json，请先配置登录凭证: {cookies_path}")
            return
            
        if name == "get_credits_info":
            self.send_result(id, {
                "content": [{
                    "type": "text",
                    "text": """## 剪映 Seedance 2.0 积分消耗

| 模型 | 5秒 | 10秒 | 15秒 |
|------|-----|------|------|
| Seedance 2.0 Fast | 15积分 | 30积分 | 45积分 |
| Seedance 2.0 | 25积分 | 50积分 | 75积分 |

请确保账户有足够积分后再生成视频。"""
                }]
            })
            return
            
        # 构建命令参数
        cmd = ["python", str(skill_dir / "scripts" / "jianying_worker.py")]
        cmd.extend(["--cookies", str(cookies_path)])
        
        # 确保输出目录存在
        default_output = r"D:\SQLMessage\AI_Videos"
        output_dir = arguments.get("output_dir", default_output)
        os.makedirs(output_dir, exist_ok=True)
        cmd.extend(["--output-dir", output_dir])
        
        if name == "text_to_video":
            cmd.extend([
                "--prompt", arguments["prompt"],
                "--duration", arguments.get("duration", "10s"),
                "--ratio", arguments.get("ratio", "横屏"),
                "--model", arguments.get("model", "Seedance 2.0")
            ])
        elif name == "image_to_video":
            cmd.extend([
                "--ref-image", arguments["image_path"],
                "--prompt", arguments["prompt"],
                "--duration", arguments.get("duration", "10s"),
                "--ratio", arguments.get("ratio", "横屏"),
                "--model", arguments.get("model", "Seedance 2.0")
            ])
        elif name == "video_to_video":
            cmd.extend([
                "--ref-video", arguments["video_path"],
                "--prompt", arguments["prompt"],
                "--duration", arguments.get("duration", "10s"),
                "--ratio", arguments.get("ratio", "横屏"),
                "--model", arguments.get("model", "Seedance 2.0")
            ])
        else:
            self.send_error(id, -32601, f"未知工具: {name}")
            return
            
        # 执行命令
        try:
            import subprocess
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5分钟超时
                cwd=str(skill_dir)
            )
            
            stdout = result.stdout
            stderr = result.stderr
            
            # 解析输出，查找视频下载信息
            video_path = None
            for line in stdout.split('\n'):
                if '下载完成' in line or '保存至' in line:
                    video_path = line.strip()
                    break
                    
            if result.returncode == 0:
                response_text = f"""✅ 视频生成任务已提交

**提示词**: {arguments.get('prompt')}
**时长**: {arguments.get('duration', '10s')}
**模型**: {arguments.get('model', 'Seedance 2.0')}

{video_path if video_path else '视频已生成，请检查输出目录'}

**输出目录**: {os.path.abspath(output_dir)}

**标准输出**:
```
{stdout[-1000:] if len(stdout) > 1000 else stdout}
```"""
                self.send_result(id, {
                    "content": [{
                        "type": "text",
                        "text": response_text
                    }]
                })
            else:
                self.send_error(id, -32603, f"视频生成失败:\n{stderr}\n{stdout}")
                
        except subprocess.TimeoutExpired:
            self.send_error(id, -32603, "视频生成超时（超过5分钟）")
        except Exception as e:
            self.send_error(id, -32603, f"执行错误: {str(e)}")
            
    async def run(self):
        """主循环"""
        while True:
            try:
                line = input()
                if not line:
                    continue
                    
                message = json.loads(line)
                method = message.get("method")
                msg_id = message.get("id")
                params = message.get("params", {})
                
                if method == "initialize":
                    self.handle_initialize(msg_id, params)
                elif method == "tools/list":
                    self.handle_tools_list(msg_id)
                elif method == "tools/call":
                    name = params.get("name")
                    arguments = params.get("arguments", {})
                    await self.handle_tool_call(msg_id, name, arguments)
                elif method == "notifications/initialized":
                    # 初始化完成通知，无需响应
                    pass
                else:
                    self.send_error(msg_id, -32601, f"未知方法: {method}")
                    
            except json.JSONDecodeError as e:
                self.send_error(None, -32700, f"JSON解析错误: {str(e)}")
            except EOFError:
                break
            except Exception as e:
                self.send_error(None, -32603, f"内部错误: {str(e)}")

if __name__ == "__main__":
    server = JianyingMCPServer()
    asyncio.run(server.run())
