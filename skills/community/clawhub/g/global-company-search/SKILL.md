---
name: global-company-search
description: "Search global companies by name, industry, product and website URL. Gather firmographic data for supplier research and overseas lead‑generation. \n\nTrigger: global company lookup, firmographic data enrichment, overseas supplier sourcing, cross‑border lead generation, target‑market research"
metadata: {"version":"1.0.3","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🏢","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Global Company Company Search

Search company data from the global company database (全球企业库) using the UpKuaJing Open Platform API.

## Overview

This skill provides access to UpKuaJing's global-company-database company data through one list search script. API key generation and top-up are provided through the `auth.py` script.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/global_company_search.py`. **Do NOT use** shell compound commands like `cd scripts && python global_company_search.py`

### Global Company List Search (`global_company_search.py`)
- **Return granularity**: Each company as one record
- **Use cases**: Focus on "which companies exist" in the global company database
- **Examples**:
  - "Find manufacturers producing LED lights"
  - "Find companies by their website URL"
- **Parameters**: See [Global Company List](references/global-company-list-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/search/depth_company/company/list","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Company search query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### List Search Billing Rules

Billed by **number of calls**, each call returns up to 20 records:
- Number of calls: `ceil(query_count / 20)` times
- **Whenever query_count > 20, must before execution:**
  1. Inform user of expected number of calls
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**


## Workflow

Choose parameters based on user intent.

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Find companies producing XXX" | Global company list (products / keywords) |
| "Find companies with email/phone" | Global company list existEmail=1 / existPhone=1 |
| "Find a company by its website URL" | Global company list companyUrls |
| "Find companies with valid email" | Global company list existValidEmail=1 |

## Usage Examples

### Scenario 1: Small Query — Search Companies

**User request**: "Find Chinese manufacturers producing LED lights"
```bash
python scripts/global_company_search.py \
  --params '{"products": ["LED lights"], "countryCodes": ["CN"], "existEmail": 1}' \
  --query_count 20
```

### Scenario 2: Large Query — Multiple Script Calls Required

**User request**: "Find 1000 US electronics companies with email addresses"
**Before execution** inform user: ceil(1000/20) = 50 API calls, confirm before executing.
```bash
python scripts/global_company_search.py --params '{"products": ["electronics"], "countryCodes": ["US"], "existEmail": 1}' --query_count 1000
```
**After execution**: Script responds {"task_id":"a1b2-c3d4", "file_url": "xxxxx", ……}
**Continue execution, append data**: Specify task_id, script continues from where it left off and appends to file
```bash
python scripts/global_company_search.py --task_id 'task-id-here' --query_count 2000
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- [Global Company List API](references/global-company-list-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/global-company-list-api.md](references/global-company-list-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Optimize query parameters**:
   - Use `products` / `companyNames` / `companyUrls` to filter precisely; industry and product names must be in **English**
   - Use `existEmail=1` or `existValidEmail=1` to filter companies with contact information
   - Use `countryCodes` to limit country scope

3. **Large result sets**:
   - For large queries, pay attention to the jsonl file size

## Notes
- Company records use `pid` as the unique identifier
- All timestamps are in **seconds** (incorp_date is a second-level timestamp)
- Country codes use ISO 3166-1 alpha-2 format (e.g., CN, US, JP)
- File paths use forward slashes on all platforms
- Industry names must be in **English**
- Search quantity affects API response time, recommend setting timeout: 120
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- linkedin-person-search — Search people from LinkedIn data
- global-company-person-search — Search people from the global company database
- global-company-shareholder — Query shareholder list from the global company database
- global-company-employee — Query employee list from the global company database
- global-company-person-colleague — Query colleague list from the global company database
- global-company-person-alumni — Query alumni list from the global company database
- global-company-person-experience — Query work experience list from the global company database
- global-company-person-education — Query education history list from the global company database
- global-company-person-school-detail — Query school detail from the global company database
- linkedin-company-search — Search companies from LinkedIn data
- upkuajing-global-company-people-search — Unified company and people search across all sources
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-contact-info-validity-check — Check contact info validity
- phone-validity-check — Check phone number validity
- email-validity-check — Check email address validity
- domain-validity-check — Check domain validity and security