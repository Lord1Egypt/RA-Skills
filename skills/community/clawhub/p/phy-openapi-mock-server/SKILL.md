---
name: OpenAPI Mock Server
description: Instant mock HTTP server from any OpenAPI 3.x or Swagger 2.0 spec. Point it at a spec file (local or URL) and get a live local server returning spec-compliant example responses — no backend code required. Wraps Stoplight Prism CLI with smart defaults. Validates the spec before starting, prints all available endpoints with example curl commands, supports validation mode (rejects non-spec requests), dynamic example selection, and auth bypass for local dev. Perfect for frontend teams blocked on a backend, contract-first API development, and integration testing without a live service. Zero external API — uses only npx and your local spec file. Triggers on "mock API", "mock server", "openapi mock", "swagger mock", "fake backend", "stub server", "contract-first", "/openapi-mock".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - openapi
    - swagger
    - mock-server
    - api-development
    - contract-first
    - frontend-development
    - testing
    - developer-tools
    - prism
    - local-dev
---

# OpenAPI Mock Server

Frontend blocked waiting for the backend? Need to test against an API that doesn't exist yet? Your spec is the source of truth — this skill turns it into a running HTTP server in one command.

Point it at any OpenAPI 3.x or Swagger 2.0 spec and get a live local mock server that returns spec-compliant responses, validates incoming requests, and shows you every available endpoint with ready-to-run curl commands.

**No backend code. No Docker. No config. Just `npx` and your spec.**

---

## Trigger Phrases

- "mock API", "mock server from spec", "openapi mock", "swagger mock"
- "fake backend", "stub server", "contract-first development"
- "I need a local API", "frontend needs a backend stub"
- "mock this endpoint", "start a mock server"
- "test against a spec", "Prism mock server"
- "/openapi-mock"

---

## How to Provide Input

```bash
# Option 1: Local spec file
/openapi-mock openapi.yaml
/openapi-mock swagger.json
/openapi-mock api/spec/openapi.yaml

# Option 2: Spec URL (fetched once, served locally)
/openapi-mock https://petstore3.swagger.io/api/v3/openapi.json

# Option 3: Custom port
/openapi-mock openapi.yaml --port 4010

# Option 4: Validation mode (reject requests that don't match the spec)
/openapi-mock openapi.yaml --validate

# Option 5: Dynamic mode (generate random examples, not just first example)
/openapi-mock openapi.yaml --dynamic

# Option 6: Show all endpoints without starting server
/openapi-mock openapi.yaml --list

# Option 7: Mock a specific tag or path only
/openapi-mock openapi.yaml --filter /users
/openapi-mock openapi.yaml --filter tag:payments
```

---

## Step 1: Validate the Spec

Before starting the server, validate the spec file is syntactically correct:

```bash
# Check spec file exists and has correct extension
SPEC_FILE="$1"
if [ ! -f "$SPEC_FILE" ] && [[ "$SPEC_FILE" != http* ]]; then
  echo "ERROR: Spec file not found: $SPEC_FILE"
  echo "Looking for spec files in current directory..."
  find . -maxdepth 3 -name "openapi.yaml" -o -name "openapi.json" \
    -o -name "swagger.yaml" -o -name "swagger.json" \
    -not -path "*/node_modules/*" 2>/dev/null | head -10
  exit 1
fi

# Validate spec format (YAML or JSON)
if [[ "$SPEC_FILE" == *.yaml ]] || [[ "$SPEC_FILE" == *.yml ]]; then
  python3 -c "import yaml,sys; yaml.safe_load(open('$SPEC_FILE'))" 2>&1 && echo "✅ YAML syntax valid" || echo "❌ YAML syntax error"
elif [[ "$SPEC_FILE" == *.json ]]; then
  python3 -c "import json,sys; json.load(open('$SPEC_FILE'))" 2>&1 && echo "✅ JSON syntax valid" || echo "❌ JSON syntax error"
fi

# Check it's actually an OpenAPI/Swagger spec
python3 -c "
import yaml, json, sys
try:
    with open('$SPEC_FILE') as f:
        spec = yaml.safe_load(f) if '$SPEC_FILE'.endswith(('.yaml','.yml')) else json.load(f)
    version = spec.get('openapi', spec.get('swagger', 'unknown'))
    title = spec.get('info', {}).get('title', 'Untitled')
    paths = len(spec.get('paths', {}))
    print(f'✅ OpenAPI {version} | {title} | {paths} paths')
except Exception as e:
    print(f'❌ Not a valid OpenAPI spec: {e}')
    sys.exit(1)
"
```

---

## Step 2: Install Prism (if needed)

```bash
# Check if Prism is already installed
if command -v prism &>/dev/null; then
  echo "✅ Prism already installed: $(prism --version)"
elif npx --yes @stoplight/prism-cli@latest --version &>/dev/null 2>&1; then
  echo "✅ Prism available via npx"
else
  echo "Installing Prism..."
  npm install -g @stoplight/prism-cli
  # Or: yarn global add @stoplight/prism-cli
  # Or: npx -p @stoplight/prism-cli prism (no install needed)
fi
```

**Requirements:** Node.js 16+ (check with `node --version`)

**Alternative if Node.js not available:**
```bash
# Docker alternative (no Node.js required)
docker run --rm -p 4010:4010 \
  -v "$(pwd):/tmp/spec" \
  stoplight/prism:latest \
  mock /tmp/spec/openapi.yaml -h 0.0.0.0
```

---

## Step 3: Extract Endpoint Inventory

Before starting, show all endpoints the mock server will serve:

```bash
python3 -c "
import yaml, json, sys

spec_file = '$SPEC_FILE'
with open(spec_file) as f:
    spec = yaml.safe_load(f) if spec_file.endswith(('.yaml','.yml')) else json.load(f)

paths = spec.get('paths', {})
base_url = 'http://localhost:4010'

print(f'\n📋 Available Endpoints ({len(paths)} paths):')
print('=' * 60)

for path, path_item in sorted(paths.items()):
    for method in ['get','post','put','patch','delete','head','options']:
        op = path_item.get(method)
        if not op:
            continue
        summary = op.get('summary', op.get('operationId', ''))
        responses = list(op.get('responses', {}).keys())
        print(f'  {method.upper():8} {path}')
        if summary:
            print(f'           → {summary}')
        print(f'           Returns: {responses}')
        print()
"
```

---

## Step 4: Start the Mock Server

```bash
PORT=${PORT:-4010}
SPEC_FILE="$1"
VALIDATE_FLAG=""
DYNAMIC_FLAG=""

# Parse options
while [[ $# -gt 1 ]]; do
  case "$2" in
    --validate) VALIDATE_FLAG="--validate-request" ;;
    --dynamic)  DYNAMIC_FLAG="--dynamic" ;;
    --port)     PORT="$3"; shift ;;
  esac
  shift
done

echo ""
echo "🚀 Starting mock server..."
echo "   Spec:  $SPEC_FILE"
echo "   URL:   http://localhost:$PORT"
echo "   Mode:  $([ -n "$VALIDATE_FLAG" ] && echo 'validation (rejects bad requests)' || echo 'passthrough (allows any request)')"
echo ""

# Start Prism mock server
npx --yes @stoplight/prism-cli mock "$SPEC_FILE" \
  --port "$PORT" \
  --host 127.0.0.1 \
  $VALIDATE_FLAG \
  $DYNAMIC_FLAG \
  --errors
```

**What Prism does:**
- Reads your spec's `example` / `examples` values for each response → returns them verbatim
- If no example is defined → generates a value from the schema (string → `"string"`, integer → `0`, etc.)
- With `--dynamic` → generates random values matching the schema on every request
- With `--validate-request` → returns `422` for requests that don't match the spec's request body schema

---

## Step 5: Generate Test curl Commands

After starting, output ready-to-run curl commands for every endpoint:

```bash
python3 -c "
import yaml, json

spec_file = '$SPEC_FILE'
with open(spec_file) as f:
    spec = yaml.safe_load(f) if spec_file.endswith(('.yaml','.yml')) else json.load(f)

paths = spec.get('paths', {})
components = spec.get('components', {}).get('schemas', {})
base = 'http://localhost:4010'

print('\n📡 Test Commands:\n')

for path, path_item in sorted(paths.items()):
    for method in ['get','post','put','patch','delete']:
        op = path_item.get(method)
        if not op:
            continue

        # Replace path params with example values
        test_path = path
        for param in op.get('parameters', []) + path_item.get('parameters', []):
            if param.get('in') == 'path':
                example = param.get('example', param.get('schema', {}).get('example', '1'))
                test_path = test_path.replace('{' + param['name'] + '}', str(example))

        # Build query string for GET
        query_params = []
        if method == 'get':
            for param in op.get('parameters', []):
                if param.get('in') == 'query' and param.get('required'):
                    example = param.get('example', param.get('schema', {}).get('example', 'value'))
                    query_params.append(f'{param[\"name\"]}={example}')

        url = f'{base}{test_path}'
        if query_params:
            url += '?' + '&'.join(query_params)

        # Build request body hint for POST/PUT/PATCH
        body_hint = ''
        req_body = op.get('requestBody', {})
        if req_body and method in ['post', 'put', 'patch']:
            body_hint = \" -H 'Content-Type: application/json' -d '{}'\"

        summary = op.get('summary', '')
        print(f'# {summary}' if summary else '')
        print(f'curl -s -X {method.upper()} \"{url}\"{body_hint} | python3 -m json.tool')
        print()
"
```

---

## Step 6: Output Report

```markdown
## Mock Server Ready
Spec: openapi.yaml (OpenAPI 3.0.3 — Petstore API)
Server: http://localhost:4010
Mode: Passthrough (use --validate to reject invalid requests)

---

### Available Endpoints (12 total)

| Method | Path | Summary | Returns |
|--------|------|---------|---------|
| GET | /pets | List all pets | 200, 400 |
| POST | /pets | Create a pet | 201, default |
| GET | /pets/{petId} | Info for a specific pet | 200, default |
| DELETE | /pets/{petId} | Delete a pet | 204, default |
| GET | /users | List users | 200 |
| POST | /users | Create user | 201, 409 |
| GET | /users/{id} | Get user by ID | 200, 404 |
| PUT | /users/{id} | Update user | 200, 404, 422 |

---

### Quick Test Commands

```bash
# List all pets
curl -s -X GET "http://localhost:4010/pets" | python3 -m json.tool

# Get specific pet
curl -s -X GET "http://localhost:4010/pets/1" | python3 -m json.tool

# Create a pet (replace {} with actual body)
curl -s -X POST "http://localhost:4010/pets" \
  -H "Content-Type: application/json" \
  -d '{"name": "Buddy", "tag": "dog"}' | python3 -m json.tool

# Test a 404 response
curl -s -X GET "http://localhost:4010/pets/99999" | python3 -m json.tool
# → Prism returns the spec's 'default' response example

# Test validation mode rejection
curl -s -X POST "http://localhost:4010/pets" \
  -H "Content-Type: application/json" \
  -d '{"invalid_field": true}' | python3 -m json.tool
# → Returns 422 with validation error details
```

---

### Tips

**Force a specific response code:**
```bash
# Tell Prism which response code to return via header
curl -H "Prefer: code=404" http://localhost:4010/pets/1
curl -H "Prefer: code=500" http://localhost:4010/pets/1
```

**Force dynamic example generation:**
```bash
curl -H "Prefer: dynamic=true" http://localhost:4010/pets
# → Returns random values matching the schema on every request
```

**Test auth-protected endpoints (bypass in local dev):**
```bash
# Prism doesn't enforce auth by default — just send the header
curl -H "Authorization: Bearer fake-token-for-local-dev" http://localhost:4010/users/me
```

---

### Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `Error: Cannot read property 'responses'` | Spec has invalid path | Check yaml syntax around that path |
| `422 Request body invalid` | `--validate` mode on, bad request | Either fix your request or remove `--validate` for dev |
| Empty response body `{}` | No `example` in spec for that field | Add `example:` values to your spec, or use `--dynamic` |
| Port 4010 in use | Another process | Use `--port 4011` |
| `npx: command not found` | Node.js not installed | Install Node.js 16+ or use the Docker alternative |
```

---

## Advanced: Adding Examples to Your Spec

Prism returns the best response when your spec has `example` values. If responses look empty:

```yaml
# Before (no examples — Prism returns minimal defaults)
paths:
  /users/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

# After (Prism returns this exact object)
paths:
  /users/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
              example:
                id: "usr_abc123"
                email: "alice@example.com"
                name: "Alice Smith"
                created_at: "2026-01-15T10:30:00Z"
```

---

## Workflow: Contract-First Development

The full parallel-development workflow this skill enables:

```
Day 1: Team agrees on API contract → openapi.yaml committed to repo
         ↓
Backend team: implements real API
Frontend team: /openapi-mock openapi.yaml → developing against mock server

Day 14: Backend is ready
Frontend: Change API_BASE_URL from http://localhost:4010 to https://api.yourapp.com
         → Integration works immediately (both sides built to the same contract)
```

```bash
# In your frontend .env.local
NEXT_PUBLIC_API_URL=http://localhost:4010   # Mock during dev
# NEXT_PUBLIC_API_URL=https://api.prod.com  # Uncomment for production
```

---

## Alternative: Mockoon CLI (no Node.js required)

If you prefer a binary over npx:

```bash
# Install Mockoon CLI
npm install -g @mockoon/cli

# Start mock server from OpenAPI spec
mockoon-cli start --data openapi.yaml --port 4010

# Or use the Mockoon GUI to visually edit mock responses
# → Export as Mockoon data file → then use CLI
```

---

## Comparison

| Tool | Approach | Best For |
|------|---------|---------|
| **Prism** (this skill) | CLI, OpenAPI-native, spec-driven | Contract-first teams, CI validation |
| **Mockoon** | GUI + CLI, visual editor | Teams who want to hand-edit mock responses |
| **MSW** | In-browser/Node service worker | Unit/integration tests in JS — not a real HTTP server |
| **WireMock** | Java, powerful but heavy | Enterprise teams, complex stateful mocks |
| **json-server** | REST from JSON file | Simple CRUD prototypes (no spec enforcement) |

**This skill** covers the most common case: you have a spec, you need a server, you need it now.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
