---
name: luban-skill
description: "鲁班.Skill（luban Skill）：工业级智能体技能优化器。当用户提及以下关键词时调用：“优化skill”、“skill评分”、“自动优化”、“auto optimize”、“skill质量检查”、“小鲁班”、“luban”、“优化技能”、“帮我改skill”、“skill怎么样”、“提升skill质量”、“skill review”、“skill打分”。"
---

# 鲁班.Skill

> 天工开物 工匠鲁班

>
>
> 核心理念：**技能不是写完就完的静态文档，而是在评估→改进→验证→巡检→硬化→精简的闭环中持续生长的活资产。**

---

## 底座架构

```
                          ┌────────────────────────────────┐
                          │       技能自进化调度器           │
                          │   事件驱动 + 定时轮询 + 按需    │
                          └──────┬─────────────────────────┘
      ┌──────────┬─────────┬────┼────┬──────────┬──────────┐
      ▼          ▼         ▼    ▼    ▼          ▼          ▼
  ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐
  │ 核心   ││EvoSkill││SkillOps││CASCADE ││ Distill││  HASP  │
  │Darwin  ││ 失败   ││ 定期   ││ 知识   ││ 精简   ││ 规则   │
  │优化循环││ 驱动   ││ 体检   ││ 更新   ││ 瘦身   ││ 硬化   │
  │(P0-P3) ││ 修补   ││        ││        ││        ││        │
  └────┬───┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘└───┬────┘
       │        │         │         │         │         │
       └────────┴─────────┴────┬────┴─────────┴─────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   技能文件仓库        │
                    │ SKILL.md + refs/ +  │
                    │ tests.yaml +         │
                    │ results.tsv          │
                    └─────────────────────┘
```

**调度优先级**：事件驱动（立即）> 按需触发（用户指令）> 定时轮询（周/月/季）

**并发控制**：同一技能同时只运行一个进化任务，新任务排队。

---

## 一、核心引擎：Darwin 优化循环（保留自 v2.0）

### 评估 Rubric（9维度，总分100）

> 依据 SkillLens (arXiv 2605.23899)：LLM-as-judge 准确率仅 46.4%，加入 meta-skill 三维度后提升到 73.8%。

#### 结构维度（59分）— 静态分析

| # | 维度 | 权重 | 评分标准 |
|---|------|------|---------|
| 1 | Frontmatter质量 | 7 | name规范、description包含做什么+何时用+触发词、≤1024字符、禁结尾加空话尾巴 |
| 2 | 工作流清晰度 | 12 | 步骤明确可执行、有序号、每步有明确输入/输出 |
| 3 | 失败模式编码 | 12 | 必须显式编码失败模式；有fallback路径、错误恢复；只写正向流程扣 ≥3 分 |
| 4 | 检查点设计 | 6 | 关键决策前有用户确认、显性标记（🔴/STOP/CHECKPOINT） |
| 5 | 可执行具体性 | 17 | 不模糊、有具体参数/格式/示例；禁止"建议/可以考虑/根据情况"等软化措辞，≥3 处扣 ≥3 分 |
| 6 | 资源整合度 | 4 | references/scripts/assets引用正确、路径可达 |

#### 效果维度（35分）— 需实测

| # | 维度 | 权重 | 评分标准 |
|---|------|------|---------|
| 7 | 整体架构 | 12 | 层次清晰、不冗余不遗漏；冗余/AI腔废话扣分 |
| 8 | 实测表现 | 23 | 用测试prompt跑一遍，输出质量是否符合宣称能力 |

#### Meta-skill 维度（6分）— 反例与黑名单

| # | 维度 | 权重 | 评分标准 |
|---|------|------|---------|
| 9 | 反例与黑名单 | 6 | 必须有"不要做什么"的反例清单；没有扣 ≥3 分 |

评分规则：维度1-7、9 各打 1-10 分×权重；维度8 跑 2-3 个测试 prompt 打分。总分 = Σ(维度分×权重)/10，满分 100。改进后总分必须严格高于改进前。

关于「实测表现」维度：用子 agent 独立执行，带 skill vs 不带 skill baseline 对比输出质量。子 agent 不可用时退化为干跑验证（标注 `dry_run`），但 dry_run 比例 >30% → 评估失效警告。

### Runtime 适配性审查（gate 项）

skill 应能在 Claude Code / Codex / Cursor / OpenClaw / Hermes / Gemini CLI / OpenCode 等 50+ runtime 通用。Phase 1 基线评估时强制跑红灯扫描：grep 命中 `在 Claude Code`、`Claude Code skill` 等措辞 → 强制 P0 修复。

### Phase 0: 初始化

```
1. 确认优化范围（全部/指定 skill）
2. 创建 git 分支：auto-optimize/YYYYMMDD-HHMM
3. 初始化 results.tsv（如不存在）
4. 读取现有 results.tsv 了解历史记录
```

### Phase 0.5: 测试 Prompt 设计

```
for each skill:
  1. 读取 SKILL.md
  2. 设计 2-3 个测试 prompt（覆盖典型场景 + 复杂/歧义场景）
  3. 保存到 skill 目录/test-prompts.json
```

展示所有测试 prompt 给用户，确认后再进入评估。

### Phase 1: 基线评估

```
for each skill:
  # 结构评分（主 agent）
  1. 读取 SKILL.md 全文，按维度 1-7 逐项打分
  # 效果评分（子 agent 独立）
  2. 对每个测试 prompt，spawn 子 agent 跑带/不带 skill 对比
  3. 打维度 8 分
  # 汇总
  4. 计算加权总分，记录到 results.tsv
```

🔴 CHECKPOINT：暂停等用户确认，再进入优化循环。

### Phase 2: 优化循环

```
for each skill (按分数从低到高):
  round = 0
  while round < MAX_ROUNDS (默认3):
    round += 1
    1. 诊断：找得分最低维度（注意 dim2/3/4 是相关簇）
    2. 提出改进方案（改什么、为什么、预期提升）
    3. 执行改进，git commit
    4. 重新评估（结构+效果，必须用独立子 agent）
    5. 决策：新总分 > 旧总分 → keep；否则 revert
       - 连续 2 轮 Δ < 2 分 → break（触顶）
    6. 追加 results.tsv
  🔴 CHECKPOINT：每个 skill 优化完后展示 diff + 分数变化，等用户确认
```

### Phase 2.5: 探索性重写（按需）

连续 2 个 skill 都在 round 1 就 break → 提议一次探索性重写（git stash → 从头重写 → 对比评估 → 择优保留）。🔴 必须征得用户同意。

### Phase 3: 汇总报告

输出优化总数、保留/回滚比例、分数变化表、主要改进摘要。

### results.tsv 格式

```tsv
timestamp	commit	skill	old_score	new_score	status	dimension	note	eval_mode
```

---

## 二、EvoSkill 模块：失败驱动的技能修补

> 论文：[arXiv:2603.02766](https://arxiv.org/abs/2603.02766)
> 核心理念：让 AI 从失败中自动发现能力缺口，自主构建修补方案。

### 触发条件

- 用户明确反馈技能执行不符合预期（"不对""没效果""缺少XX""这个技能有问题"）
- Agent 执行时遇到技能未覆盖的场景导致失败

### 缺口分类

| 缺口类型 | 判定特征 |
|----------|---------|
| 触发词遗漏 | 用户输入含关键意图但技能未触发 |
| 规则缺失/模糊 | 技能没有覆盖用户场景的指引 |
| 指令冲突 | 多条规则给出矛盾建议 |
| 流程漏洞 | 技能规定的流程某环节不可行 |
| 输出格式不当 | 技能输出格式不符合预期 |
| 版本兼容 | 依赖的外部工具版本已变更 |

### 执行流程

```
Step 1: 捕获失败上下文
  - 用户的原始指令
  - 技能被调用的完整参数
  - 技能执行后的输出/报错
  - 用户的具体反馈

Step 2: 定位缺口
  - 按缺口分类表判定类型
  - 定位技能文件中需修改的具体位置（文件路径 + 行号范围）

Step 3: 生成补丁
  - 给出 old_str → new_str 的具体修改内容
  - 附带修改理由
  - 状态：待用户确认

Step 4: 输出修复建议
```

### 输出格式

```markdown
## 🔧 EvoSkill 修复建议

**目标技能**：{skill_name}
**缺口类型**：{type}
**定位**：{file}:{line}

**当前**：{old_str}
**建议**：{new_str}
**理由**：{reason}

[待确认]
```

---

## 三、SkillOps 模块：定期健康巡检

> 论文：[arXiv:2605.13716](https://arxiv.org/abs/2605.13716)
> 核心理念：将技能库维护形式化为独立的「库时」问题，五维诊断 + 自动维护。

### 触发条件

- 定时任务：每周自动执行
- 用户指令："检查技能健康""技能体检""巡检"

### 五维诊断矩阵

| 维度 | 检查项 | 严重程度 |
|------|--------|----------|
| 效用 | SKILL.md 每条规则是否有触发条件；references 是否被引用 | 🟡/🟢 |
| 冗余 | 内容高度重复的 references；SKILL.md 中可合并的段落 | 🟢 |
| 兼容性 | 文件路径引用断裂；外部链接失效；YAML 非法 | 🔴/🟡/🔴 |
| 失败风险 | 未定义触发条件的强制规则；规则粒度过粗 | 🟡/🟢 |
| 验证缺口 | 缺少对应 rules 的验证步骤；references 缺示例和反例 | 🟡/🟢 |

### 维护动作（对齐 SkillOps 原论文概念）

| 动作 | 含义 | 示例 |
|------|------|------|
| `merge` | 合并内容高度重复的 references（相似度 > 0.8） | ref-a.md + ref-b.md → ref-merged.md |
| `repair` | 修复断裂引用或非法格式 | 路径 /old/path.md 不存在 → 改为 /new/path.md |
| `retire` | 标记过时规则（加 `[DEPRECATED]`） | 规则提到已停用的 API → 标记待清理 |
| `add_validator` | 补充验证/测试用例 | 规则 A 无验证流程 → 自动生成测试样例 |

### 执行流程

```
Step 1: 加载目标技能文件（SKILL.md + references/ 下所有文件）
Step 2: 逐维度扫描
  - 工具化扫描：Python 脚本做结构分析（路径、YAML、引用链）
  - 语义化扫描：Agent 做内容分析（规则一致性、重复、歧义）
Step 3: 汇总诊断报告（按 🔴 > 🟡 > 🟢 排序）
Step 4: 生成维护动作清单（输出报告，不自动修改）
```

### 输出格式

```markdown
## 🏥 SkillOps 健康巡检 —— {skill_name} —— {date}

| # | 严重程度 | 位置 | 问题描述 | 建议动作 |
|---|---------|------|----------|----------|
| 1 | 🔴 | SKILL.md:42 | 引用路径断裂 | repair |
| 2 | 🟡 | ref-faq.md | 规则缺少验证 | add_validator |
| 3 | 🟢 | ref-a.md + ref-b.md | 内容高度重复 | merge |
```

---

## 四、CASCADE 模块：领域知识自动更新

> 论文：[arXiv:2512.23880](https://arxiv.org/abs/2512.23880)
> 核心理念：两大元技能驱动——持续学习（web_search/代码提取/记忆利用）+ 自我反思（内省/知识图谱探索）。

### 触发条件

- 定时任务：每季度自动执行
- 用户指令："更新技能知识""补最新""刷新 references"
- 技能 references 中引用外部知识且距上次更新 > 90 天

### 执行流程

```
Step 1: 扫描 references/ 目录
  - 识别所有外部引用（arXiv ID、API 文档 URL、标准编号等）
  - 记录每个引用的最后更新日期

Step 2: 筛选过时引用
  - 距上次更新 > 阈值 → 标记待更新
  - 优先处理用户最近高频使用的技能

Step 3: 知识检索
  - 论文：搜索引用 arXiv ID，检查是否有新版本
  - API：抓取最新文档，对比 changelog
  - 标准：搜索是否发布了新版本

Step 4: 自我反思（内省）
  - 对比新旧知识差异
  - 判断是否影响技能规则的有效性
  - 仅在有实质性变化时生成更新

Step 5: 追加式更新
  - 追加新知识（不删除旧内容，标注版本号）
  - 格式：## [YYYY-MM-DD] 更新：xxx → 新内容
```

### 关键设计

- 只追加不删除：旧知识的废弃留给 SkillOps 的 `retire` 动作
- 标注版本：每次更新附带日期和版本号
- 不自动修改规则：仅更新 references，不自动改 SKILL.md 中的规则引用

---

## 五、Skill Distill 模块：判断何时该精简

> 论文：[arXiv:2604.01608](https://arxiv.org/abs/2604.01608)
> 核心理念：指标自由度 F —— 第一个可先验计算的技能效用预测器，判断哪些内容可以精简。

### 触发条件

- SkillOps 体检报告中「冗余」维度评分低
- 技能 references 文件数超过 15 个
- 用户指令："精简技能""瘦身""技能太长了"

### 指标自由度 F 的近似计算

由于原论文 Mantel 检验需实际执行数据，使用启发式近似：

```
F_approx = 1 - (模块被规则引用的次数 / 模块总字符数归一化)
```

- F ≈ 1：模块内容庞大但很少被引用 → 可精简
- F ≈ 0：模块内容紧凑且多处引用 → 保留
- F_approx ≥ 0.7：标记「可精简」；≤ 0.3：标记「核心资产」

### 精简优先级

| 优先级 | 类型 | 处理 |
|--------|------|------|
| P0 | 完全未被引用的 references | 直接建议删除 |
| P1 | 文件大但仅 1-2 处引用 | 提取引用段落到 SKILL.md，删原文件 |
| P2 | 多处重复的示例代码块 | 合并为一个 reference |
| P3 | 历史版本累积的旧内容 | 归档到 archive/ 子目录 |

### 执行流程

```
Step 1: 构建引用矩阵
  - SKILL.md 每条规则 → 引用了 references/ 的哪些段落
  - 计算每个 references 文件的「有效引用密度」

Step 2: 计算 F_approx，分级标记

Step 3: 生成精简方案
  - 展示「删除后文件大小变化」预估
  - 标注「保留的核心内容」
  - 🔴 CHECKPOINT：待用户确认后执行
```

---

## 六、HASP 模块：将建议规则硬化

> 论文：[arXiv:2605.17734](https://arxiv.org/abs/2605.17734)
> 核心理念：技能升格为可执行程序函数（PF），含 should_activate + intervene，从"建议"变"硬纠正"。

### 触发条件

- 同一规则在同一场景下连续 2 次以上被忽略
- 用户指令："规则硬化""硬一点""这个规则总被忽略"

### 硬化层级

#### 层级 1：Should → Must（措辞强化）

```
原文：建议在生成 SKILL.md 时控制文件大小在 30KB 以内

硬化后：强制约束：SKILL.md 文件大小不得超过 30KB。
超限时，必须将详细内容拆分到 references/，SKILL.md 仅保留导航链接。
```

#### 层级 2：Should → PF（可执行程序函数）

在 SKILL.md frontmatter 中追加硬规则元数据：

```yaml
hard_rules:
  - id: rule_001
    should_activate: "SKILL.md 文件大小 > 30KB"
    intervene:
      type: "block_and_restructure"
      action: "禁止继续在 SKILL.md 追加内容，将超出部分写入新 reference 文件"
    severity: "critical"
    last_violated: "2026-06-10"
    violation_count: 3
```

### 执行流程

```
Step 1: 执行日志分析
  - 对比 SKILL.md 关键规则 vs 实际执行行为
  - 识别「规则被忽略」的实例

Step 2: 分级处理
  忽略 1 次 → 暂不处理
  忽略 2 次 → 生成措辞强化建议（层级 1）
  忽略 ≥3 次 → 生成 PF 硬化建议（层级 2）

Step 3: 硬化规则注入
  - 定义 should_activate 条件 + intervene 动作
  - 🔴 CHECKPOINT：待用户确认后执行
```

### 硬化适用性

| 规则类型 | 适合硬化 | 原因 |
|----------|---------|------|
| 输出格式约束 | ✅ | 可精确检测和修正 |
| 文件大小限制 | ✅ | 可精确检测 |
| 必须包含的章节/字段 | ✅ | 结构化检查 |
| 语义风格约束 | ❌ | 难以精确检测 |
| 创造性建议 | ❌ | 无法形式化 |

---

## 七、MUSE-Autoskill 模块：修改后自动回归测试

> 论文：[arXiv:2605.27366](https://arxiv.org/abs/2605.27366)
> 核心理念：双驱动评估（单元测试 + 运行反馈），自动触发修补和重测，首次实证跨智能体技能迁移。

### 触发条件

- 任何对技能文件（SKILL.md 或 references/）的编辑操作完成后
- 自动触发，无需用户指令

### 测试用例生成维度

| 维度 | 生成方法 | 示例 |
|------|----------|------|
| 触发词识别 | 从 SKILL.md 提取所有触发词，逐一构造输入 | 输入"小鲁班" → 预期触发 |
| 输出格式 | 提取格式约束，构造验收条件 | 输出必须包含 YAML frontmatter |
| 关键规则遵守 | 提取"必须"/"禁止"语句，构造边界测试 | 输入超限请求 → 预期拒绝 |
| 流程完整性 | 按技能 Step 列表逐项模拟 | Step 3 依赖 Step 2 的输出 → 断链测试 |
| references 可达性 | 遍历所有文件路径引用 | 逐条检查文件是否存在 |
| 反例测试 | 构造明确不在范围内的输入 | "帮我写操作系统" → 预期不触发 |

### 执行流程

```
Step 1: 修改前快照
  - 保存修改前完整文件 hash
  - 自动生成 5-10 条测试用例（基于 6 维度）

Step 2: 执行修改

Step 3: 回归测试
  - 逐条运行测试用例
  - 逐条检查修改后的技能行为

Step 4: 结果判定
  全部通过 → 「回归测试通过，无退化」
  部分失败 → 列出失败项 + 偏差 + 建议回滚
  全部失败 → 强制建议回滚

Step 5: 测试用例沉淀
  - 通过的用例追加到 tests.yaml
  - 形成持续增长的回归测试集
```

### tests.yaml 格式

```yaml
skill: {skill_name}
generated_at: {date}
tests:
  - id: trigger_001
    dimension: "触发词识别"
    input: "{test_input}"
    expected: "{expected_behavior}"
    status: pass | fail
    last_run: {date}
    
  - id: format_001
    dimension: "输出格式"
    condition: "{constraint}"
    check: "{check_method}"
    status: pass | fail
    last_run: {date}
```

---

## 八、调度器：触发策略

```
事件驱动（立即响应）
  ├── P0: 用户明确反馈技能错误         → EvoSkill
  ├── P0: 技能编辑操作完成              → MUSE 回归测试
  ├── P1: 同一规则连续忽略 3 次         → HASP 层级 2
  └── P2: 同一规则连续忽略 2 次         → HASP 层级 1

按需触发（用户指令）
  ├── "优化skill"/"技能打分"            → Darwin 核心引擎
  ├── "检查技能健康"/"体检"            → SkillOps
  ├── "更新技能知识"/"补最新"          → CASCADE
  ├── "精简技能"/"瘦身"               → Skill Distill
  └── "规则硬化"/"硬一点"             → HASP

定时驱动（周期扫描）
  ├── 每周：SkillOps 健康巡检
  ├── 每月：Skill Distill 精简检查（仅当冗余评分低时）
  └── 每季度：CASCADE 知识更新检查（仅当有外部引用时）
```

### 并发控制与冲突仲裁

| 场景 | 仲裁规则 |
|------|----------|
| 任何模块 vs 用户正在手动编辑 | 用户优先，模块排队 |
| SkillOps 巡检 vs 用户正在编辑 | 巡检只读执行，仅输出报告 |
| Skill Distill vs HASP 同时触发 | HASP 优先（质量保障），精简让步 |
| MUSE 回归测试运行中 | 锁定技能文件，其他模块等待 |
| 同一技能多个任务排队 | FIFO 顺序执行 |

---

## 九、异常与边界条件

| 场景 | 处理动作 |
|------|----------|
| 不在 git 仓库 | 询问用户：`git init` 或回退到文件备份 `.bak.YYYYMMDD-HHMM` |
| results.tsv 缺失 | 新建并写表头 |
| results.tsv 损坏 | 备份为 `.bak` 后重建 |
| 分支已存在 | 分支名加 `-2`/`-3`；第 3 次失败切回现有分支询问 |
| `git revert` 失败 | 先 `git stash` 重试；仍失败从上一个 commit 读 SKILL.md 手动恢复 |
| MAX_ROUNDS 触顶 | 展示最弱维度问用户「加 1 轮 / Phase 2.5 / 收工」 |
| 优化后超 150% 体积 | 拒绝提交，进精简流程 |
| test-prompts.json 已存在 | 默认复用，问用户「复用/重写/追加」 |
| SKILL.md 找不到 | 该 skill 终止，status=error，继续下一个 |
| dry_run 比例 > 30% | 评估失效警告，强制至少 1 个 full_test |
| 多个模块同时触发 | 按优先级排队，EvoSkill > MUSE > HASP > SkillOps > CASCADE > Distill |

**原则**：异常先告知用户，再按规则处理；绝不静默跳过。

---

## 十、反例黑名单（本底座自己优化时不做的事）

| # | 反模式 | 替代做法 |
|---|--------|----------|
| 1 | 同 context 自评自改 | 必须 spawn 独立子 agent 评分 |
| 2 | `git reset --hard` 当回滚 | 用 `git revert HEAD` 保留追溯链 |
| 3 | 为凑分增冗余 | 触顶信号（连续 2 轮 Δ<2）→ break |
| 4 | 跳过 test-prompts 直接评分 | Phase 0.5 强制设计 2-3 prompts |
| 5 | 轮内改多个维度 | 每轮 1 个维度 |
| 6 | dry_run 比例 > 30% | 强制至少 1 个 full_test |
| 7 | 静默跳过异常 | 异常表 fallback 必须先告知 |
| 8 | 忽视维度相关性单独优化 | 看相关簇短板再决定 |

---

## 十一、约束规则

1. **不改变技能核心功能和用途** — 优化"怎么写"，不改"做什么"
2. **不引入新依赖** — 不添加原本没有的 scripts 或 references
3. **每轮只改一个维度** — 避免多变量无法归因
4. **保持文件大小合理** — 优化后 ≤ 原大小 150%
5. **可回滚** — 所有改动在 git 分支上，用 `git revert` 而非 `reset --hard`
6. **评分独立性** — 效果维度必须用子 agent 或干跑验证
7. **Runtime 中立** — 技能必须能在任何 skills-compatible runtime 运行
8. **人在回路** — 所有修改操作必须经用户确认（只读扫描除外）
9. **追加优于覆盖** — CASCADE 知识更新只追加不删除旧内容

---

## 十二、使用方式

| 指令 | 触发模块 |
|------|----------|
| "优化所有 skills" | Darwin 核心引擎（全量） |
| "优化 {skill_name}" | Darwin 核心引擎（单个） |
| "评估所有 skills 质量" | Phase 0.5-1（仅评估不改） |
| "检查技能健康" | SkillOps 巡检 |
| "这个技能有问题 / 不对" | EvoSkill 失败修补 |
| "更新技能知识" | CASCADE 知识更新 |
| "精简技能 / 瘦身" | Skill Distill |
| "规则硬化 / 硬一点" | HASP 规则硬化 |
| "看看优化历史" | 读取 results.tsv |

---

## 十三、资源文件速查

| 路径 | 用途 |
|------|------|
| `results.tsv` | 历次优化日志（9 列含 eval_mode） |
| `{skill目录}/test-prompts.json` | 每个 skill 的测试 prompt |
| `{skill目录}/tests.yaml` | MUSE 回归测试用例（持续沉淀） |

---

## 学术依据

- **EvoSkill** (arXiv [2603.02766](https://arxiv.org/abs/2603.02766))：失败驱动的技能缺口发现与自动修补
- **SkillOps** (arXiv [2605.13716](https://arxiv.org/abs/2605.13716))：技能库运维框架，五维健康诊断
- **CASCADE** (arXiv [2512.23880](https://arxiv.org/abs/2512.23880))：持续学习 + 自我反思驱动的技能进化
- **Skill Distill** (arXiv [2604.01608](https://arxiv.org/abs/2604.01608))：指标自由度 F 驱动的精简决策
- **HASP** (arXiv [2605.17734](https://arxiv.org/abs/2605.17734))：技能升格为可执行程序函数
- **MUSE-Autoskill** (arXiv [2605.27366](https://arxiv.org/abs/2605.27366))：全生命周期管理 + 回归测试
- **SkillLens** (arXiv [2605.23899](https://arxiv.org/abs/2605.23899))：9 维 rubric 实证来源
- **SkillOpt** (arXiv [2605.23904](https://arxiv.org/abs/2605.23904))：validation-gated edits 形式化框架
- **autoresearch**：Karpathy 自主实验循环（v1.0 原始灵感）

---

> "Train your Skills like you train your models."
> — 技能自进化底座，站在 Darwin + 六篇论文的肩膀上。
