---
name: global-company-person-school-detail
description: "Obtain detailed school information including classification, locations and social‑media links. Conduct institution verification and academic‑network research with global institutional‑data resources.\n\nTrigger: global institution lookup, educational‑institution verification, academic‑network analysis, institutional‑data enrichment, degree validation research"
metadata: {"version":"1.0.3","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏫","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Global School Detail Query

Query school detail information from the global company database (全球企业库) using the UpKuaJing Open Platform API.

## Overview

This skill provides access to detailed school information from UpKuaJing's global company database. Given a school ID (sid), it returns the school's name, type, location, and social media URLs. This is a single-record lookup with no pagination needed.

- The `sid` (school ID) can be obtained from **global-company-person-education** (education history query) results

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/school_detail.py`. **Do NOT use** shell compound commands like `cd scripts && python school_detail.py`

### School Detail Query (`school_detail.py`)
- **Return granularity**: All school details returned in one response
- **Use cases**: Lookup school details by ID to get name, location, website, and social media
- **Examples**:
  - "Get details of school S_001"
  - "Look up school information for school ID aue1fd986ee5cb5d906f9d36286714ed33"
- **Parameters**: See [School Detail API](references/school-detail-api.md)

## API Key and Top-up

This skill requires an API key. The API key is stored in the `~/.upkuajing/.env` file:
```bash
cat ~/.upkuajing/.env
```
**Example file content**:
```
UPKUAJING_API_KEY=your_api_key_here
```
### **API Key Not Set**
First check if the `~/.upkuajing/.env` file has UPKUAJING_API_KEY;
If UPKUAJING_API_KEY is not set, prompt the user to choose:
1. User has one: User provides it (manually add to ~/.upkuajing/.env file)
2. User doesn't have one: You can apply using the interface (`auth.py --new_key`), the new key will be automatically saved to ~/.upkuajing/.env
Wait for user selection;

### **Account Top-up**
When API response indicates insufficient balance, explain and guide user to top up:
1. Create top-up order (`auth.py --new_rec_order`)
2. Based on order response, send payment page URL to user, guide user to open URL and pay, user confirms after successful payment;

### **Get Account Information**
Use this script to get account information for UPKUAJING_API_KEY: `auth.py --account_info`

## API Key and UpKuaJing Account
- Newly applied API key: Register and login at [UpKuaJing Open Platform](https://developer.upkuajing.com/), then bind account

### **Report Skill Call Errors**
When an API call fails or returns abnormal data (server error, timeout, malformed response, etc.), explain the anomaly to the user in natural language and ask whether to report it to the platform for troubleshooting. Only run the report after user confirmation:
```bash
python scripts/error_report.py --params '{"requestPath":"/agent/search/depth_company/person/school/detail","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"School detail query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each query returns the complete school details:
- Each API call incurs a fee
- No pagination needed, all data returned in one response
- **Before execution:**
  1. Inform user that this query will incur a fee
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Get details of school S_001" | School Detail Query |

## Usage Examples

### Query School Detail

**User request**: "Get details of school S_001"
```bash
python scripts/school_detail.py --sid S_001
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- School Detail: Check [references/school-detail-api.md](references/school-detail-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/school-detail-api.md](references/school-detail-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Cross-skill usage**:
   - The school ID (`sid`) can be obtained from **global-company-person-education** or **global-company-person-alumni** query results

## Notes
- School detail returns complete information in one response, no pagination needed
- The school ID (`sid`) can be found in education records (from global-company-person-education) or alumni records (from global-company-person-alumni)
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- global-company-search — Search companies from the global company database
- global-company-person-search — Search people from the global company database
- global-company-shareholder — Query shareholder list from the global company database
- global-company-employee — Query employee list from the global company database
- global-company-person-colleague — Query colleague list from the global company database
- global-company-person-alumni — Query alumni list from the global company database
- global-company-person-experience — Query work experience list from the global company database
- global-company-person-education — Query education history list from the global company database
- linkedin-person-search — Search people from LinkedIn data
- linkedin-company-search — Search companies from LinkedIn data
- upkuajing-global-company-people-search — Unified company and people search across all sources
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-contact-info-validity-check — Check contact info validity
- phone-validity-check — Check phone number validity
- email-validity-check — Check email address validity
- domain-validity-check — Check domain validity and security