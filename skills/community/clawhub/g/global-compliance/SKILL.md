---
name: global-compliance
description: AI-powered global compliance checker, document generator, and risk assessor for GDPR, CCPA, SOC2, ISO27001, HIPAA and more
tags: [compliance, gdpr, ccpa, soc2, iso27001, hipaa, privacy, security, legal, regulation, audit, risk-assessment]
---

# ⚖️ Global Compliance Skill

AI-powered compliance assistant that helps enterprises check documents, generate compliance policies, assess risks, and query regulations for GDPR, CCPA, SOC 2, ISO 27001, HIPAA, and other standards.

## 📦 Installation

### Step 1: Install the Skill

```bash
clawhub install global-compliance
```

### Step 2: Install via npm

```bash
# Install globally
npm install -g openclaw-global-compliance

# Verify installation
compliance --version
compliance help
```

---

## 🚀 Usage

### When to Use This Skill

**AUTO-TRIGGER** when user's message contains:

- Keywords: `compliance`, `GDPR`, `CCPA`, `privacy policy`, `合规`, `隐私政策`, `风险评估`
- Asks about legal/regulatory requirements
- Wants to check documents for compliance
- Needs to generate compliance documents
- Wants risk assessment for different regions

**TRIGGER EXAMPLES**:
- "Check if my privacy policy complies with GDPR"
- "Generate a GDPR-compliant privacy policy"
- "What are the CCPA requirements?"
- "Assess our compliance risk"

**DO NOT USE** when:
- Only general legal questions (use general legal research)
- Contract review (use contract analysis tools)

---

## 🎯 Core Features

Complete compliance management system:

- 🔍 **Compliance Checking** - GDPR, CCPA, SOC 2, ISO 27001, HIPAA
- 📄 **Document Generation** - Privacy policies, terms of service, DPA
- ⚖️ **Risk Assessment** - Multi-jurisdiction risk analysis
- 📚 **Regulation Query** - Search and query compliance requirements
- 📊 **Audit Reports** - Generate professional audit reports
- 🌍 **Multi-Region Support** - EU, US, China, Brazil, global

---

## 💻 Agent Usage Guide

### Primary Commands

When user requests compliance checking or document generation, use these commands:

**Check Compliance:**
```bash
compliance check --type gdpr --file privacy-policy.md --output report.json
```

**Generate Document:**
```bash
compliance generate privacy-policy \
  --company "Company Name" \
  --region eu \
  --industry saas \
  --data-types "pii,usage-analytics" \
  --output privacy-policy.md
```

**Assess Risk:**
```bash
compliance assess \
  --company-info company.json \
  --standards "gdpr,ccpa,soc2" \
  --output risk-report.pdf
```

**Query Regulations:**
```bash
compliance query --standard gdpr --topic "data retention"
```

### Example Workflows

**Example 1: Check GDPR Compliance**

User: "Check if my privacy policy complies with GDPR"

Agent:
1. Ask for policy file or content
2. Execute: `compliance check --type gdpr --file policy.md`
3. Summarize results and provide recommendations

**Example 2: Generate Privacy Policy**

User: "Generate a GDPR-compliant privacy policy for my SaaS company"

Agent:
1. Gather company info (name, industry, data types)
2. Execute: `compliance generate privacy-policy --company "CompanyName" --region eu --industry saas`
3. Review output and offer to save file

**Example 3: Multi-Standard Assessment**

User: "We're expanding to Europe. What compliance requirements do we need?"

Agent:
1. Collect company details
2. Execute: `compliance assess --company-info info.json --standards "gdpr,soc2"`
3. Explain high-priority gaps and provide roadmap

---

## ⚙️ Supported Standards

### Data Privacy
- **GDPR** - EU General Data Protection Regulation
- **CCPA** - California Consumer Privacy Act  
- **PIPL** - China Personal Information Protection Law
- **LGPD** - Brazil General Data Protection Law

### Information Security
- **ISO 27001** - Information Security Management
- **SOC 2** - Service Organization Control
- **PCI-DSS** - Payment Card Industry Data Security

### Industry-Specific
- **HIPAA** - Healthcare (US)
- **GLBA** - Financial Services (US)
- **FERPA** - Education (US)

---

## 📊 Tool Functions

### 1. check_compliance

Check document or process for compliance.

**Parameters:**
- `standard` (string): gdpr | ccpa | soc2 | iso27001 | hipaa
- `content` (string): Document content or file path
- `checkpoints` (array, optional): Specific checks to run

**Returns:**
```typescript
{
  compliant: boolean,
  score: number,  // 0-100
  totalChecks: number,
  passedChecks: number,
  failedChecks: number,
  issues: Array<{
    checkpoint: string,
    severity: 'critical' | 'high' | 'medium' | 'low',
    title: string,
    description: string,
    remediation: string
  }>,
  recommendations: string[]
}
```

### 2. generate_document

Generate compliance document.

**Parameters:**
- `type` (string): privacy-policy | tos | dpa | cookie-policy
- `company_info` (object):
  - `name` (string)
  - `industry` (string)
  - `regions` (array)
  - `data_types` (array)
- `region` (string): eu | us | cn | global
- `language` (string, optional): en | zh | es

**Returns:**
```typescript
{
  type: string,
  content: string,
  format: 'markdown' | 'html' | 'pdf',
  metadata: {
    standard: string[],
    region: string,
    generated: string
  },
  warnings: string[]
}
```

### 3. assess_risk

Assess compliance risk.

**Parameters:**
- `company_info` (object): Company details
- `standards` (array): Standards to assess
- `regions` (array): Target regions

**Returns:**
```typescript
{
  overallScore: number,  // 0-100
  riskLevel: 'low' | 'medium' | 'high' | 'critical',
  byStandard: {
    [standard: string]: {
      score: number,
      gaps: string[],
      priority: number
    }
  },
  recommendations: Array<{
    priority: string,
    title: string,
    description: string,
    effort: string,
    timeline: string
  }>,
  estimatedCost: {
    immediate: number,
    annual: number
  }
}
```

### 4. query_regulation

Query regulation requirements.

**Parameters:**
- `standard` (string): Compliance standard
- `topic` (string): Topic to query

**Returns:**
```typescript
{
  standard: string,
  topic: string,
  requirements: string[],
  references: Array<{
    article: string,
    text: string,
    url: string
  }>
}
```

---

## 💰 Cost Estimation

- **Document Checking**: Free (rule-based)
- **AI-Assisted Analysis**: $0.01-0.05 per document
- **Document Generation**: $0.02-0.10 per document
- **Risk Assessment**: $0.10-0.50 per assessment

---

## 📝 Usage Examples

### Example 1: Check Privacy Policy

```bash
# Create test policy
cat > policy.md <<EOF
# Privacy Policy
We collect email addresses and usage data.
We use encryption to protect your data.
EOF

# Check GDPR compliance
compliance check --type gdpr --file policy.md

# Output:
# Score: 35/100
# Status: ✗ Non-compliant
# Found 8 issues (3 critical, 5 high)
```

### Example 2: Generate Complete Policy

```bash
# Generate GDPR-compliant privacy policy
compliance generate privacy-policy \
  --company "TechStartup Inc" \
  --region eu \
  --industry saas \
  --data-types "pii,usage-analytics" \
  --output privacy-policy.md

# Output: Complete GDPR-compliant privacy policy
```

### Example 3: Multi-Region Risk Assessment

```bash
# Assess risk for EU expansion
cat > company.json <<EOF
{
  "name": "US Company",
  "industry": "saas",
  "regions": ["us"],
  "dataTypes": ["pii", "financial"]
}
EOF

compliance assess \
  --company-info company.json \
  --standards "gdpr,ccpa,soc2"
```

---

## 🔧 Troubleshooting

### Issue 1: Package Not Installed

**Error**: `command not found: compliance`

**Solution**:
```bash
npm install -g openclaw-global-compliance
```

### Issue 2: Config File Missing

**Error**: Cannot find config file

**Solution**:
```bash
# Create default config
compliance init
```

---

## 📚 Full Documentation

- **GitHub**: https://github.com/ZhenRobotics/openclaw-global-compliance
- **Documentation**: Full compliance guides
- **Support**: GitHub Issues

---

## 🎯 Agent Behavior Guidelines

When using this skill, agents should:

**DO**:
- ✅ Ask for necessary company information
- ✅ Provide clear, actionable recommendations
- ✅ Explain compliance issues in plain language
- ✅ Warn about legal review requirements
- ✅ Suggest prioritization for critical issues

**DON'T**:
- ❌ Provide legal advice (recommend consulting lawyers)
- ❌ Guarantee 100% compliance
- ❌ Skip critical warnings
- ❌ Auto-publish generated documents without review

---

## 📊 Compliance Checkpoints

### GDPR (12 checkpoints)
- Legal basis for processing
- User rights (access, erasure, rectification, portability)
- Data retention periods
- Third-party sharing disclosure
- International transfers
- Security measures
- Breach notification
- Children's data protection
- DPO contact (if applicable)

### CCPA (8 checkpoints)
- Right to know
- Right to delete
- Right to opt-out
- Non-discrimination
- Sale of personal information disclosure
- Categories of data collected
- Third-party sharing
- Privacy policy accessibility

### SOC 2 (10 checkpoints)
- Security policies
- Access controls
- Change management
- Risk assessment
- Monitoring and logging
- Incident response
- Vendor management
- Business continuity
- Encryption
- Physical security

---

## 🆕 Version History

### v1.0.0 (2026-03-08)
- ✨ Initial release
- 🔍 GDPR compliance checker
- 🔍 CCPA compliance checker (basic)
- 📄 Privacy policy generator
- ⚖️ Risk assessment framework
- 📚 Regulation query system
- 🤖 CLI tool and Agent integration

---

**Project Status**: ✅ Ready for Use

**License**: MIT

**Author**: @justin

**Support**: https://github.com/ZhenRobotics/openclaw-global-compliance/issues

**ClawHub**: https://clawhub.ai/justin/global-compliance
