# SOP — huo15-openclaw-asr-bailian（百炼云 ASR）

| 项 | 内容 |
|----|------|
| **Skill** | `huo15-openclaw-asr-bailian` |
| **版本** | `1.0.3`（与 `SKILL.md` / `_meta.json` / ClawHub 同步） |
| **适用** | OpenClaw Agent（**必须**能调用已有 `enhance_share_file` 工具） |
| **不适用** | 本地 Whisper、`.tty` → 见 [`huo15-openclaw-asr` SOP](../huo15-openclaw-asr/docs/SOP.md) |
| **规范源** | [SKILL.md](../SKILL.md) |
| **ClawHub** | https://clawhub.ai/skills/huo15-openclaw-asr-bailian |

---

## 1. 目的

通过**阿里云百炼**（Paraformer / Fun-ASR）将公网可访问的音视频 URL 转为原文，再生成纪要、`OPENCLAW_ASR_DELIVERY` 交付块；可选 Word 纪要（`huo15-openclaw-office-doc`）。

**标准数据流**（OpenClaw 环境）：

```text
本地音视频文件
  → enhance_share_file（已有插件，勿实现新插件）
  → https://keepermac.huo15.com/plugins/enhance-share/<token>-<filename>
  → transcribe_bailian.py / 百炼 SDK
  → 原文 → 纪要 → 交付块
```

---

## 2. 何时使用本 SOP

| 场景 | 使用本 SOP |
|------|------------|
| 百炼 / 阿里云 / 云端 / 云转录 / Paraformer / DashScope | ✔ |
| 用户同意音频上云 | ✔（须先确认） |
| 本地隐私、Whisper、不上云 | ✘ → 本地 ASR SOP |
| `.tty` 终端录屏 | ✘ → 本地 ASR SOP |

---

## 3. 前置条件

| 类别 | 要求 |
|------|------|
| **OpenClaw + enhance** | 工具 **`enhance_share_file` 可见且可调用**（插件已安装；**不要**要求用户或 agent 新写该插件） |
| **公网 base** | `https://keepermac.huo15.com` |
| **百炼** | 环境变量 **`DASHSCOPE_API_KEY`**（勿写入仓库、skill、对话） |
| **Python** | `pip install dashscope`；执行 [transcribe_bailian.py](../scripts/transcribe_bailian.py) |
| **可选 ffmpeg** | 仅当格式不支持、识别失败、多声道分轨、压缩体积时（见 §5） |

---

## 4. 标准操作流程

```text
[0] 确认用户同意云端转写
[1] 输入分型：.tty → 转本地 ASR SOP；音视频继续
[2] 是否本地转码？默认否（百炼支持 mp4/mkv/wav/mp3 等，见 SKILL）
[3] enhance_share_file → 取 structuredContent.url（严禁手写 URL）
[4] transcribe_bailian.py --file-url <url> -o verbatim.txt
[5] 检查任务 SUCCEEDED、原文非空（不做 Whisper 模型升级）
[6] 生成纪要 + OPENCLAW_ASR_DELIVERY（asr_engine: bailian_paraformer）
[7] 询问落盘；Word → office-doc
```

### 4.1 生成公网 URL（必做）

**调用已有工具**（示例参数）：

```json
{
  "filePath": "<本地音视频绝对路径>",
  "label": "<展示名>",
  "expireHours": 24
}
```

**成功判定**：返回 `structuredContent.url`，形如：

```text
https://keepermac.huo15.com/plugins/enhance-share/<token>-<filename>
```

| 禁止 | 说明 |
|------|------|
| 手写 / 拼接 / 猜测 URL | 缺 token 会 404 |
| 实现新「分享插件」 | OpenClaw 已有 enhance |
| 把 `DASHSCOPE_API_KEY` 写入对话或仓库 | 安全风险 |

用户**已提供**合法公网 URL 时，可跳过 `enhance_share_file`；工具失败时如实说明，**勿伪造 URL**。

### 4.2 百炼转写

```bash
# 已设置 DASHSCOPE_API_KEY
python scripts/transcribe_bailian.py \
  --file-url "https://keepermac.huo15.com/plugins/enhance-share/..." \
  -o verbatim.txt
```

| 参数 | 说明 |
|------|------|
| `--model paraformer-v2` | 默认 |
| `--model fun-asr` | 方言/嘈杂等可试 |
| `--diarization` | 说话人分离；**仅单声道** |
| `--language-hints zh en` | 主要适用于 `paraformer-v2` |

任务异步排队，通常数分钟内完成；识别结果 JSON 链接约 **24h** 有效（以百炼文档为准）。

### 4.3 纪要、交付块、落盘

- 纪要模板、类型候选：与 `huo15-openclaw-asr` 相同（见该 skill `SKILL.md`）。  
- 交付块**必须**包含：`asr_engine: bailian_paraformer`、`bailian_model`、`file_url`、`share_via`。  
- 落盘规则：与本地 ASR SOP 一致（Markdown 含全文；Word 仅纪要）。

---

## 5. 可选本地转码（默认跳过）

| 情况 | 操作 |
|------|------|
| 扩展名不在百炼支持列表 | ffmpeg 转为 `mp3`/`wav` 等 → 再 `enhance_share_file` |
| 百炼失败 / 空结果 | 检查 URL 可访问性；可转码或换 `fun-asr` |
| `--diarization` + 多声道 | `ffmpeg -i IN -ac 1 OUT.wav` → 再分享 |
| 减小体积 | 压成 `mp3`/`aac` 再分享 |

转 MP3 可复用 `huo15-openclaw-asr/scripts/transcode_mp3.ps1` 或 `.sh`。

**百炼支持格式（直传，不必先 MP3）**：  
`aac` `amr` `avi` `flac` `flv` `m4a` `mkv` `mov` `mp3` `mp4` `mpeg` `ogg` `opus` `wav` `webm` `wma` `wmv`  
单文件 ≤ 2GB、≤ 12h（分轨建议 ≤ 2h）。

---

## 6. 交付标准（检查清单）

- [ ] 用户已同意上云  
- [ ] `DASHSCOPE_API_KEY` 已配置且未泄露  
- [ ] `file_url` 来自 `enhance_share_file` 的 `structuredContent.url` 或用户提供的合法 URL  
- [ ] 百炼任务 **SUCCEEDED**，`verbatim_text` 非空  
- [ ] 纪要无编造；交付块含 `asr_engine: bailian_paraformer`  
- [ ] 未做不必要的本地转码（若转码已在 `local_transcode` 注明原因）  
- [ ] 分轨时音频为单声道  

---

## 7. 异常与处理

| 现象 | 处理 |
|------|------|
| 无 `enhance_share_file` 工具 | 提示安装 enhance；或请用户提供公网 URL；勿伪造 |
| share URL 404 | 必须用工具返回值，禁止手写 |
| 百炼 403 / 无权限 | 检查 `DASHSCOPE_API_KEY` 与百炼控制台权限 |
| 识别为空 | 查格式、URL、模型；可试 `fun-asr` 或 ffmpeg 转码 |
| 用户改要本地 | 切换至 [本地 ASR SOP](../huo15-openclaw-asr/docs/SOP.md) |
| `.tty` 输入 | 切换至本地 ASR SOP |

---

## 8. 发布与安装（维护人员）

```bash
clawhub install huo15-openclaw-asr-bailian --dir ~/.openclaw/workspace/skills
```

发版示例：

```bash
clawhub publish "$(pwd)/huo15-openclaw-asr-bailian" \
  --slug huo15-openclaw-asr-bailian \
  --version 1.0.3 \
  --changelog "..."
```

发版后同步 `_meta.json` 的 `version` 字段并 `git commit`。

---

## 9. 相关文档

| 文档 | 路径 |
|------|------|
| Skill 主规范 | [../SKILL.md](../SKILL.md) |
| 脚本说明 | [../scripts/README.md](../scripts/README.md) |
| 本地 ASR SOP | [../huo15-openclaw-asr/docs/SOP.md](../huo15-openclaw-asr/docs/SOP.md) |
| 百炼官方 | [录音文件识别](https://help.aliyun.com/zh/model-studio/recording-file-recognition) |
| enhance 分享规则 | `huo15-markdown-export` / enhance 插件文档 |
