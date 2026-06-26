# Personal Medical History

## Data Structure

```json
{
  "medical_history": {
    "personal_info": {
      "full_name": "",
      "date_of_birth": "",
      "blood_type": "",
      "organ_donor": false
    },
    "conditions": [
      {
        "condition": "Hypertension",
        "diagnosed_date": "2020-03-15",
        "status": "managed",
        "treating_physician": "Dr. Smith",
        "notes": "Well controlled with medication"
      }
    ],
    "surgeries": [
      {
        "procedure": "Appendectomy",
        "date": "2015-06-10",
        "surgeon": "Dr. Johnson",
        "hospital": "General Hospital",
        "outcome": "uneventful recovery",
        "complications": null
      }
    ],
    "hospitalizations": [
      {
        "reason": "Pneumonia",
        "date": "2018-11-20",
        "duration_days": 5,
        "hospital": "City Medical Center"
      }
    ],
    "allergies": {
      "medications": [
        {"allergen": "Penicillin", "reaction": "Rash, hives", "severity": "moderate"}
      ],
      "foods": [],
      "environmental": []
    },
    "immunizations": [
      {"vaccine": "Tetanus", "date": "2020-05-10", "next_due": "2030-05-10"}
    ],
    "family_history": {
      "heart_disease": ["father", "paternal grandfather"],
      "diabetes": ["mother"],
      "cancer": []
    },
    "physicians": [
      {
        "name": "Dr. Smith",
        "specialty": "Internal Medicine",
        "phone": "555-0100",
        "address": "123 Medical Plaza"
      }
    ]
  }
}
```

## Adding History Records

### Script Usage
```bash
# Add condition
python scripts/add_history_record.py \
  --type condition \
  --name "Type 2 Diabetes" \
  --date "2019-08-15" \
  --physician "Dr. Garcia" \
  --notes "Managed with metformin"

# Add surgery
python scripts/add_history_record.py \
  --type surgery \
  --name "Knee arthroscopy" \
  --date "2021-03-10" \
  --surgeon "Dr. Lee"

# Add allergy
python scripts/add_history_record.py \
  --type allergy \
  --allergen "Sulfa drugs" \
  --reaction "Severe rash" \
  --severity "severe"

# Add immunization
python scripts/add_history_record.py \
  --type immunization \
  --vaccine "COVID-19" \
  --date "2023-09-15" \
  --next-due "2024-09-15"
```

## Retrieving Medical History

### Complete History
```bash
python scripts/get_medical_history.py
# Options:
#   --format summary   # One-page summary
#   --format detailed  # Full details
#   --format json      # Raw JSON
```

### Filtered Views
```bash
# Get only conditions
python scripts/get_medical_history.py --filter conditions

# Get only allergies
python scripts/get_medical_history.py --filter allergies

# Get surgeries only
python scripts/get_medical_history.py --filter surgeries
```

## Use Cases

### 1. Filling Out Medical Forms
When user needs to complete intake forms:
```
"I need to fill out a new patient form"
→ Retrieve medical history
→ Present in form-friendly format
→ Highlight allergies and current medications
```

### 2. New Doctor Consultation
```
"I'm seeing a new cardiologist"
→ Filter history for cardiac-related items
→ Include family history of heart disease
→ List all current medications
```

### 3. Emergency Situations
Quick access to critical information:
- Allergies (especially medication allergies)
- Current conditions
- Blood type (if known)
- Emergency contacts

## History Summary Format

### For New Patient Forms
```
MEDICAL HISTORY SUMMARY
Generated: [Date]

CHRONIC CONDITIONS:
• [Condition] - diagnosed [Date], status: [managed/active/etc]

PREVIOUS SURGERIES:
• [Procedure] - [Date], [Surgeon/Hospital]

HOSPITALIZATIONS:
• [Reason] - [Date], [Hospital], [Duration]

ALLERGIES:
Medications: [List with reactions]
Foods: [List]
Environmental: [List]

CURRENT MEDICATIONS:
[Separate medication list]

FAMILY HISTORY:
[Relevant family conditions]

IMMUNIZATIONS (Recent):
[List with dates]
```
