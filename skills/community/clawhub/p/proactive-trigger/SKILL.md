---
name: proactive-trigger
description: 主动触发引擎v4：基于兴趣衰减、沉默检测、话题热度，决定何时进行主动干预。触发条件：用户沉默、兴趣衰减、主动干预时机成熟。
---

# Proactive Trigger - 主动触发引擎

## 使用方法

### 直接调用
```bash
node scripts/trigger.js <命令> [选项]
```

### 信号处理模式
```bash
node scripts/trigger.js --process-signal <signal>
```

## 命令

- `assess [选项]` - 评估触发时机
- `suggest [选项]` - 生成触发建议
- `check [选项]` - 检查触发条件

## 示例

```bash
# 评估兴趣图谱
node scripts/trigger.js assess --interest-graph

# 检查沉默指数
node scripts/trigger.js suggest --silence-index

# 信号处理
node scripts/trigger.js --process-signal boundary_violation
```

## 与proactive-engine集成

该skill通过`--process-signal`参数与proactive-engine信号系统集成，是主动干预的核心决策引擎。