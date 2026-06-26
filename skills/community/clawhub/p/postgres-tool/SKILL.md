---
name: postgres-tool
description: PostgreSQL database management tool for querying databases, exporting results, inspecting schemas, and safely performing UPDATE/DELETE operations with automatic backup and recovery. Use this skill whenever users need to connect to PostgreSQL, run SQL queries, view table structures, export data, or perform data modifications with safety protections.
---

# PostgreSQL Tool

这个技能允许你连接 PostgreSQL 数据库并执行各种查询操作。

## 功能

1. **执行 SELECT 查询** - 运行 SQL 查询并以表格或 JSON 格式展示结果
2. **查看表结构** - 检查表结构、列信息、数据类型和索引
3. **导出查询结果** - 将查询结果保存为 CSV 或 Excel 文件
4. **数据修改（UPDATE）** - 安全地更新数据（自动备份 + 用户确认）
5. **数据删除（DELETE）** - 安全地删除数据（自动备份 + 用户确认）
6. **数据恢复** - 从备份恢复被修改或删除的数据

## 配置文件

配置文件 `db_config.json` 位于技能目录的 `config/` 子目录下。**脚本会自动搜索并加载配置文件，无需用户手动指定。**

配置文件搜索顺序：
1. 当前工作目录下的 `db_config.json`
2. 技能目录下的 `config/db_config.json`（默认位置）
3. 技能根目录下的 `db_config.json`

如果配置文件不存在，脚本会提示用户创建。

## 使用方法

### 1. 安装依赖

#### 内网环境（推荐）

**Windows - 一键安装：**

```bash
# 方式 1：使用批处理脚本（推荐）
cd .qoder/skills/postgres-tool
.\scripts\install-offline.bat

# 方式 2：使用 PowerShell 脚本
cd .qoder/skills/postgres-tool
.\scripts\install-offline.ps1
```

**Linux/Mac - 手动安装：**

```bash
cd .qoder/skills/postgres-tool
python -m pip install --no-index --find-links=./scripts/dependencies -r scripts/requirements.txt
```

**重要提示：**
- ✅ 自动脚本会检查 Python 环境和依赖文件完整性
- ✅ 使用 `python -m pip` 确保即使 pip 不在 PATH 中也能工作
- ✅ 提供详细的错误诊断和解决方案

#### 在线环境

如果机器可以访问互联网：

```bash
pip install psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile
```

### 常见问题与解决方案

#### 快速诊断工具

如果安装失败，首先运行诊断工具检查问题：

```bash
# 进入技能目录
cd .qoder/skills/postgres-tool

# 运行诊断脚本
python scripts/diagnose_deps.py
```

诊断工具会自动检查：
- ✅ Python 版本信息
- ✅ dependencies 目录是否存在
- ✅ wheel 文件是否完整
- ✅ wheel 文件与 Python 版本的兼容性
- ✅ pip 状态
- ✅ 已安装的依赖包

**根据诊断结果采取相应措施。**

#### 问题 1：ERROR: Could not find a version that satisfies the requirement

**错误示例：**
```
ERROR: Could not find a version that satisfies the requirement psycopg2-binary
(from versions: none)
ERROR: No matching distribution found psycopg2-binary
```

**原因分析：**
1. `dependencies` 目录中的 wheel 文件与当前 Python 版本不匹配
2. wheel 文件名包含版本号（如 `cp313` 表示 Python 3.13）
3. 使用了相对路径导致 pip 找不到目录

**解决方案：**

**步骤 1：检查 Python 版本**
```bash
python --version
```

**步骤 2：检查 wheel 文件是否匹配**
查看 `dependencies` 目录下的文件名，例如：
- `psycopg2_binary-2.9.11-cp313-cp313-win_amd64.whl` → 需要 Python 3.13
- `pandas-3.0.1-cp313-cp313-win_amd64.whl` → 需要 Python 3.13

如果文件名中的 `cp313` 与你的 Python 版本不一致，需要重新下载对应版本的 wheel 文件。

**步骤 3：使用正确的命令重新下载依赖**
```bash
# 进入技能目录
cd .qoder/skills/postgres-tool

# 删除旧的依赖文件（如果有）
rm -rf scripts/dependencies/*.whl  # Linux/Mac
del /Q scripts\dependencies\*.whl  # Windows

# 下载与当前 Python 版本匹配的 wheel 文件
pip download psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile -d scripts/dependencies
```

**步骤 4：重新运行安装脚本**
```bash
# Windows
.\install-dependencies.bat

# Linux/Mac
./install-dependencies.sh
```

#### 问题 2：内网环境无法下载依赖

**解决方案：**

在有网络的机器上先下载依赖包：
```bash
# 1. 在外网机器下载
pip download psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile -d ./offline-deps

# 2. 将整个文件夹复制到内网机器的技能目录
cp -r offline-deps /path/to/postgres-tool/scripts/dependencies

# 3. 在内网运行安装脚本
cd /path/to/postgres-tool
./scripts/install-dependencies.sh
```

#### 问题 3：wheel 文件损坏或不完整

**症状：**
```
ERROR: Corrupted or incomplete wheel file
```

**解决方案：**
```bash
# 删除所有 wheel 文件并重新下载
cd .qoder/skills/postgres-tool
rm -rf scripts/dependencies/*.whl  # Linux/Mac
del /Q scripts\dependencies\*.whl  # Windows

# 重新下载
pip download psycopg2-binary pandas openpyxl numpy python-dateutil tzdata et-xmlfile -d scripts/dependencies

# 验证文件大小（应该都大于 10KB）
ls -lh scripts/dependencies/*.whl
```

#### 问题 4：权限问题

**症状：**
```
PermissionError: [Errno 13] Permission denied
```

**解决方案：**
```bash
# Windows：以管理员身份运行 PowerShell
# Linux/Mac：使用 sudo
sudo ./install-dependencies.sh

# 或者安装到用户目录
pip install --user --no-index --find-links=./scripts/dependencies -r scripts/requirements.txt
```

### 2. 基本查询

当用户请求查询数据库时，**直接调用 `scripts/postgres_tool.py` 脚本执行查询**，不要自己写脚本。

**执行查询：**
```bash
python scripts/postgres_tool.py "SELECT * FROM table_name LIMIT 10;"
```

**列出所有表：**
```bash
python scripts/postgres_tool.py --list-tables
```

**查看表结构：**
```bash
python scripts/postgres_tool.py --schema table_name
```

### 3. 数据修改操作（UPDATE/DELETE）

**重要安全机制：**
- ✅ 操作前自动备份数据
- ✅ 必须用户确认才能执行
- ✅ 提供恢复功能可以撤销操作
- ✅ 显示将要影响的记录数

#### UPDATE 操作示例

```bash
# 更新用户状态（会自动备份并请求确认）
python scripts/postgres_tool.py --update "UPDATE users SET status='active' WHERE last_login > '2024-01-01';" --table users

# 强制执行（跳过确认，危险！）
python scripts/postgres_tool.py --update "UPDATE products SET price=price*0.9;" --table products --force
```

#### DELETE 操作示例

```bash
# 删除过期数据（会自动备份并请求确认）
python scripts/postgres_tool.py --delete "DELETE FROM logs WHERE created_at < '2023-01-01';" --table logs

# 预览模式（只显示不执行）
python scripts/postgres_tool.py --delete "DELETE FROM temp_data;" --table temp_data --dry-run
```

### 4. 数据恢复功能

如果执行了 UPDATE 或 DELETE 操作，可以通过备份文件恢复数据：

```bash
# 从备份恢复数据
python scripts/postgres_tool.py --restore backups/20260322_184500/users_all_20260322_184500.csv

# 预览恢复内容（不实际执行）
python scripts/postgres_tool.py --restore backups/20260322_184500/users_all_20260322_184500.csv --dry-run
```

备份文件包含：
- CSV 格式的数据文件
- JSON 格式的元数据（表名、备份时间、记录数等）

### 5. 查看表结构

提供以下脚本来查看数据库表信息：

```python
def list_tables():
    """列出所有表"""
    sql = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name;
    """
    return execute_query(sql)

def get_table_schema(table_name):
    """获取表结构信息"""
    sql = """
    SELECT 
        column_name,
        data_type,
        is_nullable,
        column_default
    FROM information_schema.columns
    WHERE table_name = %s
    ORDER BY ordinal_position;
    """
    return execute_query(sql, params=(table_name,))

def get_table_indexes(table_name):
    """获取表的索引信息"""
    sql = """
    SELECT 
        indexname,
        indexdef
    FROM pg_indexes
    WHERE tablename = %s;
    """
    return execute_query(sql, params=(table_name,))
```

### 4. 导出查询结果

支持导出为 CSV 或 Excel 格式：

```python
def export_to_csv(df, filename):
    """将 DataFrame 导出为 CSV 文件"""
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"已导出到 {filename}")

def export_to_excel(df, filename, sheet_name='Sheet1'):
    """将 DataFrame 导出为 Excel 文件"""
    df.to_excel(filename, index=False, sheet_name=sheet_name, engine='openpyxl')
    print(f"已导出到 {filename}")

# 使用示例
df = execute_query("SELECT * FROM your_table;")
export_to_csv(df, "query_result.csv")
export_to_excel(df, "query_result.xlsx")
```

## 安全注意事项

1. **只允许 SELECT 查询** - 为了防止意外修改数据，默认只执行 SELECT 查询
2. **参数化查询** - 如果接受用户输入作为查询参数，务必使用参数化查询防止 SQL 注入
3. **连接池** - 对于频繁查询，考虑使用连接池提高性能
4. **超时设置** - 为长时间运行的查询设置合理的超时时间

## 错误处理

在查询时要注意的错误情况：

```python
import psycopg2.errors

def safe_execute_query(sql, max_rows=1000):
    """安全地执行查询，限制返回行数"""
    try:
        # 自动添加 LIMIT 防止返回过多数据
        if 'LIMIT' not in sql.upper():
            sql = f"{sql.rstrip(';')} LIMIT {max_rows}"
        
        with get_db_connection() as conn:
            df = pd.read_sql_query(sql, conn)
            return df
    except psycopg2.errors.SyntaxError as e:
        print(f"SQL 语法错误：{e}")
        raise
    except psycopg2.errors.UndefinedTable as e:
        print(f"表不存在：{e}")
        raise
    except Exception as e:
        print(f"查询失败：{e}")
        raise
```

## 最佳实践

1. **总是指定 LIMIT** - 避免一次性查询大量数据
2. **使用连接管理** - 使用上下文管理器确保连接正确关闭
3. **记录查询日志** - 保存查询历史便于调试和优化
4. **验证 SQL** - 在执行前检查 SQL 语法
5. **处理 NULL 值** - 在展示结果时妥善处理 NULL 值

## 示例工作流

当用户说："帮我查一下 users 表的前 100 条记录，并导出为 Excel"

步骤：
1. 检查是否存在 `db_config.json`
2. 连接数据库
3. 执行查询：`SELECT * FROM users LIMIT 100;`
4. 展示结果预览
5. 导出为 `users_export.xlsx`
6. 告知用户文件位置

---

## 快速参考命令

```python
# 列出所有表
list_tables()

# 查看表结构
get_table_schema('table_name')

# 执行自定义查询
execute_query("SELECT column1, column2 FROM table WHERE condition;")

# 导出结果
df = execute_query("SELECT * FROM table;")
export_to_csv(df, "output.csv")
export_to_excel(df, "output.xlsx")
```

## 故障排查

**问题：无法连接数据库**
- 检查 `db_config.json` 中的配置是否正确
- 确认数据库服务正在运行
- 检查防火墙设置
- 验证用户名和密码

**问题：查询超时**
- 添加 LIMIT 限制返回行数
- 优化 SQL 查询语句
- 检查是否有锁表情况

**问题：中文乱码**
- 导出 CSV 时使用 `encoding='utf-8-sig'`
- 确保数据库使用 UTF8 编码
