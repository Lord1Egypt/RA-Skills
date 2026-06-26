# LabEx DevOps API Reference

Base URL: `https://mcp.labex.io`

## Public Routes

Use only these public routes in this skill.

### List DevOps courses

```bash
curl https://mcp.labex.io/learn/devops/courses
```

Response shape:

```json
{
  "courses": [
    {
      "id": 1424,
      "name": "Docker for Beginners",
      "url": "https://labex.io/courses/docker-for-beginners"
    }
  ]
}
```

### List labs in a DevOps course

```bash
curl https://mcp.labex.io/learn/docker-for-beginners/labs
```

Response shape:

```json
{
  "labs": [
    {
      "id": 92719,
      "name": "Your First Docker Lab",
      "url": "https://labex.io/labs/docker-your-first-docker-lab-92719"
    }
  ]
}
```

## curl troubleshooting

If `curl` is rejected, add a browser-like `User-Agent` (`-A` or `-H "User-Agent: …"`):

```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://mcp.labex.io/learn/devops/courses"
```

## Recommendation Rule

Use only the public routes above for this skill.

- Do not ask for credentials.
- Do not use protected routes.
- Do not start or inspect a VM.
- Finish by returning public LabEx lab URLs that the user can open in a browser.
