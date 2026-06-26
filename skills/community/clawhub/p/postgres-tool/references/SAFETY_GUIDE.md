# 🔐 PostgreSQL Query Skill - 安全操作指南

## ⚠️ 重要提示

本技能支持 **UPDATE** 和 **DELETE** 等危险操作，但实现了多层安全保护机制。在使用这些功能前，请务必阅读并理解本文档。

---

## 🛡️ 安全保护机制

### 1. 操作前自动备份 ✅

**所有** UPDATE 和 DELETE 操作在执行前都会自动备份受影响的数据：

- 备份保存为 CSV 格式
- 同时保存 JSON 元数据（表名、时间、记录数等）
- 备份文件保存在 `backups/YYYYMMDD_HHMMSS/` 目录
- 备份文件名包含表名和时间戳

**示例：**
```bash
python scripts/query_postgres.py --delete "DELETE FROM logs WHERE created_at < '2023-01-01';" --table logs

# 输出：
# 【安全保护】在执行修改/删除操作前，先备份数据...
# 正在备份数据：logs
# ✓ 已备份 1500 条记录到：backups/20260322_184500/logs_all_20260322_184500.csv
# ✓ 已保存备份元数据：backups/20260322_184500/logs_all_20260322_184500.meta.json
```

### 2. 用户确认机制 ✅

**默认情况下**，所有修改操作都需要用户输入 `yes` 确认：

```bash
【操作确认】
操作类型：DELETE
影响记录数：约 1500 条
备份文件：backups/20260322_184500/logs_all_20260322_184500.csv
SQL: DELETE FROM logs WHERE created_at < '2023-01-01';

⚠️  ⚠️  ⚠️  警告：此操作将修改/删除数据库中的数据！
确认执行 DELETE 操作？输入 'yes' 确认：
```

如果用户不输入 `yes`，操作会被取消，但备份会保留。

### 3. 恢复功能 ✅

如果误操作或需要撤销，可以通过备份文件恢复数据：

```bash
# 预览恢复内容
python scripts/query_postgres.py --restore backups/20260322_184500/logs_all_20260322_184500.csv --dry-run

# 实际恢复（需要再次确认）
python scripts/query_postgres.py --restore backups/20260322_184500/logs_all_20260322_184500.csv
```

---

## 📋 使用流程

### DELETE 操作完整流程

#### 步骤 1：预览要删除的数据

```bash
# 先查询看看有多少数据
python scripts/query_postgres.py "SELECT COUNT(*) FROM logs WHERE created_at < '2023-01-01';"
```

#### 步骤 2：执行删除（带备份和确认）

```bash
python scripts/query_postgres.py --delete "DELETE FROM logs WHERE created_at < '2023-01-01';" --table logs
```

#### 步骤 3：确认操作

系统会显示：
- 备份文件位置
- 影响记录数
- SQL 语句

输入 `yes` 确认执行，或按 Ctrl+C 取消。

#### 步骤 4：验证结果

```bash
# 检查是否还有旧数据
python scripts/query_postgres.py "SELECT COUNT(*) FROM logs WHERE created_at < '2023-01-01';"
```

#### 步骤 5：如需恢复

```bash
# 从备份恢复
python scripts/query_postgres.py --restore backups/20260322_184500/logs_all_20260322_184500.csv
```

---

### UPDATE 操作完整流程

#### 步骤 1：预览要更新的数据

```bash
# 查看将要更新的数据
python scripts/query_postgres.py "SELECT * FROM users WHERE status='inactive' LIMIT 10;"
```

#### 步骤 2：执行更新（带备份和确认）

```bash
python scripts/query_postgres.py --update "UPDATE users SET status='archived' WHERE last_login < '2023-01-01';" --table users
```

#### 步骤 3：确认操作

输入 `yes` 确认执行。

#### 步骤 4：验证结果

```bash
# 检查更新结果
python scripts/query_postgres.py "SELECT COUNT(*) FROM users WHERE status='archived';"
```

#### 步骤 5：如需恢复

```bash
# 恢复被更新的数据
python scripts/query_postgres.py --restore backups/20260322_190000/users_archived_20260322_190000.csv
```

---

## 🚨 危险操作警告

以下情况需要特别小心：

### ❌ 不带 WHERE 条件的 DELETE

```bash
# 极度危险！会删除整个表的数据！
python scripts/query_postgres.py --delete "DELETE FROM users;" --table users
```

**后果：** 
- 备份整个表（可能很大）
- 恢复时可能需要很长时间
- 可能导致外键约束问题

**建议：** 永远不要这样做！如果要清空表，使用 `TRUNCATE TABLE`（但不在本技能支持范围内）。

### ❌ 大范围的 UPDATE

```bash
# 危险！可能影响大量数据
python scripts/query_postgres.py --update "UPDATE products SET price=price*1.1;" --table products
```

**后果：**
- 备份整个表
- 可能锁表影响性能
- 恢复困难

**建议：** 分批执行，每次更新少量数据。

### ⚠️ 使用 --force 参数

```bash
# 跳过确认，极度危险！
python scripts/query_postgres.py --delete "DELETE FROM logs;" --table logs --force
```

**仅在以下情况使用 --force：**
- 自动化脚本中
- 已经测试过多次
- 有完整的备份策略
- 明确知道后果

---

## 💾 备份管理

### 备份文件结构

```
backups/
├── 20260322_184500/
│   ├── logs_all_20260322_184500.csv
│   └── logs_all_20260322_184500.meta.json
├── 20260322_190000/
│   ├── users_inactive_20260322_190000.csv
│   └── users_inactive_20260322_190000.meta.json
└── ...
```

### 备份元数据内容

每个 `.meta.json` 文件包含：

```json
{
  "table_name": "logs",
  "backup_time": "2026-03-22T18:45:00.123456",
  "record_count": 1500,
  "where_clause": "created_at < '2023-01-01'",
  "backup_file": "backups/20260322_184500/logs_all_20260322_184500.csv",
  "columns": ["id", "user_id", "action", "created_at"]
}
```

### 清理旧备份

定期清理旧备份以节省空间：

```bash
# Linux/macOS: 删除 30 天前的备份
find backups/ -type d -mtime +30 -exec rm -rf {} \;

# Windows (PowerShell): 删除 30 天前的备份
Get-ChildItem backups\ -Directory | Where-Object { $_.CreationTime -lt (Get-Date).AddDays(-30) } | Remove-Item -Recurse
```

---

## 🔍 最佳实践

### ✅ 推荐做法

1. **始终先预览** - 执行前先 SELECT 查看数据
2. **小批量操作** - 分批删除/更新，避免一次性处理大量数据
3. **保留备份** - 至少保留最近 7 天的备份
4. **测试恢复** - 定期测试备份文件的恢复功能
5. **记录日志** - 保存所有操作的 SQL 日志

### ❌ 避免的做法

1. **不要在业务高峰期操作** - 选择低峰期执行
2. **不要跳过确认** - 除非在自动化脚本中
3. **不要删除所有数据** - 总有更好的方法
4. **不要忽略备份** - 备份是最后的安全网

---

## 🆘 故障排查

### 问题：操作失败，数据部分修改

**解决方案：**
1. 检查备份文件是否完整
2. 使用恢复功能还原数据
3. 分析错误日志
4. 重新执行操作（修复问题后）

### 问题：恢复失败

**可能原因：**
- 表结构已改变
- 主键冲突
- 外键约束

**解决方案：**
```bash
# 1. 预览恢复内容
python scripts/query_postgres.py --restore backup.csv --dry-run

# 2. 检查表结构是否匹配
python scripts/query_postgres.py --schema table_name

# 3. 手动修复冲突后恢复
```

### 问题：备份文件太大

**解决方案：**
1. 只备份需要的列：`SELECT id, name FROM table WHERE ...`
2. 分批操作，减少单次备份量
3. 压缩备份文件：`gzip backup.csv`

---

## 📞 获取帮助

如果遇到问题：

1. 查看错误信息
2. 检查备份文件是否存在
3. 验证数据库连接
4. 参考 [README.md](README.md) 和 [INSTALL.md](INSTALL.md)

---

**记住：安全第一！始终谨慎操作数据库！** 🛡️
