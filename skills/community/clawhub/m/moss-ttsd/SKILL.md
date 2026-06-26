---
name: moss-ttsd
homepage: https://studio.mosi.cn
metadata:
  openclaw:
    requires:
      env: ["MOSI_TTS_API_KEY"]
    primaryEnv: "MOSI_TTS_API_KEY"
description: >
  MOSI Studio 多人对话合成（moss-ttsd）：将多个角色的对话文本合成为
  单段连续音频，多人声音自然交替。支持 1~5 个说话人。
  触发词：多说话人、多人对话、对话合成、多个角色、多种声音、多个人说话、
  "multi-speaker"、"dialogue synthesis"、"多人对话"。
  在飞书渠道：合成完成后优先发送语音气泡，不要发文件附件，
  不要只回文字说"已生成"。具体发送方法参见 mosi-tts skill 第 5 节。
---

# MOSS-TTSD 多人对话合成

将多个角色的对话文本合成为一段连续音频，多个声音自然交替出现。

支持 **1~5 个说话人**，使用 `[S1]`~`[S5]` 标签标记每位说话人。

---

## 快速开始

脚本路径：`~/.openclaw/skills/moss-ttsd/scripts/mosi_dialogue.sh`

```bash
# 2 个说话人
bash ~/.openclaw/skills/moss-ttsd/scripts/mosi_dialogue.sh \
  --text "[S1]你好，今天天气真好。[S2]是的，很适合出去走走。[S1]要不要一起去公园？" \
  --speakers "2001257729754140672,2002941772480647168" \
  --output ~/.openclaw/workspace/dialogue.wav

# 3 个说话人
bash ~/.openclaw/skills/moss-ttsd/scripts/mosi_dialogue.sh \
  --text "[S1]大家好！[S2]你好！[S3]欢迎！[S1]今天我们来聊聊AI。" \
  --speakers "ID_A,ID_B,ID_C"
```

---

## 文本格式

### 规则

- 使用 `[S1]`~`[S5]` 标签，**必须大写**
- 标签后**紧跟文本**，不加空格
- `[S1]` 对应 `--speakers` 中第 1 个 ID，`[S2]` 对应第 2 个，以此类推
- speakers 数量必须 >= 文本中用到的最大标签序号

### 正确示例

```
[S1]你好，今天天气真好。[S2]是的，很适合出去走走。[S3]我们去公园吧。
```

### 错误示例

| 错误写法 | 原因 |
|----------|------|
| `你好。你好。` | 没有标签 |
| `[s1]你好` | 标签小写 |
| `[S1] 你好` | 标签后有空格 |
| `[说话人1]你好` | 中文标签 |

---

## 音色选择

从以下公共音色中为各说话人挑选 voice ID：

| Voice ID | 名称 | 风格 |
|----------|------|------|
| 2001257729754140672 | 阿树 | 随性自然（男，默认） |
| 2001931510222950400 | 程述 | 播客理性（男） |
| 2002941772480647168 | 阿宁 | 温柔亲切（女） |
| 2020009311371005952 | 台湾女声 | 柔和疗愈（女） |
| 2020008594694475776 | 北京男声 | 清晰标准（男） |
| 2001898421836845056 | 子琪 | 活力明亮（女） |
| 2001910895478837248 | 小满 | 甜美开朗（女） |
| 2002991117984862208 | 梁子 | 专业沉稳（男） |

也可使用通过 `mosi-tts` skill 克隆得到的自定义 voice ID。

---

## 完整参数说明

```
--text,        -t  TEXT   对话文本（必填，含 [S1]~[S5] 标签）
--speakers,    -s  IDs    逗号分隔的 voice ID，1~5 个（必填）
                          例：--speakers "ID_A,ID_B,ID_C"
--output,      -o  PATH   输出 WAV 路径
                          （默认: ~/.openclaw/workspace/dialogue.wav）
--model,       -m  MODEL  模型名称（默认: moss-ttsd）
                          快照版本: moss-ttsd-20260320
--max-tokens       INT    最大生成 token 数（默认: 20000，上限: 40960）
                          长文本请调大，避免音频截断
--temperature      FLOAT  采样温度（默认: 1.1，不建议调整）
--top-p            FLOAT  核采样阈值（默认: 0.9）
--top-k            INT    Top-K 采样（默认: 50）
--rep-penalty      FLOAT  重复惩罚系数（默认: 1.1）
--audio-penalty    FLOAT  音频通道惩罚（默认: 1.5）
--meta-info               返回性能指标（延迟、token 消耗等）
--api-key,     -k  KEY    覆盖 MOSI_TTS_API_KEY 环境变量
```

---

## 环境准备

API Key 配置同 `mosi-tts` skill，读取 `MOSI_TTS_API_KEY` 环境变量。
详见 `mosi-tts` skill 的"环境准备"章节。

依赖：`curl`、`jq`、`base64`（均为标准 Unix 工具，通常已预装）

---

## 使用限制

| 项目 | 限制 |
|------|------|
| 说话人数 | 1~5 个 |
| 文本长度 | < 10000 字符（约 60 分钟音频） |
| 请求超时 | 30 分钟 |
| RPM | 5 次/分钟 |

---

## 常见问题

**Q：支持几个说话人？**
1~5 个，使用 `[S1]`~`[S5]` 标签。

**Q：长文本音频被截断怎么办？**
增大 `--max-tokens`，最大可设为 40960。

**Q：输出是什么格式？**
WAV（32kHz，16-bit，单声道）。在飞书渠道必须转成语音气泡发送，
参考 `mosi-tts` skill 第 5 节（飞书语音气泡）的 `mosi_feishu_voice.sh` 脚本：
```bash
bash ~/.openclaw/skills/mosi-tts/scripts/mosi_feishu_voice.sh \
  --wav ~/.openclaw/workspace/dialogue.wav \
  --chat-id "oc_xxxxxxxxxxxxxxxx"
```
