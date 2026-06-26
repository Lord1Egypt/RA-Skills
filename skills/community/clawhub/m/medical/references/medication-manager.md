# Medication Manager

## Adding New Medication

### Required Information
1. **Medication name** (generic or brand)
2. **Dosage** (e.g., "10mg", "1 tablet")
3. **Frequency** (e.g., "once daily", "twice daily", "every 8 hours")

### Optional Information
- Prescribing doctor
- Start date
- End date (for short-term medications)
- Instructions (with food, empty stomach, etc.)
- Refill information
- Purpose/condition being treated

### Data Structure
```json
{
  "medications": [
    {
      "id": "uuid",
      "name": "Lisinopril",
      "dosage": "10mg",
      "frequency": "once daily",
      "time_of_day": ["morning"],
      "with_food": true,
      "prescribing_doctor": "Dr. Smith",
      "start_date": "2024-03-01",
      "end_date": null,
      "ongoing": true,
      "purpose": "hypertension",
      "refill_date": "2024-04-01",
      "quantity_remaining": 30,
      "notes": "Take with breakfast"
    }
  ]
}
```

### Script Usage
```bash
python scripts/add_medication.py \
  --name "Lisinopril" \
  --dosage "10mg" \
  --frequency "once daily" \
  --time "morning" \
  --with-food \
  --purpose "hypertension"
```

## Medication List Retrieval

### Script
```bash
python scripts/list_medications.py
# Options:
#   --current-only    # Only show active medications
#   --format table    # Table format
#   --format json     # JSON format
```

### Output Example
```
Current Medications (3):
┌────────────────┬─────────┬──────────────┬─────────────┐
│ Medication     │ Dosage  │ Frequency    │ Time        │
├────────────────┼─────────┼──────────────┼─────────────┤
│ Lisinopril     │ 10mg    │ Once daily   │ Morning     │
│ Metformin      │ 500mg   │ Twice daily  │ With meals  │
│ Atorvastatin   │ 20mg    │ Once daily   │ Evening     │
└────────────────┴─────────┴──────────────┴─────────────┘
```

## Interaction Checking

### Important Note
Interaction checking is for **information only**. Always verify with doctor or pharmacist.

### Script
```bash
python scripts/check_interactions.py --new "Medication Name"
# Or check specific pair:
python scripts/check_interactions.py --drug1 "Warfarin" --drug2 "Aspirin"
```

### Common Interaction Categories
- **Blood thinners** + NSAIDs (increased bleeding risk)
- **Statins** + Grapefruit (increased side effects)
- **MAOIs** + Tyramine-rich foods (hypertensive crisis)
- **Warfarin** + Many drugs (affected INR)

### Output Format
```
Interaction Check: [New Medication]

Current Medications Flagged:
• [Medication 1] - [Interaction level: minor/moderate/major]
  [Brief explanation]
  Action: Consult doctor/pharmacist

• [Medication 2] - [Interaction level]
  [Brief explanation]
  Action: [Specific recommendation]

⚠️  ALWAYS verify with your doctor or pharmacist before making changes.
```

## Reminder System

### How It Works
- Store medication schedule in JSON
- Agent reads schedule during daily check-ins
- Suggest reminders based on user's timezone and schedule

### Reminder Types
1. **Daily medication reminders** - At specified times
2. **Refill alerts** - 7 days before estimated run-out
3. **End-of-course alerts** - For antibiotics, prednisone tapers, etc.

### Example Reminder Logic
```python
# Check if medication due
def check_medication_due(medication, current_time):
    if medication['time_of_day'] == 'morning' and current_time.hour == 8:
        return f"Reminder: Take {medication['name']} {medication['dosage']}"
    # ... other times
```

## Safety Boundaries

### NEVER
- Suggest stopping a prescribed medication
- Suggest changing dosage without doctor approval
- Interpret side effects as "normal" or "not serious"
- Recommend OTC medications without checking interactions

### ALWAYS
- Recommend consulting doctor for side effects
- Flag when user mentions stopping medication
- Remind about refill dates
- Suggest pharmacist consultation for interaction questions
