# Metric Catalog - Pregnancy Tracking

Use this catalog to keep logs consistent and clinically readable.

## Core Metrics (default)

| Metric | Format | Unit | Frequency | Notes |
|--------|--------|------|-----------|-------|
| Sleep | number | hours | daily | total sleep in last 24h |
| Hydration | number | cups or liters | daily | keep one unit system |
| Energy | scale | 1-5 | daily | subjective but trendable |
| Mood | scale | 1-5 | daily | one value per day |

## Clinical Metrics (conditional)

| Metric | Format | Unit | Frequency | Required Context |
|--------|--------|------|-----------|------------------|
| Blood pressure | systolic/diastolic | mmHg | once or twice daily | seated rest, repeat if elevated |
| Glucose | number | mg/dL or mmol/L | per care plan | fasting or post-meal tag |
| Temperature | number | deg F or deg C | as needed | fever check context |
| Weight | number | lb or kg | weekly | same time and scale conditions |

## Symptom Event Fields

Always capture:
- symptom name
- severity 1-10
- start time
- duration
- related context
- action taken

## Fetal and Contraction Fields

When user is tracking fetal movement or contractions:
- baseline movement pattern
- current change vs baseline
- contraction interval and duration
- associated warning symptoms

## Data Normalization Rules

- Keep one unit system per metric type.
- Do not mix local timezone and UTC in the same log.
- Mark estimated values as estimated.
- Mark device errors separately from observed values.
