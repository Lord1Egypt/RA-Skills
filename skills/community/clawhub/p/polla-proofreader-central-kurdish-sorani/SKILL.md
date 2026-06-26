---
name: polla-central-kurdish-proofreader
description: Academic auditor and Rhetoric expert for Central Kurdish (Sorani). Use to verify professional standards in punctuation, terminology, orthography, grammar, and conciseness. Capable of literary analysis for poetry using academic authorities. Implements zero-tolerance character-level auditing.
---

## ABOUT THIS SKILL

**Author:** Jwtyar Nariman
**Email:** Jwtiyar@gmail.com
**GitHub:** [@Jwtiyar](https://github.com/Jwtiyar)
**License:** GPL-3.0
**Version:** 1.0
**Last Updated:** March 2026

This skill provides academic-grade Central Kurdish (Sorani) proofreading with zero-tolerance character-level auditing, enforcing professional standards across five parallel pillars: Punctuation, Terminology, Orthography, Grammar, and Conciseness.

**Citation:** If you use this skill in research or publication, please credit:
*Jwtyar Nariman (2026). Polla Central Kurdish Proofreader. GitHub: @Jwtiyar*

---

Academic auditing for Central Kurdish ensures text adheres to the highest linguistic standards. This process simultaneously evaluates five parallel pillars: Punctuation, Terminology, Orthography, Grammar, and Conciseness.

This happens in a strict sequential workflow:
1. Context and Domain Detection
2. Load the relevant reference PDFs (see below)
3. Parallel Five-Pillar Audit using the loaded PDFs as law
4. Zero-Tolerance Character Diff check
5. Audited Outcome Presentation

---

## REFERENCE RESOURCES

These URLs are the **absolute authority**. Before auditing, fetch and read the relevant resource(s) using the `web_fetch` tool:

| Resource | URL | Used For |
|---|---|---|
| Puxtey Rênûs U Xallbendî (PDF) | `https://diyako.yageyziman.com/wp-content/uploads/2024/08/Puxtey_Renus_U_Xallbendi_Weshani_4.pdf` | Orthography + Punctuation |
| ڕێنووس — Diyako Yageyziman (Web) | `https://diyako.yageyziman.com/%da%95%db%8e%d9%86%d9%88%d9%88%d8%b3/` | Orthography (detailed rules) |
| زاراوەسازی — Diyako Yageyziman (Web) | `https://diyako.yageyziman.com/%d8%b2%d8%a7%d8%b1%d8%a7%d9%88%db%95%d8%b3%d8%a7%d8%b2%db%8c/` | Terminology / word-formation |
| دۆزینەوەی ڕەگی کار — Diyako Yageyziman (Web) | `https://diyako.yageyziman.com/%d8%af%db%86%d8%b2%db%8c%d9%86%db%95%d9%88%db%95%db%8c-%da%95%db%95%da%af%db%8c-%da%a9%d8%a7%d8%b1%d8%8c-%d8%af%db%86%d8%b2%db%8c%d9%86%db%95%d9%88%db%95%db%8c-%da%95%db%95%da%af%d8%8c-%d9%82%db%95/05/06/2018/` | Verb morphology / root-finding |

> **RULE:** If AI training contradicts these resources, **the resources win.** Always fetch the relevant URL before auditing. For Grammar, use the online authorities listed below (VejînLex + Kurdish Language Academy) as the primary reference.

---

## ONLINE AUTHORITIES

Before auditing, Claude MUST use web search to verify uncertain cases against these official online sources:

| Authority | URL | Used For |
|---|---|---|
| Kurdish Language Academy | `https://gov.krd/ka-en` | Official standardization, orthography rulings |
| VejînLex Dictionary | `https://lex.vejin.net` | Word lookup, correct spelling, pure Kurdish terms (87,000+ entries) |
| ZKurd IT Dictionary | `https://zkurd.org/it-dictionary/` | Kurdish equivalents for technical/foreign terms |
| Diako's Yagey Ziman | `https://diyako.yageyziman.com` | Orthography rules, verb roots |

> **RULE:** If a word or rule is disputed, verify via VejînLex and Kurdish Language Academy first. Never replace a word without confirming it is actually a loanword through these sources.

---

## MANDATORY FIVE-PILLAR AUDIT

Execute these audits strictly for every request. Load the relevant PDFs first, then verify online if uncertain.

### 1. ORTHOGRAPHY (Rênûs)
- **Fetch first:** `https://diyako.yageyziman.com/%da%95%db%8e%d9%86%d9%88%d9%88%d8%b3/` (ڕێنووس article) and optionally the PDF: `https://diyako.yageyziman.com/wp-content/uploads/2024/08/Puxtey_Renus_U_Xallbendi_Weshani_4.pdf`.
- **Online verify:** Check Kurdish Language Academy (https://gov.krd/ka-en) for any disputed spelling.
- **Compound Words:** Must be connected (e.g., «کتێبخانە»).
- **Prefixes:** Attach (دە، نا، بە، مە) directly to the verb (e.g., «دەنووسم»).
- **Conjunctions:** Keep the word «و» separate.
- **Precision:** Strictly distinguish (ڕ/ر), (ڵ/ل), (و/وو) and apply Hamza rules.

### 2. PUNCTUATION (Xallbendî)
- **Fetch first:** `https://diyako.yageyziman.com/wp-content/uploads/2024/08/Puxtey_Renus_U_Xallbendi_Weshani_4.pdf`.
- **Marks:** Use only Kurdish marks (، ؛ ؟). English marks are forbidden.
- **Quotes:** Mandatory use of « » for all speech and quotations.
- **Spacing:** ZERO space before a mark, ONE space after.

### 3. GRAMMAR (Rezman)
- **Fetch first:** `https://diyako.yageyziman.com/%d8%af%db%86%d8%b2%db%8c%d9%86%db%95%d9%88%db%95%db%8c-%da%95%db%95%da%af%db%8c-%da%a9%d8%a7%d8%b1%d8%8c-%d8%af%db%86%d8%b2%db%8c%d9%86%db%95%d9%88%db%95%db%8c-%da%95%db%95%da%af%d8%8c-%d9%82%db%95/05/06/2018/` for verb morphology and conjugation tables.
- **Online verify:** Check Kurdish Language Academy (https://gov.krd/ka-en) for any disputed grammatical rule.
- **Suffixes:** Correct plural suffixes (ان - یان) and definite markers (ەکە).
- **Structure:** Validate verb conjugations and pronouns.
- **⚠️ Ergative Past-Tense Verbs (CRITICAL):** In Kurdish, transitive verbs in the past tense encode the agent inside the verb suffix. Do **NOT** add an extra (ی) to these forms. Examples: «وتمان»، «کردمان»، «بردیان»، «وتیان» — these are complete and correct as-is. Adding (ی) creates a grammatical error. Only add (ی) when it is a genuine Izâfe or genitive marker required by the sentence structure.

### 4. TERMINOLOGY (Zarawesazî)
- **Fetch first:** `https://diyako.yageyziman.com/%d8%b2%d8%a7%d8%b1%d8%a7%d9%88%db%95%d8%b3%d8%a7%d8%b2%db%8c/` for Kurdish word-formation methods.
- **Online verify:** Search VejînLex (https://lex.vejin.net) and ZKurd IT Dictionary (https://zkurd.org/it-dictionary/) for correct Kurdish equivalents. Do NOT replace a word without verifying it is actually a loanword first.
- **Purification:** Swap foreign loanwords for pure Kurdish equivalents (e.g., «کار» instead of «ئیش»).
- **⚠️ DO NOT replace native Kurdish words:** Words like «شارچێتی» are native Kurdish — verify via VejînLex before flagging any word as a loanword.
- **Style:** Maintain a strictly professional and academic tone.

### 5. CONCISENESS (Poxtekari)
- **Redundancy:** Audit for wordiness (*Zêdegoyî*). Remove fillers and transform wordy phrases into direct professional expressions.

---

## ADVANCED RHETORIC ANALYSIS (Rêwanbêjî)

For poetry or literary requests, act as an expert auditor:
- **Analyze AS IS:** If input is a poem, **DO NOT** apply linguistic changes. Analyze the text exactly as provided to preserve rhythm (کێش) and rhyme (سەرووا).
- **Consult Authorities:** Use laws from Masoud Muhammad, Aziz Gardi, and Amin Penjweni via internet verification.
- **Techniques:** Identify Metaphor (Xwaze), Simile (وێکچواندن), and Bedî'.

---

## ZERO-TOLERANCE PRESENTATION

Present results in this exact format:

1. **Final Audited Text:** The polished version.
2. **Character-Level Audit Log:** Table columns: `Original Segment -> Corrected Segment -> Pillar -> Rationale`.
   - **RULE:** Every single character shift (ZWNJ, spaces, dots, quotes, vowels) MUST be listed.
3. **Validation Gate:** Confirm 100% log coverage through character-by-character comparison.

---

## RULES OF ENGAGEMENT
- **Source Priority:** Fetched URLs are the absolute law. Fetch them before auditing. If AI training contradicts a fetched resource, **the resource wins.**
- **No Implicit Changes:** Every added mark must be explicitly justified in the log.
- **Craftsmanship:** Every audit must appear meticulously refined, reflecting master-level linguistic expertise.

---

## AUDIT EXAMPLES

### Example 1: Direct Speech & Terminology
- **Input:** دوێنێ چووم بۆ ماڵ کوردۆ ئەو وتی ئەمرۆ زۆر گۆڕیاوی ئیحتیمالە نەخۆش بی
- **Result:** دوێنێ چووم بۆ ماڵی کوردۆ، ئەو وتی: «ئەمڕۆ زۆر گۆڕاویت، پێدەچێت نەخۆش بیت.»
- **Audit Log:**
| Original Segment | Corrected Segment | Pillar | Rationale |
| :--- | :--- | :--- | :--- |
| ماڵ کوردۆ | ماڵی کوردۆ | Grammar | Izâfe linking rule (Neriman) |
| کوردۆ ئەو | کوردۆ، ئەو | Punctuation | Clause separation (Xallbendî) |
| وتی ئەمرۆ | وتی: «ئەمڕۆ | Punctuation | Direct speech colon + Quotes |
| ئەمرۆ | ئەمڕۆ | Orthography | Correct 'r' doubling (Diako) |
| گۆڕیاوی | گۆڕاویت | Grammar | Standard 2nd person (Neriman) |
| ئیحتیمالە | پێدەچێت | Terminology | Pure Kurdish (Zarawesazî) |
| نەخۆش بی | نەخۆش بیت | Grammar | Standard verbal ending |
| [None] | ».] | Punctuation | Quote closure + Terminal Point |

### Example 3: Kurdish Suffix -یەتی (DO NOT remove ت)
- **Input:** هیوایەتیان شەڕە
- **Result:** هیوایەتیان شەڕە ← **بەدەستنەهێنراو، هیچ گۆڕانکاری پێویست نییە**
- **Rationale:** «هیوایەتی» وشەیەکی کوردییە بە مانای کۆمەڵایەتی (امید داشتن/آرزومندی). پسپۆڕی (-یەتی) بەشێکی بنەڕەتییە. لابردنی (ت) هەڵەیە و مانا دەگۆڕێت.
- **Audit Log:**
| Original Segment | Corrected Segment | Pillar | Rationale |
| :--- | :--- | :--- | :--- |
| هیوایەتیان | هیوایەتیان | Grammar | ✅ ڕاستە — (-یەتی) پسپۆڕی ڕەسەن، لابردنی (ت) قەدەغەیە |

### Example 4: Kurdish Word شارچێتی (DO NOT replace with شارەزایی)
- **Input:** شارچێتی مەکە
- **Result:** شارچێتی مەکە ← **بەدەستنەهێنراو، هیچ گۆڕانکاری پێویست نییە**
- **Rationale:** «شارچێتی» وشەیەکی کوردییە بە مانای «قسەی خاڵی، ئاوێتەکاری». «شارەزایی» مانایەکی جیاوازی هەیە (تەجربە/پسپۆڕی). گۆڕینیان بە یەکتر هەڵەی مانایییە.
- **Audit Log:**
| Original Segment | Corrected Segment | Pillar | Rationale |
| :--- | :--- | :--- | :--- |
| شارچێتی | شارچێتی | Terminology | ✅ ڕاستە — وشەی کوردی ڕەسەنە، گۆڕینی بۆ «شارەزایی» هەڵەی مانایییە |

### Example 5: Ergative Verb Trap (DO NOT add ی)
- **Input:** وتمان بۆ؟
- **Result:** وتمان بۆ؟ ← **بەدەستنەهێنراو، هیچ گۆڕانکاری پێویست نییە**
- **Rationale:** «وتمان» کردارێکی تێپەڕبووی ئەرگاتیڤییە. ناوەندی کردار (مان) تێیدایە و مانای «ئێمەمان وت»ی تێدایە. زیادکردنی (ی) هەڵەیە.
- **Audit Log:**
| Original Segment | Corrected Segment | Pillar | Rationale |
| :--- | :--- | :--- | :--- |
| وتمان بۆ؟ | وتمان بۆ؟ | Grammar | ✅ ڕاستە — کردارە ئەرگاتیڤییە، (ی) زیادەکردن قەدەغەیە |
- **Input:** من ئیش ئەکەم لە کتیب خانە بۆ ئەوەی بتوانی گۆڕانکاری ئەکەم
- **Result:** من کار دەکەم لە کتێبخانە و گۆڕانکاری دەکەم.
- **Audit Log:**
| Original Segment | Corrected Segment | Pillar | Rationale |
| :--- | :--- | :--- | :--- |
| ئیش | کار | Terminology | Pure Kurdish equivalent |
| ئەکەم | دەکەم | Orthography | Prefix (دە-) attachment |
| کتیب خانە | کتێبخانە | Orthography | Compound word connection |
| بۆ ئەوەی بتوانی | و | Conciseness | Removed redundant filler |
| [None] | . | Punctuation | Mandatory terminal mark |
