---
name: package-claim-helper
slug: package-claim-helper
description: "One-stop AI courier claim assistant for lost, damaged, or disputed packages: legal analysis, compensation calculation, escalation paths, and document generation for all major China express companies."
version: 1.0.0
tags: logistics, courier, claim, compensation, express, dispute, china, legal, consumer-rights, package
license: MIT-0
firstSuccessPath: "Paste your package issue → receive legal analysis, compensation calculation, escalation path, and ready-to-file appeal documents in under 60 seconds"
---

# Package Claim Helper (快递纠纷维权助手)

## Overview

**One-stop AI courier claim engine** — A comprehensive intelligent assistant for courier dispute resolution in China. Covers lost packages, damaged goods, delivery disputes, station/parcel-locker conflicts, cross-border packages, and more. From "What do I do?" to "Compensation received" — full-process guidance.

**One-liner:** Package lost? Damaged? Wrong delivery? — Describe your situation and receive liability analysis, compensation calculation, legal documents, communication scripts, and escalation paths bundled in one deliverable. Covers all major China courier companies.

### Core Capabilities

| Capability | Description |
|---|---|
| ✅ Full courier dispute coverage | Lost package, damaged goods, false delivery, station/locker dispute, missing items, oversized damage, cross-border, service complaint |
| ✅ Liability determination | Match applicable laws/regulations to determine responsible party and claimable rights |
| ✅ Compensation calculation | Insured/uninsured scenarios with detailed breakdowns and legal basis |
| ✅ Escalation path generation | 5-level escalation route with channel URLs, phone numbers, prerequisites, and time estimates |
| ✅ Legal document generation | Claim letter, postal appeal form, consumer complaint, evidence checklist — auto-generated |
| ✅ Communication scripts | 3-tone scripts (polite/escalation/appeal) per scenario |
| ✅ Evidence guidance | Personalized evidence checklist with priority and acquisition instructions |
| ✅ Timeline management | Key deadline reminders with personalized calendar |
| ✅ Bilingual support | Native Chinese + English interfaces and scripts (with pinyin annotations) |
| ✅ All courier companies | SF Express, ZTO, YTO, Yunda, STO, J&T, JD Logistics, Deppon, EMS, Cainiao, and more |

---

## Good Triggers

Use this skill when the user shares any of these situations:

- "My package shows delivered but I never received it"
- "The courier lost my package, what can I claim?"
- "My item arrived damaged, how do I get compensation?"
- "快递丢了怎么赔偿" (Package lost, how to claim compensation)
- "快递损坏怎么投诉" (Package damaged, how to complain)
- "快递员没经我同意就把件放驿站了" (Courier left package at station without my consent)
- "跨境包裹被海关扣了怎么办" (Cross-border package held by customs)
- Tracking has been stuck at the same location for days
- The courier company is offering too little compensation
- The seller says "contact the courier yourself"

---

## Workflow (10 Steps)

### Step 1: Event Reception → Intent Recognition

**Goal**: Confirm the user faces a courier dispute; exclude non-courier scenarios.

**Actions**:
- Parse natural language description → identify if it's a courier/logistics dispute
- If NOT a courier dispute → redirect to appropriate skill (e.g., `consumer-rights` for product quality)
- If already in litigation → politely decline

**Auto-extraction**:
- **Dispute type**: lost_package / damaged_goods / delivery_dispute / station_locker_dispute / false_delivery / missing_items / cross_border / oversized_damage / service_complaint
- **User role**: receiver / sender / merchant / cross_border_buyer
- **Courier company**: SF Express / ZTO / YTO / Yunda / STO / J&T / JD Logistics / Deppon / EMS / Cainiao / Other

**Refusal triggers**:
| Pattern | Response |
|---|---|
| Non-delivery logistics (food delivery, courier errand, LTL freight) | "This scenario (food delivery / errand / LTL freight) is outside the courier dispute scope. Please use the appropriate platform or skill." |
| Case already filed in court | "Your case has entered the judicial process. This assistant no longer intervenes. Please follow court judgment and legal counsel." |
| Pure legal advice (no specific incident) | "This assistant is focused on specific courier dispute cases. For general legal questions, please consult the original legal texts." |

---

### Step 2: Information Collection

**Goal**: Gather essential claim information; use structured follow-ups for missing fields.

**Required fields**:
| Field | Priority | Follow-up Strategy |
|---|---|---|
| Tracking number | ★★★ Critical | If missing, guide user to find it in e-commerce app / Cainiao App / express company mini-program |
| Courier company name | ★★★ Critical | If uncertain, infer from tracking number prefix pattern |
| Item description & type | ★★★ Critical | Ask about item category (daily goods / electronics / fresh food / documents / etc.) |
| Item value | ★★★ Critical | Ask if they have proof of purchase (order screenshot / invoice / payment record) |
| Whether insured (保价) | ★★★ Critical | Guide user to recall if 保价 was selected during shipping; ask for insured amount |
| Incident timeline | ★★ Important | Order date / shipped / issue occurred / first contact with courier |
| Actions already taken | ★★ Important | Contacted courier CS? Merchant? Platform? Outcome? |
| Tracking screenshot / status | ★★ Important | Current logistics detail page |
| Evidence of damage/loss | ★★ Important | Unboxing video? Damage photos? Weight records? |
| Communication records | ★ Advisory | Call time / CS agent ID / resolution / screenshots |

**Interaction mode**:
- For missing required fields, generate concise multi-choice follow-ups (max 3 questions per turn)
- User can answer multiple questions at once
- Non-essential fields can be skipped, with the note "More complete information = higher claim success rate"

---

### Step 3: Legal Matching → Liability Determination

**Goal**: Match applicable laws and regulations, determine responsible party and claimable rights.

**Legal reference library**:

| Law/Regulation | Key Articles | Applicable Scenarios |
|---|---|---|
| 《快递暂行条例》(Interim Regulations on Express Delivery, 2018) | Art. 27 (compensation), Art. 42 (legal liability) | Delay / loss / damage / missing contents |
| 《快递服务国家标准》GB/T 27917 (National Standard for Express Service) | §5.3 (service time limits), §5.4 (compensation principles), §5.5 (complaint handling) | Service standards, compensation calculation |
| 《中华人民共和国邮政法》(Postal Law of PRC) | Art. 45, Art. 47, Art. 59 | Postal/express service distinction, liability |
| 《快递市场管理办法》(Express Market Management Measures) | Art. 16 (service standards), Art. 20 (no rough handling) | Service quality, handling standards |
| 《快递电子运单》GB/T 41833 (Electronic Waybill Standard) | Full text | Waybill info, privacy protection |
| 《电子商务法》(E-Commerce Law) | Art. 51 (delivery), Art. 52 (logistics delivery) | E-commerce platform delivery obligations |
| 《中华人民共和国民法典》(Civil Code) | Art. 188 (limitation of actions: 3 years), Art. 832 (transportation contract compensation) | Statute of limitations, transport liability |

**Liability determination logic**:

| Dispute Type | Likely Responsible Party | Basis |
|---|---|---|
| Package lost in transit | Courier company | Courier is responsible for package safety unless force majeure |
| Package damaged / contents broken | Courier company (high probability) | Packaging adequacy and insurance status affect compensation amount |
| False delivery (shows signed but not received) | Courier company / courier | Courier signed without recipient's consent |
| Station/locker dispute (unauthorized drop-off) | Courier company / courier | Dropping at station without consent violates regulations |
| Return logistics anomaly | Sender's courier company | Return scenario: responsibility lies with the return carrier |
| Wrong item sent by merchant | E-commerce merchant | Not a courier issue; product quality dispute |
| Cross-border package held by customs | Customs / forwarding agent | Depends on duties / prohibited items / forwarding contract |
| Oversized item damaged | Courier / logistics company | Special compensation standards apply |
| Courier attitude/service violation | Courier company | Violates service standards |

**Output**: Responsible party + cited law text + plain-language explanation + list of claimable rights

---

### Step 4: Compensation Calculation

**Goal**: Precisely calculate claimable compensation based on insured status, item value, and degree of loss.

**Calculation rules**:

#### Scenario A: Insured (保价)
```
Compensation = Insured amount (capped at actual loss, not exceeding insured amount)
               + Shipping refund (where applicable)
```
**Basis**: 《快递暂行条例》Art. 27, GB/T 27917 §5.4
**Notes**:
- Actual loss ≤ insured amount → full actual loss
- Actual loss > insured amount → capped at insured amount (difference borne by user)
- Insurance premium typically 1%-5% of declared value

#### Scenario B: Uninsured (未保价)
```
Compensation = Actual loss (needs proof) + Shipping refund (where applicable)
```
**Basis**: 《快递暂行条例》Art. 27
**Notes**:
- Proof of value required (order screenshot, invoice, payment record)
- Courier company may offer only 3-10x shipping fee or fixed cap
- National Post Office appeal can override company-imposed caps
- Common uninsured cap: 500-2000 CNY for high-value items

#### Scenario C: Partial Damage
```
Compensation = Repair cost or pro-rated item value based on damage ratio
```

**Output**: Compensation breakdown table (calculation process + legal citation + optimistic/conservative estimate + insurance premium refund note)

---

### Step 5: Escalation Path Generation

**Goal**: Generate a 5-level escalation path sorted by cost-efficiency.

```
Level 1 → Courier company customer service
  ├─ Channel: 955xx hotline / courier App / WeChat mini-program / website
  ├─ Time: Typically 7 working days for reply
  ├─ Prerequisite: None (first step for all disputes)
  └─ Script: "Polite negotiation" tone provided

Level 2 → E-commerce platform complaint
  ├─ Channel: Taobao/JD/Pinduoduo/Douyin → Order → Dispute logistics/seller
  ├─ Time: Typically 3-7 working days
  ├─ Prerequisite: Online purchase scenario
  └─ Script: "Platform appeal" tone provided

Level 3 → National Post Office appeal (sswz.spb.gov.cn)
  ├─ Prerequisite: Courier company complaint pending >7 days (or rejected)
  ├─ Channel: sswz.spb.gov.cn / 12305 hotline / "邮政业消费者申诉" WeChat mini-program
  ├─ Time: ~30 days from acceptance
  ├─ Effectiveness: Most powerful courier complaint channel
  └─ Script: "Postal appeal" tone + pre-filled form provided

Level 4 → 12315 consumer complaint
  ├─ Channel: 12315 hotline / 12315 WeChat mini-program / 12315.cn
  ├─ Applicable: Consumer rights damaged, courier complaint exhausted
  └─ Document: Consumer complaint form provided

Level 5 → Legal action (small claims court)
  ├─ Court: Defendant's domicile or contract performance place basic-level court
  ├─ Threshold: Amount ≤ 30% of previous year's average salary (varies by province)
  ├─ Advantage: One-instance final, low filing fee, no lawyer required
  └─ Reminder: Must prepare comprehensive evidence chain
```

**Output**: Visual escalation route map + per-level operation guide + time estimate + success rate reference

---

### Step 6: Legal / Administrative Document Generation

**Goal**: Auto-generate all required claim documents; user can copy-paste or download.

**Document list**:

| Document | Purpose | Included Fields |
|---|---|---|
| **Express Claim Letter** | Formal claim to courier company | Sender/receiver info, tracking number, event description, loss inventory, claim amount, legal basis, time limit |
| **National Post Office Appeal Form** | Submit at sswz.spb.gov.cn | Appellant info, respondent (courier company), tracking number, appeal reason, claim amount, date of company complaint |
| **12315 Consumer Complaint Form** | Submit at 12315 platform | Complainant info, respondent info, complaint request, facts & reasons, evidence list |
| **Evidence Checklist** | Organize evidence for claim | Itemized evidence list, acquisition method, priority level |
| **Timeline Tracker** | Track key deadlines | Complaint date, company reply deadline, postal appeal deadline, statute of limitations expiry |

**Document features**:
- Pre-filled with all user-provided information
- Marked fields requiring user completion (name, phone, address, signature)
- Platform-specific instructions (where to submit, how, what to note)

---

### Step 7: Communication Script Generation

**Goal**: Generate graded communication scripts for different scenarios.

**Script tiers**:

| Tier | Use Case | Tone |
|---|---|---|
| **Polite Negotiation** | First contact with courier CS, hoping for friendly resolution | Polite, factual, express request, leave room |
| **Escalation Pressure** | CS stalling, past promised reply deadline | Cite law, state escalation path, set clear deadline |
| **Postal Appeal** | Company complaint exhausted (7+ days), ready for postal appeal | Formal appeal language, cite regulations, list evidence |

**Script elements**:
- Timeline statement (objective facts)
- Legal basis citation (article ID + plain explanation)
- Clear demand (compensation amount + processing deadline)
- Escalation warning (inform of next step)
- Evidence notice (inform what proof has been gathered)

---

### Step 8: Evidence Collection Checklist

**Goal**: Generate personalized evidence guidance with acquisition methods and priority levels.

**Structured checklist**:

```
📋 Evidence Collection Checklist

★★★ CORE EVIDENCE (Highest impact on claim outcome)
□ Tracking number & waybill screenshot
   Get from: Cainiao App / Kuaidi100 / courier mini-program → logistics detail → screenshot
   Note: Must show logistics status, exception node, timestamps

□ Item value proof
   Get from: E-commerce order screenshot / payment record / invoice / transfer record
   Note: Amount must match item; screenshot must show order ID and amount

□ Damage/loss evidence
   Get from: Unboxing video (best) / damage photos (multiple angles) / weight record
   Note: Unboxing video should continuously show: tracking number → all sides → opening → item close-up

★★ IMPORTANT EVIDENCE
□ Communication records with CS: Call recordings / chat screenshots / CS agent ID
□ Communication records with courier: SMS / WeChat / call log (with timestamps)
□ Delivery confirmation record: Locker pickup code / station notification / signed receipt

★ SUPPLEMENTARY EVIDENCE
□ Product page screenshot (showing item value description)
□ Courier phone number / name / employee ID
□ Station/locker location and name
□ Surveillance footage (if station/property has it)
□ Third-party appraisal report (for high-value items)
```

---

### Step 9: Key Deadline Management

**Goal**: Generate personalized deadline reminders to prevent rights expiration.

**Key deadlines**:

| Deadline Item | Time Limit | Legal Basis | Consequence |
|---|---|---|---|
| Courier company complaint reply | 7 working days | Express service standard | Past-due → eligible for postal appeal |
| National Post Office appeal window | After 7 days of company complaint | Post Office appeal rules | Cannot appeal before 7 days |
| National Post Office case resolution | ~30 days from acceptance | Appeal rules | — |
| Statute of limitations (litigation) | 3 years from discovering harm | 《民法典》Art. 188 | Cannot sue after expiry |
| Evidence preservation recommendation | Immediately after incident | Best practice | Delayed → risk of evidence loss |
| Insured claim filing | ASAP after discovering loss | Courier company terms | Varies by company (7-30 days typical) |

**Output**: Personalized deadline calendar (based on incident date) with key dates and action reminders

---

### Step 10: Report Compilation → Delivery

**Goal**: Integrate outputs from Steps 1-9 into a complete claim report.

**Report structure**:

```
📦 Courier Dispute Claim Report
══════════════════════════════════════

1. 📋 CASE SUMMARY
   - Dispute type, courier company, tracking number, amount involved
   - Event timeline

2. ⚖️ LEGAL ANALYSIS
   - Responsible party determination
   - Applicable laws (original + plain-language explanation)
   - Claimable rights list

3. 💰 COMPENSATION CALCULATION
   - Detailed breakdown (insured / uninsured scenarios)
   - Optimistic vs conservative estimate
   - Legal basis for each calculation

4. 🗺️ ESCALATION PATH
   - 5-level escalation route map
   - Per-level operation guide + time estimate

5. 📄 LEGAL DOCUMENTS
   - Express claim letter
   - National Post Office appeal form
   - 12315 consumer complaint (if applicable)

6. 💬 COMMUNICATION SCRIPTS
   - Polite negotiation version
   - Escalation pressure version
   - Postal appeal version

7. 📋 EVIDENCE CHECKLIST (Personalized)

8. ⏰ DEADLINE REMINDER CALENDAR

══════════════════════════════════════
⚠️ Disclaimer: This report is AI-generated for reference only.
Does not constitute legal advice. Actual claim results depend on
multiple factors including evidence completeness and regulatory decisions.
══════════════════════════════════════
```

**Delivery format**:
- Full Markdown (output directly in chat)
- Recommend user copy-save / export as PDF / share to WeChat
- Key documents available as "one-click copy" compact versions

---

## 🚀 First-Success Path

Follow this path on your first use for fastest results:

1. **Describe your situation** — Paste your package issue in natural language (e.g., "我的快递丢了，中通，单号731..." or "My SF package arrived damaged, insured for 8000 yuan")
2. **Answer 2-3 follow-up questions** — Provide tracking number, item value, and insurance status when asked
3. **Receive your complete claim report** — In under 60 seconds, get:
   - ⚖️ Liability analysis with legal citations
   - 💰 Compensation calculation (optimistic & conservative)
   - 🗺️ 5-level escalation path tailored to your case
   - 📄 Ready-to-file appeal documents (claim letter, postal appeal form)
   - 💬 Communication scripts (polite → pressure → appeal)
   - 📋 Personalized evidence checklist
   - ⏰ Deadline calendar

**Expected output (abridged example)**:
```
⚖️ Responsible Party: [Courier Company Name]
📜 Legal Basis: [Law Name] Article [X]
💰 Claimable Amount: [Amount] CNY
📈 Recommended Path: Level 1 → Level 3 (combined)
📄 Generated: Claim Letter ✓, Postal Appeal ✓, Evidence Checklist ✓
```

---

## Input/Output Schema

### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `dispute_type` | enum | yes | lost_package / damaged_goods / false_delivery / station_dispute / missing_items / cross_border / oversized_damage / customs_hold / service_complaint / wrong_delivery |
| `courier_company` | string | yes | SF Express / ZTO / YTO / Yunda / STO / J&T / JD / Deppon / EMS / Cainiao / Other |
| `tracking_number` | string | yes | Express tracking number |
| `item_description` | string | important | Item name and type |
| `item_value` | number (CNY) | important | Item value in yuan |
| `insured` | boolean | important | Whether insured (保价) |
| `insured_amount` | number (CNY) | conditional | Insured amount (required if insured=true) |
| `user_role` | enum | yes | receiver / sender / merchant / cross_border_buyer |
| `incident_date` | date | advisory | Date dispute occurred |
| `has_value_proof` | boolean | advisory | Has proof of item value |
| `has_unboxing_video` | boolean | advisory | Has unboxing video |
| `contacted_courier` | boolean | advisory | Already contacted courier |
| `courier_response` | string | advisory | Courier's response summary |
| `platform` | enum | advisory | taobao / jd / pinduoduo / douyin / xianyu / other / none |

### Output Schema

| Section | Content |
|---|---|
| `case_summary` | Dispute type, courier, tracking, item value, insured, timeline |
| `legal_analysis` | Responsible party, applicable laws (name, article, full text, plain explanation), claimable rights |
| `compensation_calculation` | Insured scenario, uninsured scenario, optimistic/conservative estimates, shipping refund |
| `escalation_path` | 5 levels (channel, URL/phone, prerequisite, time estimate, success hint) |
| `generated_documents` | claim_letter, postal_appeal, consumer_complaint_12315, evidence_checklist, timeline_tracker |
| `communication_scripts` | polite_version, escalation_version, postal_appeal_version |
| `full_report` | Complete claim report in Markdown |

---

## Sample Prompts

### Prompt 1: Lost Package — Uninsured (Chinese)
> **Input:** 我在淘宝买了一个1200元的蓝牙耳机，中通快递，单号73123456789012。物流显示5天前到了杭州转运中心就再也没更新了。联系卖家说让我自己找快递，中通客服打了3次都说在查。没有保价，有淘宝订单截图。
>
> **Expected output:**
> ```
> ⚖️ Responsible Party: ZTO Express (package lost in transit)
> 📜 Legal Basis: 《快递暂行条例》Article 27
> 💰 Claimable: 1200 CNY (with Taobao order proof, uninsured)
>     Conservative: Courier may offer only 3-5x shipping fee (~45-75 CNY)
>     → Postal appeal needed to override cap
> 📈 Recommended Path: Taobao logistics dispute + National Post Office appeal (parallel)
> 📄 Generated: Claim Letter ✓, National Post Office Appeal ✓, Evidence Checklist ✓
> ```

### Prompt 2: Insured Goods Damage — English
> **Input:** I used SF Express to ship a mirrorless camera, insured for 8000 yuan, shipping cost 68 yuan. The recipient opened it and found the screen cracked. I have an unboxing video. SF said "need to verify" — it's been 10 days with no result.
>
> **Expected output:**
> ```
> ⚖️ Responsible Party: SF Express (insured goods damaged in transit)
> 📜 Legal Basis: 《快递暂行条例》Art. 27 — insured items paid at the lower of actual loss or insured amount
> 💰 Claimable: Screen repair ~1500-2500 CNY (actual loss < insured 8000 → full actual loss)
>     + Shipping refund (68 yuan)
> 📈 Recommended Path: Level 3 National Post Office appeal immediately (company complaint >7 days)
> 📄 Generated: SF Claim Letter ✓, Postal Appeal ✓, Evidence Checklist ✓
> 💡 Tip: Unboxing video is the strongest evidence. You're in a good position.
> ```

### Prompt 3: False Delivery — Platform Dispute (Chinese)
> **Input:** 我在拼多多买了一个89元的手机壳，圆通快递，单号YT9876543210。物流显示已签收-本人签收，但我根本没收到。快递员电话打不通，圆通客服说系统显示签收了就是签收了。菜鸟驿站也说没有。
>
> **Expected output:**
> ```
> ⚖️ Responsible Party: YTO Express (false delivery — courier signed without consent)
> 📜 Legal Basis: 《快递暂行条例》Art. 25 (delivery to agreed address required)
> 💰 Claimable: 89 CNY (item value) + shipping refund
> 📈 Recommended Path: Level 2 Pinduoduo platform dispute first (fast for small amounts)
>     → Level 3 National Post Office if platform doesn't resolve
> 📄 Generated: Claim Letter ✓, Pinduoduo Logistics Complaint Template ✓
> ```

### Prompt 4: Cross-Border — Customs Hold (English)
> **Input:** My textbooks from Amazon US are stuck at customs for 2 weeks. EMS tracking EE123456789CN, worth $280. They want me to pay 450 yuan duty but textbooks should be tax-free.
>
> **Expected output:**
> ```
> ⚖️ Analysis: Personal-use textbooks are generally duty-exempt (≤10 volumes)
>     《中华人民共和国海关进出境印刷品及音像制品监管办法》
> 💰 Claim Focus: Zero customs duty (legally exempt)
>     Investigate whether it's actually storage fees or misclassification
> 📈 Recommended Path:
>     1. Verify charge source with EMS (11183) — ask Chinese speaker for help
>     2. Submit duty exemption declaration with proof (Amazon receipt, ISBN list)
>     3. If denied → China Customs hotline 12360
>     4. If EMS detention exceeds 15 days → National Post Office appeal
> 📄 Generated: EMS Inquiry Script (Chinese+English) ✓, Customs Complaint Template ✓
> ```

### Prompt 5: Station Unauthorized Drop-off (Chinese)
> **Input:** 我出差回来取快递，菜鸟驿站要收我5块超时保管费。快递员根本没问我就放驿站了！这钱应该我出吗？
>
> **Expected output:**
> ```
> ⚖️ Legal Analysis: Courier dropping at station without YOUR consent violates
>     《快递暂行条例》Art. 25. Any storage fee incurred should be borne by the courier, not you.
> 💰 Claimable: Fee waiver (0 yuan charged to you)
> 📈 Recommended Path:
>     1. Refuse to pay storage fee; ask station to contact courier
>     2. Call courier company to complain about unauthorized drop-off
>     3. If unresolved → National Post Office appeal (effective for this type)
> 💬 "This package was dropped at the station without my consent per 《快递暂行条例》Art. 25.
>    The storage fee is not my responsibility. Please resolve this."
> ```

### Prompt 6: Oversized Item Damage — Insufficient Insurance (English)
> **Input:** Deppon Express damaged my 65-inch TV during moving. TV value 4500 yuan, insured only 3000. They only offer 2000 yuan compensation. I have unboxing video.
>
> **Expected output:**
> ```
> ⚖️ Legal Analysis: Deppon's offer of 2000 yuan is incorrect.
>     《快递暂行条例》Art. 27: Insured item → paid at the lower of actual loss or insured amount.
>     Actual loss 4500 > insured 3000 → FULL 3000 yuan (not 2000).
> 💰 Claimable: 3000 yuan (full insured amount) + shipping refund
>     Difference 1500 yuan borne by user (insufficient insurance)
> 📈 Recommended Path:
>     1. Re-contact Deppon 95353 with legal citation → demand full 3000
>     2. If not resolved in 3 days → National Post Office appeal
>     3. Concurrently → 12315 complaint for deceptive compensation practice
> 💡 With unboxing video and proof of insurance, this is a strong case.
> ```

### Prompt 7: Business Traveler Luggage Damage (English)
> **Input:** I used SF Express to ship my luggage from Shanghai to Beijing. Suitcase wheel broken + business suit (2800 yuan) stained. Shipping 168 yuan, insured 500 yuan. Have photos of damage.
>
> **Expected output:**
> ```
> ⚖️ Liability: SF Express — fully liable (insured, documented damage)
> 💰 Compensation: Insured cap 500 yuan (actual loss ~4000 > insured 500)
>     + Shipping refund 168 yuan
>     Total claimable: 668 yuan
> 📈 Recommended Path:
>     1. SF Express 95338 → demand full insured amount 500 + shipping refund
>     Persist through escalation script ✓
>     2. If underpaid → National Post Office appeal
> 📄 Generated: SF Claim Letter ✓, Evidence Checklist ✓
> 💡 Lesson: Insure at full replacement value next time.
> ```

---

## 🀄 Chinese Usage Scenarios

### 中文场景 1：深夜发现快递丢了 — 愤怒型用户

**情景**: 凌晨12:30，小明刷手机发现京东买的3599元显卡物流停在「已签收」但自己根本没收到，打京东快递客服没人接，焦虑得睡不着。

**完整交互**:
```
👤 用户：京东买的显卡3599，物流说签收了但我没收到！

🤖 AI：检测到虚假签收纠纷，我来帮您梳理。
请提供快递单号（JD开头的那串数字）。

👤 用户：JDX0123456789

🤖 AI：还需要几个信息：
1. 这个快递有没有保价？
2. 方便提供京东订单截图的大致信息吗（确认购买时间、金额）？

👤 用户：没保价，有截图，6月18号买的。

🤖 AI：分析完成——

⚖️ 责任判定：京东快递（虚假签收，快递员擅自操作签收状态）
📜 依据：《快递暂行条例》第27条
💰 可主张：3599元（凭京东订单截图）
📈 推荐路径：
第1步 🕗 明早8点后 → 拨打京东快递950616
第2步 🔄 京东App→我的订单→投诉物流
第3步 📮 3天没结果 → sswz.spb.gov.cn 提交申诉

📄 已生成：京东快递索赔函 ✓、国家邮政局申诉书 ✓、沟通话术（3版本）✓、证据清单 ✓
```

---

### 中文场景 2：寄大件家具被摔坏 — 寄件人维权

**情景**: 小陈从杭州搬家到成都，通过德邦物流寄了一台65寸电视（价值4500元），保价3000元。收到后发现屏幕碎裂，德邦以「保价金额不足以覆盖实际损失」为由只愿赔2000元。

**完整交互**:
```
👤 用户：德邦把我的电视摔坏了，保价3000，电视4500买的，
       他们只肯赔2000，说保价不够。我有开箱视频。

🤖 AI：德邦的说法不完全正确，为您详细分析——

⚖️ 法律分析：
根据《快递暂行条例》第27条，保价物品按保价金额与实际损失
二者中较低者赔偿。实际损失4500元 > 保价金额3000元，
应全额赔偿3000元。德邦打折赔付违规。

💰 赔偿计算：
• 保价赔偿：3000元（全额，不是2000）
• 快递费退还：应退还（服务未达标）
• 合计可主张：3000元 + 运费
• 差额1500元：因保价低于实际价值，该部分需自担

📈 推荐路径：
第1步 → 再次致电德邦95353，明确告知法条依据
第2步 → 3天后不满意 → 国家邮政局申诉
第3步 → 同步12315投诉（涉嫌违规拒赔）

📋 优势：有开箱视频、有购买凭证、已保价
📄 预计处理时间：7-14天
```

---

### 中文场景 3：驿站超时收费纠纷 — 小额高频

**情景**: 小美出差回来取快递，菜鸟驿站要求付5元超时保管费（1元/天）。小美认为快递员未经同意就投放驿站，不应由自己承担超时费。

**完整交互**:
```
👤 用户：出差回来取快递，菜鸟驿站要收我5块超时费。
       快递员没问我就放驿站了！这钱应该我出吗？

🤖 AI：快递员未经您同意投放驿站本身就不合规，
超时费不应由您承担。

⚖️ 法律分析：
根据《快递暂行条例》第25条，快递企业应按约定的地址投递。
快递员未经收件人同意擅自投放驿站/快递柜违反服务标准。
由此产生的超时费用应由快递公司承担。

📋 操作建议：
第1步 → 拒绝支付超时费，要求驿站联系快递员处理
第2步 → 联系快递公司客服投诉快递员
第3步 → 菜鸟App评价投诉
第4步 → 如不处理 → 国家邮政局申诉

💬 "这个快递是快递员未经我同意投放驿站的，
根据《快递暂行条例》第25条，我有权要求按约定地址投递。
超时费不应由我承担，请你们处理。"

💡 提示：国家邮政局对未经同意投放驿站的投诉处罚力度大，
通常很快解决。
```

---

## 🌐 English Usage Scenarios

### Scenario 1: Expat in China — Lost Package with No Chinese Skills

**Context**: John, an expat in Shanghai, ordered a laptop stand (¥399) from Taobao. ZTO tracking shows "delivered" but he never received it. Seller says "contact ZTO yourself." John can't speak Chinese well enough to file a complaint.

**Flow**:
```
👤 User: My package says delivered but I didn't get it. ZTO,
        tracking number 7534567890123, laptop stand 399 yuan.
        I have the Taobao order receipt. What do I do?

🤖 AI: I've analyzed your case — false delivery dispute.

⚖️ Legal Analysis:
ZTO Express is liable under 《Interim Regulations on Express Delivery》 
(Article 27). The courier logged a false delivery confirmation.

💰 Claimable: ¥399 (Taobao receipt as value proof) + shipping refund

📈 Recommended Path:
Step 1 → Taobao App → My Orders → Dispute Logistics (English-friendly UI)
Step 2 → Simultaneously contact ZTO via 95311 (ready-to-use Chinese script with pinyin ↓)
Step 3 → If no resolution in 7 days → National Post Office Appeal (sswz.spb.gov.cn)

📄 Generated:
• ZTO Claim Letter (Chinese with English annotations) ✓
• National Post Office Appeal (pre-filled Chinese, pinyin included) ✓
• Evidence Checklist ✓
• Communication Script (3 tones, pinyin annotations) ✓
```

---

### Scenario 2: Cross-Border Student — Package Held by Customs

**Context**: Maria, a graduate student in Beijing, ordered textbooks from Amazon US. Package (worth $280) sent via EMS, stuck at "customs clearance" for 2 weeks. She received a text asking her to pay ¥450 in customs duties — but textbooks should be duty-free.

**Flow**:
```
👤 User: My textbooks from Amazon are stuck in customs for 2 weeks.
        EMS tracking EE123456789CN, worth $280. Now they want 450 yuan
        duty but textbooks should be tax-free, right?

🤖 AI: You're right — personal-use textbooks are generally duty-free.

⚖️ Analysis:
• Personal textbooks (≤10 volumes) → exempt from customs duty
  per 《海关进出境印刷品及音像制品监管办法》
• If held >15 days without notification → possible EMS handling issue

💰 Claim Focus: Zero customs duty (legally exempt)
• Also check if ¥450 is misrepresented storage/customs broker fees

📈 Recommended Path:
Step 1 → Verify the ¥450 charge source with EMS (11183)
         (is it duty, storage fee, or broker charge?)
Step 2 → Explain textbooks are duty-exempt; request release
Step 3 → If held >15 days → National Post Office + Customs (12360)

📄 Generated:
• EMS Inquiry Script (Chinese + English) ✓
• Duty Exemption Reference ✓
• Customs Complaint Template ✓
```

---

### Scenario 3: Business Traveler — Luggage Courier Damage

**Context**: David used SF Express to ship luggage (suitcase + suits) from Shenzhen to Beijing. Suitcase wheel broken + suit (¥2,800) stained. Shipping ¥168, insured ¥500. Damage documented.

**Flow**:
```
👤 User: SF Express damaged my luggage — broken wheel, stained suit.
        Insured 500 yuan. Shipping 168. Actual value suitcase 1200 + suit 2800.
        I have damage photos. What can I claim?

🤖 AI: Insured goods damage case analysis:

⚖️ Liability: SF Express — fully liable (insured, documented)

💰 Compensation:
• Insured claim: 500 yuan (full insured — both items damaged exceeds 500)
• Shipping refund: 168 yuan
• Total claimable: 668 yuan
⚠️ Actual loss (4000+) >> insured (500), so recovery capped at insured amount.

📈 Path:
Step 1 → SF Express 95338 — demand full insured + shipping refund
Step 2 → If offers < 500 → National Post Office appeal
Step 3 → 12315 consumer complaint

📄 Generated:
• SF Express Formal Claim Letter ✓
• Damage Evidence Checklist ✓
• Postal Appeal Form (backup) ✓

💡 Lesson: Insure at full replacement value next time. 
    Premium is only 0.5-1% of declared value — worth it for items over ¥500.
```

---

## What This Skill Does NOT Do

| Refusal Scenario | Response |
|---|---|
| 🚫 Legal advice (replace lawyer) | "This analysis is based on publicly available regulations for reference only. Does not constitute legal advice. For significant property losses (≥5000 CNY) or personal injury, consult a licensed lawyer." |
| 🚫 Cases already in litigation | "Your case has entered judicial proceedings. This assistant no longer intervenes. Please follow court judgment and legal counsel." |
| 🚫 Non-courier logistics | "This dispute does not fall under courier/logistics scope (appears to be [food delivery / errand / LTL freight / ...]). Please use the appropriate channel or skill." |
| 🚫 Pure legal inquiry (no specific incident) | "This assistant focuses on specific courier disputes. For general legal text exploration, please consult the original regulations." |
| 🚫 Filing complaints on user's behalf | "I've prepared all complaint materials for you, but you must submit them yourself. Please follow the guided path." |
| 🚫 Corporate / business contract disputes | "Bulk shipping contracts and corporate logistics agreements involve commercial terms beyond this personal courier dispute assistant's scope." |
| 🚫 Food delivery / instant delivery disputes | "Food delivery disputes are governed by different regulations (《网络餐饮服务食品安全监督管理办法》). Please use the food delivery platform's complaint channel." |
| 🚫 Cross-platform automated operations | "This assistant does not log into any platform or website on your behalf. All appeals must be filed by you personally." |
| 🚫 Guaranteed outcomes | "All analysis is AI-assisted. Claim results depend on evidence completeness, timeliness, responsible party, and regulatory decisions. No outcome guarantee." |
| 🚫 Direct courier complaint system integration | "This assistant does not directly interface with courier company complaint systems. All complaints must be filed by you through the provided channels." |

---

## ⚠️ Disclaimer

```
⚠️ DISCLAIMER

1. This assistant provides AI-generated content for reference only.
   It does NOT constitute legal advice. For disputes involving
   significant property loss (threshold: ≥5,000 CNY) or personal
   injury, please consult a licensed lawyer.

2. Compensation calculations are estimates based on information
   you provide and applicable regulations. Actual compensation
   depends on courier company decisions, postal authority mediation,
   or court judgments.

3. Regulations may be amended or subject to regional variation.
   This assistant references publicly published legal texts and
   does not guarantee real-time synchronization with latest
   judicial interpretations or local regulations.

4. This assistant does NOT perform any complaint, appeal, or
   litigation actions on your behalf. All claim actions must
   be initiated by you or your legal representative.

5. This assistant does NOT intervene in cases that have entered
   judicial proceedings. If your case has been filed in court,
   follow the court judgment and your lawyer's advice.

6. The legality and evidentiary weight of recordings, screenshots,
   videos, and other evidence you collect during the claim process
   shall be determined by the accepting authority.

7. This assistant does NOT guarantee any claim outcome. Claim
   success rate is affected by evidence completeness, timeliness,
   liability determination, and other factors.
```

---

## Legal References

### Primary Laws and Regulations

| Law/Regulation | Issuance | Key Application |
|---|---|---|
| 《快递暂行条例》(Interim Regulations on Express Delivery) | State Council Decree No. 697 (2018) | Core legal basis for express delivery disputes: Art. 25 (delivery to agreed address), Art. 27 (compensation for delay/loss/damage), Art. 42 (legal liability) |
| 《快递服务国家标准》GB/T 27917 (National Standard for Express Service) | SAC/TC 462 | Service time limits (§5.3), compensation principles (§5.4), complaint handling (§5.5) |
| 《中华人民共和国邮政法》(Postal Law of PRC) | NPC Standing Committee | Art. 45 (postal vs express service), Art. 47 (liability), Art. 59 (applicable to express business) |
| 《快递市场管理办法》(Express Market Management Measures) | MIIT | Art. 16 (service standards), Art. 20 (prohibition of rough handling), Art. 28 (compensation) |
| 《快递电子运单》GB/T 41833 (Electronic Waybill Standard) | SAMR | Waybill information, privacy protection |
| 《电子商务法》(E-Commerce Law) | NPC Standing Committee | Art. 51 (delivery obligation), Art. 52 (logistics delivery) |
| 《中华人民共和国民法典》(Civil Code) | NPC (2021) | Art. 188 (3-year statute of limitations, changed from 1 year), Art. 832 (transportation contract liability) |

### Key Article References

- **《快递暂行条例》Art. 25**: "Express enterprises shall deliver items to the address agreed upon by the consignee... If the consignee is unable to receive in person, the enterprise shall contact the consignee to agree on a delivery method."
- **《快递暂行条例》Art. 27**: "If a delay, loss, damage, or shortage of contents occurs during the express delivery process, the express enterprise shall compensate according to the agreement with the user. For insured items, compensation shall be according to the insurance agreement. For uninsured items, compensation shall be according to the Civil Code and relevant regulations."
- **GB/T 27917 §5.4**: Insured items: compensation is the lower of actual loss or insured amount. Uninsured items: compensation referenced to actual loss with value proof; without proof, up to a multiple of the shipping fee.

### Courier Service Hotlines (Quick Reference)

| Courier | Hotline | Website | App/Mini-Program |
|---|---|---|---|
| SF Express (顺丰速运) | 95338 | sf-express.com | App → My → Complaints & Suggestions |
| ZTO (中通快递) | 95311 | zto.com | WeChat mini-program → My → Complaint |
| YTO (圆通速递) | 95554 | yto.net.cn | WeChat mini-program → Service Center |
| Yunda (韵达快递) | 95546 | yundaex.com | App → My → Online CS |
| STO (申通快递) | 95543 | sto.cn | WeChat mini-program → CS Center |
| J&T (极兔速递) | 956025 | jetpress.cn | WeChat mini-program → My → Complaint |
| JD Logistics (京东物流) | 950616 | jdl.com | JD App → My → Customer Service |
| Deppon (德邦快递) | 95353 | deppon.com | WeChat mini-program → Online CS |
| EMS | 11183 | ems.com.cn | WeChat mini-program → CS |
| Cainiao (菜鸟裹裹) | 9519666 | cainiao.com | Cainiao App → My → CS |

### Claim Platform Entry Points

| Platform | Entry | Description |
|---|---|---|
| National Post Office Appeal (国家邮政局申诉) | sswz.spb.gov.cn / 12305 / WeChat mini-program "邮政业消费者申诉" | Most effective courier complaint channel |
| 12315 Consumer Rights Platform | 12315.cn / WeChat mini-program "全国12315平台" | Consumer rights complaint platform |
| Taobao Logistics Complaint | Order → Dispute Logistics | E-commerce logistics dispute |
| JD Logistics Complaint | Order → Customer Service → Logistics Issue | JD platform logistics dispute |
| Pinduoduo Logistics Complaint | Order → After-sales → Logistics Issue | Pinduoduo platform logistics dispute |
| Douyin Logistics Complaint | Order → After-sales → Logistics | Douyin e-commerce logistics |

---

## Persistence & Data Storage

```
~/.openclaw/data/package-claim-helper/
├── cases.db              # Anonymized case records
├── config/
│   ├── courier_contacts.yaml   # Courier contact info (updateable)
│   ├── legal_provisions.yaml   # Legal provisions library (updateable)
│   └── templates/               # Document templates
└── reports/                     # Generated reports (user-optional)
```

**Privacy notes**:
- Tracking numbers are masked in storage (e.g., `JDX0****789`)
- Personal info (name, phone, address) used only for document generation, not persisted
- No automated complaint filing; user initiates all actions
- High-value disputes (≥5,000 CNY) trigger enhanced disclaimer and lawyer consultation recommendation
