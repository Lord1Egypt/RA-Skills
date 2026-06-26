---
name: meeting-summary
description: "会议录音 → 结构化纪要。支持 Step ASR 转写、pyannote 说话人分割、声纹实名匹配、LLM 纪要生成，以及长录音 chunk 化增量处理。"
version: 2.3.0
tags:
  - meeting
  - asr
  - speaker-diarization
  - voiceprint
  - summary
  - transcription
  - step-asr
  - pyannote
---

# Meeting Summary Skill

把会议录音处理成**可交付的结构化纪要**。

**触发条件**：用户发送录音文件（mp3/wav/ogg/opus/m4a/flac）、说"总结会议/会议纪要/帮我总结录音"、说"注册声纹/记住我的声音"、说"谁在说话/识别说话人"、要求先快速出纪要再补精度、要求参考历史纪要风格。

**依赖**：StepFun API Key（[申请](https://platform.stepfun.com/interface-key)）、ffmpeg、Python (numpy, scipy, soundfile, onnxruntime)、可选 pyannote.audio（独立 venv + PyTorch + [HF](https://huggingface.co/) 账号）。详见 `{baseDir}/references/setup-guide.md`。

---

## 路由与执行方式

- **模型**：强制使用 `anthropic/claude-opus-4-6`（P0.5 优先级，不受默认模型影响）
- **执行方式**：main 收到录音后 **spawn subagent** 处理，不占主 session
- spawn 时传入：音频路径、用户 open_id、输出路径
- subagent 完成后 auto-announce 结果给 main → main 转发给用户
- **说话人确认仍由 main 完成**：subagent 输出说话人列表后，main 问用户确认，再决定是否用 `--speaker-map` 重跑

## ⚡ 快速参考：收到录音后做什么

> **这是整个 skill 最重要的部分。严格按顺序执行，不要跳步。**

```
步骤 0：spawn subagent（model: claude-opus-4-6）
步骤 1：环境检查（≤3 条命令，不通过就停）
步骤 2：跑主脚本（1 条命令）
步骤 3：检查输出（读 JSON 的 speakers + summary）
步骤 4：[回传 main] 说话人确认（≥2人时必须问用户）
步骤 5：交付纪要（展示 summary 字段的结构化内容）
```

### 步骤 1：环境检查

运行以下命令，**全部通过才继续**。任何一项失败 → 告诉用户缺什么 → 停止。

```bash
# 检查 ffmpeg
which ffmpeg

# 检查 StepFun API Key
test -f ~/.stepfun_api_key && echo "OK" || echo "MISSING"

# 检查 pyannote venv（可选，不影响基础流程）
PYANNOTE_PYTHON="${MEETING_SUMMARY_PYANNOTE_PYTHON:-$HOME/.venv-pyannote/bin/python}"
test -f "$PYANNOTE_PYTHON" && echo "pyannote: OK" || echo "pyannote: NOT AVAILABLE (will use energy-vad fallback)"
```

**禁止事项**：
- ❌ 不要尝试安装 pyannote、torch、numpy 或任何依赖
- ❌ 不要创建 venv
- ❌ 不要降级/升级包版本
- ❌ 不要修改脚本代码
- ❌ 不要修改环境变量

如果 pyannote 不可用，**直接使用 energy-vad 降级路径**，脚本已内置降级逻辑。

### 步骤 2：跑主脚本

**只用这一条命令**。不要拆步骤、不要手动调中间脚本。

```bash
cd {baseDir} && \
MEETING_SUMMARY_PYANNOTE_PYTHON="${MEETING_SUMMARY_PYANNOTE_PYTHON:-$HOME/.venv-pyannote/bin/python}" \
HF_TOKEN="$(cat ~/.huggingface_token 2>/dev/null || echo '')" \
python3 scripts/meeting-summarize.py \
  --audio "/path/to/recording.m4a" \
  --out /tmp/meeting-summary.json \
  --minutes-out /tmp/meeting-summary.md
```

**可选参数**（已知信息直接传入，不让模型猜）：
- `--num-speakers N`：已知参会人数
- `--speaker-map /path/to/map.json`：已知人名映射
- `--max-new-chunks 2`：快速模式（CPU 慢机器用）

**超时设置**：`timeout: 600`（10 分钟），`yieldMs: 300000`（5 分钟后台化）

### 步骤 3：检查输出

```bash
python3 -c "
import json
with open('/tmp/meeting-summary.json') as f:
    data = json.load(f)
# 说话人信息
for s in data.get('speakers', []):
    print(f'{s.get(\"display_name\", s.get(\"speaker\"))}: source={s.get(\"source\")}, segments={s.get(\"segment_count\")}')
print()
# 纪要概要
summary = data.get('summary', {})
print('参会人:', summary.get('participants', []))
print('概要:', summary.get('overview', []))
"
```

### 步骤 4：说话人确认（强制）

**规则：如果检测到 ≥2 个有效说话人（排除 segment_count ≤ 2 的噪声片段），必须先问用户确认身份。**

即使声纹匹配给出了名字（source=voiceprint），仍然要确认。声纹可能匹配错误。

**模板**：
```
检测到 X 位说话人：
- Speaker_A（YY 段发言）
- Speaker_B（ZZ 段发言）

请告诉我每位说话人对应谁？
```

用户确认后，可以：
- 方案 A：用 `--speaker-map` 重跑（更准确）
- 方案 B：直接在最终输出中替换名字（更快）

**绝对禁止**：不要猜测说话人身份映射，不要根据上下文推断"谁可能是谁"。

### 步骤 5：交付纪要

从 JSON 的 `summary` 字段提取结构化内容，按以下格式组织：

```
## 会议纪要：[标题]
**参会人**：[确认后的名字]
**时长**：XX 分 XX 秒

### 概要
[overview]

### 关键要点
1. ...

### 关键决定
- ...

### 行动项
- **[姓名]**：[任务]（[截止时间]）

### 风险与待定事项
- ⚠️ ...
```

**不要**：
- 不要展示 `summary_markdown` 字段的原文（它是脚本生成的单段落摘要，太简略）
- 不要把 JSON 原样甩给用户
- 不要忽略 `risks_or_open_items`

---

## 环境变量参考

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MEETING_SUMMARY_PYANNOTE_PYTHON` | `~/.venv-pyannote/bin/python` | pyannote venv 的 Python 路径 |
| `HF_TOKEN` | 空 | Hugging Face token（pyannote gated model 需要） |
| `STEPFUN_API_KEY` | 从 `~/.stepfun_api_key` 读取 | StepFun API Key |
| `MEETING_SUMMARY_LLM_MODEL` | `step-3.5-flash` | LLM 模型名 |
| `MEETING_SUMMARY_LLM_URL` | `https://api.stepfun.com/v1/chat/completions` | LLM API 地址 |
| `MEETING_SUMMARY_WORKSPACE` | `~/.openclaw/workspace` | 工作区根目录 |

---

## 声纹管理

```bash
# 注册声纹（建议 3-10 秒、清晰、单人语音）
python3 {baseDir}/scripts/voiceprint-manager.py enroll --name "张三" --audio /path/to/voice.wav

# 识别说话人
python3 {baseDir}/scripts/voiceprint-manager.py identify --audio /path/to/audio.wav --json

# 查看已注册声纹
python3 {baseDir}/scripts/voiceprint-manager.py list

# 删除声纹
python3 {baseDir}/scripts/voiceprint-manager.py delete --name "张三"
```

---

## 错误处理决策树

```
脚本执行失败？
├── ffmpeg 不存在 → 告诉用户安装 ffmpeg → 停止
├── StepFun API Key 缺失 → 告诉用户配置 → 停止
├── pyannote 加载失败 → 正常！脚本会自动降级到 energy-vad → 继续
├── ASR 超时 → 文件可能太大，建议用 --transcript-only 或分段 → 重试
├── LLM 调用失败 → 检查 StepFun API Key 余额 → 告诉用户
└── 其他 Python 错误 → 贴完整 traceback 告诉用户 → 停止
```

**核心原则：不要尝试修复环境问题。** 告诉用户哪里坏了，让用户或专门的安装流程去修。

---

## 缓存机制

缓存目录：`{baseDir}/../../cache/meeting-summary/`（即 `~/.openclaw/workspace/cache/meeting-summary/`）

- **ASR 缓存**：`<音频哈希>--asr--<语言>.json`
- **Diarization chunk 缓存**：`<音频哈希>--chunk-diarization--<说话人数>--<chunk序号>--<起始>--<结束>--<模式>.json`
- **合并 diarization 缓存**：`<音频哈希>--diarization--<说话人数>.json`

使用原则：
- 改 speaker-map 时，不重跑 ASR
- 改纪要风格时，不重跑 diarization
- 只补缺失 chunk，不整场重算
- **删除缓存时用精确文件名**，不要用 glob pattern 误删 chunk 缓存

---

## 判断与降级规则

### 说话人数判断
- 默认 LLM 估计值可能偏低，尤其是口语化、多人插话时
- 若转写里明显存在 3+ 角色切换，不要机械接受低估值
- 保守策略：用户未指定时，把估计值当参考，必要时提示"可能不止 X 人"

### 长录音处理
- 30+ 分钟音频：用 `--max-new-chunks 2` 先出结果
- 改人名、改格式时，优先复用缓存
- CPU 推理超过 10 分钟无输出 → 主动 poll 检查，不要死等

### 输出质量检查
- `summary_markdown` 只有一段话 → 用 `summary` 字典里的结构化字段组织纪要
- `speakers` 里有 Unknown 占比 > 50% → 提示用户声纹未注册或音频质量问题
- `action_items` 里的 owner 和实际说话人不匹配 → 向用户确认

---

## 已知限制

- pyannote CPU 推理慢，30 分钟音频可能需要很长时间
- 声纹匹配受音频质量、说话时长、噪音影响明显
- LLM 估人数在多人打断场景容易低估
- 未注册声纹时，`Unknown` 占比高是正常现象
- 不支持实时转写，仅离线处理
- **声纹匹配 ≠ 100% 准确**：即使 source=voiceprint，也可能匹配错误，必须人工确认

---

## 参考文件

- **完整安装 / 环境排障**：`{baseDir}/references/setup-guide.md`
