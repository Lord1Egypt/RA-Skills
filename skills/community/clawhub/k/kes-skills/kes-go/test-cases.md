---
name: kes-go
description: KingbaseES Go 连接 — 测试用例
---

# KingbaseES Go 测试用例

## 测试用例 1: Go gokb 基础连接

**场景**：Go 开发者想连接 KingbaseES

**输入问题**："Go 语言连接金仓数据库用什么驱动？给个例子"

**期望答案要点**：
- 驱动包：`kingbase.com/gokb`
- 使用 `sql.Open("kingbase", connInfo)`
- 连接字符串格式：`host=%s port=%d user=%s password=%s dbname=%s sslmode=disable`

**验证方法**：答案包含正确的驱动导入路径和连接字符串格式

---

## 测试用例 2: Go Modules 安装

**场景**：用户使用 Go Modules 方式安装驱动

**输入问题**："Go modules 怎么安装金仓驱动？"

**期望答案要点**：
- `require kingbase.com/gokb v1.0.0`
- `replace kingbase.com/gokb => ./gokb`

**验证方法**：答案包含 require 和 replace 指令

---

## 测试用例 3: GOPATH 安装

**场景**：用户使用 GOPATH 方式

**输入问题**："金仓 Go 驱动 package not found 怎么办？"

**期望答案要点**：
- 确认 `kingbase.com/gokb` 位于 `$GOPATH/src/`

**验证方法**：答案指出 GOPATH 路径要求
