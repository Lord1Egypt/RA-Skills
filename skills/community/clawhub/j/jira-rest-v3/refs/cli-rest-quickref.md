# CLI REST Quick Reference for openClaw Jira Skill

This quick reference gives openClaw a concrete, repeatable pattern for performing Jira Cloud REST calls from the command line.

Use this file whenever the agent drifts into abstract API explanation instead of executing a real request.

---

## 1) Core rule
For every `jira.*` task:
1. choose the endpoint
2. build the URL
3. create headers
4. create JSON body file if needed
5. execute the HTTP call from CLI
6. parse the JSON result

Do not stop after describing the endpoint.

---

## 2) Linux Bash helper
```bash
jira_api() {
  local method="$1"
  local path="$2"
  local query="${3:-}"
  local body_file="${4:-}"

  : "${ATREST_JIRA_BASE_URL:?Missing ATREST_JIRA_BASE_URL}"
  : "${ATREST_JIRA_AUTH_MODE:?Missing ATREST_JIRA_AUTH_MODE}"

  local base="${ATREST_JIRA_BASE_URL%/}"
  local ua="${ATREST_JIRA_USER_AGENT:-openClaw-jira-atrest/1.0}"
  local auth_header

  if [ "$ATREST_JIRA_AUTH_MODE" = "basic" ]; then
    : "${ATREST_JIRA_EMAIL:?Missing ATREST_JIRA_EMAIL}"
    : "${ATREST_JIRA_API_TOKEN:?Missing ATREST_JIRA_API_TOKEN}"
    auth_header="Authorization: Basic $(printf '%s' "${ATREST_JIRA_EMAIL}:${ATREST_JIRA_API_TOKEN}" | base64 | tr -d '\n')"
  elif [ "$ATREST_JIRA_AUTH_MODE" = "bearer" ]; then
    : "${ATREST_JIRA_BEARER_TOKEN:?Missing ATREST_JIRA_BEARER_TOKEN}"
    auth_header="Authorization: Bearer ${ATREST_JIRA_BEARER_TOKEN}"
  else
    echo "Unsupported auth mode: $ATREST_JIRA_AUTH_MODE" >&2
    return 1
  fi

  local url="${base}${path}"
  if [ -n "$query" ]; then
    url="${url}?${query}"
  fi

  if [ -n "$body_file" ]; then
    curl --silent --show-error --fail \
      --request "$method" \
      --url "$url" \
      --header "Accept: application/json" \
      --header "Content-Type: application/json" \
      --header "$auth_header" \
      --header "User-Agent: $ua" \
      --data-binary "@$body_file"
  else
    curl --silent --show-error --fail \
      --request "$method" \
      --url "$url" \
      --header "Accept: application/json" \
      --header "$auth_header" \
      --header "User-Agent: $ua"
  fi
}
```

### Linux examples
#### Get one issue
```bash
jira_api GET "/rest/api/3/issue/PROJ-123" "fields=summary,status,assignee,updated"
```

#### Search with JQL
```bash
JQL_ENC=$(python - <<'PY'
import urllib.parse
print(urllib.parse.urlencode({
    'jql': 'project = PROJ AND statusCategory != Done ORDER BY updated DESC',
    'maxResults': '50',
    'fields': 'summary,status,assignee,priority,updated'
}))
PY
)

jira_api GET "/rest/api/3/search/jql" "$JQL_ENC"
```

#### Create issue
```bash
cat > /tmp/jira-create.json <<'JSON'
{
  "fields": {
    "project": { "key": "PROJ" },
    "issuetype": { "name": "Task" },
    "summary": "Create from Linux helper"
  }
}
JSON

jira_api POST "/rest/api/3/issue" "" "/tmp/jira-create.json"
```

---

## 3) Windows PowerShell helper
```powershell
function Invoke-JiraApi {
    param(
        [Parameter(Mandatory=$true)][string]$Method,
        [Parameter(Mandatory=$true)][string]$Path,
        [string]$Query = '',
        [string]$BodyFile = ''
    )

    if (-not $env:ATREST_JIRA_BASE_URL) { throw 'Missing ATREST_JIRA_BASE_URL' }
    if (-not $env:ATREST_JIRA_AUTH_MODE) { throw 'Missing ATREST_JIRA_AUTH_MODE' }

    $base = $env:ATREST_JIRA_BASE_URL.TrimEnd('/')
    $ua   = if ($env:ATREST_JIRA_USER_AGENT) { $env:ATREST_JIRA_USER_AGENT } else { 'openClaw-jira-atrest/1.0' }

    if ($env:ATREST_JIRA_AUTH_MODE -eq 'basic') {
        if (-not $env:ATREST_JIRA_EMAIL) { throw 'Missing ATREST_JIRA_EMAIL' }
        if (-not $env:ATREST_JIRA_API_TOKEN) { throw 'Missing ATREST_JIRA_API_TOKEN' }
        $pair = "{0}:{1}" -f $env:ATREST_JIRA_EMAIL, $env:ATREST_JIRA_API_TOKEN
        $basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($pair))
        $auth = "Basic $basic"
    }
    elseif ($env:ATREST_JIRA_AUTH_MODE -eq 'bearer') {
        if (-not $env:ATREST_JIRA_BEARER_TOKEN) { throw 'Missing ATREST_JIRA_BEARER_TOKEN' }
        $auth = "Bearer $($env:ATREST_JIRA_BEARER_TOKEN)"
    }
    else {
        throw "Unsupported auth mode: $($env:ATREST_JIRA_AUTH_MODE)"
    }

    $headers = @{
        Accept        = 'application/json'
        Authorization = $auth
        'User-Agent'  = $ua
    }

    $uri = if ($Query) { "$base$Path?$Query" } else { "$base$Path" }

    if ($BodyFile) {
        $headers['Content-Type'] = 'application/json'
        Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers -Body (Get-Content -Path $BodyFile -Raw)
    }
    else {
        Invoke-RestMethod -Method $Method -Uri $uri -Headers $headers
    }
}
```

### Windows examples
#### Get one issue
```powershell
Invoke-JiraApi -Method Get -Path '/rest/api/3/issue/PROJ-123' -Query 'fields=summary,status,assignee,updated'
```

#### Search with JQL
```powershell
$jql = [uri]::EscapeDataString('project = PROJ AND statusCategory != Done ORDER BY updated DESC')
Invoke-JiraApi -Method Get -Path '/rest/api/3/search/jql' -Query "jql=$jql&maxResults=50&fields=summary,status,assignee,priority,updated"
```

#### Create issue
```powershell
$payload = @{
  fields = @{
    project   = @{ key = 'PROJ' }
    issuetype = @{ name = 'Task' }
    summary   = 'Create from Windows helper'
  }
} | ConvertTo-Json -Depth 20

$tmp = Join-Path $env:TEMP 'jira-create.json'
Set-Content -Path $tmp -Value $payload -Encoding UTF8
Invoke-JiraApi -Method Post -Path '/rest/api/3/issue' -BodyFile $tmp
```

---

## 4) curl on Windows
Use `curl.exe`, not bare `curl`, to avoid the PowerShell alias confusion.

```powershell
curl.exe --silent --show-error --fail `
  --request GET `
  --url "$env:ATREST_JIRA_BASE_URL/rest/api/3/project/search?maxResults=5" `
  --header "Accept: application/json" `
  --header "Authorization: Basic <base64(email:token)>"
```

---

## 5) Safer write pattern
For POST and PUT:
- generate JSON with the shell language
- write JSON to a temp file
- send it with `--data-binary @file` or `Get-Content -Raw`

This is much more reliable than trying to keep large JSON literals correctly quoted inline.

---

## 6) Recommended connectivity self-test
Use one of these before complicated workflows:
- `GET /rest/api/3/myself`
- `GET /rest/api/3/project/search?maxResults=1`

If this fails, fix environment variables or permissions first.
