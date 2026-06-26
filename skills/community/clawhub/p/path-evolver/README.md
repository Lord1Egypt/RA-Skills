# Path Evolver

> Let AI Agent's execution paths learn, solidify, and evolve automatically.

让 AI Agent 的执行路径自动学习、固化、进化。

---

## 🌐 Language / 语言

- [English](#english) (Below)
- [中文](#中文) (下方)

---

<a name="english"></a>
## English

### One-Liner

Record successful paths → Auto-memoize → Discover better tools → Recommend upgrades

### Why Path Evolver?

**Problem:**
- AI agents re-select tools and methods every time
- Successful paths aren't recorded, requiring re-exploration
- Unknown if better tools exist in the market
- Low efficiency, repetitive work

**Solution:**
- **Path Caching** - Record successful execution paths
- **Success Rate Tracking** - Track success/failure for each path
- **Auto-Memoization** - Solidify paths when success rate ≥ 80% and count ≥ 3
- **Proactive Discovery** - Search ClawHub/GitHub for better tools
- **Smart Triggers** - Avoid searching every time

### Core Features

| Feature | Description |
|---------|-------------|
| Path Caching | Record successful execution paths for each task type |
| Success Rate Tracking | Track success count and rate for each path |
| Auto-Memoization | Solidify paths when success rate ≥ 80% and count ≥ 3 |
| Proactive Discovery | Search for better tools when triggered |
| Smart Triggers | Avoid searching every time, improve efficiency |
| Self-Evolution | This skill itself continuously improves |

### Use Cases

**Scenario 1: Repeated Tasks**
```
Task: Send Feishu message

1st time: Select tool → Execute → Record path (successCount: 1)
2nd time: Check cache → Use same path → successCount: 2
3rd time: successCount: 3, successRate: 100% → Auto-memoize
4th+ time: Use memoized path directly, no exploration needed
```

**Scenario 2: Discover Better Solutions**
```
Task: Web search

Current path: web_search (requires API key)
Problem: API key needed

Trigger search:
- Discover multi-search-engine (no API key needed)
- Discover agent-browser (supports complex SPAs)

Prompt user: "Found multi-search-engine might be better, switch?"
```

### Configuration

Default configuration:

```json
{
  "memoizeThreshold": {
    "successRate": 0.8,
    "minCount": 3
  },
  "cacheExpiryDays": 30,
  "searchTriggers": {
    "newTaskType": true,
    "toolFailure": true,
    "cacheExpired": true,
    "userRequest": true
  }
}
```

Adjustable:
- `successRate`: Success rate threshold (default 80%)
- `minCount`: Minimum execution count (default 3)
- `cacheExpiryDays`: Cache expiry days (default 30)

### Installation

**ClawHub:**
```bash
clawhub install path-evolver
```

**Manual:**
```bash
git clone https://github.com/doudoulaodou/path-evolver.git ~/.openclaw/workspace/skills/path-evolver
```

### Expected Improvements

| Metric | Expected Improvement |
|--------|---------------------|
| Repeated task efficiency | 50-80% (use cache directly) |
| Tool selection accuracy | 30-50% (based on history) |
| New tool discovery | Proactive, never miss |

---

<a name="中文"></a>
## 中文

### 一句话介绍

记录成功路径 → 自动固化 → 发现更优解 → 推荐升级

### 为什么需要这个？

**问题：**
- 每次都要重新选择工具和方法
- 成功的路径没有记录，下次还要探索
- 不知道市面上是否有更好的工具
- 效率低，重复劳动

**解决：**
- **路径缓存** - 记录成功的执行路径
- **成功率追踪** - 统计每种路径的成功率
- **自动固化** - 成功率达标后自动固化
- **主动搜索** - 发现更优工具时提示升级
- **智能触发** - 避免每次都搜索

### 核心功能

| 功能 | 说明 |
|------|------|
| 路径缓存 | 记录每种任务的成功执行路径 |
| 成功率追踪 | 统计每种路径的成功次数和成功率 |
| 自动固化 | 成功率 >= 80% 且次数 >= 3 后自动固化 |
| 主动搜索 | 智能触发 ClawHub/GitHub 搜索 |
| 自我进化 | 这个 skill 本身持续改进 |

### 安装

```bash
clawhub install path-evolver
```

---

## License

MIT License

---

## Author

- Author: 豆豆老爸 (doudoulaodou)
- Created: 2026-04-15
- Version: 1.0.1

---

## Feedback & Contributions

Issues and PRs welcome!

GitHub: https://github.com/doudoulaodou/path-evolver
