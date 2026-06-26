---
name: idea-darwin-zh
version: 1.0.0
emoji: 🧬
homepage: https://github.com/warmskull/idea-darwin
description: |
  Idea Darwin 引擎（中文版）— 自动化 idea 迭代系统，通过结构化竞争与选择进化原始想法。从 ideas.md 导入想法，将其结构化为带评分的卡片，然后运行迭代轮次：深化、派生、交叉、批判、验证，最终让高潜力 idea 浮现。使用 /idea-darwin 触发。当用户提到"跑一轮"、"迭代 idea"、"idea 池"、"idea 打分"、"idea 状态"、"头脑风暴迭代"、"进化我的想法"、"给 idea 排名"、"idea 流水线"时也应触发本 skill。即使用户没有显式说 /idea-darwin，只要任务涉及从文件中结构化想法、给 idea 打分排序、或运行任何形式的系统化 idea 迭代与筛选流程，都应使用本 skill。
---

# Idea Darwin 引擎

基于轮次的 idea 迭代系统，将想法视为竞争中的生命体 — 通过评分、选择、交叉、进化的结构化轮次，让最强的概念浮现出来。

核心隐喻是达尔文选择：评分高的 idea 存活并进化；弱 idea 被标记供用户决策；交叉产生新物种。这从根本上解决了头脑风暴的常见失败模式 — 所有想法永远停留在同样模糊的状态。

## 命令

| 命令 | 说明 |
|---|---|
| `/idea-darwin init` | 初始化：解析 ideas.md，创建目录结构、配置文件和初始卡片（支持可选参数，见下方） |
| `/idea-darwin round` | 执行下一个迭代轮次 |
| `/idea-darwin round N` | 连续执行 N 个轮次 |
| `/idea-darwin status` | 查看 idea 池状态和排名 |
| `/idea-darwin dormant IDEA-XXXX` | 将指定 idea 设为休眠 |
| `/idea-darwin wake IDEA-XXXX` | 唤醒休眠中的 idea |
| `/idea-darwin` | 无参数：显示简要状态并建议下一步 |

参数从 `$ARGUMENTS` 中提取。未提供参数时显示当前状态和建议。

### init 可选参数

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--budget <N>` | 每轮最多处理的 idea 数量 | `12` |
| `--actions <N>` | 每个 idea 每轮最多执行的动作数 | `2` |
| `--disruption <N>` | 每 N 轮引入一次外部刺激（扰动轮） | `3` |

示例：`/idea-darwin init --budget 8 --actions 3 --disruption 5`

以上参数写入 config.yaml，之后可手动修改。未指定的参数使用默认值。

## 文件结构

系统在工作目录中维护以下结构（初始化时创建）：

```
project/
├── ideas.md          # 用户的原始想法（只读 — 永远不要修改此文件）
├── config.yaml       # 系统配置与状态
├── stimuli.md        # 外部刺激条目（用户可编辑，系统只读）
├── cards/            # Idea 卡片
│   ├── IDEA-0001.md
│   └── ...
├── rounds/           # 轮次报告
│   ├── round-000.md
│   └── ...
├── reports/          # 排行榜和聚类报告
│   └── leaderboard.md
└── graph/            # 关系图谱
    └── relations.json
```

## Idea 编号

- 格式：`IDEA-XXXX`（4 位零填充，从 0001 开始）
- 全局唯一 — 编号永不回收，即使 idea 休眠或被移除
- `config.yaml` 中的 `next_idea_id` 追踪下一个可用编号
- 每张卡片通过 `parent_ids` 和 `child_ids` 记录血统关系

## Idea 状态机

```
seed → exploring → refining → crossing → validated → dormant
```

| 状态 | 含义 | 可用动作 |
|---|---|---|
| seed | 刚进入池 | 打标签、生成卡片、深化、快速交叉验证 |
| exploring | 探索阶段 | 深化、派生、批判、初步交叉 |
| refining | 打磨阶段 | 逻辑加固、可行性分析、风险审查 |
| crossing | 高交叉阶段 | 与互补 idea 融合、评估融合质量 |
| validated | 已验证 | 输出 MVP 方案、生成执行路线图 |
| dormant | 休眠中 | 仅被动参与交叉和相似度匹配 |

状态转换由系统基于分数和动作结果推荐，但用户始终拥有最终决定权。

## 评分系统

### 6 个评分维度（每项 1–10 分）

| 维度 | 权重 | 含义 |
|---|---|---|
| 创新性 (Novelty) | 0.10 | 是否有真正的突破，还是简单重复？ |
| 可行性 (Feasibility) | 0.20 | 技术、资源、路径上是否可行？ |
| 潜在价值 (Value) | 0.20 | 做成后能产生多大影响？ |
| 逻辑完整性 (Logic) | 0.20 | 是否自洽，有无明显漏洞？ |
| 交叉潜力 (CrossPotential) | 0.10 | 与其他 idea 碰撞出新东西的可能性？ |
| 可验证性 (Verifiability) | 0.20 | 能否设计实验或最小验证路径？ |

### 三层评分公式

评分分三层，每层捕捉不同的战略视角 — Survival 衡量独立质量，Development 衡量成长潜力，Priority 混合两者并加入时效性和多样性加成，防止 idea 池陷入局部最优。

```
Survival = 0.10×Novelty + 0.20×Feasibility + 0.20×Value
         + 0.20×Logic + 0.10×CrossPotential + 0.20×Verifiability

Development = 0.30×Novelty + 0.30×CrossPotential
            + 0.20×VariationPotential + 0.20×Freshness

Priority = 0.50×Survival + 0.30×Development
         + 0.10×NewIdeaBoost + 0.10×DiversityBonus
```

- **变异潜力 (VariationPotential)**（0–10）：此 idea 还能分出多少种不同方向。随子代增多而递减。
- **新鲜度 (Freshness)**（0–10）：此 idea 最近是否有变化？连续多轮未被处理时衰减。
- **新 idea 加成 (NewIdeaBoost)**：新入池 idea 前 2 轮 +2，之后归零。
- **多样性加分 (DiversityBonus)**：池中代表性不足的类别 +1–2。

评分时参考 `references/prompts.md` 中的 Prompt 模板。

## 初始化流程

用户执行 `/idea-darwin init` 时：

1. **定位 ideas.md**
   - 检查当前目录是否存在 ideas.md
   - 若未找到，使用 `AskUserQuestion` 询问路径

2. **创建目录和配置**
   - 创建 cards/、rounds/、reports/、graph/
   - 生成 config.yaml（合并用户提供的可选参数；未指定的使用默认值）：

```yaml
source:
  ideas_file: "./ideas.md"
counter:
  next_idea_id: 1
  current_round: 0
schedule:
  max_ideas_per_round: 12      # --budget
  max_actions_per_idea: 2       # --actions
disruption:
  trigger_every_n_rounds: 3     # --disruption
  wildcard_budget_ratio: 0.10
```

   - 在项目根目录生成 `stimuli.md`（外部刺激文件），包含初始模板和编辑说明

3. **解析 ideas.md**
   - 识别每个独立 idea（通常以 ## 标题分隔）
   - **不修改 ideas.md** — 始终只读

4. **为每个 idea 生成卡片**
   - 分配 ID（从 IDEA-0001 开始）
   - 打标签（主题 / 问题类型 / 阶段 / 风格 / 资源标签）
   - 按 `assets/card-template.md` 格式生成完整卡片
   - 初始评分（6 维度 + 三层综合分数）
   - 写入 cards/IDEA-XXXX.md

5. **生成 round-000.md 报告**
   - 列出所有初始卡片摘要、分数和建议下一步
   - 写入 rounds/round-000.md

6. **向用户展示结果**
   - 展示所有卡片的汇总表（ID、标题、分数、建议动作）
   - 告知用户 `stimuli.md` 及其使用方式：
     > `stimuli.md` 已在项目根目录创建。每隔 N 轮，系统会随机选取最多 5 条已启用的条目作为外部刺激，打破思维惯性。
     > 你可以随时编辑此文件来添加/修改/禁用条目。每条格式如下：
     > ```
     > ## [条目标题]
     > - status: enabled / disabled
     > - [内容描述]
     > ```
   - 等待用户确认后进入正式轮次循环

## 轮次执行流程

用户执行 `/idea-darwin round` 时，严格按以下 9 步顺序执行：

### 第 1 步：导入新想法
- **每轮开始时检查默认 idea 文档**：读取 config.yaml 中 `source.ideas_file` 指向的文件
- 将默认 ideas.md 与现有卡片对比，识别新增内容
- 新 idea：打标签 → 生成卡片 → 初始评分
- 新 idea 标记为 `stage: seed`，获得 NewIdeaBoost
- **这是每轮的强制前置步骤** — 系统不能只循环处理已有卡片而忽略源文件的增量更新

### 第 2 步：更新关系图谱
- 基于所有卡片的标签和内容，计算 idea 间的相似度
- 识别潜在交叉候选（高相似度 = 近邻交叉候选；低相似度但互补 = 远距交叉候选）
- 更新 graph/relations.json

### 第 3 步：全局评分刷新
- 为所有 **活跃** idea（非休眠）重新计算 6 维评分
- 更新 Survival / Development / Priority
- 标记：高潜力（Priority > 7）、停滞（连续 3+ 轮无变化）、低潜力（Priority < 3）

### 第 4 步：预算分配
根据 `max_ideas_per_round` 分配处理名额：
- 25% 给新入池 idea
- 30% 给高优先级 idea 的深化
- 20% 给高潜力 idea 的派生
- 15% 给交叉实验
- 10% 给扰动 / 随机探索

按 Priority Score 降序选取 idea。每个 idea 最多获得 `max_actions_per_idea` 个动作。

### 第 5 步：决定动作
为每个选中的 idea 分配动作，基于状态机（参见上方表格）。
当状态机不足以决策时，使用分数驱动规则：
- `高创新 + 低可验证` → 深化
- `高创新 + 高交叉潜力` → 交叉
- `高价值 + 低可行性` → 批判 + 打磨
- `高可行性 + 低逻辑` → 深化
- `高重复度` → 合并

### 第 6 步：执行动作
逐一处理选中的 idea。动作的详细执行规范参见 `references/actions.md`，Prompt 模板参见 `references/prompts.md`。

**每个 idea 的执行流程：**
1. 读取完整卡片
2. 按对应动作类型的 Prompt 模板执行 — 深入思考
3. 产出结构化输出：
   - 更新后的卡片内容
   - 新派生 idea（自动分配 ID，双向更新 parent_ids/child_ids）
   - 分数变化
   - 发现的风险
   - 建议的下一步动作
4. 写入更新后的卡片文件

新派生 idea 同样需要完整的卡片生成和初始评分。

### 第 7 步：验证与去重
- 对所有新产生的 idea 执行 **双层验证**：
  - 第一层（硬伤检查）：逻辑矛盾？缺乏真实需求？完全不可落地？高度重复？
  - 第二层（价值判断）：是否值得继续？下一步做什么？最大风险是什么？
- 验证失败 → 标记 `validated: false`，降低优先级，报告给用户
- **用户决定** 是否休眠或移除 — 系统仅推荐
- 对全池进行相似度检查，合并高度重复的 idea

### 第 8 步：生成轮次报告
写入 `rounds/round-XXX.md`，包含：
- 本轮处理的 idea 和执行的动作
- 新产生的 idea 摘要
- Top 5 分数变化（升/降）
- 验证未通过的 idea（需要用户决策）
- 下轮推荐优先处理项
- 若为扰动轮：使用了哪些外部刺激，应用了哪些创新框架

### 第 8.5 步：输出轮次简报

所有文件更新完成后，**在对话中直接输出一份轮次简报**（不写入文件），让用户无需打开任何文件即可全面了解情况。格式：

```
## 第 N 轮简报

### 执行动作
| ID | 标题 | 动作 | 关键产出 |
|---|---|---|---|
| IDEA-XXXX | ... | 深化/派生/交叉/批判/... | 一句话总结 |

### 卡片变化
| ID | 标题 | 分数变化 | 状态变化 | 备注 |
|---|---|---|---|---|
| IDEA-XXXX | ... | Priority X.XX→X.XX | seed→exploring | 变化原因 |

### 新 Idea（详情）

本轮新产生的每个 idea：

#### IDEA-XXXX: [标题]
- **来源**：[交叉/派生/刺激] 来自 IDEA-XXXX + IDEA-XXXX
- **核心问题**：[一段话]
- **关键洞察**：[这个 idea 最有价值的地方]
- **初始分数**：Priority X.XX（Survival X.XX / Development X.XX）
- **当前张力**：[最大的未决问题]
- **建议下一步**：[深化/派生/交叉/批判 + 具体方向]

### 当前排名
| 排名 | ID | 标题 | Priority | 阶段 |
|---|---|---|---|---|

### 下轮预告
- [建议优先处理项]
- [是否即将进入扰动轮]

### 需要你做决定的事项
> 列出本轮需要用户决策的关键事项。每项 **必须包含 idea 的完整标题**（而非仅 ID），附带上下文和建议选项。
> 示例：
> 1. **IDEA-0002 "编程学习 Agent 教程网站" 与 IDEA-0004 "渐进式拆箱教学法" 高度重叠** — 合并还是重新定位？建议：[...]
> 2. **IDEA-0006 "自动诊断线程" 验证未通过** — 休眠、转向还是继续观察？
> 3. **IDEA-0003 "热管理本体论" 被降级** — 是否接受从本体论降级为结构化 Excel 作为第一步？
>
> 如果本轮不需要用户决策，写"本轮无需用户决策。"
```

此简报是用户与系统之间的主要交互界面 — 保持完整且易读。"需要你做决定的事项"是最重要的交互触点：系统应清晰列出决策事项和推荐方案，而非让用户自己从报告中挖掘问题。

### 第 9 步：保存状态
- 更新所有修改过的卡片文件
- 在 config.yaml 中递增 `current_round`
- 更新 `next_idea_id`
- 更新 reports/leaderboard.md（Top 10 排名）

## 外部刺激与扰动轮

每隔 `trigger_every_n_rounds` 轮（默认 3），引入外部刺激进行"扰动轮"。目的是防止 idea 池收敛到局部最优，强制引入新视角。

### 外部刺激文件 (stimuli.md)

`stimuli.md` 位于项目根目录。初始化时创建，由用户维护。格式：

```markdown
## 行业趋势：具身 AI 加速落地
- status: enabled
- 2026 年具身 AI 从实验室走向产线，机器人运营成本下降 60%

## 技术变革：统一多模态模型架构
- status: enabled
- 视觉、语言、代码统一到单一模型中，API 范式正在改变

## 反共识观点：SaaS 已死
- status: disabled
- 开源 + 自部署正在替代传统 SaaS 订阅模式
```

- 每条：`##` 标题 + `status` 字段 + 内容描述
- `enabled` = 参与随机选取；`disabled` = 跳过
- 用户可随时添加、编辑或切换条目
- 系统仅读取此文件 — 永远不写入

### 扰动轮机制

1. **打乱优先级**：给低优先级但有新意的 idea 浮出水面的机会
2. **远距交叉**：强制交叉标签不重叠的 idea
3. **外部刺激**：从 stimuli.md 中随机选取最多 5 条已启用条目
4. **假设反转**：对高分 idea 追问"如果核心假设是错的呢？"
5. **创新框架**：应用 SCAMPER / 第一性原理 / 类比迁移 / 约束反转 / 极端用户视角

每轮还保留 `wildcard_budget_ratio`（默认 10%）的名额用于非最优路径探索。

## 休眠与唤醒

### `/idea-darwin dormant IDEA-XXXX`
1. 读取卡片，将 stage 设为 `dormant`
2. 在卡片的"休眠记录"中记录原因和轮次
3. 该 idea 不再被选中进行深化/派生，但仍被动参与交叉和相似度匹配

### `/idea-darwin wake IDEA-XXXX`
1. 读取卡片，将 stage 恢复到休眠前的状态（从历史推断，通常为 `exploring`）
2. 更新"休眠记录"

系统**永远不会**自动休眠任何 idea。只有用户才能做这个决定。

## `/idea-darwin status`

读取 config.yaml 和所有卡片，然后输出：
- 当前轮次
- 池中 idea 总数（按状态分类）
- Top 10 排名（按 Priority Score 降序）
- 最近一轮处理了什么
- 建议下一步

## 关键约束

1. **ideas.md 只读**：永远不修改用户的 ideas.md
2. **编号不回收**：在任何情况下编号都不重复使用
3. **分支限制**：每个 idea 每轮最多派生 2–3 个子代
4. **每轮去重**：轮次结束前必须进行相似度检查
5. **用户主权**：系统永远不自动休眠或移除 idea — 仅推荐
6. **结构化输出**：每个动作必须产出结构化结果
7. **卡片格式一致**：所有卡片严格遵循 `assets/card-template.md`
8. **报告可追溯**：每份轮次报告必须包含完整操作日志

## 参考文件

- `references/actions.md`：每种标准动作的详细规范和使用场景
- `references/prompts.md`：每种动作的 Prompt 模板
- `assets/card-template.md`：卡片文件模板
