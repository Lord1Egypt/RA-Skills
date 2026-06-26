---
name: glmv-caption
description:
  Generate captions (descriptions) for images, videos, and documents using ZhiPu
  GLM-V multimodal model series. Use this skill whenever the user wants to describe,
  caption, summarize, or interpret the content of images, videos, or files.
  Supports single/multiple inputs, URLs, local paths, base64 (images only), and
  optional structured JSON output via response_format + system prompt.
metadata:
  openclaw:
    requires:
      env:
        - ZHIPU_API_KEY
      bins:
        - python
    primaryEnv: ZHIPU_API_KEY
    emoji: "🖼️"
    homepage: https://github.com/zai-org/GLM-V/tree/main/skills/glmv-caption
---

# GLM-V Caption Skill

Generate captions for images, videos, and documents using the ZhiPu GLM-V multimodal model.

## When to Use

- Describe, caption, summarize, or interpret image/video/document content
- User mentions "describe this image", "caption", "summarize this video", "图片描述", "视频摘要", "文档解读", "看图说话"
- Extract visual or textual information from media files
- Compare multiple images
- User provides an image/video/file and asks what's in it

## Supported Input Types

| Type  | Formats                           | Max Size          | Max Count | Base64 | Local Path |
| ----- | --------------------------------- | ----------------- | --------- | ------ | ---------- |
| Image | jpg, png, jpeg                    | 5MB / 6000×6000px | 50        | ✅     | ✅ (→base64) |
| Video | mp4, mkv, mov                     | 200MB             | —         | ❌     | ✅ (→tunnel) |
| File  | pdf, docx, txt, xlsx, pptx, jsonl | —                 | 50        | ❌     | ✅ (→tunnel) |

**⚠️ file_url cannot mix with image_url or video_url in the same request.**

### How Local Paths Work for Videos & Files

The GLM-V API requires public HTTPS URLs for videos and files. When you provide a **local path**, the script automatically:

1. Creates a temporary directory and symlinks/copies the file into it (no other files are exposed)
2. Starts a local Python HTTP server on a random port
3. Launches `cloudflared tunnel` (trycloudflare.com quick tunnel) to expose the server to the public internet
4. Uses the resulting HTTPS URL for the API call
5. Cleans up (kills cloudflared, shuts down HTTP server, removes temp dir) when done

**Prerequisite:** `cloudflared` must be installed. Get it from [Cloudflare Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

## Resource Links

| Resource        | Link                                                                                                                              |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Get API Key** | [https://bigmodel.cn/usercenter/proj-mgmt/apikeys](https://bigmodel.cn/usercenter/proj-mgmt/apikeys)                              |
| **API Docs**    | [Chat Completions / 对话补全](https://docs.bigmodel.cn/api-reference/%E6%A8%A1%E5%9E%8B-api/%E5%AF%B9%E8%AF%9D%E8%A1%A5%E5%85%A8) |

## Prerequisites

### API Key Setup / API Key 配置（Required / 必需）

This script reads the key from the `ZHIPU_API_KEY` environment variable and shares it with other Zhipu skills.
脚本通过 `ZHIPU_API_KEY` 环境变量获取密钥，与其他智谱技能共用同一个 key。

**Get Key / 获取 Key：** Visit [Zhipu Open Platform API Keys / 智谱开放平台 API Keys](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) to create or copy your key.

**Setup options / 配置方式（任选一种）：**

1. **OpenClaw config (recommended) / OpenClaw 配置（推荐）：** Set in `openclaw.json` under `skills.entries.glmv-caption.env`:

   ```json
   "glmv-caption": { "enabled": true, "env": { "ZHIPU_API_KEY": "你的密钥" } }
   ```

2. **Shell environment variable / Shell 环境变量：** Add to `~/.zshrc`:

   ```bash
   export ZHIPU_API_KEY="你的密钥"
   ```

3. **.env file / .env 文件：** Create `.env` in this skill directory:
   ```
   ZHIPU_API_KEY=你的密钥
   ```

### Cloudflared (Required for local video/file paths)

Only needed when passing local file/video paths — not required if you only use URLs.

Install from [Cloudflare Downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/).

**⛔ MANDATORY: cloudflared 检查与安装流程 (YOU MUST FOLLOW THIS EXACTLY)⛔**

当你（AI agent）准备用 `--videos` 或 `--files` 传入 **本地文件路径** 时，**在执行脚本之前**，你必须先检查 cloudflared 是否已安装。按照以下流程操作：

#### Step 1: 检查 cloudflared 是否存在

```bash
# macOS / Linux
which cloudflared

# Windows
where cloudflared
```

如果命令返回了路径（如 `/usr/local/bin/cloudflared`），说明已安装，**直接执行脚本即可**。

如果命令报错（`not found` / `找不到`），进入 Step 2。

#### Step 2: 向用户说明情况并征求同意

**你必须先完整地向用户解释以下内容，然后询问用户是否同意下载安装。未经用户明确同意，不得自行下载。**

向用户展示的说明内容（原文照搬，不要精简）：

---

> **检测到系统未安装 cloudflared，本地视频/文件路径需要该工具才能使用。**
>
> **什么是 cloudflared？**
>
> cloudflared 是 Cloudflare 公司官方开源的命令行隧道工具（Apache 2.0 协议，GitHub 24000+ stars）。
> 它的功能是：在本机与 Cloudflare 全球边缘网络之间建立一条加密的临时隧道，将本地服务暴露为公网 HTTPS URL。
> 开源仓库地址：https://github.com/cloudflare/cloudflared
>
> **在本场景中的必要性：**
>
> 智谱 GLM-V API 要求视频和文件以公网 HTTPS URL 的形式传入（不支持本地上传）。
> 当你提供本地文件路径时，脚本的工作流程是：
>
> 1. 在本机启动一个临时 HTTP 服务器（**仅暴露你指定的那几个文件**，不会暴露其他目录）
> 2. 使用 cloudflared 建立一条临时隧道（通过 trycloudflare.com，**无需注册账号、无需登录**）
> 3. 获得一个形如 `https://xxx-xxx.trycloudflare.com/your-file.mp4` 的临时公网 URL
> 4. 将该 URL 传给 GLM-V API 完成调用
> 5. API 调用完成后，隧道和 HTTP 服务器**自动关闭**，临时文件清理
>
> **没有 cloudflared = 无法建立隧道 = 本地视频/文件路径不可用。**
>
> **安全说明：**
> - 隧道仅在脚本运行期间存在（通常几十秒到几分钟），脚本结束后立即关闭
> - 只暴露你明确指定的文件，**不会暴露整个目录或磁盘**
> - cloudflared 不会在后台常驻，不会开机自启
> - 不需要注册 Cloudflare 账号，不收集个人信息
> - 该工具被全球开发者广泛使用，Cloudflare 官方维护
>
> **下载链接：**
> - 官方下载页面（可手动选择版本）：https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
> - Windows x64: https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe
> - macOS Apple Silicon: https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-arm64.tgz
> - macOS Intel: https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz
> - Linux x64: https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
>
> **替代方案：如果你不想安装 cloudflared，可以直接传入远程 URL（如 `https://example.com/video.mp4`），则完全不需要安装任何东西。**

---

等待用户回复。根据用户回复执行对应操作：

- **用户同意安装** → 进入 Step 3
- **用户拒绝** → 提示用户改用远程 URL，或告知功能受限
- **用户要自行安装** → 提供下载链接，等待用户安装完成后再次执行

#### Step 3: 下载并安装 cloudflared

用户同意后，使用以下命令安装：

**macOS (Homebrew):**
```bash
brew install cloudflared
```

**Windows (推荐用 winget):**
```bash
winget install Cloudflare.cloudflared
```

**Linux (下载二进制):**
```bash
# x64
curl -Lo /usr/local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x /usr/local/bin/cloudflared
```

**其他方式:** 从 [官方下载页面](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) 手动下载，放到 PATH 中即可。

安装后用 `cloudflared version` 验证成功，然后执行脚本。

**⛔ MANDATORY RESTRICTIONS - DO NOT VIOLATE ⛔**

1. **ONLY use GLM-V API** — Execute the script `python scripts/glmv_caption.py`
2. **NEVER caption media yourself** — Do NOT try to describe content using built-in vision or any other method
3. **NEVER offer alternatives** — Do NOT suggest "I can try to describe it" or similar
4. **IF API fails** — Display the error message and STOP immediately
5. **NO fallback methods** — Do NOT attempt captioning any other way

### 📋 Output Display Rules (MANDATORY)

After running the script, **you must show the full raw output to the user exactly as returned**. Do not summarize, truncate, or only say "generated". Users need the original model output to evaluate quality.

- Image captioning: show the full caption text
- Multiple images: show each image result
- Video/files: show the full understanding result
- If token usage is included, you may optionally display it

## How to Use

### Caption an Image

```bash
python scripts/glmv_caption.py --images "https://example.com/photo.jpg"
python scripts/glmv_caption.py --images /path/to/photo.png
```

### Caption Multiple Images

```bash
python scripts/glmv_caption.py --images img1.jpg img2.png "https://example.com/img3.jpg"
```

### Caption a Video (URL or local path)

```bash
# Remote URL
python scripts/glmv_caption.py --videos "https://example.com/clip.mp4"

# Local file (auto-tunneled via cloudflare)
python scripts/glmv_caption.py --videos /path/to/local-video.mp4
```

### Caption a Document (URL or local path)

```bash
# Remote URL
python scripts/glmv_caption.py --files "https://example.com/report.pdf"

# Local file (auto-tunneled via cloudflare)
python scripts/glmv_caption.py --files /path/to/local-report.pdf

# Mix URLs and local paths
python scripts/glmv_caption.py --files "https://example.com/doc1.docx" /path/to/local-doc2.txt
```

### Custom Prompt

```bash
python scripts/glmv_caption.py --images photo.jpg --prompt "Describe the architecture style in detail"
```

### Save Result

```bash
python scripts/glmv_caption.py --images photo.jpg --output result.json
```

### Thinking Mode

```bash
python scripts/glmv_caption.py --images photo.jpg --thinking
```

### Structured Output / 结构化输出

```bash
python scripts/glmv_caption.py \
  --images photo.jpg \
  --response-format \
  --sys-prompt '请严格返回 JSON：{"summary":"string","objects":[{"name":"string","confidence":0.0}]}'
```

推荐做法：

- `--response-format` 仅在你显式传入时才启用结构化输出模式
- 该 flag 不传时，请求里**不会**自动带 `response_format`
- `--response-format` 不带值时，默认使用 `json_object`
- 建议总是配合 `--sys-prompt` 明确给出期望的 JSON 字段、类型和示例

## CLI Reference

```
python {baseDir}/scripts/glmv_caption.py (--images IMG [IMG...] | --videos VID [VID...] | --files FILE [FILE...]) [OPTIONS]
```

| Parameter             | Required | Description                                                                                  |
| --------------------- | -------- | -------------------------------------------------------------------------------------------- |
| `--images`, `-i`      | One of   | Image paths or URLs (supports multiple, base64 OK)                                           |
| `--videos`, `-v`      | One of   | Video paths or URLs (supports multiple, mp4/mkv/mov, local paths auto-tunneled)              |
| `--files`, `-f`       | One of   | Document paths or URLs (supports multiple, pdf/docx/txt/xlsx/pptx/jsonl, local paths auto-tunneled) |
| `--prompt`, `-p`      | No       | Custom prompt (default: "请详细描述这张图片的内容" / "Please describe this image in detail") |
| `--model`, `-m`       | No       | Model name (default: `glm-5v-turbo`)                                                         |
| `--temperature`, `-t` | No       | Sampling temperature 0-1 (default: 0.8)                                                      |
| `--top-p`             | No       | Nucleus sampling 0.01-1.0 (default: 0.6)                                                     |
| `--max-tokens`        | No       | Max output tokens (default: 1024, max 32768)                                                 |
| `--thinking`          | No       | Enable thinking/reasoning mode                                                               |
| `--response-format`   | No       | Enable structured output. If passed without a value, defaults to `json_object`; omitted = disabled |
| `--sys-prompt`        | No       | System prompt inserted before the user message; recommended for defining the expected JSON schema |
| `--output`, `-o`      | No       | Save result JSON to file                                                                     |
| `--pretty`            | No       | Pretty-print JSON output                                                                     |
| `--stream`            | No       | Enable streaming output                                                                      |

**Note:** `--images`, `--videos`, and `--files` are mutually exclusive per API limits.

## Structured Output Notes

Based on BigModel structured output guidance, enabling JSON mode is done by sending:

```json
{
  "response_format": {"type": "json_object"}
}
```

This skill exposes that capability through `--response-format`.

- `--response-format` present → request includes `response_format`
- `--response-format` absent → request behaves exactly like before
- `--sys-prompt` is passed as the request's `system` message
- Best practice: use `--sys-prompt` to define the exact JSON shape you want the model to return

Example:

```bash
python {baseDir}/scripts/glmv_caption.py \
  --files /path/to/report.pdf \
  --response-format json_object \
  --sys-prompt 'Return JSON only: {"title":"string","summary":"string","risks":["string"]}' \
  --pretty
```

## Response Format

```json
{
  "success": true,
  "caption": "A landscape photo showing a mountain range at sunset...",
  "usage": {
    "prompt_tokens": 128,
    "completion_tokens": 256,
    "total_tokens": 384
  }
}
```

Key fields:

- `success` — whether the request succeeded
- `caption` — the generated caption text
- `usage` — token usage statistics
- `warning` — present when content was blocked by safety review
- `error` — error details on failure

## Error Handling

**API key not configured:**

```
ZHIPU_API_KEY not configured. Get your API key at: https://bigmodel.cn/usercenter/proj-mgmt/apikeys
```

→ Show exact error to user, guide them to configure

**Authentication failed (401/403):** API key invalid/expired → reconfigure

**Rate limit (429):** Quota exhausted → inform user to wait

**File not found:** Local file missing → check path

**Content filtered:** `warning` field present → content blocked by safety review

**Tunnel failure (local paths only):**

```
Tunnel setup failed: cloudflared not found. Install it from: ...
```

→ Guide user to install cloudflared, or use a remote URL instead
