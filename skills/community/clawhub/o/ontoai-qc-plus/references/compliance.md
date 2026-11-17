# Compliance Checks

Version 1.4.0 | 2026-10-11

> Compliance findings rank at **maximum severity**, equal to factual-integrity defects. A hit enters Must Fix (when certainty = 1.0).
> This file performs **risk flagging only** and does not constitute legal advice. Findings graded Must Fix should prompt the user: "recommend legal/compliance review."
> Language scope: L1 targets Chinese artifacts; L7 targets English artifacts; L2–L4 are language-agnostic (regex-based) and apply to both. L5/L6 patterns are Chinese-oriented but their principles apply to any language.

---

## L1 · Advertising-Law Superlatives (Chinese artifacts)

**Basis**: Article 9 of the Advertising Law of the People's Republic of China（《中华人民共和国广告法》第九条）— advertisements must not use terms such as "国家级" (national-grade), "最高级" (highest-grade), "最佳" (best).

**Trigger words (regex; inherently Chinese)**:
```
国家级|最高级|最佳|最优|最强|最好|最大|最高|最先进|最低价|最便宜|最新科学|最新技术
|第一(品牌|名|家)?|首个|首选|独家|唯一|独创|顶级|极品|巅峰|极致|史无前例|前所未有
|百分百|百分之百|100%有效|绝对|万能|永久|无敌|永不|包治|根治|彻底解决|一次解决
|领先|遥遥领先|革命性|颠覆性|划时代|史上最
```

**Grading**:
- In **advertising / marketing / e-commerce / landing-page** scenarios → **Must Fix**
- In internal docs, technical docs, non-marketing contexts → Should Fix or not reported
- With genuine verifiable evidence (e.g. "全国销量第一" backed by an authoritative statistics source) → demote to Unverified; prompt the user to have the proof ready

**Protection boundaries**:
- Product model names (e.g. "极光 MAX"), established proper nouns, official titles
- Statements already certified by an authoritative body with documentation available

---

## L2 · Secrets & Credential Leakage

**Trigger (regex; language-agnostic)**:
```
(sk-|pk_live|pk_test)[A-Za-z0-9]{16,}
AKIA[0-9A-Z]{16}
-----BEGIN [A-Z ]*PRIVATE KEY-----
(password|passwd|pwd|secret|token|api[_-]?key|access[_-]?key)\s*[:=]\s*['"]?[^\s'"]{6,}
(mongodb|mysql|postgres|redis):\/\/[^\s:@]+:[^\s@]+@
Bearer\s+[A-Za-z0-9._-]{20,}
```

**Grading**: **Must Fix**, severity 5.

**Additional checks**: sample keys in config files, front-end code, log output, screenshots, and example documents (even fake ones — prompt "suggest replacing with a placeholder").

**Action**: flag the location, **never substitute on the user's behalf** (replacement requires the user's confirmed key-management plan).

---

## L3 · Personal Private Information

**Trigger (regex; Chinese formats — for English artifacts, adapt patterns to SSN/phone/address formats)**:
```
身份证：[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]
手机号：1[3-9]\d{9}
银行卡：\d{16,19}
邮箱（对外发布物）：[\w.+-]+@[\w-]+\.[\w.]+
详细住址：.{2,10}(省|市).{2,10}(区|县).{5,30}(路|街|号)
```

**Grading**: public-release scenario → **Must Fix** (suggest redaction); internal docs → Should Fix.

**Protection boundaries**: publicly listed business contact info, customer-service numbers, official website email — necessary information; keep.

---

## L4 · Copyright & Licensing

| # | Check | Grading |
|---|---|---|
| 4.1 | Quoting others' work (text/image/music/video) without attribution | Must Fix (add source or delete) |
| 4.2 | Using unlicensed material (commercial images, fonts, sound effects) | Must Fix (flag licensing risk) |
| 4.3 | Commercial font risk (Microsoft YaHei, FangZheng fonts require a commercial license) | Should Fix |
| 4.4 | Long unattributed excerpts (beyond fair-quotation scope) | Must Fix |
| 4.5 | Derivative works / adaptations without authorization | Must Fix |

**Action**: **flag risk only; never issue a legal conclusion.** Prompt "recommend confirming licensing status."

---

## L5 · Industry-Prohibited Claims

| Industry | Prohibited statements | Grading |
|---|---|---|
| **Finance** | Principal-guaranteed returns, guaranteed profit, zero risk, promised annualized yield, insider information, limit-up predictions | Must Fix |
| **Medical** | 根治/包治 (cure-all), special efficacy, no side effects, most advanced therapy, 100% cure rate | Must Fix |
| **Education** | Guaranteed pass, refund-if-fail (without basis), crash-course promises, score-gain guarantees | Must Fix |
| **Real estate** | Appreciation guarantees, ROI promises, school-district promises (without official documents) | Must Fix |
| **Recruiting** | Gender/age/region/marital-status restrictions | Must Fix |

**Sample trigger regex (Chinese)**:
```
保本|保收益|稳赚|零风险|包过|包治|根治|特效|无副作用|药到病除|速成|保证.{0,6}(收益|回报|升值|通过)
```

English equivalents (guaranteed returns / risk-free investment / miracle cure / guaranteed pass) are covered by L7 for marketing contexts and by the same principle here otherwise.

---

## L6 · Sensitive Statements

| # | Check | Grading |
|---|---|---|
| 6.1 | Ethnic or religious misstatements or discrimination | Must Fix |
| 6.2 | Regional discrimination | Must Fix |
| 6.3 | Gender, age, or disability discrimination | Must Fix |
| 6.4 | Errors concerning national sovereignty or territorial integrity | Must Fix |
| 6.5 | Unverified statements about major public events | Unverified |

**Note**: hit rate is extremely low but severity is maximum (5). Prefer missing over erring — **when unsure, don't report, or send to Unverified**.

---

## L7 · English Truth-in-Advertising / Superlatives (FTC)

**Basis**: Section 5 of the U.S. Federal Trade Commission Act (FTC Act §5) — the core prohibition of deceptive advertising claims; unsupported superlative or absolute claims about a product's efficacy, ranking, or safety are actionable as deceptive advertising. For endorsement- and testimonial-style claims (influencer quotes, user reviews), the FTC's Guides Concerning the Use of Endorsements and Testimonials in Advertising (16 CFR Part 255) may additionally apply. (Secrets/privacy/copyright checks live in L2–L4; their regexes are language-agnostic and apply to English as-is.)

**Trigger words (regex, case-insensitive)**:
```
\s(best|#1|number one|greatest|most advanced|most powerful|leading|top-?rated|world'?s? leading|ultimate|unbeatable|unsurpassed|flawless|perfect|100%|guaranteed|risk-?free|no side effects|clinically proven|scientifically proven|instant(ly)?|miracle|magic)\b
```

**Grading**:
- In **English advertising / marketing / e-commerce / landing-page / SaaS-site** scenarios → **Must Fix** (when certainty = 1.0)
- In technical docs, non-marketing contexts → Should Fix or not reported
- With genuine, verifiable backing (e.g. "ranked #1 by G2 in 2026" with a source) → demote to Unverified; prompt the user to have the proof ready

**Relationship to L1 (Chinese Advertising Law)**: L1 governs Chinese superlatives (最佳/第一/国家级); L7 governs the English equivalents. For mixed Chinese/English artifacts, load both sections.

**Protection boundaries**: product model names, established proper nouns, statements already certified by an authoritative body with documentation available.

---

## How to Report Compliance Findings

A compliance finding must state three things clearly:

1. **The hit excerpt** (verbatim)
2. **The risk type** (which of L1–L7)
3. **The consequence of not fixing** (e.g. "may be ruled an illegal advertisement by the market regulator, exposing the publisher to fines")

**Never rewrite compliance language yourself** — rewording may change the legal meaning; only prompt the user to review.

---

## Note on a Removed Item

An early draft included AI-generated-content labeling obligations under the《人工智能生成合成内容标识办法》(Measures for Labeling AI-Generated Synthetic Content, effective 2025-09-01).
**Removed**, because those Measures bind **online information-service providers** (platforms), not ordinary users producing documents, code, and images with AI — including them was a misapplication.

If the user **actively asks** "do I need to label this as AI-generated?", answer per the following (not a QC item):
- Platform operators (products offering AI-generation services) carry the mandatory labeling obligation;
- Individual users publishing on a platform follow that platform's rules and prompts.
