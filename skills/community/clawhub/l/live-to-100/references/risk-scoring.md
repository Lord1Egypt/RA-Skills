# Longevity Risk Scoring (0-100)

Use this pragmatic scoring model for coaching prioritization, not diagnosis.

## Formula

- Total score = sum of six sub-scores (0-100)
- Lower is better
- If a field is missing, assign midpoint for that item and mark as provisional

## Sub-scores and weights

## 1) Body composition (0-20)

- BMI:
  - < 18.5 or >= 32: +8
  - 28-31.9: +6
  - 25-27.9: +3
  - 18.5-24.9: +0
- Waist circumference:
  - Male >= 102 cm or Female >= 88 cm: +8
  - Male 94-101 or Female 80-87: +4
  - Below these: +0
- Rapid weight gain (> 5% in 6 months): +4

## 2) Cardiometabolic (0-25)

- Blood pressure:
  - >= 140/90: +10
  - 130-139 or 80-89: +6
  - < 130/80: +0
- Resting heart rate:
  - > 90: +5
  - 75-90: +2
  - < 75: +0
- Glucose/HbA1c:
  - Diabetic range: +6
  - Prediabetic range: +3
  - Normal/unknown: +0 or midpoint if missing
- Lipid abnormality (high LDL/TG or low HDL): +4

## 3) Sleep and recovery (0-15)

- Average sleep:
  - < 6 h: +7
  - 6-6.9 h: +4
  - 7-9 h: +0
- Irregular schedule (> 2 h shift most days): +4
- Frequent insomnia/daytime fatigue: +4

## 4) Activity and sedentary load (0-20)

- Daily steps:
  - < 4000: +8
  - 4000-6999: +4
  - >= 7000: +0
- Structured exercise:
  - 0 days/week: +6
  - 1-2 days/week: +3
  - >= 3 days/week: +0
- Sitting time:
  - > 9 h/day: +6
  - 7-9 h/day: +3
  - < 7 h/day: +0

## 5) Habits (0-10)

- Smoking current: +5
- Alcohol heavy/binge pattern: +3
- Late caffeine + frequent late-night eating: +2

## 6) Medical context and family history (0-10)

- Existing chronic disease burden (HTN, diabetes, CVD, CKD, etc.): +5
- Multiple medications with adherence issues: +2
- Strong first-degree family history (early CVD/stroke/diabetes/cancer): +3

## Bands and interpretation

- 0-20: Low current risk, focus on consistency and maintenance
- 21-40: Mild-moderate risk, prioritize 2-3 high-yield changes
- 41-60: Elevated risk, tighten follow-up and consider clinician review
- 61-100: High risk, recommend medical evaluation while running conservative lifestyle plan

## Output requirements

- Show total score and each sub-score.
- Name top 3 drivers increasing risk.
- Give a "4-week score improvement target" (e.g., minus 5 to 10 points).
