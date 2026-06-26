---
name: invoice-extractor-from-mail
description: Designed for AP finance teams in cross-border trade enterprises. Automatically fetches invoice attachments from email (IMAP/OAuth) or local files, batch-extracts key fields (invoice number, amount, currency, etc.) via ADP, and exports results to Excel or business systems — no manual data entry required.
---

<div align="center">
<a id="Invoice extractor from mail skill"></a>

# Invoice Extractor from Mail Skill
</div>

**Invoice Extractor from Mail Skill** is a dedicated invoice extraction skill officially built by Laiye Technology for finance teams in traditional manufacturing enterprises. Powered by Laiye ADP (Agentic Document Processing) core capabilities, it establishes an end-to-end automated document processing pipeline from email to business systems, compressing the previously tedious "find attachments -> manual data entry" workflow into a single automated execution: automatically retrieve attachments -> ADP intelligent extraction -> automatic field mapping -> one-click output to Excel / business systems, significantly improving cross-border procurement invoice processing efficiency and data accuracy.

---

## Use Cases
- AP finance teams in traditional manufacturing enterprises can improve end-to-end processing efficiency for overseas invoice collection from email attachments, intelligent information extraction, and data entry during overseas procurement and cross-border settlement workflows.
- Audit teams in cross-border trade enterprises can batch-extract key information from overseas invoices and uniformly archive them during audit and compliance review workflows, improving document organization efficiency and completeness.
- Whether invoices are scattered across employee mailboxes or stored in local files, they can all be processed in batch with concurrency, dramatically improving email processing efficiency.

---

## 1. Core Design Principles

**Guided decision tree, not an exhaustive matrix.**

The Skill does not preset specific email types or business system platforms. Each step asks only one question, follows the corresponding branch based on the user's answer, and automatically skips unnecessary steps.

This means:
- New email types and new business system platforms do not require modifying the Skill; simply guide the user to provide the corresponding connection parameters during the conversation.
- The configuration file structure uses a universal `type` + `params` pattern, without defining a dedicated schema for each vendor.

---

## 2. User Workflow

```
First-time use:
  invoice-extract init
  |-- Q1: Where do the files come from?
  |   |-- "Email" -> Q2: Which email service? -> Collect connection parameters -> Q3: Filter criteria
  |   +-- "Local" -> Skip email configuration
  |-- Q4: ADP Key (required for first use)
  |-- Q5: Do you need field mapping? -> Yes -> Guide configuration / No -> Use ADP raw fields
  +-- Q6: Where should results be output?
      |-- "Local Excel file" (default)
      |-- "Upload to cloud platform" -> Which platform? -> Guide connection parameter configuration
      +-- "Push to business system API" -> Guide endpoint, authentication, and field mapping configuration

Daily use:
  invoice-extract run [--source mail|local] [--path ./invoices/] [--out ./result.xlsx]
```

---

## 3. Skill Internal Processing Flow

```
+----------------------------------------------------------+
|  Phase 1: Retrieve Files                                  |
|  +-----------+     +----------------+                     |
|  | Local     |     | Email          |                     |
|  | Files     |     | Attachments    |                     |
|  | Read      |     | Connect->Filter|                     |
|  | Directly  |     | ->Download     |                     |
|  +-----+-----+     +-------+--------+                     |
|        +--------+-----------+                             |
|                 v                                         |
|  Phase 2: Unified Adaptation                              |
|  Select optimal method by source: file_url / file_path    |
|  / base64                                                 |
|                 v                                         |
|  Phase 3: ADP Extraction                                  |
|  Auto-match invoice extraction app -> Call ADP API ->     |
|  Receive structured JSON                                  |
|                 v                                         |
|  Phase 4: Field Mapping (Optional)                        |
|  ADP raw fields -> Business field names                   |
|                 v                                         |
|  Phase 5: Output                                          |
|  Local Excel file / Upload to user-specified business     |
|  system                                                   |
+----------------------------------------------------------+
```

### Detailed Description for Each Phase

#### Phase 1: Retrieve Files

**Branch A -- Local Files:**
- Supports user uploading a single file or specifying a local folder
- Supported formats: .jpeg, .jpg, .png, .bmp, .tiff, .pdf, .doc, .docx, .xls, .xlsx
- Supported size: 50 MB (if file > 20 MB, the ADP async interface is recommended)
- Folder mode automatically performs recursive scanning, filtering by file extension
- Batch processing supports concurrency, with a default concurrency of 2 (ADP free users will automatically be limited to 1 concurrent process)

**Branch B -- Email Attachments:**
- Ask the user: "What email service do you use?" (no preset options; the user specifies)
- Based on the user's answer, guide the collection of corresponding connection parameters:
  - Generic IMAP types (QQ / 163 / Gmail / Outlook / Feishu Mail / DingTalk Mail / Enterprise Mail / Exchange, etc.): User needs to provide: email address, authorization code, IMAP server address
  - API types (enterprise self-built mail open platforms / other systems providing Mail Open API): Corresponding app_id, app_secret, authentication method
  - Other unknown types: Ask the user what protocol the email service supports, and provide two guided paths: IMAP and API
- Collect filter criteria:
  - Whether to filter unread emails only
  - Attachment type whitelist
  - Sender whitelist
  - Time range
  - Maximum number of messages to process

#### Phase 2: Unified Adaptation

ADP supports three file input methods. The Skill automatically selects the optimal method based on the source:

| Source | Adaptation Method | Priority Notes |
|---|---|---|
| Local files | Pass `file_path` (local path) | Most direct, no conversion needed |
| API-type attachments (providing a temporary download URL) | Pass `file_url` to ADP | No download needed, most efficient |
| Agent scenarios (file already uploaded to server) | Pass `file_url` to ADP | Same as above |
| IMAP-type attachments (binary stream download) | Download then pass `file_path`; if unable to write to disk, convert to `base64` | Prefer writing to disk and using path; fall back to base64 |

#### Phase 3: ADP Extraction (via CLI)

This Skill completes extraction through the ADP CLI tool (rather than calling the API directly). The CLI runs faster after installation and is simpler to integrate.

**Prerequisites before first run:**
1. Install ADP CLI
  ```bash
  # Agent usage
  npx skills add laiye-ai/adp-cli -y -g

  # npm (recommended)
  npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli

  # Linux / macOS
  curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash

  # Windows (PowerShell)
  irm https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1 | iex
  ```

  
2. Run `adp config get` to check credentials. If not configured, guide the user to execute `adp config set --api-key <KEY> --api-base-url <URL>`
  > a. The API key provided by the user can be saved as an environment variable to avoid repeated configuration each time ADP is called. <br>
  > b. The base URL can be auto-populated based on the user's region without requiring user input. ADP provides independent public cloud access URLs for domestic and overseas users. Accessing the nearest endpoint ensures the highest speed and stability. <br>
  > | Region | Login Address | API Base URL |
  > |-----|----------|--------------|
  > | Chinese Mainland | [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub) | `https://adp.laiye.com/` |
  > | Overseas Region | [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub) | `https://adp-global.laiye.com/` |

3. Run `adp app-id list` to get the invoice processing application ID. Subsequently, prefer using `adp app-id cache`
  > The `app id` should preferably be a preset invoice processing application. If the application list contains multiple invoice-processing-related applications, ask the user which one to use.
  > After querying the app id list, the ID list can be saved to cache for faster future queries.

**Core Flow: Execute Extraction**

```bash
# Single file extraction -- local file
adp extract local <file_path> --app-id <app_id>

# Single file extraction -- URL
adp extract url <file_url> --app-id <app_id>

# Single file extraction -- Base64
adp extract base64 <base64> --app-id <app_id>

# Large file async extraction and result querying
adp extract local <file_path> --app-id <app_id> --async
adp extract query <task_id>

# Batch extraction -- local folder (email attachments downloaded and placed in a folder)
adp extract local <folder_path> --app-id <app_id> --export <output_folder> --concurrency 2

# Batch extraction -- URL list file (one URL per line)
adp extract url <url_list_file> --app-id <app_id> --export <output_folder> --concurrency 2
```

**Application Matching Logic:**
- From `adp app-id list` / `adp app-id cache`, preferably select the preset invoice processing application. If the application list contains multiple invoice-processing-related applications, ask the user which one to use.
- If the preset template does not meet the user's needs, a custom extraction template can be created using `adp custom-app create`. Custom templates can be reused.

#### Phase 4: Field Mapping (Optional)

- To ensure that data exported from ADP can be smoothly imported into business systems, users can manually adjust field name mappings.
- If the user has configured mapping rules: Replace the ADP raw field name `field_name` with the mapped field name.
- If not configured: Use the raw field names returned by ADP directly.
- Mapping rules are grouped by document type and support post-run additions/modifications.

#### Phase 5: Output

**Mode A (Default) — Local Excel File:**
- Generates `./out/invoices_YYYYMMDD_HHMM.xlsx`
- One row per document
- When outputting the Excel file, proactively ask the customer to verify the extraction results and whether they need to import the results into a business system

**Mode B — Upload to Cloud Platform (file-based):**
- Upload the generated Excel to cloud storage
- Ask the user which platform they use
- Based on the answer, guide the collection of corresponding authentication parameters and target location
- Common scenario references (for guidance only, not hardcoded):
  - Feishu Docs: Requires app_id + folder_token
  - DingTalk: Requires access_token + space_id
  - OneDrive/SharePoint: Requires OAuth + drive_id
  - Google Sheets: Requires service account + spreadsheet_id
  - Others: Ask the user for the platform's API documentation or upload method

**Mode C — Push to Business System API (structured data):**
- Push ADP's structured JSON extraction results directly to the user's business system (ERP, finance system, etc.) via HTTP API
- Guide the user to provide the following:
  1. **API Endpoint**: The receiving interface URL of the business system (e.g., `https://erp.company.com/api/v1/invoices`)
  2. **Authentication**: Bearer Token / API Key / OAuth 2.0 / Basic Auth
  3. **Request Format**: POST body structure (JSON) and the field names expected by the business system
  4. **Field Mapping**: Use `field_map.json` to map ADP's `field_key` to the target field names in the business system
- Push flow:
  ```
  ADP structured JSON → Field mapping (field_key → business system field name) → Assemble request body → POST to endpoint
  ```
- Common scenario references (for guidance only, not hardcoded):
  - SAP: Requires API endpoint + OAuth client credentials + field mapping
  - Kingdee/Yonyou: Requires API endpoint + App Key + App Secret + field mapping
  - Custom ERP: Requires user to provide API documentation; Skill guides configuration accordingly
- After push completes, display the push status for each record (success/failure); failed records are written to `failed.log`

---

## 4. Configuration File Structure

All configurations are stored in the `~/.invoice_extract/` directory, with `chmod 600` permissions, and must not be committed to version control.

### 4.1 Source Configuration `source.json`

Universal structure: `type` + `params`, without defining a dedicated schema for each email platform.

```json
{
  "type": "imap",
  "params": {
    "host": "imap.qq.com",
    "port": 993,
    "ssl": true,
    "username": "you@qq.com",
    "password": "your_authorization_code",
    "mailbox": "INBOX"
  }
}
```

```json
{
  "type": "local",
  "params": {
    "path": "./invoices/"
  }
}
```

### 4.2 Filter Criteria `filter.json` (Email Mode Only)

```json
{
  "unread_only": true,
  "with_attachment_only": true,
  "attachment_ext": ["pdf", "jpg", "jpeg", "png", "bmp", "tiff"],
  "sender_whitelist": [],
  "since": "2026-04-01",
  "until": "2026-04-30",
  "max_messages": 200
}
```

### 4.3 ADP Credentials (Managed via CLI)

```bash
# View current configuration
adp config get

# Set API Key
adp config set --api-key <KEY>

# Set API Base URL (Chinese Mainland: https://adp.laiye.com/ Overseas: https://adp-global.laiye.com/)
adp config set --api-base-url <url>

# Check balance
adp credit
```

### 4.4 Field Mapping `field_map.json` (Optional)

> **Full field schema reference:** See [`refers/adp-invoice-fields.md`](refers/adp-invoice-fields.md) for the complete ADP field definition, JSON structure, and mapping rules.

Mapping rules: The left-side key is the `field_key` from ADP output JSON (fixed identifier, cannot be modified). The right-side value is the user-defined display name (used as Excel column headers or business system target field names, freely modifiable by user).

Example:

```json
{
  "invoice/receipt": {
    "invoice_number":             "Invoice Number",
    "invoice_date":               "Invoice Date",
    "supplier_name":              "Vendor",
    "total_amount":               "Grand Total",
    "line_items_description":     "Item Description",
    "line_items_total_amount":    "Line Amount"
  }
}
```

- If no mapping is configured, the Skill uses ADP's raw `field_name` as the display name
- For API push mode (Mode C), the values become the field names in the POST request body

### 4.5 Output Configuration `output.json`

```json
{
  "type": "excel",
  "params": {
    "dir": "./out/"
  }
}
```

```json
{
  "type": "cloud",
  "platform": "feishu",
  "params": {
    "app_id": "cli_xxxxxxx",
    "app_secret": "xxxxxxxxxxxxxxxx",
    "folder_token": "xxxxxxxx"
  }
}
```

```json
{
  "type": "api",
  "params": {
    "endpoint": "https://erp.company.com/api/v1/invoices",
    "method": "POST",
    "auth_type": "bearer",
    "auth_token": "your_token_here",
    "headers": {
      "Content-Type": "application/json"
    }
  }
}
```

> **API mode notes:**
> - `auth_type` supports: `bearer` (Bearer Token), `api_key` (in header or query), `oauth2` (Client Credentials), `basic` (username + password)
> - When pushing, the Skill assembles ADP extraction results into a JSON body according to `field_map.json` mapping, then POSTs each record to the endpoint
> - If the business system supports batch APIs, the user can configure `"batch": true` and the Skill will combine multiple records into an array for a single push
> - Before pushing, a preview is displayed (request body of the first record) for user confirmation before batch execution

---

## 5. Command Reference

```bash
# First-time configuration (guided wizard)
invoice-extract init

# Execute extraction (using saved configuration)
invoice-extract run

# Override source (extract from local files this time)
invoice-extract run --source local --path ./invoices/

# Override time range
invoice-extract run --since 2026-04-01 --until 2026-04-30

# Preview only (list files to be processed without actually extracting)
invoice-extract dry-run

# View/edit field mapping
invoice-extract map --edit

# Reconfigure a specific step
invoice-extract init --only source
invoice-extract init --only adp
invoice-extract init --only output
```

---

## 6. Excel Output Column Conventions

- Use the `field_name` from the ADP output JSON results as columns, with one field name corresponding to one column name.
- All results from one document are output as a single row.
- The Excel sheet is named "adp extract result".

---

## 7. Error Handling

| Scenario | Behavior |
|---|---|
| Email connection failure | Terminate immediately, prompt to check connection parameters |
| Single file download/read failure | Skip, log to `failed.log`, continue processing the next file |
| ADP CLI not installed | Automatically execute the installation script |
| ADP credentials not configured / authentication failure | Terminate immediately, guide the user to execute `adp config set --api-key <KEY>` |
| ADP extraction failure (corrupted file / blank page, etc.) | Do not retry, log to `failed.log` |
| ADP async task timeout | Exponential backoff polling with `adp extract query <task_id>`, up to 3 retries |
| Cloud platform upload failure | Excel is still retained locally, prompt the user to check platform configuration |
| API push authentication failure (401/403) | Terminate immediately, prompt user to check if token/credentials have expired |
| API push single record failure (4xx/5xx) | Skip the record, log to `failed.log`, continue pushing the next one; summarize failure count after completion |
| API push endpoint unreachable | Terminate immediately, prompt user to check network and endpoint URL |

---

## 8. Security and Privacy

- All credential files have `chmod 600` permissions and must not be committed to version control.
- Email passwords/authorization codes are stored locally only and are not sent to ADP.
- ADP will transmit files to its server for processing. For sensitive files, please confirm data compliance first.
- Cache directory: `./.cache/invoice_extract/`

---

## 9. Limitations

- Single file <= 50 MB (ADP limitation)
- Recommended <= 100 files per batch; please process in batches if exceeded.
- Encrypted emails (S/MIME) and password-protected PDFs are not supported.
- Default concurrency is 2, but ADP free users only support a concurrency of 1. If the user is a free user, concurrency will be automatically reduced to 1.

## 10. Billing Rules
- **New user benefit:** 100 free credits per month, with no restrictions on which applications can be used.
- **Credit consumption rules:**
    | Processing Stage | Cost |
    |-----------------|------|
    | Document parsing | 0.5 credits/page |
    | Purchase order extraction | 1.5 credits/page |
    | Invoice/receipt extraction | 1.5 credits/page |
    | Custom extraction | 1 credit/page |

> When credits are insufficient, you can log in to the ADP portal directly to top up. We provide independent public cloud access URLs for domestic and overseas users, which need to be configured separately by region. Accessing the nearest endpoint ensures the highest speed and stability.<br>
> - Chinese Mainland users: [Login](https://adp.laiye.com/)<br>
> - Non-Chinese Mainland users: [Login](https://adp-global.laiye.com/)<br>

If you encounter any payment issues, please contact support: global_product@laiye.com

---

## 11. Related Resources
- **CLI Documentation**: [ADP CLI User Guide](https://laiye-tech.feishu.cn/wiki/YIaawiK2DimisZk5KfDc8a8cnLh)
- **API Documentation**: [OpenAPI User Guide](https://laiye-tech.feishu.cn/wiki/S1t2wYR04ivndKkMDxxcp2SFnKd)
- **User Guide**: [Public Cloud Operation Manual](https://laiye-tech.feishu.cn/wiki/OfexwgVUQiOpEek4kO7c7NEJnAe)
- **Problem Feedback**: global_product@laiye.com
- **Official Website**: [Laiye Technology](https://laiye.com)

---

Copyright (c) 2026 [Laiye Technology (Beijing) Co., Ltd.] All rights reserved.
