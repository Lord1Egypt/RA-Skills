---
slug: industry-deep-dive-pipeline-skill
displayName: Industry Deep-Dive Pipeline
not_for:
  - Quick single-pass summaries or news recaps (multi-stage research pipeline)
  - Marketing copy, product one-pagers, or social posts (long-form article output)
  - Publishing or distributing the finished article (stops at publish-ready draft)
  - Research without a topic brief or source materials (needs an input corpus)
name: industry-deep-dive-pipeline
description: >
  This skill should be used when turning a topic brief, research materials,
  vendor case, policy event, or industry question into a publish-ready single
  deep-dive article for technology, AI, data, cloud, or enterprise-software
  audiences. It runs source verification, originality and competition review,
  full editorial planning, two human decision gates, drafting, deterministic
  red-line checks, an existing eight-role review panel, revision, and final
  evidence packaging. It stops at an approved Markdown article plus evidence and
  review records; it does not create publication layouts, covers, social copy,
  CMS drafts, or publish content.

  【适用】中立第三方产业深度研究 / 行业长文（个人 IP、公众号深度稿、厂商案例的独立分析）。【不适用】品牌营销稿、产品稿、按 content brief
  写的推广文、技术教程——这类内容请用对应项目工作区里专门的写作 Skill；本 Skill 不做品牌露出与营销措辞，也不产出发布物料。
description_zh: 产业深度文章全流程编排
description_en: Industry deep-dive pipeline
version: "1.1.5"
agent_created: true
read_when:
  - 产业深度文章
  - 行业深度稿
  - 从选题到定稿
  - 原创性复核与写作
  - 科技行业长文
  - industry deep dive
  - research article pipeline
allowed-tools:
  - Read
  - Write
metadata:
  openclaw:
    permissions:
      - file_read
      - file_write
---

# Industry Deep-Dive Pipeline

将单篇科技、AI、数据、云和企业软件产业选题推进到审核通过的正式 Markdown。采用 Prompt Chaining + Evaluator-Optimizer：固定主链保证可追踪，八角色会审后的修订循环保证质量。

## When to use

- 输入包含选题简报、事件、厂商案例、政策变化或研究材料，需要形成有判断、有证据、有边界的深度文章。
- 需要先查中文与英文同类内容，确认信息增量和表述撞车风险。
- 需要在正文前完成目标读者、核心判断、论证链、反方、结构、标题和风险策划。
- 需要事实表、原创性复核、会审记录和终稿复检形成完整证据包。

## Do not use

- 新闻快讯、摘要、产品说明书、技术教程或营销稿。
- 厂商大会全景报告；改用 `vendor-summit-report`。
- LinkedIn 单平台短观察；改用 `linkedin-industry-observation`。
- 微信排版、封面、摘要、关键词、社交物料、CMS/Notion 入库或发布；交给独立发布套件。
- 多篇系列的自动排期与批量生成。系列信息仅作单篇上下文。

## Required inputs

读取 `references/planning-schema.md`，建立 case bundle。至少确认：

- `topic`
- `source_materials`
- `target_reader`
- `target_format`
- `length_range`
- `writing_profile`
- `timeliness`
- `confidentiality`

可选输入：合集或系列关系、历史平台信号、必须处理的反方、本篇新增红线、时效窗口和用户已有假设。

## Workflow

### Step 1: [Deterministic] Diagnose input

1. 校验路径、URL、日期、目标格式和 writing profile。
2. 判断文章类型、时效等级、事实风险与敏感性。
3. 把用户已有判断标为待验证假设，不直接当成结论。
4. 复制 `templates/case-brief.template.md` 为 `00-case-brief.md`。
5. 运行：

```bash
python scripts/validate_case_bundle.py --case-dir <case-dir> --stage input --enforce
```

输入门禁失败时停止，报告缺项。

### Step 2: [LLM] Build fact table

1. 从材料提取数字、日期、公司、政策、产品状态、引述和因果声明。
2. 使用搜索发现来源，回到官网、财报、论文、监管原文或官方发布核验关键事实。
3. 高风险事实至少双源确认，或由一手权威源确认。
4. 记录原始日期、核验日期、状态、来源等级、可使用措辞和失效条件。
5. 复制 `templates/fact-table.template.md` 为 `01-fact-table.md`。
6. 按需读取 `references/evidence-and-originality.md`。

### Step 3: [LLM] Review originality and competition

1. 拆出核心判断、分析框架和标志性表达。
2. 搜索中英文新闻覆盖、同主题分析和高度相似论证。**⚠️ 外发前确认**：待搜的核心判断、分析框架与标志性表达可能来自未公开/内部材料；向第三方搜索服务发送前须确认这些内容允许外发，未经确认只发最小化、脱敏后的查询片段，或跳过外发并把原创性标为「本地待核」。
3. 区分公共观点、独立深化、可验证差异和表述撞车。
4. 主动查找直接反方、历史反例和证伪变量。
5. 输出 `02-originality-review.md`。

以下情况停止：核心判断已被充分覆盖且无信息增量；论点依赖无法核实的事实；选题只能依靠夸大标题成立。

### Step 4: [LLM] Produce full planning brief

1. 复制 `templates/planning-brief.template.md` 为 `03-planning-brief.md`。
2. 完成选题可行性、竞争程度、读者分层、核心判断、论证链、原创锚点、反方、标题、结构、收藏载体、风险和系列关系。
3. 只保留真正需要人做价值判断的待确认项。
4. **标题与每个小标题都要过落地测试**：能不能当判断句读？是否需要额外解释才明白？抽象概念名、读者导向式锚定（"谁该关注，谁不必"）、纯结构架子（"三条路径，同一道边界"）都是空标题，必须在 Gate A 前替换成带内容的结论式表述。
   - **「概念＋判断」不是字面格式门禁**：两个抽象名词并列（如「跨国同源与组织孤岛」「被动适配与主动多云」）不自动等于有实质。标题单独抽出时必须让读者读出**对象、关系和方向**：谁与谁发生什么关系，哪一侧受限，或什么结果已经出现。若必须读完整节才能把名词翻译成判断，继续改成具体动作或反常关系；如「同源平台落地，组织仍然孤立」「接入既有云，不能自建区域」。
5. **术语自检**：任何缩写先问"读者看到这个词能不能还原出它指什么"。内部惯用缩写（把"跨组织共享网络"写成"网络"）不得进标题与正文，宁可换一个更长但能懂的说法。替换术语会连锁改变标题字数，必须同时复核标题长度上限，超限按"术语可理解性优先"处理并记 known deviation ＋ 给一个合规备选。
6. **同行价值与产品范式检查**：如果事实表或策划 brief 已识别出可迁移的产品范式、架构选择或技术路线（如语义层进入治理目录、Agent 控制平面、上下文工程），不能被区域清单、合规结构或预算分析压缩成一两句。同行读者要能读出「能拿走的范式」；边界证据支撑限制判断，不能替代全文价值。

### Gate A: [Human] Confirm planning

暂停并确认：核心判断、标题方向、篇幅与取舍、争议处理、平台目标和系列关系。确认前禁止写正文。

### Step 5: [LLM] Draft article

1. 只使用确认后的策划与事实表。
2. **开头留存门**：前两段必须先让读者知道交付了什么、缺了什么、为什么值得继续读；法人、签约、底层基础设施只保留能直接解释主判断的 1–2 句，其余后移。若前三段仍主要在回答「谁和谁签合同」，说明证据先于命题，必须重写开头。
3. 判断先行，论据、反方和边界随后展开。
4. 禁止补入事实表中没有的新数字、日期、状态和强结论。
5. 禁止把任务背景、内部备注、发布信息和写作过程带入正文。
6. **视角锁定在读者一侧**：正文主语用读者的主体身份（如"公司"），不用厂商口吻的"客户"分层表述（"哪些客户不必关注""另一批客户不必关注它"）。这类句子读起来像卖方在做客户细分，不是行业观察。
7. 输出 `04-draft.md`；只保留必要的图表占位。

### Step 6: [Deterministic] Run machine gate

运行：

```bash
python scripts/scan_draft_gates.py \
  --draft <case-dir>/04-draft.md \
  --facts <case-dir>/01-fact-table.md \
  --profile <writing-profile.json> \
  --output <case-dir>/05-machine-gate.json \
  --enforce
```

检查未登记数字、凭据、UUID、个人路径、元信息、对举句、营销词、口语缓冲和 profile 红线。失败时回到 Step 5 修订并重跑。

### Step 7: [LLM] Run eight-role review

调用 `tech-content-review-panel`，复用 G1/G2、R1-R4、G3 和 T1。复制 `templates/review-record.template.md` 为 `06-review-record.md`，将意见分为必改、建议改、可选和张力项。

### Gate B: [Human] Resolve real tensions

仅在出现传播与专业、深度与完读、风险与表达、系列一致与单篇独立等真实张力时暂停。事实错误、来源缺失、格式错误和明确红线由流程直接修正，不推给用户决定。

### Step 8: [LLM] Revise to final

1. 处理全部必改和建议改。
2. 按 Gate B 决策处理张力项。
3. 禁止接受会审中新出现且未经核验的事实。
4. 记录未采纳意见及理由，避免重复提出。
5. 输出 `07-final.md`。

### Step 9: [Deterministic + LLM] Re-check

1. 重核事实、时效和来源。
2. 对 `07-final.md` 重跑 `scan_draft_gates.py`，输出写 `05-machine-gate-final.json`，**不覆盖初稿的 `05-machine-gate.json`**——保留「初稿门禁 → 会审 → 定稿门禁」三段的审计链。
3. 人工通读检查机器难以识别的 AI 腔、逻辑跳步和姿态越界。**机器正则抓不到元语言与预告式句式，必须逐条清**：方法预告（"最省事的办法是把它的能力分成两类"）、导引词（"分开看会更清楚""需要把口径说清楚""有一处需要留意的是""一个容易被忽略的事实是""同样需要限定"）、写作自指（"把这几条写下来是为了…"）。同时清总起句＋冒号，判据是「冒号前的句子删掉不减信息量」，改写方向是揉成连贯陈述，不是把冒号换成句号。对举按宽口径计数：正则只匹配「不是…是／而非」，但「而不是／而不在于／而不只是」同属对举家族，总量按「标题 1 ＋ 判断位 2」控制。
4. 对照策划，确认判断、范围、标题和表格一致；**并重核字数是否仍在 `length_range` 内**——修订往往会削掉上百汉字，回补的内容必须已在事实表内有支撑，不得为凑字数引入新事实。
5. **跑本地排版与表达体检脚本**（若项目有 `check_boundary_style.py` 这类工具）：汉字数／破折号／对举／表格与 bullet／小标题字数／黑名单词／引号成对／总起句＋冒号。**总起句＋冒号的检测口径是"首句冒号"**——按行内第一个冒号判断会把整段的引述句误报成铺垫句（实测一篇能报出 15 处假阳性）；同时要排除冒号后紧跟引号（直接引语）的情形。检测出的每一项都要人工判定，不能直接当成问题清单。
6. **复查四处一致性**：① 术语——被替换掉的旧缩写是否还有残留（标题、小标题、引言、收束四处最容易漏）；② 视角——主语是否统一在读者一侧；③ 结构——节标题读一遍，凡"删掉它该节判断仍然成立"的都是架子，要重写；④ **开头留存与范式覆盖**——前两段先亮交付价值与边界，已在策划中登记的同行可迁移范式不得在成稿中消失或退化为一两句。
7. 会审张力项若能被上游写作规范直接裁决（如 `tech-writing-pipeline` §4「媒体视角与专家视角分界表」把启动方式列为硬规则），在 `06-review-record.md` 与 case brief 记 `gate_b: not_required` 并写明裁决理由，不推给用户；`--stage final` 要求该字段为 `approved` 或 `not_required`。
8. 输出 `08-final-check.md`。
9. 运行：

```bash
python scripts/validate_case_bundle.py --case-dir <case-dir> --stage final --enforce
```

### Step 9.5: [LLM] Expression-precision review (long-form articles)

`--stage final` 全绿只说明事实、结构与机器红线过关，**不说明用词精度过关**。目标读者是行业读者的长文，在 Step 9 之后、Step 10 之前，必须再按 `tech-writing-pipeline` §5「评审与收紧循环」＋ §5.1「reader-fit 阅读测试」跑一次表达层评审，评审团用 `tech-content-review-panel` 八角色，输出落 `09-language-review.md`。

1. 先跑 `tech-writing-pipeline` Verification 的五组 grep（AI 腔／铺垫冒号／预告式、黑话与破折号、对冲词、说教与祈使、口语缓冲），记录修订前命中数。
2. 八角色逐条给意见，**级别只看表达，不重开事实与原创性裁决**（G1 引用已通过的终检结论）。重点关注：术语误用（把数学词、系统词用在商业语境）、动词错配、指代不明、主语越位（观察文里突然出现厂商口吻与第二人称）、造作书面语与口语混杂、前后表述冲突（同一事实两处说法不同，读者判定作者自相矛盾）。
3. reader-fit 选 3–4 个与定位匹配的角色，问统一五问；只采纳与定位锁兼容的修改，被拒的建议要写明理由。
4. 修订后复跑：机器门禁、Verification 五组 grep、排版体检、`validate_case_bundle.py --stage final --enforce`，并重核 `length_range`（表达收紧常净减几十到上百汉字）。
5. 同步更新 `08-final-check.md`（新增表达精度评审一节与最终字数）与 `FINAL-PACKAGE.md`（word count、Review 段），并重新复制语义名交付稿、核对哈希。
6. **收口复查四项**（机器门禁与 grep 都抓不到，必须逐段人工过）：① 缺空行造成的段落粘连——两段黏成 400＋字裸段，Markdown 不报错、脚本不报错（2026-09-11 实测：改稿时丢了一个空行，两段并成一段）；② 单段超 200 汉字；③ 段内话题突转（如存储话题段末尾突然接到生态位缺口），应拆段；④ **同一判断在两处说两遍**——多轮修订最容易留下，读者会读成作者重复自己。四项按「拆段／删重复」处理，不靠换词。
7. **删重复导致字数跌破 `length_range` 下限时，只从事实表内「已登记但正文未使用」的条目回补**（2026-09-11 海外版删掉 181 字重复内容后回补 F045／F012／F031），不得新造事实，也不得把评论扩写成填充。回补后重跑全链。

**触发条件**：面向行业读者的长文一律执行；2026-09-11 的实测教训是标题已确认合格时仍被指出"表达精度用词一般"——**标题过关不等于用词过关，会审通过不替代这一轮**。

### Step 10: [Deterministic] Package deliverables

复制 `templates/final-package.template.md` 为交付说明。交付：`07-final.md`、事实表、原创性复核、确认后的策划、会审记录和终稿复检。

**另出一份语义名交付稿**：`07-final.md` 这类编号名在全局搜索时看不出内容。在项目的稿件目录（如 `articles/drafts/`）按「完整标题-版次-日期」复制一份，供检索与直接取用。两处内容必须逐字节一致（复制后用哈希核对），任何后续改动都回到 case 目录改，再重新复制——不要把交付稿当成可独立编辑的第二份稿子。case 内仍保留 `07-final.md`，机器校验依赖它。

## Hard Rules

1. 搜索用于发现，关键事实回到一手来源。
2. 用户假设必须经过验证，不因用户提出就视为事实。
3. 原创、首创、唯一等判断必须有检索证据和边界。
4. Gate A 未确认不得写正文。
5. Gate B 只处理真实价值张力，不把事实和格式问题交给用户。
6. 正文中的高风险数字、日期和状态必须出现在事实表。
7. 改稿后必须重跑机器门禁并人工通读。
8. 私有写作 profile 只按需读取，不复制进通用 Skill 或公开包。
9. 输出止于审核定稿和证据包；禁止生成或执行发布动作。
10. 任何工具失败执行重试与交叉验证；修复后必须重跑。

## Failure Handling

| 场景 | 处理 |
|---|---|
| 输入材料缺失 | 停止，列缺项，不猜测内容 |
| 高风险事实无法确认 | 删除、降级或标记待核，禁止进入强判断 |
| 原创空间不足 | 停止写作，给出合并、换角度或放弃建议 |
| Gate A 未确认 | 保持任务进行中，不生成正文 |
| 机器门禁失败 | 修订对应问题并重跑，最多两轮后报告剩余阻塞 |
| 会审新增未经核验事实 | 拒绝纳入，回到事实表核验 |
| Gate B 未确认 | 保留张力项，暂停终稿修订 |
| 工具首次失败 | 同操作重试 1-2 次，再换工具交叉验证 |
| 最终验证失败 | 不标完成，不生成发布物料 |

## Output Format

```text
<case-dir>/
├── 00-case-brief.md
├── 01-fact-table.md
├── 02-originality-review.md
├── 03-planning-brief.md
├── 04-draft.md
├── 05-machine-gate.json
├── 06-review-record.md
├── 07-final.md
├── 08-final-check.md
├── 09-language-review.md   # 长文必产（Step 9.5 表达精度评审）
└── FINAL-PACKAGE.md
```

## References

- `references/planning-schema.md`：输入、策划和 case bundle 字段。
- `references/evidence-and-originality.md`：来源分级、事实状态和原创性判断。
- `references/writing-profile-interface.md`：私有写作 profile 接口。
- `references/replay-evaluation.md`：Fireworks、Kimi 和欧洲 AI 回放标准。

## Pitfalls

- 公司案例写成公司介绍，产业判断退到次要位置。
- 原创性复核只搜同标题，遗漏同论证不同表述。
- 会审后改稿未复扫，重新引入红线和事实错误。
- 定稿重扫直接覆盖 `05-machine-gate.json`，丢掉初稿门禁记录，审计链断裂。
- 门禁全绿就交付：元语言、预告式句式、总起句＋冒号、宽口径对举（而不是／而不在于）全部过不了正则，只能靠 Step 9 通读逐条清。机器 P0/P1 为 0 不等于表达过关。
- **标题确认合格就以为全篇过关**：2026-09-11 的退回是"目前标题够了，但表达精度用词一般"。机器门禁、八角色会审、终检复扫三关全过，仍可能存在术语误用、动词错配、指代不明、前后表述冲突、造作书面语与口语混杂。这些只有 Step 9.5 的表达精度评审抓得到，**不能省**。
- 前置会审与表达评审混成一件事：`tech-content-review-panel` 的八角色在 Step 7 判的是原创、深度、论证与红线；用词精度要在 Step 9.5 用 `tech-writing-pipeline` §5／§5.1 的流程单独跑，两轮不能互相替代。
- 术语用内部缩写：把"跨组织共享网络"缩写成"网络"放进标题，读者无法还原它指什么。同时别忘了替换术语会改变标题字数，超限要显式记 known deviation。
- 视角写成厂商口吻：正文主语用"客户"，写出"哪些客户不必关注"这类卖方细分句式。读者的主体身份应当直接做主语。
- 小标题是架子：写成"三条路径，同一道边界"这类结构描述，删掉它该节判断仍然成立，等于没有标题。
- **把「概念＋判断」执行成形式**：两个抽象名词并列、字数合格、语气像结论，不代表读者能读出对象—关系—方向；标题单独抽出必须能读出谁与谁的关系及方向。2026-09-11 定调：**概念张力优于口语化直陈**（「跨国同源与组织孤岛」优于「同源平台落地，组织孤立」），但空架子（删掉后该节判断仍成立）仍然不行。
- **证据先于命题的开头**：先花三段讲签约主体、底层云和 legal 流程，读者还不知道文章要证明什么；开篇应先给反常事实、读者价值和主判断，法人结构只保留解释判断所需的最少信息。
- **边界清单吞掉同行范式**：八项不可用功能和预算竞争都容易写得很扎实，却把语义层进入治理目录、Agent 控制平面、上下文工程等可迁移路线压成背景句；同行读者的「能拿走什么」必须成为独立论证段。
- 把体检脚本的原始输出当问题清单：总起句＋冒号检测器若按行内第一个冒号判断，会把带引述的整段误报（实测一篇 15 处假阳性），必须人工逐条判定而非直接改。
- 语义名交付稿当成可独立编辑的第二份稿子，导致与 case 内 `07-final.md` 漂移。交付稿只能是副本，改动必须回 case。
- **把评审意见当成交付物**：诊断表列全了却写「待确认后再动」，作者会判定这是在用流程回避改写（2026-09-11 连退两轮）。表达层的诊断一旦成立，就是改写的指令。
- **多轮修订后的段落粘连与重复判断**：改稿时丢空行会让两段并成 400＋字裸段；同一判断被写进两个相邻段落（海外版第 79 与 81 段把三路径取舍说了两遍）。两者机器都查不出，只有收口时逐段过。
- **同一文件多处修订禁止并行 Edit（2026-09-11 事故）**：同一消息里对同一文件发多个 Edit，每个都独立读-改-写回整份文件，互相覆盖，全部报成功但只有最后一个存活（实测 8 个并行只剩 1 个、14 个分批只剩最后 1 个）。多改动落盘必须单次 Write 全量写回，或严格串行（一轮一个 Edit）。暴露信号：复扫时小标题显示旧版、已修掉的 P1 回归。
- **误覆盖后的回滚源是语义名交付稿**：`articles/drafts/` 语义名交付稿与 case 内 `07-final.md` 逐字节一致（md5 比对），是误覆盖或误重构后唯一可靠的恢复源（海外版曾因四节重构误删最强论据节、品类定位改单品，靠交付稿救回）。结构性改版前先 dump 纯文本快照做字符级 diff，否则内容零丢失无从校验。
- **变更范围越权（2026-09-11 P0 事故）**：用户指令只让改国内版，执行中把反馈内容套到海外版做四节重构，返工约 10 分钟。铁律：反馈「两版看起来都适用」是技术判断，不是变更授权；动手前先声明「本轮触碰文件清单」，扩大范围必须先回报确认。收口时校验实际修改文件 ⊆ 声明清单，越界即说明原因。
- **批量 Edit 后立即关键串复扫**：批量或串行多个 Edit 落盘后，立即 grep 关键串计数（标题、小标题、本轮已修句式、门禁曾报的 P1 串），确认全部改动真实存活，再进入下一步。依据：Edit 的成功返回值不可信（2026-09-11 实证静默丢失），只有内容级验证能闭环。
- 把摘要、关键词、标签、封面提示词或发布备注混入正文。
- 系列上下文变成跨篇自指，导致单篇无法独立成立。
- 为减少打断跳过 Gate A，最终围绕错误判断写完整篇文章。
- 主题判断成立不等于策划逻辑成立：把“度量/采购/验收”写成操作清单，会偏离产业研究的方法链。策划必须明确“厂商说了什么、做了什么、想争什么、市场会不会买单、行业如何演化”，操作性框架只能作为证据载体。
- 由调查报道触发的主题，不能把争议个案直接升格为行业结论；要把各方动作、利益关系和时间表放在同一分析链上，并保留事实冲突。

## Verification

- [ ] 必填输入齐全，case bundle 通过 input 校验。
- [ ] 高风险事实可追溯率 100%。
- [ ] 原创性复核覆盖中英文同类内容、反方和证伪变量。
- [ ] Gate A 有明确确认记录。
- [ ] 初稿机器门禁通过后才进入会审。
- [ ] Gate B 只包含真实张力项。
- [ ] 终稿重跑机器扫描并完成人工通读。
- [ ] 长文已跑 Step 9.5 表达精度评审，产出 `09-language-review.md`，Verification 五组 grep 归零。
- [ ] 术语与视角一致性复查完成：无旧缩写残留，主语统一在读者一侧，每个小标题删掉后该节判断不成立。
- [ ] 收口复查完成：无段落粘连（缺空行）、无 >200 汉字裸段、无段内话题突转、同一判断未在两处重复。
- [ ] 语义名交付稿已产出，且与 case 内 `07-final.md` 哈希一致。
- [ ] 凭据与私有标识 P0=0。
- [ ] 输出不包含发布物料或外部动作。
- [ ] 初稿门禁 05-machine-gate.json 未被定稿重扫覆盖，定稿门禁单独写入 05-machine-gate-final.json（保留初稿门禁 → 会审 → 定稿门禁三段审计链）。
- [ ] case bundle 通过 final 校验。
- [ ] Gate A 的确认结论（继续／修改／终止）已写明，未取得确认时不进入初稿步骤。
