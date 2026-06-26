---
name: partykeys_midi
description: "Control PartyKeys MIDI keyboard via WebSocket - connect device, light up keys with 12 colors, listen to playing, play sequences, and follow mode for music teaching."
metadata: {"openclaw": {"requires": {"bins": ["python3"]}, "os": ["darwin", "linux"]}}
---

# PartyKeys MIDI 键盘控制

通过 MCP 控制 PartyKeys MIDI 键盘（音乐密码）的 LED 灯光和监听弹奏。

## 统一架构

**手机 App 和浏览器页面使用同一套通信协议**，都连接 WebSocket 端口 18790：

```
                MCP Server (端口 18790)
                     /       \
                    /         \
      WebSocket    /           \    WebSocket
                  ↓             ↓
            ┌──────────┐  ┌──────────┐
            │ 手机 App  │  │ 浏览器页面 │
            │          │  │          │
            │   BLE    │  │   Web BT │
            └────┬─────┘  └────┬─────┘
                 │             │
                 └──────┬──────┘
                        ↓
                    MIDI 键盘
```

**单一服务**：调用 `music_connect()` 时，MCP 只启动 WebSocket 服务（端口 18790）。

## 安装

首次使用前运行安装脚本：

```bash
bash {baseDir}/scripts/setup.sh
```

## 连接设备

连接键盘前，**先询问用户选择连接方式**：

> 请选择 MIDI 键盘的连接方式：
>
> - **🌐 浏览器连接** — 在 Chrome/Edge 浏览器中连接设备（推荐本机使用）
> - **📱 手机 App** — 通过手机 App 桥接蓝牙（推荐云端/远程使用）
>
> 两种连接方式使用同一套协议，可任选其一。

### 方式 1：浏览器连接（web）

**使用流程**：
1. 用户打开 `partykeys-bridge-web/standalone.html` 网页
2. 输入 WebSocket 地址：`ws://<本机 IP>:18790/ws`
3. 点击「连接服务器」，然后点击「连接设备」
4. 选择并连接 MIDI 键盘

**适用系统**：所有系统（Windows、Linux、macOS）

**安全上下文（必读）**：Web Bluetooth 只在浏览器的「安全上下文」里可用，即 **`https://` 或本机的 `http://localhost` / `http://127.0.0.1`**。远程 `http://IP` 无法使用 Web Bluetooth，需改用 **手机 App**。

### 方式 2：手机 App（mobile）

**使用流程**：
1. 用户在手机下载 **PartyKeys Bridge** App（Android/iOS）
2. 打开 App，输入服务器地址 `ws://<服务器 IP>:18790/ws`
3. 在 App 中扫描并连接 MIDI 键盘
4. 保持 App 在前台

**适用系统**：所有系统（Windows、Linux、macOS、云端服务器）

## 可用工具

### music_connect
连接 MIDI 键盘设备。
- `mode`: `mobile` 或 `web`（可选，不传时让用户选择）

### music_disconnect
断开设备连接。

### music_light_keys
点亮指定按键的 LED 灯。
- `keys`: 音符列表（必填），如 `["C4", "E4", "G4"]` 或 `["3c", "40", "43"]` 或 `"3c,40,43"`
- `colors`: 颜色数组，每个键对应一个颜色（可选），如 `[1, 3, 5]`
- `color`: 单个颜色值，所有键共用（可选，已废弃，推荐使用 `colors`）

### 12 种颜色

| 值 | 颜色 | 值 | 颜色 |
|----|------|----|------|
| 0 | 关闭（熄灭） | 7 | 绿色 |
| 1 | 红色 | 8 | 青绿 |
| 2 | 橙红 | 9 | 青色 |
| 3 | 橙色 | 10 | 蓝色 |
| 4 | 黄橙 | 11 | 蓝紫 |
| 5 | 黄色 | 12 | 紫色 |
| 6 | 黄绿 | | |

### music_listen
监听用户弹奏输入。
- `timeout`: 超时时间，毫秒（默认 5000）
- `mode`: `"single"` 或 `"continuous"`

### music_play_sequence
播放音符序列。
- `sequence`: 音符序列数组，每个元素含 `keys` 和 `delay`（毫秒）

### music_follow_mode
跟弹模式。
- `notes`: 音符序列
- `timeout`: 每个音符超时，毫秒（默认 30000）

### music_status
获取硬件连接状态。

### music_set_mode
切换键盘/设备工作模式。
- `mode`: `skin` / `free` / `game` / `skin_config` / `drum` / `free_light` / `singing` / `singing_advanced` / `app_connect`

### music_set_octave
设置键盘音区（8度偏移）。
- `octave`: 整数，-3~3，0 为默认音区

### music_set_bpm
设置节拍速度。
- `bpm`: 整数，20~300

### music_set_beat_type
设置节拍类型（拍号）。
- `beat`: `"4/4"` / `"4/3"` / `"8/6"`

### music_chord_light
根据和弦名称点亮键盘对应按键（教学用）。
- `chord`: 和弦名称，格式：根音+和弦类型，如 `C`、`Dm`、`G7`、`FMaj7`、`Am7`
- `position`: 把位偏移，0 为默认，正数升高，负数降低

### music_set_skin
设置键盘/设备皮肤（色盘）。
- `skin_id`: 色盘编号，0~127
- `query`: 若为 true 则仅查询已有皮肤列表

### music_query_device
查询设备在线状态，获取当前已连接的设备列表。

### music_query_version
查询设备固件版本信息。
- `target`: `"all"` / `"box"` / `"keyboard"`

## 示例

**浏览器连接模式**:
```
music_connect(mode="web")
music_light_keys(keys=["3c", "40", "43"], colors=[1, 3, 5])
music_disconnect()
```

**手机中转模式**:
```
music_connect(mode="mobile")
music_light_keys(keys=["C4", "E4", "G4"], color="blue")
music_disconnect()
```

**12 色渐变**:
```
# 点亮 12 个键，每个键不同颜色
music_light_keys(
  keys=["30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "3a", "3b"],
  colors=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
)
```

**关闭所有灯光**:
```
music_light_keys(keys=[])
```
