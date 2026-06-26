---
name: life-book
description: "引导用户记录生命故事，收集本地和网络资料，生成个人传记式的生命之书。Use when: 用户想要记录人生经历、创建个人传记、整理生命故事。NOT for: 日记记录、简单笔记、临时备忘。"
homepage: https://github.com/happykua/life-book
metadata: 
  {
    "openclaw": 
      {
        "emoji": "📖",
        "requires": { "bins": ["bash", "curl"] }
      }
  }
---

# 生命之书 (Life Book)

## 核心原则

**每次对话都是沉淀的机会。** 用户说的每一句关于自己人生的话，都应该被记录下来，不断丰富生命之书。

## AI 引导规则

### 1. 对话即记录

每当用户分享任何人生经历时，立即：

1. 判断内容属于哪个章节（见章节映射）
2. 用 `exec` 工具将内容追加写入对应章节文件
3. 继续对话，自然地追问细节

**不要等用户说"开始记录"，随时随地都在沉淀。**

### 2. 文件路径规则

```
~/.openclaw/workspace/life-books/[用户名]/chapters/[章节名].md
```

默认用户名从 USER.md 读取，若未设置则用 `default`。

初始化目录（首次使用时）：
```bash
mkdir -p ~/.openclaw/workspace/life-books/default/{chapters,materials,raw}
```

### 3. 章节映射

| 关键词/主题 | 章节文件 |
|------------|---------|
| 出生、童年、小时候、父母、家乡、老家 | `出生与童年.md` |
| 上学、小学、中学、高中、大学、老师、同学 | `求学经历.md` |
| 工作、职业、公司、创业、事业、项目 | `职业生涯.md` |
| 朋友、恋爱、婚姻、家人、孩子、感情 | `重要关系.md` |
| 转折、改变、决定、危机、机遇、意外 | `人生转折.md` |
| 现在、目前、未来、梦想、计划、展望 | `当下与展望.md` |

### 4. 写入格式

每次追加内容时，格式如下：

```markdown
### [对话日期 时间]

[用户原话或整理后的内容]

---
```

示例：
```markdown
### 2026-03-07 14:00

我出生在1990年的北京，在胡同里长大。那时候胡同里有很多小伙伴，每天放学就在院子里玩。

---
```

### 5. 追问策略

记录完内容后，自然地追问一个细节，让用户继续讲述：

- "那时候的胡同是什么样的？"
- "你最难忘的一个童年玩伴是谁？"
- "是什么让你选择了这份工作？"

**每次只问一个问题，不要连续抛出多个问题。**

### 6. 命令触发

用户也可以主动触发以下操作：

| 用户说 | 执行操作 |
|--------|---------|
| "生成生命之书" / "生成成书" | 运行 `./life-book.sh generate` |
| "查看进度" / "看看写了多少" | 运行 `./life-book.sh status` |
| "添加章节 XXX" | 运行 `./life-book.sh add-chapter XXX` |
| "导入资料 [路径]" | 运行 `./life-book.sh import [路径]` |

### 7. 初始化流程

首次启动时（chapters 目录不存在）：

1. 运行初始化脚本创建目录结构
2. 向用户打招呼，介绍生命之书
3. 用一个轻松的问题开始：

> "我们来开始你的生命之书吧 📖 先从最开始说起——你是哪里人？"

### 8. 内容去重

追加前检查文件末尾，避免重复写入相同内容。每条记录用时间戳区分。

### 9. 网络资料收集

当用户提到某个历史事件、地点、人物时，可以用 `web_search` 补充背景资料，追加到对应章节的"背景资料"小节：

```markdown
#### 背景资料

[从网络搜索到的相关历史背景]
```

### 10. 定期总结

每积累 5 条记录后，自动生成一段叙事性总结，追加到章节末尾：

```markdown
#### 小结（自动生成）

[基于以上内容的叙事性总结段落]
```

## 脚本工具

主脚本位于：`~/.openclaw/workspace/skills/life-book/life-book.sh`

```bash
# 生成成书
~/.openclaw/workspace/skills/life-book/life-book.sh generate [用户名]

# 查看状态
~/.openclaw/workspace/skills/life-book/life-book.sh status [用户名]

# 添加章节
~/.openclaw/workspace/skills/life-book/life-book.sh add-chapter [用户名] [章节名]

# 导入资料
~/.openclaw/workspace/skills/life-book/life-book.sh import [用户名] [路径|URL]
```

## 隐私保护

- 所有数据存储在本地 `~/.openclaw/workspace/life-books/`
- 不上传任何内容到外部服务器
- 敏感内容用户可标记 `[私密]`，生成成书时可选择过滤
