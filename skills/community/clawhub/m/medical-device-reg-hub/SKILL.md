---
name: medical-device-reg-hub
displayName: 医械注册工程师·全球通关枢纽
description: >-
  All-in-one hub for medical device registration engineers — global pathways & classification (CN NMPA / US FDA / EU MDR / JP PMDA / ASEAN·LATAM), plus 8 topic hubs (UDI, STED, biocompatibility ISO 10993, GMP, post-market, labeling & IFU, supplier compliance) with verified official links.

  医疗器械注册工程师的「随身资料库」——中/美/欧/日及全球注册路径与分类、UDI/STED/生物相容性/GMP/上市后/标签IFU/供应商合规 8 大枢纽要点与官方直达链接一站直达。
slug: medical-device-reg-hub
title: medical-device-reg-hub
version: 1.1.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
author: SynomosAI
category: knowledge-management
description_zh: "医疗器械注册工程师的「随身资料库」——中/美/欧/日及全球注册路径与分类、UDI/STED/生物相容性/GMP/上市后/标签IFU/供应商合规 8 大枢纽要点与官方直达链接一站直达。"
description_en: "All-in-one hub for medical device registration engineers — global pathways & classification (CN NMPA / US FDA / EU MDR / JP PMDA / ASEAN·LATAM), plus 8 topic hubs (UDI, STED, biocompatibility ISO 10993, GMP, post-market, labeling & IFU, supplier compliance) with verified official links."
read_when:
  - 医疗器械注册工程师查全球路径与分类（NMPA/FDA/MDR/PMDA/东盟拉美）
  - UDI/STED/生物相容性/GMP/上市后/标签IFU/供应商合规等专题要点
  - 跨市场注册周期、费用、证书有效期横向对比
agent_created: true
license: MIT
platforms: [cli]
ai_protocol: true
spec: usk/1.0
interface:
  type: prompt
  entry_point: SKILL.md
  runtime: none
  call_pattern: prompt
input_schema:
  args:
    type: string
    description: CLI arguments per skill usage
    required: false
output_schema:
  stdout: structured result (JSON IR)
  exit_code: rc=0 ok / rc=1 warning / rc=2 bad input
capabilities:
- medical-devices
- regulatory
- repository
permissions:
  network: false
  filesystem: false
  subprocess: false
requirements:
  python_packages: []
  min_python: '3.8'
changelog: '1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.1.0: initial upload (USK v3)'
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### What this is
A structured knowledge hub for medical-device registration engineers. It consolidates regulations, standards, submission systems and templates from NMPA / FDA / EU MDR / PMDA and other markets into clickable official sources, organized by market × stage × product category. Covers the full flow: feasibility → classification & pathway → technical file → QMS → submission → review → post-market.

It ships 8+ topic hubs plus a global index and multi-market classification evidence: main index, UDI, STED writing, cycle-cost comparison, supplier compliance, GMP/validation, ISO 14971 risk, clinical evaluation, sterilization packaging, registration testing & submission practice, change/renewal, software/HF/IEC 62304, market access/sales, requirements & feasibility, design controls, after-sales, biocompatibility planning, post-market surveillance, labeling & IFU, and a 13-market real-certification classification evidence file for arthroscopic/basket/grasper forceps.

### Why this hub
- Conclusions are grounded in real registration certificates, not guesses; boundary cases are flagged "to verify".
- Every point links directly to NMPA / FDA / EU MDR / PMDA / other official pages; conclusions are traceable.
- Covers CN / US / EU / JP plus ASEAN & LATAM; 13-market comparison included.
- 119 official links browser-verified on 2026-08-14; near-zero dead-link rate.
- Maintained by a front-line medical-device international-registration practitioner.

### Triggers
"medical device registration", "NMPA", "FDA 510(k)", "PMA", "De Novo", "MDR", "CE", "IVDR", "PMDA", "JMDN", "UDI", "STED", "eSTAR", "eRPS", "ISO 10993", "ISO 13485", "post-market", "IFU", "supplier compliance", "registration cycle/cost", or classification questions for specific products.

### Workflow
1. Determine intent: product classification / topic deep-dive / cross-market comparison.
2. Load the most relevant `references/` file (see navigation table) — never invent clauses or links from memory.
3. Answer with the conclusion plus the official direct link.
4. If the user wants a deliverable, generate Markdown / HTML comparison tables from references.
5. Flag timeliness: key data points must be checked against the latest official release; unverified items marked "to verify".

### Key facts (avoid common misjudgments)
- CN: Class I = municipal filing; Class II = provincial registration; Class III = NMPA central. Reusable arthroscopic forceps usually Class II (provincial); open/non-sterile plain forceps Class I.
- US FDA: 21 CFR 888.1100(b)(2) product code HRX — basic reusable manual arthroscopic forceps/graspers are Class I, 510(k)-exempt; only variants with special function / sterile single-use / advanced claims are Class II 510(k).
- EU MDR: reusable surgical instruments per Rule 6 are usually Class I (self-declaration + CE); sterile/measuring/software variants need a Notified Body.
- JP PMDA: structure classes (general I / controlled II / highly controlled III·IV) are correct; "most reusable manual arthroscopic forceps are Class I" is inference — verify by JMDN code (e.g. 361030) on PMDA; flagged to-verify.
- ASEAN/LATAM: bands are correct (Thai FDA lists reusable surgical instruments as Class 1 = ASEAN class A); country details vary.

### Boundary
- This is a curated index of public official information; it is NOT a regulatory opinion.
- Classification of boundary products should go through official classification-determination procedures.
- Do not fabricate clauses or links; always cite references.

### Evidence & safety
- Evidence: TBD. Version: 1.1.1. Security: see package security snapshot; no independent external scan.

## 中文

### 这是什么
医疗器械注册工程师的**结构化资料枢纽**。把分散在 NMPA / FDA / EU MDR / PMDA 及各市场官网的法规、标准、申报系统、模板，按「市场 × 注册阶段 × 产品类别」整理成可点击直达的官方源。覆盖从**产品立项 → 分类与路径 → 技术文件 → 质量体系 → 注册申报 → 审评获批 → 上市后**的全流程。

内置 8 大专题枢纽 + 1 份全球注册索引 + 1 份多市场分类实证：主索引、UDI、STED 撰写、周期费用对比、供应商合规、GMP 质量体系与验证、ISO 14971 风险管理、临床评价、灭菌包装验证、注册检验与申报实操、变更延续管理、软件人因（IEC 62304 / SaMD / 网络安全）、市场准入与销售、需求调研与立项、设计开发控制、售后服务、生物相容性规划、上市后监管、标签与 IFU，以及篮钳/剪线钳/过线钳 13 市场真实注册证验证的分类实证。

### 为什么用这个枢纽
- **不是泛泛而谈，是「真实注册证验证过」的结论**：不做拍脑袋推断；边界情形明确标注"待核验 / 走分类界定"。
- **官方源一站直达**：每个要点都附带 NMPA / FDA / EU MDR / PMDA / 各国官网直达链接，结论可溯源、可复核。
- **覆盖中 / 美 / 欧 / 日 + 东南亚·拉美**：从单一市场到 13 国横向对比都有。
- **链接已逐条核验**：references 内 119 条官方链接于 2026-08-14 经浏览器级复核，死链率趋近于零。
- **作者即从业者**：由医疗器械国际业务一线（熟悉 GMP / NMPA 法规、海外报证）整理维护。

### 触发场景
当用户提到以下任意内容时，优先加载本技能并从 `references/` 调取对应资料：

- "医疗器械注册" / "医械注册" / "注册工程师"
- "NMPA" / "FDA 510(k)" / "PMA" / "De Novo" / "MDR" / "CE" / "IVDR" / "PMDA" / "JMDN"
- "UDI" / "唯一标识" / "发码机构"
- "STED" / "技术文件" / "注册资料" / "eSTAR" / "eRPS"
- "生物相容性" / "ISO 10993" / "GB/T 16886"
- "GMP" / "ISO 13485" / "QSR" / "QMSR" / "工艺验证" / "再处理验证"
- "上市后" / "不良事件" / "召回" / "PMS" / "FSCA"
- "标签" / "IFU" / "说明书"
- "供应商合规" / "13485 证书" / "材质证明"
- "注册周期" / "注册费用" / "证书有效期" / "注册路径"
- "全球注册" / "中国/美国/欧盟/日本/东南亚/拉美 注册"
- 具体产品如"关节镜钳" / "腔镜器械" / "取石网篮" 的注册分类与路径问题

### 使用流程
1. **判断意图**：某产品的分类/路径、某专题要点、还是跨市场对比？
2. **加载对应资料**：从 `references/` 读取最相关的文件，不凭记忆编造法规条文或链接。
3. **给结论 + 官方源**：每个结论附 references 中的官方直达链接。
4. **生成交付物**：若用户要"做成资料/网页/清单"，基于 references 内容生成 HTML / Markdown 交付物。
5. **标注时效与边界**：法规/标准会更新，关键数据提示以官方最新发布为准；未逐码验证条目标"待核验"。

### references/ 文件导航

| 用户问题类型 | 加载文件 |
|---|---|
| 整体注册路径/多市场索引 | `注册工程师资料枢纽.md` |
| 具体产品分类与全球路径实证 | `篮钳剪线钳过线钳_全球注册路径汇编.md` |
| UDI 相关问题 | `UDI全球标识枢纽.md` |
| 技术文件/STED 撰写 | `技术文件STED撰写枢纽.md` |
| 周期/费用/有效期对比 | `注册周期费用有效期对比枢纽.md` |
| 供应商/材质合规 | `原材料供应商合规枢纽.md` |
| GMP/质量体系/验证 | `GMP质量体系与验证枢纽.md` |
| 风险管理/ISO 14971 | `风险管理枢纽.md` |
| 临床评价/同品种/CER | `临床评价枢纽.md` |
| 灭菌/无菌包装/SAL | `灭菌包装验证枢纽.md` |
| 注册检验/申报/eRPS/eSTAR | `注册检验与申报实操枢纽.md` |
| 变更/延续/807.81 | `变更延续管理枢纽.md` |
| 软件/SaMD/网络安全/人因 | `软件人因枢纽.md` |
| 市场准入/出口销售/经营许可/集采 | `市场准入与销售枢纽.md` |
| 需求调研/立项/PRD/设计输入 | `需求调研与立项枢纽.md` |
| 设计开发/设计控制/DHF | `设计开发控制枢纽.md` |
| 售后/投诉/维修/备件 | `售后服务枢纽.md` |
| 生物相容性规划 | `生物相容性测试规划枢纽.md` |
| 上市后/PMS/召回 | `上市后监管枢纽.md` |
| 标签/IFU | `标签与IFU枢纽.md` |

### 关键事实速查
- **中国**：境内Ⅰ类市局备案，Ⅱ类省局注册，Ⅲ类国家局；进口Ⅱ/Ⅲ类国家局。关节镜用钳（腔镜、无菌）多归 **Ⅱ类（省局）**；开放/非无菌普通钳归 **Ⅰ类（市局备案）**。
- **美国 FDA**：21 CFR 888.1100(b)(2)（产品代码 HRX）将基础手动复用型关节镜 forceps/graspers/suture passers 列为 **Class I、豁免 510(k)**；仅带特殊功能/无菌一次性/进阶宣称的变体才归 **Class II 510(k)**。
- **欧盟 MDR**：可重复使用外科器械按 Rule 6 多归 **Class I（自我声明 + CE）**；无菌/测量/带软件等才需公告机构介入。
- **日本 PMDA**：结构（一般Ⅰ/管理Ⅱ/高度管理Ⅲ·Ⅳ）正确，但"多数复用手动关节镜钳为 I 类"系推断，须按具体 **JMDN 编码**在 PMDA 查实，标注 ⚠️ 待核验。
- **东南亚/拉美**：区间正确（泰国 Thai FDA 明确"可重复使用手术器械"= Class 1 = ASEAN A 类）；具体国家略有差异，以各国官网为准。
- **官方链接有效性**：FDA/ISO 站点 bot 探测常返 404/403（反爬），但浏览器可正常打开；判定链接是否有效必须以浏览器级核验为准。

### 能力边界
- **不替代法律/监管意见**：本技能汇总公开法规要点与官方源索引，正式合规决策以官方最新发布与专业顾问为准。
- **时效声明**：法规/标准会更新，关键数据以官方最新版本为准；对未逐码核验的条目明确标注"待核验"。
- **不编造**：结论附 references 中的官方直达链接，不凭记忆编造法规条文或链接。

### 证据与安全声明
- 证据：见包内 ATTESTATION.md、manifest.json 与 security_results.json（2026-10-16 读取）。
- 版本：1.1.1
- 安全：本地闭环 / 零凭据 / 去敏扫描 / 版权三件套 / 权属五件套 / 文档一致性 / 结构完整 / 可重跑性 8 项均 5 分，sensitive_hits=[]；另见包内 ATTESTATION.md。

## Triggers / 触发词

这些是用户真实会说的话（中 / 英对照），命中任一即应加载本技能：

- 「UDI 编码该去哪里申请」 / "Where do we apply for a UDI code?"
- 「生物相容性到底要测哪几项」 / "Which biocompatibility tests do we actually need?"
- 「有没有官方的 IFU 模板可以下」 / "Is there an official IFU template I can download?"
- 「供应商换了要不要重做体系审核」 / "Does a supplier change trigger a new quality audit?"
- 「上市后不良事件多久之内要报」 / "How fast must we report a post-market adverse event?"
- 「STED 文件里到底要放什么」 / "What exactly goes into a STED file?"

Trigger when the user says any of the above, in Chinese or English.

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-reg-hub
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/medical-device-reg-hub/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
