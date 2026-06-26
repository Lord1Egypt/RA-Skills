# Label Compliance Guide (FDA, EU, and Others)

This document summarizes key compliance requirements for product labels (especially food labels) in major regulated markets. It is for reference when generating LMP labels with this skill. **This is not legal advice**; confirm with local regulations and counsel before market use.

---

## Label types (compliant) — 合规标签类型

When the user asks for a compliant-style label, choose the type that best matches the request and generate LMP according to the corresponding section below.

| Type identifier | Name (EN) | Name (中文) | Section |
|----------------|-----------|-------------|---------|
| **fda-nutrition-facts** | US FDA Nutrition Facts | 美国 FDA 营养标签 | §1 |
| **eu-food** | EU Food (1169/2011) | 欧盟食品标签 | §2 |
| **china-gb28050** | China prepackaged nutrition (GB 28050) | 中国预包装食品营养标签 | §3 |
| **uk-fic** | UK food information (UK FIC) | 英国食品信息标签 | §4 |
| **supplement-facts** | US FDA Supplement Facts | 美国膳食补充剂标签 | §5 |
| **other** | General / multi-market | 通用/多市场 | §6 |

---

## 1. US FDA Food Label (Nutrition Facts)

### Legal basis

- **21 CFR Part 101** (food labeling)
- **21 CFR 101.9**: nutrition label format and mandatory declarations (as amended 2016, including Added Sugars)

### Mandatory elements (summary)

| Item | Requirement |
|------|-------------|
| Title | Must be **"Nutrition Facts"** (or prescribed Supplement Facts format where applicable) |
| Serving | **Serving size** + **Servings per container** |
| Calories | **Calories** (bold) + value per serving, in kcal |
| Core nutrients (order) | Total Fat (g) → Saturated Fat (g) → Trans Fat (g) → Cholesterol (mg) → Sodium (mg) → Total Carbohydrate (g) → Dietary Fiber (g) → Total Sugars (g) → **Added Sugars (g)** → Protein (g) |
| % Daily Value | Most of the above must show **% DV** (based on 2,000-calorie diet), right-aligned column |
| Footnote | At least "*Percent Daily Values are based on a 2,000 calorie diet." plus optional second footnote |
| Format / type size | Title, bold entries, minimum type size per CFR (this skill uses minimum 14pt for body text) |

### LMP generation tips for FDA-style nutrition labels

- **Always include**: Serving size, Servings per container, Calories, Total Fat / Saturated / Trans, Cholesterol, Sodium, Total Carbohydrate, Dietary Fiber, Total Sugars, **Added Sugars**, Protein, plus **% Daily Value** column and footnote(s).
- Rounding must follow 101.9 (e.g. &lt;0.5 g may be declared as 0; sodium has specific rules).
- If the label is for layout reference only, note in metadata.description that it "must be completed per 21 CFR 101.9 before use in the US market."

---

## 2. EU Food Label

### Legal basis

- **Regulation (EU) No 1169/2011** (food information to consumers)

### Mandatory elements (summary)

| Item | Requirement |
|------|-------------|
| Name | Legal name or customary name of the food |
| Ingredients | In descending order by weight; **allergens** must be emphasised (e.g. bold, underline) |
| Net quantity | Weight or volume (g/kg or ml/L) |
| Date marking | "Use by" or "Best before" in the prescribed format |
| Storage/use conditions | When necessary |
| Operator | Name and address of the food business operator |
| Country of origin | When required by law |
| Nutrition declaration (if made) | Usually per **100 g or 100 ml**: energy, fat, saturates, carbohydrate, sugars, protein, salt |

### LMP generation tips for EU-style labels

- EU does not require a US-style Nutrition Facts table; if a nutrition declaration is made, format and units must comply with 1169/2011.
- Allergens must be **emphasised** in the ingredients list or in a separate statement (e.g. bold).
- Language: prepacked food sold in a Member State typically requires the official language(s) of that state.

---

## 3. China — Prepackaged food nutrition label (GB 28050)

### Legal basis

- **GB 28050** — National food safety standard: General rules for nutrition labeling of prepackaged foods (食品安全国家标准 预包装食品营养标签通则)

### Mandatory elements (summary)

| Item | Requirement |
|------|-------------|
| Title | **营养成分表** (Nutrition facts table) |
| Core nutrients (per 100 g or 100 ml or per serving) | Energy (kJ/kcal), protein (g), fat (g), carbohydrate (g), sodium (mg or g) |
| NRV% | Voluntary; if declared, use NRV reference values in the standard |
| Format | Table format; units and rounding per GB 28050 |

### LMP generation tips for China GB 28050–style labels

- Use **营养成分表** as the table title; list energy, protein, fat, carbohydrate, sodium.
- Optional: add NRV% column and footnote (e.g. “* NRV%为营养素参考值”).
- Language: use Chinese for labels targeting the China market.
- Add a note in metadata.description that the label "must be verified against GB 28050 before use in China."

---

## 4. UK — Food information (UK FIC, post-Brexit)

### Legal basis

- **UK retained law** from Regulation (EU) No 1169/2011 (UK FIC)

### Mandatory elements (summary)

| Item | Requirement |
|------|-------------|
| Name | Name of the food |
| Ingredients | Descending order by weight; **allergens** must be emphasised |
| Net quantity | Weight or volume (g/kg or ml/L) |
| Date marking | “Use by” or “Best before” in prescribed format |
| Operator | Name and address of the food business operator |
| Country of origin | When required |
| Nutrition declaration (if made) | Per **100 g or 100 ml**: energy, fat, saturates, carbohydrate, sugars, protein, salt |

### LMP generation tips for UK FIC–style labels

- Same structure as EU §2: allergens emphasised, nutrition per 100 g/100 ml when declared.
- Language: English (or as required for the UK market).
- Add a note in metadata.description that the label "must be verified against UK FIC before use."

---

## 5. US FDA Supplement Facts

### Legal basis

- **21 CFR 101.36** (supplement labeling)

### Mandatory elements (summary)

| Item | Requirement |
|------|-------------|
| Title | **"Supplement Facts"** (not "Nutrition Facts") |
| Serving | Serving size + Servings per container |
| Ingredients / dietary ingredients | Listed with amount per serving and % DV where established |
| Other | May include botanicals, vitamins, minerals; format and order per 101.36 |
| Footnote | Similar to Nutrition Facts where applicable |

### LMP generation tips for Supplement Facts–style labels

- Use the title **"Supplement Facts"** and the structure required by 21 CFR 101.36 (serving, list of dietary ingredients with amount and % DV).
- Do not use the same table layout as Nutrition Facts; follow supplement-specific layout and footnote rules.
- Add a note in metadata.description that the label "must be completed per 21 CFR 101.36 before use in the US market."

---

## 6. Other / multi-market

- For generic or multi-market labels, include placeholders or short notes for: FDA (% DV + footnote), EU (allergens + 100 g/100 ml), China (NRV%, 营养成分表). The user should complete and verify against each target regulation.

---

## 7. References (links for verification)

- FDA Nutrition Facts: [21 CFR 101.9](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101/subpart-A/section-101.9)
- FDA Supplement Facts: [21 CFR 101.36](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-B/part-101/subpart-A/section-101.36)
- EU: [Regulation (EU) No 1169/2011](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A32011R1169)
- China: GB 28050 (National food safety standard – nutrition labeling for prepackaged foods)
- UK: UK FIC (retained EU 1169/2011)

---

*For skill and label design reference only; not a substitute for legal or compliance review.*
