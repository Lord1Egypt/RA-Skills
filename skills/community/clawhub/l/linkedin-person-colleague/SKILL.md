---
name: linkedin-person-colleague
description: "Find internal colleagues through company‑ID and personnel‑ID on LinkedIn. Map organizational structures and gather contacts for sales outreach and account intelligence.\n\nTrigger: LinkedIn colleague lookup, map organizational relationships, internal team discovery, account intelligence research, B2B contact expansion"
metadata: {"version":"1.0.5","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"🤝","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# LinkedIn Person Colleague Query

Query colleague data from LinkedIn using the UpKuaJing Open Platform API.

## Overview

This skill provides access to colleague information from UpKuaJing's LinkedIn data. Given a company ID (pid) and a person ID (hid), it returns the list of colleagues with their person IDs and job titles.

**Prerequisite**: Both the company ID (pid) and person ID (hid) are required as input. If the user does not already have them, use the **linkedin-person-search** skill first to search for the target person and obtain their pid and hid, then proceed with this skill.

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/linkedin_person_colleague_list.py`. **Do NOT use** shell compound commands like `cd scripts && python linkedin_person_colleague_list.py`

### Colleague List Query (`linkedin_person_colleague_list.py`)
- **Return granularity**: Each colleague as one record
- **Use cases**: Find colleagues of a specific person at a company
- **Examples**:
  - "Find colleagues of person H_67890 at company US_12345"
  - "Get more colleagues using the next page cursor"
- **Parameters**: See [Colleague List API](references/linkedin-person-colleague-list-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/search/linkedin/person/colleague/list","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"LinkedIn colleague list query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one page of colleague records:
- Each API call incurs a fee
- Use `--cursor` to get additional pages (each page is a separate call)
- **Before execution:**
  1. Inform user that this query will incur a fee
  2. Stop, wait for explicit user confirmation in a separate message, then execute script

### Fee Confirmation Principle

**Any operation that incurs fees must first inform and wait for explicit user confirmation. Do not execute in the same message as the notification.**

## Workflow

### Decision Guide

| User Intent | Use API |
|-------------|---------|
| "Find colleagues of person H_67890 at company US_12345" | Colleague List Query |
| User has a person/company name but no pid/hid | linkedin-person-search (find the person and get pid/hid, then use this skill) |

## Usage Examples

### Query Colleague List

**User request**: "Find colleagues of person H_67890 at company US_12345"
```bash
python scripts/linkedin_person_colleague_list.py --pid US_12345 --hid H_67890
```

**Get next page** (use cursor returned from previous response):
```bash
python scripts/linkedin_person_colleague_list.py --pid US_12345 --hid H_67890 --cursor 'cursor_string_from_previous_response'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Colleague List: Check [references/linkedin-person-colleague-list-api.md](references/linkedin-person-colleague-list-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/linkedin-person-colleague-list-api.md](references/linkedin-person-colleague-list-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Query parameters**:
   - Both the company ID (pid) and person ID (hid) are required. If the user provides a person/company name instead, first use **linkedin-person-search** to find the target person and obtain their pid and hid.

3. **Pagination**:
   - When the response returns a non-empty `cursor`, more data is available
   - Pass the `cursor` value to get the next page
   - An empty `cursor` means there is no more data

## Notes
- Colleague records use `hid` as the person unique identifier; `pid` is the company identifier
- `titleNames` is a list of job title strings for each colleague
- File paths use forward slashes on all platforms
- **Prohibit outputting technical parameter format**: Do not display code-style parameters in responses, convert to natural language
- **Do not** estimate or guess per-call fees — use `python scripts/auth.py --price_info` to get accurate pricing information
- **Do not** guess parameter names, get accurate parameter names and formats from documentation

## Related Skills

Other UpKuaJing skills you might find useful:

- linkedin-person-search — Search people from LinkedIn data
- linkedin-company-search — Search companies from LinkedIn data
- global-company-person-colleague — Query colleague list from the global company database
- linkedin-company-employee — Query employee list from LinkedIn data
- linkedin-person-experience — Query work experience list from LinkedIn data
- global-company-person-search — Search people from the global company database
- upkuajing-global-company-people-search — Unified company and people search across all sources
- upkuajing-contact-info-validity-check — Check contact info validity
- phone-validity-check — Check phone number validity
- email-validity-check — Check email address validity
- domain-validity-check — Check domain validity and security- upkuajing-email-tool — Email verification and sending tool
- upkuajing-sms-tool — SMS tool
