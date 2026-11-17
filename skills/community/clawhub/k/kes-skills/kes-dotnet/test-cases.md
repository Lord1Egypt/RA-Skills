---
name: kes-dotnet
description: KingbaseES .NET 框架集成 — 测试用例
---

# KingbaseES .NET 框架测试用例

## 测试用例 1: KDBNDP 基础连接

**场景**：C# 项目连接金仓

**输入问题**："C# 怎么连接金仓数据库？"

**期望答案要点**：
- `using Kdbndp`
- `KdbndpConnection` + 连接字符串
- 端口 54321

**验证方法**：答案包含 KdbndpConnection 类名

---

## 测试用例 2: EF Core 配置

**场景**：使用 EF Core 操作金仓

**输入问题**："EF Core 怎么配置金仓？"

**期望答案要点**：
- `.UseKingbase("Host=...")`
- 验证 LINQ 到 SQL 转换的兼容性

**验证方法**：答案包含 UseKingbase 方法
