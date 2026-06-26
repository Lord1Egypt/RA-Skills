---
name: Automated Lead Generation Pipeline with Gmail & Salesforce Integration
description: "Enrich and score sales leads using AI-powered analysis, data validation, and CRM integration. Use when the user needs lead qualification, contact enrichment, data cleansing, or automated scoring for sales pipeline optimization."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["LEADGENIUS_API_KEY", "CRM_API_KEY", "ENRICHMENT_SERVICE_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "⭐"
    }
  }
---

# LeadGenius: AI-Powered Lead Enrichment & Scoring

LeadGenius is an enterprise-grade lead intelligence skill that transforms raw prospect data into actionable sales intelligence. Using advanced AI algorithms, this skill automatically enriches contact records, validates data accuracy, assigns dynamic lead scores, and syncs enriched profiles directly to your CRM. Perfect for sales teams, demand gen professionals, and marketing operations who need to maximize conversion rates and prioritize high-value opportunities.

## Overview

LeadGenius solves the critical sales challenge: identifying which leads are actually worth pursuing. Manual lead qualification wastes 30-40% of sales team time, and incomplete contact data kills deal momentum. This skill eliminates friction by:

- **AI-Powered Lead Scoring**: Machine learning models evaluate 50+ engagement and firmographic signals to predict lead quality (0-100 scale)
- **Contact Enrichment**: Append missing email addresses, phone numbers, job titles, company details, LinkedIn URLs, and technographic data
- **Data Validation & Cleansing**: Remove duplicates, flag invalid emails, standardize formatting, verify phone numbers in real-time
- **CRM Sync**: Automatically push enriched records and scores to Salesforce, HubSpot, Pipedrive, or your custom CRM via API
- **Batch Processing**: Process 10,000+ leads in minutes with intelligent rate-limiting and error recovery
- **Compliance & Privacy**: GDPR-compliant data handling with audit logging for regulated industries

LeadGenius integrates with **Salesforce**, **HubSpot**, **Pipedrive**, **Zoho CRM**, **Google Sheets**, **Slack notifications**, and **Zapier** for workflow automation.

## Quick Start

Try these example prompts to get started immediately:

### Example 1: Score and Enrich a Single Lead
```
Enrich and score this prospect:
Name: Sarah Chen
Company: Acme Corp
Email: s.chen@acmecorp.com
Industry: SaaS
Company size: 150 employees

Add missing contact details, assign a lead score (0-100), and flag any data quality issues.
```

### Example 2: Batch Enrich from CSV with CRM Sync
```
I have a CSV file with 500 prospects (name, company, industry only).
Please:
1. Enrich all records with email, phone, LinkedIn URL, job title
2. Score each lead based on engagement potential
3. Flag low-quality records for review
4. Sync all valid records to my Salesforce instance
5. Send me a summary report to Slack

My Salesforce org ID is: 00D123456789ABCDE
```

### Example 3: Find High-Intent Leads with Specific Criteria
```
Score and filter all leads where:
- Company revenue: $10M - $1B
- Industry: Financial Services or Healthcare
- Decision-maker title: VP or C-level
- Company has recent funding/news

Return top 50 leads sorted by score, ready to add to my HubSpot campaign.
```

### Example 4: Data Quality Audit
```
Run a data quality audit on our existing 2,000-person prospect database:
- Flag duplicate records
- Validate all email addresses
- Identify missing critical fields (email, phone, job title)
- Score data completeness
- Generate a remediation plan

Send results to my Google Sheet.
```

## Capabilities

### Lead Enrichment
- **Contact Information**: Email, phone, mobile, direct dial, fax
- **Professional Details**: Job title, department, seniority level, LinkedIn URL, verified work history
- **Company Intelligence**: Revenue, headcount, industry, subindustry, headquarters location, founded year, funding history, technology stack
- **Firmographic & Technographic Data**: CRM system in use, marketing platform, cloud services, security certifications
- **Social Signals**: Twitter handle, GitHub profile, company news mentions, hiring activity

### AI-Powered Lead Scoring
- **Engagement Scoring**: Email open rates, website visits, content downloads, event attendance, form submissions
- **Firmographic Scoring**: Company fit based on industry, size, growth stage, location, technology adoption
- **Behavioral Scoring**: Sales call sentiment, email response time, website session duration, page visit frequency
- **Intent Scoring**: Keywords in recent news, job postings, LinkedIn activity, customer use-case relevance
- **Propensity Model**: Custom ML models trained on your historical closed-won deals
- **Real-Time Scoring**: Updates as new engagement data arrives from your web analytics and CRM

### Data Validation & Cleansing
- **Email Validation**: Real-time SMTP verification with bounce detection
- **Phone Validation**: Format standardization, international number support, carrier verification
- **Duplicate Detection**: Smart matching on name, email, phone, company to eliminate redundant records
- **Field Standardization**: Title case for names, uppercase for states, consistent date formatting
- **Completeness Scoring**: Quantify data quality with missing field flags and recommendations
- **Duplicate Resolution**: Merge records intelligently, preserving engagement history

### CRM & Marketing Platform Integrations
- **Salesforce**: Direct data sync via REST API, custom field mapping, lead assignment rules
- **HubSpot**: Lead objects, custom properties, automated workflow triggers
- **Pipedrive**: Deal sync with custom fields and pipeline automation
- **Zoho CRM**: Native integration with custom module mapping
- **Microsoft Dynamics 365**: Dynamic entity updates with relationship linking
- **Google Sheets**: Two-way sync for collaborative lead management
- **Slack**: Real-time notifications when high-priority leads are identified
- **Zapier/Make.com**: Webhook triggers for downstream automation

### Reporting & Analytics
- **Lead Quality Dashboard**: Visual breakdown of lead scores, enrichment rates, data quality metrics
- **Scoring Distribution**: Histogram showing lead tier breakdown
- **Enrichment Coverage**: % of records with email, phone, company data complete
- **Trend Analysis**: Lead quality changes over time, seasonal patterns
- **ROI Calculator**: Estimated pipeline value from enriched leads
- **Custom Reports**: Export to CSV, PDF, or send automated weekly/monthly reports to Slack

## Configuration

### Environment Variables (Required)
```bash
# LeadGenius API credentials
export LEADGENIUS_API_KEY="sk_live_1234567890abcdef"
export LEADGENIUS_BASE_URL="https://api.leadgenius.io/v2"

# CRM Integration (choose one or configure multiple)
export SALESFORCE_ORG_ID="00D123456789ABCDE"
export SALESFORCE_API_TOKEN="sfdc_token_here"
export HUBSPOT_API_KEY="hs-api-key-here"
export PIPEDRIVE_API_KEY="pd_api_key_here"

# Enrichment Data Services
export ENRICHMENT_SERVICE_KEY="enrich_key_here"
export CLEARBIT_API_KEY="clearbit_key_here"  # Optional secondary enrichment
export HUNTER_API_KEY="hunter_api_key_here"  # Optional email finder

# Notifications
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
export NOTIFICATION_EMAIL="ops@company.com"

# Data Compliance
export GDPR_MODE="true"
export AUDIT_LOG_ENABLED="true"
export DATA_RETENTION_DAYS="90"
```

### Configuration Options
```json
{
  "scoring": {
    "model": "advanced",
    "weight_engagement": 0.35,
    "weight_firmographic": 0.40,
    "weight_behavioral": 0.25,
    "threshold_hot": 75,
    "threshold_warm": 50,
    "threshold_cold": 0
  },
  "enrichment": {
    "max_api_calls_per_second": 100,
    "retry_failed_lookups": true,
    "max_retries": 3,
    "confidence_threshold": 0.85
  },
  "crm_sync": {
    "auto_update_existing": true,
    "map_custom_fields": {
      "lead_score": "Lead_Score__c",
      "enrichment_date": "Last_Enrichment_Date__c",
      "data_quality": "Data_Quality_Score__c"
    },
    "assignment_rules": "use_crm_rules"
  },
  "deduplication": {
    "strategy": "smart_merge",
    "match_threshold": 0.95,
    "merge_engagement_history": true
  }
}
```

## Example Outputs

### Lead Enrichment Output
```json
{
  "original_record": {
    "name": "John Smith",
    "company": "TechCorp Inc",
    "email": "john@techcorp.com"
  },
  "enriched_record": {
    "name": "John Smith",
    "email": "john.smith@techcorp.com",
    "phone": "+1-415-555-0123",
    "mobile": "+1-415-555-0124",
    "linkedin_url": "https://linkedin.com/in/johnsmith",
    "job_title": "VP of Sales",
    "department": "Sales",
    "seniority_level": "Executive",
    "company": "TechCorp Inc",
    "company_revenue": "$450M",
    "company_headcount": "2,150",
    "company_founded": "2010",
    "industry": "Software/SaaS",
    "hq_city": "San Francisco",
    "hq_state": "CA",
    "technologies": ["Salesforce", "HubSpot", "Marketo", "AWS"],
    "recent_news": ["Series D funding $75M", "Opened EU office"],
    "hiring_status": "aggressive"
  },
  "lead_score": {
    "total_score": 82,
    "engagement_score": 75,
    "firmographic_score": 88,
    "behavioral_score": 80,
    "intent_score": 85,
    "tier": "HOT",
    "recommendation": "Add to priority nurture sequence"
  },
  "data_quality": {
    "completeness_score": 94,
    "missing_fields": [],
    "confidence": 0.98,
    "last_verified": "2024-01-15T14:32:00Z"
  },
  "enrichment_metadata": {
    "enrichment_timestamp": "2024-01-15T14:32:00Z",
    "sources": ["Clearbit", "RocketReach", "Crunchbase"],
    "processing_time_ms": 1240
  }
}
```

### Batch Enrichment Summary Report
```
LeadGenius Enrichment Report
Generated: 2024-01-15 | Processed: 500 leads in 3m 24s

ENRICHMENT RESULTS:
  ✓ Successfully enriched: 485 (97%)
  ⚠ Partially enriched: 12 (2.4%)
  ✗ Failed enrichment: 3 (0.6%)

DATA QUALITY METRICS:
  Email addresses found: 98.2%
  Phone numbers found: 87.5%
  Job titles appended: 94.1%
  LinkedIn URLs added: 91.3%
  Company data complete: 99.8%

LEAD SCORING DISTRIBUTION:
  HOT (75-100): 128 leads (25.6%)
  WARM (50-74): 247 leads (49.4%)
  COLD (0-49): 125 leads (25.0%)

TOP 10 LEADS (by score):
  1. Jane Doe - VP Product - Acme Corp - Score: 96
  2. Mike Johnson - CTO - TechCorp - Score: 94
  3. Lisa Wang - Director of Sales - DataSys Inc - Score: 92
  ... (7 more)

CRM SYNC STATUS:
  Synced to Salesforce: 485 records
  Synced to HubSpot: 485 records
  Sync errors: 0

NEXT STEPS:
  • 128 HOT leads ready for immediate outreach
  • 3 failed enrichments - check email/company name spelling
  • Review 12 partially enriched records for manual completion
```

## Tips & Best Practices

### Maximize Lead Quality
1. **Start with Clean Source Data**: Ensure company names match official legal entities for best enrichment accuracy
2. **Enrich Before Scoring**: Complete enrichment always yields better scoring accuracy than sparse data
3. **Set Industry-Specific Thresholds**: SaaS/tech buyers often need different score thresholds than enterprise manufacturing
4. **Refresh Stale Leads**: Re-enrich quarterly; job titles, company data, and technologies change frequently
5. **Combine with First-Party Data**: Layer your engagement data (email opens, website visits, form fills) with enriched firmographics for 40% better accuracy

### Optimize CRM Sync
1. **Map Custom Fields Early**: Define your lead score field, enrichment date, and data quality custom fields in your CRM before first sync
2. **Use Assignment Rules**: Configure CRM assignment rules to automatically route high-score leads to top closers
3. **Set Up Automation**: Create CRM workflows that trigger nurture campaigns when leads hit certain score thresholds
4. **Monitor Sync Health**: Check weekly sync reports for errors; most errors are company name mismatches or field mapping issues
5. **Batch Process Off-Peak**: Process large enrichments during non-business hours to avoid CRM API rate limits

### Reduce False Positives
1. **Balance Scoring Weights**: If your conversion data shows company size matters more than engagement, adjust weightings
2. **Test Score Thresholds**: Run pilots with different HOT/WARM/COLD thresholds against your actual close rates before rolling out
3. **Include Negative Signals**: Mark leads from industries/company sizes where you've had poor success; these should lower scores
4. **Review Outliers Monthly**: Audit leads scoring 85+ that didn't convert; adjust model weights based on patterns
5. **Avoid Over-Reliance on Scores**: Use scores as input to human judgment, not replacement; sales intuition still matters

### Data Privacy & Compliance
1. **Honor Unsubscribe Lists**: Filter out contacts who've opted out of marketing before enrichment
2. **Review GDPR Impact**: EU contacts have stricter consent requirements; consider GDPR_MODE=true
3. **Audit Data Sources**: Review which sources provide your enrichment data quarterly for compliance
4. **Retain Audit Logs**: Keep 90-180 days of enrichment logs to prove data sourcing in case of privacy audits

## Safety & Guardrails

### What LeadGenius Will NOT Do
- **Will NOT provide personal data on non-business contacts** (home addresses, family information, social security numbers)
- **Will NOT bypass GDPR, CCPA, or data privacy regulations** even if requested
- **Will NOT enrich contacts without consent confirmation** when required by applicable law
- **Will NOT access or modify your CRM without explicit API credentials and permission**
- **Will NOT guarantee 100% accuracy** for all enrichment fields; some lookups have confidence scores below 100%
- **Will NOT process data outside the EU if EU data residency is required**
- **Will NOT retain your proprietary customer data** beyond the processing window (default 90 days)

### Limitations & Boundaries
- **Enrichment Success Rates Vary by Segment**: B2B professional emails (90%+ success) vs. small business or consumer emails (60-75% success)
- **Job Title Data Can Be Stale**: Titles may reflect LinkedIn snapshots from 30-90 days ago; verify with recent activity
- **Phone Numbers Less Available**: Mobile and direct dial numbers are harder to source; success rates typically 60-80%
- **Company Data Lag**: Recent rebrands or mergers may take 14-30 days to propagate through enrichment databases
- **No Intent Guarantees**: AI scoring is probabilistic; high-scored leads are more likely to convert but not guaranteed
- **Rate Limiting Applies**: API enforces 100 requests/second per org to prevent abuse; batch jobs may take longer during high-volume periods