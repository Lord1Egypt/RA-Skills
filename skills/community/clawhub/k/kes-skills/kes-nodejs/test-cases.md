---
name: kes-nodejs
description: KingbaseES Node.js 连接 — 测试用例
---

# KingbaseES Node.js 测试用例

## 测试用例 1: Node.js 基础连接

**场景**：Node.js 项目需要连接 KingbaseES

**输入问题**："Node.js 连接金仓数据库，使用连接池"

**期望答案要点**：
- 使用 `kb` 包：`const { Pool } = require('kb')`
- Pool 配置示例（max、idleTimeoutMillis 等）
- 连接使用 `$1` `$2` 占位符

**验证方法**：答案使用正确的包名 (`kb`) 和 API（Pool/Client）

---

## 测试用例 2: 版本兼容性

**场景**：用户使用 Node.js 16，不确定是否兼容

**输入问题**："Node.js 16 能用金仓驱动吗？"

**期望答案要点**：
- 驱动基于 Node.js 10.19.0 开发
- 支持 Node.js 8/10/12
- 高于 Node.js 12 可能出现不兼容

**验证方法**：答案指出版本限制

---

## 测试用例 3: 驱动安装

**场景**：用户找不到 kb 模块

**输入问题**："Cannot find module 'kb' 怎么解决？"

**期望答案要点**：
- 从 `$KINGBASE_HOME/Interface/` 复制 node_modules

**验证方法**：答案指出驱动来源路径
