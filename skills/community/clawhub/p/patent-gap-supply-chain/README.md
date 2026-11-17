# patent-gap-supply-chain

通过"专利缺口"反推产业链关系的竞争情报工作流 skill，适用于 WorkBuddy / Codebuddy / Claude Code / Codex。

A competitive intelligence workflow skill that infers supply-chain relationships from patent gaps. Works with WorkBuddy / Codebuddy / Claude Code / Codex.

---

## 中文说明

### 这是什么

当研究科技股 / 硬件 / 制造 / 医药类公司时，发现标的 A 的产品使用了技术 T，但 A 没有 T 的相关专利——这套 skill 引导从专利缺口切入，**先判断缺口是真实外部依赖还是商业秘密/know-how保护**，再激活五条线索并行验证，竞对三角验证增强信号，**负向验证排除假阳性**，**专利质量评分识别真技术持有者**，**证据时效追踪避免过时结论**，财务数据交叉验证定论，输出带置信度的产业链关系推断报告。

**v0.4.0 新增**：
- **专利质量评分**：不看数量看质量——权利要求宽度、被引影响、同族规模、法律状态四维评分，核心专利(≥8/12)才支撑高置信度
- **负向验证**：主动寻找"B 不是 A 供应商"的证据（收入错配/产品错配/地理不可行/客户名单排除），反证失败正向证据链才成立
- **证据时效追踪**：每条证据带时间戳，>18个月标记为过时并降权，结论不能只靠过时证据

**v0.3.0**：竞对三角验证 + 财务交叉验证 + 反向工作流 + 行业指南 + 真实案例
**v0.2.0**：商业秘密/know-how 评估

### 核心设计

- **商业秘密先排除再定论**：专利缺口可能是商业秘密保护策略，必须先评估
- **专利质量 > 专利数量** (v0.4.0)：一份核心专利胜过几十份外围专利
- **负向验证必做** (v0.4.0)：主动尝试推翻推断，经受住反证的推断才可信
- **证据时效必标** (v0.4.0)：过时证据不能单独支撑高置信度
- **竞对三角验证**：多同行同一缺口 → 同一供应商，是最强信号之一
- **财务交叉验证**：无财报佐证的推断置信度最多"中等"
- **双向工作流**：正向（缺口→供应商）+ 反向（专利所有者→下游客户）
- **专利降级为入口线索**：专利缺口只触发验证，不直接定论

### 安装

    git clone https://github.com/tianzhiceng297-boop/patent-gap-supply-chain.git ~/.workbuddy/skills/patent-gap-supply-chain

或手动复制 `SKILL.md` 和 `references/` 到 `~/.workbuddy/skills/patent-gap-supply-chain/`。

### 触发场景

- "研究 XX 科技股"
- "分析 XX 公司的供应链 / 供应商"
- "查一下 XX 技术的专利归属"
- "XX 公司用了某技术但好像没专利"
- "识别 XX 的供应商"
- "XX 公司的下游客户有哪些？" (反向工作流)
- "哪些公司依赖 XX 的技术？" (反向工作流)

### 适用边界

| 标的类型 | 适用性 |
|---------|--------|
| 硬件 / 制造 / 医药 / 材料 | 强适用 |
| 软件 / 互联网 | 弱适用（降低置信度） |
| 商业模式创新 | 不适用 |

---

## English

### What it is

When researching tech / hardware / manufacturing / pharma companies, you find that target A's product uses technology T, but A holds no patents related to T. This skill starts from the patent gap, **first evaluates whether the gap reflects true external dependency or deliberate trade secret / know-how protection**, then activates five parallel verification leads, competitive triangulation, **negative verification**, **patent quality scoring**, **evidence freshness tracking**, and financial cross-validation, outputting a confidence-scored supply-chain inference report.

**New in v0.4.0**:
- **Patent quality scoring**: 4-factor quality score (claim breadth, citations, family size, legal status). Core patents (≥8/12) support high confidence; peripheral patents cap at low.
- **Negative verification**: Actively search for evidence that B is NOT A's supplier. Inference survives active disproof attempts or is down-weighted.
- **Evidence freshness tracking**: Every evidence item carries a timestamp. Stale (>18 months) evidence is down-weighted; conclusions cannot rest primarily on stale evidence.

**v0.3.0**: competitive triangulation + financial cross-validation + reverse workflow + industry guide + real case
**v0.2.0**: trade secret / know-how assessment

### Core design

- **Trade secrets ruled out before concluding**: patent gap may reflect trade secret strategy
- **Patent quality > patent count** (v0.4.0): one core patent outweighs dozens of peripheral ones
- **Negative verification mandatory** (v0.4.0): actively try to disprove; surviving inferences are credible
- **Evidence freshness tracked** (v0.4.0): stale evidence cannot support "high" alone
- **Competitive triangulation**: multi-peer same gap → same supplier is a top-tier signal
- **Financial cross-validation required**: no "high" without financial corroboration
- **Bidirectional workflow**: forward (gap → supplier) + reverse (patent owner → downstream clients)
- **Patents demoted to an entry lead**: a patent gap triggers verification but does not directly conclude

### Installation

    git clone https://github.com/tianzhiceng297-boop/patent-gap-supply-chain.git ~/.workbuddy/skills/patent-gap-supply-chain

Or manually copy `SKILL.md` and `references/` to `~/.workbuddy/skills/patent-gap-supply-chain/`.

### Trigger scenarios

- "Research [tech stock]"
- "Analyze [company]'s supply chain / suppliers"
- "Look up patent ownership of [technology]"
- "[Company] uses a technology but seems to have no patents"
- "Identify [company]'s suppliers"
- "Who are [company]'s downstream customers?" (reverse workflow)
- "Which companies depend on [technology]?" (reverse workflow)

### Applicability

| Target type | Applicability |
|-------------|---------------|
| Hardware / manufacturing / pharma / materials | Strong |
| Software / internet | Weak (reduce confidence) |
| Business-model innovation | Not applicable |

---

## File structure

- `SKILL.md` — core: triggers, direction selection, 11-step workflow (triangulation + negative verification + patent quality + evidence freshness + financial cross-validation), I/O contract, tool integration, key principles
- `references/workflow.md` — detailed 11-step operations + reverse workflow appendix
- `references/checklists.md` — all checklists including patent quality scoring, negative verification, evidence freshness, 5-layer confidence adjustment
- `references/industry-guide.md` — vertical-specific guidance: semiconductor, pharma, new energy, consumer electronics, materials/chemicals
- `examples/sample-output.md` — fictional case showing full 11-step report format
- `examples/real-case.md` — real A-share case: Goertek & Apple VR supply chain
- `CHANGELOG.md` — version history

## License

MIT
