---
name: narrative-memory
description: 叙事记忆系统v2：捕捉生命中有意义的时刻，编织成连贯的个人叙事。三层过滤确保记忆精华，支持模式识别和决策反思。触发条件：里程碑事件、关键决策、价值判断、情感转折、首次体验、深度反思。
---

# Narrative Memory - 叙事记忆系统

## 使用方法

### 直接调用
```bash
node scripts/narrative.js <命令> [选项]
```

### 信号处理模式
```bash
node scripts/narrative.js --process-signal <signal>
```

## 命令

- `add <事件描述>` - 添加新的叙事记忆
- `timeline [选项]` - 查看时间线
- `list [选项]` - 列出叙事记忆

## 示例

```bash
# 添加记忆
node scripts/narrative.js add "完成了重要项目" --category milestone --importance 0.9

# 查看时间线
node scripts/narrative.js timeline --days 7

# 信号处理
node scripts/narrative.js --process-signal milestone_recorded
```

## 与proactive-engine集成

该skill通过`--process-signal`参数与proactive-engine信号系统集成，支持自动捕获重要生命时刻。