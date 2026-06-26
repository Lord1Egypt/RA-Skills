---
name: openc3-flow
description: "Get all CI/CD flows from Open-C3 platform. Returns the complete list of flows in the system."
metadata: { "openclaw": { "emoji": "🚀", "requires": { "bins": ["curl", "jq"] } } }
---

# Open-C3 Flow List Skill

Retrieve all CI/CD flows from Open-C3 platform via API.

## Configuration

This skill requires three configuration parameters:

1. **OPEN_C3_URL**: The base URL of your Open-C3 deployment (e.g., `http://192.168.10.67/`)
2. **APP_NAME**: Your application name for API authentication (e.g., `jobx`)
3. **APP_KEY**: Your application key for API authentication

### Setting Up Configuration

Configuration is stored in `config.env` in the skill directory.

## When to Use

✅ **USE this skill when:**
- "Get all flows from the system"
- "List all CI/CD pipelines"
- "Show me all available flows"
- "What flows are configured in Open-C3?"

## API Endpoint

### Get All Flows

```bash
curl -X GET "${OPEN_C3_URL}/api/ci/group/ci/dump" \
  -H "appname: ${APP_NAME}" \
  -H "appkey: ${APP_KEY}"
```

**Response:** Returns a JSON object containing all flows in the system, organized by service tree.

## Examples

**Get all flows:**

```bash
./scripts/list-all-flows.sh
```

**Output Format:**

The script returns a formatted table with:
- Total count of all flows
- Table with columns: ID, Name, Service Tree ID, Service Tree Name, Source Address
- Summary statistics grouped by service tree

## Notes

- All API calls require `appname` and `appkey` headers
- This endpoint returns all flows across all service trees
- Keep your `APP_KEY` secure and never commit it to version control
