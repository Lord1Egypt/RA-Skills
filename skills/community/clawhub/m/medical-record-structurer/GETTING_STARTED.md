# 🚀 Getting Started

Get up and running with Medical Record Structurer in 5 minutes!

## ⚡ Quick Start (Zero Configuration)

The fastest way to try the skill - no setup required!

### Step 1: Run the Demo
```bash
cd /home/node/.openclaw/workspace/skills/medical-record-structurer
python demo.py
```

This will:
- Process 3 sample medical records
- Show you the structured output
- Demonstrate all features

### Step 2: Try with Your Own Data
```bash
python demo.py --input "患者李四，女，32岁，主诉腹痛2天，伴有恶心呕吐..."
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

# Run with custom input
python demo.py --input "你的病历文本"

# Save output to file
python demo.py --output result.json
```

### Using the Python API
```python
from scripts.process_record import process_medical_record

# Process a medical record (free trial - no API key needed!)
result = process_medical_record(
    input_text="患者张三，男，45岁，主诉头痛3天...",
    user_id="user_123"
)

print(result["structured_record"])
```

### Using Command Line
```bash
# Process a record
python scripts/process_record.py \
  --input "患者张三，男，45岁，主诉头痛3天..." \
  --user-id "user_123"
```

## 🎁 Free Trial

Every new user gets **10 free calls** - no credit card required!

```python
result = process_medical_record(
    input_text="你的病历文本",
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
   export SKILLPAY_API_KEY="your-api-key"
   export SKILLPAY_SKILL_ID="your-skill-id"
   ```
3. Continue using the skill - only $0.001 per call!

## 📋 Input Format

The skill accepts medical records in various formats:

### Chinese Format
```
患者[姓名]，[性别]，[年龄]岁，主诉[症状描述]，
诊断[疾病名称]，治疗方案[治疗内容]
```

### English Format
```
Patient [name], [gender], [age] years old, 
chief complaint: [symptoms],
diagnosis: [disease], treatment: [plan]
```

### Example Input
```
患者王五，男，58岁，主诉胸痛2小时，伴有呼吸困难。
既往有高血压病史10年。
体格检查：血压160/95mmHg，心率110次/分。
初步诊断：急性冠脉综合征。
治疗方案：立即给予阿司匹林300mg口服，
硝酸甘油0.5mg舌下含服，联系心内科会诊。
```

## 📤 Output Format

The skill returns a structured EMR (Electronic Medical Record):

```json
{
  "emr_version": "1.0",
  "record_id": "EMR_20240306120000",
  "record_date": "2024-03-06T12:00:00",
  "patient_demographics": {
    "name": "王五",
    "gender": "男",
    "age": 58
  },
  "clinical_information": {
    "chief_complaint": "胸痛2小时，伴有呼吸困难",
    "history_of_present_illness": "既往有高血压病史10年",
    "physical_examination": "血压160/95mmHg，心率110次/分"
  },
  "assessment_and_plan": {
    "diagnosis": "急性冠脉综合征",
    "treatment_plan": "立即给予阿司匹林300mg口服，硝酸甘油0.5mg舌下含服",
    "medications": "阿司匹林300mg，硝酸甘油0.5mg",
    "follow_up_instructions": "联系心内科会诊"
  }
}
```

## 🔧 Troubleshooting

### "User ID is required"
Make sure to provide a user_id parameter:
```python
process_medical_record(input_text="...", user_id="any_unique_id")
```

### Permission Denied
If you see permission errors for `~/.openclaw/`:
```bash
mkdir -p ~/.openclaw/skill_trial
chmod 755 ~/.openclaw
```

### No Output
Check that your input text contains recognizable medical information:
- Patient name
- Symptoms (主诉/chief complaint)
- Diagnosis (诊断/diagnosis)

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

**Happy Structuring! 🎉**
