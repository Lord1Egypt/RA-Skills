---
name: local-hub
description: 本地能力中心。通过 HTTP 调用本机麦克风、摄像头、Ollama、YOLO、Stable Diffusion、TTS/转写、通知、剪贴板、天气、白名单脚本等。当需要「验证是否有声音、拍一张照、用本地模型对话、文生图/图生图、朗读、系统通知、读剪贴板、看图描述、列模型、天气、跑脚本」时使用。需先确保 local_hub 服务已启动（workspace/local_hub/run.sh）。
metadata:
  openclaw:
    requires:
      bins: [curl]
---

# Local Hub — 本地能力中心

> **⚠️ 使用前必读**：本 skill 仅包含「调用说明」，不包含服务端代码。实际提供接口的 **local_hub 服务**需在本机单独部署并先启动。服务未启动时，所有 curl 调用会连接失败。
>
> **服务端代码与下载**：  
> - 仓库：<https://github.com/DamianLeeMoha/local_hub>  
> - 直接下载 zip：<https://github.com/DamianLeeMoha/local_hub/releases/download/v1.0.0/local_hub-v1.0.0.zip>  
> 解压后进入目录，创建虚拟环境并安装依赖（`python3 -m venv .venv-hub`、`source .venv-hub/bin/activate`、`pip install -r requirements.txt`），再执行 `./run.sh`。

**这是什么**：一个跑在你本机的 HTTP 服务（默认 `http://127.0.0.1:9000`），把麦克风、摄像头、Ollama、YOLO、Stable Diffusion 等统一成一组 API。Silas 通过 **exec + curl** 调用这些接口，不占用 OpenClaw 的 skill 检索维度，只是「多了一个可调的后端」。

**与其它 skills 的关系**：和 pptx、screen-capture 等**不在同一维度**——其它 skills 是「能力目录里的一条」；local_hub 是**底层服务**。本 skill 只是「调用说明」：告诉 Silas 何时、如何用 curl 去调这个服务。

---

## 前置条件

- **服务必须先启动**（用户或你在本机执行一次）：
  ```bash
  cd ~/.openclaw/workspace/local_hub && source .venv-hub/bin/activate && ./run.sh
  ```
- 健康检查（可选）：`curl -s http://127.0.0.1:9000/health` 返回 `{"status":"ok",...}` 表示服务在线。

---

## 何时使用

| 需求 | 用哪个接口 | 说明 |
|------|------------|------|
| 验证刚才播放的声音是否被听到 | `POST /audio/check` | 录约 1 秒，返回是否有声音（rms、has_sound） |
| 本机 TTS 朗读一段文字 | `POST /audio/tts` | JSON: text, voice(可选)；macOS say，返回音频 path |
| 音频转文字 | `POST /audio/transcribe` | 上传 file 或 form path；需设 TRANSCRIBE_SCRIPT |
| 拍一张摄像头画面 | `POST /camera/snapshot` | 返回保存的图片路径 |
| 对一张图做目标检测（YOLO） | `POST /vision/yolo` | 需上传图片（form），返回检测框等 |
| 用视觉模型描述图片 | `POST /vision/describe` | 上传图片，Ollama llava 等；query model=llava |
| 用本地 Ollama 对话（含 openclaw-distill） | `POST /llm/chat` | JSON body：model, prompt, system(可选) |
| 列出本机 Ollama 模型 | `GET /llm/models` | 返回 models 列表 |
| 文本向量（embedding） | `POST /llm/embed` | JSON: model, text |
| 文生图（Stable Diffusion） | `POST /image/txt2img` | 需本机 A1111 在 7860 端口 |
| 图生图（Stable Diffusion） | `POST /image/img2img` | 需提供 image_path + prompt |
| 系统通知（macOS） | `POST /notify` | JSON: title, body |
| 读/写剪贴板 | `GET /clipboard`、`POST /clipboard` | GET 读文本，POST JSON text 写 |
| 系统状态（音量、电池等） | `GET /system/status` | macOS 简要状态 |
| 天气 | `GET /weather` | query 可选城市 |
| 执行白名单脚本 | `POST /run/script` | JSON: name, params(可选)；需配置 RUN_SCRIPT_WHITELIST |

---

## 怎么用（curl 示例）

**基地址**：`http://127.0.0.1:9000`（若改过端口或主机，以实际为准）。

### 1. 检查是否有声音（播放后验证）

```bash
curl -s -X POST "http://127.0.0.1:9000/audio/check?duration=1&threshold=0.01"
```

返回示例：`{"rms":0.02,"threshold":0.01,"has_sound":true,"duration":1.0}`。看 `has_sound` 为 true/false。

### 2. 摄像头拍一张

```bash
curl -s -X POST http://127.0.0.1:9000/camera/snapshot
```

返回示例：`{"path":"/Users/.../local_hub/data/camera_1234567890.jpg"}`。后续可读该文件或交给 describe-image。

### 3. 本地 Ollama 对话

```bash
curl -s -X POST http://127.0.0.1:9000/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"model":"openclaw-distill","prompt":"你好","system":null}'
```

返回里有 `response` 字段即模型回复。可换 `qwen2.5:14b`、`llava` 等本机已有模型。

### 4. YOLO 检测（上传图片）

```bash
curl -s -X POST http://127.0.0.1:9000/vision/yolo \
  -F "file=@/path/to/image.jpg"
```

返回 `detections` 列表及保存路径。

### 5. 文生图（Stable Diffusion）

```bash
curl -s -X POST http://127.0.0.1:9000/image/txt2img \
  -H "Content-Type: application/json" \
  -d '{"prompt":"a cute robot, high quality","negative_prompt":"","steps":20,"width":512,"height":512}'
```

返回 `paths` 数组，为生成图在 `local_hub/data/` 下的路径。

### 6. 图生图

```bash
curl -s -X POST http://127.0.0.1:9000/image/img2img \
  -H "Content-Type: application/json" \
  -d '{"image_path":"/path/to/input.png","prompt":"make it cyberpunk","denoising_strength":0.6,"steps":20}'
```

### 7. TTS（朗读并保存音频）

```bash
curl -s -X POST http://127.0.0.1:9000/audio/tts \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","voice":"Tingting"}'
```

### 8. 系统通知

```bash
curl -s -X POST http://127.0.0.1:9000/notify \
  -H "Content-Type: application/json" \
  -d '{"title":"提醒","body":"会议 5 分钟后开始"}'
```

### 9. 剪贴板

```bash
# 读取
curl -s http://127.0.0.1:9000/clipboard
# 写入
curl -s -X POST http://127.0.0.1:9000/clipboard -H "Content-Type: application/json" -d '{"text":"复制这段"}'
```

### 10. 图片描述（Ollama 视觉模型）

```bash
curl -s -X POST "http://127.0.0.1:9000/vision/describe?model=llava" -F "file=@/path/to/image.jpg"
```

### 11. 列出 Ollama 模型 / 天气 / 系统状态

```bash
curl -s http://127.0.0.1:9000/llm/models
curl -s "http://127.0.0.1:9000/weather?query=Beijing"
curl -s http://127.0.0.1:9000/system/status
```

### 12. 执行白名单脚本（需先配置 RUN_SCRIPT_WHITELIST 与 scripts/ 下可执行文件）

```bash
curl -s -X POST http://127.0.0.1:9000/run/script \
  -H "Content-Type: application/json" \
  -d '{"name":"my_script","params":{"key":"value"}}'
```

---

## 执行方式

- 用 **exec** 调用上述 curl 命令；返回的 JSON 可解析后回复用户（例如「检测到有声音」「已生成图：…」）。
- 若服务未启动，curl 会报连接失败；此时可提示用户先启动 `local_hub/run.sh`，或说明「本地能力中心未就绪」。

---

## 依赖与端口

- **local_hub**：workspace 内 `local_hub/`，Python + FastAPI，默认端口 **9000**。
- **Ollama**：本机 11434，local_hub 会转调。
- **Stable Diffusion**：本机需有 A1111 类服务，默认 **7860**；可通过环境变量 `SD_BASE_URL` 改。

完整 API 与参数见：`workspace/local_hub/README.md`（若有）。
