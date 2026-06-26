---
name: personal-scheduler
description: 个人日程管理 Skill - 自然语言设置、自动提醒、重复日程、Web界面、导入导出
version: 1.0.0
author: "于先生"
metadata:
  openclaw:
    emoji: "📅"
    requires:
      bins:
        - python
      ports:
        - 8080
---

# 📅 个人日程管理 Skill

面向个人用户的智能日程管理工具，支持自然语言对话设置、自动提醒、重复日程、Web界面管理、导入导出。

## ✨ 功能特性

### 1. 自然语言设置日程

无需记住命令，像聊天一样设置日程：

```
明天下午3点开会
→ 创建日程：明天 15:00-16:00「开会」

明天上午9点半去出入境
→ 创建日程：明天 09:30-10:30「去出入境」

每周一上午10点团队例会
→ 创建重复日程：每周一 10:00-11:00「团队例会」

把明天3点的会议改到4点
→ 修改日程时间

删除明天下午3点的会议
→ 删除匹配日程
```

### 2. 自动提醒（无需手动设置）

创建日程时**自动**创建提醒任务：
- 默认提前 15 分钟提醒
- 通过飞书/其他渠道发送
- 支持自定义提醒时间

### 3. 重复日程

支持创建重复事件：
- `每周一上午10点例会` - 每周重复
- `每天下午5点下班打卡` - 每天重复

### 4. 本地数据存储

- SQLite 数据库存储所有日程
- 数据完全本地，保护隐私
- 自动备份到 `data/backups/`

### 5. Web 界面管理

浏览器访问 `http://localhost:8080`：
- 月/周/日/列表视图
- 拖拽调整时间
- 点击创建/编辑
- **支持中英文切换**

### 6. 导入/导出

支持 .ics 格式（与 iPhone/Google/Outlook 日历互通）：
```bash
# 导出备份
python scripts/calendar_io.py export

# 导入日历
python scripts/calendar_io.py import mycalendar.ics
```

## 🚀 快速开始

### 安装依赖

```bash
pip install flask
```

### 配置

编辑 `data/config.json`：

```json
{
  "default_reminder_minutes": 15,
  "feishu_user_id": "your_feishu_user_id"
}
```

### 使用

```bash
# 添加日程
python scripts/main.py "明天下午3点开会"

# 添加重复日程
python scripts/main.py "每周一上午10点例会"

# 修改日程
python scripts/main.py "把明天3点的会议改到4点"

# 删除日程
python scripts/main.py "删除明天下午3点的会议"

# 查询日程
python scripts/main.py list

# 启动 Web 界面
python scripts/main.py web

# 导出备份
python scripts/calendar_io.py export
```

## 📝 自然语言支持

### 创建日程

| 输入示例 | 解析结果 |
|---------|---------|
| 明天下午3点开会 | 明天 15:00-16:00「开会」 |
| 明天上午9点半去银行 | 明天 09:30-10:30「去银行」 |
| 后天晚上7点到9点吃饭 | 后天 19:00-21:00「吃饭」 |
| 3月15号全天出差 | 2026-03-15 全天「出差」 |
| 每周一上午10点例会 | 每周一 10:00-11:00「例会」 |
| 每天下午5点打卡 | 每天 17:00-18:00「打卡」 |

### 修改日程

| 输入示例 | 操作 |
|---------|------|
| 把明天3点的会议改到4点 | 修改时间 |
| 把会议推迟30分钟 | 推迟30分钟 |
| 提前1小时 | 提前1小时 |

### 删除日程

| 输入示例 | 操作 |
|---------|------|
| 删除明天下午3点的会议 | 删除匹配日程 |
| 取消后天的约会 | 删除匹配日程 |

## 🔔 提醒机制

创建日程时自动创建 OpenClaw 定时任务：

```
日程时间: 2026-03-07 09:30
提醒时间: 2026-03-07 09:15（提前15分钟）
定时任务: 15 9 7 3 *（cron表达式）
```

到时间自动发送飞书消息：
```
⏰ 日程提醒

📌 去出入境
🕐 03月07日 09:30
⏳ 还有 15 分钟
```

## 🌐 Web 界面

### 功能
- 月/周/日/列表视图切换
- 点击日期查看当日日程
- 点击 + 按钮添加日程
- 中英文语言切换

### 访问
```bash
python scripts/main.py web
# 浏览器访问 http://localhost:8080
```

## 📁 文件结构

```
personal-scheduler/
├── SKILL.md                 # 本文件
├── scripts/
│   ├── main.py             # 主入口
│   ├── scheduler.py        # 核心逻辑
│   ├── natural_language.py # 自然语言解析
│   ├── send_reminder.py    # 发送提醒
│   ├── web_server.py       # Web服务
│   └── calendar_io.py      # 导入导出
├── web/
│   └── index.html          # Web界面（支持中英文）
└── data/
    ├── config.json         # 用户配置
    ├── scheduler.db        # SQLite数据库
    └── backups/            # 自动备份
```

## ⚙️ 配置说明

### config.json

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| default_reminder_minutes | 默认提前提醒分钟数 | 15 |
| feishu_user_id | 飞书用户ID（用于发送提醒） | - |
| timezone | 时区 | Asia/Shanghai |

## 🛠️ 技术栈

- **后端**: Python + Flask
- **数据库**: SQLite
- **前端**: HTML + CSS + JavaScript
- **定时任务**: OpenClaw Cron

## 📄 License

MIT
