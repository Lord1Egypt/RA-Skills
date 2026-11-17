> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# M 门算法规约核心（🔴 必读分片，R-50 物理切分）

> ⚠️ **本规约不是机器执行** —— 13 项 M 门是「**主控 LLM 推理模拟执行**」（零 shell、零 exec）。历史叫法「M **机械化**硬门」是**旧名（已弃用）**、与实现不符。
> 🧾 **信任模型唯一真源** = [`M-Gate-背景.md`](M-Gate-背景.md) §诚实声明（各类错判率、已知漏洞、替代方案）；读到「机械化」三字时，以该节为准。**M 门 = LLM 推理判定，非机器强制。**
> 📦 **分片边界**：本文件 = 🔴 核心（判定协议 / 四档出口 / 闸门第 0 步 / 统一抽取规则 / M-Form·M-Exist·M-Integrity 13 项）；背景与沿革 → [`M-Gate-背景.md`](M-Gate-背景.md)（按需）；输出 JSON schema → [`M-Gate-Algorithm-appendix.md`](M-Gate-Algorithm-appendix.md)。旧路径 `M-Gate-Algorithm.md` 仅为兼容入口，**不承载规则**。

## 🧾 可复核判定协议（双字段 + 证伪证据）

> **定位**：本节把「判定要可复核」从散文要求升级为**报告固定字段**。判定权仍归 **LLM 推理**（主控 / T7 / T8），字段化只为让主人**人工抽检**时一眼看出「原文是什么、裁的是什么、凭什么」——**不引入任何运行时 shell 或脚本执行**，零 exec 口径不变。

**四条固定字段（每个 M 门条目必备；v2.12.40 由三条扩为四条；v2.15.13 FB-13 增第五字段 `basis`）**：

| 字段 | 含义 | 来源 |
|---|---|---|
| `判定输入` | **本次判定实际读了哪个版本**：`{文件路径, 版本标识（v{N} / 报告文件名）, 首行原文, 末行原文, 字节数}` | 主控 `read` 到的磁盘原件，逐字照抄 |
| `原文值` | 判定的输入事实：计数 / 编号集合 / 标题清单 / 文件存在性等**机械可读**原样值 | 主控 `read` 到的磁盘原文，逐字照抄，不归并、不改写 |
| `裁定值` | LLM 推理给出的结论值（如「通过」/「不通过」+ 命中数） | 按本规约伪代码推理得出 |
| `证伪依据` | **不一致时必填**：逐条枚举命中的具体位置（文件 + 行号 + 原文片段）、真阳性模式扫描结果（该模式在一份**已知合规样本**上命中数应为 0）、规范冲突说明（哪条规则与哪条规则互斥） | 主控 `read` + 推理填写 |
| `basis` | **证据类型二分（v2.15.13 FB-13）**：`mechanical`（存在性 / 计数 / 编号比对，主人可检查复算）/ `llm`（语义推理判定，不可机械复算）——每个门条目必填其一 | 按判据性质归类；交付说明「M 门结论」段**按 basis 分组呈现**（mechanical 组列枚举证据；llm 组显式标「以 LLM 判定为主、未列不代表通过」——实测 2026-10-06：交付说明只能列「可实证 7 项」其余无分类，主人无法分辨硬证据） |

**通过档证据（最低要求 —— 修「放行零证据」）**：

> 原口径只在**不一致**时才要证据，于是「一致」成为**零成本放行路径**。现改为：**通过档同样必须给出人类可复算的枚举证据**。

1. **扫描对象指纹**：`判定输入` 四项必填（路径 / 版本标识 / 首行原文 / 末行原文 / 字节数）。缺任一项 → 报告不完整。
2. **命中清单（不得只给计数）**：本次检查提取到的对象**逐条列出行号与原文片段**。只写「命中 3 处 / 无残留」而不列清单 = **未枚举**，按 P0 处理。
3. **零命中自证**：某检查项提取结果为 0 条时，必须给出**扫描范围**（从哪一行到哪一行）+ **匹配规则**（提取式）。「无」不是证据，「在 X 范围内按 Y 规则提取得到 0 条」才是。
4. **人类 5 秒可复核**：主人拿报告后，抽检任一清单项应能直接 `检查` 命中；命中不了 = 该清单是编的。

**判定铁律**：

1. **`证伪依据` 留空 = 报告不完整**（四档通用，含「通过」档 —— 通过档按下条给枚举证据，不一致档按三项内容给证伪）。
2. **`原文值` 与 `裁定值` 不一致时**，三项内容（命中位置枚举 / 真阳性模式扫描 / 规范冲突说明）**缺任一项即视为伪造报告**——按 **P0** 处理，T8 不得签字放行。
3. **不得用「汇总数」代替逐条枚举**：只写「命中 3 处」而不列这 3 处的文件 + 行号 = 未枚举。
4. **`原文值` 不得转述**：必须能回到磁盘原件逐字核对；改写、概括、四舍五入后的值不是原文值。
5. **判定权不下放，但「不跑命令」≠「只给结论」**：四字段由 LLM 推理填写，不新增脚本执行路径，**不得**因此要求 agent 跑任何命令；但机械校验的缺席必须由**人类可复算的枚举证据**补偿 —— **不得以「agent 无 exec」为由省略清单**（二者是不同要求）。

> **它解决什么**：M 门是「LLM 自评自过」（见上节诚实声明 §3），字段化把「凭什么这么判」变成**可被主人一眼证伪**的对象——主人抽检只需核对「`原文值` 是否属实 / 不一致处是否枚举齐全」，不必重跑整套推理。

---

## 🎚️ 判定结果分档（四档 —— 替代「退出码」语义）

> **口径变更**：M 门 / 阶段闸门的结论**不再用「退出码 0/1」表达**——退出码是进程级概念，而本门是 **LLM 结构化判定**（无进程、无返回值）。历史文档与本文件旧段落的「exit 0」「退出码 1」一律按本节四档读。

**四档（结论必须落其一，不得自创第五档）**：

| 档位 | 含义 | 是否阻断 | 是否触发修订轮 | 处置 |
|---|---|---|---|---|
| **通过** | 全部检查项判定为真 | 否 | 否 | 放行至下一节点 |
| **不通过** | 存在**内容 / 证据**缺陷（P0/P1/P2） | 是 | **是** | 触发对应修订（T5/T7 独立写手）或补检索 |
| **无法判定** | 输入不可读 / 证据不足 / 上游产物自相矛盾，**不足以**判为通过或不通过 | 是 | **否** | 补证据或等人在环裁决后**重跑同一判定**；不得凭「差不多」升格为「通过」，也不得降格成「不通过」 |
| **路径或参数错误** | 目标产物不存在 / 路径越界 / 参数非法（如引用了非当前轮的 `v{N}`）/ 前置产物未落盘 | 是 | **否** | 先修路径 / 参数 / 前置产物，再**重跑同一判定**；**不得**当作内容缺陷 |

<details>
<summary>历史误判与修正（为何「路径错误」必须单独成档）</summary>

同族实现在早期版本把「定稿不存在」误判成 **P1 内容问题** → 下游据此触发了一轮**不该发生**的修订（改的是本来没有问题的稿子，白烧一整轮）。
本仓库 2026-09-14 实测同型问题：**产物不存在被当成内容缺陷**。
根因 = 判定分档缺少「非内容类失败」这一维 → 一律落进「不通过」→ 一律触发内容修订。

</details>

**分档纪律（三条）**：

1. **路径 / 参数问题永远不升级为内容问题**——两者处置完全不同（前者修参数重跑、后者改稿）；把前者写成后者 = 制造假修订轮。
2. **「无法判定」≠「通过」**——判不了就如实写「无法判定」（fail-closed）；两档在处置上不可互换。
3. **档位须与 `证伪依据` 自洽**——判「不通过」必须给出被证伪的具体位置；判「路径或参数错误」必须指出**哪个**路径 / 参数不满足**哪条**约束。

---

## 🎯 计数类档位真源 + P2 量化锚点（修 M-3 + M-5）

> 背景：个体化命题实测「同一指标 4 个数（45/53/54/75）」与「超阈 9.4 倍被降档 P2」两类同型漏检。真源声明后，**计数类指标走档位**、**P2 走量化锚点**，两者互相不重叠。

### M-3 计数类档位真源

**全库计数类断言禁止给精确数字**（LLM 推理计数的错判率与产物实际值的偏差可达 ±20%），只给**档位**：

| 指标类型 | 档位表述（唯一口径） | 精确值出口 |
|---|---|---|
| 破折号（`——`）出现处数 | `0-8 / 9-30 / >30` | 唯一出口：T8 终检或主人在 host shell 跑 `计数 '——' file.md` 回填 |
| 正文字符数 | `达上限 / 超 5-10% / 超 >10%` | 唯一出口：T8 终检（read + 逐字计数）或主人在 host shell 跑 `匹配 '\p{Han}' file.md \| 统计行数` 回填 |
| 引用条目数 | `<20 / 20-50 / >50` | 唯一出口：T8 终检或交付说明 |
| 参考文献条数 | 同上 | 同上 |
| 反方质疑处数 | `<3 / 3-5 / >5` | 唯一出口：T7 审计报告（交接报告必填 `反方质疑档位`） |
| 数据卡 / 案例卡 / 文献卡计数 | `<5 / 5-10 / >10` | 唯一出口：交付说明 |

**单一出口 / 4 条新纪律**：
1. **全流程不得重报精确数字**（即与 T8 出口不同处不得给精确数）；重报 = 同源不一致。
2. **档位标注**必须含**口径真源链接**（如「字数档位 = [`字数判定表.md`](字数判定表.md) §二」）。
3. **派发话术 = 档位 + 上限**，不派发话术 = 「达上限」档。
4. **T5 自报数字降级为「未验证」档**（仅作进度预览；T7/T8 重跑验证后取真档位）。

**禁止行为**：
- 同份交付物 4 处出现不同精确数（如「破折号 45 / 53 / 54 / 75」）—— 任一不一致 = 门故障（**M-3 失守 = 假绿灯**）。
- T7 / G14 / T9 / T8 四处对同一指标的档位表述**必须同源**；两份报告给两个不同档 = 门失败。

### M-5 P2 量化锚点 + 累积升级

**P2 不得容纳「超阈严重缺陷」**——下列约束**机械门**：

| 阈值 | P2 资格 |
|---|---|
| **实测 ≤ 阈值 1.5 倍** | ✅ 可降为 P2 |
| **1.5 倍 < 实测 ≤ 3 倍** | ⚠️ **形态类瑕疵**（不影响结论成立的表述问题）才可 P2；其他必须升 P1 |
| **实测 > 阈值 3 倍** | ❌ **一律不得 P2**；最低 P1（必含修订） |
| **形态类瑕疵**（如「不影响结论成立的拼写 / 编号闭环 / 表格对齐」） | ✅ 可 P2（即使超阈 1.5-3 倍） |

**累积升级**：
- **单轮 P2 ≥ 3 项 ⇒ 升级 P1**（不再分别报 P2，统一升档）
- 升级判定写入 M-Gate-Report v{N}.json 的 `p2_promotions: [{from: P2, to: P1, count: N, items: [...]}]` 字段
- T8 终检不复检升级判定（升级在 t7_5_integrity 完成；T8 仅引用其结论）

**禁止行为**：
- 「超阈 9.4 倍 / 11.5 倍」类严重失守被塞进 P2 即数即判，超过 3 倍必须最低 P1。
- 单轮堆叠 5+ 项 P2 不升档（**累积升级 = 机械门，不得「形式合规」地逐项 P2 放行**）。

**真源约束**：M-Gate / T7 / T8 / T9 任何一处报告 P2 项时**必填**：
- 阈值（项目级真源 = `字数判定表.md` §二 / `M-Gate-核心.md` 形态瑕疵清单）
- 实测值（含口径与档位）
- 倍数（实测 / 阈值）
- 形态类瑕疵标志（`is_formal_defect: true/false`，P2 必填 false ⇒ 必升 P1）

---

## 🔁「报告后激活」重跑时序

> **一句话**：**凡前提为「相关报告已落盘」的检查项，必须在报告落盘后重跑；主控预跑的结果不得直接当作闸门输入。**

**背景**：主控常在等待子代理时「先跑一遍」相关检查，等报告落盘后**沿用**先前结论当闸门输入。此时判定对象已变（报告是新写的），预跑结果**天然过期**——沿用它等于用旧结论给新产物盖章。

**适用清单（前提 = 某份报告 / 产物落盘）**：

| 检查项 | 报告后激活的触发点 | 不得沿用的预跑结果 |
|---|---|---|
| M-Form-8（三角验证覆盖） | `drafts/初稿-v1.md` 落盘**后**的正式判定 | 写手启动前的「预估覆盖」 |
| M-Exist-1 / M-Exist-3 | 修订稿 / T7 审计报告落盘**后** | 上一轮稿件的对比结果 |
| M-Integrity-2（T7.5 门） | `audits/审计报告-vN.md` 落盘**后** | 审计进行中读到的中间态 |
| T7.5 的「M 门记录」项 | 当前轮章节级 M 门记录**写盘后** | 上一轮记录（不得跨轮沿用） |
| T9 建议分流（T8 读 T9 报告） | `audits/审稿报告-vN.md` 落盘**后** | T9 运行中的中间态 |
| T8 终检（读 M-Gate-Report / T9 报告） | 两份报告**均落盘后** | 任一报告缺位时的推断值 |

**三条纪律**：

1. **落盘即失效**：被判定的对象一旦被上游改写，先前结论**立即作废**（同型：`drafts/current_draft.md` 必须在每轮修订后重刷，否则 T7 审旧稿）。
2. **闸门只认「报告后」的判定**：写进 `status.md` / 报告 JSON 的门结论，必须注明**它读的是哪个版本**（`v{N}` / 报告文件名）；无版本标注的门结论按**过期**处理。
3. **预跑结论的合法用途**：只作**进度预览 / 提前预警**，不得作为闸门输入、不得作为「已通过」的依据。

**落地位置**：`phase-order.yaml` 中凡 `condition` 依赖他角色报告者、或 `kind: mechanical_checkpoint` 而前置为「报告已落盘」者，一律以 `rerun_after_report: true` 显式标注；未标注者不得以「报告已存在」为由跳过重跑。

---

---

## 🔒 判定独立性分级（修「判定者 = 被判物」）

> **问题**：M 门 / 闸门的判定者常与产物生产者同处一个上下文，复核的输入又常常是**自己刚写的** `status.md` / 报告记录。想自过只需写一组自洽字段 + 「一致」——**成本低于真实核查**。

**三级独立性**：

| 级别 | 适用 | 硬要求 | 残留风险 |
|---|---|---|---|
| **L0 完全独立** | T7 审计（独立子代理）、T9 盲审（硬定义） | 判定者**不得**是产物作者；不得读产物作者的自我结论；T9 另加输入白名单 + 报告必填「独立性声明」 | 无（本仓可达的最高级） |
| **L1 主控亲为 + 指纹补偿** | T8 技术终检、T2.5 / T7.5 闸门 | **必须重读磁盘产物**（不得只凭自己写的 `status.md` 记录）；`判定输入` 四项必填；必做三方对账（见下节） | **无法达到 L0**：主控既生产又判定 → **已知残留风险，必须在 `final/交付说明.md` 披露** |
| **L2 无独立证据** | 心跳 / 自检类纯文本声明 | 仅作进度信号，**不得**作为任何门通过的独立依据 | 高（与 minimax 子代理失稳叠加） |

**三条纪律**：

1. **判定者 ≠ 产物作者**（可行时优先）：本仓已有「修订轮必须 spawn 独立写手」先例（M-Integrity-2 步骤 8）——**对称扩展到判定环节**即可，无需新机制。
2. **L1 不得冒充 L0**：主控亲为的判定必须在报告里标明「判定者 = 主控（L1）」，并披露无法独立复核的项。
3. **禁止「读自己写的东西」当复核**：L1 判定前必须重读**磁盘原件**；`status.md` 只能用来「对账」，不能用来「取数」。

---

## 🩺 闸门第 0 步：输入新鲜度校验（修「旧文件冒充新产物过闸」）

> **问题**：闸门的判据是「读某个文件路径」，但**从无前置检查**确认这个文件真的来自本轮。两种真实击穿路径：① 主控内存里拼完但没落盘 → 门读到**上一轮残留文件**，形式合规即「通过」；② 批改只更新了 `run/` 未更新 `outputs/` → 闸门读到旧副本照样通过。

**任何闸门执行前，先做第 0 步（三项全过才允许开门）**：

| # | 校验 | 不满足时的档位 |
|---|---|---|
| 1 | **存在**：目标产物文件在磁盘上 | 「路径或参数错误」（**不得**当作内容缺陷、**不得**触发修订） |
| 2 | **非空**：文件字节数 > 0（并在报告中记录字节数） | 「路径或参数错误」 |
| 3 | **新鲜**：文件 mtime **≥** 上游角色完成时间（以心跳 / 报告时间戳为准） | 「路径或参数错误」，要求上游重新落盘 |

**三条纪律**：

1. **第 0 步失败 = 拒绝开门**：不是「警告后继续」，而是 fail-closed。
2. **零产物归第 0 步**：上游「正常 ack 但零产物文件」一律由本步拦下（处置模板见 `errors.md` E13）。
3. **第 0 步结论也要入报告**：逐项写「存在 / 非空 / mtime vs 上游完成时间」三个实测值，不得只写「已校验」。

**两条扩展（回应实测）**：

4. **★ 扩展到「流程节点」，不只 M 门**：凡 `condition` 依赖上游产物的节点（如 `t5_feedback_revision` 依赖 `analysis/批判报告-vN.md`、`t9_review` 依赖 `final/定稿.md`），**条件求值前必须先做本步存在性校验**；产物不存在 → 判「**路径或参数错误**」并**回报「上游 <角色> 未产出」**，**不得**落 `on_not_triggered`。
   > **实测根据**：2026-09-14 某 run **Phase 3.6（T6）整段跳过**，但 `t5_feedback_revision.condition = T6_requires_revision` 在报告缺失时照常落 `not_triggered` → 「**上游漏跑**」与「**跑了但条件不满足**」在状态机里结果完全相同 → **一路跑到 T9 都无人发现**。
5. **★ 「名称 ↔ 指纹」强制同源**：报告写 `判定输入` 时，**对象名与 sha256 必须来自同一次 read**。
   > **实测根据**：同次 run 中 T9 报告声称评审 `final/定稿.md`，但其记录的 sha256 实际对应 `drafts/current_draft.md`（未定稿的稿源）——**有指纹字段才可机械化证伪**。T8 终检必核「报告声明的指纹 = 交付版本指纹」，不符 → **打回重跑**。

---

## 📖 核心概念（优先阅读）

**执行 M 门前，请先阅读**：[`glossary-full.md`](glossary-full.md)（完整真源 ~21KB；子代理精简核心见 [`glossary-core.md`](glossary-core.md) ~2.5K）

词汇表第二章详细定义了 M 门的性质、覆盖范围、单一真源原则。本文档是算法实现细节，不重复概念定义。

---

## 执行模型

**M 门的执行方式**：
1. 主控用 `read` 工具读取本算法文档
2. 主控用 `read` 工具读取 `final/定稿.md` + `final/证据包/` 所有文件 
3. 主控按下面的**伪代码推理判定**，产出 `M-Gate-Report-v2.2.12.json`
4. **判定通过**才能返回，否则触发修订或补检索

**本文档中的代码示例**：
- **Python 风格** → 伪代码，描述算法逻辑（主控 LLM 推理执行）
- **Bash 风格** → 验证示例，供人类主人在 host shell 手动执行（非 agent 执行）

**工具能力边界**：详见 [glossary-full.md 第五章](glossary-full.md) + [工具能力边界.md](工具能力边界.md)

---

## 📦 分片加载策略（🔴 核心必读）

| 分片 | 内容 | 加载 |
|---|---|---|
| **核心**（本文件）| **可复核判定协议（双字段 + 证伪证据）/ 通过档证据 / 判定结果分档（四档）/ 计数类档位真源 + P2 量化锚点 /「报告后激活」重跑时序 / 判定独立性分级 / 闸门第 0 步 / 执行模型 / 执行前置 / 统一抽取规则真源 / 未定义 helper 替代口径** + M-Form 8 项 / M-Exist 3 项 / M-Integrity 2 项（规则 + 伪代码）| 🔴 跑 M 门前 + T7 审计前 + T8 终检前**必读** |
| **背景**（按需）| 诚实声明（信任模型 / 已知漏洞 / 主人操作建议 / 替代方案）/ 渐进式执行模式 / 版本史 / 章节级增量验证 / 设计哲学与借鉴出处 / 附录导航 | 🟡 需理解信任边界或沿革时 → [`M-Gate-背景.md`](M-Gate-背景.md) |
| **附录**（按需）| 输出格式（M-Gate-Report JSON schema）/ 论衡哲学化 / 教训沉淀 / 历史版本归档 | 🟡 按需 → [`M-Gate-Algorithm-appendix.md`](M-Gate-Algorithm-appendix.md) |

**理由（R-50，v2.14.1 起）**：主流程真正需要的是「13 项规则 + 触发条件 + 伪代码 + 四档出口」；信任模型与版本沿革属**按需**。
原文「分片必读」只是**指针纪律**——不守纪律的 agent 会整吞整份文件；切分后「必读部分」与「背景部分」成为**文件系统硬边界**（读核心文件即天然不含背景），不再依赖 agent 自觉。
**读到 🔴 标记时按指定分片读；背景分片只在需要信任模型/沿革时读，不为凑「完整性」把背景一并读入。**

## 执行前置

> 🔴 本段读的是**本核心文件**（`M-Gate-核心.md`）；背景/信任模型见 [`M-Gate-背景.md`](M-Gate-背景.md)，输出 schema 见 [`M-Gate-Algorithm-appendix.md`](M-Gate-Algorithm-appendix.md)。

1. ✅ **分片读取本规约**（🟠 **分片必读**：用 `read` 工具读 `M-Gate-核心.md` 的**可复核判定协议 + 判定结果分档 + 「报告后激活」重跑时序 + 执行模型 + M-Form 8 项 + M-Exist 3 项 + M-Integrity 2 项**规则与伪代码段；**附录段按需** → [`M-Gate-Algorithm-appendix.md`](M-Gate-Algorithm-appendix.md)，**不再需要读 4 个历史版本**）
2. ✅ **读取 final/定稿.md + final/证据包/所有文件**（用 `read` 工具）
3. ✅ **依次执行 M-Form 8 项 + M-Exist 3 项 + M-Integrity 2 项**（按本规约伪代码推理，含升级算法）；每项同时填 **`判定输入` / `原文值` / `裁定值` / `证伪依据`** 四字段（通过档也必须给**枚举清单**，不得只给计数）
4. ✅ **每项结论落到四档之一**（通过 / 不通过 / 无法判定 / 路径或参数错误）；**路径类失败不得当内容缺陷**
5. ✅ **产出 M-Gate-Report-v2.2.12.json**（用 `write` 工具写入，含 `判定记录` 段）
6. ✅ **判定为「通过」才允许 T8 返回**（注：本门为 **LLM 结构化判定**，非进程级返回码 —— 见顶部诚实声明）；「不通过」→ 触发 T5 修订或主控补检索；「无法判定」/「路径或参数错误」→ **不触发修订**，修正后重跑同一判定

**Phase 0 同意关卡**：本算法不调用任何外部服务（纯 LLM 推理 + 项目内文件 I/O），**不新增网络级外发**，因此不产生「额外」的网络级同意需求；但流水线整体仍受 Phase 0 同意关卡约束（文件清单 + 外部服务 4 选 1 已由主人在 Phase 0 确认），本算法在其授权范围内运行，不构成免同意通道。实战验证如需在宿主侧跑 dry-run 对比，由主人手工执行并明示同意（金标准）。

---

## 🔧 统一抽取规则真源（修 M-2：消除两处同源不一致）

> **背景**：13 项 M 门里有两组「同源却各写一份」的抽取规则 ——
> ① **文末节集合**：M-Form-2 写「必需四节」、M-Form-7 写「白名单七节」，两处各自成文；
> ② **引用编号正则**：M-Form-1 用「字母 + 数字」式、M-Exist-3 另写一套（另含表格体例）。
> 机械化照做会把不一致**固化成互相矛盾的门**。**本节 = 这两类抽取规则的唯一真源**；
> M-Form-1 / M-Form-2 / M-Form-3 / M-Form-7 / M-Form-8 / M-Exist-1 / M-Exist-3 一律**引用本节**，不再各写一份。
> 本节仍是 **LLM 推理执行**的伪代码定义（**零 exec 口径不变**，见顶部诚实声明）。

### A. 文末节集合（唯一真源）

| 集合 | 内容 | 消费者 |
|---|---|---|
| `ENDNOTE_SECTIONS_REQUIRED`（必需子集，4 节） | 参考文献 / 数据来源 / 案例来源 / 先行者文献 | M-Form-2（缺任一 = 不通过） |
| `ENDNOTE_SECTIONS_OPTIONAL`（白名单可选子集，3 节） | 致谢 / AI 使用声明 / 方法论附录 | M-Form-7（出现即合法；不出现不判失败） |
| `ENDNOTE_SECTIONS_ALL`（= 必需 4 节 ∪ 可选 3 节） | 上文 4 节 + 可选 3 节 | M-Form-7 白名单判定 |
| `ENDNOTE_SECTIONS_NONSTANDARD`（非标准节） | `## 附` 等历史变体 | M-Exist-1 / M-Form-3 的「文末」收录面 |

**三条关系（一次写死，杜绝再分叉）**：

1. `REQUIRED ⊂ ALL`：**必需四节**与**白名单七节**不是两个集合，**是同一节集合的两个口径**（「至少要有」vs「最多只能有」）。
2. `NONSTANDARD ⊄ ALL`：`## 附` 等非标准节**收录进「文末」用于双向对比**，但**不在白名单内** ⇒ M-Form-7 判违规。
3. **标题匹配口径唯一**：`title == 节名` 或 `title.startswith(节名)`（前缀匹配，容忍「数据来源（可信度标注）」这类带括号变体）。

### B. 引用编号正则（唯一真源）

```python
import re

# 唯一真源常量（三类格式必须同时覆盖；①② 由 T5 铁律强制，③ 为表格体例）
#   ① 标准编号：[D01] [C01] [C-主01] [L01] [先01]
#   ② 基线编号：[D-基-R-01] 等「字母-分段-序号」写法
#   ③ 表格编号：[1.1] [2.3] 等「章.序」写法
CITATION_STD_RE = re.compile(r'\[(?:D|C|C-主|L|先)\d+\]')
CITATION_BASE_RE = re.compile(r'\[(?:D|C|L|先)-[\w\-]*?\d+\]')
CITATION_TABLE_RE = re.compile(r'\[\d+\.\d+\]')
CITATION_NUMBER_RE = re.compile(
    r'\[(?:(?:D|C|C-主|L|先)\d+|(?:D|C|L|先)-[\w\-]*?\d+|\d+\.\d+)\]'
)
```

**② 基线格式的收窄约束（防误报面扩大）**：必须**以 `-` 开头**且**以数字结尾**，中间仅允许 `[\w\-]`；
**不接受** `[D-x]` / `[图1]` / `[注]` 这类形态 —— 它们更可能是正文里的普通方括号标注，不是引用编号。

**消费口径（三处必须同源）**：

| 消费者 | 用哪个常量 | 用途 |
|---|---|---|
| M-Form-1 | `CITATION_NUMBER_RE` | 统计定稿（含 SVG 文本节点）的引用编号集合，判「有无引用」 |
| M-Form-3 / M-Form-8 | `CITATION_NUMBER_RE`（分类型时用 `CITATION_STD_RE` / `CITATION_BASE_RE` / `CITATION_TABLE_RE`） | 正文 vs 文末提取、三角验证分类型覆盖 |
| M-Exist-1 / M-Exist-3 | `CITATION_NUMBER_RE`（分类型同上） | 与数据卡 / 文末清单做双向对比 |

### C. 判定出口（第 3/4 档，唯一真源；修 M-5）

> **背景**：全部伪代码原先只有 `{"通过": True}` / `{"通过": False}` **两档**，而规约强制**四档**
> （见 §判定结果分档）。照两档机械化的后果 = **「产物不存在」被判「不通过」** ⇒ 触发本不该发生的修订轮
> （2026-09-14 实测同型事故：白烧一整轮）。故给出**四个出口**，全部伪代码统一调用。

```python
def verdict_pass(**fields):
    """第 1 档：通过"""
    return {"通过": True, "档位": "通过", **fields}

def verdict_fail(reason, **fields):
    """第 2 档：不通过（内容 / 证据缺陷，触发修订轮）"""
    return {"通过": False, "档位": "不通过", "失败原因": reason, **fields}

def verdict_undecidable(reason, **fields):
    """第 3 档：无法判定（输入不可读 / 证据不足 / 上游自相矛盾；不触发修订轮）"""
    return {"通过": False, "档位": "无法判定", "失败原因": reason, **fields}

def verdict_path_error(reason, **fields):
    """第 4 档：路径或参数错误（产物不存在 / 路径越界 / 参数非法；不触发修订轮）"""
    return {"通过": False, "档位": "路径或参数错误", "失败原因": reason, **fields}
```

**统一第 0 步**：每个检查项先做 §闸门第 0 步 三项校验（存在 / 非空 / 新鲜）；
不满足即 `verdict_path_error(...)` 并**立即返回**，不得继续走内容判定。

**与附录 JSON 严格对齐**：`"档位"` 取值只能是
`"通过" | "不通过" | "无法判定" | "路径或参数错误"`（见 M-Gate-Algorithm-appendix.md 的 `判定记录_双字段` 段）；
`通过: True/False` 仅作兼容旧读法的布尔镜像，**档位以 `档位` 字段为准**。

---

## 🧩 未定义 helper 清单与替代口径（修 M-7）

> **背景**：本规约伪代码引用了约 20 个**全仓无实现**的辅助函数。它们历史上被读作「可机械化的承诺」，
> 实际既无实现、也不会有实现（**零 exec** + 发布版不携带脚本）。
> **本节口径 = 优先标注**：这些 helper **不做机械实现 —— 由主控 LLM 推理替代**
> （`read` 磁盘原件 + 按本节规则推理）。这与本规约首句一致：**本规约不是机器执行**。
> **不得**把本节读成「待实现清单」，也**不得**以「helper 未实现」为由跳过对应检查项。
> 新增 helper **必须同批登记本表**（防未定义函数再次静默累积）。

| helper | 替代口径（LLM 推理执行） | 使用处 |
|---|---|---|
| `extract_text_nodes(glob)` | `read` 各 SVG 后提取 `<text>` / `<desc>` / `<title>` / `<tspan>` 节点文本 | M-Form-1 / M-Exist-3 |
| `extract_intext_v2(draft)` / `extract_endnote_v2(...)` | 按 §统一抽取规则真源 A + B 切分与提取 | M-Exist-1 |
| `can_trace_back(ref)` | 逐条判内联引用能否在文末节 + 证据包找到对应条目 | M-Exist-1（内联模式） |
| `extract_body(text)` / `extract_endnote(text)` | 按 `ENDNOTE_SECTIONS_ALL` + `ENDNOTE_SECTIONS_NONSTANDARD` 的首次命中位置切分 | M-Form-3 |
| `extract_trust_dict_standard(card)` / `extract_trust_dict_table(card)` | 逐条读数据卡，建立「编号 → 信任级别」映射 | M-Form-6 / M-Exist-3 |
| `count_d_entries(card)` | 双格式并集去重后计数 | M-Integrity-1 |
| `count_data_requirements_in_brief(brief)` | 读任务简报「研究问题」段，累加各子问题「需找数据点 ≥N」 | M-Integrity-1 |
| `get_paragraph_containing(text, needle)` | 取 `needle` 所在段落（上下空行或标题界定） | M-Form-5 |
| `check_header_vs_actual_count(card)` | 比对数据卡头部「共 N 条」与实际计数 | M-Integrity-1 |
| `check_M_Form_6(card)` / `check_M_Exist_3(...)` | 复用本规约 M-Form-6 / M-Exist-3 判定 | M-Integrity-1 / M-Integrity-2 |
| `get_latest_audit_report(dir)` | 列目录取 `vN` 最大者 | M-Integrity-2 |
| `check_p0_p1_listed(report)` | 读审计报告，核对 P0/P1 段显式列出（可为零条但须显式写） | M-Integrity-2 |
| `check_m_gate_all_pass_current_round()` | 读本轮章节级 M 门记录 + status.md 记录表 | M-Integrity-2 |
| `check_evidence_sha256_placeholder(doc)` | 读「证据包指纹」；`sha256`/`bytes` 为空或占位符记 `pending_owner_verification`，不得判通过 | M-Integrity-2 |
| `check_draft_vs_report_isolation(...)` | 分别 `read` 三份产物，判论文与报告内容互不混入 | M-Integrity-2 |
| `check_revision_by_independent_writer(status)` | 读 status.md 修订回环记录，判是否由独立写手执行 | M-Integrity-2 |
| `emit_placeholder_sha256(card)` | 发占位符文本（非哈希计算，**不**作闸门强制项） | M-Integrity-1 |

**两条纪律**：

1. **登记 ≠ 放行**：helper 未实现**不降低**检查强度 —— 判定照跑、四档照落、枚举证据照给（见 §通过档证据）。
2. **替代口径不得漂移**：若某 helper 的替代口径与实际做法不同，**改口径而不是改门**；口径变更须同步本表。

---

## M-Form 形式合规门（8 项）

### M-Form-1: 引用标注完整性

**伪代码**（主控 LLM 推理执行）：
```python
# 第 0 步：输入新鲜度（见 §闸门第 0 步；不满足即第 4 档，立即返回，不触发修订）
if not exists("final/定稿.md"):
    return verdict_path_error("final/定稿.md 不存在（路径或参数错误，不触发修订）")

# 读取定稿全文 + final/图件/ 内 SVG
draft_text = read("final/定稿.md")
svg_texts = []
for svg_file in glob("final/图件/*.svg"):
    # 提取 SVG 文本节点：<text>…</text> / <desc>…</desc> / <title>…</title> / <tspan>
    svg_texts.append(extract_text_nodes(svg_file))  # helper 无机械实现 → 由 LLM 推理替代（见 §未定义 helper 清单）

# 提取所有引用标注（md 正文 + SVG 内嵌文本 视为事实层）
all_text = draft_text + "\n".join(svg_texts)
# 引用编号正则：唯一真源见 §统一抽取规则真源 B（覆盖 ①标准 ②基线 ③表格 三类格式）
references = CITATION_NUMBER_RE.findall(all_text)
references_unique = sorted(set(references))

# 判定（四档出口见 §统一抽取规则真源 C）
if len(references_unique) > 0:
    return verdict_pass(**{"引用数": len(references_unique), "SVG 文本节点纳入": len(svg_texts)})
else:
    return verdict_fail("正文 + SVG 内嵌文本均无任何引用标注", **{"引用数": 0})
```

**关键扩展**：SVG 内的 `<text>` / `<desc>` / `<title>` / `<tspan>` 节点现视为事实层（M-Gate 核验覆盖），与正文 .md 同等待遇 —— 防止「正文中正、SVG 中错」的双线不一致。

**判据强度复核（M-3）**：本项判据仅为「引用编号集合非空（数量 > 0）」，**属实弱门** —— 只抓「全篇零引用」这类极端缺陷，抓不到「某章缺引用 / 密度不足」。**评估结论：弱，但有意保留**，理由三条：① 更严的判据（如「每章 ≥N 条」）在**中英混排 / 内联引用模式**下会误报（内联模式的「（机构，年份）」不产生编号，见 M-Exist-1 内联分支）；② 引用覆盖的**正确性**已由其他门承担 —— 编号对应由 M-Exist-1 双向对比、论点级覆盖由 M-Form-8 三角验证、残留编号由 M-Form-3；③ 在 **P0 阻断类**门里塞入易误报的强判据 = 用误报换假阴性，代价是白烧修订轮（本仓已有同型事故）。⇒ **维持「数量 > 0」**；如需更严，应新增**独立**分档项并在非阻断档报告，而不是改写本门。

**人类验证示例**（可选，主人手动复核用）：

### M-Form-2: 文末四节存在性

**伪代码**（主控 LLM 推理执行）：
```python
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists("final/定稿.md"):
    return verdict_path_error("final/定稿.md 不存在（路径或参数错误，不触发修订）")

# 读取定稿全文
draft_text = read("final/定稿.md")

# 必需四节：唯一真源见 §统一抽取规则真源 A（ENDNOTE_SECTIONS_REQUIRED）
# 本项不再自写节名清单；标题匹配口径（前缀匹配 + 括号变体容忍）亦取自该节
required_sections = [f"## {s}" for s in ENDNOTE_SECTIONS_REQUIRED]

missing = [s for s in required_sections if s not in draft_text]

if len(missing) == 0:
    return verdict_pass(**{"必需节已齐": len(required_sections)})
else:
    return verdict_fail("缺必需文末节", **{"缺失章节": missing})
```

### M-Form-3: 临时编号残留

**v2.2.0 算法**（**有 bug**）：简单检查段落中 [L/D/Cxx] → 误判合规内联引用为「残留」。

**v2.2.1.2 新算法**：

**伪代码**（主控 LLM 推理执行）：
```python
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists("final/定稿.md"):
    return verdict_path_error("final/定稿.md 不存在（路径或参数错误，不触发修订）")

# 读取定稿
draft_text = read("final/定稿.md")

# 文末节集合：唯一真源见 §统一抽取规则真源 A
#   收录面 = ENDNOTE_SECTIONS_ALL（白名单七节）+ ENDNOTE_SECTIONS_NONSTANDARD（## 附 等变体）
#   本项不再自写 markers 清单 —— 历史上它与 M-Form-7 白名单分叉，即 M-2 要消除的不一致之一
ENDNOTE_MARKERS = [f"## {s}" for s in list(ENDNOTE_SECTIONS_ALL) + list(ENDNOTE_SECTIONS_NONSTANDARD)]

# 辅助函数：提取正文部分（排除文末节）
def extract_body(text):
    for marker in ENDNOTE_MARKERS:
        if marker in text:
            text = text.split(marker)[0]
    return text

# 辅助函数：提取文末部分
def extract_endnote(text):
    parts = []
    for marker in ENDNOTE_MARKERS:
        if marker in text:
            parts.append(text.split(marker)[1] if len(text.split(marker)) > 1 else "")
    return "\n".join(parts)

# 提取正文和文末的引用编号（正则唯一真源见 §统一抽取规则真源 B）
body_text = extract_body(draft_text)
endnote_text = extract_endnote(draft_text)

intext = sorted(set(CITATION_NUMBER_RE.findall(body_text)))
endnote = sorted(set(CITATION_NUMBER_RE.findall(endnote_text)))

# 计算真正残留（正文有但文末无）
orphan = sorted(set(intext) - set(endnote))

if len(orphan) == 0:
    return verdict_pass(**{"正文编号数": len(intext), "文末编号数": len(endnote)})
else:
    return verdict_fail("正文引用编号在文末无对应（临时编号残留）", **{"残留编号": orphan})
```

**人类验证示例**（可选）：

**实战验证**：
- 实战 5（教师场域孤岛）：v2.2.0 算法 38 条命中（误判）→ v2.2.1.2 算法 0 命中（合规内联引用）✅
- 实战 4（品牌一致性）：v2.2.0 算法 14 条命中（误判）→ v2.2.1.2 算法 0 命中 ✅

### M-Form-4: 角色元数据泄露

**伪代码**（主控 LLM 推理执行）：
```python
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists("final/定稿.md"):
    return verdict_path_error("final/定稿.md 不存在（路径或参数错误，不触发修订）")

# 读取定稿
draft_text = read("final/定稿.md")
lines = draft_text.split("\n")

# ① ASCII 角色代号：词边界约束（不再裸 substring）
#    前后不得为 [A-Za-z0-9]，避开 T1WI / T1DM / MT5 这类正文术语
ROLE_TOKEN_RE = re.compile(r'(?<![A-Za-z0-9])T([1-8])(?![0-9A-Za-z])')

# ② 中文内部术语：结构位置约束（仅位置命中算泄露）
INTERNAL_TERMS = ["交接报告", "七段", "论衡主控", "子代理", "反哺报告", "角色卡"]
COOCCUR_TERMS = ["主控", "角色卡", "交接报告", "子代理", "报告", "节点", "M 门"]

def structural_position(line, term):
    """结构位置四则：标题行 / 独立成段 / 括号注记 / 内部术语共现行"""
    if re.match(r'^\s{0,3}#{1,6}\s+', line):                       # ① 标题行
        return True
    if re.fullmatch(r'[\s\W]*' + re.escape(term) + r'[\s\W]*', line):  # ② 独立成段
        return True
    if re.search(r'[（(][^）)]*' + re.escape(term) + r'[^）)]*[）)]', line):  # ③ 括号注记
        return True
    return sum(1 for t in COOCCUR_TERMS if t in line) >= 2          # ④ 内部术语共现行

leaks_p0 = []    # 结构位置命中 → P0（阻断）
suspected = []   # 仅裸出现 → 疑似（非阻断，供人工抽检）

for idx, line in enumerate(lines, 1):
    if ROLE_TOKEN_RE.search(line):
        leaks_p0.append({"行号": idx, "类型": "角色代号", "原文": line.strip()[:80]})
        continue
    for term in INTERNAL_TERMS:
        if term not in line:
            continue
        if structural_position(line, term):
            leaks_p0.append({"行号": idx, "类型": term, "原文": line.strip()[:80]})
        else:
            suspected.append({"行号": idx, "类型": term, "原文": line.strip()[:80]})

if len(leaks_p0) == 0:
    return verdict_pass(**{"结构位置命中": 0, "疑似（非阻断）": len(suspected)})
else:
    return verdict_fail("角色元数据在结构位置泄露", **{"优先级": "P0", "泄露清单": leaks_p0})
```

**为何这样写不再误报（M-4①）**：旧写法是 `word in draft_text`（裸 substring），而本项是 **P0**（命中即阻断交付）——于是正文里合法的「T1 加权成像」「七段式论证」都会误报，**一次误报 = 白烧一轮修订**。新写法收窄三层：

1. **ASCII 代号走词边界**：必须前后非字母数字（避开同一文档里的合法临床/技术写法）。
2. **中文术语走结构位置**：仅标题行 / 独立成段 / 括号注记 / 内部术语共现行四类位置命中算泄露。
3. **仅裸出现降为「疑似」**：进抽检清单，**不阻断、不触发修订**。

**不会退化为恒真（必中样本仍全数命中）**：

| 样本 | 旧写法 | 新写法 |
|---|---|---|
| 标题行 `## 主控签字` | 命中 | **命中（P0：标题行）** |
| 独立成段 `子代理` | 命中 | **命中（P0：独立成段）** |
| 正文 `（T5）` | 命中 | **命中（P0：括号注记 / 词边界）** |
| `交接报告 + 主控` 同行 | 命中 | **命中（P0：内部术语共现行）** |
| `T1 加权成像显示白质病变` | 命中（误报） | 不命中 → 疑似（非阻断） |
| `七段式论证贯穿全文` | 命中（误报） | 不命中 → 疑似（非阻断） |
| `MT5 与基线模型对比` | 命中（误报） | 不命中（`T5` 前有字母，非独立代号） |

**注意**：M-Form-4 是 P0 优先级，角色元数据泄露 = 读者看到论衡内部代码 = 失去学术严肃性。

### M-Form-5: 过程语言残留

**伪代码**（主控 LLM 推理执行）：
```python
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists("final/定稿.md"):
    return verdict_path_error("final/定稿.md 不存在（路径或参数错误，不触发修订）")

# 读取定稿
draft_text = read("final/定稿.md")

import re

# 过程语言检查
process_patterns = [
    r'v[0-9] 稿',
    r'初稿',
    r'草稿',
    r'修订说明',
    r'上一版',
    r'下一版'
]

found = []
for pattern in process_patterns:
    matches = re.findall(pattern, draft_text)
    if matches:
        found.extend(matches)

# 特殊检查："据行业经验估算" 必须有 [行业估算] 标记
estimate_uses = re.findall(r'据行业经验估算', draft_text)
for use in estimate_uses:
    # 检查上下文是否有 [行业估算] 标记
    context = get_paragraph_containing(draft_text, use)  # helper 无机械实现 → 由 LLM 推理替代（取该串所在段落）
    if "[行业估算" not in context:
        found.append("据行业经验估算（未标记）")

if len(found) == 0:
    return verdict_pass(**{"残留词数": 0})
else:
    return verdict_fail("正文含过程语言残留", **{"残留词": found})
```

**注意**："据行业经验估算" 是 v2.1.1 引入的「合法估算标记」。段落开头标 `[行业估算，非数据卡]` → G6 论据类型自标（合法）；无标记直接用 → P1 残留。

> 📌 **数据卡路径口径（v2.12.28）**：M 门与 G 项一律读**源文件 `data/数据卡.md`**；`final/证据包/` 中是**交付副本，不得作判定依据**（副本可能滞后于源）。

evidence-pack-copy-note

### M-Form-6: 信任级别标注完整性

**v2.2.1 算法**：仅支持标准 [Dxx] 格式。

**v2.2.1.2 新算法**（双格式支持）：

**伪代码**（主控 LLM 推理执行）：
```python
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists("data/数据卡.md"):
    return verdict_path_error("data/数据卡.md 不存在（路径或参数错误，不触发修订）")

# 读取数据卡
data_card_text = read("data/数据卡.md")

# ---- 标准格式：逐条配对（M-4②：计数相等 ≠ 逐条配对）----
# 按条目首行切块，再在**块内**找信任级别
std_blocks = re.split(
    r'(?=^\s*(?:\*\*|#{2,4}\s*)?\[D\d+\])', data_card_text, flags=re.MULTILINE
)
std_entries = [
    b for b in std_blocks
    if re.match(r'^\s*(?:\*\*|#{2,4}\s*)?\[D\d+\]', b)
]

unpaired_std = []
for block in std_entries:
    did = re.match(r'^\s*(?:\*\*|#{2,4}\s*)?(\[D\d+\])', block).group(1)
    # 信任级别必须出现在「该条目自己的块内」（容忍加粗与 emoji 修饰）
    if not re.search(r'信任级别[^\n]{0,16}?(已发布|主人投喂|二手转引)', block):
        unpaired_std.append(did)

# ---- 表格格式：逐行配对（信任级别必须在本行内）----
table_rows = re.findall(r'^\|\s*\d+\.\d+\s*\|.*$', data_card_text, re.MULTILINE)
unpaired_table = []
for row in table_rows:
    if not re.search(r'\|\s*(已发布|主人投喂|二手转引)\s*\|', row):
        unpaired_table.append(row.split('|')[1].strip())

all_pass = (len(unpaired_std) == 0 and len(unpaired_table) == 0)

if all_pass:
    return verdict_pass(**{"标准格式条目": len(std_entries), "表格格式行": len(table_rows)})
else:
    return verdict_fail(
        "存在未配对（缺信任级别）的数据条目",
        **{"未配对_标准": unpaired_std, "未配对_表格": unpaired_table}
    )
```

**为何不再用「计数相等」（M-4②）**：`len(条目) == len(信任级别)` **不等价于**「每条都有信任级别」——
反例：**2 条缺标注 + 2 条重复标注** ⇒ 两边计数相等、等式成立，而整份数据卡实际有 2 条无信任级别，**照样通过**。
现改为**逐条配对**：先切出「条目块 / 表格行」，再在**各自块内**匹配信任级别；
未配对条目逐条列出（`未配对_标准` / `未配对_表格`），**任一条未配对即不通过**（不得用汇总计数代替逐条枚举，见 §可复核判定协议）。

**人类验证示例**（可选）：

**实战验证**：
- 实战 5（教师场域孤岛）：标准格式 47 条 D + 0 信任级别 → 失败
- 实战 4（品牌一致性）：表格格式 35 行 + 0 信任级别 → v2.2.1.2 能识别为表格格式

### M-Form-7: 定稿文末节标题白名单纯净

**背景**：首次实战（ai-productivity-scene-dependence）定稿文末混入「图表清单」「引用规范（四节闭环）」「主控签字（T8 终检）」三段操作员报告内容，而「终检必查项①」只在文档层声明、未机械执行 —— T8 签字时自己签「✅ 交付边界纯净」但文末明明混着禁止项。规范从文档层到执行层断链、签字走形式。

**伪代码**（主控 LLM 推理执行）：
```python
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists("final/定稿.md"):
    return verdict_path_error("final/定稿.md 不存在（路径或参数错误，不触发修订）")

# 读取定稿全文
draft_text = read("final/定稿.md")

import re

# 白名单（唯一真源见 §统一抽取规则真源 A：ENDNOTE_SECTIONS_ALL）
# 本项不再自写节名清单 —— 下行数组是该真源的**展开视图**（派生展示，非第二真源）：
#   必需 4 节（ENDNOTE_SECTIONS_REQUIRED）+ 可选 3 节（ENDNOTE_SECTIONS_OPTIONAL）
#   改真源时必须同步展开本行（内容与项数须与 §统一抽取规则真源 A 逐字一致，防漂移）
whitelist = ["参考文献", "数据来源", "案例来源", "先行者文献", "致谢", "AI 使用声明", "方法论附录"]  # v2.7.3 +方法论附录（可选，主人 Phase 5 勾选）；v2.12.32 +致谢（可发表性 F 选项启用时必含，否则与 F 判定表强制要求冲突）
assert set(whitelist) == set(ENDNOTE_SECTIONS_ALL)  # 展开视图自检：不一致 = 已漂移，按真源修正

def is_whitelisted(title):
    # 前缀匹配：容忍「数据来源（可信度标注）」这类带括号的变体
    return any(title == w or title.startswith(w) for w in whitelist)

# 提取所有二级标题（含行号）
lines = draft_text.split('\n')
sections = [(i, m.group(1)) for i, l in enumerate(lines)
            if (m := re.match(r'^##\s+(.+)$', l))]

# 找文末节起点（第一个白名单标题）
start_idx = next((idx for idx, (i, t) in enumerate(sections) if is_whitelisted(t)), None)

if start_idx is None:
    return verdict_undecidable(
        "文末无任何白名单节 → 无法界定「文末」起点，不足以判为通过或不通过",
        **{"优先级": "P0"}
    )

# 起点之后的所有 ## 标题必须在白名单内
violations = [t for (i, t) in sections[start_idx:] if not is_whitelisted(t)]

if len(violations) == 0:
    return verdict_pass(**{"文末节数": len(sections) - start_idx})
else:
    return verdict_fail(
        "文末混入操作员报告节（图表清单/主控签字/引用规范等），需移入 final/交付说明.md 或删除",
        **{"优先级": "P0", "违规节标题": violations}
    )
```

**档位说明（M-5）**：「文末无任何白名单节」⇒ **无法判定**（该判定项的输入前提不成立），**不是**「不通过」——
它**不触发修订轮**；内容缺陷由 M-Form-2（必需四节缺失）判「不通过」并触发修订，两项不重复计罚。
「起点之后混入非白名单节」才是真正的内容缺陷 ⇒ **不通过**（P0，触发修订）。

**人类验证示例**（可选）：

**判定铁律**：M-Form-7 是 **P0 优先级**。文末混入操作员报告节 = 读者看到论衡内部代码 = 失去「论文是给读者的，报告是给主人的」边界。**T8 在 M-Form-7 通过档之前，禁止在签字块写「交付边界纯净」四个字**（按上文 §六口径变更，**M 门结论用「通过/警告/失败」四档表达，不使用「exit 0」进程级措辞**）。

> **修正（回应实测 P1）**：旧白名单**缺「致谢」**，而可发表性 F 选项（默认启用）**强制要求** `## 致谢` ⇒ **致谢启用时必判 M-Form-7 违规**（两套判据互斥）。现已补入（亦同步至 `deliverables.md` 白名单表 + 下行 bash 例 + 失败原因文案）。

### M-Form-8: 三角验证覆盖率检查

**背景**：论文三实战 §四 P4 一直缺 [Lxx]（L=0 D=22 C=3），直到 T7 fallback 审计才发现（v3→v4 加了 [L06] [L12]）。**毛在才不出现**——主控「三角验证把关」职责未机制化，写手 v1 落地前没自动跑 [Lxx]+[Dxx]+[Cxx] 三维检查。

**三角验证原理**（论衡核心机制）：任何论点必须能映射到文献卡[Lxx]+数据卡[Dxx]+案例卡[Cxx]（涉企业行为/事件者必须配案例卡，至少两项齐全）。检索不到就标缺口，严禁编造。主角控「三角验证把关」职责（2026-08-13 原创性保证增）原本是主控手动检查，v2.3.7 P1-4 升级为**写手 v1 落地前的 M 门规则化必查**。

**伪代码**（主控 LLM 推理执行，写手 **v1 落盘后、T7 前**跑）：
```python
import re

# 第 0 步：输入新鲜度（见 §闸门第 0 步；简报与初稿均须本轮已落盘）
if not exists("01-任务简报.md") or not exists("drafts/初稿-v1.md"):
    return verdict_path_error("任务简报或初稿-v1 不存在（路径或参数错误，不触发修订）")

# 读取任务简报 + 初稿
brief = read("01-任务简报.md")
draft_text = read("drafts/初稿-v1.md")

# 提取任务简报 §四「核心论点」清单（如 [论点N] 格式）
# 如任务简报未明确标论点，以 §三 研究问题作为论点提取依据
claim_pattern = re.findall(r'\[论点\d+\]|第[一二三四五六七八九十]+章', brief)
claims = [c.strip() for c in claim_pattern]

# 【v2.12.56 M-6 修 fail-open】提不出论点 ⇒ claims 为空 ⇒ 不得真空通过
if len(claims) == 0:
    return verdict_undecidable(
        "任务简报未提供可提取的论点（[论点N] / 章标题均无）⇒ 三角验证无判定对象，不得真空通过",
        **{"论点数": 0}
    )

# 从初稿提取引用编号（正则唯一真源见 §统一抽取规则真源 B —— 不再自写 3 套）
all_refs = CITATION_NUMBER_RE.findall(draft_text)
l_refs = [x for x in all_refs if re.match(r'\[L', x)]
d_refs = [x for x in all_refs if re.match(r'\[D', x)]
c_refs = [x for x in all_refs if re.match(r'\[C', x)]

# 对每个论点检查三角验证：拆初稿为按论点的段落（按章节切分）
sections = re.split(r'^## ', draft_text, flags=re.MULTILINE)

violations = []
for claim in claims:
    # 找包含该论点的章节
    section_for_claim = next((s for s in sections if claim in s), "")
    # 检查三角验证覆盖率（分类型均取自统一正则，见 §统一抽取规则真源 B）
    sec_refs = CITATION_NUMBER_RE.findall(section_for_claim)
    has_l = any(re.match(r'\[L', x) for x in sec_refs)
    has_d = any(re.match(r'\[D', x) for x in sec_refs)
    has_c = any(re.match(r'\[C', x) for x in sec_refs)
    # 三角验证：至少 2 项齐全（不必须 3 项）
    coverage = sum([has_l, has_d, has_c])
    if coverage < 2:
        violations.append({
            "claim": claim,
            "section": section_for_claim[:50],
            "has_L": has_l,
            "has_D": has_d,
            "has_C": has_c,
            "coverage": f"{coverage}/3"
        })

if len(violations) == 0:
    return verdict_pass(**{"论点数": len(claims)})
else:
    return verdict_fail(
        "写手 v1 未补齐三角验证覆盖（<2 类引用），需补检索或降级为「观点」",
        **{"优先级": "P0", "未复核论点数": len(violations), "违规详情": violations}
    )
```

**为何「提不出论点」判无法判定（M-6）**：原实现下 `claims` 为空 ⇒ `violations` 为空 ⇒ 直接落「通过」（**fail-open**）——
写成「提不出论点反而全过」。现改为第 3 档：**不触发修订**，但**也不放行**（阻断），
要求先补任务简报论点、或走人在环裁决后**重跑同一判定**。

**触发时机**：
1. **写手 v1 落地后**（v1 写手产物已落盘）→ T4 分析员或主控跑 M-Form-8 预检 → 不通过 → 打回 v2 重写（计入修订轮）
2. **T7 审计员**跑最终审计时也跑 M-Form-8 → 不通过 → 打回（计入修订轮）

**实战背景**：§四 P4 [论点4] 一直缺 [Lxx]（L=0 D=22 C=3）直到 T7 fallback 审计才发现 → v3→v4 加了 [L06] [L12] 修补 → 浪费 1 轮修订。v2.3.7 升级后 M-Form-8 在 v1 落地时拦截，不再依赖 T7 兜底。

**人类验证示例**（可选）：

---

## M-Exist 存在性合规门（3 项）

### M-Exist-1: 文末四节双向对比

**v2.2.0 算法**（**有 bug**）：提取严格匹配 4 个标准文末节 → 对「## 附」段误判。

**v2.2.1.2 升级算法**（修正同源不一致）+ **v2.2.4 内联引用 + 补检索回填分支**：

```
算法步骤：
0. 【第 0 步】输入新鲜度（见 §闸门第 0 步）：final/定稿.md 与 01-任务简报.md 须存在 / 非空 / 新鲜；
   不满足 → **第 4 档「路径或参数错误」**（不触发修订，修路径后重跑同一判定）
1. 判断引用格式：读 01-任务简报.md「引用格式」字段
   - 「内联（机构，年份）」或「公众号/商业评论/行业分析」 → 走内联模式分支
   - 「[Lxx]/[Dxx] 编号」或「期刊/学术」 → 走标准对比
   - **字段缺失 / 取值不在枚举内 → 第 3 档「无法判定」**（**不得默认走标准模式** ——
     默认会让内联稿在标准对比下**空转后报通过**，即历史击穿路径）

2A. 标准模式：
   ① 提取正文 [Dxx]/[Cxx]/[Lxx]/[先xx]（不在文末任意节内）→ set_intext
   ② 提取文末任意节（标准 ## 数据来源 + ## 案例来源 + ## 参考文献 + ## 先行者文献 + 非标准 ## 附 等 + 文末最后 1/3 段 fallback）的所有引用编号 → set_endnote
   ③ 计算双向对比：求差集 set_intext set_endnote = 漏引；求差集 set_intext set_endnote = 孤儿
   ④ 判定（四档，v2.12.56 M-5 对齐）：漏引空 + 孤儿空 → 通过（第 1 档）；任一非空 → 不通过（第 2 档）；产物不存在 → 第 4 档（见步骤 0）；体例字段缺失 → 第 3 档（见步骤 1）
   ⑤ **引用体例层（T-8）**：额外检查「正文标记体系 ↔ 文末编号体系」**是否为同一体系** —— 若正文用 `[Lxx]` 而文末用 `[1]…[N]`（或反之）⇒ **两套体例并存，判 P1**。步骤 ③ 的双向对比在**各自体系内**自洽，**覆盖不到跨体系**，故须独立此步。真源 = [`../deliverables.md`](../../deliverables.md) §T-8 引用体例单一化

2B. 内联模式：
   ① 提取正文内联引用（机构，年份）：匹配 '（[^（）]*[0-9]{4}[^（）]*）' | 去重
   ② 5 项依赖编号的检查必须改为「可回溯性」检查（**M-Exist 系列内一致性**）：
      - M-Exist-1：每条内联引用能否在文末四节+证据包找到对应条目（**本项 = 双向对比；M-Exist-2 不在此清单内**，M-Exist-2 是证据包文件层完整性，详见 §M-Exist-2 段，二者职责不重叠）
      - G2 数据溯源：每个正文数字能否在数据卡/文献卡找到来源（防无主数据）
      - M-Exist-3：引用机构的信任级别在数据卡/案例卡有标注
      - G4-2 四节对比：正文引用的机构/数据/案例在文末四节有对应
   ③ 判定（四档，v2.12.56 M-5 对齐）：全部内联引用可回溯 + 所有数字有源 + 信任级别齐全 → 通过（第 1 档）；任一不可回溯 → 不通过（第 2 档，P1）；零内联引用 → 无法判定（第 3 档，见下方伪代码）

伪代码（标准模式）：
intext = extract_intext_v2(draft_text)     # 文末节集合与编号正则唯一真源见 §统一抽取规则真源 A/B
endnote = extract_endnote_v2(draft_text, standard=True, non_standard=True, last_third=True)
leaked = sorted(set(intext) - set(endnote))
orphan = sorted(set(endnote) - set(intext))

# 四档出口（见 §统一抽取规则真源 C）
if len(leaked) == 0 and len(orphan) == 0:
    return verdict_pass(**{"漏引": leaked, "孤儿": orphan})
else:
    return verdict_fail("双向对比非空（漏引 / 孤儿）", **{"漏引": leaked, "孤儿": orphan})

伪代码（内联模式）：
unresolved = [ref for ref in inline_refs if not can_trace_back(ref)]   # helper 无机械实现 → LLM 推理替代
if len(inline_refs) == 0:
    return verdict_undecidable("内联模式但未提取到任何（机构，年份）式引用 —— 判定对象为空，不得真空通过")
if len(unresolved) == 0:
    return verdict_pass(**{"内联引用_条数": len(inline_refs)})
else:
    return verdict_fail("内联引用不可回溯（P1）", **{"不可回溯": unresolved})
```

**补检索回填校验分支**（当流水线发生过补检索时触发）：

```
1. 判断是否发生补检索：检查 run/<项目名>/literature/ 是否有「补检索-*.md」文件

2. 回填校验（教训 P1-2：不可用「L总数==清单条目数」判定）：
   ⚠️ 反例警示—— **不要用** 等式判定「L总数==文末清单条目数」。
   文末参考文献清单可包含**非 L 文献**（法规[S]/报告[R]/标准/数据库[DB/OL]/网站等），
   如 GAO/EU AI Act/中国办法/OECD/Stanford HAI/AIID，等式在实战中「23==23」可能只是巧合（不同来源凑出同样数字）。
   审核工具误读为「L23==ref23 PASS」，**这是反例不是示例**。

   正确判定法：
   ① 提取补检索新增 L 编号（文献卡中「补检索」段标记）
   ② 对**每个**补检索 L，**人工逐条**检查文末参考文献清单是否有对应条目（按作者/标题/期刊匹配）
   ③ 判定：每个补检索 L 都在文末清单有对应条目 → 通过；任一缺 → P1
```

**实战验证**：
- 实战 4（品牌一致性-发布稿）：v2.2.0 算法误判 14 条漏引 → v2.2.1.2 算法 0 漏引 0 孤儿（## 附 段被识别）✅
- 实战 AI安全隐患：v2.2.1.2 标准对比在内联引用模式下空转 → v2.2.4 内联模式分支覆盖 24 条引用 ✅

### M-Exist-2: 证据包完整性校验（原「证据包文件完整性 sha256」）

**重写原因**：
- 原「M-Exist-2 证据包文件完整性 sha256」设计是「理想」但**实战中 sha256 字段永远占位**（主人不手动跑 `校验哈希`）
- 论衡「零 exec 哲学」= LLM 不能跑 sha256 实际计算（仅可读文件验证非空）
- 实战中占位符 `[哈希校验待主人回填]` 永远不会被回填 = 字段形同虚设
- v2.5.5 重命名为「证据包完整性校验」，判定项从「sha256 匹配」改为「文件存在性 + 字节数 + 章节结构」（LLM 推理实际能判定）

```
算法步骤：
1. 读取 final/证据包/ 目录下所有 .md 文件
2. **LLM 推理判定 5 项**（不是 sha256）：
   - ✅ 文件存在性：所有证据文件存在
   - ✅ 文件非空：字节数 > 1000（小文件例外如 先行者清单 可能 <1000）
   - ✅ 文件时间戳：在实战项目时间窗内（本次项目启动后 ~结束前）
   - ✅ 章节结构：文件含「## 基本信息」「## 条目列表」或类似必备段
   - ✅ 数据卡格式：JSON/YAML 校验或文本格式规范（数据卡含「[Dxx]」编号 + 信任级别字段）
3. **判定（四档，v2.12.56 M-5 对齐）**：
   - （a）5 项全过 → **通过（第 1 档）**
   - （b）部分项过但缺失具体证据 → **无法判定（第 3 档）**（标黄提示主人补；**不触发修订**）
   - （c）**证据包目录 / 文件不存在** → **路径或参数错误（第 4 档）**（不触发修订；先修路径或让上游落盘）
   - （d）文件存在但**全空 / 内容缺损**（主控未生成证据）→ **不通过（第 2 档）**（真错误，触发修订）
4. **人类主人补填 sha256 可选**：
   - 主人如需更严验证，在 host shell 跑 （检查 final/证据包/*.md） 后追加到 final/交付说明.md
   - 实战中**几乎没人补**，但保留为「理论严格性」项
5. **本文档中所有 sha256 示例**：是「跨平台命令参考」，**不是 agent 执行的代码**。
```

**能力边界澄清**：
- 论衡 agent **不能** 直接计算 sha256（不在工具白名单内）
- 主控 LLM 能用 `read` 读全文做「文件非空/章节结构/数据卡格式」验证（**这是 LLM 推理，不是 sha256**）
- 真正 sha256 由人类主人在 host shell **手动计算后回填**到「证据包指纹」段
- 本算法的「exit code」判定仅指「5 项 LLM 推理判定通过」，不包括 sha256 完整性验证（sha256 是人类补填项）

**实战背景**：原 M-Exist-2 sha256 字段永远占位，浪费交付说明.md 文档版面。重命名为「证据包完整性校验」后，字段实际可用（LLM 能判定）。

### M-Exist-3: 数据信任级别一致性对比

**关键扩展**：SVG 文本节点（`text`/`desc`/`title`/`tspan`）现视为事实层，内嵌的 `[Dxx]` / `[Cxx]` 信任级别与 md 正文同等对比。防“正文修了 SVG 没修”双线不一致。

**v2.2.1 算法**：匹配 '\[D[0-9]+\]' final/定稿.md → **不支持表格行 [1.x] 引用**。

**v2.2.1.2 新算法**（双格式支持）：

```
算法步骤：
1. 正文引用提取（编号正则唯一真源见 §统一抽取规则真源 B）：
   - 标准 + 基线 + 表格三类格式：用 CITATION_NUMBER_RE 提取 final/定稿.md → set_intext_d（D 类）
   - 表格格式单列：用 CITATION_TABLE_RE 提取 → set_intext_table
   - **扩展**：SVG 内嵌文本纳入（final/图件/*.svg 的 text/desc/title/tspan 节点）→ set_svg_d

2. 数据卡条目提取：
   - 标准格式 [Dxx]：匹配 '^\*\*\[D[0-9]+\]' data/数据卡.md → set_card_d
   - 表格格式 [1.x]：匹配 '^\| ([0-9]+\.[0-9]+) |' data/数据卡.md → set_card_table

3. 信任级别一致性对比：
   - 标准格式对比：求差集/-13 set_intext_d set_card_d
   - 表格格式对比：求差集/-13 set_intext_table set_card_table
   - SVG 格式对比：求差集/-13 set_svg_d set_card_d

4. 信任级别空标检查：
   - 标准格式：每条 [Dxx] 对应数据卡信任级别非空
   - 表格格式：每行 [1.x] 表格的「信任级别」列非空

5. 判定（四档，v2.12.56 M-5 对齐）：所有对比空 + 信任级别全填 → 通过（第 1 档）；任一非空 → 不通过（第 2 档）；定稿或数据卡不存在 → 路径或参数错误（第 4 档）；信任级别映射不可读 → 无法判定（第 3 档）

伪代码：
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists("final/定稿.md") or not exists("data/数据卡.md"):
    return verdict_path_error("定稿或数据卡不存在（路径或参数错误，不触发修订）")

# 扩展：SVG 内嵌文本节点视为事实层，纳入引用编号提取与对比
draft_text = read("final/定稿.md")
data_card_text = read("data/数据卡.md")
svg_text = extract_text_nodes("final/图件/*.svg")  # text/desc/title/tspan 节点合并（LLM 推理替代）
all_text = draft_text + "\n" + svg_text
# 引用编号正则：唯一真源见 §统一抽取规则真源 B —— 本项不再自写 D 类正则一套
intext_d = sorted({x for x in CITATION_NUMBER_RE.findall(all_text) if re.match(r'\[D', x)})
intext_table = sorted(set(CITATION_TABLE_RE.findall(draft_text)))  # 表格格式仅在正文，SVG 不支持
card_d = sorted(set(re.findall(r'^\*\*\[D\d+\]', data_card_text, re.MULTILINE)))
card_table = sorted(set(re.findall(r'^\| (\d+\.\d+) \|', data_card_text, re.MULTILINE)))
trust_d = extract_trust_dict_standard(data_card_text)   # helper 无机械实现 → LLM 推理替代
trust_table = extract_trust_dict_table(data_card_text)
leaked = sorted(set(intext_d) - set(card_d))
orphan = sorted(set(card_d) - set(intext_d))
missing_trust = [d for d in intext_d if d not in trust_d or trust_d[d] == '']
all_pass = (len(leaked) == 0 and len(orphan) == 0 and len(missing_trust) == 0)

# 四档出口（见 §统一抽取规则真源 C）
if all_pass:
    return verdict_pass(**{"漏注": 0, "孤儿": 0, "信任级别空标": 0})
else:
    return verdict_fail(
        "信任级别对比非空或存在空标",
        **{"漏注": leaked, "孤儿": orphan, "信任级别空标": missing_trust}
    )
```

---

## M-Integrity 阶段闸门（2 项，含修订轮流程约束）

### M-Integrity-1: T2.5 完整性门（T2 数据检索 → T4 分析前）

> **重要修正**：原版逻辑矛盾 — M-Integrity-1 在 T2→T4 之间，大纲（T4 产物）尚不存在却需查「数据条目数 ≥ 大纲 D 列数」。修正为查任务简报（Phase 0 已产物化）子问题的数据需求数。

**证据源质量阈值（实测补强，回应 P2-3）**：除条目数对账外，加三道比例阈值（LLM `read` 计数判定，超限 → 触发 T2/T3 补检或降级标注）：
- **二手转引比例 ≤ 30%**：数据卡中标注「二手转引 / 原始口径待复核」的条目 / 总条目
- **单源案例比例 ≤ 20%**：案例卡中仅 1 个独立来源的条目 / 总条目（单源 → 标 ⚠️ 且**不计入三角验证**）
- **不可访问 URL 比例 ≤ 10%**：数据/案例卡中 URL 无法访问（检索时报错/超时）的条目 / 总条目（不可访问 → 标「待人工复核」，不作为引用支撑）

```
算法步骤（主控 LLM 兜底执行）：
1. 检查数据卡文件存在：列出 data/数据卡.md → 必须存在
2. 提取数据条目数（双格式）：
   标准 [Dxx] 计数：计数 '^\*\*\[D[0-9]+\]' data/数据卡.md
   表格 [1.x] 计数：计数 '^\| [0-9]+\.[0-9]+ \|' data/数据卡.md
   两者取并集 dedupe
3. **修正**：提取任务简报子问题数据需求数
   从 01-任务简报.md 「研究问题」段读取每个子问题的「需找数据点 ≥N」
   需求总数 = Σ 子问题数据需求数
   （不再检查 analysis/分析大纲.md，因 T4 尚未产出）
4. 数据条目数 >= 任务简报需求总数 → 数据完整 → 通过；否则 → 触发 T2 重检索
5. 信任级别完整性：M-Form-6 **判定通过** → 通过；否则 → 触发 T2 补标注
6. 信任级别一致性：M-Exist-3 **判定通过** → 通过；否则 → 触发 T2 补数据卡
7. **修复**：哈希指纹为**可选验证**——主控发占位符 `[哈希校验待主人回填]` 到 `final/交付说明.md`「证据包指纹」段，**不**作为闸门强制项。主人如需真实哈希，由**主人本人**在宿主 shell 手动计算后回填（参考 M-Exist-1 的证据包完整性比对规则）。**该步骤不是 agent 执行的代码，是人类验证示例。**
8. **新增**：数据卡头部「共 N 条」声明 vs 实际检查计数一致性
   头部声明：匹配 '共 [0-9]+ 条' data/数据卡.md
   实际计数：步骤 2 的双格式并集 dedupe
   不一致 → 标 Failed（防 T2 未自检 + T4 人工检查才发现的延后问题）
9. 判定（四档，v2.12.56 M-5 对齐）：全部判定通过（项数以伪代码为准） → T2.5 **通过（第 1 档）**派发 T4；任一失败 → **不通过（第 2 档）**不派发 T4；数据卡 / 任务简报不存在 → **路径或参数错误（第 4 档）**（不触发修订）；条目数或需求数不可读 → **无法判定（第 3 档）**（不触发修订，补证据后重跑同一判定）
   **删「主人签字 Phase 1」**：T2.5 是**机械检查点**（LLM 结构化判定，非机器强制），主人签字/决策节点为 Phase 0 / Phase 2.5 / Phase 3.5 / Phase 5 四节点；检索完成→T4 之间**不应**打断主人

伪代码：
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists('data/数据卡.md') or not exists('01-任务简报.md'):
    return verdict_path_error("数据卡或任务简报不存在（路径或参数错误，不触发修订）")

data_card = 'data/数据卡.md'
data_count = count_d_entries(data_card)          # helper 无机械实现 → LLM 推理替代（见 §未定义 helper 清单）
outline_count = count_data_requirements_in_brief('01-任务简报.md')  # v2.2.17 显式标注：读任务简报，不读分析大纲
data_ok = data_count >= outline_count
trust_form_ok = check_M_Form_6(data_card)
trust_exist_ok = check_M_Exist_3(data_card, 'final/定稿.md')
sha256_pending = emit_placeholder_sha256(data_card)  # v2.2.17：发占位符，**不**作为闸门强制项
header_consistent = check_header_vs_actual_count(data_card)  
# 失败项逐条列出（不得只给「有失败」）
fail_reasons = [
    name for name, ok in [
        ("数据条目数 >= 简报需求数", data_ok),
        ("M-Form-6 信任级别完整性", trust_form_ok),
        ("M-Exist-3 信任级别一致性", trust_exist_ok),
        ("数据卡头部声明 vs 实际计数", header_consistent),
    ] if not ok
]

# 四档出口（见 §统一抽取规则真源 C）
if data_count is None or outline_count is None:
    return verdict_undecidable("数据条目数或简报需求数不可读，不足以判定", **{"sha256_pending": sha256_pending})
if outline_count == 0:
    # v2.12.65 P0-1：需求数 0 = 简报未标「需找数据点」（断链），禁 data_count >= 0 恒真放行
    return verdict_undecidable("简报未标注任何「需找数据点」，数据量需求不可判（断链）", **{"sha256_pending": sha256_pending})
all_pass = data_ok and trust_form_ok and trust_exist_ok and header_consistent
if all_pass:
    return verdict_pass(**{"数据条目数": data_count, "简报需求数": outline_count, "sha256_pending": sha256_pending})
else:
    return verdict_fail("T2.5 完整性门未全过", **{"失败项": fail_reasons, "sha256_pending": sha256_pending})
```

**实战反例**：T2 写数据卡时凭印象在头部写「共 29 条」，实际检查只有 26 条，T4 靠人工检查才发现。本次新增步骤 9 拦截。

### M-Integrity-2: T7.5 完整性门（T8 审计 → T8 终检前）

> **输入边界（P0-2）**：只读 `audits/` + `status.md` + 本轮 M 门记录 + `drafts/current_draft.md`；**禁读 `final/`**（T8 产物，T7.5 时不存在；旧版步骤 4 读 `final/交付说明.md` 必然落第 4 档，已移出至 T8）。

```
算法步骤（主控 LLM 兜底执行）：
1. 检查审计报告最新版：列出 audits/审计报告-vN.md → N 取最大 → 必须存在
2. P0/P1 清单已**显式列出**：读 audits/审计报告-vN.md → **P0/P1 条目数可为 0**（审计零缺陷是正常结果，不是失败）；**但必须显式写「本轮无 P0/P1」**，不得留空或以未列示代替；出现 P0/P1 条目时须逐条列明。
3. M 门（M-Form 8 项 + M-Exist 3 项）**全部判定通过**：读**当前轮已产出**的章节级 M 门记录 + `status.md`「7.三.五 M 门执行记录表」→ 全部 true（**不得依赖 `final/M-Gate-Report-v2.2.12.json`**：该文件由 T8 终检产出，而 T7.5 在 T8 **之前**执行 —— 前后依赖倒置会使门必然判失败或被迫推断，2026-09-12 审计 P1-6）
4. 信任级别一致性：M-Exist-3 判定为「通过」（第 1 档）→ 通过；不通过 / 无法判定 / 路径或参数错误 → 按对应档处置（不将后者当作内容缺陷）
5. 论文交付物 vs 操作员报告独立隔离：
   - `drafts/current_draft.md`（当前工作草稿）不含 audits/ 内容（避免草稿混入审计残留）
   - 隔离范围在 §隔离性核查 详写；本闸门仅以草稿 ↔ 报告的边界做最小检查
6. **删「主人签字 Phase 5」**：T7.5 是**机械检查点**（LLM 结构化判定，非机器强制）（T7 审计 → T8 终检），主人签字在 Phase 5（T8 终检交付后主人验收），**不在** T7.5 闸门里；原「如有修订回环 ≤2 轮降级触发则主人读局限性.md」逻辑，改为 T8 终检交付时一并请主人验收（含局限性声明）
7. **修订轮流程约束**：检查本轮修订是否由独立写手子代理执行
   - 证据：status.md 修订回环记录写明「spawn 独立写手 vN 执行」
   - 若发现主控代执行 → 打回修订轮，强制 spawn 独立写手
   - 例外：主控直接 edit 定点修复（<5 处纯校对类）不视为违反
8. 判定（四档，v2.12.56 M-5 对齐）：1-5 + 7 项全通过（步骤 6 为「删主人签字」元说明，非检查项）→ T7.5 **通过（第 1 档）**派发 T8；任一失败 → **不通过（第 2 档）**不派发 T8；审计报告不存在 → **路径或参数错误（第 4 档）**（不触发修订）；审计报告 P0/P1 段不可读或本轮 M 门记录缺失 → **无法判定（第 3 档）**（不触发修订，补证据后重跑同一判定）

伪代码：
# 第 0 步：输入新鲜度（见 §闸门第 0 步）
if not exists('audits/审计报告-vN.md'):
    return verdict_path_error("audits/ 下无审计报告（路径或参数错误，不触发修订）")

audit_latest = get_latest_audit_report('audits/')   # helper 无机械实现 → LLM 推理替代（见 §未定义 helper 清单）
if not audit_latest:
    return verdict_path_error("audits/ 下无审计报告（路径或参数错误，不触发修订）")
p0_p1_listed = check_p0_p1_listed(audit_latest)
m_gate_ok = check_m_gate_all_pass_current_round()  # 读**本轮已产出**的章节级 M 门记录 + status.md「7.三.五 M 门执行记录表」；**不得读** final/M-Gate-Report-v2.2.12.json（T8 产物，T7.5 时尚未生成 —— 2026-09-12 审计 P1-6）
sha256_ok = check_evidence_sha256_placeholder('final/交付说明.md')  # 未回填/占位符 => pending_owner_verification，不得判通过
trust_ok = check_M_Exist_3(...)
isolation_ok = check_draft_vs_report_isolation('final/定稿.md', 'final/交付说明.md', 'audits/')
revision_independent = check_revision_by_independent_writer('status.md')
# 失败项逐条列出（不得只给「有失败」）
fail_reasons = [
    name for name, ok in [
        ("审计报告最新版", bool(audit_latest)),
        ("P0/P1 清单已列", p0_p1_listed),
        ("M 门全过（本轮记录）", m_gate_ok),
        ("证据包指纹占位符", sha256_ok),
        ("信任级别一致性", trust_ok),
        ("论文 vs 报告隔离", isolation_ok),
        ("修订轮独立写手", revision_independent),
    ] if ok is not True
]

# 四档出口（见 §统一抽取规则真源 C）
if p0_p1_listed is None or m_gate_ok is None:
    return verdict_undecidable("审计报告 P0/P1 段不可读或本轮 M 门记录缺失，不足以判定")
all_pass = audit_latest and p0_p1_listed and m_gate_ok and sha256_ok and trust_ok and isolation_ok and revision_independent  
if all_pass:
    return verdict_pass(**{"审计报告": str(audit_latest)})
else:
    return verdict_fail("T7.5 完整性门未全过", **{"失败项": fail_reasons})
```

---

