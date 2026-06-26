# LabEx Ansible API Reference

Base URL: `https://mcp.labex.io`

## Public Routes

Use only these public routes in this skill.

### List Ansible courses

```bash
curl https://mcp.labex.io/learn/ansible/courses
```

Response shape:

```json
{
  "courses": [
    {
      "id": 9860,
      "name": "Red Hat Enterprise Linux Automation with Ansible (RH294) Certification Labs",
      "url": "https://labex.io/courses/red-hat-enterprise-linux-automation-with-ansible-rh294"
    }
  ]
}
```

### List labs in a Ansible course

```bash
curl https://mcp.labex.io/learn/red-hat-enterprise-linux-automation-with-ansible-rh294/labs
```

Response shape:

```json
{
  "labs": [
    {
      "id": 590544,
      "name": "Install Ansible on Red Hat Enterprise Linux",
      "url": "https://labex.io/labs/rhel-install-ansible-on-red-hat-enterprise-linux-590544"
    }
  ]
}
```

## curl troubleshooting

If `curl` is rejected, add a browser-like `User-Agent` (`-A` or `-H "User-Agent: …"`):

```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://mcp.labex.io/learn/ansible/courses"
```

## Recommendation Rule

Use only the public routes above for this skill.

- Do not ask for credentials.
- Do not use protected routes.
- Do not start or inspect a VM.
- Finish by returning public LabEx lab URLs that the user can open in a browser.
