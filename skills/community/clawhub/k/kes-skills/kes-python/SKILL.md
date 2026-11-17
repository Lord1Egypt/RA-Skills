---
name: kes-python
name_for_command: kes-python
description: 指导用户完成Python连接KingbaseES数据库。当用户提到Python开发、ksycopg2驱动、pip安装、Python连接金仓时，必须使用此技能。
---

# KingbaseES Python 连接指南

本技能指导用户完成 Python 连接 KingbaseES 的完整流程，涵盖 ksycopg2 驱动安装、环境变量配置、连接和连接池。

## 安装 ksycopg2

```bash
pip install ksycopg2
```

**支持版本**：Python 2.7, Python 3.5 ~ 3.13

## 系统依赖

ksycopg2 依赖 `libkci` 库，需确保以下库可用：
- `libssl`
- `libcrypto`

## 环境变量配置

```bash
# Linux x86_64
export LD_LIBRARY_PATH=$KINGBASE_HOME/lib:$LD_LIBRARY_PATH
export KINGBASE_HOME=/home/kingbase/install/kingbase
```

## 基本连接

```python
import ksycopg2

# 建立连接
conn = ksycopg2.connect(
    database="test",
    user="SYSTEM",
    password="123456",
    host="127.0.0.1",
    port="54321"
)

# 创建游标
cur = conn.cursor()

# 执行查询
cur.execute("SELECT version()")
result = cur.fetchone()
print(result[0])

# 执行写入
cur.execute("INSERT INTO test_table(name, value) VALUES(%s, %s)", ("测试", 123))
conn.commit()

# 关闭连接
cur.close()
conn.close()
```

## DSN 连接方式

```python
import ksycopg2

conn = ksycopg2.connect(
    "host=127.0.0.1 port=54321 dbname=test user=SYSTEM password=123456"
)
```

## 高可用主从连接

```python
# 配置多个主机，ksycopg2 自动故障切换
conn = ksycopg2.connect(
    host="primary,standby",
    port="54321",
    dbname="test",
    user="SYSTEM",
    password="123456",
    target_session_attrs="read-write"  # 自动连接到主节点
)
```

## 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `无法加载 libkci` | 环境变量未设置 | 设置 `LD_LIBRARY_PATH` 指向 `$KINGBASE_HOME/lib` |
| `连接被拒绝` | 端口/地址错误 | 检查端口（默认 54321）和 `sys_hba.conf` |
| `编码错误` | 字符集不匹配 | 确保数据库与客户端编码一致（推荐 UTF-8） |
