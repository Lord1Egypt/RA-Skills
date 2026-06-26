# PostgreSQL Tool 快速参考

## 🚀 3 步开始

### 1. 安装依赖
```bash
cd .qoder/skills/postgres-tool
.\scripts\install-offline.bat  # Windows
./scripts/install-offline.sh   # Linux/Mac
```

### 2. 配置数据库
创建 `db_config.json`：
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
```

## 🔧 故障诊断

```bash
# 运行诊断
python scripts/diagnose_deps.py

# 重新安装依赖
python -m pip install --no-index --find-links=./scripts/dependencies -r scripts/requirements.txt
```

## 💡 提示

1. **自动备份** - UPDATE/DELETE 前会自动备份
2. **使用 LIMIT** - 避免返回过多数据
3. **数据恢复** - 从 `backups/` 目录恢复误删数据

---
详细文档：`OFFLINE_DEPLOYMENT_GUIDE.md` | `SAFETY_GUIDE.md` | `EXAMPLES.md`
