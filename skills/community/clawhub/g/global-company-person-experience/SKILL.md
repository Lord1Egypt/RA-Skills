---
name: global-company-person-experience
description: "Check overseas staff’s education history via personnel ID. Access their university, degree, major and GPA data to support candidate screening and background checks.\n\nTrigger: employee education verification, personnel academic background check, candidate qualification assessment, pre‑hire screening, overseas staff background validation"
metadata: {"version":"1.0.4","homepage":"https://www.upkuajing.com","clawdbot":{"emoji":"💼","requires":{"bins":["python"],"env":["UPKUAJING_API_KEY"]},"primaryEnv":"UPKUAJING_API_KEY"}}
---

# Global Company Person Work Experience Query

Query work experience data from the global company database (全球企业库) using the UpKuaJing Open Platform API.

## Overview

This skill provides access to person work experience information from UpKuaJing's global company database. Given a person ID (hid), it returns the list of work experiences with company names, job titles, employment dates, and period status. Optionally filter by company ID (pid) to get only the experience at a specific company.

- The `hid` (person ID) can be obtained from **global-company-person-search** (person search) results

## Running Scripts

### Environment Setup

1. **Check Python**: `python --version`
2. **Install dependencies**: `pip install -r requirements.txt`

Script directory: `scripts/*.py`
Run example: `python scripts/*.py`

**Important**: Always use direct script invocation like `python scripts/person_experience_list.py`. **Do NOT use** shell compound commands like `cd scripts && python person_experience_list.py`

### Work Experience List Query (`person_experience_list.py`)
- **Return granularity**: Each work experience as one record
- **Use cases**: View a person's work history, find out where someone has worked
- **Examples**:
  - "Find work experience of person H_67890"
  - "Find work experience of person H_67890 at company US_12345"
  - "Get more work experience using the next page cursor"
- **Parameters**: See [Work Experience List API](references/person-experience-list-api.md)

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
python scripts/error_report.py --params '{"requestPath":"/agent/search/depth_company/person/experience/list","requestId":"f47ac10b58cc4372a5670e02b2c3d479","context":"Work experience query failed with a server error"}'
```
- Do not report normal business conditions (insufficient balance, invalid API key, parameter errors) — handle them via their own flows
- Error reporting does not incur query fees
- **Parameters**: See [Error Report API](references/skill-error-report-api.md)

## Fees

**All API calls incur fees**, different interfaces have different billing methods.

**Latest pricing**: Users can visit [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
Or use: `python scripts/auth.py --price_info` (returns complete pricing for all interfaces)

### Query Billing Rules

Billed by **number of calls**, each call returns one page of work experience records:
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
| "Find work experience of person H_67890" | Work Experience List Query |
| "Find work experience of person H_67890 at company US_12345" | Work Experience List Query (with --pid) |

## Usage Examples

### Query Work Experience List

**User request**: "Find work experience of person H_67890"
```bash
python scripts/person_experience_list.py --hid H_67890
```

**Filter by company**:
```bash
python scripts/person_experience_list.py --hid H_67890 --pid US_12345
```

**Get next page** (use cursor returned from previous response):
```bash
python scripts/person_experience_list.py --hid H_67890 --cursor 'cursor_string_from_previous_response'
```

## Error Handling

- **API key invalid/non-existent**: Check `UPKUAJING_API_KEY` in `~/.upkuajing/.env` file
- **Insufficient balance**: Guide user to top up
- **Invalid parameters**: **Must first check the corresponding API documentation in references/ directory**, get correct parameter names and formats from documentation, do not guess
- **Skill call errors / abnormal responses**: Explain to the user and, with user confirmation, report to the platform via `python scripts/error_report.py` (see [Report Skill Call Errors](#report-skill-call-errors))

### API Documentation Reference

- Work Experience List: Check [references/person-experience-list-api.md](references/person-experience-list-api.md)
- Error Report: Check [references/skill-error-report-api.md](references/skill-error-report-api.md)

## Best Practices

1. **Check API documentation**:
   - **Before executing queries, must first check the corresponding API reference documentation**
   - Check [references/person-experience-list-api.md](references/person-experience-list-api.md)
   - Do not guess parameter names, get accurate parameter names and formats from documentation

2. **Pagination**:
   - When the response returns a non-empty `cursor`, more data is available
   - Pass the `cursor` value to get the next page
   - An empty `cursor` means there is no more data

3. **Cross-skill usage**:
   - The `hid` (person ID) can be obtained from **global-company-person-search** (person search) results
   - The `pid` (company ID) from work experience results can be used with **global-company-search** or **global-company-employee** to find more details about the company

## Notes
- Work experience records use `hid` as the person unique identifier; `pid` is the company identifier
- `postStatus` indicates employment status: 0-unknown, 1-employed, 2-left, 3-uncertain
- `endDate` of 0 means "present" (currently holds the position)
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
- global-company-person-education — Query education history list from the global company database
- global-company-person-school-detail — Query school detail from the global company database
- linkedin-person-search — Search people from LinkedIn data
- linkedin-company-search — Search companies from LinkedIn data
- upkuajing-global-company-people-search — Unified company and people search across all sources
- upkuajing-customs-trade-company-search — Search customs trade companies
- upkuajing-contact-info-validity-check — Check contact info validity
- phone-validity-check — Check phone number validity
- email-validity-check — Check email address validity
- domain-validity-check — Check domain validity and security