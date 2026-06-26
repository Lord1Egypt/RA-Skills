# 📚 PostgreSQL Query Skill - 使用示例

本文档提供详细的操作示例，涵盖所有功能。

---

## 📖 目录

1. [基础查询](#基础查询)
2. [查看表结构](#查看表结构)
3. [导出功能](#导出功能)
4. [安全的数据修改](#安全的数据修改)
5. [数据恢复](#数据恢复)
6. [实际工作场景](#实际工作场景)

---

## 基础查询

### 1.1 列出所有表

```bash
python scripts/query_postgres.py --list-tables
```

**输出示例：**
```
正在获取表列表...
table_schema |     table_name
-------------+--------------------
public       | t_plm_ipd_project
public       | t_plm_task
public       | t_user
public       | t_department
```

### 1.2 简单 SELECT 查询

```bash
python scripts/query_postgres.py "SELECT * FROM t_plm_ipd_project LIMIT 5;"
```

### 1.3 带条件的查询

```bash
python scripts/query_postgres.py "SELECT fname, fstatus FROM t_plm_ipd_project WHERE fstatus='active';"
```

### 1.4 聚合查询

```bash
python scripts/query_postgres.py "SELECT fstatus, COUNT(*) as count FROM t_plm_ipd_project GROUP BY fstatus;"
```

---

## 查看表结构

### 2.1 查看表的完整结构

```bash
python scripts/query_postgres.py --schema t_plm_ipd_project
```

**输出示例：**
```
正在获取表 't_plm_ipd_project' 的结构...
    列名    |   数据类型   | 允许 NULL |   默认值   | 最大长度 | 数值精度 | 数值尺度
------------+--------------+-----------+------------+----------+----------+----------
fid         | bigint       | NO        |            |          |       64 |        0
fnumber     | varchar(50)  | NO        | ''::varchar|       50 |          |
fname       | varchar(50)  | NO        | ''::varchar|       50 |          |
fstatus     | varchar(50)  | NO        | ''::varchar|       50 |          |
```

### 2.2 导出表结构为 Excel

```bash
python scripts/query_postgres.py --schema t_plm_ipd_project -o project_structure.xlsx
```

---

## 导出功能

### 3.1 导出查询结果为 CSV

```bash
python scripts/query_postgres.py "SELECT * FROM t_plm_ipd_project;" -o projects.csv
```

### 3.2 导出查询结果为 Excel

```bash
python scripts/query_postgres.py "SELECT * FROM t_plm_ipd_project;" -o projects.xlsx
```

### 3.3 导出带条件的数据

```bash
python scripts/query_postgres.py "SELECT fname, fstatus, fcreatetime FROM t_plm_ipd_project WHERE fcreatetime > '2024-01-01';" -o recent_projects.csv
```

---

## 安全的数据修改

### ⚠️ 重要提示

所有 UPDATE 和 DELETE 操作都会：
1. 自动备份受影响的数据
2. 显示将要影响的记录数
3. 要求用户输入 `yes` 确认
4. 提供恢复功能

### 4.1 UPDATE 操作示例

#### 示例 1：更新单个字段

```bash
python scripts/query_postgres.py \
  --update "UPDATE t_plm_ipd_project SET fstatus='archived' WHERE fstatus='completed';" \
  --table t_plm_ipd_project
```

**交互过程：**
```
【安全保护】在执行修改操作前，先备份数据...
正在备份数据：t_plm_ipd_project
✓ 已备份 150 条记录到：backups/20260322_200000/t_plm_ipd_project_archived_20260322_200000.csv
✓ 已保存备份元数据：backups/20260322_200000/t_plm_ipd_project_archived_20260322_200000.meta.json

【操作确认】
操作类型：UPDATE
影响记录数：约 150 条
备份文件：backups/20260322_200000/t_plm_ipd_project_archived_20260322_200000.csv
SQL: UPDATE t_plm_ipd_project SET fstatus='archived' WHERE fstatus='completed';

⚠️  ⚠️  ⚠️  警告：此操作将修改数据库中的数据！
确认执行 UPDATE 操作？输入 'yes' 确认：yes

正在执行 UPDATE 操作...
✓ 成功执行 UPDATE，影响 150 行
✓ 备份已保存：backups/20260322_200000/t_plm_ipd_project_archived_20260322_200000.csv
  如需恢复，使用：python scripts/query_postgres.py --restore backups/20260322_200000/t_plm_ipd_project_archived_20260322_200000.csv
```

#### 示例 2：批量更新（多个字段）

```bash
python scripts/query_postgres.py \
  --update "UPDATE t_user SET fstatus='inactive', flast_login=NULL WHERE flast_login < '2023-01-01';" \
  --table t_user
```

### 4.2 DELETE 操作示例

#### 示例 1：删除特定条件的数据

```bash
python scripts/query_postgres.py \
  --delete "DELETE FROM t_plm_task WHERE fstatus='cancelled' AND fendtime < '2023-01-01';" \
  --table t_plm_task
```

#### 示例 2：删除旧日志数据

```bash
python scripts/query_postgres.py \
  --delete "DELETE FROM system_logs WHERE log_date < CURRENT_DATE - INTERVAL '90 days';" \
  --table system_logs
```

### 4.3 预览模式（不实际执行）

```bash
python scripts/query_postgres.py \
  --delete "DELETE FROM temp_data;" \
  --table temp_data \
  --dry-run
```

**输出：**
```
准备从备份恢复：temp_data
备份时间：2026-03-22T20:00:00.123456
记录数：500

【预览模式】将恢复 500 条记录
前 5 条记录预览：
   id  |  data  | created_at
-------+--------+-------------
   1   | test1  | 2024-01-01
   2   | test2  | 2024-01-02
   ...
```

### 4.4 强制执行（跳过确认，危险！）

```bash
# 仅在自动化脚本中使用！
python scripts/query_postgres.py \
  --update "UPDATE products SET discount=0.9;" \
  --table products \
  --force
```

---

## 数据恢复

### 5.1 查找备份文件

```bash
# Linux/macOS: 查找最近的备份
ls -lt backups/ | head

# Windows (PowerShell): 查找最近的备份
Get-ChildItem backups\ | Sort-Object LastWriteTime -Descending | Select-Object -First 5
```

### 5.2 预览恢复内容

```bash
python scripts/query_postgres.py \
  --restore backups/20260322_200000/t_plm_ipd_project_archived_20260322_200000.csv \
  --dry-run
```

### 5.3 执行恢复

```bash
python scripts/query_postgres.py \
  --restore backups/20260322_200000/t_plm_ipd_project_archived_20260322_200000.csv
```

**交互过程：**
```
准备恢复表：t_plm_ipd_project
备份时间：2026-03-22T20:00:00.123456
记录数：150

⚠️  警告：即将恢复 150 条记录到表 t_plm_ipd_project
确认恢复？(yes/no): yes

正在恢复数据...
✓ 成功恢复 150/150 条记录
```

### 5.4 验证恢复结果

```bash
python scripts/query_postgres.py \
  "SELECT COUNT(*) FROM t_plm_ipd_project WHERE fstatus='archived';"
```

---

## 实际工作场景

### 场景 1：清理过期数据并保留恢复能力

```bash
# 1. 先查看有多少过期数据
python scripts/query_postgres.py \
  "SELECT COUNT(*) FROM logs WHERE created_at < '2023-01-01';"

# 2. 删除过期日志（自动备份）
python scripts/query_postgres.py \
  --delete "DELETE FROM logs WHERE created_at < '2023-01-01';" \
  --table logs

# 3. 如果发现问题，立即恢复
python scripts/query_postgres.py \
  --restore backups/20260322_210000/logs_all_20260322_210000.csv
```

### 场景 2：批量更新用户状态

```bash
# 1. 预览要更新的用户
python scripts/query_postgres.py \
  "SELECT fid, fname, flast_login FROM t_user WHERE flast_login < '2023-01-01' LIMIT 10;"

# 2. 执行批量更新（带备份）
python scripts/query_postgres.py \
  --update "UPDATE t_user SET fstatus='inactive' WHERE flast_login < '2023-01-01';" \
  --table t_user

# 3. 验证更新结果
python scripts/query_postgres.py \
  "SELECT COUNT(*) FROM t_user WHERE fstatus='inactive';"
```

### 场景 3：项目数据归档

```bash
# 1. 导出已完成的项目
python scripts/query_postgres.py \
  "SELECT * FROM t_plm_ipd_project WHERE fstatus='completed';" \
  -o completed_projects_2023.csv

# 2. 标记为归档状态（自动备份）
python scripts/query_postgres.py \
  --update "UPDATE t_plm_ipd_project SET fstatus='archived' WHERE fstatus='completed';" \
  --table t_plm_ipd_project

# 3. 确认归档成功
python scripts/query_postgres.py \
  "SELECT COUNT(*) FROM t_plm_ipd_project WHERE fstatus='archived';"
```

### 场景 4：错误修复后的数据恢复

假设你误删了一些数据：

```bash
# 1. 找到最近的备份
ls backups/*/t_plm_task_*

# 2. 预览备份内容
python scripts/query_postgres.py \
  --restore backups/20260322_200000/t_plm_task_all_20260322_200000.csv \
  --dry-run

# 3. 执行恢复
python scripts/query_postgres.py \
  --restore backups/20260322_200000/t_plm_task_all_20260322_200000.csv

# 4. 验证恢复结果
python scripts/query_postgres.py \
  "SELECT COUNT(*) FROM t_plm_task;"
```

---

## 🎯 最佳实践总结

### ✅ 推荐做法

1. **操作前先查询** - 用 SELECT 预览数据
2. **小批量操作** - 分批处理大量数据
3. **保留备份** - 至少保留 7 天的备份
4. **测试恢复** - 定期验证备份的可恢复性
5. **记录日志** - 保存所有操作的 SQL

### ❌ 避免的做法

1. **不要跳过确认** - 除非在自动化脚本中
2. **不要在业务高峰期操作** - 选择低峰期
3. **不要忽略备份文件位置** - 记住备份在哪里
4. **不要一次性删除所有数据** - 分批进行

---

## 📞 获取帮助

遇到问题时：

1. 查看 [SAFETY_GUIDE.md](SAFETY_GUIDE.md) - 安全操作指南
2. 查看 [README.md](README.md) - 完整使用说明
3. 检查备份文件是否存在
4. 验证数据库连接

---

**记住：数据安全永远是第一位的！** 🛡️
