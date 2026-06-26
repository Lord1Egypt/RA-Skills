# LabEx Linux API Reference

Base URL: `https://mcp.labex.io`

## Public Routes

Use only these public routes in this skill.

### List Linux courses

```bash
curl https://mcp.labex.io/learn/linux/courses
```

Response shape:

```json
{
  "courses": [
    {
      "id": 1427,
      "name": "Quick Start with Linux",
      "url": "https://labex.io/courses/quick-start-with-linux"
    }
  ]
}
```

### List labs in a Linux course

```bash
curl https://mcp.labex.io/learn/quick-start-with-linux/labs
```

Response shape:

```json
{
  "labs": [
    {
      "id": 270253,
      "name": "Your First Linux Lab",
      "url": "https://labex.io/labs/linux-your-first-linux-lab-270253"
    }
  ]
}
```

## curl troubleshooting

If `curl` is rejected, add a browser-like `User-Agent` (`-A` or `-H "User-Agent: …"`):

```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://mcp.labex.io/learn/linux/courses"
```

## Recommendation Rule

Use only the public routes above for this skill.

- Do not ask for credentials.
- Do not use protected routes.
- Do not start or inspect a VM.
- Finish by returning public LabEx lab URLs that the user can open in a browser.
