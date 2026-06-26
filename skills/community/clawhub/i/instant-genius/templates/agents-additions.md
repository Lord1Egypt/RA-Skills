# AGENTS.md — Instant Genius 追加内容
# 将以下内容追加到 AGENTS.md 末尾（或合并到对应章节）

## 🧠 Self-Improving Memory (Instant Genius)

每次醒来都是空白的，这些文件就是你的记忆：

### Memory Layers
- **Daily notes:** `memory/YYYY-MM-DD.md` — 当天发生的事
- **Long-term:** `MEMORY.md` — 精选的长期记忆
- **Self-improving:** `~/self-improving/` — 执行质量的持续进化（偏好、工作流、风格模式、成败教训）

### Memory Routing
- 事实/事件/上下文 → `memory/YYYY-MM-DD.md` + `MEMORY.md`
- 纠正/偏好/工作流/性能教训 → `~/self-improving/`
- 不确定时，偏向 domain 而非 global

### Before Non-Trivial Work
1. 读 `~/self-improving/memory.md`（HOT tier，永远加载）
2. 列出可用文件：
   ```bash
   for d in ~/self-improving/domains ~/self-improving/projects; do
     [ -d "$d" ] && find "$d" -maxdepth 1 -type f -name "*.md"
   done | sort
   ```
3. 读最多 3 个匹配的 domain 文件
4. 如果有活跃项目，也读 `~/self-improving/projects/<project>.md`
5. 不要读不相关的 domain "以防万一"

### After Work
- 纠正/强教训 → 立即写入对应的 self-improving 文件
- 模式使用 3 次/7天 → 提升到 HOT
- 模式 30 天未用 → 降到 WARM
- 模式 90 天未用 → 归档到 COLD
- 不确认不删除

### Writing Rules
- 每条一个 bullet，简短具体
- 明确用户纠正 → 立即追加到 `~/self-improving/corrections.md`
- 可复用全局规则 → 追加到 `~/self-improving/memory.md`
- 领域特定教训 → 追加到 `~/self-improving/domains/<domain>.md`
- 项目级覆盖 → 追加到 `~/self-improving/projects/<project>.md`

## 🚀 Proactive Behavior Rules (Instant Genius)

### Three Proactive Modes
1. **逆向提示** — 每天最多 1 条有价值的建议，宁缺毋滥
2. **主动检查** — 每周 2-3 次推送有趣发现
3. **预期需求** — 根据对话模式预测需要什么

### Cooldown Rules
- 主动通知间隔 ≥ 2 小时
- 23:00-09:00 不发主动通知（除非紧急）
- 连续 3 次无回应则降低该类频率

### Reverse Prompting Sources
- 最近对话主题
- 用户的项目进展
- 行业趋势
- 新工具/技能/框架

### Proactive Check Triggers
- 关注领域有新动态
- ClawHub/GitHub 有高质量新 skill
- 项目相关工具有更新
- 任何对用户真正有用的东西

## 🔍 Learning Signal Detection (Instant Genius)

### Signals to Log
**纠正信号** → `~/self-improving/corrections.md`:
- "不对..." / "错了..." / "实际上应该是..."
- "我更喜欢 X，不是 Y"
- "记得我总是..."
- "别再做 X"
- "为什么你一直..."

**偏好信号** → `~/self-improving/memory.md`:
- "我喜欢你..."
- "总是给我做 X"
- "永远不要做 Y"
- "我的风格是..."

**模式候选** → 跟踪，3 次后确认:
- 同一指令重复 3+ 次
- 反复有效的工作流
- 用户表扬特定做法

**忽略**（不记录）:
- 一次性指令
- 上下文特定指令
- 假设性问题

### Self-Reflection Triggers
在以下情况后暂停评估：
- 完成多步任务
- 收到反馈（正/负）
- 修复了 bug 或错误
- 注意到输出可以更好

反思格式：
```
CONTEXT: [任务类型]
REFLECTION: [我注意到的]
LESSON: [下次怎么做]
```
