---
name: openclaw-asr-bailian
displayName: 火一五媒体转写·百炼云 ASR
description: >-
  默认优先使用的云端转写 skill：百炼 Paraformer/Fun-ASR；本地文件经 OpenClaw 已有
  enhance_share_file 插件生成 https://keepermac.huo15.com 公网 URL 后提交百炼。
  触发：百炼、阿里云转写、云端 ASR、云转录、Paraformer、DashScope。本地 Whisper 请用
  huo15-openclaw-asr。
version: 1.0.3
user-invocable: true
homepage: https://cnb.cool/huo15/ai/huo15-skills
aliases:
  - 百炼转写
  - 阿里云转写
  - 云端 ASR
  - 云转录
  - Paraformer
  - DashScope 转写
  - 录音文件识别百炼
---

# OpenClaw 媒体转写 · 百炼云 ASR（默认云端路线）

> **定位**：凡用户需要**云端转写**、或明确说 **百炼 / 阿里云 / 不用本地 Whisper** 时，**优先加载并执行本 skill**，不要在本仓库的 `huo15-openclaw-asr` 里自行对接百炼 API。  
> **本地隐私转写**（Whisper / WhisperX / `.tty`）→ 使用 **`huo15-openclaw-asr`**。

本 skill 与 `huo15-openclaw-asr` **共用**纪要模板、OpenClaw 交付块结构、保存 Markdown/Word（office-doc）流程；差异仅在 **ASR 引擎固定为百炼**。

官方文档：[百炼 · 录音文件识别（Paraformer / Fun-ASR）](https://help.aliyun.com/zh/model-studio/recording-file-recognition) · [Python SDK](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-python-sdk)

---

## 默认策略

| 场景 | 使用 skill |
|------|------------|
| 云端 / 百炼 / 阿里云 ASR | **本 skill（默认）** |
| 本地、不上云、Whisper、`.tty` | `huo15-openclaw-asr` |
| 用户未说明 | 先问：本地还是云端；若倾向云端 → **本 skill** |

**上云前必须确认**：用户同意音频通过公网 URL 提交至阿里云百炼处理。

---

## 百炼 URL 约束与 OpenClaw 公网分享（必读）

百炼录音文件识别**只接受 HTTP/HTTPS 的音频 URL**，**不支持**本地路径直传、Base64 或二进制流（见[百炼文档](https://help.aliyun.com/zh/model-studio/recording-file-recognition)）。

在 **OpenClaw** 工作区中，标准链路为：

```text
本地音视频文件 → enhance_share_file（已有插件）→ 公网 URL → 百炼 API
```

| 项 | 说明 |
|----|------|
| **公网域名** | `https://keepermac.huo15.com`（bot 对外 base URL；分享链接形如 `https://keepermac.huo15.com/plugins/enhance-share/<token>-<filename>`） |
| **工具** | **`enhance_share_file`**（**OpenClaw 已安装**，来自 enhance 插件；**不要**在本 skill 内实现或要求用户新写该插件） |
| **agent 动作** | 对本地待转写文件**调用已有工具** `enhance_share_file`，从返回的 **`structuredContent.url`** 取真实公网 URL，再传给 `transcribe_bailian.py --file-url` 或等效百炼 SDK |
| **严禁** | 手写、拼接、猜测 share URL（缺 token 会 404）；与 `huo15-markdown-export` / enhance 规则一致 |

**调用示例（概念）**：

```json
enhance_share_file({
  "filePath": "<本地音视频绝对路径>",
  "label": "<展示名，如 会议录音>",
  "expireHours": 24
})
→ structuredContent.url = "https://keepermac.huo15.com/plugins/enhance-share/<token>-meeting.mp4"
```

若用户**已提供**可公网访问的 URL，可跳过 `enhance_share_file`；若工具不可用或失败，如实告知用户并降级（勿伪造 URL）。

---

## 百炼支持的音视频格式（不必先转 MP3）

百炼录音文件识别支持多种**音视频**格式（不限 MP3），见[官方说明](https://help.aliyun.com/zh/model-studio/recording-file-recognition)：

`aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`

- **mp4 / mkv / mov 等视频**可直接提交（服务端处理音轨），**默认无需**本地先抽音频再转 MP3。
- 单文件：**≤ 2GB、≤ 12 小时**；启用说话人分离时建议 **≤ 2 小时**。
- 格式变种众多，**不保证每一种都能识别成功**；若失败再考虑 [可选本地转码](#可选本地转码ffmpeg)。

---

## 总流程（决策树）

1. **确认引擎**：本 skill 固定 `asr_engine: bailian_paraformer`（默认模型 **`paraformer-v2`**）。
2. **识别输入**
   - `.tty` → 转交 **`huo15-openclaw-asr`** 的 [`.tty` 分支](../huo15-openclaw-asr/SKILL.md#tty终端录屏--会话日志)（百炼不做终端录屏解析）。
   - 音视频 → 继续本流程。
3. **是否本地转码（默认：否）**  
   - **默认**：源文件扩展名属于[格式列表](#百炼支持的音视频格式不必先转-mp3) → **不跑 ffmpeg**，直接进入步骤 4。  
   - **仅在下述情况**再本地转码（见 [可选本地转码](#可选本地转码ffmpeg)）：格式不在列表、百炼返回失败/无识别结果、需说话人分离但为多声道、或用户要求压缩体积。  
   - **不要**为「百炼只认 MP3」而习惯性转码。
4. **获得公网 URL（必做）**  
   - **OpenClaw 标准路径**：对步骤 2/3 得到的本地文件调用 **`enhance_share_file`**，使用返回的 **`structuredContent.url`**（域名 **`https://keepermac.huo15.com`**）。详见 [百炼 URL 约束与 OpenClaw 公网分享](#百炼-url-约束与-openclaw-公网分享必读)。  
   - 若用户已提供合法公网 URL，可跳过分享步骤。  
   - **勿**在 skill、脚本或对话中写入 `DASHSCOPE_API_KEY`；**勿**自行实现 enhance 插件。
5. **调用百炼转写**  
   使用本目录脚本（推荐）：

   ```bash
   pip install dashscope
   # 环境变量 DASHSCOPE_API_KEY 已设置
   python scripts/transcribe_bailian.py --file-url "https://keepermac.huo15.com/plugins/enhance-share/..." -o verbatim.txt
   ```

   可选参数：
   - `--model paraformer-v2`（默认；方言/嘈杂场景可改 **`fun-asr`**，见百炼文档选型）
   - `--diarization`：说话人分离（**仅单声道**；多声道需先 `ffmpeg -ac 1` 混成单声道，**不必**强行转成 MP3）
   - `--language-hints zh en`（**仅 `paraformer-v2`** 等支持的模型）

6. **结果检查（不做 Whisper 模型升级）**  
   - 任务状态须为 **SUCCEEDED**；原文非空。  
   - 若明显乱码、大段空结果 → 提示用户换模型（如 `fun-asr`）或检查 URL/格式，**不要**编造纪要。
7. **生成纪要 + OpenClaw 交付块**  
   严格基于原文；模板与 YAML 字段与 `huo15-openclaw-asr` 一致，但交付块须标明云端来源（见下节）。
8. **可选落盘**  
   与 `huo15-openclaw-asr` 相同：询问后保存 Markdown（原文+纪要+交付块）或 Word（仅纪要，调用 **`huo15-openclaw-office-doc`**）。

---

## 可选本地转码（ffmpeg）

仅在需要时使用；**百炼路线默认跳过本节。**

| 情况 | 建议 |
|------|------|
| 扩展名不在百炼支持列表 | 转为 `mp3` 或 `wav` 等支持格式后，再 `enhance_share_file` 分享 |
| 百炼任务失败或识别结果为空 | 先查 share URL 是否有效、百炼能否拉取；仍失败可试转码或换 `fun-asr` |
| `--diarization` 且源文件为多声道 | `ffmpeg -i INPUT -ac 1 OUTPUT.wav`（或其它支持格式），**不必** MP3 |
| 减小上传体积 | 可 `ffmpeg` 压成 `mp3`/`aac` 后再 `enhance_share_file` |

转 MP3 可复用 `huo15-openclaw-asr` 脚本（**仅当选择转 MP3 时**）：

- Windows：`../huo15-openclaw-asr/scripts/transcode_mp3.ps1`
- Unix：`../huo15-openclaw-asr/scripts/transcode_mp3.sh`

---

## 凭证与环境

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 百炼 API Key（[配置到环境变量](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-python-sdk)，禁止硬编码） |

任务为**异步**：提交后排队，通常数分钟内完成；结果 JSON 的下载链接 **24 小时有效**（以官方说明为准）。

---

## OpenClaw（龙虾）交付块

在 `huo15-openclaw-asr` 交付块基础上**增加/固定**下列字段：

```markdown
---OPENCLAW_ASR_DELIVERY---
version: 1
asr_engine: bailian_paraformer
bailian_model: "<paraformer-v2 | fun-asr | ...>"
source_kind: audio_video
source_path: "<原始文件路径或标识>"
file_url: "<enhance_share_file 返回的 structuredContent.url，或用户提供的公网 URL>"
share_via: "enhance_share_file | user_provided_url"
local_transcode: "<none | 说明：如 ffmpeg 混单声道 wav；默认 none 表示直传原文件>"
language_guess: "<zh | en | mixed | unknown>"
type_candidates:
  - code: "<meeting|interview|...>"
    confidence: <0.0-1.0>
    reason: "<一句理由>"
verbatim_text: |
  <原文全文>
summary_markdown: |
  <纪要全文>
notes_for_openclaw: |
  云端百炼转写；模型=<模型名>；用户已确认上云；<其它不确定性>
---END_OPENCLAW_ASR_DELIVERY---
```

纪要模板、类型候选表：见 [huo15-openclaw-asr · 纪要模板](../huo15-openclaw-asr/SKILL.md#纪要模板)。

---

## 保存 Word（纪要）

与 `huo15-openclaw-asr` 相同：调用 **`huo15-openclaw-office-doc`** 的 `create-word-doc.py`，`--doc-format 会议纪要`。详见 [选项 B：保存为 Word](../huo15-openclaw-asr/SKILL.md#选项-b保存为-word仅纪要)。

---

## 与 `huo15-openclaw-asr` 的分工小结

| 能力 | 本 skill | huo15-openclaw-asr |
|------|----------|-------------------|
| 百炼 Paraformer / Fun-ASR | ✔ 默认 | 不实现，仅指向本 skill |
| 公网 URL（enhance_share_file） | ✔ 标准 | ✘ |
| Whisper / WhisperX | ✘ | ✔ 默认 |
| `.tty` 终端日志 | ✘ | ✔ |
| 纪要 / 交付块 / 落盘 | ✔（复用约定） | ✔ |

---

## 自检清单

- [ ] 已确认用户同意**云端**转写。
- [ ] 已配置 `DASHSCOPE_API_KEY`（未泄露到仓库或对话）。
- [ ] 已通过 **`enhance_share_file`** 取得公网 URL（`https://keepermac.huo15.com/...`），或用户已提供合法 URL；**未手写/拼接** share 链接。
- [ ] 音频 URL 已提交百炼；**默认未做不必要的本地转码**。
- [ ] 若曾本地转码：已在 `local_transcode` / `notes_for_openclaw` 中说明原因（格式、分轨、压缩等）。
- [ ] 已用 `transcribe_bailian.py` 或等效 SDK 调用，任务 **SUCCEEDED**，原文非空。
- [ ] 若启用说话人分离：音频为**单声道**。
- [ ] 纪要严格来源于原文；已输出带 `asr_engine: bailian_paraformer` 的交付块。
- [ ] 若保存 Word：已走 `huo15-openclaw-office-doc`。

---

## 附加资源

- **标准操作（SOP）**：[docs/SOP.md](docs/SOP.md)
- 脚本说明：[scripts/README.md](scripts/README.md)
