---
name: navil-policy
description: Reduce MCP token costs by up to 94% and enforce least-privilege tool access. Creates YAML policies that control which MCP tools each agent can see and call. Use when user mentions token costs, context window bloat, too many tools, tool scoping, reducing tokens, saving money on API calls, least privilege, restricting tool access, creating access policies, or agent permissions. Also when user says "my context window is full" or "too many tool schemas" or "MCP is too expensive".
version: 1.0.2
metadata:
  openclaw:
    emoji: "📋"
    homepage: https://github.com/navilai/navil
    requires:
      bins:
        - pip
    install:
      - id: pip-navil
        kind: pip
        package: navil
        bins: [navil]
        label: "Install Navil policy engine"
---

# Navil Policy — MCP Tool Scoping and Cost Optimization

GitHub's MCP server exposes 90+ tools consuming 50,000+ tokens before your agent thinks about your question. At scale, MCP tool definitions can exceed model context limits entirely.

Navil Policy solves this by controlling which tools each agent **sees** in `tools/list` responses. A code review agent sees 3 tools instead of 90. That is a 94% reduction in schema tokens — cheaper inference, faster responses, and a smaller attack surface.

## When to Use This Skill

- User complains about token costs or context window bloat from MCP
- User has multiple MCP servers and agents are seeing too many tools
- User wants to restrict which tools specific agents can access
- User says "MCP is too expensive" or "my context is full of tool schemas"
- User asks about least privilege, tool scoping, or agent permissions
- User wants to auto-generate policies from observed agent behavior

## How Tool Scoping Works

Navil's policy engine sits in the proxy layer (set up by navil-shield). When an agent requests `tools/list`, Navil filters the response based on the policy file before the agent ever sees it.

This means:
- **The agent doesn't know** the filtered tools exist — they never enter the context window
- **Token savings are immediate** — fewer tool schemas = less context consumed
- **Security improves** — agents can't call tools they can't see
- **No code changes** — the policy file controls everything

## Creating a Policy

### Step 1: Check if Navil Shield is Active

```bash
navil --version
```

If navil is not installed, install it first:

```bash
pip install navil --break-system-packages 2>/dev/null || pip install navil
```

If MCP servers are not yet wrapped with navil shim, the policy engine cannot filter tool lists. Recommend installing navil-shield first.

### Step 2: Observe Current Tool Usage

To see what tools are currently being exposed to agents:

```bash
navil policy check --tool "*" --agent default --action list
```

### Step 3: Generate a Starter Policy

Navil can auto-generate policies by watching how agents actually use tools:

```bash
navil policy auto-generate
```

This creates `~/.navil/policy.auto.yaml` based on observed baselines. Review it, then copy rules you want to keep into `~/.navil/policy.yaml`.

### Step 4: Write Custom Policy

For manual policy creation, create `~/.navil/policy.yaml`:

```yaml
# Example: Scope tools by workflow
scopes:
  code-review:
    allow:
      - get_pull_request
      - list_files
      - create_review_comment
    description: "Code review agent sees only PR-related tools"

  deploy:
    allow:
      - create_deployment
      - get_deployment_status
    description: "Deploy agent sees only deployment tools"

  read-only:
    allow:
      - get_*
      - list_*
      - search_*
    description: "Read-only agents cannot modify anything"

  default:
    allow: "*"
    description: "Backward compatible — unrestricted access"

# Rate limiting per agent
rate_limits:
  default:
    requests_per_minute: 60
  deploy:
    requests_per_minute: 10
```

### Step 5: Apply and Test

```bash
navil policy check --tool create_deployment --agent code-review --action call
# Expected: DENIED — code-review scope doesn't include deployment tools

navil policy check --tool get_pull_request --agent code-review --action call
# Expected: ALLOWED
```

### Step 6: Monitor Policy Decisions

View the live decision log to verify policies are working:

```bash
navil policy suggest
```

This shows pending auto-generated rules with confidence scores. Accept the ones that make sense.

### Step 7: Rollback if Needed

```bash
navil policy rollback
```

This undoes auto-generated policy changes. Your manually written `policy.yaml` is never modified by the auto-generator.

## Token Savings Calculator

Present this to the user when they ask about cost:

| Scenario | Tools Exposed | Approx Schema Tokens | With Navil Scoping | Savings |
|----------|--------------|---------------------|-------------------|---------|
| GitHub MCP (all tools) | 90+ | ~50,000 | 3 tools (~1,600) | **97%** |
| Database MCP | 106 | ~54,600 | 8 tools (~4,100) | **92%** |
| Full enterprise stack (5 servers) | 300+ | ~150,000+ | 20 tools (~10,000) | **93%** |

At typical API pricing, scoping a heavy MCP setup saves $50-200/month in token costs alone.

## Policy Templates

Navil ships with community templates for common MCP servers. Ask the user which servers they use, then suggest the appropriate template:

- **GitHub MCP**: Read-only, code-review, full-access scopes
- **Filesystem MCP**: Read-only, workspace-scoped, full-access scopes
- **kubectl MCP**: View-only, namespace-scoped, admin scopes

## Important Notes

- `policy.yaml` (manual rules) **always takes precedence** over `policy.auto.yaml` (generated rules)
- Policies filter what agents **see** in `tools/list`, separate from what they can **call**
- The `default` scope with `allow: "*"` ensures backward compatibility
- Scoped responses are cached with 60s TTL in the Rust proxy — near-zero performance cost

## Links

- Policy documentation: https://github.com/navilai/navil#tool-scoping
- Community policy templates: https://github.com/navilai/navil/tree/main/policies
- Token cost guide: https://navil.ai/docs/token-costs
