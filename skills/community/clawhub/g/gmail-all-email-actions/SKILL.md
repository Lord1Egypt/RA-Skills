---
name: gmail-all-email-actions
description: "Gmail - All Email Actions: Gmail integration: send, read, search, reply, forward emails. Manage labels, drafts, trash. Supports attachments and custom from addresses. Use when an agent needs gmail all email actions, gmail all email actions, automated email notifications and alerts, customer inquiry response and follow up, email search and retrieval for information gathering, inbox management and organization with labels, create draft, to through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/gmail-all-email-actions
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/gmail-all-email-actions"}}
---
# Gmail - All Email Actions

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Gmail connection that enables agents to send, read, search, and manage email through Google OAuth integration. The tool provides comprehensive email functionality including composing and sending new messages with attachments, replying to emails while maintaining thread continuity, and forwarding messages to new recipients. Agents can search and filter emails using Gmail's powerful query syntax to find specific messages by sender, subject, date, labels, or attachment status. The tool supports full email lifecycle management including reading message content with parsed headers and body text, moving messages to trash or permanently deleting them, and modifying labels to organize emails or mark them as read. Draft functionality allows agents to create, retrieve, and send draft emails for workflows requiring human review before sending. Additional capabilities include listing all available labels for organization, retrieving user profile information such as email address and message counts, and sending from custom authenticated email addresses.

## Product Instructions
### Gmail - All Email Actions

Complete Gmail management: send, reply, forward, search, read, trash, label, and draft emails.

#### Actions

##### send_message
Send a new email.

**Required:** `to` (array of email addresses), `subject`, `body_text` or `body_html`
**Optional:** `cc`, `bcc`, `from_email` (requires send-as alias configured in Gmail), `body_html`, `attachments`, `thread_id`

```json
{
  "action": "send_message",
  "to": ["recipient@example.com"],
  "subject": "Project Update",
  "body_text": "Hi, here is the latest update on the project.",
  "cc": ["manager@example.com"]
}
```

**With attachment:**
```json
{
  "action": "send_message",
  "to": ["team@example.com"],
  "subject": "Monthly Report",
  "body_text": "Please find the report attached.",
  "attachments": [
    {
      "filename": "report.pdf",
      "file_url": "https://example.com/files/report.pdf",
      "content_type": "application/pdf"
    }
  ]
}
```

##### reply_message
Reply to an existing email. The reply stays in the same thread and automatically uses the original subject and recipient.

**Required:** `message_id`, `body_text` or `body_html`
**Optional:** `cc`, `bcc`, `attachments`

```json
{
  "action": "reply_message",
  "message_id": "18a1b2c3d4e5f6g7",
  "body_text": "Thanks for the update. I'll review this by Friday."
}
```

##### forward_message
Forward an email to new recipients. The original message content is included automatically.

**Required:** `message_id`, `to`
**Optional:** `body_text` (added above the forwarded content), `cc`, `bcc`, `attachments`

```json
{
  "action": "forward_message",
  "message_id": "18a1b2c3d4e5f6g7",
  "to": ["colleague@example.com"],
  "body_text": "FYI - see the message below."
}
```

##### list_messages
Search and list emails. Returns message IDs and thread IDs. Use `get_message` to read full content.

**Required:** none
**Optional:** `q` (Gmail search query), `max_results` (1-500, default 20), `label_ids`, `page_token`

```json
{
  "action": "list_messages",
  "q": "is:unread from:boss@example.com",
  "max_results": 10
}
```

**Common search queries:**
- `is:unread` - unread messages
- `from:user@example.com` - from a specific sender
- `subject:meeting` - subject contains "meeting"
- `has:attachment` - messages with attachments
- `newer_than:7d` - from the last 7 days
- `older_than:30d` - older than 30 days
- `in:sent` - sent messages
- `label:work` - messages with a specific label

##### get_message
Read the full content of an email including headers, body, and attachment metadata.

**Required:** `message_id`
**Optional:** `format` - `full` (default, headers + body), `metadata` (headers only), `minimal` (IDs only)

```json
{
  "action": "get_message",
  "message_id": "18a1b2c3d4e5f6g7",
  "format": "full"
}
```

##### trash_message
Move an email to the trash.

**Required:** `message_id`

```json
{
  "action": "trash_message",
  "message_id": "18a1b2c3d4e5f6g7"
}
```

##### untrash_message
Restore an email from the trash back to its original location.

**Required:** `message_id`

```json
{
  "action": "untrash_message",
  "message_id": "18a1b2c3d4e5f6g7"
}
```

##### modify_labels
Add or remove labels from an email. Use `list_labels` first to find available label IDs.

**Required:** `message_id`, at least one of `add_label_ids` or `remove_label_ids`

```json
{
  "action": "modify_labels",
  "message_id": "18a1b2c3d4e5f6g7",
  "add_label_ids": ["STARRED"],
  "remove_label_ids": ["UNREAD"]
}
```

**Common label IDs:** `INBOX`, `SENT`, `TRASH`, `DRAFT`, `SPAM`, `STARRED`, `IMPORTANT`, `UNREAD`, `CATEGORY_PERSONAL`, `CATEGORY_SOCIAL`, `CATEGORY_PROMOTIONS`

**Useful patterns:**
- Mark as read: `remove_label_ids: ["UNREAD"]`
- Mark as unread: `add_label_ids: ["UNREAD"]`
- Archive: `remove_label_ids: ["INBOX"]`
- Star: `add_label_ids: ["STARRED"]`

##### list_labels
Get all available labels (system and user-created).

**Required:** none

```json
{
  "action": "list_labels"
}
```

##### create_draft
Create a draft email that can be edited or sent later.

**Required:** `to`, `subject`, `body_text` or `body_html`
**Optional:** `cc`, `bcc`, `from_email`, `body_html`, `attachments`, `thread_id`

```json
{
  "action": "create_draft",
  "to": ["client@example.com"],
  "subject": "Proposal Draft",
  "body_html": "<h1>Proposal</h1><p>Here are the details...</p>"
}
```

##### send_draft
Send a previously created draft.

**Required:** `draft_id`

```json
{
  "action": "send_draft",
  "draft_id": "r123456789"
}
```

##### get_draft
Retrieve the content of a draft.

**Required:** `draft_id`
**Optional:** `format` - `full` (default), `metadata`, `minimal`

```json
{
  "action": "get_draft",
  "draft_id": "r123456789"
}
```

##### delete_draft
Permanently delete a draft.

**Required:** `draft_id`

```json
{
  "action": "delete_draft",
  "draft_id": "r123456789"
}
```

##### get_profile
Get the authenticated user's Gmail profile including email address and message counts.

**Required:** none

```json
{
  "action": "get_profile"
}
```

#### Common Workflows

**Check and read unread emails:**
1. `list_messages` with `q: "is:unread"` to get message IDs
2. `get_message` for each message ID to read content
3. `modify_labels` with `remove_label_ids: ["UNREAD"]` to mark as read

**Send email with review:**
1. `create_draft` to compose the email
2. `get_draft` to review content
3. `send_draft` to send, or `delete_draft` to discard

**Reply to a conversation:**
1. `list_messages` with a search query to find the thread
2. `get_message` to read the message you want to reply to
3. `reply_message` with the message_id and your response

**Organize inbox:**
1. `list_messages` to find messages
2. `list_labels` to see available labels
3. `modify_labels` to apply labels, archive, or star messages

#### Important Notes

- **Attachments:** Provide public URLs for file attachments. The files are fetched and attached automatically. Content type is auto-detected if not specified.
- **HTML emails:** You can send both `body_text` and `body_html` together. Recipients who support HTML will see the rich version; others see plain text.
- **Search syntax:** The `q` parameter uses standard Gmail search operators. Combine multiple operators for precise filtering (e.g., `from:alice@example.com newer_than:7d has:attachment`).
- **Pagination:** When `list_messages` returns a `next_page_token`, pass it as `page_token` in the next request to get more results.
- **From address:** The `from_email` field only works if you have configured a send-as alias in Gmail settings.
- **Thread management:** Use `thread_id` with `send_message` or `create_draft` to add a message to an existing conversation thread.

## When To Use
- Use this skill for `Gmail - All Email Actions` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: gmail   all email actions, gmail all email actions, automated email notifications and alerts, customer inquiry response and follow up, email search and retrieval for information gathering, inbox management and organization with labels, create draft, to.
- Supported action names: `create_draft`, `delete_draft`, `forward_message`, `get_draft`, `get_instructions`, `get_message`, `get_profile`, `get_thread`, `list_labels`, `list_messages`, `modify_labels`, `reply_message`, `send_draft`, `send_message`, `trash_message`, `untrash_message`.

## Use Cases
- Automated email notifications and alerts
- Customer inquiry response and follow-up
- Email search and retrieval for information gathering
- Inbox management and organization with labels
- Draft creation for human-in-the-loop email workflows
- Email forwarding and delegation workflows
- Reading and summarizing email content
- Marking messages as read or starring important emails
- Sending reports and documents as attachments
- Monitoring inbox for specific senders or keywords

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `16`.
x402 availability: not enabled for this product.

- `create_draft` (action slug: `create-draft`): Create a draft email that can be edited or sent later. Price: `5` credits. Parameters: `attachments`, `bcc`, `body_html`, `body_text`, `cc`, `from_email`, `subject`, `thread_id`, plus 1 more.
- `delete_draft` (action slug: `delete-draft`): Permanently delete a Gmail draft. Price: `5` credits. Parameters: `draft_id`.
- `forward_message` (action slug: `forward-message`): Forward an email to new recipients. The source message content is included automatically. Price: `5` credits. Parameters: `attachments`, `bcc`, `body_text`, `cc`, `message_id`, `to`.
- `get_draft` (action slug: `get-draft`): Retrieve draft email content with safe body and metadata controls. Price: `5` credits. Parameters: `body_format`, `draft_id`, `format`, `max_body_chars`, `message_format`, `metadata_headers`.
- `get_instructions` (action slug: `get-instructions`): Return Gmail tool usage instructions and examples. Price: `5` credits. Parameters: none.
- `get_message` (action slug: `get-message`): Read a Gmail message with safe body and metadata controls. Price: `5` credits. Parameters: `body_format`, `format`, `max_body_chars`, `message_format`, `message_id`, `metadata_headers`.
- `get_profile` (action slug: `get-profile`): Get the authenticated Gmail profile including email address and message/thread counts. Price: `5` credits. Parameters: none.
- `get_thread` (action slug: `get-thread`): Read Gmail thread messages with safe body and metadata controls. Price: `5` credits. Parameters: `body_format`, `format`, `include_html`, `max_body_chars`, `max_messages`, `message_format`, `metadata_headers`, `thread_id`.
- `list_labels` (action slug: `list-labels`): List all available Gmail labels, including system and user-created labels. Price: `5` credits. Parameters: none.
- `list_messages` (action slug: `list-messages`): Search and list Gmail messages for triage. The tool requests a Gmail message page, fetches compact metadata for each listed message, then applies post-fetch date/category/label filters and optional thread dedupe. Returns messages plus result_size_estimate, next_page_token, fetched_count, and returned_count; returned_count can be lower than fetched_count. Price: `5` credits. Parameters: `dedupe_by_thread`, `exclude_categories`, `exclude_label_ids`, `include_spam_trash`, `label_ids`, `max_internal_date_ms`, `max_results`, `min_internal_date_ms`, plus 2 more.
- `modify_labels` (action slug: `modify-labels`): Add or remove labels from an email. Common uses: mark as read, star, or archive. Price: `5` credits. Parameters: `add_label_ids`, `message_id`, `remove_label_ids`.
- `reply_message` (action slug: `reply-message`): Reply to an existing email. The reply stays in the same thread and automatically uses the original subject and recipient context. Price: `5` credits. Parameters: `attachments`, `bcc`, `body_html`, `body_text`, `cc`, `message_id`.
- `send_draft` (action slug: `send-draft`): Send a previously created Gmail draft. Price: `5` credits. Parameters: `draft_id`.
- `send_message` (action slug: `send-message`): Send a new email. Supports plain text, HTML, attachments, CC/BCC, custom from address, and optional thread continuation. Price: `5` credits. Parameters: `attachments`, `bcc`, `body_html`, `body_text`, `cc`, `from_email`, `subject`, `thread_id`, plus 1 more.
- `trash_message` (action slug: `trash-message`): Move an email message to trash. Price: `5` credits. Parameters: `message_id`.
- `untrash_message` (action slug: `untrash-message`): Restore an email message from trash. Price: `5` credits. Parameters: `message_id`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "gmail-all-email-actions"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "gmail-all-email-actions"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "gmail-all-email-actions"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "gmail-all-email-actions"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "gmail-all-email-actions"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "gmail-all-email-actions"
  }
}
```

## Call This Tool
Product slug: `gmail-all-email-actions`

Marketplace page: https://www.agentpmt.com/marketplace/gmail-all-email-actions

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
    "name": "Gmail---All-Email-Actions",
    "arguments": {
      "action": "create_draft",
      "attachments": [
        {
          "content_type": "application/octet-stream",
          "file_url": "https://example.com",
          "filename": "example filename"
        }
      ],
      "bcc": [
        "example bcc"
      ],
      "body_html": "example body html",
      "body_text": "example body text",
      "cc": [
        "example cc"
      ],
      "from_email": "user@example.com",
      "subject": "example subject",
      "thread_id": "example thread id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "gmail-all-email-actions",
  "parameters": {
    "action": "create_draft",
    "attachments": [
      {
        "content_type": "application/octet-stream",
        "file_url": "https://example.com",
        "filename": "example filename"
      }
    ],
    "bcc": [
      "example bcc"
    ],
    "body_html": "example body html",
    "body_text": "example body text",
    "cc": [
      "example cc"
    ],
    "from_email": "user@example.com",
    "subject": "example subject",
    "thread_id": "example thread id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_draft` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/gmail-all-email-actions
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
