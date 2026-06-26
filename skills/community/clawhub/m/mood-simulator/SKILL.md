---
name: mood-simulator
description: 情绪状态模拟器v4：评估用户当前情绪状态、能量水平、专注度，支持实时情绪追踪。触发条件：情绪转折、能量变化、专注度调整。
---

# Mood Simulator - 情绪状态模拟器

## 使用方法

### 直接调用
```bash
node scripts/simulator.js <命令> [选项]
```

### 信号处理模式
```bash
node scripts/simulator.js --process-signal <signal>
```

## 命令

- `simulate [选项]` - 模拟情绪状态
- `adjust [选项]` - 调整情绪参数
- `track` - 追踪情绪变化

## 示例

```bash
# 模拟情绪
node scripts/simulator.js simulate --energy 70 --focus 80

# 调整时间因子
node scripts/simulator.js adjust --time-factor morning

# 信号处理
node scripts/simulator.js --process-signal transition
```

## 与proactive-engine集成

该skill通过`--process-signal`参数与proactive-engine信号系统集成，支持实时情绪追踪和能量警报。