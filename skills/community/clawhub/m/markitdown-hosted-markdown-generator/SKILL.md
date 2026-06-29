---
name: markitdown-hosted-markdown-generator
description: "MarkItDown Hosted Markdown Generator: Convert files to Markdown. Supports PDF, Word (.docx), Excel (.xlsx/.xls), PowerPoint (.pptx), HTML, CSV, JSON, XML, images, audio, EPub, and ZIP archives. Use when an agent needs markitdown hosted markdown generator, markitdown, convert pdf documents to markdown, extract text from word documents, convert excel spreadsheets to readable markdown, parse powerpoint presentations into text, convert, url through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/markitdown
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/markitdown"}}
---
# MarkItDown Hosted Markdown Generator

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Turn any file into clean, readable Markdown for Agentic workflows. Accepts, PDF, Word doc, Excel spreadsheet, PowerPoint, HTML page, image, or audio file and sends back structured Markdown text — ready for analysis, indexing, or feeding into your next workflow. Uses Microsoft's official MarkItDown package for premium results that AI Agents can parse and understand.

## Product Instructions
### MarkItDown

Convert files and URLs to Markdown using Microsoft's MarkItDown library. Supports PDF, Word (.docx), Excel (.xlsx), PowerPoint (.pptx), HTML, CSV, JSON, XML, images (PNG, JPG), audio (MP3, WAV -- transcription), EPub, ZIP archives, and plain text. Maximum file size: 50 MB.

#### Actions

##### convert

Convert a file to Markdown. Provide the file using exactly ONE of three input methods.

**Required Parameters (one of):**
- `url` (string) -- Public URL or signed storage URL of the file to convert. The tool follows redirects and detects file format from the URL path or Content-Type header.
- `file_id` (string) -- File ID from the AgentPMT file upload tool. The tool retrieves the file from cloud storage and uses the stored original filename to detect format.
- `file_base64` (string) -- Base64-encoded file content for direct inline submission.

**Optional Parameters:**
- `filename` (string) -- Original filename including extension (e.g., "report.pdf"). Helps detect the correct format when using `file_base64`. Also useful when the URL or file_id does not clearly indicate the file type.

**Response Fields:**
- `action` (string) -- Always "convert"
- `source` (string) -- Input method used: "url", "file_id", or "file_base64"
- `markdown` (string) -- The converted Markdown text content
- `length` (integer) -- Character count of the Markdown output

**Example -- Convert from URL:**
```json
{
  "action": "convert",
  "url": "https://example.com/report.pdf"
}
```

**Example -- Convert from file upload:**
```json
{
  "action": "convert",
  "file_id": "abc123-def456"
}
```

**Example -- Convert from base64 with filename hint:**
```json
{
  "action": "convert",
  "file_base64": "JVBERi0xLjQK...",
  "filename": "quarterly_report.pdf"
}
```

**Example Response:**
```json
{
  "action": "convert",
  "source": "url",
  "markdown": "# Report Title\n\nSection content here...",
  "length": 4521
}
```

#### Workflows

1. **Document analysis pipeline** -- Upload a file using the file upload tool, then pass the returned `file_id` to MarkItDown to convert it to Markdown for further processing or summarization by an AI agent.
2. **Web page to Markdown** -- Provide a public URL of an HTML page to extract its content as clean Markdown, useful for archiving or content repurposing.
3. **Spreadsheet data extraction** -- Convert Excel or CSV files to Markdown tables for readable display or further data analysis.
4. **Presentation content extraction** -- Convert PowerPoint files to Markdown to extract slide content, speaker notes, and structure for review or repurposing.
5. **Archive inspection** -- Convert a ZIP file to get a Markdown listing/extraction of its contents.

#### Notes

- Exactly one input method must be provided per request (`url`, `file_id`, or `file_base64`). Providing none will result in a validation error.
- The maximum file size is 50 MB regardless of input method. Files exceeding this limit are rejected.
- When using `file_base64`, providing `filename` with the correct extension significantly improves format detection accuracy.
- When using `url`, the tool auto-detects format from the URL file extension first, then falls back to the HTTP Content-Type header.
- For `file_id` input, the file must not be deleted or expired, and must belong to the same budget context.
- Audio files (MP3, WAV) are transcribed to text and returned as Markdown.
- Image files are processed for any text content (OCR-style extraction via MarkItDown).
- If format cannot be determined, the file is treated as a binary file with extension `.bin`.
- The conversion runs asynchronously on the server; large files may take longer to process.

## When To Use
- Use this skill for `MarkItDown Hosted Markdown Generator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: markitdown hosted markdown generator, markitdown, convert pdf documents to markdown, extract text from word documents, convert excel spreadsheets to readable markdown, parse powerpoint presentations into text, convert, url.
- Supported action names: `convert`.

## Use Cases
- Convert PDF documents to Markdown
- Extract text from Word documents
- Convert Excel spreadsheets to readable Markdown
- Parse PowerPoint presentations into text
- Convert HTML pages to Markdown
- Extract content from EPub files
- Process ZIP archives of documents

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)
- File Storage - Over 10MB: ../file-storage-over-10mb (ClawHub: `file-storage-over-10mb`, page: https://clawhub.ai/agentpmt/file-storage-over-10mb; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-storage-over-10mb`)
- File Storage - 10MB or less: ../file-storage-10mb-or-less (ClawHub: `file-storage-10mb-or-less`, page: https://clawhub.ai/agentpmt/file-storage-10mb-or-less; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-storage-10mb-or-less`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `convert` (action slug: `convert`): Convert a file to Markdown. Provide the file using exactly one of: url, file_id, or file_base64. Supports PDF, Word, Excel, PowerPoint, HTML, CSV, JSON, XML, images, audio, EPub, and ZIP. Max 50MB. Price: `5` credits. Parameters: `file_base64`, `file_id`, `filename`, `url`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "markitdown"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "markitdown"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "markitdown"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "markitdown"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "markitdown"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "markitdown"
  }
}
```

## Call This Tool
Product slug: `markitdown`

Marketplace page: https://www.agentpmt.com/marketplace/markitdown

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "MarkItDown-Hosted-Markdown-Generator",
    "arguments": {
      "action": "convert",
      "file_base64": "example file base64",
      "file_id": "example file id",
      "filename": "example filename",
      "url": "https://example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "markitdown",
  "parameters": {
    "action": "convert",
    "file_base64": "example file base64",
    "file_id": "example file id",
    "filename": "example filename",
    "url": "https://example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `convert` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/markitdown
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
