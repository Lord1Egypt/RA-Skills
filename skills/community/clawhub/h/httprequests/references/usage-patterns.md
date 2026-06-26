# Usage Patterns

## Supported methods

- GET
- POST
- PUT
- DELETE

## Common patterns

### Simple GET

```powershell
python scripts/request_http.py --method GET --url "https://example.com/api"
```

### GET with headers

```powershell
python scripts/request_http.py --method GET --url "https://example.com/api" --headers '{"Authorization":"Bearer xxx","Accept":"application/json"}'
```

### GET with query params

```powershell
python scripts/request_http.py --method GET --url "https://example.com/search" --params '{"q":"SOL","limit":10}'
```

### POST with JSON body

```powershell
python scripts/request_http.py --method POST --url "https://example.com/api" --headers '{"Content-Type":"application/json"}' --json '{"name":"test"}'
```

### POST with form data

```powershell
python scripts/request_http.py --method POST --url "https://example.com/form" --data '{"username":"demo","password":"secret"}'
```

## Notes

- `--headers`, `--params`, `--json`, and `--data` expect JSON object strings
- Prefer `--json` for JSON APIs
- Prefer `--data` for form submissions
- Use `--show-headers` when response headers matter
- Use `--max-body` to limit large responses
