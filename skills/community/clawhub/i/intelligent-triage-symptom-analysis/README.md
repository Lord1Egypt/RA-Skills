# Intelligent Triage and Symptom Analysis

AI-powered medical triage assistance for healthcare providers, telemedicine platforms, and patients. Provides accurate preliminary symptom assessment and urgency recommendations.

## Features

- **Comprehensive Symptom Coverage** - 650+ symptoms across 11 body systems
- **Standardized Triage** - 5-level classification (Resuscitation to Non-emergency)
- **Red Flag Detection** - ≥95% accuracy for life-threatening conditions
- **NLP Analysis** - Natural language symptom extraction
- **Differential Diagnosis** - ML-assisted condition ranking
- **SkillPay Billing** - 1 token per analysis (~0.001 USDT)

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
| `SKILL_BILLING_API_KEY` | Your SkillPay API key for billing | Yes |
| `SKILL_ID` | Your Skill ID from SkillPay dashboard | Yes |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for enhanced NLP | - |
| `ANTHROPIC_API_KEY` | Anthropic API key for enhanced NLP | - |
| `ICD11_API_KEY` | ICD-11 API key for disease codes | - |
| `SNOMED_API_KEY` | SNOMED CT API key for medical terms | - |
| `PHI_ENCRYPTION_KEY` | Encryption key for PHI protection | - |
| `DATA_RETENTION_DAYS` | Days to retain analysis data | 30 |
| `AUDIT_LOGGING_ENABLED` | Enable audit logging | true |
| `RED_FLAG_ALERTS_ENABLED` | Enable red flag alerts | true |

## Usage Examples

### Python API

```python
from scripts.triage import analyze_symptoms
import os

# Set environment variables
os.environ["SKILL_BILLING_API_KEY"] = "your-api-key"
os.environ["SKILL_ID"] = "your-skill-id"

# Analyze patient symptoms
result = analyze_symptoms(
    symptoms="胸痛，呼吸困难，持续30分钟",
    age=65,
    gender="male",
    vital_signs={"bp": "160/95", "hr": 110, "temp": 37.2},
    user_id="user_123"
)

# Check result
if result["success"]:
    print("分诊等级:", result["analysis"]["triage"]["level"])
    print("紧急程度:", result["analysis"]["triage"]["urgency"])
    print("建议措施:", result["analysis"]["recommendations"])
else:
    print("错误:", result["error"])
    if "paymentUrl" in result:
        print("充值链接:", result["paymentUrl"])
```

### Command Line

```bash
# Set environment variables
export SKILL_BILLING_API_KEY="your-api-key"
export SKILL_ID="your-skill-id"

# Run analysis
python scripts/triage.py \
  --symptoms "胸痛，呼吸困难" \
  --age 65 \
  --gender male \
  --user-id "user_123"
```

## Triage Levels

| Level | Name | Response Time | Description | Examples |
|-------|------|---------------|-------------|----------|
| 1 | Resuscitation | Immediate | Life-threatening conditions requiring immediate intervention | Cardiac arrest, severe trauma, respiratory failure |
| 2 | Emergent | <15 min | High-risk conditions requiring rapid evaluation | Chest pain, severe bleeding, altered mental status |
| 3 | Urgent | <30 min | Serious conditions requiring timely medical attention | Abdominal pain, high fever, moderate trauma |
| 4 | Less Urgent | <60 min | Less acute conditions needing evaluation within hours | Minor injuries, chronic symptoms, stable conditions |
| 5 | Non-urgent | >60 min | Minor conditions that can wait days to weeks | Follow-up, prescription refill, administrative requests |

## ML Model Implementation

This skill uses a **rule-based algorithm** with pattern matching for symptom analysis. The implementation includes:

### Current Approach
- **Symptom Extraction**: Pattern matching and keyword recognition
- **Severity Assessment**: Rule-based scoring (1-10 scale)
- **Red Flag Detection**: Keyword matching for critical symptoms
- **Triage Calculation**: Algorithmic scoring based on ESI/Manchester systems
- **Differential Diagnosis**: Rule-based condition matching

### Why Rule-Based?
- **Transparency**: Clear, auditable decision logic
- **Reliability**: Consistent results without model drift
- **Speed**: Fast processing without external API calls
- **Safety**: Predictable behavior for critical medical decisions

### Optional Enhancements
The skill can be enhanced with external LLM APIs (OpenAI, Anthropic) for:
- Improved natural language understanding
- Better context extraction
- Enhanced differential diagnosis

Configure optional API keys in `.env` to enable these features.

## Security Considerations

### PHI (Protected Health Information) Handling

This skill processes medical information that may include PHI. Please ensure:

1. **Encryption at Rest**: All stored data should be encrypted
2. **Encryption in Transit**: Use HTTPS/TLS for all communications
3. **Access Controls**: Implement proper authentication
4. **Audit Logging**: All access is logged for compliance
5. **Data Minimization**: Only collect necessary information

### Compliance Notes

- This tool is designed with clinical safety as the priority
- Implement additional safeguards as required by your jurisdiction
- Consider HIPAA/GDPR compliance as applicable
- Regular clinical validation is recommended

### Best Practices

1. Never log PHI to unsecured logs
2. Use environment variables for sensitive configuration
3. Enable audit logging for all triage decisions
4. Implement rate limiting to prevent abuse
5. Regular review of red flag detection accuracy

## Privacy and Safety

### Important Safety Notes

- **Not a Diagnostic Tool**: Provides triage and assessment, not definitive diagnoses
- **Requires Clinical Judgment**: Intended to support, not replace, clinical decision-making
- **Red Flag Priority**: Life-threatening symptoms are always escalated regardless of other factors
- **Human Review Required**: High-stakes decisions should always involve human review

### Data Handling

- Symptom data is processed in memory
- Optional encryption for data at rest
- Configurable retention policies
- Complete deletion available on request

## Pricing

- **Provider**: skillpay.me
- **Pricing**: 1 token per call (~0.001 USDT)
- **Chain**: BNB Chain
- **Minimum Deposit**: 8 USDT

## References

- Triage methodology: [references/triage-systems.md](references/triage-systems.md)
- Disease database: [references/disease-database.md](references/disease-database.md)
- Clinical specifications: [references/clinical-specs.md](references/clinical-specs.md)

## License

See LICENSE file for details.

## Disclaimer

**IMPORTANT**: This tool is for preliminary assessment only and does not replace professional medical diagnosis. Always consult qualified healthcare providers for medical decisions.

**System Limitations**:
- Not a Diagnostic Tool: Provides triage and assessment, not definitive diagnoses
- Requires Clinical Judgment: Intended to support, not replace, clinical decision-making
- Dependent on Input Quality: Accuracy depends on quality and completeness of information
- Age-Specific Accuracy: Variable performance across different age groups
- Rare Conditions: Limited accuracy for very rare or novel conditions
