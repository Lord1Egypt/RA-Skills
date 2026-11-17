---
name: kes-c-odbc
description: KingbaseES C/ODBC 连接 — 测试用例
---

# KingbaseES C/ODBC 测试用例

## 测试用例 1: KCI 编译链接

**场景**：C 语言项目需要编译链接 KCI

**输入问题**："C 语言怎么连接金仓数据库？"

**期望答案要点**：
- 使用 `libkci` 库
- 编译命令：`gcc -o myapp myapp.c -I$KINGBASE_HOME/include -L$KINGBASE_HOME/lib -lkci`
- 设置 `LD_LIBRARY_PATH`

**验证方法**：答案包含编译链接命令和环境变量

---

## 测试用例 2: ODBC DSN 配置

**场景**：需要通过 ODBC 连接，如 BI 工具集成

**输入问题**："Tableau 怎么连接金仓数据库？"

**期望答案要点**：
- ODBC DSN 配置：Driver、Servername、Port、Database、Username、Password
- 连接字符串方式：`Driver={KingbaseES ODBC Driver};Server=...`
- 适用 BI 工具集成场景

**验证方法**：答案包含 DSN 配置和适用场景

---

## 测试用例 3: libkci 加载失败

**场景**：运行时找不到 libkci

**输入问题**："C 程序运行报错无法加载 libkci"

**期望答案要点**：
- 设置 `export LD_LIBRARY_PATH=$KINGBASE_HOME/lib:$LD_LIBRARY_PATH`
- 库文件位于 `$KINGBASE_HOME/lib/libkci.so`

**验证方法**：答案指出 LD_LIBRARY_PATH 配置
