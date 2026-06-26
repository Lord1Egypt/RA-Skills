---
name: mimo-tts-proxy
description: |
  小米 TTS 代理技能。将 OpenAI TTS API 格式转换为小米大模型平台 TTS API（api.xiaomimimo.com），支持 Opus/MP3/AAC/FLAC/WAV/PCM 六种格式的本地转码。
  当需要为机器人添加语音回复能力、或配置 TTS 语音合成时使用此技能。
  也适用于需要搭建本地 TTS 代理服务的场景。
metadata:
  openclaw:
    emoji: 🔊
    requires:
      bins: ["ffmpeg"]
      config: ["messages.tts"]
    install:
      - id: ffmpeg
        kind: system
        label: "FFmpeg (系统自带，检查: ffmpeg -version)"
---

# 小米 TTS Proxy

## 音色与风格控制

### 预置音色（`voice` 参数）

| 音色 | voice 参数值 |
|------|------------|
| MiMo-默认 | `mimo_default` |
| MiMo-中文女声 | `default_zh` |
| MiMo-英文女声 | `default_en` |

### 风格控制（`input` 文本开头加 `<style>` 标签）

将 `<style>风格</style>` 置于待合成文本开头，小米的 TTS 会识别并应用对应风格：

| 风格 | 示例 |
|------|------|
| 语速控制 | `<style>变快</style>` / `<style>变慢</style>` |
| 情绪变化 | `<style>开心</style>` / `<style>悲伤</style>` / `<style>生气</style>` |
| 角色扮演 | `<style>孙悟空</style>` / `<style>林黛玉</style>` |
| 风格变化 | `<style>悄悄话</style>` / `<style>夹子音</style>` / `<style>台湾腔</style>` |
| 方言 | `<style>东北话</style>` / `<style>四川话</style>` / `<style>粤语</style>` |
| 唱歌 | `<style>唱歌</style>`（必须放在最开头） |

**样例**：
```bash
curl -X POST http://127.0.0.1:18899/audio/speech \
  -d '{"input":"<style>东北话</style>哎呀妈呀，这天儿也太冷了！","voice":"mimo_default","response_format":"opus"}'
```

---

## 技能简介

本技能在本地启动一个 HTTP 代理服务（默认 `:18899`），将 OpenAI TTS API 格式请求转换为小米大模型平台 TTS API（`api.xiaomimimo.com`），并支持 FFmpeg 硬件转码为 Opus/MP3/AAC/FLAC/WAV/PCM 等格式。

**适用场景**：为 OpenClaw 配置语音合成、搭建通用 TTS 代理服务。

---

## 使用前提

- FFmpeg 已安装（`ffmpeg -version` 确认）
- 拥有小米大模型平台 API Key
- 建议 Node.js ≥ 18（代理使用原生 fetch）

---

## 首次配置（交互式）

首次使用本技能时，需要完成以下配置步骤：

### 步骤 1：配置环境变量

创建或更新 `~/.openclaw/tts-proxy.env` 文件，内容如下：

```bash
# 小米 TTS API 配置
MIMO_TTS_BASE=https://api.xiaomimimo.com
MIMO_TTS_KEY=你的_小米API_Key
TTS_PROXY_PORT=18899
```

> **注意**：`MIMO_TTS_BASE` 不要包含 `/v1` 后缀，代理会自动添加。
> 如果使用代理转发小米 API（解决国内访问问题），在 `MIMO_TTS_BASE` 中填写代理地址。

### 步骤 2：安装 Systemd 服务（可选但推荐）

代理通过 systemd 服务运行，可实现开机自启和自动管理。

复制服务单元文件并注册：

```bash
sudo cp mimo-tts-proxy.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now mimo-tts-proxy.service
sudo systemctl status mimo-tts-proxy.service
```

### 步骤 3：验证运行状态

```bash
curl http://127.0.0.1:18899/health
# 应返回：{"status":"ok","provider":"mimo-v2-tts"}
```

### 步骤 4：配置 OpenClaw TTS

在 OpenClaw 配置中（`~/.openclaw/openclaw.json`），找到或添加 `messages.tts` 节点：

```json
{
  "messages": {
    "tts": {
      "auto": "inbound",
      "provider": "openai",
      "providers": {
        "openai": {
          "baseUrl": "http://127.0.0.1:18899",
          "apiKey": "not-needed",
          "model": "tts-1",  # 占位值，代理实际固定使用 mimo-v2-tts
          "voice": "mimo_default"
        }
      }
    }
  }
}
```

配置后重启 OpenClaw Gateway 使配置生效。

---

## 服务管理命令

| 操作 | 命令 |
|------|------|
| 查看状态 | `systemctl status mimo-tts-proxy.service` |
| 查看日志 | `journalctl -u mimo-tts-proxy.service -f` |
| 重启服务 | `systemctl restart mimo-tts-proxy.service` |
| 停止服务 | `systemctl stop mimo-tts-proxy.service` |
| 健康检查 | `curl http://127.0.0.1:18899/health` |

---

## API 端点

### `POST /audio/speech`

与 OpenAI TTS API 格式兼容：

```bash
curl -X POST http://127.0.0.1:18899/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "<style>开心</style>你好，这是中文语音测试",
    "voice": "mimo_default",
    "response_format": "opus"
  }' \
  -o output.opus
```

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `input` | string | 必填 | 要合成的文本 |
| `voice` | string | `mimo_default` | 音色：`mimo_default`（默认）/`default_zh`（中文女声）/`default_en`（英文女声） |
| `model` | string | `tts-1` | 占位值，代理固定使用 `mimo-v2-tts` |
| `response_format` | string | `mp3` | 输出格式：`opus`/`mp3`/`aac`/`flac`/`wav`/`pcm`/`pcm16` |

**支持的输出格式**：

| 格式 | MIME 类型 | 说明 |
|------|-----------|------|
| `opus` | audio/opus | ✅ 推荐，飞书等平台支持 |
| `mp3` | audio/mpeg | FFmpeg 转码 |
| `aac` | audio/aac | FFmpeg 转码 |
| `flac` | audio/flac | FFmpeg 转码 |
| `wav` | audio/wav | 小米 API 原生输出 |
| `pcm` / `pcm16` | audio/L16 | PCM 16bit 24kHz 原始音频 |

### `GET /health`

健康检查：

```bash
curl http://127.0.0.1:18899/health
# → {"status":"ok","provider":"mimo-v2-tts"}
```

---

## 故障排查

### 健康检查失败

```bash
systemctl status mimo-tts-proxy.service
journalctl -u mimo-tts-proxy.service -n 50 --no-pager
```

### 返回 404 或 502

1. 确认 `MIMO_TTS_BASE` 不带 `/v1` 后缀（代理自动添加）
2. 确认 `MIMO_TTS_KEY` 正确且有 TTS 配额
3. 检查上游小米 API 是否可达：
   ```bash
   curl -X POST https://api.xiaomimimo.com/v1/chat/completions \
     -H "Content-Type: application/json" \
     -H "api-key: 你的Key" \
     -d '{"model":"mimo-v2-tts","messages":[{"role":"assistant","content":"test"}],"audio":{"format":"wav","voice":"mimo_default"}}'
   ```

### 音频格式问题

如果播放无声，确认使用 `opus` 格式（飞书/微信等平台的要求）。`wav` 格式在某些平台可能不兼容。

### 配额耗尽

`{"error":{"code":"429","message":"monthly quota exhausted"}}`

小米 TTS 月度配额用完，需要到小米大模型平台购买增量包或等待下月重置。

---

## 文件位置

| 文件 | 说明 |
|------|------|
| `~/.openclaw/tts-proxy.mjs` | 代理脚本 |
| `~/.openclaw/tts-proxy.env` | 环境变量配置 |
| `/etc/systemd/system/mimo-tts-proxy.service` | systemd 服务单元 |
| `http://127.0.0.1:18899` | 代理监听地址 |
