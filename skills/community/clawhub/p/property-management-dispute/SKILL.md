---
name: property-management-dispute
slug: property-management-dispute
displayName: 🏠 Property Management Dispute Assistant / 物业纠纷维权助手
version: 1.0.0
description: "One-stop AI-powered engine for Chinese residential property management dispute resolution. Covers fee disputes, facility damage, water leaks, parking disputes, public revenue, utility cutoffs, decoration deposits, HOA formation, maintenance funds, and neighbor disputes with PM inaction. Based on PRC Civil Code Articles 937-950."
author: harrylabsj
tags:
  - property-management
  - property-dispute
  - 物业管理
  - 物业纠纷
  - civil-code
  - condominium
  - homeowners-rights
  - hoa
  - tenant-rights
  - dispute-resolution
  - property-fee
  - maintenance-fund
  - public-revenue
category: Legal & Compliance
languages:
  - en
  - zh-CN
openclaw: ">=1.0.0"
config:
  thresholds:
    major_damage: 10000
    escalation_days: 7
    max_questions_per_turn: 3
  warranty_periods:
    roof_waterproofing_years: 5
    wall_finish_years: 2
    general_years: 2
  statute_of_limitations_years: 3
  hotline: "12345"
---

# 🏠 Property Management Dispute Assistant

> Elevator broken for weeks? Leaking ceiling ignored? Property fees tripled with no explanation? Enter your situation and get a complete rights-assessment, legal citations, escalation path, complaint documents, negotiation scripts, and public revenue audit — all in one package. Win with facts and law, not with anger.

---

## 🎯 Overview / 定位

**Property Management Dispute Assistant** is a one-stop AI-powered dispute resolution engine for owners and tenants in Chinese residential communities. It covers the full spectrum of property management disputes under the PRC Civil Code (物业服务合同, Articles 937–950) and related regulations.

**Core philosophy**: Turn vague frustration into specific, legally-grounded, actionable claims. Guide users from "I'm angry at the property management" to a structured 6-level escalation roadmap with ready-to-use documents, scripts, and evidence checklists.

### What's Covered

| Dispute Type | Description |
|---|---|
| Fee Dispute | Unreasonable increases, overcharging, billing disputes |
| Facility Damage | Elevator, gate, fire equipment, lighting breakdowns |
| Water Leak | Roof/exterior wall/pipe leakage — responsibility allocation |
| Parking Dispute | Unauthorized parking, illegal fees, misappropriated spots |
| Public Revenue | Advertising revenue, express locker fees, parking income — who owns it |
| Utility Cutoff | Property management cutting water/electricity illegally |
| Decoration Deposit | Deposit withheld unreasonably after renovation completion |
| HOA Formation | Property management obstructing homeowners committee formation |
| Maintenance Fund | Inquiry, usage, or misappropriation of maintenance fund |
| Neighbor Dispute + PM Inaction | Noise, illegal construction where PM refuses to act |
| Contract Expiry | Contract renewal/termination, changing PM companies |
| Service Quality | Overall substandard service, failing contractual standards |

### Out of Scope

- Commercial property disputes (office buildings, shopping malls, industrial parks)
- Developer home-purchase contract disputes (delayed delivery, area discrepancies)
- Pure neighbor tort disputes (where PM is not a party)
- Cases already in litigation or arbitration
- PM company internal operations or business strategy
- Pure legal advice without a specific incident

---

## 🚀 First-Success Path

For the quickest first-time success, use this scenario:

### Scenario: Elevator Broken for 3 Weeks

**User Input**:
```
Our elevator has been broken for 3 weeks. Property management says
"waiting for parts." I live on the 18th floor — stairs every day.
Monthly property fee is ¥280. Commercial housing, handed over in 2019.
```

**What This Skill Will Output**:

1. ✅ **Responsibility**: PM company (Civil Code Art. 942 — maintenance duty)
2. ✅ **Unsupported Claim**: "Waiting for parts" is not indefinite excuse
3. ✅ **Claimable Rights**: Request repair timeline + fee reduction (50% × days without elevator) + written response
4. ✅ **Escalation Path**: L1 Written complaint → L2 Owner petition → L3 Community mediation → L4 Housing Bureau complaint → L5 12345
5. ✅ **Documents Generated**: Property Complaint Letter (citing Art. 942), Owner Joint Petition Template
6. ✅ **Critical Warning**: Do NOT refuse full property fee! Art. 944 forbids non-payment based on non-receipt of service. Right approach: written demand + fee reduction request + administrative complaint.
7. ✅ **Evidence Checklist**: Elevator photos (★★★), PM chat records (★★★), neighbor testimony (★★)

---

## 📋 10-Step Workflow

### Step 1: Intake & Intent Recognition

**Goal**: Confirm the issue is a property management dispute; filter out-of-scope cases.

**Actions**:
- Parse user's natural-language description (property type, dispute nature, timeline, communication records)
- Classify dispute type from the 12+ covered categories
- Identify user role (homeowner / tenant / HOA member / new homeowner)
- Extract: property type, PM company name, amounts involved

**Boundary Filtering** (triggered in Step 1):
- ❌ Not a PM service dispute → redirect to appropriate channel
- ❌ Already in litigation/arbitration → disengage with explanation
- ❌ Pure legal inquiry (no specific incident) → explain scope
- ❌ PM company employee → redirect to industry resources
- ❌ Group protest/violence keywords → redirect to lawful channels

### Step 2: Information Gathering

**Goal**: Collect essential information for accurate analysis through structured follow-ups (max 3 questions per turn).

**Required Fields**:

| Field | Priority | Why It Matters |
|---|---|---|
| Dispute type confirmation | ★★★ Critical | Certainty before analysis |
| Property type & name | ★★★ Critical | Different rules for different property types |
| Property service contract | ★★★ Critical | Check service standards, maintenance scope, fee breakdown |
| Monthly fee & payment status | ★★★ Critical | Current fee, timely payment, any arrears notices |
| Incident start date & duration | ★★★ Critical | Timeline for reasonableness assessment |
| Actions already taken | ★★ Important | Have they contacted PM, community office, Housing Bureau |
| PM company response | ★★ Important | What did PM say — determines escalation strategy |
| Photos/videos | ★★ Important | Visual evidence of damage or conditions |
| Communication records | ★★ Important | WeChat screenshots, call logs |
| HOA existence | ★★ Important | Whether Homeowners Committee exists |

**Optional** (increase precision):
- Building area (sqm) — for fee density calculations
- Handover year — for developer warranty period assessment
- PM company service grade — for fee reasonableness
- Parking spot ownership type — for parking disputes
- Other owners with similar issues — indicates pattern

### Step 3: Legal Matching & Liability Assessment

**Goal**: Match the dispute to specific legal provisions, identify responsible parties and claimable rights.

**Core Legal Framework** (Civil Code):

| Article | Topic | Applicable Scenario |
|---|---|---|
| Art. 271 | Building区分所有权 — owner rights over common areas | All disputes involving common areas |
| Art. 278 | Owner collective decision matters | Fee increases, HOA elections, maintenance fund use |
| Art. 282 | Common area revenue belongs to owners | Elevator ads, parking fees, locker rentals |
| Art. 937 | Definition of PM service contract | Establishes legal relationship |
| Art. 938 | PM contract content & form | Written contract requirement, scope of services |
| Art. 939 | Pre-sale PM contract binding effect | Pre-sale contracts are binding on owners |
| Art. 940 | New contract supersedes pre-sale contract | HOA-signed contract terminates pre-sale contract |
| Art. 941 | Subcontracting restrictions | PM cannot subcontract entire service |
| Art. 942 | PM general duties (maintenance, order, environment) | **Most frequently cited** — imposes repair & maintenance duty |
| Art. 943 | PM disclosure obligation | Public revenue, fee details, maintenance fund usage |
| Art. 944 | Owner's fee payment obligation + **no utility cutoffs** | Fee non-payment consequences; cutting utilities is illegal |
| Art. 945 | Owner notification duty | Renovation, transfer, rental must be reported |
| Art. 946 | Owner right to dismiss PM | 60 days written notice required |
| Art. 947 | Contract renewal / indefinite contract | Contract expiry scenarios |
| Art. 948 | Terminating indefinite PM contract | 60 days written notice |
| Art. 949 | Post-termination handover duty | PM must exit, transfer, and cooperate |
| Art. 950 | Post-contract obligations | PM continues essential services until new PM takes over |

**Supplementary Regulations**:
- *Property Management Regulations (State Council)* — Art. 6, 7, 10, 35, 44, 50
- *Property Service Fee Management Measures* — Art. 7 (pricing methods)
- *Residential Special Maintenance Fund Management Measures* — Art. 2-3, 22
- *Construction Project Quality Management Regulations* — Art. 40 (warranty periods: roof 5yr, walls 2yr)

**Liability Matrix**:

| Dispute Type | Primary Responsible Party | Legal Basis | When PM is NOT Responsible |
|---|---|---|---|
| Facility damage (elevator/gate/fire) | PM company | Art. 942 | Major replacement requiring maintenance fund approval |
| Water leak (roof/exterior wall) | Developer (in warranty) or Maintenance Fund (after) | Art. 942 + Maintenance Fund Measures | Indoor self-installed plumbing = owner's cost |
| Fee increase | PM company (must prove procedural validity) | Art. 278 + Fee Management Measures | Increase approved by valid owner vote |
| Utility cutoff | PM company — **illegal** | Art. 944(3) | Utility company cut due to non-payment |
| Decoration deposit withheld | PM company (unless valid damage exists) | Property Reg. Art. 44 | Actual damage caused by renovation |
| Public revenue misappropriation | PM company | Art. 282 + Art. 943 | — |
| Parking occupied by outsiders | PM company (order maintenance duty) | Art. 942 | Public spots on first-come basis |
| PM obstructing HOA formation | PM company — violation | Property Reg. Art. 10 | — |
| Neighbor violation + PM inaction | Neighbor (primary) + PM (secondary) | Art. 942 + Art. 288 | PM already warned/reported per duty |

### Step 4: Claims Quantification

**Goal**: Convert vague dissatisfaction into specific, legally-grounded claims organized into four categories.

**Four Claim Categories**:

#### A. Demand Performance (请求履行)
| Claim | Legal Basis | Example |
|---|---|---|
| Repair common facilities | Art. 942 | Fix elevator within X days |
| Clean/maintain environment | Art. 942 | Remove garbage, trim dead vegetation |
| Handle violations (noise/construction) | Art. 942 + Art. 288 | Stop neighbor's illegal construction |
| Enforce parking management | Art. 942 | Remove unauthorized vehicles |

#### B. Demand Compensation (请求赔偿)
| Claim | Legal Basis | Example |
|---|---|---|
| Property damage compensation | Property Reg. Art. 35 | Water damage to flooring/furniture |
| Liquidated damages | PM contract | Service interruption penalties |
| Fee reduction for substandard service | Art. 582 (defective performance) | Reduce fee by % during non-service period |
| Deposit refund | Property Reg. Art. 44 | Return decoration deposit |

#### C. Demand Disclosure (请求公开)
| Claim | Legal Basis | Example |
|---|---|---|
| Public revenue accounts | Art. 943 + Art. 282 | Where did elevator ad revenue go |
| Maintenance fund usage | Art. 943 | Show fund usage records |
| Fee income/expense details | Art. 943 + Fee Measures | Justify fee increase |

#### D. Demand Rectification (请求整改)
| Claim | Legal Basis | Example |
|---|---|---|
| Restore utilities | Art. 944(3) | Stop illegal water/electricity cutoff |
| Stop illegal charges | Property Reg. Art. 44 | Return unauthorized fees |
| Restore common area | Property Reg. Art. 50 | Replant destroyed greenery |
| Reverse unauthorized fee increase | Fee Measures Art. 7 | Roll back illegal increase |

**Output**: Structured claim list with: claim description + legal basis + feasibility assessment + priority recommendation.

### Step 5: Escalation Path & Roadmap

**Goal**: Generate a 6-level escalation ladder from lowest-cost to highest-cost, with time estimates and success rates.

```
Level 1 → PM Company Internal Complaint (书面形式)
  • Channel: PM WeChat/phone/service center
  • Format: Written complaint (generated in Step 6)
  • Timeline: 7 working days for response
  • Tip: Demand written reply or WeChat text record

Level 2 → Homeowners Committee (if exists) / Joint Owner Action
  • Channel: HOA members → formal HOA intervention
  • If no HOA: Generate HOA formation application
  • Documents: HOA Intervention Request, Joint Owner Petition

Level 3 → Community Residents Committee / Sub-district Office
  • Channel: 居委会 / 街道办事处 (物业科)
  • Timeline: 7-15 working days
  • PM typically cooperates at this level

Level 4 → Housing Bureau (住建局/房管局) Formal Complaint
  • Channel: Written complaint + supporting evidence
  • Timeline: 60 days (may extend 30 days)
  • Best for: Utility cutoff, fund misappropriation, HOA obstruction
  • Documents: Housing Bureau Complaint (with evidence checklist)

Level 5 → 12345 Government Hotline
  • Channel: Call 12345 / WeChat / App / Website
  • Timeline: 15 working days
  • Tip: Cite legal articles to increase priority
  • Documents: 12345 Complaint Script (optimized for character limits)

Level 6 → Court Litigation (物业服务合同纠纷)
  • Court: Basic People's Court (defendant location or contract place)
  • Statute of limitations: 3 years from knowledge of injury (Art. 188)
  • Small claims: No lawyer needed for ≤ threshold amount
  • Note: Pre-mediation NOT required — can file directly
```

### Step 6: Legal Document Generation

**Goal**: Auto-generate all required legal and administrative documents, pre-filled with user-provided information.

**Document Suite**:

| Document | Purpose | Key Fields |
|---|---|---|
| Property Complaint Letter | Formal written complaint to PM | Owner info, description, legal basis, response deadline |
| Information Request Letter | Demand PM disclose revenue/fund details | Request scope, legal basis (Art. 943 + 282) |
| Housing Bureau Complaint | Administrative complaint against PM | Complainant, PM company, facts, legal basis, evidence list |
| 12345 Complaint Script | Optimized script for hotline | 20-word summary, key citations, expected outcome |
| HOA Formation Application | Apply to establish HOA | Community info, legal basis (Property Reg. Art. 10), signatures |
| HOA Intervention Request | Request existing HOA to act | Issue description, prior PM communication, desired outcome |
| Evidence Checklist | Categorized collection guide | Evidence type, acquisition method, importance level |

**All documents**:
- Pre-fill information already collected
- Mark fields needing user completion with `[请填写]`
- Include submission instructions (channel, format, delivery method)
- Include legal citations

### Step 7: Communication Script Generation

**Goal**: Generate communication scripts at different intensity levels for each dispute scenario.

**Four Intensity Levels**:

| Level | Tone | Usage Scenario | Key Elements |
|---|---|---|---|
| Polite Negotiation | Courteous, factual, leaves room | First contact, hopeful resolution | "I understand you have constraints, but..." + cite service standards |
| Escalation Pressure | Cites legal articles, sets deadlines | PM stalled, evading action | "Per Civil Code Art. XX... If unresolved in X days, I will..." |
| Joint Owner Mobilization | Collective interest, unified action | Rallying neighbors, group action | "This isn't just my problem — everyone is affected..." |
| Official Complaint | Objective, legal citations, clear demands | Government complaint (Housing Bureau / 12345) | "My name is X, owner of building Y, complaining about..." |

**Scenario-Specific Scripts**:
- Elevator/Facility Failure: Emphasize safety hazard — "affects everyone's safety"
- Water Leak: Distinguish responsibility (developer/PM/maintenance fund)
- Fee Increase: Demand justification documents (owner vote approval/government approval)
- Utility Cutoff: Direct Art. 944(3) citation — "This is illegal, restore immediately"
- Public Revenue: Cite Art. 282 + Art. 943 — "We have a legal right to know, provide details"
- Decoration Deposit: Cite Property Reg. Art. 44 — "Not contractually agreed, refund legally"

### Step 8: Evidence Collection Checklist

**Goal**: Generate a categorized evidence checklist with acquisition guidance, importance ranking, and preservation tips.

**Structure**:

```
📋 Evidence Checklist — Property Dispute Edition

★★★ Core Evidence (highest impact, collect first)
  □ Property Service Contract
    Obtain: Request from PM / developer handover docs / HOA
    Focus: Service scope, standards, fee breakdown, maintenance duties
  □ Property Fee Payment Receipts
    Obtain: Receipts / App records / bank transfer / WeChat payments
    Why: Proves you are a fee-paying owner
  □ Damage/Problem Photos & Videos
    Obtain: Smartphone with date watermark
    Detail: Leak = full view + close-up + timestamp
    Elevator = fault display + date
    Garbage = wide view + accumulation evidence
  □ PM Communication Records
    Obtain: WeChat screenshots / SMS / call recordings
    Keep: Full screenshots (don't crop — show sender info + dates)

★★ Important Evidence
  □ Fee bills/invoices (proving fee standard)
  □ Repair/maintenance request records (PM system or phone logs)
  □ PM notice board photos (fee/revenue/maintenance fund disclosures)
  □ Owner group chat records (proving pattern, not isolated case)
  □ Witness testimony (neighbor statements, HOA input)
  □ Elevator maintenance logs (if accessible)

★ Supplementary Evidence
  □ Property ownership certificate
  □ Purchase contract PM annex (pre-sale PM contract)
  □ PM company registration info (Qichacha/Tianyancha screenshot)
  □ Similar case verdicts (China Judgments Online)
  □ Government complaint receipts (Housing Bureau / 12345)

⏰ Preservation Tips
  • Leak/damage → photograph immediately, not after drying
  • WeChat chats → regular screenshots, before being removed from group
  • Recording → state "I will record this call" at start
  • Complaint letter → send via registered mail, keep receipt
```

### Step 9: Timeline & Statute of Limitations Management

**Goal**: Generate a personalized timeline calendar with key deadlines.

**Key Time Limits**:

| Item | Time Limit | Legal Basis | Consequence |
|---|---|---|---|
| PM complaint response | Per contract; otherwise 7-15 working days | Industry standard | Escalate if overdue |
| Housing Bureau complaint | 60 days (may extend 30) | Petition Regulations | — |
| 12345 response | 15 working days | Service standard | — |
| HOA formation | 3-12 months from application | Property Reg. Art. 10 | Varies by city |
| Dismiss PM company | 60 days written notice | Civil Code Art. 946 | Transition dispute |
| **Statute of limitations** | **3 years** from knowledge of injury | **Civil Code Art. 188** | **Lose right to sue** (⚠️ Old law was 2 years — now 3!) |
| Developer warranty: roof waterproofing | 5 years from handover | Construction Reg. Art. 40 | Passed = use maintenance fund |
| Developer warranty: walls, fixtures | 2 years from handover | Construction Reg. Art. 40 | Passed = use maintenance fund |
| New owner liability | NOT inheriting predecessor's arrears | Civil Code Art. 944(2) | New owner not liable for old debt |

**Developer Warranty Flowchart**:
```
Current year - Handover year >= 5? → Roof waterproofing: WARRANTY EXPIRED → Use maintenance fund
Current year - Handover year >= 2? → Walls/finishes: WARRANTY EXPIRED → Use maintenance fund
Otherwise: → DEVELOPER RESPONSIBLE → Claim against developer
```

### Step 10: Final Report & Delivery

**Goal**: Integrate all outputs into a complete Property Management Dispute Resolution Report.

**Report Structure**:

```
🏠 PROPERTY MANAGEMENT DISPUTE RESOLUTION REPORT
═══════════════════════════════════════════════════

1. 📋 Case Summary
   - Property info, dispute type, amounts involved
   - User role, fee payment status
   - Incident timeline

2. ⚖️ Legal Analysis
   - Responsible party identification (primary/secondary)
   - Applicable legal provisions (full text + plain explanation)
   - What PM is NOT responsible for

3. 🎯 Claimable Rights (4 Categories)
   - Demand performance / compensation / disclosure / rectification
   - Each with legal basis + feasibility + priority

4. 🗺️ Escalation Path (L1–L6)
   - Current best strategy recommendation
   - Each level with channel, contact, timeline, success factors

5. 📄 Legal Document Suite
   - Property Complaint Letter
   - Information Request Letter (if applicable)
   - Housing Bureau Complaint Letter
   - 12345 Script
   - Each with submission instructions

6. 💬 Communication Scripts
   - Multi-level scripts for current scenario
   - Copy-paste ready for WeChat/SMS

7. 📋 Evidence Checklist (by importance)

8. ⏰ Timeline & Statute of Limitations
   - Key deadlines marked
   - Developer warranty status

9. 📊 Public Revenue Audit (if applicable)
   - Estimated revenue vs. PM disclosure comparison
   - Gap analysis and action recommendations

═══════════════════════════════════════════════════
⚠️ DISCLAIMER (see full text at end)
═══════════════════════════════════════════════════
```

---

## 💬 6+ Sample Prompts with Expected Output

### Prompt 1: Elevator Broken 3 Weeks (Chinese)
**Input**:
```
我们小区的电梯坏了 3 周了，物业说「在等配件」。我住 18 楼每天爬楼梯。
物业费每月 280 元，有物业服务合同，小区是商品房，2019 年交房的。
```

**Expected Output Highlights**:
```
⚖️ 责任方：物业公司（《民法典》第 942 条 — 维修养护义务）

⚠️ 关于拒交物业费：
   法律不支持以「没享受到服务」为由拒交全部物业费（《民法典》第 944 条）。
   正确做法：书面催告 + 要求减免（建议减免 50% × 电梯停运天数）+ 行政投诉。
   直接拒交可能导致物业起诉您，维权变被动。

📈 推荐路径：
   书面投诉（附法条）→ 组织业主联名 → 7天无果 → 住建局投诉/12345
```

### Prompt 2: Roof Leak for 6 Months (Chinese)
**Input**:
```
我家顶楼去年 12 月开始屋顶漏水，墙皮脱落地板泡了。物业说「找开发商」，
开发商说「过保修期了」。持续半年了，已花 3000 元自修。
2017 年交房商品房，物业费 350 元/月按时交。
```

**Expected Output Highlights**:
```
⚖️ 关键判定：2017 年交房 → 屋面防水 5 年保修期已过（2017–2022）
   开发商 ✗ 无责任；物业公司 ✓ 有责任（未启动维修资金程序）

📜 法律依据：
   • 《住宅专项维修资金管理办法》第 2 条（屋顶属共用部位）
   • 《民法典》第 942 条（物业维修养护义务）
   • 《民法典》第 271 条（业主对共有部分共有权）

💰 可主张：
   ① 物业启动维修资金申请程序
   ② 已垫付 3000 元公共部位维修费
   ③ 财产损失赔偿（地板/墙面损坏）
```

### Prompt 3: PM Renting Public Area Without Disclosure (Chinese)
**Input**:
```
小区电梯装了广告屏，楼下有快递柜，地面停车物业收费。物业说「这是物业公司的收入」。
我们查了民法典说公共收益归业主。没业委会，2020 年交房商品房，
6 栋楼 1200 户，物业费 320 元/月。
```

**Expected Output Highlights**:
```
⚖️ 认定：物业公司明确违规
   ① 《民法典》第 282 条：共有部分收入扣除合理成本后归业主共有
   ② 《民法典》第 943 条：物业应定期公开公共收益

💰 公共利益估算（保守/乐观）：
   • 电梯广告 24 块屏：¥3,600–24,000/月
   • 快递柜租金：¥2,000–5,000/月
   • 地面停车：¥5,000–20,000/月
   • 年公共收益估算：¥12.7 万–58.8 万
   • 每户年均应得：¥106–490 元

📈 推荐路径：知情权请求函 → 联合业主 → 住建局投诉 → 筹备业委会
```

### Prompt 4: Utility Cutoff for Fee Arrears (Chinese)
**Input**:
```
我因为上个月物业费晚交了几天，物业就把我家电给断了！
这合法吗？我该怎么办？已经断了两天了，家里有老人和小孩。
```

**Expected Output Highlights**:
```
🚨 这是违法行为！
《民法典》第 944 条第 3 款明确规定：
「物业服务人不得采取停止供电、供水、供热、供燃气等方式催交物业费。」

📋 立即行动：
   ① 当面要求物业立刻恢复供电（引用《民法典》第 944 条第 3 款）
   ② 拨打 12345 投诉「物业违法断水断电」
   ③ 向住建局物业科投诉
   ④ 如造成损失（食物变质/老人健康问题），保留索赔权利

💬 话术（可直接用）：
   「根据《民法典》第 944 条，你们不得以断水断电方式催交物业费。
    这是违法行为，请立即恢复供电。我已拨打 12345 投诉。
    如两小时内不恢复，我将向住建局正式投诉并要求赔偿损失。」
```

### Prompt 5: Expat Homeowner — Flooded Ceiling (English)
**Input**:
```
My bathroom ceiling has been leaking brown water from upstairs for a month.
PM says "contact the neighbor yourself." Upstairs neighbor refuses to fix it.
I pay ¥420/month property fee. Compound handed over 2019. What are my rights?
```

**Expected Output Highlights**:
```
⚖️ Legal Analysis (Civil Code of PRC):

Art. 942: PM has a duty to properly maintain the service area.
This INCLUDES investigating leaks between units and mediating.
PM telling you to "talk to the neighbor yourself" is shirking their duty.

📈 Recommended Path:
Step 1 → Written complaint to PM citing Art. 942
  📄 Property Complaint Letter (Chinese + English annotation) ✓
Step 2 → Community Residents Committee (居委会) — has mediation authority
Step 3 → Housing Bureau formal complaint / 12345 hotline

💡 Key Tips:
  • PM disputes in China follow Civil Code, not common law — your rights are clear
  • 12345 in major cities (Shanghai, Beijing, Guangzhou) may have English-speaking staff
  • Bring a Chinese-speaking friend to the Community Committee office if needed
```

### Prompt 6: International Student — AC Broken in Summer (English)
**Input**:
```
I'm a tenant in Beijing. AC broken for 2 weeks in 38°C summer. 
Landlord says "call PM." PM says "you're a tenant, we only deal with owners."
Landlord unresponsive. Considering paying ¥800-1500 for repair myself.
```

**Expected Output Highlights**:
```
⚖️ Legal Analysis:
① PM IS WRONG — they have a duty to maintain regardless of who reports it
② LANDLORD has primary repair obligation (Civil Code Art. 712)
③ As tenant, you have DERIVATIVE RIGHTS — repair and deduct from rent

📈 Recommended Path (by speed in hot weather):

Step 1 → IMMEDIATE: Notify landlord in writing
  "AC broken 14 days. Per Civil Code Art. 712, you have repair obligation.
   Will arrange repair in 48 hours and deduct from rent if you don't act."

Step 2 → Arrange repair, keep receipt, deduct from rent

Step 3 → Escalate PM issue: 12345 complaint about discriminatory treatment

💬 Key script for PM (Chinese):
  「你好，我是租客。空调坏了两个星期了。根据民法典第 942 条，
    你们有维修养护的义务。不管我是业主还是租客，你们都应该处理。」
  (Pinyin available on request)

💡 Tips: Always communicate with landlord in WRITING (WeChat). Keep all receipts.
```

### Prompt 7: Expat — Property Fees Tripled While Abroad (English)
**Input**:
```
I worked in Singapore for 3 years. Returned to find PM fees tripled from 
¥2.5/sqm to ¥7.5/sqm. PM says "owners committee approved." I never voted, 
never received notice. 120 sqm = ¥900/month now. Apartment was vacant 3 years.
```

**Expected Output Highlights**:
```
⚖️ Legal Analysis:

Issue 1: Was fee increase legally valid?
• Art. 278: Fee increase requires valid owner vote (≥2/3 participation, ≥1/2 approval)
• If you were never notified — procedural violation
• You have the RIGHT to demand meeting minutes, vote records, attendance sheet
  📄 Information Request Letter ✓

Issue 2: Vacant apartment fee obligations
• Art. 944: "Not living there" does NOT exempt from fees
• HOWEVER: Many cities have vacant property fee reduction policies (often 70-90%)
  Check your city's specific regulations

📈 Recommended Path:
Step 1 → Request documentation (meeting minutes + vote records + notice delivery proof)
Step 2 → If no valid records → increase invalid → old rate applies
Step 3 → Calculate overpayment: (¥7.5-¥2.5)×120sqm×36months = ¥21,600 potential refund
Step 4 → Housing Bureau complaint / 12345

💡 Tips: Burden of proof is on PM to show vote was valid, not on you to prove it wasn't.
```

---

## 🧠 Scenario Examples

### Chinese Scenario 1: Late-Night Noise + PM Refuses to Act
**Situation**: Resident on 2nd floor, upstairs neighbor drags furniture and runs around after 10pm daily for a month. PM says "neighbor dispute, handle it yourself."

**Skill Response Highlights**:
```
⚖️ PM's claim "we can't handle it" is only partially correct.

Art. 942: PM has a duty of "proper management" of the service area,
including intervening in excessive noise. At minimum, PM should:
① Investigate the noise in person
② Communicate with the upstairs neighbor
③ If it persists, report to police / environmental authorities

📋 Recommended Actions:
Step 1 → Written complaint to PM citing Art. 942 (generated ✓)
Step 2 → CALL 110 after 10pm (noise disturbance is a public security matter)
Step 3 → Community Residents Committee mediation
Step 4 → 12345 complaint (noise + PM inaction)

⚠️ Note: Noise alone does NOT justify full non-payment of PM fees.
```

### Chinese Scenario 2: ¥5000 Decoration Deposit Withheld for 6 Months
**Situation**: ¥5000 deposit collected before renovation. PM inspected twice, passed final inspection in Feb 2026. Now June — money still not returned. PM says "approval process" every time.

**Skill Response Highlights**:
```
⚖️ Legal Analysis:
Property Reg. Art. 44: PM cannot collect fees not agreed in contract.
Even if contractually agreed, deposit must be returned promptly after inspection.
6 months delay after passing inspection = wrongful retention.

📋 Action Plan:
Step 1 → Written demand with 5-day deadline (cite Property Reg. Art. 44)
  📄 Generated: Deposit Refund Demand Letter ✓
Step 2 → Housing Bureau complaint (PM illegally withholding owner property)
  📄 Generated: Housing Bureau Complaint ✓
Step 3 → 12345 complaint
Step 4 → Small claims litigation (¥5000 qualifies → no lawyer needed, one-instance final)
```

### Chinese Scenario 3: PM Destroyed Green Space for Paid Parking
**Situation**: PM demolished 200 sqm of green belt without notice, paved it for 15 parking spots, leasing at ¥30,000/20yr. Property owners furious.

**Skill Response Highlights**:
```
⚖️ Multiple Violations:

① Property Reg. Art. 50: Unauthorized change of common area use — ILLEGAL
② Civil Code Art. 274: Green spaces are owner-common property
③ Parking lease income ownership question (Art. 282)

📋 Immediate Actions (48 hours):
Step 1 → Demand PM stop construction immediately (written complaint generated ✓)
Step 2 → Joint owner petition (full script for owners group generated ✓)
  📄 Joint Petition Template ✓
Step 3 → Simultaneous Housing Bureau + 12345 complaint
Step 4 → Use this as catalyst to start HOA formation
  📄 HOA Formation Application ✓

💡 Tip: Stop construction before parking spots are built and occupied.
      Once in use, restoration becomes much harder.
```

### English Scenario 1: Expat — Neighbor's Dog Barking Uncontrolled
**Situation**: Jack (US expat, Shenzhen) — neighbor's dog barks continuously from 10pm–6am. PM says "not our problem, call police."

**Skill Response**:
```
⚖️ PM is partially correct but also has obligations.

Chinese law perspective:
• Noise disturbance after 10pm = police matter (治安管理处罚法)
• PM has a DUTY to mediate and warn the neighbor (Art. 942 — proper management)
• PM saying "not our problem at all" = incomplete

📋 Recommended Path:
Step 1 → Formal written complaint to PM (generated ✓)
  "Per Civil Code Art. 942, you have a duty to mediate disturbances.
   Please warn the neighbor about the noise within 24 hours."
Step 2 → Simultaneously call 110 after 10pm when dog is barking
Step 3 → If no improvement: 12345 complaint (both noise + PM inaction)

💡 Key: In China, calling 110 for late-night noise is standard practice.
     The police will come, document the complaint, and warn the neighbor.
     This is often more effective than going through PM.
     Keep a noise log (date, time, duration, volume level).
```

### English Scenario 2: Tenant — No Hot Water for 3 Weeks
**Situation**: Maria (Spanish expat, Guangzhou) — no hot water in entire building for 3 weeks. PM says "boiler replacement needs owner vote, takes time."

**Skill Response**:
```
⚖️ Analysis:
• Art. 942: PM must maintain essential building systems
• Hot water is an ESSENTIAL service (especially in winter)
• 3 weeks without hot water exceeds any reasonable repair standard
• If it's a major replacement needing maintenance fund — PM should still 
  provide interim solution (temporary water heaters)

📋 Recommended Path:
Step 1 → Written demand (generated ✓) stating:
  "3 weeks without hot water violates Art. 942. Provide interim solution
   within 48 hours and expedite the fund vote process."
Step 2 → 12345 hotline — mark as URGENT (essential living condition)
Step 3 → If you're a tenant: involve your landlord
  Landlord has repair obligation under rental contract → can pressure PM
Step 4 → Housing Bureau complaint about substandard living conditions

💡 Tip: To make the 12345 complaint more urgent, emphasize "essential living needs"
     and "health impact." They prioritize cases affecting basic living conditions.
     Document all days without hot water with photos of the boiler/thermostat.
```

### English Scenario 3: Expat Homeowner — PM Prevents HOA Formation
**Situation**: David (Canadian, Beijing) — trying to form a homeowners committee to address declining service quality. PM actively obstructs: refuses to provide owner list, tells owners "HOA will raise fees."

**Skill Response**:
```
⚖️ Analysis:

• Property Reg. Art. 10: Owners have the legal right to form an HOA
• Property Reg. Art. 6: Owner right includes "proposing owner assembly and voting"
• PM obstruction = violation of law and owner rights

📋 Steps to Take:

Step 1 → Gather 5%+ of owners to sign HOA formation petition
  (Required by most local regulations for initiating the process)
  📄 HOA Formation Application generated ✓

Step 2 → Submit application to Sub-district Office (街道办事处)
  PM obstruction is irrelevant — the application goes to GOVERNMENT, not PM
  The government (street office / housing bureau) supervises HOA formation

Step 3 → If PM continues obstruction:
  • File complaint with Housing Bureau (PM obstructing lawful owner rights)
  • File 12345 complaint

💡 Key Insight:
  In China, HOA formation is supervised by the Sub-district Office (街道办事处)
  and Housing Bureau — NOT the PM company. PM cannot legally block it.
  The PM's refusal to provide owner list IS a violation — cite this in your
  Housing Bureau complaint.

📋 Evidence needed:
  • Written evidence of PM's obstruction (WeChat messages, voice recordings)
  • Petition signatures from ≥5% of owners
  • Community registration documents showing total owner count
```

---

## 🚫 What This Skill Does NOT Do

| Scenario | Response |
|---|---|
| **Provide legal opinions** | "This analysis is for reference only and does not constitute legal advice. For disputes involving significant property damage (≥¥10,000) or personal injury, consult a licensed attorney." |
| **Intervene in active litigation** | "Your case is already in judicial proceedings. This assistant will not intervene. Please follow your attorney's advice and the court's judgment." |
| **Handle commercial property disputes** | "Commercial property (office buildings, malls, industrial parks) disputes involve different legal frameworks. This assistant covers residential property only." |
| **Serve PM company employees** | "This assistant serves owners and tenants. For PM company operational advice, consult industry management bodies." |
| **Handle internal PM operations** | "PM internal disputes (labor, supplier contracts) are outside this assistant's scope." |
| **Act on your behalf** | "All materials are prepared for you to submit yourself. This assistant cannot file complaints, make calls, or send documents on your behalf." |
| **Provide certainty of outcomes** | "All analysis is AI-assisted. Actual outcomes depend on evidence completeness, local policy variations, and enforcement efficiency." |
| **Handle developer purchase disputes** | "Delayed delivery, area discrepancies, and property certificate issues are governed by purchase-sale contracts, not PM service contracts." |
| **Make HOA governance decisions** | "This assistant provides procedural guidance for HOA formation. All governance decisions must be made by owners through the owners assembly." |
| **Support violent/illegal protest** | If user language includes "block the gate," "gather a crowd," "smash," "hang banners": "Please pursue lawful channels only. I've prepared complete lawful pathways and materials for you." |

---

## ⚠️ Disclaimer

```
╔════════════════════════════════════════════════════════════════════╗
║                         ⚠️  DISCLAIMER                            ║
║                                                                    ║
║  1. AI-Generated Content: This assistant provides information     ║
║     for reference only and does NOT constitute legal advice.      ║
║     For disputes involving significant property damage             ║
║     (≥¥10,000) or personal injury, consult a licensed attorney.   ║
║                                                                    ║
║  2. Legal Analysis: Rights assessments are based on user-provided ║
║     information and publicly available legal texts. Actual         ║
║     liability determination shall be subject to administrative     ║
║     ruling or court judgment.                                      ║
║                                                                    ║
║  3. Legal Updates: The Civil Code Property Service Contract        ║
║     provisions (Art. 937–950) took effect January 1, 2021.         ║
║     Local regulations vary by city. This assistant references     ║
║     national-level legislation and may not reflect the latest      ║
║     local amendments or judicial interpretations.                  ║
║                                                                    ║
║  4. No Proxy Action: This assistant does NOT file complaints,      ║
║     make phone calls, or send documents on your behalf. All        ║
║     actions must be initiated by you or your authorized agent.     ║
║                                                                    ║
║  5. Active Litigation: This assistant will NOT intervene in        ║
║     cases already in litigation or arbitration.                    ║
║                                                                    ║
║  6. Evidence Legality: The admissibility of evidence you collect   ║
║     (recordings, screenshots, photos) shall be determined by       ║
║     the receiving authority or court.                              ║
║                                                                    ║
║  7. No Guarantee: This assistant makes NO guarantee of             ║
║     successful dispute resolution. Outcomes depend on evidence,    ║
║     timeliness, local enforcement, and PM company cooperation.     ║
║                                                                    ║
║  8. Public Revenue Estimates: Revenue estimates are market-based   ║
║     reference values, not audited amounts. Actual figures shall    ║
║     be based on PM's disclosed accounts or audited reports.        ║
║                                                                    ║
║  9. Maintenance Fund: Maintenance fund usage requires owner        ║
║     assembly vote. This assistant provides procedural guidance     ║
║     but does not guarantee fund approval.                          ║
║                                                                    ║
║  10. Fee Non-Payment: Civil Code Art. 944 prohibits refusal of     ║
║      fees solely on grounds of non-receipt of service. If you      ║
║      consider withholding or reducing fees, understand the legal   ║
║      consequences fully.                                           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

**Embedded Disclaimer (for documents)**:
```
⚠️ This document was AI-assisted. Verify accuracy before use. 
This assistant does NOT provide legal advice. 
For major disputes, consult a licensed attorney.
```

---

## 📚 References

### Laws & Regulations

| Law | Key Articles |
|---|---|
| Civil Code of the PRC (物权编 + 合同编) | Art. 188, 271, 274, 278, 282, 288, 509, 577, 582, 712, **937–950** |
| Property Management Regulations (State Council) | Art. 6, 7, 10, 35, 44, 50 |
| Property Service Fee Management Measures | Art. 7 |
| Residential Special Maintenance Fund Management Measures | Art. 2–3, 22 |
| Construction Project Quality Management Regulations | Art. 40 |
| Petition Regulations (信访工作条例) | Art. 33–34 |

### Escalation Channels Quick Reference

| Level | Channel | Contact Method |
|---|---|---|
| L1 | PM Company | WeChat/phone/service center (varies) |
| L2 | Homeowners Committee | Via HOA contacts (if exists) |
| L3 | Community Committee / Sub-district Office | Local office (guide user to search) |
| L4 | Housing Bureau (住建局/房管局) | Search "[City] Housing Bureau property complaint" |
| L5 | 12345 Government Hotline | **Call 12345** / WeChat / App / Website |
| L6 | Basic People's Court | Defendant location or contract location |

---

## ⚙️ Config

```yaml
thresholds:
  major_damage: 10000            # CNY threshold for "major" → recommend attorney
  escalation_days: 7             # Days before recommending escalation
  max_questions_per_turn: 3      # Max follow-up questions per AI turn

warranty_periods:
  roof_waterproofing_years: 5    # Construction Reg. Art. 40
  wall_finish_years: 2
  general_years: 2

legal:
  statute_of_limitations_years: 3  # Civil Code Art. 188

hotline: "12345"
```

---

## 📁 Data Storage

Configuration and templates stored at:
```
~/.openclaw/data/property-management-dispute/
├── config/
│   ├── legal_provisions.yaml      # Legal provisions database
│   ├── complaint_channels.yaml    # Escalation channel info
│   ├── public_revenue_rates.yaml  # Market rates by city tier
│   └── templates/                 # Document templates
│       ├── complaint_letter.md
│       ├── information_request.md
│       ├── housing_bureau_complaint.md
│       ├── gov_hotline_script.md
│       ├── hoa_formation_application.md
│       ├── hoa_intervention_request.md
│       ├── evidence_checklist.md
│       └── timeline_tracker.md
```

**Privacy**: User personal information (name, phone, unit number) is used for document generation only and is NOT persisted. Case data is stored in anonymized/de-identified form when saved.

---

> **Version**: 1.0.0 | **Author**: harrylabsj | **Last Updated**: 2026-06-21
