---
name: mu-self-evolve
version: "3.1.0"
description: "AI Agent 持续进化系统：每日经验沉淀+每周错误反思，正向提炼与负向纠偏合一。v3.1 新增断链防护：会话内即时沉淀（触发信号当场写入日记）+ 日记缺失兑底补写。v3.0：VFM 确定性验算、评分+衰减淘汰、WHERE×WHY 病理归档、主动 Skill 合成。触发词：记录错误、进化系统、自我反思、踩坑记录、self-evolve、self-improve。"
tags: 自我进化,记忆管理,错误记录,持续学习,经验沉淀,自动化,工作流程,反思复盘
visibility: public
license: MIT
---

**IRON LAW：**
1. 记录的错误/教训必须基于实际发生的事件，禁止编造或臆测未发生的失败
2. 提升规则到 MEMORY.md/TOOLS.md/SOUL.md 的阈值必须满足（Recurrence≥2 + VFM≥50 + 确定性验算通过），不可随意写入
3. **所有文件修改必须用 `read → write` 覆写，禁止使用 edit 工具。** 原因：本流程耗时长，edit 的 oldText 基于早期读取的内容构造，等到实际执行时文件可能已被其他会话修改，导致匹配失败。用 write 全量覆写不依赖文本匹配，天然避免此问题
4. **会话内即时沉淀（断链防护）**：对话中检测到任何触发信号（见「触发检测」）时，必须在事件发生的**当场**把一行带时间戳的记录追加写入当日日记 `memory/YYYY-MM-DD.md`（Claude Code 环境为 `~/.claude/memory/daily/YYYY-MM-DD.md`，文件不存在则创建）。禁止拖到会话末尾批量补写，禁止绕过日记直接录入账本——日记是每日六步的唯一数据源，漏记即断链，进化闭环就空转

无例外。

# mu-self-evolve · 持续进化系统

把经验、错误、纠正、知识缺口沉淀为持久记忆，正向提炼 + 负向纠偏，形成完整进化闭环。

适用于任何基于 LLM 的 AI Agent（OpenClaw / Claude Code / Cursor 等），让 Agent 像人一样从经验中学习。

文件结构与领域标签见 [references/file-structure.md](references/file-structure.md)

> Claude Code 环境兼容说明见 [references/claude-code-compat.md](references/claude-code-compat.md)

---

## ⏰ 定时运转

### 首次引导流程

1. 检查是否已有进化 cron：`openclaw cron list` 查找名称含"进化"或"evolve"的任务
2. 若无 cron：询问木老师——"要不要设每天自动进化？推荐 19:30，你习惯几点？"
3. 木老师确认后创建 cron：
   ```bash
   openclaw cron add \
     --name "🧬 每日自我进化" \
     --cron "30 19 * * *" \
     --tz "Asia/Shanghai" \
     --exact \
     --session isolated \
     --announce \
     --message "执行每日自我进化流程（见 mu-self-evolve SKILL.md）。今天是周几？如果是周五，额外执行【第六步：周度反思】。若今日日记不存在，先按 SKILL.md 前置兑底补写流程扫描当日真实痕迹重建日记，再进入六步；确实无素材才允许跳过并发摘要说明。"
   ```
   > Claude Code 环境下用系统 crontab 或手动触发，详见 [references/claude-code-compat.md](references/claude-code-compat.md)
4. 若已有：告知木老师当前配置，问是否需要调整

### 每日六步（周一到周日）

**前置：读取今日日记 + 兕底补写**

若 `memory/$(date +%Y-%m-%d).md` 不存在（今天还没有日记），**禁止直接跳到第六步**——先执行兑底补写，重建出日记后再进入六步流程。

**兕底补写流程（v3.1 新增，防进化闭环空转）：**

扫描当天的真实痕迹重建日记，素材源（路径按环境映射，见 [references/claude-code-compat.md](references/claude-code-compat.md)）：
1. **定时任务执行留痕** — 当天各 cron/automation 的运行记录（如任务自己的 memory.md、日志输出）
2. **长期记忆当日新增** — `grep 当天日期 MEMORY.md / CLAUDE.md`，命中条目回填为日记事件
3. **工作区当日变更** — `ls -lt` / `git status` 列出当天新增或修改的文件，有意义的变更记一行

每条一行带时间戳，写入日记后进入第 1 步。**严禁编造**（IRON LAW #1）：三类素材源全部为空时，才允许跳到第六步发摘要说明"今日无日记记录"。

1. **读取今日日记** — `memory/YYYY-MM-DD.md` 梳理当天经验
   - **出口条件**：今日日记已读完，提取出所有纠正/错误/新需求/正向反馈事件

2. **分类录入（含冲突裁决）** — 纠正→LEARNINGS.md，错误→ERRORS.md，新需求→FEATURE_REQUESTS.md。格式模板见 [references/record-templates.md](references/record-templates.md)
   - **出口条件**：所有事件已录入对应文件，每条有唯一ID（LRN/ERR/FEAT-YYYYMMDD-XXX），复现检查已完成
   - ⚠️ **写入铁律**：录入/修改必须用 `read → write` 覆写（见 IRON LAW #3）
   - ⚠️ **录入前冲突裁决**（三选一）：
     - 录入前先 `grep -i "关键词" .learnings/LEARNINGS.md` 搜索同主题条目
     - **矛盾**（同主题但结论相反）→ 覆盖旧条目（旧条目移入 archive）
     - **补充**（同主题但可合并）→ 合并到同一条目，Recurrence-Count +1
     - **无关联** → 正常新增
   - ⚠️ **容量检查**：录入前先 `wc -l .learnings/LEARNINGS.md`，若 >500 行 → 运行淘汰评分脚本（见下方"淘汰机制"），根据建议先归档再录入；未超限则直接录入
   - ⚠️ **ERRORS.md 同理**：录入前 `wc -l .learnings/ERRORS.md`，若 >300 行 → 运行淘汰评分脚本处理
   - ⚠️ **复现检查**：录入新条目前，先检查历史记录：
     ```bash
     grep -r "Pattern-Key" .learnings/ .learnings/archive/
     ```
     若命中：从 archive 恢复该条目，Recurrence-Count +1，不新建重复条目
   - ⚠️ **病理标注**：每条 ERRORS/LEARNINGS 必须标注 WHERE（出错环节）和 WHY（根因类型），详见 [references/record-templates.md](references/record-templates.md)

3. **检查提升条件** — 对候选条目运行 VFM 验算脚本：
   ```bash
   python3 scripts/vfm_verify.py <pattern-key>
   ```
   - 脚本输出置信度评分（0-100），基于复现次数、跨任务数、解决率、病理集中度
   - **提升条件**：脚本置信度≥70 + Recurrence≥2 + 跨2个以上不同任务 + VFM≥50
   - **出口条件**：满足条件的条目已标记为 promoted，不满足的留在 LEARNINGS.md 观察
   - 未通过验算的规则可标记为 `candidate`（候选），待更多数据积累后重新验算

4. **更新长期记忆** — 最重要 1-3 条洞察追加到 MEMORY.md（保持 ≤80 行）
   - **出口条件**：MEMORY.md 已追加新洞察且 ≤80 行（超限时已执行 mini 蒸馏）
   - 追加后若超80行：先执行 **mini 蒸馏**（合并高度相似的条目、删除已过时的旧条目），再追加新洞察
   - 判断条件：内容相同只是表述不同 → 合并保留更精准的一条；超过30天未触发的规则 → 移入「## 已归档」
   - mini 蒸馏不等于周度蒸馏，只做局部合并，不生成 Narrative
   - ⚠️ **写入铁律**：修改 MEMORY.md 必须用 `read → write` 覆写（见 IRON LAW #3）

5. **子Agent执行质量回顾** — 检查今日子Agent是否通读SKILL.md、产出是否符合规范
   - **出口条件**：已回顾今日子Agent执行情况，问题已记录到 LEARNINGS.md

6. **发送摘要** — 通知木老师进化结果
   - **出口条件**：摘要已发送，包含今日录入数/提升数/关键洞察

### 周五加跑：第六步 — 周度反思（仅周五执行）

详细步骤见 [references/weekly-reflection.md](references/weekly-reflection.md)

概览（含关键判断条件）：
- 6a. 错误扫描 — 回顾本周日记，提取重复错误模式
  **判断**：同一类错误本周出现≥2次 → 进入 6c；仅出现1次 → 记录观察，不提规则
- 6b. 生成 Narrative — 写入 `memory/narratives/YYYY-MM-DD.md`，按 (WHERE×WHY) 病理键结构化
  **判断**：有可写内容（至少1条值得反思的模式）才生成；无内容则跳过，不强行凑字数
- 6c. 规则提议 — 重复≥2次的错误模式 → 提炼为行为规则
  **判断**：新规则与 MEMORY.md/SOUL.md 现有规则是否重复？重复则只强化措辞，不新增条目
- 6d. MEMORY.md 蒸馏 — 从本周日记沉淀新条目；删除已过时旧条目（移入「## 已归档」）；精简到≤80行
  **判断**：条目是否超过30天未触发？是 → 移入归档；两条意思相同？→ 合并保留更精准的一条
- 6e. 归档旧日志 — 超过30天的 `memory/YYYY-MM-DD.md` 和 `memory/narratives/YYYY-*.md` 移动到 `memory/archive/`（保留原文件名，不删除不合并）
  **范围**：同时覆盖 daily notes + narratives，两者用同一个 30天规则
  **判断**：以文件名日期为准，今天日期 - 文件日期 > 30天 → 移动
- 6f. **评分+衰减淘汰** — 运行淘汰评分脚本，替代行数硬截断
  **操作**：
  ```bash
  # 先做评委偏差审计
  python3 scripts/bias_audit.py
  # 再跑淘汰评分
  python3 scripts/eviction_score.py
  # 如需单独处理 ERRORS.md
  python3 scripts/eviction_score.py .learnings/ERRORS.md
  ```
  **淘汰逻辑**：`effective_score = VFM × 0.5^(age_days/30)`，半衰期30天
  - effective_score < 25 且 age > 14天 → 建议归档
  - 但 Recurrence≥2 的条目豁免（跨任务复现覆盖低分）
  - 被检索命中时 Last-Seen 重置 → 衰减重置
  - 容量超限时按 effective_score 从低到高归档（不再按行数截断）
  **通知格式**：
  ```
  🪶 淘汰评分：
  - LEARNINGS: X条 → 保留N / 归档N / 当前行数X
  - ERRORS: X条 → 保留N / 归档N / 当前行数X
  - 偏差审计: PASS/FAIL
  ```
- 6g. **条目聚类扫描 + 主动Skill合成** — 识别可合成新 Skill 的条目群
  **判断**：本周 LEARNINGS 中≥3条条目属于同一领域/解决同一类问题 → 生成 Skill 草案
  **操作**：①扫描本周 LEARNINGS.md 全部条目的领域+摘要+WHERE+WHY ②按领域和病理类型语义聚类 ③每个聚类≥3条 → 生成 Skill 草案（SKILL.md 骨架 + 核心脚本框架） ④报告木老师确认后，走 mu-dev-workflow 创建新 Skill
  **与6f的联动**：聚类时同时检查是否有条目已被标记为 candidate（未通过VFM验算的规则），若同一聚类的多条 candidate 互相印证 → 提升其置信度

---

## 淘汰机制说明

v3.0 用评分+衰减淘汰替代行数硬截断，核心公式：

```
effective_score = VFM × 0.5^(days_since_last_seen / 30)
```

| 状态 | 条件 | 处理 |
|------|------|------|
| promoted | 状态=promoted | 移出至永久记忆 |
| resolved+旧 | 状态=resolved 且 >30天 | 移至 archive |
| 高复现 | Recurrence≥2 | **豁免**（不论分数和年龄） |
| 仅1次+旧 | Recurrence=1 且 >14天 | 标记 dormant，移至 archive |
| 低分+旧 | effective<25 且 >14天 | 移至 archive |
| 正常 | effective≥25 或 <14天 | 保留 |

> 被检索命中（grep 匹配到）时，Agent 手动更新 Last-Seen 日期 → 衰减重置

---

## 快速参考

| 情况 | 操作 |
|------|------|
| 命令/工具失败 | 记录到 `.learnings/ERRORS.md`，标注 WHERE+WHY |
| 木老师纠正我 | 记录到 `.learnings/LEARNINGS.md`，category: correction |
| 木老师正向反馈 | 记录到 LEARNINGS.md，category: positive_signal |
| 木老师要我没有的功能 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| 内部 API/MCP 失败 | 记录到 ERRORS.md，附接口和 token 状态，WHERE=api_call，WHY=具体根因 |
| 知识过时/有盲区 | 记录到 LEARNINGS.md，category: knowledge_gap |
| 发现更好做法 | 记录到 LEARNINGS.md，category: best_practice |
| 反复出现的模式 | 加 Pattern-Key，验算通过后提升 |
| 类似已有条目 | 录入前冲突裁决：合并/覆盖/新增 |

---

## 触发检测

**数据流向（v3.1 明确）：会话中检测到以下任何信号 → 当场写入当日日记（一行带时间戳，见 IRON LAW #4）→ 由每日六步统一分类录入账本。** 禁止会话中直接写入 LEARNINGS/ERRORS 账本而跳过日记。

自动识别以下信号并记录：

**纠正信号** → LEARNINGS.md correction：
- "不对"、"应该是"、"其实"、"你搞错了"、"重新来"、"不是这样的"
- "我跟你说过"、"别再这样了"、"为什么总是"、"我之前就说了"、"停止做X"
- 木老师编辑/覆盖了我的输出

**功能需求信号** → FEATURE_REQUESTS.md：
- "能不能"、"有没有办法"、"帮我做个"、"我希望你能"、"为什么不能"

**知识缺口信号** → LEARNINGS.md knowledge_gap：
- 木老师提供了我不知道的信息
- 我引用的接口/文档已过时
- API 行为和我预期不符

**错误信号** → ERRORS.md：
- 命令退出码非零
- HTTP 4xx/5xx
- Token 过期、认证拦截
- 超时或连接失败

**正向反馈信号** → LEARNINGS.md positive_signal：
- "好"、"可以"、"对"、"行"、"就这样"、"不错"、"喜欢这个"
- "这个格式好"、"这次写得好"、"比上次好"
- 木老师对特定输出未纠正且直接采用（隐式正向）

**偏好信号** → LEARNINGS.md best_practice：
- "我喜欢你这样"、"以后都这样"、"永远不要Y"、"我的风格是"
- 木老师对特定方案明确赞许

---

## 提升到永久记忆

| 经验类型 | 提升目标 | 示例 |
|----------|---------|------|
| 行为风格、原则 | SOUL.md | "输出用数字序号不用 bullet" |
| 工作流、子Agent规则 | AGENTS.md | "有专属子Agent先分配给子Agent" |
| 工具使用、API配置 | TOOLS.md | "发文件用本地路径而非远程 URL" |
| 高频场景规律 | MEMORY.md | 偏好设置、常用 ID 等 |
| 可复用能力模式 | 新建 mu-xxx Skill | 独立封装为技能 |

**提升条件（v3.0 三重门控）：**
1. **确定性验算**：`python3 scripts/vfm_verify.py <pattern-key>` 输出置信度≥70
2. **经验门槛**：Recurrence≥2 且跨2个以上不同任务 + VFM≥50
3. **时效性**：30天内反复出现，或木老师明确说"以后都这样"/"记住这个"（一次即可，VFM阈值降至40）

**VFM 评分（提升前自检）：**

| 维度 | 权重 | 判断问题 |
|------|------|---------|
| 高频使用 | ×3 | 这条规则会每天/每周触发吗？ |
| 减少失败 | ×3 | 这条能把之前的翻车变成成功吗？ |
| 减轻木老师负担 | ×2 | 能让木老师少解释一句话吗？ |
| 节省未来成本 | ×2 | 能让未来的我省时间/token吗？ |

每项 0-10 分，加权总分 **≥50 才提升**。低于50的留在 LEARNINGS.md 观察。

> v3.0 新增：维度二"减少失败"不再仅靠 LLM 估算，需对照 vfm_verify.py 的解决率数据。无数据的条目该维度给0分。

**提升后状态改为：**
```
**状态**: promoted
**提升到**: TOOLS.md · "工具规则" 章节
```

---

## 定期回顾

```bash
# 统计待处理条目数
grep -h "状态.*pending" .learnings/*.md | wc -l

# 列出高优先级待处理
grep -B5 "优先级.*high\|critical" .learnings/*.md | grep "^## \["

# 搜索特定领域
grep -B2 "领域.*mcp" .learnings/*.md | grep "^## \["

# 按病理键搜索
grep -B2 "WHERE.*mcp" .learnings/*.md | grep "^## \["
```

回顾动作：
- 已解决的改为 resolved
- 反复出现的提升到上层文件
- 满足条件的提取为新 Skill
- 清理 3 个月以上且已 resolved 的条目

---

## 提取为新 Skill 的条件

| 条件 | 说明 |
|------|------|
| 反复出现 | 同一病理键(WHERE×WHY)的条目≥3条 |
| 已验证 | 状态 resolved，方案可用 |
| 非显而易见 | 需要调试才能发现 |
| 可复用 | 不是某次任务专属 |
| 木老师说 | "做成 skill"、"以后常用" |

6g 聚类扫描发现满足条件的聚类后，直接生成 Skill 草案（SKILL.md 骨架 + 核心脚本框架），报告木老师确认后走 mu-dev-workflow 安装到 `<SKILL_DIR>/mu-xxx/`。

---

## 已知局限

1. **并发 write 风险**：read→write 覆写在多会话并发修改同一文件时，可能丢失其他会话的写入。IRON LAW #3 选择 write 是因为 edit 的 oldText 匹配失败概率更高，但 write 并非完美方案
2. **VFM 验算依赖数据量**：`vfm_verify.py` 需要足够的条目才能产出有意义的置信度评分，早期阶段（条目<5）验算结果参考价值有限
3. **衰减半衰期是经验值**：30天半衰期对标 CrewAI，但可能需要根据实际使用模式调整
4. **触发检测非穷举**：信号词列表无法覆盖所有表达方式，隐式正向反馈可能被遗漏
5. **VFM 评分仍有主观性**：虽然"减少失败"维度引入了确定性验算，但其他三个维度仍依赖 LLM 判断
6. **聚类+Skill合成依赖 LLM 判断**：6g 的语义聚类和 Skill 草案生成非确定性算法，可能遗漏或误聚合

## 子Agent派活原则

派活一句话：**"谁+做什么"**。子Agent自己匹配Skill→通读SKILL.md→严格执行。

- 禁止在派活时附加规则、输出要求、注意事项——这些全在SKILL.md里
- 不搞中间层：不建信封文件、不建角色persona文件、不建路由表
- 规则只写在SKILL.md一个地方，所有人（主Agent和子Agent）读同一份

---

## References 索引

| 文件 | 内容 |
|------|------|
| [references/record-templates.md](references/record-templates.md) | LRN/ERR/FEAT 三种记录的完整 Markdown 模板（含 WHERE×WH 病理键） |
| [references/weekly-reflection.md](references/weekly-reflection.md) | 周五第六步：6a错误扫描 + 6b Narrative + 6c规则提议 + 6f评分淘汰 + 6g Skill合成 |
| [references/file-structure.md](references/file-structure.md) | 文件结构与领域标签说明（含 WHERE/WHY 标签 + 用户自定义标签） |
| [references/claude-code-compat.md](references/claude-code-compat.md) | Claude Code 环境兼容说明（路径映射+调度降级） |
| [scripts/env_detect.py](scripts/env_detect.py) | 环境自动检测（OpenClaw 优先，Claude Code 降级） |
| [scripts/vfm_verify.py](scripts/vfm_verify.py) | VFM 确定性验算脚本（复现/跨任务/解决率/病理集中度→置信度评分） |
| [scripts/eviction_score.py](scripts/eviction_score.py) | 评分+衰减淘汰脚本（effective_score=VFM×0.5^(age/30)） |
| [scripts/bias_audit.py](scripts/bias_audit.py) | 评委偏差审计脚本（缺陷注入→验证淘汰机制可信度） |
