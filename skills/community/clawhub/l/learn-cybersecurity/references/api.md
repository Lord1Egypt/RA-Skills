# LabEx Cybersecurity API Reference

Base URL: `https://mcp.labex.io`

## Public Routes

Use only these public routes in this skill.

### List Cybersecurity courses

```bash
curl https://mcp.labex.io/learn/cybersecurity/courses
```

Response shape:

```json
{
  "courses": [
    {
      "id": 9660,
      "name": "Kali Linux for Beginners",
      "url": "https://labex.io/courses/kali-linux-for-beginners"
    }
  ]
}
```

### List labs in a Cybersecurity course

```bash
curl https://mcp.labex.io/learn/kali-linux-for-beginners/labs
```

Response shape:

```json
{
  "labs": [
    {
      "id": 552195,
      "name": "Setting Up Your Kali Linux Environment",
      "url": "https://labex.io/labs/kali-setting-up-your-kali-linux-environment-552195"
    }
  ]
}
```

## curl troubleshooting

If `curl` is rejected, add a browser-like `User-Agent` (`-A` or `-H "User-Agent: …"`):

```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://mcp.labex.io/learn/cybersecurity/courses"
```

## Recommendation Rule

Use only the public routes above for this skill.

- Do not ask for credentials.
- Do not use protected routes.
- Do not start or inspect a VM.
- Finish by returning public LabEx lab URLs that the user can open in a browser.
