# Symptom Tracker & Appointment Preparation

## Symptom Logging Workflow

### When to Use
User mentions symptoms: "I have headache", "My knee hurts", "I've been feeling dizzy"

### Data Structure
```json
{
  "symptoms": [
    {
      "id": "uuid",
      "description": "headache",
      "severity": 6,
      "severity_scale": "1-10",
      "location": "forehead",
      "quality": "throbbing",
      "triggers": ["stress", "lack of sleep"],
      "relief_factors": ["rest", "dark room"],
      "start_date": "2024-03-01",
      "end_date": null,
      "ongoing": true,
      "notes": "Worse in mornings"
    }
  ]
}
```

### Required Information
1. **What** - Symptom description
2. **Severity** - 1-10 scale (ask if not provided)
3. **When** - Start date/time
4. **Context** - Triggers, what makes it better/worse

### Optional Information
- Location (for localized symptoms)
- Quality (throbbing, sharp, dull, etc.)
- Associated symptoms
- Impact on daily activities

### Script Usage
```bash
python scripts/add_symptom.py \
  --description "headache" \
  --severity 6 \
  --location "forehead" \
  --triggers "stress,lack_of_sleep" \
  --notes "Worse in mornings"
```

## Appointment Preparation Workflow

### Trigger Phrases
- "Prep me for my appointment"
- "I'm seeing the doctor tomorrow"
- "What should I tell my cardiologist?"

### Preparation Checklist
1. **Symptom Timeline** (last 30 days)
   - Current symptoms with severity
   - Duration of each symptom
   - Changes over time

2. **Medication Review**
   - Current medications and dosages
   - Recent changes to medications
   - Side effects experienced

3. **Medical History Relevant to Visit**
   - Conditions related to specialty
   - Previous procedures
   - Family history if relevant

4. **Questions to Ask**
   - Suggest 3-5 questions based on symptoms
   - User can add their own

5. **Recording Space**
   - Prepare template for doctor's recommendations
   - Follow-up instructions
   - New prescriptions

### Output Format
```
Appointment Brief for [Doctor/Specialty] on [Date]

Current Symptoms (Last 30 Days):
• [Symptom] - [Severity]/10, started [Date]
• [Symptom] - [Severity]/10, started [Date]

Current Medications:
• [Medication] [Dosage] - [Frequency]

Relevant Medical History:
• [Condition] - diagnosed [Date]
• [Procedure] - [Date]

Questions to Ask:
1. [Generated question based on symptoms]
2. [Generated question about medication]
3. [User-added question]

Notes from Appointment:
[Space for recording doctor's recommendations]

Follow-up:
[Space for next steps]
```

## Safety Check

Before logging symptoms or prepping appointments, check for emergency red flags:
- Chest pain or pressure
- Difficulty breathing
- Severe bleeding
- Sudden severe headache ("worst ever")
- Loss of consciousness
- Suicidal thoughts

**If ANY present**: Immediately direct to emergency services, do not proceed with tracking.
