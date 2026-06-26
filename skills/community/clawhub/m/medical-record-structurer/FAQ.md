# Frequently Asked Questions (FAQ)

## General Questions

### What is Medical Record Structurer?
Medical Record Structurer is an AI-powered tool that converts unstructured medical notes (doctor's口述, handwritten notes, or free-text records) into standardized electronic medical records (EMR) format.

### Is it free to use?
Yes! Every new user gets **10 free calls** with no credit card required. After that, it's only $0.001 per call.

### Do I need an API key?
- **For the first 10 calls**: No API key needed!
- **After free trial**: Yes, you'll need a SkillPay API key

### What languages are supported?
The skill supports both **Chinese** and **English** medical records.

## Usage Questions

### What input formats work best?
The skill works best with records containing:
- Patient name and demographics
- Chief complaint (主诉)
- History of present illness
- Physical examination findings
- Diagnosis
- Treatment plan

### Can I process handwritten records?
Yes, but you'll need to convert them to text first using OCR. The skill focuses on structuring text, not OCR.

### How accurate is the extraction?
The extraction accuracy depends on:
- Clarity of the input text
- Standard medical terminology usage
- Completeness of information

For well-formatted records, accuracy is typically >90%.

### Can I batch process multiple records?
Yes, you can call the API multiple times in a loop:
```python
for record in records:
    result = process_medical_record(record, user_id="user_123")
```

## Technical Questions

### What data is stored?
Only **free trial usage counts** are stored locally:
- User ID (hashed)
- Number of calls used
- Timestamps

**No medical data is ever stored.**

### Is my data secure?
Yes! See our [Security Policy](SECURITY.md) for details. Key points:
- Medical data is processed in-memory only
- No PHI is transmitted to third parties
- All code is open source and auditable

### What are the system requirements?
- Python 3.8+
- No external dependencies
- Works offline (except for billing after trial)

### Can I use this in production?
Yes, but please:
- Review the output for accuracy
- Implement appropriate error handling
- Ensure compliance with local healthcare regulations

## Billing Questions

### How much does it cost?
- **First 10 calls**: Free
- **After trial**: $0.001 USDT per call

### What payment methods are accepted?
Payments are processed via SkillPay using BNB Chain USDT.

### How do I check my balance?
```python
result = process_medical_record(...)
print(f"Balance: {result.get('balance')}")
```

### What happens if I run out of balance?
You'll receive a payment URL to top up your account:
```python
if "paymentUrl" in result:
    print(f"Please recharge: {result['paymentUrl']}")
```

## Troubleshooting

### "User ID is required" error
You must provide a user_id parameter:
```python
process_medical_record(input_text="...", user_id="any_unique_string")
```

### No fields extracted
Try to include standard medical terminology:
- Use "主诉" or "chief complaint" for symptoms
- Use "诊断" or "diagnosis" for the diagnosis
- Include patient demographics

### Permission denied errors
Create the required directory:
```bash
mkdir -p ~/.openclaw/skill_trial
chmod 755 ~/.openclaw
```

### Slow processing
Processing is typically instant. If slow:
- Check your internet connection (only needed for billing)
- Verify the input text isn't excessively long

## Compliance Questions

### Is this HIPAA compliant?
The tool is designed with HIPAA safeguards:
- No persistent PHI storage
- Local processing
- Audit trails

**However**, you are responsible for ensuring your specific use case complies with HIPAA and other applicable regulations.

### Can I use this for clinical decisions?
This tool is for **documentation assistance only**. Always:
- Verify extracted information
- Use clinical judgment
- Follow institutional policies

## Getting Help

### Where can I get support?
- 📧 Email: support@openclaw.dev
- 💬 Discord: [Join our community](https://discord.gg/openclaw)
- 🐛 GitHub Issues: [Report bugs](https://github.com/openclaw/skills/issues)

### How do I report a bug?
Please include:
1. Input text (anonymized)
2. Expected output
3. Actual output
4. Python version

### Can I request features?
Yes! Please open a feature request on GitHub or contact us via Discord.

---

**Still have questions?** Contact us at support@openclaw.dev
