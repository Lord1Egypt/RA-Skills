# 设置指南

> [!WARNING]
> **隐私提醒 · Privacy Notice**
> 使用此技能即表示您了解：By using this skill you understand:
> 1. 上传的聊天记录、图片、设定等素材会被AI分析以生成角色档案
>    Uploaded chat logs, images, and notes will be analyzed by AI to generate character profiles
> 2. 角色会记住你的喜好和互动历史 Characters will remember your preferences and interaction history
> 3. 系统会创建持久状态文件和定时消息 System will create persistent state files and scheduled messages
> 4. 输入角色名时可能触发网络搜索 Character names may trigger web searches
> 5. **所有数据保存在本地，你可随时删除 All data stays local — you can delete anytime**
> 6. 上传的聊天记录如果包含第三方对话，请确保已获对方同意
>    If uploaded chat logs contain third-party conversations, ensure you have consent

## 快速开始

只需两步：

**第一步** — 告诉AI你要创建的角色
> "帮我建一个粘人的动漫女友，叫弥海砂"
> "这是她的设定：xxxx"（直接粘贴文字）
> "上传了我的聊天记录，帮我分析一下适合什么角色"

**第二步** — AI会自动完成：
1. 生成角色档案 → `state/character-profile.md`
2. 设置角色头像（如你上传了图片）
3. 生成初始关系状态 → `state/relationship-state.json`
4. 配置消息渠道
5. 按性格创建cron任务
6. 启动陪伴

## 角色素材上传

| 素材类型 | 例子 | 用处 |
|:---|:---|:---|
| 角色名+出处 | "弥海砂 死亡笔记" | 提取设定 |
| 性格描述 | "表面高冷内心温柔" | 性格参数 |
| 聊天记录 | 上传对话截图/文本 | 学习说话风格 |
| 人物图 | 上传角色形象 | 设为头像 |
| 设定文档 | 百科/小传/同人设定 | 完整档案 |
| 关系参考 | "我想让她一开始很烦我" | 初始关系锚点 |

## 关系状态文件

Skill会在 `state/relationship-state.json` 中维护当前关系状态：

```json
{
  "stage": "stranger",
  "affection": 15,
  "last_interaction": "2026-06-01T10:30:00",
  "total_days": 5,
  "continuous_silent_days": 0,
  "milestones": []
}
```

每个cron任务执行时读取此文件，决定消息风格，并在发送后更新。

## 性格与cron频率对照

| 性格 | cron间隔 | 每天消息 |
|:---:|:---:|:---:|
| 粘人 | 30min~1h | 12~20+ |
| 高冷(初期) | 4~8h | 2~4 |
| 高冷(后期) | 1~3h | 6~10 |
| 傲娇 | 1~3h | 5~8 |
| 病娇 | 15~30min | 20+ |
| 厌烦型 | 6~12h | 1~2 |
| 温柔型 | 1~2h | 8~12 |

## 可选集成

### 图像生成
配置图像API后，角色可按性格发场景配图。
高冷型即使配了也不会轻易发图。

### 语音（TTS）
配置TTS服务后，角色发的消息可以用对应声线朗读。
需要选择匹配角色人设的语音模型。

### 语音识别（STT）
配置STT后，用户可以发语音消息，AI识别内容并回复。

## 日常提醒配置

提醒内容必须符合角色人设。示例：

**厌烦型：**
> "到点了。该干嘛干嘛去，别让我天天说。"

**温柔型：**
> "记得吃饭哦～我不看着你你就不好好吃是吧？"

**傲娇型：**
> "我才不是关心你呢！只是顺嘴说一下……快去吃饭！"

## 发布到ClawHub

```bash
clawhub publish ./skills/virtual-companion --slug virtual-companion --name "虚拟伴侣 | Virtual Companion" --version 1.1.0 --changelog "新增角色进化系统、日常提醒、配图规则细化"
```
