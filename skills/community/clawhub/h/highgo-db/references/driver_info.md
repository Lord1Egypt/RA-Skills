# 瀚高数据库 (HighGo DB) 驱动详细说明

瀚高数据库（HighGo Database）提供的 `psycopg2` 是标准 PostgreSQL 驱动的修改版本。由于瀚高数据库支持特殊的安全特性（如国密 SM4 算法），使用原生的 `psycopg2` 可能无法连接或无法正常进行加密通信。

## 驱动目录结构 (`@psycopg2/`)

该驱动通常作为文件夹（如 `@psycopg2/`）分发，包含以下核心文件：
- `__init__.py`: 驱动入口。
- `_psycopg.so`: 编译后的 C 扩展模块。
- `libpq.so.5`: 瀚高修改版的 libpq 库，包含瀚高特有的通信逻辑。
- `libgmssl.so.3`: 国密算法支持库（可选）。
- 其他辅助模块如 `extras.py`, `sql.py` 等。

## 与标准 psycopg2 的区别
- **安全增强**: 支持 `sm3` 密码加密、`sm4` 链路加密等。
- **目录前缀**: 为了避免与环境中的 `pip install psycopg2` 冲突，瀚高通常将包名或目录名稍作修改（如 `@psycopg2`），但在代码内部仍然通过 `import psycopg2` 进行自我引用。

## 运行环境要求
- **Python 3.x**: 建议使用 3.8+。
- **操作系统**: 通常针对特定的 Linux 发行版提供编译好的 `.so` 文件。如果系统库不匹配，可能需要设置 `LD_LIBRARY_PATH` 指向该驱动目录。

## 脚本桥接机制
由于该驱动被命名为 `@psycopg2`，直接 `import` 并不被 Python 支持。`execute_query.py` 脚本通过以下方式解决：
1. 创建临时目录。
2. 将 `@psycopg2` 符号链接为 `psycopg2`。
3. 将临时目录加入 `sys.path`。
4. 动态导入 `psycopg2`。
