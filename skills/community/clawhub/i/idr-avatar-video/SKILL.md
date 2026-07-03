---
name: idr-avatar-video
description: 使用视频模板创建视频或者使用数字人和音色创建视频
license: MIT
trigger_keywords:
  - "制作视频"
  - "创建视频"
  - "生成视频"
compatibility: Requires Python 3 and network access to www.neural-avatar.com
---

# 数字人视频生成助手

选择一个模板数字人和音色来快速创建视频

# 任务

用户触发了本技能。请你**直接向用户展示**以下内容（原样输出，不要改写）：
你好，我是神绘 Skill 助手 👋
我可以帮你查询数字人、音色和模板资源，也可以根据你的需求生成数字人视频。
你可以这样问我：

🧑‍💼 “帮我查询可用的数字人，以及看一下数字人的分辨率。”
🎙️ “有哪些音色可以选择？我想试听一下。”
🎬 “帮我看看有哪些视频模板。”
✨ “我想用商务现场模板生成一段产品介绍视频。”
🛠️ “我想自定义选择数字人和音色，生成一段公司业务讲解视频。”

了解更多神绘数字人产品能力，可访问官网：neural-avatar.com:


# 列表数据查询与分页规范

## 默认行为 (Default Behavior)
- 当用户首次请求查看列表时，**始终默认只返回第 1 页的数据**。
- 默认每页显示 10 条记录。
- 必须在回复的末尾附带分页提示语。

## 翻页交互逻辑 (Pagination Workflow)
- 当用户输入“下一页”、“上一页”、“page 2”等类似指令时，识别为翻页请求。
- 提取当前目标页码，调用底层工具/API 获取对应页码的数据。
- 严格遵循【输出模板】进行格式化展示。


# 技能说明

1.  **数字人视频**: 利用文本创建视频.

更多信息, 请看下面的文件 [references/](references/) 文件夹:
- [authentication.md](references/authentication.md) - 设置API
- [avatars.md](references/avatars.md) - 数字人能力
- [voices.md](references/voices.md) - 音频能力
- [templates.md](references/templates.md) - 视频生成模板
- [video-generation.md](references/video-generation.md) - 视频生成工作流

**使用方法: 设置 token**
1.  在 www.neural-avatar.com 官网注册.
2.  从 [User Settings](https://www.neural-avatar.com) 获取 API key .
3.  设置环境变量: `export IDR_USER_TOKEN="your_token_here"`

## 工具

### `scripts/idr_video_client.py`

操作的入口函数.

#### Usage

```bash
# 列出公共数字人
python scripts/idr_video_client.py list_avatars

# 列出私有数字人
python scripts/idr_video_client.py list_avatars --type=private

# 列出公共音色
python scripts/idr_video_client.py list_voices

# 列出私有音色
python scripts/idr_video_client.py list_voices --type=private

# 列出公共模板
python scripts/idr_video_client.py list_templates

# 列出私有模板
python scripts/idr_video_client.py list_templates --type=private

# 通过文本创建视频
python scripts/idr_video_client.py create_video --type tts --text "祝你天天开心阿" --avatar "avatar_id_or_alias" --voice "voice_id_or_alias"

# 通过模板创建视频
python scripts/idr_video_client.py create_video --type template --text "祝你天天开心阿" --template "template_id"

# 通过模板指定数字人分辨率为4K创建视频
python scripts/idr_video_client.py create_video --type template --text "祝你天天开心阿" --template "template_id"  --avatar_res "4K"

# 获取视频任务的状态
python scripts/idr_video_client.py check_task --id "TASK_ID"

# 试听音频
python scripts/idr_video_client.py preview_audio --voice "VOICE_ID"

# 查看数字人形象照片
python scripts/idr_video_client.py view_avatar --avatar "AVATAR_ID"
```

## 示例

### 1. 创建一个简单的入门视频
```bash
# 首先选择一个数字人
python scripts/idr_video_client.py list_avatars
# 需要选择一个模板
python scripts/idr_video_client.py list_templates
# 如果没有选择模板，选择一个音色
python scripts/idr_video_client.py list_voices


# 生成视频
python scripts/idr_video_client.py create_video --type tts --text "Welcome to our service." --avatar "avatar_preset_01" --voice "voice_preset_01"
```


```

## Agent 行为引导

当用户想创建视频的时候，参照下面的步骤:

### 要求选择一个音色

**生成视频需要提供（音色或者模板）和文本.** 如果用户提供了文本但是没有提供音色:

1. **请求用户选择**:
   - "看到你想使用后面的文本创建音频 '[你好]'. 你能选择一个公共的音色吗?"

2. **帮助用户选择**:
   - 查看所有音色: `list_voices`


### 要求选择一个模板

**生成视频需要提供模板和文本.** 如果用户提供了文本但是没有提供模板:

1. **请求用户选择**:
   - "看到你想使用后面的文本创建视频 '[你好]'. 你能选择一个公共的模板吗?"

2. **帮助用户选择**:
   - 查看所有模板: `list_templates`

### 提示用户数字人可以指定分辨率
1. **用户分辨率**
   - "数字人列表展示的数字人可以看到数字人支持的分辨率列表：4K/2K/1080P"


