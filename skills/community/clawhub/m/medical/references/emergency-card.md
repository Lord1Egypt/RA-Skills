# Emergency Health Summary

## Purpose

One-page summary of critical health information for emergency situations. Designed to be:
- Screenshot and saved to phone lock screen
- Printed and kept in wallet
- Accessible to paramedics and emergency room staff

## Data Included

```json
{
  "emergency_card": {
    "full_name": "John Michael Doe",
    "date_of_birth": "1985-06-15",
    "age": 38,
    "blood_type": "O+",
    "organ_donor": true,
    "critical_allergies": [
      {"allergen": "Penicillin", "reaction": "Anaphylaxis"},
      {"allergen": "Sulfa drugs", "reaction": "Severe rash"}
    ],
    "medical_conditions": [
      "Hypertension",
      "Type 2 Diabetes"
    ],
    "current_medications": [
      {"name": "Lisinopril", "dose": "10mg daily"},
      {"name": "Metformin", "dose": "500mg twice daily"}
    ],
    "emergency_contacts": [
      {"name": "Jane Doe", "relationship": "spouse", "phone": "555-0123"}
    ],
    "primary_physician": {
      "name": "Dr. Sarah Smith",
      "phone": "555-0100"
    },
    "insurance": {
      "provider": "Blue Cross",
      "policy_number": "XXX123456",
      "group_number": "GRP789"
    }
  }
}
```

## Generating Emergency Card

### Script
```bash
python scripts/generate_emergency_card.py
# Options:
#   --format text      # Plain text (for printing)
#   --format phone     # Optimized for phone lock screen
#   --include-insurance # Add insurance info
```

## Output Formats

### Phone Lock Screen Format
```
╔════════════════════════════════════════╗
║  ⚠️ EMERGENCY HEALTH INFO ⚠️           ║
╠════════════════════════════════════════╣
║  John Doe  •  DOB: 6/15/1985           ║
║  Blood Type: O+  •  Organ Donor: Y     ║
╠════════════════════════════════════════╣
║  🚨 ALLERGIES: Penicillin = Anaphylaxis║
║                Sulfa = Severe rash     ║
╠════════════════════════════════════════╣
║  CONDITIONS: Hypertension, Diabetes    ║
╠════════════════════════════════════════╣
║  MEDICATIONS:                          ║
║  • Lisinopril 10mg daily               ║
║  • Metformin 500mg 2x daily            ║
╠════════════════════════════════════════╣
║  ICE: Jane Doe (spouse) 555-0123       ║
║  Dr: Sarah Smith 555-0100              ║
╚════════════════════════════════════════╝
```

### Wallet Card Format (Business Card Size)
```
┌──────────────────────────────────────┐
│ EMERGENCY INFO                       │
│ John Doe • 6/15/1985 • O+            │
│                                      │
│ ALLERGIES: Penicillin (anaphylaxis)  │
│            Sulfa (severe)            │
│                                      │
│ CONDITIONS: HTN, Diabetes            │
│                                      │
│ MEDS: Lisinopril 10mg, Metformin     │
│       500mg BID                      │
│                                      │
│ ICE: Jane 555-0123                   │
│ Dr: Smith 555-0100                   │
└──────────────────────────────────────┘
```

## Updating Emergency Card

Emergency card should be regenerated when:
- New medication added
- New allergy discovered
- Change in medical conditions
- Emergency contact changes
- Insurance changes

```
User: "I have a new allergy to latex"
→ Add to allergies
→ Prompt: "Update emergency card? (Y/n)"
→ If yes: regenerate and remind to replace saved/printed copies
```

## Security Considerations

### Information Balance
Include enough to save your life, not enough for identity theft:

**Include:**
- Name, DOB, blood type
- Critical allergies (can be life-saving)
- Current medications
- Major conditions
- Emergency contacts

**Exclude from public card:**
- Full insurance policy numbers
- Social security number
- Full address
- Detailed medical history

### Optional Password Protection
For sensitive medications (psychiatric, HIV, etc.):
```bash
python scripts/generate_emergency_card.py \
  --sensitive-redacted \
  --password-protected

# Creates two versions:
# 1. Public: Allergies, conditions, non-sensitive meds
# 2. Protected: Full medication list with password
```

## Emergency Protocol for Agent

If user asks for emergency card during apparent emergency:
1. **Generate card immediately**
2. **Simultaneously ask**: "Are you experiencing a medical emergency right now?"
3. If yes emergency: "Please call 911. I'm generating your health info for first responders."
4. Present card in most accessible format

## Usage Reminders

When generating card, remind user:
- Save screenshot to phone lock screen
- Print wallet-sized version
- Review and update every 6 months or when health changes
- Share with close family members
- Keep one copy easily accessible at home
