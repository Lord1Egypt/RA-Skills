# My Diary (my-diary)

A personal diary management skill for AI assistants. Allows you to record, view, search, and delete diary entries.

## Features

- **Write Diary** - Record daily thoughts, events, or reminders
- **View Diaries** - Browse all diary entries in chronological order
- **Search Diaries** - Find entries by keywords
- **Delete Diaries** - Remove unwanted entries

## Installation

This skill is distributed via [ClawHub](https://clawhub.openclaw.ai). To install:

```bash
clawhub install my-diary
```

Or manually place the skill folder in your skills directory.

## Configuration

### Storage Location

By default, diaries are stored at:
```
D:\Nancy\MyWork\WorkBuddyWorkSpace\diary\my-diary.json
```

You can modify this path in `SKILL.md` if needed.

## Usage Examples

### Writing a Diary Entry

**Trigger phrases:**
- "Write diary: [content]"
- "记日记：[content]"

**Examples:**
```
User: Write diary: Today I learned to cook pasta
User: 记日记：今天学会了做意面
```

The skill will:
1. Read the existing diary file (or create a new one)
2. Generate a unique ID (timestamp)
3. Add the new entry with timestamp
4. Save to file and confirm success

---

### Viewing All Diaries

**Trigger phrases:**
- "View diary" / "My diary"
- "查看日记" / "我的日记"

**Example:**
```
User: View my diary
```

The skill will list all entries in reverse chronological order with date and content summary.

---

### Viewing a Specific Entry

**Trigger phrases:**
- "View entry #N"
- "查看第X篇日记"

**Examples:**
```
User: View the latest entry
User: 查看第1篇日记
```

---

### Searching Diaries

**Trigger phrases:**
- "Search diary: [keyword]"
- "搜索日记：[关键词]"

**Examples:**
```
User: Search diary: meeting
User: 搜索日记：315
```

The skill will search for entries containing the keyword (case-insensitive) and display matching results.

---

### Deleting a Diary Entry

**Trigger phrases:**
- "Delete diary"
- "删除日记"

**Examples:**
```
User: Delete the first diary entry
User: 删除第2篇日记
```

The skill will list entries for selection, confirm deletion, then remove the entry.

## Data Format

Diary entries are stored in JSON format:

```json
{
  "version": "1.0",
  "entries": [
    {
      "id": "1700000000000",
      "content": "Diary content here...",
      "created_at": "2026-03-15 14:30:00"
    }
  ]
}
```

## Notes

- Each entry is automatically timestamped
- Entries are displayed in reverse chronological order (newest first)
- Deletion requires confirmation
- Search is case-insensitive

---

# 我的日记 (my-diary)

个人日记管理技能。用于记录日记、查询日记、查看日记列表、删除日记等操作。

## 功能

- **写入日记** - 记录每日的想法、事件或提醒
- **查看日记** - 按时间顺序浏览所有日记条目
- **搜索日记** - 通过关键词查找条目
- **删除日记** - 移除不需要的条目

## 安装

此技能通过 [ClawHub](https://clawhub.openclaw.ai) 分发。安装方法：

```bash
clawhub install my-diary
```

或手动将技能文件夹放入你的 skills 目录中。

## 配置

### 存储位置

默认情况下，日记保存在：
```
D:\Nancy\MyWork\WorkBuddyWorkSpace\diary\my-diary.json
```

如需修改，可在 `SKILL.md` 中更改此路径。

## 使用示例

### 写入日记

**触发短语：**
- "写入日记：[内容]"
- "记日记：[内容]"

**示例：**
```
用户：写入日记：今天学会了做意面
用户：记日记：晚上有315晚会
```

技能将执行：
1. 读取现有日记文件（或创建新文件）
2. 生成唯一ID（时间戳）
3. 添加新条目并附带时间戳
4. 保存到文件并确认成功

---

### 查看所有日记

**触发短语：**
- "查看日记"
- "我的日记"

**示例：**
```
用户：查看我的日记
```

技能将按时间倒序列出所有条目，显示日期和内容摘要。

---

### 查看指定日记

**触发短语：**
- "查看第X篇日记"

**示例：**
```
用户：查看最新的日记
用户：查看第1篇日记
```

---

### 搜索日记

**触发短语：**
- "搜索日记：[关键词]"

**示例：**
```
用户：搜索日记：315
用户：搜索日记：开会
```

技能将搜索包含关键词的条目（不区分大小写）并显示匹配结果。

---

### 删除日记

**触发短语：**
- "删除日记"

**示例：**
```
用户：删除第1篇日记
用户：删除第2篇日记
```

技能将列出条目供选择，确认后删除并确认成功。

## 数据格式

日记条目以 JSON 格式存储：

```json
{
  "version": "1.0",
  "entries": [
    {
      "id": "1700000000000",
      "content": "日记内容...",
      "created_at": "2026-03-15 14:30:00"
    }
  ]
}
```

## 注意事项

- 每次写入自动记录时间
- 日记按时间倒序排列（最新优先）
- 删除前需要确认
- 搜索不区分大小写
