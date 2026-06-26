# LabEx Python Programming API Reference

Base URL: `https://mcp.labex.io`

## Public Routes

Use only these public routes in this skill.

### List Python programming courses

```bash
curl https://mcp.labex.io/learn/python/courses
```

Response shape:

```json
{
  "courses": [
    {
      "id": 1419,
      "name": "Quick Start with Python",
      "url": "https://labex.io/courses/quick-start-with-python"
    }
  ]
}
```

### List labs in a Python programming course

```bash
curl https://mcp.labex.io/learn/quick-start-with-python/labs
```

Response shape:

```json
{
  "labs": [
    {
      "id": 270256,
      "name": "Your First Python Lab",
      "url": "https://labex.io/labs/python-your-first-python-lab-270256"
    }
  ]
}
```

## curl troubleshooting

If `curl` is rejected, add a browser-like `User-Agent` (`-A` or `-H "User-Agent: …"`):

```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://mcp.labex.io/learn/python/courses"
```

## Recommendation Rule

Use only the public routes above for this skill.

- Do not ask for credentials.
- Do not use protected routes.
- Do not start or inspect a VM.
- Finish by returning public LabEx lab URLs that the user can open in a browser.
