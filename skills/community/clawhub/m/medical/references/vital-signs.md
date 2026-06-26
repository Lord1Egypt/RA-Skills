# Vital Signs & Chronic Condition Monitoring

## Supported Vital Signs

| Vital Sign | Units | Normal Range* | Frequency |
|------------|-------|---------------|-----------|
| Blood Pressure | mmHg | <120/80 | Daily or per doctor |
| Heart Rate | bpm | 60-100 | As needed |
| Blood Glucose | mg/dL | 70-140 (fasting) | Per diabetic protocol |
| Weight | lbs/kg | - | Weekly |
| Temperature | °F/°C | 97-99°F | When ill |
| Oxygen Saturation | % | 95-100% | As prescribed |
| Sleep | hours | 7-9 | Daily |
| Pain Level | 0-10 | 0 | As experienced |

*Normal ranges vary by individual. Follow your doctor's targets.

## Data Structure

```json
{
  "vitals": {
    "blood_pressure": [
      {
        "date": "2024-03-01T08:00:00",
        "systolic": 128,
        "diastolic": 82,
        "position": "sitting",
        "arm": "left",
        "notes": "Morning reading"
      }
    ],
    "blood_glucose": [
      {
        "date": "2024-03-01T07:30:00",
        "value": 105,
        "context": "fasting",
        "notes": "Before breakfast"
      }
    ],
    "weight": [
      {
        "date": "2024-03-01",
        "value": 165,
        "unit": "lbs"
      }
    ],
    "heart_rate": [
      {
        "date": "2024-03-01T08:00:00",
        "value": 72,
        "context": "resting"
      }
    ],
    "pain": [
      {
        "date": "2024-03-01T14:00:00",
        "level": 4,
        "location": "lower back",
        "quality": "aching"
      }
    ]
  },
  "targets": {
    "blood_pressure": {"systolic_max": 130, "diastolic_max": 85},
    "blood_glucose": {"fasting_max": 130, "post_meal_max": 180},
    "weight": {"target": 160, "unit": "lbs"}
  }
}
```

## Logging Vitals

### Script Usage
```bash
# Blood pressure
python scripts/add_vital.py \
  --type bp \
  --systolic 128 \
  --diastolic 82 \
  --notes "Morning, before meds"

# Blood glucose
python scripts/add_vital.py \
  --type glucose \
  --value 105 \
  --context "fasting"

# Weight
python scripts/add_vital.py \
  --type weight \
  --value 165 \
  --unit lbs

# Pain
python scripts/add_vital.py \
  --type pain \
  --level 4 \
  --location "lower back"
```

## Trend Analysis

### Weekly Averages
```bash
python scripts/get_vital_trends.py \
  --type bp \
  --period week

# Output:
# Week of Mar 1-7:
#   Average: 126/80 mmHg
#   Readings: 7
#   Above target: 2 days
```

### Monthly Trends
```bash
python scripts/get_vital_trends.py \
  --type weight \
  --period month \
  --chart
```

### Trend Report Format
```
VITAL SIGNS TREND REPORT
Period: [Start] to [End]

BLOOD PRESSURE:
• Average: [XXX/XX] mmHg ([N] readings)
• Range: [min/max]
• Trend: [improving/stable/worsening]
• Days above target: [N]

BLOOD GLUCOSE:
• Average fasting: [XXX] mg/dL
• Average post-meal: [XXX] mg/dL
• Trend: [improving/stable/worsening]

WEIGHT:
• Start: [XXX] lbs
• End: [XXX] lbs
• Change: [+/-X.X] lbs
• Trend: [gaining/losing/stable]
```

## Alert System

### Setting Targets
```bash
python scripts/set_vital_targets.py \
  --type bp \
  --systolic-max 130 \
  --diastolic-max 85
```

### Alert Triggers
When vital is logged outside target range:
1. Note the deviation
2. Track frequency of deviations
3. Suggest discussing with doctor if pattern emerges
4. Never suggest medication changes

### Example Alert
```
Blood pressure logged: 145/92 mmHg
Your target: <130/85 mmHg

This reading is above your target range.

If this is:
• A single reading - monitor and recheck later
• Multiple readings this week - consider checking with your doctor
• Accompanied by symptoms (headache, dizziness) - contact doctor today

Track: When did you take this reading? Any factors (stress, missed medication, etc.)?
```

## Chronic Condition Protocols

### Hypertension Monitoring
- Daily BP at same time
- Track medication adherence
- Note salt intake if relevant
- Weekly averages for doctor visits

### Diabetes Monitoring
- Per doctor's protocol (fasting, pre/post meal)
- Track medication/insulin timing
- Note carbohydrate intake if helpful
- A1C tracking (every 3 months)

### Weight Management
- Weekly weigh-ins, same day/time
- Track diet/exercise alongside
- Focus on trends, not single readings
- Celebrate consistency over perfection

### Chronic Pain
- Pain level (0-10) when experienced
- Location and quality
- Triggers and relief measures
- Impact on activities
- Medication effectiveness tracking
