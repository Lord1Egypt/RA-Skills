# Member Profile

Create one file per family member: `data/members/{name}.md`

## Template

Copy this template for each family member and fill in the details.

```markdown
# {姓名}

## Basic Info

| Field | Value |
|-------|-------|
| Name | {姓名} |
| Role | 成人 / 儿童 / 老人 |
| Birth Date | YYYY-MM-DD |
| Gender | 男 / 女 |
| Weight | {kg} （儿童必填） |
| Blood Type | A / B / AB / O / 未知 |

## Allergies ⚠️

| Allergen | Reaction | Severity | Notes |
|----------|----------|----------|-------|
| 青霉素 | 皮疹 | 中度 | 2018年发现 |
| {过敏原} | {反应} | 轻/中/重 | {备注} |

> **Important**: If no known allergies, write "无已知过敏"

## Chronic Conditions

| Condition | Diagnosed | Status | Notes |
|-----------|-----------|--------|-------|
| 高血压 | 2020-03 | 控制中 | 每日服药 |
| {疾病} | {date} | 控制中/已治愈/观察中 | {备注} |

> If none, write "无慢性病"

## Current Medications

| Medication | Dose | Frequency | Since | Prescriber |
|------------|------|-----------|-------|------------|
| 氨氯地平 | 5mg | 每日1次 早 | 2020-03 | 张医生 |
| {药名} | {剂量} | {频次} | {date} | {医生} |

> If none, write "当前无长期用药"

## Medication Notes

- {Special instructions, preferences, or warnings}
- e.g., "不吃胶囊，只能吃药片"
- e.g., "怕苦，需要喂药技巧"
- e.g., "乳糖不耐受，注意药品辅料"

## Vaccination History (Optional)

| Vaccine | Date | Notes |
|---------|------|-------|
| 乙肝疫苗（全程） | 2022-01, 2022-03, 2022-06 | 已完成 |
| {疫苗} | {date} | {备注} |

> For children: track vaccination schedule carefully

## Medication History

| Date | Medication | Reason | Duration | Outcome |
|------|-----------|--------|----------|---------|
| YYYY-MM-DD | 阿莫西林 | 扁桃体炎 | 7天 | 痊愈 |
| {date} | {药名} | {原因} | {疗程} | {结果} |

## Emergency Contact

| Role | Name | Phone |
|------|------|-------|
| 本人 | {姓名} | {phone} |
| 紧急联系人 | {姓名} | {phone} |
```

## Minimal Profile (Quick Start)

If the user just wants to get started, this is the **minimum** required info:

```markdown
# {姓名}

| Field | Value |
|-------|-------|
| Name | {姓名} |
| Role | 成人 / 儿童 / 老人 |
| Birth Date | YYYY-MM-DD |
| Weight | {kg} |
| Allergies | {list or "无已知过敏"} |
```

**Why weight matters for children**: Most pediatric dosages are calculated by weight (mg/kg), not age. An incorrect weight leads to an incorrect dose.

**Why allergies matter**: A missed allergy can be fatal. Always confirm before prescribing any medication.

## Role-Specific Fields

### 👶 Children (儿童)
- **Weight** — Required, update every 3-6 months
- **Birth Date** — Required, calculate exact age in months
- **Vaccination History** — Track carefully
- **Growth Notes** — Height, weight tracking (optional)
- **Feeding Notes** — Breastfed, formula, solids, picky eating (optional)

### 👨 Adults (成人)
- **Chronic Conditions** — Important for drug interaction checks
- **Current Medications** — Critical to avoid interactions
- **Lifestyle** — Smoking, drinking, exercise (optional, for drug advice)

### 👴 Elderly (老人)
- **Chronic Conditions** — Very important, polypharmacy risk
- **Current Medications** — List everything, including OTC and supplements
- **Kidney/Liver Function** — Affects drug metabolism
- **Fall Risk** — Relevant for certain medications (sedatives, blood pressure drugs)

## How to Collect

When setting up for the first time, the agent should:

1. **Ask for family members**: "家里有几位成员？分别是谁？（大人/小孩/老人）"
2. **For each member, collect minimum info**:
   - 姓名、角色（大人/小孩/老人）、出生日期、体重
   - **过敏史**：最重要的问题 — "有没有什么药物过敏？"
3. **For children, also ask**:
   - 当前月龄/年龄
   - 疫苗接种情况
   - 近期有没有生病吃药
4. **For adults/elderly, also ask**:
   - 有没有慢性病？（高血压、糖尿病等）
   - 有没有在长期服药？
5. **Create the profile file** and confirm with the user

## Profile Updates

- **Weight**: Update every 3-6 months for children, yearly for adults
- **Allergies**: Update immediately when new allergies are discovered
- **Medications**: Update whenever starting or stopping a medication
- **Chronic conditions**: Update at each medical visit
