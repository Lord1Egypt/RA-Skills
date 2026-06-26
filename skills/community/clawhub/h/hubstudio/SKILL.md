---
name: hubstudio-openapi
description: HubStudio OpenAPI skill for full endpoint lookup, request/response field explanation, and parameter constraint checking. Use when querying HubStudio API interfaces, validating request payloads, or building automation against openapi.yaml.
---

# HubStudio Integration Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Configure HubStudio](#configure-hubstudio)
4. [Using API/CLI](#using-apicli)
5. [Connection Details](#connection-details)
6. [Automation Examples](#automation-examples)
7. [FAQ](#faq)
8. [Advanced Usage](#advanced-usage)
9. [ADB Connection Skill](#adb-connection-skill)
10. [Resources](#resources)

---

## Introduction

HubStudio provides browser environment automation, cloud phone operations, environment management, account management, and group management through local APIs.

This Skill is designed to:
- Locate all HubStudio endpoints quickly
- Explain request/response fields and constraints
- Provide safe call patterns for automation
- Standardize API testing and troubleshooting

Core docs:
- Official API docs: [https://api-docs.hubstudio.cn/](https://api-docs.hubstudio.cn/)
- Full local generated reference: [reference.md](reference.md)

---

## Installation

### 1. Install HubStudio Desktop

Install and open HubStudio client on your machine, then log in.

### 2. Verify Local API Service

The current OpenAPI file uses:

```bash
http://127.0.0.1:6873
```

Verify service health with:

```bash
curl -s -X POST "http://127.0.0.1:6873/api/v1/browser/all-browser-status" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 3. Install Optional Tooling

```bash
# API calls and JSON inspection
brew install curl jq

# Python validation scripts
python3 -m pip install --user pyyaml
```

---

## Configure HubStudio

### 1. Login and Prepare Data

1. Login to HubStudio client
2. Ensure browser environments/cloud phones exist
3. Confirm local API is reachable

### 2. Configure Runtime Variables (Optional)

```bash
export HUBSTUDIO_BASE_URL="http://127.0.0.1:6873"
export HUBSTUDIO_AUTH_TOKEN="<your-token-if-needed>"
```

### 3. Timing Notes

- Browser environment startup typically takes **3-5 seconds**
- Cloud phone startup typically takes **30-90 seconds**
- Build retry/timeout logic based on those windows

---

## Using API/CLI

HubStudio OpenAPI in this project contains 56 operations across these domains:
- Browser Environment
- Cloud Phone
- Environment Management
- Account Management
- Group Management

### Recommended Call Pattern

```bash
curl -s -X POST "$HUBSTUDIO_BASE_URL/<endpoint>" \
  -H "Content-Type: application/json" \
  -d '<json-body>'
```

### Node CLI (Direct Execution)

This project includes `hubstudio.js`, so you can execute capabilities directly:

```bash
node hubstudio.js help
node hubstudio.js list
node hubstudio.js browserCreate
node hubstudio.js browserStart 1474900026
node hubstudio.js browserStatus 1474900026
node hubstudio.js browserForeground 1474900026
node hubstudio.js browserArrange
node hubstudio.js browserStop 1474900026
node hubstudio.js testAll
```

`hubstudio.js` now supports all OpenAPI endpoints via generated commands in `commands.generated.json`.
Example generated command:

```bash
node hubstudio.js postV1BrowserStart --body '{"containerCode":"1474900026"}'
```

### Cloud Phone ADB Commands

```bash
# Enable ADB
node hubstudio.js postV1CloudMobileBatchUpdateAdb --body '{"mobileIds":["<mobileId>"],"enableAdb":true}'

# Query ADB connection info
node hubstudio.js postV1CloudMobileListAdb --body '{"mobileIds":["<mobileId>"]}'
```

### Common Browser Environment APIs

```bash
# Open environment
curl -s -X POST "http://127.0.0.1:6873/api/v1/browser/start" \
  -H "Content-Type: application/json" \
  -d '{"containerCode":"1474900026"}'

# Close environment
curl -s -X POST "http://127.0.0.1:6873/api/v1/browser/stop" \
  -H "Content-Type: application/json" \
  -d '{"containerCode":"1474900026"}'

# Get all open environment status
curl -s -X POST "http://127.0.0.1:6873/api/v1/browser/all-browser-status" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Discover Full Endpoint Details

- Open [reference.md](reference.md) for:
  - All endpoints and methods
  - Request/response field descriptions
  - Required fields and constraints
  - Grouped view by tags

---

## Connection Details

### Base URL

From `openapi.yaml`:

```bash
http://127.0.0.1:6873
```

### Response Convention

Most endpoints return:

```json
{
  "code": 0,
  "msg": "Success",
  "data": {}
}
```

Interpretation:
- `code = 0`: success
- non-zero code: business error (missing field, not found, permission, precondition)

---

## Automation Examples

### Example 1: Open Browser Environment

```bash
node hubstudio.js browserStart 1474900026
```

### Example 2: Query Running Browser Environments

```bash
node hubstudio.js browserStatus
```

### Example 3: Smoke Test All OpenAPI Endpoints

```bash
# Current smoke test report (generated previously):
cat scripts/endpoint_test_report.json | jq '.total, .reachable, .transport_fail_count'
```

### Example 4: Validate Skill Completeness

```bash
python3 scripts/validate_completeness.py
```

---

## FAQ

### Q1: API Returns HTTP 200 But Business Failure

This is expected for many endpoints. Check response body `code` and `msg` for business-level result.

### Q2: Environment Open Failed

Check:
1. `containerCode` is correct
2. Environment exists in current account/workspace
3. HubStudio client is logged in and local service is running

### Q3: Why Some Endpoint Tests Fail with Missing Parameters?

Endpoint smoke tests are designed for reachability first. Business failures due to required params/resources are normal unless strict case data is provided.

### Q4: How to Find Required Fields?

Use [reference.md](reference.md). Each endpoint lists:
- Required parameters
- Request body required fields
- Type and constraint details

---

## Advanced Usage

### 1. OpenClaw Integration

In OpenClaw workflows, call HubStudio endpoints directly with structured payloads:

```bash
# Example: open environment
openclaw hubstudio call --path "/api/v1/browser/start" \
  --method POST \
  --body '{"containerCode":"1474900026"}'
```

### 2. Retry Strategy

- Browser environment APIs: retry 1-2 times, interval 2-3 seconds
- Cloud phone APIs: retry 2-4 times, interval 5-10 seconds

### 3. Batch Operations

For batch tasks, iterate IDs with per-item result logging and partial-failure tolerance.

### 4. Validation Loop

1. Update data in `openapi.yaml`
2. Re-generate `reference.md`
3. Run `python3 scripts/validate_completeness.py`
4. Run endpoint smoke tests and inspect `scripts/endpoint_test_report.json`

---

## ADB Connection Skill

Use this capability when the user asks to connect cloud phones through ADB.

- Android 12 / Android 15: direct `adb connect <ip:port>` mode
- Android 13 / Android 14 / Android 15A: SSH tunnel + `adb connect localhost:<port>` mode
- Full guide and command templates: [ADB_CONNECTION_GUIDE.md](ADB_CONNECTION_GUIDE.md)

Execution rule:
1. Ensure cloud phone is powered on
2. Enable ADB via `postV1CloudMobileBatchUpdateAdb`
3. Query ADB info via `postV1CloudMobileListAdb`
4. Choose direct or tunnel workflow by Android version
5. Validate with `adb devices`

---

## Resources

- HubStudio API Docs: [https://api-docs.hubstudio.cn/](https://api-docs.hubstudio.cn/)
- Full Generated API Reference: [reference.md](reference.md)
- ADB workflow details: [ADB_CONNECTION_GUIDE.md](ADB_CONNECTION_GUIDE.md)
- Completeness Checker: `scripts/validate_completeness.py`
- Endpoint Smoke Test Report: `scripts/endpoint_test_report.json`
