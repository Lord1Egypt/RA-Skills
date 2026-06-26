# OpenClaw Dream — 设计文档

> 记忆整理与自动化巩固方案，目标作为 OpenClaw 开源 Skill 发布

## 一、Claude Code Auto Dream vs OpenClaw/Baikal 现状对比

### Claude Code Auto Dream

| 维度 | 实现 |
|------|------|
| 触发方式 | 自动（24h + 5 sessions 双门控） |
| 执行者 | 后台 sub-agent |
| 数据源 | session transcript JSONL + memory files |
| 操作范围 | 只改 memory 文件，不碰代码 |
| 核心操作 | 日期绝对化、矛盾删除、重复合并、过时清理、索引修剪（200行上限） |
| 手动触发 | `/dream` 命令 |
| 安全 | lock file 防并发，只读代码 |
| 理论基础 | Sleep-time Compute 论文（空闲时间做预处理） |

**优势：**
- 全自动，用户无感
- 有明确的行数上限（200行），防止 MEMORY.md 膨胀
- 从 session transcript 挖掘高价值信号（不只靠 memory 文件本身）
- 双门控避免无效运行

**劣势：**
- 仅限 Claude Code 的项目场景（单项目、单用户）
- 不支持多 agent 记忆协调
- 不支持自定义整理规则
- 没有记忆分类/分级（所有记忆平等对待）
- 遗忘策略单一（没有 importance scoring 和 time decay）
- 不支持跨项目记忆迁移
- 闭源，服务端 feature flag 控制，用户无法自定义

### OpenClaw/Baikal 现状

| 维度 | 实现 |
|------|------|
| 触发方式 | Heartbeat 半自动（AGENTS.md 里写了规则但执行靠自觉） |
| 执行者 | 主 agent 自己做（占用主进程） |
| 数据源 | memory/*.md + MEMORY.md + self-improving JSONL |
| 操作范围 | MEMORY.md + TOOLS.md + playbooks/ |
| 核心操作 | 手动 review + 提炼，不够系统化 |
| 手动触发 | 无专用命令 |
| 安全 | 无 lock file |
| 额外能力 | self-improving 分类记录（error/correction/best_practice/decision） |

**优势：**
- 记忆分类分级（不同类型不同文件）
- 多层记忆（JSONL → daily notes → MEMORY.md → TOOLS.md/playbooks）
- 有 self-improving 框架（自动捕获错误和纠正）
- 多 agent 架构可扩展
- 开源可定制

**劣势：**
- 没有自动化执行——全靠 heartbeat 里的"自觉"
- 日期绝对化没做
- 矛盾检测没做
- 重复合并没做
- 没有行数上限控制
- 占用主进程（heartbeat 做整理会阻塞用户消息）

---

## 二、设计目标

做一个比 Claude Code Auto Dream 更好的方案：

1. **自动触发 + 后台执行**：不占主进程
2. **记忆分类感知**：不同类型记忆用不同整理策略
3. **多 agent 安全**：lock file + 幂等性
4. **可观测**：整理完生成 changelog
5. **可配置**：用户可自定义规则、阈值、保留策略
6. **作为 Skill 发布**：任何 OpenClaw 用户都能安装使用

---

## 三、架构设计

### 命名

**`openclaw-dream`** — 致敬 Claude Code，但做得更好。

### 触发机制

利用 OpenClaw 已有的 **cron** 机制（不是 heartbeat）：
- 默认每 24h 执行一次（凌晨 3-4 AM）
- 条件检查：距上次 dream ≥ N 小时 AND 累积 ≥ M 条新记忆
- 手动触发：用户说 "dream" / "整理记忆" / "consolidate memory"

### 执行方式

用 **sessions_spawn** 启动独立 sub-agent，不阻塞主进程：
- runtime: "subagent"
- model: 用便宜模型（sonnet 而非 opus）
- 完成后主 agent 收到通知，可选择汇报结果

### 四阶段流程

```
Phase 1: Scan（扫描）
  ├── 读 MEMORY.md
  ├── 读 memory/*.md（最近 N 天）
  ├── 读 self-improving JSONL
  └── 生成当前状态快照

Phase 2: Analyze（分析）
  ├── 检测相对日期（"昨天"、"上周"、"最近"）
  ├── 检测矛盾条目（同一主题不同结论）
  ├── 检测重复内容（语义相似度 > 阈值）
  ├── 检测过时条目（引用已不存在的文件/配置）
  ├── 检测低重要性条目（noise filtering）
  └── 生成问题清单

Phase 3: Consolidate（整理）
  ├── 相对日期 → 绝对日期
  ├── 矛盾条目 → 保留最新，删除旧的
  ├── 重复条目 → 合并为一条
  ├── 过时条目 → 标记删除
  ├── JSONL 高频模式 → 提炼为规则写入 MEMORY.md
  ├── daily notes 关键事件 → 提炼为长期记忆
  └── 记忆总行数 → 控制在上限内

Phase 4: Write（写入）
  ├── 更新 MEMORY.md
  ├── 更新向量索引（openclaw memory index）
  ├── 生成 changelog（memory/dream-log-YYYY-MM-DD.md）
  ├── 更新 .last_dream 时间戳
  └── （可选）通知用户整理结果摘要
```

### 比 Claude Code 做得更好的地方

| 维度 | Claude Code | OpenClaw Dream |
|------|-------------|----------------|
| 记忆分类 | 无区分 | 按类型不同策略（事实 vs 教训 vs 配置 vs 人物） |
| 重要性评分 | 无 | 整理时对每条记忆评分，低分的降级/删除 |
| 时间衰减 | 无 | 旧记忆权重降低，但"经验教训"类永不过期 |
| 多 agent | 不支持 | lock file + agent-aware（不同 agent 的记忆隔离） |
| 整理日志 | 无 | 每次生成 dream-log，可审计 |
| 自定义规则 | 不支持 | SKILL.md 配置 + DREAM.md 自定义规则文件 |
| 触发灵活性 | 24h+5session 固定 | cron + 手动 + heartbeat 多种方式 |
| 向量索引 | 无 | 整理后自动重建 memory_search 索引 |
| 记忆来源 | session transcript | daily notes + JSONL + MEMORY.md（更丰富） |

### 配置项

```yaml
# DREAM.md 或 skill 配置
schedule: "0 3 * * *"          # cron 表达式，默认每天凌晨 3 点
min_hours: 24                   # 距上次 dream 最少间隔
min_new_entries: 10             # 最少新记忆条数
max_memory_lines: 200           # MEMORY.md 行数上限
model: "sonnet"                 # 用便宜模型
importance_threshold: 3         # 1-10，低于此分数的降级
decay_days: 30                  # 超过 N 天的非永久记忆降权
keep_categories:                # 这些分类永不自动删除
  - "经验教训"
  - "人物关系"
  - "安全规则"
notify: true                    # 整理完通知用户
changelog: true                 # 生成 dream-log
```

---

## 四、实现计划

### Phase 1：核心 Skill（本周）
1. 创建 `openclaw-dream` skill 目录结构
2. 写 SKILL.md（触发规则 + 四阶段流程详细指令）
3. 写 `scripts/dream.py`（扫描 + 分析逻辑）
4. 在 Baikal 上测试

### Phase 2：自动化集成（下周）
1. 配置 cron job 自动触发
2. 实现 lock file 防并发
3. 实现 dream-log 生成
4. 测试边界情况（空记忆、超大记忆、并发）

### Phase 3：发布到 ClawHub（下周末）
1. 按 AgentSkills spec 打包
2. 写 README + 使用文档
3. `clawhub publish`
4. 在 OpenClaw Discord/GitHub 社区推广

---

## 五、开放问题

1. **要不要支持 "选择性遗忘"？** — 用户可以标记某些记忆为"不可删除"
2. **跨 agent 记忆同步？** — Lake 和 Baikal 的记忆是否应该有同步机制
3. **记忆冲突解决策略？** — 当两条记忆矛盾时，默认保留最新，还是让用户确认？
4. **是否需要 dry-run 模式？** — 先展示要改什么，用户确认后再执行

---

*created: 2026-03-28*
