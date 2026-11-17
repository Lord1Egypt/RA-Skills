---
name: kes-python
description: KingbaseES Python 连接 — 测试用例
---

# KingbaseES Python 测试用例

## 测试用例 1: ksycopg2 安装与 libkci

**场景**：用户在 Linux 服务器安装 ksycopg2 时遇到 libkci 加载错误

**输入问题**："pip install ksycopg2 后导入报错，说找不到 libkci"

**期望答案要点**：
- 需要设置 `LD_LIBRARY_PATH` 环境变量
- `export LD_LIBRARY_PATH=$KINGBASE_HOME/lib:$LD_LIBRARY_PATH`
- ksycopg2 依赖 libkci 库

**验证方法**：答案指出 LD_LIBRARY_PATH 配置和 libkci 依赖关系

---

## 测试用例 2: Python 版本兼容

**场景**：用户不确定 Python 版本是否支持

**输入问题**："Python 3.13 能用 ksycopg2 连接金仓吗？"

**期望答案要点**：
- ksycopg2 支持 Python 2.7, 3.5 ~ 3.13
- 3.13 在支持范围内

**验证方法**：答案正确指出版本支持范围

---

## 测试用例 3: 高可用主从连接

**场景**：主从架构下需要配置自动故障切换

**输入问题**："金仓数据库主从架构，Python 连接怎么自动切换到主节点？"

**期望答案要点**：
- 配置多个 host：`host="primary,standby"`
- 使用 `target_session_attrs="read-write"`

**验证方法**：答案包含多主机配置和 target_session_attrs 参数
