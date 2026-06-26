---
name: ollang
description: Master skill for the Ollang translation platform. Routes to the right Ollang sub-skill based on intent — upload files, create orders, check status, manage revisions, run QC, browse projects and folders. Use when the user mentions Ollang or wants to perform any translation/captioning/dubbing workflow.
---

# Ollang — Master Skill

This is the entry point for all Ollang API operations. Based on the user's intent, delegate to the appropriate sub-skill below.

## Sub-Skills

| Sub-Skill | When to Use |
|-----------|-------------|
| `ollang-health` | User wants to check if the API is up |
| `ollang-upload` | User wants to upload a video, audio, document, or VTT file |
| `ollang-order-create` | User wants to create a translation, CC, subtitle, or dubbing order |
| `ollang-order-get` | User wants to check the status or details of a specific order |
| `ollang-orders-list` | User wants to list, search, or filter their orders |
| `ollang-order-cancel` | User wants to cancel an order |
| `ollang-order-rerun` | User wants to rerun or regenerate an order |
| `ollang-revision` | User wants to report an issue or manage revisions on an order |
| `ollang-human-review` | User wants to request or cancel human (linguist) review |
| `ollang-qc-eval` | User wants to run a quality control evaluation on an order |
| `ollang-project` | User wants to list or inspect projects |
| `ollang-folder` | User wants to list or find folders |

## Full Workflow

A complete end-to-end translation workflow looks like this:

```
1. Upload file          →  ollang-upload        →  returns projectId
2. Create order         →  ollang-order-create  →  returns orderId(s)
3. Monitor status       →  ollang-order-get     →  poll until "completed"
4. Quality check        →  ollang-qc-eval       →  scores + segment analysis
5. Report issues        →  ollang-revision      →  create revisions if needed
6. Upgrade to human     →  ollang-human-review  →  optional linguist review
```

## Authentication

All endpoints (except health check) require the `X-Api-Key` header.
The API key is read from the `OLLANG_API_KEY` environment variable.

If the variable is not set, instruct the user to configure it:
```bash
export OLLANG_API_KEY=<your-api-key>
```
Get your API key at https://lab.ollang.com.

## API Base URL

```
https://api-integration.ollang.com
```

## Behavior

1. Identify the user's intent from their message
2. Map it to the correct sub-skill from the table above
3. Read the API key from the `OLLANG_API_KEY` environment variable. If not set, tell the user to set it with: `export OLLANG_API_KEY=<your-api-key>`
4. Execute the operation and present results clearly
5. Suggest logical next steps (e.g., after upload → offer to create an order)
