---
name: kes-qt
description: KingbaseES Qt 驱动 — 测试用例
---

# KingbaseES Qt 测试用例

## 测试用例 1: Qt 驱动安装

**场景**：Qt 项目需要连接金仓

**输入问题**："Qt 怎么连接金仓数据库？"

**期望答案要点**：
- qkingbase 驱动放入 `plugins/sqldrivers`
- 可用驱动列表中出现 "KINGBASE"
- 验证代码 `QSqlDatabase::drivers()`

**验证方法**：答案包含驱动安装路径和验证方法

---

## 测试用例 2: 兼容性检查

**场景**：用户不确定 Qt 版本是否支持

**输入问题**："Qt 5.6 能用金仓驱动吗？"

**期望答案要点**：
- Qt 4.8 和 Qt 5.6 均支持
- Linux amd64/aarch64 仅 64 位
- Windows MSVC 需要对应运行时

**验证方法**：答案引用兼容性矩阵
