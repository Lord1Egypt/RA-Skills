# Diary Skill - AI 日记记录系统

全天候思考搭子与日记记录系统，支持本地和多平台同步。

## 功能特点

- ✅ 智能记录：自动识别用户想法、文章讨论、协作任务
- ✅ 多平台同步：支持本地/飞书/Flomo/Notion
- ✅ 双人设模式：INTJ 分析型（话少）/ ENFP 温暖型（陪聊）
- ✅ 时间线记录：以时间为主线，用 tag 区分类型
- ✅ 不脑补原则：只记录用户明确说的话

## 快速开始

### 1. 安装

```bash
# 复制到 OpenClaw workspace
cp -r diary ~/.openclaw/workspace/

# 创建日记目录
mkdir -p ~/write_me/00inbox/journal
```

### 2. 配置

编辑 `config/diary-config.json`：

```json
{
  "storage": {
    "type": "local",
    "path": "~/write_me/00inbox/journal",
    "feishu": {
      "enabled": false,
      "folder_token": ""
    }
  },
  "personality": {
    "type": "enfp",
    "file": "personalities/enfp.md"
  }
}
```

**存储位置配置**：
- `type`: 主存储位置（`local`/`feishu`/`flomo`/`notion`）
- 本地存储始终启用，其他平台可选同步

**人设配置**：
- `intj`: 分析型，话少，关注规律和系统
- `enfp`: 温暖型，陪聊，关注情感和陪伴

### 3. 飞书集成（可选）

如果你已经配置了飞书：

1. 确保环境变量已设置：
   ```bash
   export FEISHU_APP_ID="your_app_id"
   export FEISHU_APP_SECRET="your_app_secret"
   ```

2. 在配置中启用飞书：
   ```json
   {
     "storage": {
       "feishu": {
         "enabled": true,
         "folder_token": "your_folder_token"
       }
     }
   }
   ```

3. OpenClaw 会自动：
   - 按月创建飞书文档（标题：`日记 YYYY-MM`）
   - 同步日记内容
   - 返回文档链接

### 4. 使用

在 OpenClaw（Telegram/WhatsApp/Slack）中：

```
你：记一下今天的想法
AI：好的，跟我说说吧！

你：今天和朋友聊天，聊到了职业规划
AI：听起来是个重要的对话！你们具体聊了什么？有什么新的想法吗？
```

## 触发方式

### 手动触发
- "记一下XXX"
- "记录XXX"
- "写日记"
- "/diary"

### 自动识别
当你说以下内容时，AI 会主动询问是否记录：
- "今天发生了..."
- "刚才..."
- "我在想..."
- 分享文章链接
- 表达情绪

## 记录格式

### [主动记录] - 用户明确要求记的
```markdown
## 14:30 [主动记录] - 项目进展

**事实**：
和同事讨论了项目方案。

**用户说**：
"他提出要改设计风格，我觉得有道理但工作量会增加。"
```

### [陪读] - 共读文章讨论
```markdown
## 18:00 [陪读] - 教育改革文章

**文章**：
《大学专业调整的思考》

**用户观点**：
"不是'砍专业'，而是'重构教育'。"

**讨论**：
AI：这个话题可以写成文章吗？
用户：可以，感觉挺有意思的。
```

### [协作] - 和AI一起做的事
```markdown
## 23:30 [协作] - 搭建日记系统

**决定**：
- AI负责记录日常聊天
- 用户复制给其他工具做深度处理

**用户说**：
"AI更像是'记录员'。"
```

## 人设对比

### INTJ 分析型（话少）

**特点**：
- 简洁、精准、分析性强
- 关注规律和系统
- 少说话，多记录

**示例**：
```
用户："今天又加班了，好累。"
INTJ："记录：加班。这是本周第3次。"
```

### ENFP 温暖型（陪聊）

**特点**：
- 温暖、陪伴感强
- 关注情感和感受
- 主动关心，提供支持

**示例**：
```
用户："今天又加班了，好累。"
ENFP："辛苦了！这周已经加班3次了，感觉怎么样？需要聊聊吗？"
```

## 多平台同步

### 本地存储（默认）
- 路径：`~/write_me/00inbox/journal/YYYY-MM.md`
- 格式：Markdown
- 按月分文件

### 飞书同步
- 自动创建月度文档
- 标题：`日记 YYYY-MM`
- 实时同步
- 返回文档链接

### Flomo 同步
- 每条记录作为独立 memo
- 自动添加日期标签
- 支持搜索和回顾

### Notion 同步
- 写入指定 database
- 按日期组织
- 支持筛选和视图

## 配置示例

### 纯本地存储
```json
{
  "storage": {
    "type": "local",
    "path": "~/write_me/00inbox/journal"
  },
  "personality": {
    "type": "intj"
  }
}
```

### 本地 + 飞书同步
```json
{
  "storage": {
    "type": "local",
    "path": "~/write_me/00inbox/journal",
    "feishu": {
      "enabled": true,
      "folder_token": "fldcnXXXXXXXXXXXXXXXXXXX"
    }
  },
  "personality": {
    "type": "enfp"
  }
}
```

### 多平台同步
```json
{
  "storage": {
    "type": "local",
    "path": "~/write_me/00inbox/journal",
    "feishu": {
      "enabled": true,
      "folder_token": "fldcnXXXXXXXXXXXXXXXXXXX"
    },
    "flomo": {
      "enabled": true,
      "api_key": "your_flomo_api_key"
    },
    "notion": {
      "enabled": true,
      "database_id": "your_notion_database_id"
    }
  },
  "personality": {
    "type": "enfp"
  }
}
```

## 核心原则

### 1. 不替用户脑补
- ❌ 不要写"用户觉得"、"用户想"
- ✅ 只记录用户明确说的话
- ✅ 如果是 AI 观察，明确标注

### 2. 保留用户原话
- 用引号标记
- 不改写或总结
- 保持原始表达

### 3. 以时间线为主体
- 按时间顺序记录
- 用 tag 区分类型
- 方便回顾和检索

### 4. 尊重人设设定
- INTJ：简洁、分析、少话
- ENFP：温暖、陪伴、多话

## 日期判断

一天以实际睡觉为界：
- **00:00-06:00** → 写入前一天
- **06:00-24:00** → 写入当天

## 常见问题

### Q: 如何切换人设？
A: 编辑 `config/diary-config.json`，修改 `personality.type` 为 `intj` 或 `enfp`。

### Q: 如何添加飞书同步？
A:
1. 设置环境变量 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`
2. 在配置中启用飞书并设置 `folder_token`
3. OpenClaw 会自动同步

### Q: 本地文件在哪里？
A: 默认在 `~/write_me/00inbox/journal/YYYY-MM.md`，可在配置中修改。

### Q: 如何导出日记？
A: 本地文件就是 Markdown 格式，可以直接复制或用其他工具处理。

### Q: AI 会记录所有对话吗？
A: 不会。只记录：
- 用户明确要求记的（"记一下XXX"）
- 用户分享的文章和想法
- 完成的协作任务

### Q: 如何删除某条记录？
A: 直接编辑本地 Markdown 文件，或在飞书文档中删除。

## 文件结构

```
diary/
├── skill.json                  # OpenClaw skill 元数据
├── prompt.md                   # 核心 prompt
├── personalities/
│   ├── intj.md                 # INTJ 分析型人设
│   └── enfp.md                 # ENFP 温暖型人设
├── config/
│   └── diary-config.json       # 配置文件
└── README.md                   # 本文档
```

## 贡献

欢迎提交 Issue 和 PR！

## 许可

MIT License

---

最后更新：2026-03-14
