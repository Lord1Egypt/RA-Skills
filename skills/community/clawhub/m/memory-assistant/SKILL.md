---
name: memory-assistant
description: Helps users remember where they put things and schedule voice reminders. Use when the user says "记一下"/"记一下"/"提醒我", records item locations (e.g. keys, passport), or asks for time-based reminders with voice notification. Integrates SenseAudio TTS for spoken alerts.
---

# 帮记助手（健忘症语音提醒）

针对“健忘症”的帮记助手：支持**随手放的东西**快速录入与查询、**日程/约会**定时提醒，并通过 **SenseAudio** 合成语音进行语音提醒。

## 前置条件

- 环境变量中配置 `SENSEAUDIO_API_KEY`（<https://senseaudio.cn/platform/api-key>）。
- 使用语音脚本需 Python 3.8+，并安装：`pip install requests`。播放时 macOS 使用 `afplay`，Windows 使用系统默认播放器，Linux 使用 `paplay`/`aplay`/`ffplay`。

## 核心场景

### 场景一：随手放的东西

用户用自然语言快速录入物品与位置，例如：

- 「记一下，我把备用电池放在电视柜左侧第二个抽屉里了。」
- 「记一下，护照在书房第二个书架最上层。」
- 「备用钥匙放在玄关鞋柜上面。」

**处理流程：**

1. 从用户输入中抽取：**物品**（如：备用电池、护照、备用钥匙）、**位置**（如：电视柜左侧第二个抽屉）。
2. 将记录写入持久化存储（如 JSON 文件或数据库），格式见 [reference.md](reference.md)。
3. 回复确认并支持后续用「某某放哪儿了」查询并朗读位置。

### 场景二：定时提醒（含提前提醒）

用户说明时间与事项，并要求提前提醒，例如：

- 「下午三点要开会，记得提前提醒我。」
- 「六点钟和王先生约在和平饭店见面，提前半小时提醒我。」

**处理流程：**

1. 从用户输入中解析：**提醒时间**、**事项描述**、**提前时长**（若未说则用默认，如 15 分钟）。
2. 将提醒写入提醒列表，并计算**实际播报时间** = 提醒时间 − 提前时长。
3. 到播报时间时，用 SenseAudio TTS 将提醒内容合成为语音并播放（或保存为音频文件供播放）。

## 数据模型

- **物品位置记录**：`{ "item": "备用电池", "location": "电视柜左侧第二个抽屉", "created_at": "ISO8601" }`
- **定时提醒**：`{ "at": "ISO8601", "event": "下午三点开会", "advance_minutes": 30, "created_at": "ISO8601" }`

完整字段与存储路径见 [reference.md](reference.md)。

## 语音提醒（SenseAudio TTS）

所有需要“读出来”的提醒（如：到点提醒、查询到的位置）均通过 SenseAudio 文本转语音 API 合成。

- **接口**：`POST https://api.senseaudio.cn/v1/t2a_v2`
- **鉴权**：`Authorization: Bearer YOUR_API_KEY`
- **必填参数**：`model: "SenseAudio-TTS-1.0"`，`text`（要朗读的文案），`voice_setting.voice_id`（如 `male_0004_a`）
- **流式**：可设 `stream: false` 一次取回整段音频；响应中 `data.audio` 为 hex 编码，需解码为二进制后保存为 mp3/wav 或送入播放器。

详细请求/响应格式、音色列表与示例代码见 [reference.md](reference.md)。API 文档：<https://senseaudio.cn/docs>，TTS 说明：<https://senseaudio.cn/docs/text_to_speech_api>。

## 指令与回复约定

1. **录入位置**：用户说「记一下，我把 X 放在 Y 了」→ 解析并存储，回复「已记下：X 在 Y。」并可问是否要试听语音。
2. **查询位置**：用户问「X 放哪儿了」→ 查存储，若存在则回复「X 在 Y。」并用 TTS 生成语音；若无则回复「还没有记录 X 放哪儿。」
3. **添加提醒**：用户说时间 + 事项 +（可选）提前多久 → 解析时间与提前量，写入提醒列表，回复「已设置：在 [时间] 提前 [N] 分钟提醒你：[事项]。」
4. **播放语音**：生成提醒或位置朗读时，调用 SenseAudio 得到音频文件，提示用户播放或直接播放（取决于环境）。

## 语音播报脚本

技能提供两个脚本，用于**语音播报物品位置**和**定时播报待办提醒**。`{baseDir}` 表示本技能所在目录（由运行环境或工作区解析，不暴露具体绝对路径）。

### 1. 语音播放：`{baseDir}/scripts/speak.py`

- **播报自定义文本**：`python {baseDir}/scripts/speak.py --text "下午三点有会议，请提前准备" --play`
- **播报物品位置**：根据 `items.json` 查询并合成「X 在 Y」后播放：`python {baseDir}/scripts/speak.py --item 备用电池 --play`
- **仅生成音频不播放**：省略 `--play`，可用 `--out 路径.mp3` 指定输出文件。
- 选项：`--voice` 指定音色 ID（默认 `male_0004_a`）。

### 2. 定时播报：`{baseDir}/scripts/run_reminders.py`

- **单次检查**：到点提醒会从 `reminders.json` 中找出 `notify_at <= 当前时间` 且 `status=pending` 的条目，合成「提醒：XXX」并播放，然后标记为 `notified`。  
  `python {baseDir}/scripts/run_reminders.py`
- **常驻定时检查**：`python {baseDir}/scripts/run_reminders.py --daemon`（默认每 60 秒检查一次，可用 `--interval N` 修改）。
- **仅查看将播报的提醒**：`python {baseDir}/scripts/run_reminders.py --dry-run`。

建议用系统定时任务定期执行（如每分钟一次），以实现到点语音提醒：
- **macOS**：cron 或 launchd：`cd {baseDir} && python scripts/run_reminders.py`
- **Windows**：任务计划程序（Task Scheduler）：`python {baseDir}\scripts\run_reminders.py`
- **Linux**：cron：`cd {baseDir} && python scripts/run_reminders.py`

## 配置

- **{baseDir}**：表示本技能所在根目录，由运行环境解析，文档与命令中均不写死 `.cursor/skills` 或绝对路径。
- **SenseAudio API Key**：在环境变量中配置 `SENSEAUDIO_API_KEY`。密钥申请：<https://senseaudio.cn/platform/api-key>。
- **存储路径**：物品记录与提醒列表的默认路径见 [reference.md](reference.md)，可配置覆盖。

## 参考

- 数据格式、存储路径、SenseAudio 请求示例与音色表：[reference.md](reference.md)
- 更多对话示例：[examples.md](examples.md)
- 脚本用法细节见 [reference.md](reference.md) 的「脚本说明」小节。
