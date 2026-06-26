---
name: process-flow-navigator
description: 业务流程图导航助手 - 帮助你在复杂的多分支流程中导航、规划路径、查询技能编码。支持 A→K 主流程及所有子流程分支。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": [] },
        "install": [],
      }
  }
instant: true
author: Instant
company: Instant
---

# Process Flow Navigator - 业务流程导航助手

## 功能

- 🧭 **流程导航** - 告诉你在哪个节点，帮你规划下一步
- 🗺️ **路径规划** - 从任意节点到任意节点的多路径规划
- 🏷️ **技能编码查询** - 快速查找各节点的校验/执行/判定技能编码
- 📊 **流程可视化** - 输出当前分支的结构图

## 支持的流程节点

| 节点 | 校验技能 | 执行技能 | 判定技能 |
|------|---------|---------|---------|
| A | PROC-A-CHECK-001 | PROC-A-EXEC-001 | PROC-A-B-JUDGE-001 |
| B | PROC-B-CHECK-002 | PROC-B-EXEC-002 | PROC-B-C-JUDGE-002 |
| C | PROC-C-CHECK-003 | PROC-C-EXEC-003 | - |
| D | PROC-D-CHECK-004 | PROC-D-EXEC-004 | PROC-D-E-JUDGE-004 |
| E | PROC-E-CHECK-005 | PROC-E-EXEC-005 | PROC-E-F-JUDGE-005 |
| F | PROC-F-CHECK-006 | PROC-F-EXEC-006 | PROC-F-G-JUDGE-006 |
| G | PROC-G-CHECK-007 | PROC-G-EXEC-007 | PROC-G-H-JUDGE-007 |
| H | PROC-H-CHECK-008 | PROC-H-EXEC-008 | PROC-H-I-JUDGE-008 |
| I | PROC-I-CHECK-009 | PROC-I-EXEC-009 | PROC-I-J-JUDGE-009 |
| J | PROC-J-CHECK-010 | PROC-J-EXEC-010 | PROC-J-K-JUDGE-010 |
| K | PROC-K-CHECK-011 | PROC-K-EXEC-011 | PROC-K-END-001 |

## 使用示例

### 导航到下一步
```
我在流程 B，下一步怎么走？
```

### 路径规划
```
从流程 B 到结束，有几种路线？
```

### 查询技能编码
```
流程 C 的技能编码是什么？
```

### 查看分支结构
```
显示 C 分支的完整流程
```

## 流程终点

| 终点 | 到达条件 |
|------|---------|
| **结束** | 最终判断 [是]、判断 9 [是] |
| **售后** | 判断 7 [乱码]、判断 8 [否]、判断 9 [否] |

## 核心规则

- **最终判断 [是]** → 结束
- **最终判断 [否]** → 继续流转

## 数据来源

本 skill 基于用户提供的业务流程图.pdf 创建，包含完整的节点连接关系和技能编码映射。

## 更新日志

- **v1.0.0** - 初始版本，包含完整 A-K 流程导航能力

---

## ©️ 版权

**Instant** © 2026 - 保留所有权利
