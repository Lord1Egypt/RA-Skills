---
name: kes-php
description: KingbaseES PHP 连接 — 测试用例
---

# KingbaseES PHP 测试用例

## 测试用例 1: PDO 基础连接

**场景**：PHP 项目需要连接 KingbaseES

**输入问题**："PHP 怎么连接金仓数据库？"

**期望答案要点**：
- 使用 `pdo_kdb` 驱动
- DSN 格式：`kdb:host=<主机>;dbname=<数据库>;port=<端口>`
- 配置 `php.ini` 加载扩展

**验证方法**：答案包含 DSN 格式和 php.ini 配置

---

## 测试用例 2: kdbCopy 批量导入

**场景**：需要从 PHP 数组快速导入大量数据

**输入问题**："PHP 怎么批量导入数据到金仓数据库？"

**期望答案要点**：
- `$pdo->kdbCopyFromArray('table_name', columns, data)`
- 也可用 kdbCopyFromFile / kdbCopyToFile / kdbCopyToArray

**验证方法**：答案使用 kdbCopy 系列函数

---

## 测试用例 3: 版本兼容性

**场景**：用户使用 PHP 8.4 不确定是否支持

**输入问题**："PHP 8.4 能用 pdo_kdb 吗？"

**期望答案要点**：
- PHP 5.6-8.4 均支持
- 注意选择 NTS/TS 对应的驱动包

**验证方法**：答案正确指出版本支持范围
