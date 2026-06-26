# 辅助脚本说明

## `transcribe_bailian.py`

调用[百炼 Paraformer 录音文件识别](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-python-sdk)（`dashscope.audio.asr.Transcription`）。

**依赖**：Python 3.9+，`pip install dashscope`

**环境变量**：

| 变量 | 说明 |
|------|------|
| `DASHSCOPE_API_KEY` | 百炼 API Key（必填，勿写入仓库） |

**公网 URL（OpenClaw 标准）**：百炼不接受本地直传。在 OpenClaw 中由**已有** `enhance_share_file` 插件生成 URL（域名 `https://keepermac.huo15.com`），再将返回的 `structuredContent.url` 传入本脚本。本仓库**不实现**该插件。

```bash
# file-url 来自 enhance_share_file 的 structuredContent.url
python scripts/transcribe_bailian.py \
  --file-url "https://keepermac.huo15.com/plugins/enhance-share/<token>-meeting.mp4" \
  -o verbatim.txt
```

仅在格式不支持、识别失败、多声道分轨或需压缩时，才在本地 ffmpeg 处理后再走 `enhance_share_file`。
