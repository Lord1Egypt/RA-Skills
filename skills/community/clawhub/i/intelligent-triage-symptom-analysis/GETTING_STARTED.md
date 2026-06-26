# 🚀 Getting Started

Get up and running with Intelligent Triage and Symptom Analysis in 5 minutes!

## ⚡ Quick Start (Zero Configuration)

The fastest way to try the skill - no setup required!

### Step 1: Run the Demo
```bash
cd /home/node/.openclaw/workspace/skills/intelligent-triage-symptom-analysis
python demo.py
```

This will:
- Analyze 4 sample symptom scenarios
- Show triage levels and recommendations
- Demonstrate red flag detection

### Step 2: Try with Your Own Symptoms
```bash
python demo.py --symptoms "头痛，发烧，持续3天" --age 30 --gender female
```

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Install Dependencies
```bash
# No external dependencies required!
# The skill uses only Python standard library
```

## 🎯 Basic Usage

### Using the Demo Script
```bash
# Run with built-in examples
python demo.py

# Run with custom symptoms
python demo.py --symptoms "胸痛，呼吸困难" --age 65 --gender male

# Save output to file
python demo.py --symptoms "腹痛，恶心" --output triage.json
```

### Using the Python API
```python
from scripts.triage import analyze_symptoms

# Analyze symptoms (free trial - no API key needed!)
result = analyze_symptoms(
    symptoms="胸痛，呼吸困难，持续30分钟",
    age=65,
    gender="male",
    user_id="user_123"
)

print(f"Triage Level: {result['analysis']['triage']['level']}")
print(f"Urgency: {result['analysis']['triage']['urgency']}")
```

### Using Command Line
```bash
python scripts/triage.py \
  --symptoms "胸痛，呼吸困难" \
  --age 65 \
  --gender male \
  --user-id "user_123"
```

## 🎁 Free Trial

Every new user gets **10 free calls** - no credit card required!

```python
result = analyze_symptoms(
    symptoms="你的症状描述",
    user_id="your_unique_user_id"  # Any string works!
)

# Check remaining free calls
if result.get("trial_mode"):
    print(f"剩余免费次数: {result['trial_remaining']}")
```

## 💳 After Free Trial

When your free trial ends:

1. Get an API key from [skillpay.me](https://skillpay.me)
2. Set environment variable:
   ```bash
   export SKILL_BILLING_API_KEY="your-api-key"
   export SKILL_ID="your-skill-id"
   ```
3. Continue using the skill - only $0.001 per call!

## 📋 Input Parameters

### Required
- **symptoms** (string): Description of symptoms in natural language
- **user_id** (string): Unique identifier for the user

### Optional
- **age** (int): Patient age (affects triage priority)
- **gender** (string): "male", "female", or "other"
- **vital_signs** (dict): Blood pressure, heart rate, temperature
- **duration** (string): How long symptoms have been present

### Example Input
```python
result = analyze_symptoms(
    symptoms="胸痛，呼吸困难，持续30分钟",
    age=65,
    gender="male",
    vital_signs={"bp": "160/95", "hr": 110, "temp": 37.2},
    duration="30 minutes",
    user_id="user_123"
)
```

## 📤 Output Format

The skill returns comprehensive triage analysis:

```json
{
  "analysis": {
    "analysis_id": "TRG_20240306120000",
    "timestamp": "2024-03-06T12:00:00",
    "triage": {
      "level": 2,
      "name": "Emergent",
      "name_cn": "紧急",
      "urgency": "<15 min",
      "color": "Orange"
    },
    "red_flags": [
      {
        "category": "cardiac",
        "symptom": "胸痛",
        "priority": "CRITICAL"
      }
    ],
    "differential_diagnosis": [
      {"condition": "Acute Coronary Syndrome", "probability": 0.25, "urgency": "HIGH"},
      {"condition": "Pulmonary Embolism", "probability": 0.15, "urgency": "HIGH"}
    ],
    "recommendations": [
      "立即前往急诊/Go to emergency department immediately",
      "不要进食或饮水/Do not eat or drink"
    ]
  }
}
```

## 🚨 Triage Levels

| Level | Name | Response Time | Description |
|-------|------|---------------|-------------|
| 1 | Resuscitation | Immediate | Life-threatening |
| 2 | Emergent | <15 min | Potential life threat |
| 3 | Urgent | <30 min | Serious condition |
| 4 | Less Urgent | <60 min | Less acute |
| 5 | Non-urgent | >60 min | Minor condition |

## 🚩 Red Flag Symptoms

The system automatically detects life-threatening symptoms:

### Cardiac
- Chest pain (胸痛)
- Chest tightness (胸闷)
- Palpitations (心悸)
- Shortness of breath (呼吸困难)

### Neurological
- Coma (昏迷)
- Seizure (抽搐)
- Paralysis (偏瘫)
- Severe headache (剧烈头痛)

### Respiratory
- Choking (窒息)
- Wheezing (喘鸣)
- Low oxygen (血氧低)

### Trauma
- Severe bleeding (大出血)
- Severe trauma (严重外伤)
- Head injury (头部外伤)

## 🔧 Troubleshooting

### "User ID is required"
Make sure to provide a user_id parameter:
```python
analyze_symptoms(symptoms="...", user_id="any_unique_id")
```

### No symptoms detected
Try to be more specific in your description:
```python
# ✅ Better
analyze_symptoms(symptoms="剧烈头痛，伴有恶心呕吐，持续2小时", ...)

# ❌ Too vague
analyze_symptoms(symptoms="感觉不舒服", ...)
```

### Permission Denied
If you see permission errors for `~/.openclaw/`:
```bash
mkdir -p ~/.openclaw/skill_trial
chmod 755 ~/.openclaw
```

## ⚠️ Important Disclaimer

**This tool is for preliminary assessment only and does not replace professional medical diagnosis. Always consult qualified healthcare providers for medical decisions.**

## 📚 Next Steps

- Read the [full documentation](SKILL.md)
- Check out [examples](EXAMPLES.md)
- See [FAQ](FAQ.md) for common questions
- Review [security policy](SECURITY.md)

## 💬 Need Help?

- 📧 Email: support@openclaw.dev
- 💬 Discord: [Join our community](https://discord.gg/openclaw)
- 🐛 Issues: [GitHub Issues](https://github.com/openclaw/skills/issues)

---

**Stay Healthy! 🏥**
