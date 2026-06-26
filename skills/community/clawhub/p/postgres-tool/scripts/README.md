# Scripts 目录说明

## 📁 文件结构

```
scripts/
├── postgres_tool.py          # 主程序
├── diagnose_deps.py          # 诊断工具
├── install-offline.bat       # Windows 安装脚本
├── install-offline.ps1       # PowerShell 安装脚本
├── requirements.txt          # 依赖列表
└── dependencies/             # wheel 文件
```

## 🚀 快速开始

### 1. 安装依赖

**Windows (批处理):**
```bash
cd .qoder/skills/postgres-tool
.\scripts\install-offline.bat
```

**PowerShell (推荐):**
```bash
cd .qoder/skills/postgres-tool
.\scripts\install-offline.ps1
```

### 2. 配置数据库

创建 `db_config.json`:
```json
{
  "host": "localhost",
  "port": 5432,
  "database": "your_db",
  "user": "username",
  "password": "password"
}
```

### 3. 测试
```bash
python scripts/postgres_tool.py --list-tables
```

## 📋 常用命令

```bash
# 查询
python scripts/postgres_tool.py "SELECT * FROM table LIMIT 10;"

# 统计
python scripts/postgres_tool.py "SELECT COUNT(*) FROM table;"

# 表结构
python scripts/postgres_tool.py --schema table_name

# 导出 CSV
python scripts/postgres_tool.py "SELECT * FROM table;" -o output.csv

# 导出 Excel
python scripts/postgres_tool.py "SELECT * FROM table;" -o output.xlsx

# 诊断问题
python scripts/diagnose_deps.py
```

## 💡 提示

1. **自动备份** - UPDATE/DELETE 前会自动备份
2. **使用 LIMIT** - 避免返回过多数据
3. **数据恢复** - 从 `backups/` 目录恢复误删数据

---
详细文档：`../references/QUICK_REFERENCE.md` | `../references/OFFLINE_DEPLOYMENT_GUIDE.md`
