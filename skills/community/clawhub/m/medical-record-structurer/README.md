# Medical Record Structurer

A professional medical record processing tool that transforms unstructured medical notes (voice or text) into standardized electronic medical records (EMR).

## Features

- **Voice/Text Input Processing** - Accepts doctor's口述 or handwritten notes
- **AI-Powered Field Extraction** - Automatically identifies and extracts medical fields
- **Standardized EMR Output** - Generates structured electronic medical records
- **Payment Integration** - skillpay.me integration for pay-per-use monetization (0.001 USDT per use)
- **OCR Support** - Process handwritten medical records via image recognition
- **STT Support** - Process voice recordings via speech-to-text

## Installation

1. Clone or download this skill to your OpenClaw workspace:
```bash
cd /home/node/.openclaw/workspace/skills/
```

2. Install Python dependencies (if any additional packages are needed):
```bash
pip install -r requirements.txt  # if requirements.txt exists
```

3. Copy the environment variables file and configure:
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

## Environment Variables Configuration

Copy `.env.example` to `.env` and configure the following variables:

### Required Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SKILLPAY_API_KEY` | Your SkillPay API key for billing | Yes |
| `SKILLPAY_SKILL_ID` | Your Skill ID from SkillPay dashboard | Yes |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OCR_API_KEY` | API key for OCR services (image processing) | - |
| `OCR_PROVIDER` | OCR provider (google, azure, aws, tesseract) | google |
| `STT_API_KEY` | API key for speech-to-text services | - |
| `STT_PROVIDER` | STT provider (google, azure, aws, whisper) | whisper |
| `PHI_ENCRYPTION_KEY` | Encryption key for PHI protection | - |
| `DATA_RETENTION_DAYS` | Days to retain processed records | 30 |
| `AUDIT_LOGGING_ENABLED` | Enable audit logging | true |

## Usage Examples

### Python API

```python
from scripts.process_record import process_medical_record
import os

# Set API key via environment variable
os.environ["SKILLPAY_API_KEY"] = "your-api-key"
os.environ["SKILLPAY_SKILL_ID"] = "your-skill-id"

# Process with user_id for billing
result = process_medical_record(
    input_text="患者张三，男，45岁，主诉头痛3天...",
    user_id="user_123"
)

# Check result
if result["success"]:
    print("结构化病历:", result["structured_record"])
    print("剩余余额:", result["balance"])
else:
    print("错误:", result["error"])
    if "paymentUrl" in result:
        print("充值链接:", result["paymentUrl"])
```

### Command Line

```bash
# Set API key via environment variable
export SKILLPAY_API_KEY="your-api-key"
export SKILLPAY_SKILL_ID="your-skill-id"

# Run with user_id for billing
python scripts/process_record.py \
  --input "患者张三，男，45岁，主诉头痛3天..." \
  --user-id "user_123"
```

## Output Format

Structured medical record includes:
- Patient demographics (name, age, gender)
- Chief complaint
- History of present illness
- Past medical history
- Physical examination
- Diagnosis
- Treatment plan
- Medications
- Follow-up instructions

## Security Considerations

### PHI (Protected Health Information) Handling

This skill processes medical records containing PHI. Please ensure:

1. **Encryption at Rest**: All stored medical records should be encrypted
2. **Encryption in Transit**: Use HTTPS/TLS for all API communications
3. **Access Controls**: Implement proper authentication and authorization
4. **Audit Logging**: All access to PHI is logged for compliance
5. **Data Minimization**: Only collect necessary information
6. **Retention Policy**: Configure automatic data deletion after retention period

### Compliance Notes

- This tool is designed with HIPAA considerations in mind
- Implement additional safeguards as required by your jurisdiction
- Consider GDPR compliance if serving EU patients
- Regular security audits are recommended

### Best Practices

1. Never log PHI to unsecured logs
2. Use environment variables for sensitive configuration
3. Rotate API keys regularly
4. Monitor access patterns for anomalies
5. Implement rate limiting to prevent abuse

## OCR/STT Support

This skill supports external OCR and STT services for processing:

### OCR (Optical Character Recognition)
For processing handwritten or scanned medical records:
- Google Vision API
- Azure Computer Vision
- AWS Textract
- Tesseract (open source)

### STT (Speech-to-Text)
For processing voice-recorded medical notes:
- Google Speech-to-Text
- Azure Speech Services
- AWS Transcribe
- OpenAI Whisper (open source)

Configure the respective API keys in your `.env` file to enable these features.

## Pricing

- **Provider**: skillpay.me
- **Price**: 0.001 USDT per request
- **Chain**: BNB Chain
- **Minimum Deposit**: 8 USDT

## References

- For detailed field specifications: see [references/emr-schema.md](references/emr-schema.md)
- For payment API details: see [references/skillpay-api.md](references/skillpay-api.md)

## License

See LICENSE file for details.

## Disclaimer

This tool is for medical record structuring only and does not provide medical advice. Always verify the structured output with qualified healthcare professionals.
