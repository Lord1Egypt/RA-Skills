---
name: jira-ticket
description: "Create Jira tickets with web-researched content. Use when asked to create, file, or open a Jira issue/ticket/story/bug/task, especially when the ticket content should be informed by web research or search results. Triggers on phrases like 'create a Jira ticket', 'file a Jira issue', 'open a bug in Jira', 'make a Jira story with research'."
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🎫",
        "requires": { "bins": ["curl", "jq"], "env": ["JIRA_API_TOKEN", "JIRA_EMAIL", "JIRA_BASE_URL"] },
      },
  }
---

# Jira Ticket Creator with Web Research

Create Jira tickets whose content is enriched by web search. Follow these phases in order.

## Setup

Three environment variables are required:

- `JIRA_BASE_URL` — your Atlassian instance (e.g. `https://yourteam.atlassian.net`)
- `JIRA_EMAIL` — the email tied to your Atlassian account
- `JIRA_API_TOKEN` — an API token from https://id.atlassian.com/manage-profile/security/api-tokens

All Jira API calls use Basic auth via `curl -u` and force HTTP/1.1:

```bash
curl --http1.1 -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H "Content-Type: application/json" "$JIRA_BASE_URL/rest/api/3/..."
```

---

## Phase 1 — Parse Arguments

Parse the user's request to extract:

| Field | Required | Description |
|-------|----------|-------------|
| project | yes | Jira project key (e.g. `ENG`, `OPS`) |
| issuetype | no | `Task`, `Bug`, `Story`, `Epic` (default: `Task`) |
| summary | yes | Short title for the ticket |
| search_query | no | Topic to web-search for enriching the description |
| priority | no | `Highest`, `High`, `Medium`, `Low`, `Lowest` (default: `Medium`) |
| assignee | no | Atlassian account email or ID |
| labels | no | Comma-separated labels |
| components | no | Comma-separated component names |

If the user does not provide a project key, ask for it before proceeding.

---

## Phase 2 — Web Research (if applicable)

If the user asked for research, or if the ticket would benefit from context (e.g. a bug report referencing an external API, a story about integrating a third-party service):

1. Use the `web_search` tool to search for the relevant topic.
2. Use the `xurl` tool or `curl` to fetch key pages for details.
3. Extract the most relevant information: error descriptions, API docs, best practices, version notes, or solution approaches.

Compile findings into a structured summary:

```
### Research Summary
- **Source**: [URL]
- **Key findings**: ...
- **Relevant details**: ...
```

If no research is needed, skip to Phase 3.

---

## Phase 3 — Compose Ticket Content

Build the ticket description in Atlassian Document Format (ADF). Combine:

- The user's original request/context
- Research findings from Phase 2 (if any)
- Acceptance criteria (when creating Stories)
- Steps to reproduce (when creating Bugs)

Keep the description concise and actionable.

### ADF Structure

Jira API v3 uses ADF for the description field. Minimal example:

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "paragraph",
      "content": [{ "type": "text", "text": "Description text here." }]
    }
  ]
}
```

For richer formatting (headings, bullet lists, links):

```json
{
  "type": "doc",
  "version": 1,
  "content": [
    {
      "type": "heading",
      "attrs": { "level": 3 },
      "content": [{ "type": "text", "text": "Summary" }]
    },
    {
      "type": "bulletList",
      "content": [
        {
          "type": "listItem",
          "content": [
            {
              "type": "paragraph",
              "content": [{ "type": "text", "text": "Item one" }]
            }
          ]
        }
      ]
    },
    {
      "type": "paragraph",
      "content": [
        { "type": "text", "text": "Source: " },
        {
          "type": "text",
          "text": "link text",
          "marks": [{ "type": "link", "attrs": { "href": "https://example.com" } }]
        }
      ]
    }
  ]
}
```

---

## Phase 4 — Validate Project and Fields

Before creating the ticket, verify the project exists and discover available fields:

```bash
# Verify project
curl --http1.1 -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/3/project/$PROJECT_KEY" | jq '{key, name, id}'

# List available issue types for the project
curl --http1.1 -s -u "$JIRA_EMAIL:$JIRA_API_TOKEN" -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/3/project/$PROJECT_KEY/statuses" | jq '.[].name'
```

If the project or issue type is invalid, report the error and ask the user to correct it.

---

## Phase 5 — Create the Ticket

```bash
curl --http1.1 -s -X POST \
  -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  -H "Content-Type: application/json" \
  "$JIRA_BASE_URL/rest/api/3/issue" \
  -d '{
    "fields": {
      "project": { "key": "PROJECT_KEY" },
      "summary": "Ticket summary here",
      "issuetype": { "name": "Task" },
      "priority": { "name": "Medium" },
      "description": { ADF_OBJECT },
      "labels": ["label1", "label2"]
    }
  }'
```

Extract the response:

```bash
# Parse response for issue key and URL
ISSUE_KEY=$(echo "$RESPONSE" | jq -r '.key')
ISSUE_URL="$JIRA_BASE_URL/browse/$ISSUE_KEY"
```

If the API returns an error, display the error message and suggest corrections.

---

## Phase 6 — Report

Present the result to the user:

- **Issue key**: e.g. `ENG-1234`
- **URL**: direct link to the ticket
- **Summary**: the title that was set
- **Research included**: yes/no, with sources listed

---

## Notes

- The Jira REST API v3 requires ADF for descriptions — plain text or markdown will be rejected.
- Rate limits: Jira Cloud allows ~100 requests per minute per user.
- The `jira.yaml` network policy preset in NemoClaw already allows `*.atlassian.net`, `auth.atlassian.com`, and `api.atlassian.com` on port 443.
- To use this skill inside NemoClaw's sandbox, enable the Jira preset in your sandbox policy.

## Examples

```
# Create a simple task
/jira-ticket ENG "Update API rate limiting docs"

# Create a bug with web research
/jira-ticket ENG --type Bug --search "Node.js fetch timeout ECONNRESET" "Fix intermittent ECONNRESET in payment service"

# Create a story with priority and labels
/jira-ticket PLATFORM --type Story --priority High --labels "q2,backend" "Add OAuth2 PKCE flow for mobile clients"
```
