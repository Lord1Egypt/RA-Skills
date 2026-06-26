# 🎫 Receipt Manager Skill

**English** | [中文](#收据管理器技能)

---

## <a name="english"></a>English

### Quick Start

1. **Install**: `git clone https://github.com/clinchcc/openclaw-receipt-manager.git ~/.openclaw/workspace/skills/receipt`
2. **Init**: `python3 ~/.openclaw/workspace/skills/receipt/scripts/receipt_db.py init`
3. **Use**: Send receipt image to OpenClaw

### Commands

```bash
# List receipts
python3 scripts/receipt_db.py list

# Search
python3 scripts/receipt_db.py search --q "walmart"

# Monthly summary
python3 scripts/receipt_db.py summary --month 2026-02
```

### Files

- `scripts/receipt_db.py` - Main CLI
- `scripts/handler.py` - OpenClaw handler
- `data/receipts/` - Local SQLite DB + images

### Privacy

✅ All data stored **locally** - nothing sent to cloud

---

## <a name="收据管理器技能"></a>收据管理器技能

**[English](#english)** | 中文

### 快速开始

1. **安装**: `git clone https://github.com/clinchcc/openclaw-receipt-manager.git ~/.openclaw/workspace/skills/receipt`
2. **初始化**: `python3 ~/.openclaw/workspace/skills/receipt/scripts/receipt_db.py init`
3. **使用**: 发送收据图片给 OpenClaw

### 命令

```bash
# 列出收据
python3 scripts/receipt_db.py list

# 搜索
python3 scripts/receipt_db.py search --q "沃尔玛"

# 月度汇总
python3 scripts/receipt_db.py summary --month 2026-02
```

### 文件

- `scripts/receipt_db.py` - 主 CLI
- `scripts/handler.py` - OpenClaw 处理器
- `data/receipts/` - 本地 SQLite 数据库 + 图片

### 隐私

✅ 所有数据**本地存储** - 不上传云端
