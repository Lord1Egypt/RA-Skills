# Data Analysis Dimensions & Algorithm Reference

## Core Analysis Dimensions

### 1. Cycle Regularity Analysis
- Average cycle length (mean_cycle_length)
- Cycle length standard deviation (cycle_length_std) — regularity indicator
- Cycle length trend (3/6-cycle moving average)
- Coefficient of variation (CV) — CV < 0.1 is very regular
- Shortest/longest cycle
- Mean and variance of period duration

### 2. Symptom Pattern Analysis
- Symptom occurrence frequency (occurrence_rate)
- Symptom-to-cycle-phase correlation heatmap
- Symptom severity trends
- Top 5 most frequent symptoms
- New symptom flagging

### 3. Physical Sign Trends
- Basal body temperature curve & biphasic confirmation
- Weight fluctuation correlation with cycle phases
- Sleep quality change patterns
- Exercise performance by cycle phase

### 4. Prediction Engine
- Next period prediction (based on average cycle + recent trends)
- Ovulation estimation (14 days ± 2 days before next predicted period)
- Fertile window
- Prediction confidence interval

### 5. Influencing Factor Correlation
- Temporal correlation between tagged events (travel, stress, illness, etc.) and cycle changes
- Possible attribution for delays/early starts
- Seasonal pattern recognition

## Data Storage Format

Recommended JSON file storage:

```json
{
  "user_profile": {
    "life_stage": "menstruating|pregnant|postpartum|perimenopause|postmenopause|premenarche",
    "age": null,
    "typical_cycle_length": null,
    "typical_period_length": null,
    "conditions": [],
    "medications": [],
    "created_at": "ISO datetime"
  },
  "cycles": [
    {
      "id": "uuid",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD",
      "flow_level": "light|medium|heavy",
      "symptoms": {
        "cramps": {"present": true, "severity": 3},
        "headache": {"present": true, "severity": 2}
      },
      "mood": "irritable|anxious|low|stable|energetic",
      "mood_score": 6,
      "bbt": 36.5,
      "weight": null,
      "notes": "string",
      "events": ["travel", "stress", "illness"],
      "medications_taken": [],
      "exercise": "light|moderate|intense|none"
    }
  ],
  "daily_logs": [
    {
      "date": "YYYY-MM-DD",
      "cycle_day": null,
      "symptoms": {},
      "mood_score": null,
      "bbt": null,
      "weight": null,
      "sleep_hours": null,
      "exercise": null,
      "notes": ""
    }
  ],
  "events": [
    {
      "date": "YYYY-MM-DD",
      "type": "travel|stress|illness|medication_change|lifestyle_change|other",
      "description": "string",
      "severity": 3
    }
  ]
}
```

## Visualization Specification

### Color Palette (Women's Health Theme)
- Primary: Soft Purple #9B7EC4
- Menstrual Red: Soft Coral #E8737A
- Follicular Green: #7EC49B
- Luteal Gold: #C4A87E
- Ovulation Pink: #E89BB4
- Background: Warm White #FAF7F5
- Dark Background: Deep Purple-Gray #1E1B2E
- Text: Dark Gray #2D2A3E
- Accent: Warm Amber #F0A060

### Chart Type Selection
- Cycle trends: Line chart (cycle length over time)
- Symptom distribution: Radar chart (symptom frequency radar)
- Menstrual calendar: Heatmap calendar
- Prediction timeline: Gantt-style chart
- Phase physical signs: Multi-axis line chart
- Influencing factors: Sankey/correlation diagram
- Cycle variability: Box plot
- Mood curve: Area chart

## Recommendation Generation Algorithm

### Trigger Condition Tiers
- Level 1 (Informational): After each entry → cycle phase info + tips
- Level 2 (Pattern Discovery): After 3 cycles → personal pattern insights
- Level 3 (Alert): Anomaly detection → gentle reminder + scientific explanation
- Level 4 (Deep Analysis): After 6 cycles → comprehensive health report

### Recommendation Categories
1. Nutrition
2. Exercise
3. Lifestyle
4. Mental Wellness
5. Medical Referral

### Stress Testing Rules
Each recommendation must pass:
1. Verify data support (is this based on the user's actual data?)
2. Cross-validation (is there medical literature support?)
3. Safety boundary check (could this be harmful?)
4. Personalization score (1-5; rewrite if below 3)
5. Feasibility check (can the user actually do this now?)
