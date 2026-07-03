---
name: lynx-skill
description: >
  Stateless Go CLI for the Lynx Reservations (www.lynx-reservations.com) travel
  agency system. Use this skill whenever the user needs to search files, retrieve
  itineraries, upload attachments, or manage documents in the Lynx system.
  Commands map 1:1 to the lynx-mcp-server MCP tools but run as standalone CLI
  commands with no background server. The user will need valid Lynx credentials
  (LYNX_USERNAME, LYNX_PASSWORD, LYNX_COMPANY_CODE).
---

# lynx-skill

Stateless Go CLI that replicates every tool from `lynx-mcp-server` as standalone commands — no daemon, no SSE, no Bearer token.

## Quick Install

```bash
cd lynx-travel-agent/lynx-skill
go build -o bin/lynx .
# optional: put it in PATH
cp bin/lynx ~/bin/lynx   # or /usr/local/bin/
```

## Credentials

The binary reads these environment variables. **All three are required:**

| Variable | Description |
|---|---|
| `LYNX_USERNAME` | Lynx username |
| `LYNX_PASSWORD` | Lynx password |
| `LYNX_COMPANY_CODE` | Company code |

## Available Commands

| # | Command | Description |
|---|---------|-------------|
| 1 | `file-search-by-party-name` | Search files by customer last name |
| 2 | `file-search-by-file-reference` | Search files by Lynx file reference |
| 3 | `retrieve-itinerary` | Get detailed itinerary for a file |
| 4 | `retrieve-file-documents` | Get documents for a transaction |
| 5 | `attachment-upload` | Upload a file attachment from disk |
| 6 | `file-document-save` | Save document at the file level |
| 7 | `transaction-document-save` | Save document at the transaction level |

All commands output **JSON to stdout**. Errors go to **stderr**. Exit code `0` = success, `1` = failure.

---

### 1. `file-search-by-party-name`

Search for files by the customer's last name.

```
lynx file-search-by-party-name --party-name=LASTNAME
```

**Flags:**

| Flag | Type | Required | Description |
|------|------|----------|-------------|
 --party-name` | string | yes | Customer last name to search for |

**Output:**

```json
{
  "count": 1,
  "results": [
    {
      "companyCode": "XX",
      "clientIdentifier": "12345",
      "clientReference": "REF-ABC",
      "currency": "EUR",
      "fileIdentifier": "12345",
      "fileReference": "FTXXXXXXXXX",
      "partyName": "SMITH",
      "status": "Active",
      "travelDate": "2026-06-15"
    }
  ]
}
```

**Examples:**

```bash
lynx file-search-by-party-name --party-name=Smith
lynx file-search-by-party-name --party-name=Smi
```

---

### 2. `file-search-by-file-reference`

Search for a file using its Lynx file reference (e.g. `FTXXXXXXXXX`).

```
lynx file-search-by-file-reference --file-reference=FTXXXXXXXXX
```

**Flags:**

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--file-reference` | string | yes | Lynx file reference |

**Output:** Same JSON structure as `file-search-by-party-name` (`count` + `results` array).

**Example:**

```bash
lynx file-search-by-file-reference --file-reference=FT16476987
```

---

### 3. `retrieve-itinerary`

Get the full itinerary for a given file.

```
lynx retrieve-itinerary --file-identifier=ID
```

**Flags:**

| Flag | Short | Type | Required | Default | Description |
|------|-------|------|----------|---------|-------------|
| `--file-identifier` | `-f` | string | yes | — | Numeric file identifier (from search results) |
| `--show-cancelled` | `-c` | bool | no | `false` | Include cancelled bookings in the results |

**Output:**

```json
{
  "type": "...",
  "partyName": "SMITH",
  "fileReference": "FTXXXXXXXXX",
  "fileIdentifier": "12345",
  "clientIdentifier": "12345",
  "agentReference": "AGT001",
  "itineraryCount": 2,
  "itineraries": [
    {
      "voucherIdentifier": "V123",
      "date": "15 Jun 2026",
      "transactionIdentifier": "btx12345",
      "supplier": "Hotel ABC",
      "status": "Confirmed",
      "confirmationNumber": "CONF-001",
      "location": "Paris"
    }
  ]
}
```

**Examples:**

```bash
# Active bookings only (default)
lynx retrieve-itinerary --file-identifier=16476987

# Include cancelled bookings
lynx retrieve-itinerary --file-identifier=16476987 --show-cancelled
```

---

### 4. `retrieve-file-documents`

Retrieve all documents associated with a specific transaction within a file.

```
lynx retrieve-file-documents \
  --file-identifier=ID \
  --transaction-identifier=TXID
```

**Flags:**

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--file-identifier` | string | yes | Numeric file identifier |
| `--transaction-identifier` | string | yes | Transaction identifier (from itinerary) |

**Output:**

```json
{
  "count": 1,
  "results": [
    {
      "fileIdentifier": "12345",
      "transactionIdentifier": "btx12345",
      "documentIdentifier": "doc_001",
      "documentName": "Invoice",
      "documentType": "SUPP",
      "content": "<span>Invoice details</span>",
      "attachmentUrl": "/documents/file/f16476987/d20250709064401.pdf"
    }
  ]
}
```

**Example:**

```bash
lynx retrieve-file-documents \
  --file-identifier=16476987 \
  --transaction-identifier=btx12345
```

---

### 5. `attachment-upload`

Upload a file (PDF, image, etc.) from disk and associate it with a document.

```
lynx attachment-upload \
  --identifier=FILEID \
  --file=/path/to/document.pdf
```

**Flags:**

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--identifier` | string | yes | Unique identifier for the attachment |
| `--file` | string | yes | Path to the file on disk |

**Output:**

```json
{
  "attachmentUrl": "/documents/file/f16476987/d20250709064401.pdf"
}
```

The returned `attachmentUrl` can be passed to `file-document-save` or `transaction-document-save` as `--attachment-url`.

**Examples:**

```bash
lynx attachment-upload --identifier=f16476987 --file=./documents/invoice.pdf
lynx attachment-upload --identifier=f16476987 --file=./documents/receipt.jpg
```

---

### 6. `file-document-save`

Save (create or update) a document at the **file level**.

```
lynx file-document-save \
  --file-identifier=ID \
  --name=NAME \
  --content=CONTENT \
  --type=TYPE \
  [--attachment-url=URL]
```

**Flags:**

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--file-identifier` | string | yes | Numeric file identifier |
| `--name` | string | yes | Document name |
| `--content` | string | yes | Document content (plain text or HTML) |
| `--type` | string | yes | Document type code — see valid values below |
| `--attachment-url` | string | no | Attachment URL from `attachment-upload` |

**Valid `--type` values:**

| Code | Display Name |
|------|-------------|
| `SUPP` | Supplier Communication |
| `CLINT` | Agent Communication |
| `GEN` | General |
| `INV` | Accounting Communication |
| `AFTER` | After Hours Phone Inquiry |
| `EMAIL` | Email |
| `FLIGH` | Flight Information |
| `BOOKI` | Mail Merge Document |
| `PHONE` | Phone Conversation |
| `CLCOM` | Travelling Client Communication |

> ⚠️ Only these exact codes are accepted. Passing an invalid code will be rejected before the request is sent. The `documentType` field returned by `retrieve-file-documents` is the internal code (e.g. `SUPP`), which can be passed directly to `--type`.

**Output:**

```json
{
  "status": "ok"
}
```

**Examples:**

```bash
lynx file-document-save \
  --file-identifier=16476987 \
  --name="Note" \
  --content="Customer requested change of date" \
  --type=SUPP

lynx file-document-save \
  --file-identifier=16476987 \
  --name="Invoice" \
  --content="<span>Invoice #1234 — 1500.00 EUR</span>" \
  --type=INV \
  --attachment-url=/documents/file/f16476987/d20250709064401.pdf
```

---

### 7. `transaction-document-save`

Save (create or update) a document at the **transaction level**.

```
lynx transaction-document-save \
  --file-identifier=ID \
  --transaction-identifier=TXID \
  --name=NAME \
  --content=CONTENT \
  --type=TYPE \
  [--attachment-url=URL]
```

**Flags:**

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--file-identifier` | string | yes | Numeric file identifier |
| `--transaction-identifier` | string | yes | Transaction identifier |
| `--name` | string | yes | Document name |
| `--content` | string | yes | Document content (plain text or HTML) |
| `--type` | string | yes | Document type code — see valid values in `file-document-save` |
| `--attachment-url` | string | no | Attachment URL from `attachment-upload` |

**Output:**

```json
{
  "status": "ok"
}
```

**Examples:**

```bash
lynx transaction-document-save \
  --file-identifier=16476987 \
  --transaction-identifier=btx12345 \
  --name="Voucher" \
  --content="Confirmation voucher for hotel booking" \
  --type=SUPP

lynx transaction-document-save \
  --file-identifier=16476987 \
  --transaction-identifier=btx12345 \
  --name="Invoice" \
  --content="<b>Paid: 500 EUR</b>" \
  --type=INV \
  --attachment-url=/documents/file/f16476987/d20250709064401.pdf
```

---

## SAMPLES — Multi-Step Workflows

### Sample 1: Find a customer file, inspect itinerary, save a note

```bash
# Step 1 — Search by customer last name
lynx file-search-by-party-name --party-name=Smith

# Step 2 — From the results, grab the fileIdentifier (e.g. 16476987)
#          and inspect the itinerary
lynx retrieve-itinerary --file-identifier=16476987

# Step 3 — From the itinerary, get a transactionIdentifier (e.g. btx12345)
#          and save a note at transaction level
lynx transaction-document-save \
  --file-identifier=16476987 \
  --transaction-identifier=btx12345 \
  --name="Note" \
  --content="Customer requested date change" \
  --type=SUPP
```

### Sample 2: Upload an invoice and attach it to a file

```bash
# Step 1 — Search file by reference
lynx file-search-by-file-reference --file-reference=FT16476987

# Step 2 — Upload the invoice PDF from disk
lynx attachment-upload \
  --identifier=f16476987 \
  --file=./invoices/invoice_1234.pdf

# Step 3 — Save the document at file level with the attachment URL
lynx file-document-save \
  --file-identifier=16476987 \
  --name="Invoice #1234" \
  --content="<span>Invoice 1234 — 1500 EUR</span>" \
  --type=INVOICE \
  --attachment-url=/documents/file/f16476987/d20250709064401.pdf
```

### Sample 3: Retrieve documents, check content, save a new receipt

```bash
# Step 1 — Retrieve all documents for a transaction
lynx retrieve-file-documents \
  --file-identifier=16476987 \
  --transaction-identifier=btx12345

# Step 2 — Pipe the JSON output through jq to inspect document names
lynx retrieve-file-documents \
  --file-identifier=16476987 \
  --transaction-identifier=btx12345 \
  | jq '.results[].documentName'

# Step 3 — Upload a payment receipt
lynx attachment-upload \
  --identifier=f16476987 \
  --file=./receipts/payment_receipt.pdf

# Step 4 — Save the receipt at transaction level
lynx transaction-document-save \
  --file-identifier=16476987 \
  --transaction-identifier=btx12345 \
  --name="Payment Receipt" \
  --content="<b>Paid: 500 EUR on 01-Jun-2026</b>" \
  --type=RECEIPT \
  --attachment-url=/documents/file/f16476987/d20250709064401.pdf
```

### Sample 4: Full document management lifecycle

```bash
# 1. Find the file
lynx file-search-by-party-name --party-name=Smith

# 2. Get the itinerary (find transaction identifiers)
lynx retrieve-itinerary --file-identifier=16476987

# 3. Upload an attachment
lynx attachment-upload \
  --identifier=f16476987 \
  --file=./invoice.pdf

# 4. Save the document at file level
lynx file-document-save \
  --file-identifier=16476987 \
  --name="Invoice" \
  --content="<span>See attached PDF</span>" \
  --type=SUPP \
  --attachment-url=/documents/file/f16476987/d20250709064401.pdf

# 5. Verify the document was saved by retrieving all documents
lynx retrieve-file-documents \
  --file-identifier=16476987 \
  --transaction-identifier=btx12345
```

## Troubleshooting

| Symptom | Likely Cause |
|---------|--------------|
| `authentication failed` | Missing or invalid `LYNX_*` env vars |
| `LYNX_USERNAME is not set` | Environment variable not defined |
| `invalid partyName argument` | Missing `--party-name` flag |
| `invalid file reference argument` | Missing `--file-reference` flag |
| `failed to parse response` | GWT-RPC format changed or invalid identifier |
| `unexpected response format` | Attachment upload was rejected (check file size) |
| `exit code 1, no stdout` | Error written to stderr; run `lynx <command> 2>&1` to inspect |

### Quick debug recipes

```bash
# Capture stderr
lynx file-search-by-party-name --party-name=Smith 2>&1

# Pretty-print JSON
lynx file-search-by-party-name --party-name=Smith | jq

# Extract specific field
lynx file-search-by-party-name --party-name=Smith | jq '.results[].fileIdentifier'

# Check env vars are set
env | grep LYNX
```

## Architecture

```
lynx-skill/
├── main.go                     # Entry point — calls cmd.Run()
├── go.mod                      # Module: dodmcdund.cc/lynx-travel-agent/lynxskill (Go 1.23.10)
├── .gitignore                  # Ignores /bin/, /lynxskill, .env
├── SKILL.md                    # This file — OpenClaw skill definition
├── README.md                   # User-facing documentation
├── lynx_architecture.md        # Full architecture document (decisions, comparisons)
│
├── cmd/                        # CLI commands — one file per command + dispatcher
│   ├── cmd.go                  # Command registry, dispatcher, .env auto-loader, config
│   ├── file_search_by_party_name.go
│   ├── file_search_by_file_reference.go
│   ├── retrieve_itinerary.go
│   ├── retrieve_file_documents.go
│   ├── attachment_upload.go
│   ├── file_document_save.go
│   └── transaction_document_save.go
│
├── gwt/                        # GWT-RPC protocol layer
│   ├── types.go                # GWT type constants (class names)
│   ├── build.go                # GWT-RPC body builders (one func per action)
│   ├── parse.go                # GWT response parsers + response structs
│   └── parse_test.go           # Parser tests (10-result FileSearchResponse)
│
└── lynx/                       # HTTP client layer
    ├── auth.go                 # GWT-RPC login → JSESSIONID + http.Client with cookiejar
    └── client.go               # HTTP helpers: DoGWTRequest, DoMultipartRequest, GWT error parse
```

## Lessons from Implementation (AP-17)

### 1. GWT-RPC Requires Two Parsers

The Lynx backend returns two GWT-RPC serialization formats. The parser auto-detects:

- **Old format (pre-mid 2025):** Type strings like `com.lynxtraveltech.client.shared.model.FileSearchResponse/2457361185` appear directly in the data array. The parser walks backward from the end of the parsed array, mapping indices to values.
- **Lazy serialization (current):** Type strings are resolved through index-based references. The first mapped string in the data array determines which format is active.

The `ParseFileSearchResponse` function uses **backward scanning**: it iterates from the last element backward, identifies `FileSearchResults` type markers, and extracts 10 fields per result. This approach correctly handles multi-result responses (tested with 10 results in `parse_test.go`).

### 2. .env Auto-Load (Convenience vs Security)

`cmd/cmd.go:13-33` implements a lightweight `.env` loader — no external dependency. It reads `.env` from the working directory at startup:

- Lines are split on `=`, whitespace-trimmed
- Only sets env vars that are **not already set** (env vars take precedence)
- Silently returns if `.env` doesn't exist

**.gitignore already includes `.env`** to prevent credential leaks. If `.env` exists with real credentials, it will be ignored by git. This resolves the "ACTION REQUIRED" item from the initial architecture.

### 3. No Retry/Backoff (Deferred)

The MCP server implements exponential backoff retry (0s → 5s → 10s → 30s → 30s, max 5 attempts) with `RetryHTTPRequest`. The CLI does **not** implement retry yet. Rationale:

- CLI is designed for agent use (one-shot commands), not high-throughput automation
- If 429 or transient failures are observed in practice, add a simple retry wrapper in `lynx/client.go`

### 4. Attachment Upload — Consolidated Parsing

The MCP server has **duplicated** `parseResponseBody` functions in `pkg/tools/attachment_upload.go:155` and `pkg/rest/attachment_upload.go:146`. The CLI consolidates this into a single `parseAttachmentResponse` in `cmd/attachment_upload.go:84-101`.

The Lynx backend returns `SUCCESS:/path/to/file:` (colon-delimited). The parser:
1. Strips `SUCCESS:` prefix
2. Trims trailing colon and whitespace
3. Validates the result starts with `/`

### 5. MCP Identifier Typo Corrected

The MCP server parameter is named `identifer` (missing 'i', consistent throughout the codebase). The CLI parameter correctly uses `--identifier`. This is a breaking change from the MCP naming but fixes the original typo.

### 6. Test Coverage

`gwt/parse_test.go` contains a parser test with a real GWT-RPC response for `file-search-by-party-name` ("BRAY" search yielding 10 results). Run tests:

```bash
cd lynx-travel-agent/lynx-skill && go test ./gwt/ -v
```

## Differences from lynx-mcp-server

- **Stateless**: no background server, no SSE, no Bearer token
- **Attachment upload**: reads files from disk directly (not base64)
- **Session**: each command authenticates independently (fresh `JSESSIONID`)
- **Flag style**: `--kebab-case` flags (CLI convention); MCP uses camelCase
- **Binary name**: the CLI binary is `lynx` (vs the MCP server binary `lynx-mcp-server`)
- **Output**: JSON to stdout, errors to stderr
