---
name: PCI DSS Compliance Checker
description: Evaluates an organization's payment card processing environment against PCI DSS requirements and returns a comprehensive compliance assessment.
---

# Overview

The PCI DSS Compliance Checker is a security assessment tool designed to evaluate whether an organization meets the Payment Card Industry Data Security Standard (PCI DSS) requirements. This API accepts detailed information about your payment processing infrastructure, security controls, and operational practices, then performs a thorough compliance analysis across all 12 PCI DSS requirements.

Organizations handling payment card data—whether through e-commerce platforms, physical point-of-sale systems, mobile payments, or third-party processors—must maintain PCI DSS compliance to protect cardholder data and avoid regulatory penalties. This tool streamlines the self-assessment process by analyzing your security posture across network security, access controls, encryption, vulnerability management, and security policies.

The Compliance Checker is ideal for merchants, payment processors, service providers, security teams, and compliance officers who need to understand their PCI DSS compliance status, identify gaps in their security controls, and prioritize remediation efforts.

## Usage

**Sample Request:**

```json
{
  "organization_name": "TechRetail Inc.",
  "business_type": "E-commerce Retailer",
  "company_size": "Medium (50-500 employees)",
  "transaction_volume": "1-5 million transactions/year",
  "card_brands": ["Visa", "Mastercard", "American Express"],
  "processing_methods": ["Online", "Mail Order/Telephone"],
  "stores_card_data": true,
  "transmits_card_data": true,
  "processes_card_data": true,
  "ecommerce_website": true,
  "physical_locations_pos": false,
  "mobile_payments": true,
  "third_party_processors": true,
  "cloud_services": true,
  "firewall_installed": true,
  "default_passwords_changed": true,
  "network_segmentation": true,
  "card_data_protected": true,
  "transmission_encrypted": true,
  "cryptographic_keys": true,
  "antivirus_installed": true,
  "secure_systems_development": true,
  "vulnerability_management": true,
  "access_controls_by_role": true,
  "unique_user_ids": true,
  "multifactor_auth": true,
  "physical_access_restricted": true,
  "media_securely_handled": true,
  "access_logged": true,
  "logs_regularly_reviewed": true,
  "log_integrity_protected": true,
  "vulnerability_scans": true,
  "penetration_testing": true,
  "network_monitoring": true,
  "security_policy_maintained": true,
  "security_awareness_program": true,
  "incident_response_plan": true,
  "service_provider_monitoring": true
}
```

**Sample Response:**

```json
{
  "compliance_status": "Compliant",
  "overall_score": 98,
  "assessment_date": "2025-01-20",
  "organization": "TechRetail Inc.",
  "requirement_summary": {
    "requirement_1": {
      "name": "Install and maintain firewall configuration",
      "status": "Compliant",
      "score": 100
    },
    "requirement_2": {
      "name": "Do not use vendor-supplied defaults",
      "status": "Compliant",
      "score": 100
    },
    "requirement_3": {
      "name": "Protect stored cardholder data",
      "status": "Compliant",
      "score": 100
    },
    "requirement_4": {
      "name": "Encrypt transmission of cardholder data",
      "status": "Compliant",
      "score": 100
    },
    "requirement_5": {
      "name": "Protect systems against malware",
      "status": "Compliant",
      "score": 100
    },
    "requirement_6": {
      "name": "Develop and maintain secure systems",
      "status": "Compliant",
      "score": 100
    },
    "requirement_7": {
      "name": "Implement strong access control measures",
      "status": "Compliant",
      "score": 95
    },
    "requirement_8": {
      "name": "Identify users and restrict access",
      "status": "Compliant",
      "score": 100
    },
    "requirement_9": {
      "name": "Restrict physical access to cardholder data",
      "status": "Compliant",
      "score": 100
    },
    "requirement_10": {
      "name": "Track and monitor access to cardholder data",
      "status": "Compliant",
      "score": 95
    },
    "requirement_11": {
      "name": "Test security systems regularly",
      "status": "Compliant",
      "score": 100
    },
    "requirement_12": {
      "name": "Maintain information security policy",
      "status": "Compliant",
      "score": 100
    }
  },
  "recommendations": [
    "Continue conducting regular vulnerability scans and penetration tests.",
    "Maintain robust service provider monitoring programs.",
    "Schedule quarterly access control audits to ensure least privilege is maintained."
  ],
  "next_steps": "Schedule annual compliance validation assessment."
}
```

## Endpoints

### POST /pci-compliance

**Description:** Performs a PCI DSS compliance assessment based on the organization's payment processing environment and security controls.

**Method:** POST

**Path:** `/pci-compliance`

**Request Body:**

The endpoint accepts a JSON object with the following properties:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `organization_name` | string | Yes | Name of the organization undergoing assessment |
| `business_type` | string | Yes | Type of business (e.g., E-commerce Retailer, Payment Processor, Service Provider) |
| `company_size` | string | Yes | Size of the organization (e.g., Small, Medium, Large, Enterprise) |
| `transaction_volume` | string | Yes | Annual transaction volume (e.g., <1M, 1-5M, 5-10M, >10M transactions/year) |
| `card_brands` | array[string] | Yes | List of payment card brands processed (e.g., Visa, Mastercard, American Express, Discover) |
| `processing_methods` | array[string] | Yes | Payment processing methods (e.g., Online, Mail Order/Telephone, In-Person, Mobile) |
| `stores_card_data` | boolean | Yes | Whether organization stores cardholder data |
| `transmits_card_data` | boolean | Yes | Whether organization transmits cardholder data |
| `processes_card_data` | boolean | Yes | Whether organization processes cardholder data |
| `ecommerce_website` | boolean | Yes | Whether organization operates an e-commerce website |
| `physical_locations_pos` | boolean | Yes | Whether organization operates physical POS locations |
| `mobile_payments` | boolean | Yes | Whether organization accepts mobile payments |
| `third_party_processors` | boolean | Yes | Whether organization uses third-party payment processors |
| `cloud_services` | boolean | Yes | Whether organization uses cloud services for payment processing |
| `firewall_installed` | boolean | Yes | Whether firewall is installed and configured |
| `default_passwords_changed` | boolean | Yes | Whether all default passwords have been changed |
| `network_segmentation` | boolean | Yes | Whether cardholder data environment is segmented from public network |
| `card_data_protected` | boolean | Yes | Whether stored cardholder data is encrypted |
| `transmission_encrypted` | boolean | Yes | Whether cardholder data transmission is encrypted |
| `cryptographic_keys` | boolean | Yes | Whether cryptographic keys are securely managed |
| `antivirus_installed` | boolean | Yes | Whether antivirus/malware protection is installed |
| `secure_systems_development` | boolean | Yes | Whether secure development practices are followed |
| `vulnerability_management` | boolean | Yes | Whether vulnerability management processes are in place |
| `access_controls_by_role` | boolean | Yes | Whether access controls are based on business need and role |
| `unique_user_ids` | boolean | Yes | Whether all users have unique user IDs |
| `multifactor_auth` | boolean | Yes | Whether multi-factor authentication is implemented |
| `physical_access_restricted` | boolean | Yes | Whether physical access to cardholder data facilities is restricted |
| `media_securely_handled` | boolean | Yes | Whether media containing cardholder data is securely handled |
| `access_logged` | boolean | Yes | Whether access to cardholder data is logged |
| `logs_regularly_reviewed` | boolean | Yes | Whether logs are regularly reviewed |
| `log_integrity_protected` | boolean | Yes | Whether log integrity is protected |
| `vulnerability_scans` | boolean | Yes | Whether regular vulnerability scans are performed |
| `penetration_testing` | boolean | Yes | Whether penetration testing is conducted annually |
| `network_monitoring` | boolean | Yes | Whether network is monitored for unauthorized access |
| `security_policy_maintained` | boolean | Yes | Whether information security policy is maintained and updated |
| `security_awareness_program` | boolean | Yes | Whether security awareness training program is in place |
| `incident_response_plan` | boolean | Yes | Whether incident response plan is documented and tested |
| `service_provider_monitoring` | boolean | Yes | Whether service providers are monitored for compliance |

**Response (200 OK):**

Returns a JSON object containing the compliance assessment results, including:

- `compliance_status`: Overall compliance status (Compliant, Non-Compliant, Partial)
- `overall_score`: Numeric compliance score (0-100)
- `assessment_date`: Date of assessment
- `organization`: Organization name from request
- `requirement_summary`: Detailed assessment for each of the 12 PCI DSS requirements with status and individual scores
- `recommendations`: List of prioritized remediation recommendations
- `next_steps`: Guidance on follow-up actions

**Response (422 Validation Error):**

Returns validation errors if required fields are missing or invalid:

```json
{
  "detail": [
    {
      "loc": ["body", "organization_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- Kong Route: https://api.mkkpro.com/compliance/pci-dss-checker
- API Docs: https://api.mkkpro.com:8038/docs
