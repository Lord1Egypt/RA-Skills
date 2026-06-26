# Frequently Asked Questions (FAQ)

## General Questions

### What is Intelligent Triage and Symptom Analysis?
An AI-powered medical triage tool that analyzes symptoms and provides urgency recommendations based on established clinical triage systems (ESI and Manchester Triage System).

### Is it free to use?
Yes! Every new user gets **10 free calls** with no credit card required. After that, it's only $0.001 per call.

### Do I need an API key?
- **For the first 10 calls**: No API key needed!
- **After free trial**: Yes, you'll need a SkillPay API key

### Is this a replacement for a doctor?
**No!** This tool provides preliminary assessment only. Always consult qualified healthcare providers for medical decisions.

## Usage Questions

### How accurate is the triage?
The system is designed to:
- Detect red flag symptoms with ≥95% sensitivity
- Provide appropriate triage levels with ≥90% accuracy
- Never miss life-threatening conditions

### What symptoms are supported?
650+ symptoms across 11 body systems:
- Cardiovascular, Respiratory, Gastrointestinal
- Neurological, Musculoskeletal, Dermatological
- Genitourinary, Endocrine, Hematological
- Immunological, Psychiatric

### Can I use this for emergency situations?
For life-threatening emergencies, **call emergency services immediately**. This tool is for:
- Initial assessment while waiting for care
- Telemedicine pre-screening
- Non-urgent symptom evaluation

### How should I describe symptoms?
Be specific and include:
- What the symptom is
- When it started
- Severity (mild/moderate/severe)
- Any triggers or relieving factors

Example: "Severe chest pain started 30 minutes ago, worse with breathing"

## Technical Questions

### What data is stored?
Only **free trial usage counts** are stored locally:
- User ID (hashed)
- Number of calls used
- Timestamps

**No medical data is ever stored or transmitted.**

### Is my data secure?
Yes! See our [Security Policy](SECURITY.md) for details. Key points:
- All symptom analysis happens locally
- No PHI is transmitted over the network
- All code is open source and auditable

### What are the system requirements?
- Python 3.8+
- No external dependencies
- Works completely offline

### Can I integrate this into my healthcare app?
Yes, but please:
- Include appropriate disclaimers
- Ensure compliance with healthcare regulations
- Consider liability implications

## Triage Questions

### What are the triage levels?
| Level | Name | Response Time |
|-------|------|---------------|
| 1 | Resuscitation | Immediate |
| 2 | Emergent | <15 min |
| 3 | Urgent | <30 min |
| 4 | Less Urgent | <60 min |
| 5 | Non-urgent | >60 min |

### What are red flag symptoms?
Life-threatening symptoms that trigger immediate escalation:
- Chest pain, severe bleeding
- Difficulty breathing, choking
- Loss of consciousness, seizures
- Severe trauma, signs of shock

### Why did I get a different triage level than expected?
The system considers:
- Symptom severity
- Patient age (elderly/children prioritized)
- Vital signs (if provided)
- Red flag combinations

### Can I provide vital signs?
Yes, and it improves accuracy:
```python
analyze_symptoms(
    symptoms="chest pain",
    vital_signs={"bp": "160/95", "hr": 110, "temp": 38.5}
)
```

## Billing Questions

### How much does it cost?
- **First 10 calls**: Free
- **After trial**: $0.001 USDT per call

### What payment methods are accepted?
Payments are processed via SkillPay using BNB Chain USDT.

### How do I check my balance?
```python
result = analyze_symptoms(...)
print(f"Balance: {result.get('balance')}")
```

### What happens if I run out of balance?
You'll receive a payment URL to top up your account.

## Troubleshooting

### "User ID is required" error
You must provide a user_id parameter:
```python
analyze_symptoms(symptoms="...", user_id="any_unique_string")
```

### No symptoms detected
Try to be more descriptive:
```python
# ✅ Better
"Severe headache with nausea, started 2 hours ago"

# ❌ Too vague
"I don't feel well"
```

### Permission denied errors
Create the required directory:
```bash
mkdir -p ~/.openclaw/skill_trial
chmod 755 ~/.openclaw
```

## Compliance Questions

### Is this FDA approved?
This tool is for educational and preliminary assessment purposes. It is not a medical device and has not been submitted to the FDA.

### Can healthcare providers use this?
Yes, as a decision support tool. However:
- Clinical judgment should always prevail
- Providers are responsible for final decisions
- Document appropriately in patient records

### Is this HIPAA compliant?
The tool is designed with HIPAA safeguards:
- No persistent PHI storage
- Local processing
- No data transmission

**However**, you are responsible for ensuring your specific use case complies with HIPAA and other applicable regulations.

## Getting Help

### Where can I get support?
- 📧 Email: support@openclaw.dev
- 💬 Discord: [Join our community](https://discord.gg/openclaw)
- 🐛 GitHub Issues: [Report bugs](https://github.com/openclaw/skills/issues)

### How do I report a bug?
Please include:
1. Symptom description
2. Expected vs actual triage level
3. Any vital signs provided

### Can I request features?
Yes! Please open a feature request on GitHub.

---

**Important**: This tool is for preliminary assessment only and does not replace professional medical diagnosis. Always consult qualified healthcare providers for medical decisions.
