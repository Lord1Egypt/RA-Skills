# openclaw-plugin-dg-lab

[![npm version](https://img.shields.io/npm/v/openclaw-plugin-dg-lab.svg)](https://www.npmjs.com/package/openclaw-plugin-dg-lab)
![License](https://img.shields.io/npm/l/openclaw-plugin-dg-lab)
<br>
![Visitor Count](https://count.getloli.com/get/@openclaw-plugin-dg-lab?theme=rule34)

[中文](README.md) | [English](README_EN.md)

一个 [OpenClaw](https://github.com/openclaw/openclaw) 插件，用于通过 WebSocket 连接并控制 **郊狼 (DG-Lab) V3** 电刺激设备。

## ⚠️ 安全声明

**本插件控制电刺激设备，不当使用可能造成身体伤害。**

- **严禁在胸部、心脏、头部、颈部附近使用。** 请遵守 DG-Lab 官方安全指南。
- **务必从最低强度开始**，逐步增加。
- 如果您有心脏起搏器、心脏病、癫痫或正在怀孕，**请勿使用**。
- **请将设备远离儿童。** 这是成人用品。
- **您对使用本插件的方式承担全部责任。** 作者不对任何伤害、损坏或不当使用承担责任。
- **AI 情感引擎可以自动触发电刺激。** 在启用 `/dg_emotion on` 之前请充分了解这一点。
- **软件强度限制是便利功能，不是安全保障。** 请务必在 DG-Lab App 中设置安全的硬件上限。

**使用本插件即表示您知晓这些风险并同意负责任地使用。**

## 功能特性

- **原生集成** — 与 OpenClaw Gateway 共享进程，无需额外服务
- **二维码配对** — `/dg_qr` 生成二维码，DG-Lab App 扫码即连
- **AI 工具调用** — `dg_shock` 和 `dg_pulse_list` 让 AI 直接控制电刺激
- **情感引擎** — `/dg_emotion on` 开启后，AI 根据回复关键词自动触发刺激
- **强度限制** — `/dg_limit` 设置软上限；同时尊重 App 端设置的硬件上限
- **安全计时** — 连续使用 1 小时自动断电，强制休息 10 分钟
- **设备反馈同步** — 实时追踪 App 上报的设备强度和上限
- **WebSocket 心跳** — 保持连接存活
- **波形连续发送** — 超过 7 秒的波形自动分段无缝发送
- **自定义波形库** — 导入 `.pulses` / `.json5` / `.json` 文件，兼容 Coyote-Game-Hub 格式
- **V3 协议合规** — 使用官方频率压缩算法和消息长度限制

## 环境要求

- [OpenClaw](https://github.com/openclaw/openclaw) (2026.1+)
- 郊狼 Coyote V3 设备 + 官方 App
- 有公网 IP 的服务器（或端口转发）

## 安装


**一键安装（推荐）：**

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/FengYing1314/openclaw-plugin-dg-lab/main/install.sh)"
```

**通过 NPM 安装：**

```bash
openclaw plugins install openclaw-plugin-dg-lab
```
或者：
```bash
npm install -g openclaw-plugin-dg-lab
```

**开发者/源码安装方式:**

```bash
cd ~/.openclaw/workspace/plugins
git clone https://github.com/FengYing1314/openclaw-plugin-dg-lab.git
cd openclaw-plugin-dg-lab
npm install
npm run build

# 链接安装插件
cd ~/.openclaw/workspace
openclaw plugins install -l ./plugins/openclaw-plugin-dg-lab
```

## 配置

在 `~/.openclaw/openclaw.json` 中添加：

```json
{
  "plugins": {
    "entries": {
      "openclaw-plugin-dg-lab": {
        "enabled": true,
        "config": {
          "serverIp": "你的公网IP",
          "port": 18888,
          "limitIntensity": 40
        }
      }
    }
  }
}
```

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `serverIp` | string | `127.0.0.1` | 公网 IP 或域名，用于生成二维码 |
| `port` | number | `18888` | WebSocket 服务器端口 |
| `limitIntensity` | number | `40` | 默认强度软上限 (0-200) |

**注意：请在防火墙中放行 TCP 18888 端口！**

然后重启：

```bash
openclaw gateway restart
```

## 聊天指令

| 指令 | 说明 |
|------|------|
| `/dg_qr` | 生成连接二维码，用 App 扫码连接 |
| `/dg_emotion on/off` | 开启/关闭情感联动模式 |
| `/dg_limit <0-200>` | 设置强度软上限 |
| `/dg_test +5` | 手动测试强度调整 |
| `/dg_status` | 查看当前插件状态（连接数、强度、设备上限、队列） |
| `/dg_pulse list` | 列出所有已加载的波形 |
| `/dg_pulse load <文件>` | 导入 `.pulses` / `.json5` / `.json` 波形文件 |
| `/dg_pulse play <名称>` | 在 A 通道播放自定义波形 |
| `/dg_pulse delete <id>` | 删除波形 |

## AI 工具

### `dg_shock`

向连接的设备发送电刺激。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `strength` | number | ✓ | 强度增量 (正=增加, 负=减少, 0=归零) |
| `duration` | number | | 波形持续时间 ms (默认: 1000) |
| `waveform` | string | | `punish` / `tease` / `test` 或自定义波形名称 (默认: punish) |
| `channel` | string | | `A` / `B` (默认: A) |

### `dg_pulse_list`

列出所有可用波形（内置 + 自定义）。

### `dg_qr_generate`

生成配对二维码并返回文件路径。

## 内置波形

| 名称 | 频率 | 强度 | 描述 |
|------|------|------|------|
| `punish` | ~66Hz (15ms) | 100% 持续 | 高频持续刺激 |
| `tease` | ~5Hz (200ms) | 20-80% 正弦 | 低频呼吸式 |
| `test` | ~10Hz (100ms) | 50→90→50% | 中频短促测试 |

## 自定义波形（波形库）

将 `.pulses`、`.json5` 或 `.json` 文件放入插件的 `data/` 目录，启动时自动加载。

**支持的格式：**

1. **Coyote-Game-Hub 格式**（波形数组）：
```json5
[
  { id: 'abc123', name: '呼吸', pulseData: ['0A0A0A0A00000000', ...] }
]
```

2. **单个波形**: `{ name: "我的波形", pulseData: [...] }`

3. **纯 hex 数组**: `["0A0A0A0A64646464", ...]`

每个 hex 字符串 16 字符（8 字节）：4 字节频率（压缩值, 10-240）+ 4 字节强度（0-100）。每条代表 100ms（4 × 25ms 窗口）。

## 情感引擎

通过 `/dg_emotion on` 启用后，插件分析 AI 回复中的关键词：

| 类型 | 关键词（示例） | 增量 | 波形 |
|------|---------------|------|------|
| 惩罚 | 罚、教训、电击、punish、maximum | +15 | punish (3s) |
| 生气 | 生气、哼、不听话、angry、warning | +8 | punish (2s) |
| 安抚 | 乖、奖励、摸摸、good girl、reward | -3 | tease (5s) |

## 架构

```
DG-Lab App ←── WebSocket ──→ 插件 WS 服务器 ←── OpenClaw Gateway
                                    ↑
                           AI 调用 dg_shock
                          或情感引擎 Hook
```

1. 插件在配置端口启动 WebSocket 服务器
2. `/dg_qr` 生成二维码：`https://www.dungeon-lab.com/app-download.php#DGLAB-SOCKET#ws://IP:PORT/CONTROL_ID`
3. DG-Lab App 扫码后通过 WebSocket 连接
4. 插件发送强度指令 (`strength-CH+MODE+VALUE`) 和波形指令 (`pulse-CH:[hex...]`)
5. App 实时上报设备强度和上限 (`strength-A+B+limitA+limitB`)

## 安全机制

| 机制 | 说明 |
|------|------|
| **软件强度限制** | 所有强度变化钳制到 `min(插件上限, 设备上限)` |
| **设备上限同步** | 尊重 DG-Lab App 中设置的硬件上限 |
| **1小时自动休息** | 情感模式运行 60 分钟后强制冷却 10 分钟 |
| **优雅关闭** | 插件停止时所有通道归零 |
| **消息长度检查** | 超过 1950 字符（协议限制）的指令被丢弃 |
| **最大 7 秒/段** | 波形自动拆分为 ≤70 帧/次发送 |
| **心跳包** | 20 秒 WebSocket 保活 |
| **断连清理** | 设备断开时重置强度追踪 |

## 协议参考

本插件实现了 [DG-Lab V3 Socket 控制协议](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/socket/README.md)，并使用了 [V3 频率压缩算法](https://github.com/DG-LAB-OPENSOURCE/DG-LAB-OPENSOURCE/blob/main/coyote/extra/README.md)。

## 许可证

MIT © [FengYing](https://github.com/FengYing1314)
