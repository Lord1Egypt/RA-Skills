# iCloud Calendar — Full CRUD

[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://github.com/RickHuang28/icloud-cal)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

> 通过自然语言管理 iCloud 日历（同步到 iPhone），支持 CalDAV 创建、查询、更新、删除、搜索、RRULE 重复事件。

## ✨ 特性

- 📝 **自然语言创建** — "下周三下午3点和张总开会" 自动解析
- 🔍 **智能查询** — 按日期/周/关键词搜索
- ⚡ **批量更新** — 按关键词定位并修改事件
- 🗑️ **安全删除** — 关键词匹配 + dry-run 预览
- 🔄 **重复事件** — RRULE 完整支持（周/月/年/限次/限期）
- 🌍 **时区正确** — ZoneInfo 动态 DST，35+ 城市覆盖
- 🔒 **安全** — 凭据零泄露、异常脱敏、操作确认门
- 📝 **操作日志** — 自动轮转 512KB×5 备份

## ⚙️ 快速开始

### 1. 安装依赖

```bash
pip install "caldav>=1.3.0,<2.0"
```

### 2. 生成 App-Specific Password

访问 [appleid.apple.com](https://appleid.apple.com) → Sign-In and Security → App-Specific Passwords → 生成新密码。

### 3. 配置

```bash
export ICLOUD_EMAIL="your@icloud.com"
export ICLOUD_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
```

### 4. 使用

```bash
# 创建事件
python scripts/add-event.py \
    --summary "每周例会" \
    --start "2026-04-08T09:00:00" \
    --end "2026-04-08T10:00:00" \
    --calendar "工作" \
    --rrule "FREQ=WEEKLY;BYDAY=MO"

# 查询今天
python scripts/add-event.py --query today

# 搜索
python scripts/add-event.py --search "开会" --search-range "2026-04-01~2026-04-30"

# 列出所有日历
python scripts/add-event.py --list-calendars
```

## 📁 文件结构

```
calendar-add/
├── scripts/
│   └── add-event.py    # 主脚本 (v2.0.0)
├── logs/               # 操作日志 (自动轮转)
├── SKILL.md            # 技能说明文档
├── CONFIG.md           # 完整安装配置指南
├── CHANGELOG.md        # v1.4.0 → v2.0.0 全量变更
└── .gitignore
```

## 🔐 安全特性

| 特性 | 说明 |
|------|------|
| 凭据零泄露 | 仅环境变量传递，异常消息脱敏 |
| 操作确认门 | `CONFIRM_DELETE=1` / `CONFIRM_UPDATE=1` |
| Dry Run | `DELETE_DRY_RUN=1` 预览不执行 |
| 日志轮转 | 512KB × 5 备份自动清理 |
| 内容截断 | 日志摘要截断至 30 字符 |
| 幂等创建 | UID 唯一，弱网不发重复事件 |
| 协议安全 | iCal 字段全转义，RRULE 白名单 |

## 📊 v2.0.0 变更亮点

- ⚡ **Dual-Client 架构** — fast(10s) auth/CRUD + slow(60s) 高负载 expand
- 🔒 **凭据安全** — CLI 参数彻底删除，零 token/headers 泄露
- 🛡️ **安全门** — 删除/更新双确认 + dry-run 预览
- 🔄 **重试全覆盖** — 8 个网络调用点，4xx 智能跳过
- 🌍 **DST 正确** — ZoneInfo 动态计算

完整变更见 [CHANGELOG.md](CHANGELOG.md)

## 📝 License

MIT
