<p align="center">
  <img src="./assets/banner.svg" alt="OfferCatcher" width="100%">
</p>

<p align="center">
  <strong>再也不错过任何一场面试。</strong><br>
  <sub>AI 驱动的邮件解析，将招聘邮件转为原生提醒事项。</sub>
</p>

<p align="center">
  <a href="#功能特性">功能特性</a> •
  <a href="#快速开始">快速开始</a> •
  <a href="#安装">安装</a> •
  <a href="#使用方法">使用方法</a> •
  <a href="#配置">配置</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-0f172a?style=flat-square" alt="OpenClaw Skill">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square" alt="Python 3.11+">
  <img src="https://img.shields.io/badge/Platform-macOS-000000?style=flat-square" alt="macOS">
  <img src="https://img.shields.io/badge/License-MIT-f59e0b?style=flat-square" alt="MIT License">
  <a href="README.md"><img src="https://img.shields.io/badge/README-English-55b3c5?style=flat-square" alt="English"></a>
</p>

---

## 痛点

你在找工作。邮箱里塞满了招聘邮件——面试邀请、在线测评、笔试通知、截止日期。重要的邮件被淹没在"投递成功"回执和垃圾邮件里。

**你错过了一场面试。** 或者记错了时间。或者忘了那个编程测试的截止日期。

## 解决方案

**OfferCatcher** 自动扫描你的邮件，使用 AI 提取招聘事件，在 iPhone/Mac 上创建原生提醒。

```
📧 邮件到达 → 🤖 AI 解析 → 🔔 提醒创建
```

没有正则。没有脆弱的模式匹配。智能提取，适配所有邮件格式和语言。

## 功能特性

- **🤖 AI 驱动解析** — LLM 理解任意邮件格式，任意语言
- **🍎 原生苹果集成** — 与 Mail.app 和 Reminders.app 深度集成
- **📱 跨设备同步** — 通过 iCloud 同步到 iPhone、iPad、Mac
- **⚡ 全自动运行** — 一次配置，通过 OpenClaw heartbeat 自动运行
- **🌍 全语言支持** — 中文、英文、日文，统统不在话下

## 社区

- [LINUX DO](https://linux.do) — 中文开发者社区

## 快速开始

```bash
# 安装
curl -sSL https://raw.githubusercontent.com/NissonCX/offercatcher/main/install.sh | bash

# 配置
echo 'mail_account: "Gmail"' >> ~/.openclaw/offercatcher.yaml

# 扫描
python3 ~/.openclaw/workspace/skills/offercatcher/scripts/recruiting_sync.py --scan-only
```

OpenClaw 会自动解析结果并创建提醒。

## 安装

### 环境要求

- macOS（Apple Mail 和 Reminders 集成）
- Python 3.11+
- [OpenClaw](https://github.com/NissonCX/openclaw)（可选，用于自动化）

### 方式一：从 ClawHub 安装（推荐）

```bash
# 搜索 skill
openclaw skills search offercatcher

# 安装到工作区
openclaw skills install offercatcher
```

### 方式二：一键安装

```bash
curl -sSL https://raw.githubusercontent.com/NissonCX/offercatcher/main/install.sh | bash
```

### 方式三：手动安装

```bash
git clone https://github.com/NissonCX/offercatcher.git
cd offercatcher
```

## 使用方法

### 第一步：查看邮箱账号

```bash
python3 scripts/list_mail_sources.py
```

显示 Apple Mail 中配置的所有账号：

```json
[
  {"account": "Gmail", "mailbox": "INBOX"},
  {"account": "iCloud", "mailbox": "INBOX"}
]
```

### 第二步：配置

创建 `~/.openclaw/offercatcher.yaml`：

```yaml
mail_account: "Gmail"    # Apple Mail 账号名
mailbox: "INBOX"         # 要扫描的邮箱文件夹
days: 2                  # 扫描最近 N 天
max_results: 60          # 最大邮件数
```

### 第三步：扫描邮件

```bash
python3 scripts/recruiting_sync.py --scan-only
```

输出（JSON 格式，供 OpenClaw LLM 解析）：

```json
{
  "emails": [
    {
      "message_id": "12345",
      "subject": "面试邀请 - 软件工程师",
      "sender": "recruiting@company.com",
      "received_at": "2026-04-01 10:00",
      "body": "尊敬的候选人，您的面试安排在..."
    }
  ]
}
```

### 第四步：AI 解析 + 创建提醒

OpenClaw 自动：
1. 使用 LLM 解析每封邮件
2. 提取公司、事件类型、时间、链接
3. 创建原生 Apple Reminders

或手动应用解析结果：

```bash
python3 scripts/recruiting_sync.py --apply-events /tmp/events.json
```

### 手动记录事件

```bash
python3 scripts/manual_event.py \
  --title "Google 面试" \
  --due "2026-04-15 14:00" \
  --notes "链接: https://meet.google.com/xxx"
```

## 工作原理

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   --scan-only   │ ──▶ │   OpenClaw LLM  │ ──▶ │  --apply-events │
│    扫描邮件     │     │    解析事件     │     │   创建提醒      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### 为什么用 LLM 而不是正则？

| 正则 | LLM |
|------|-----|
| 遇到新格式就挂 | 适配任意格式 |
| 需要公司特定规则 | 适用于任何公司 |
| 需要人工维护 | 零维护 |
| 特定语言 | 全语言支持 |

## 配置

### 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--mail-account` | 全部 | Apple Mail 账号名 |
| `--mailbox` | INBOX | 邮箱文件夹 |
| `--days` | 2 | 扫描最近 N 天 |
| `--max-results` | 60 | 最大邮件数 |
| `--dry-run` | false | 测试运行，不创建提醒 |
| `--verbose` | false | 详细日志 |

### 环境变量

```bash
OFFERCATCHER_MAIL_ACCOUNT="Gmail"
OFFERCATCHER_DAYS=7
OFFERCATCHER_MAX_RESULTS=100
OFFERCATCHER_LOG_LEVEL=DEBUG
```

### 事件 JSON 格式

`--apply-events` 接受的格式：

```json
{
  "events": [
    {
      "id": "唯一标识",
      "company": "阿里巴巴",
      "event_type": "interview",
      "title": "阿里巴巴面试",
      "timing": {"start": "2026-04-15 14:00", "end": "2026-04-15 15:00"},
      "role": "软件工程师",
      "link": "https://meeting-url"
    }
  ]
}
```

事件类型：`interview`、`ai_interview`、`written_exam`、`assessment`、`authorization`、`deadline`

## 效果展示

<table>
  <tr>
    <td align="center">
      <img src="./assets/showcase-list.jpg" alt="提醒列表" width="260">
      <br><sub><b>提醒列表</b></sub>
    </td>
    <td align="center">
      <img src="./assets/showcase-detail.jpg" alt="提醒详情" width="260">
      <br><sub><b>提醒详情</b></sub>
    </td>
  </tr>
</table>

## 项目结构

```
offercatcher/
├── scripts/
│   ├── recruiting_sync.py      # 主脚本（扫描/应用）
│   ├── apple_reminders_bridge.py # Apple Reminders 桥接
│   ├── manual_event.py         # 手动记录事件
│   └── list_mail_sources.py    # 列出邮箱账号
├── tests/                      # 单元测试
├── SKILL.md                    # OpenClaw skill 定义
└── README.md                   # 英文文档
```

## 贡献

欢迎提交 Pull Request！

## 许可证

[MIT License](./LICENSE)

---

<p align="center">
  用 ❤️ 为求职者打造
</p>