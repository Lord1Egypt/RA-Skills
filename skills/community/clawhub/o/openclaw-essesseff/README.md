# openclaw-essesseff

> **OpenClaw skill** — install via [ClawHub](https://clawhub.ai)

A comprehensive OpenClaw AgentSkill for the [essesseff](https://www.essesseff.com) DevOps platform. Covers both direct API interaction and shell-script-based app onboarding.

## What This Skill Covers

### essesseff Public API
Full reference for all public API endpoints:
- **Templates** — list and retrieve global and account-specific app templates
- **Organizations** — list and inspect GitHub orgs for your account
- **Apps** — create, list, get, and update essesseff apps
- **Deployments** — query deployment history by environment and status
- **Images** — list container images, get by tag
- **Image Lifecycle** — get current state, drive DEV→RC→QA→STABLE→STAGING→PROD transitions
- **Environments** — get current env deployment, set Argo CD URLs, drive promotion pipeline
- **Packages** — get GitHub API payloads for expired image package deletion
- **Retention Policies** — list and update per-lifecycle-state retention days (BUILD, DEV, RC, QA, STABLE, STAGING, PROD, REJECTED, EXPIRED, etc.)

### essesseff Onboarding Utility
Shell-script automation for:
- Listing available templates
- Creating all 9 essesseff repositories (via API for subscribers, or clone/replace/push for non-subscribers)
- Configuring Argo CD for dev, qa, staging, and/or prod environments

## Install

```bash
npx clawhub@latest install openclaw-essesseff
```

Or via the ClawHub CLI:

```bash
clawhub install openclaw-essesseff
```

## References

| File | Contents |
|---|---|
| `references/api-overview.md` | Auth, base URL, rate limiting, error codes |
| `references/api-templates.md` | Global and account-specific template endpoints |
| `references/api-organizations.md` | Organization list and detail |
| `references/api-apps.md` | App CRUD, deployments, notifications secret |
| `references/api-images.md` | Image list, get by tag, lifecycle get/transition |
| `references/api-environments.md` | Environment status, Argo CD URL, full promotion pipeline |
| `references/api-packages.md` | Expired package deletion payloads |
| `references/api-retention-policies.md` | Retention policy list and update |
| `references/onboarding-utility.md` | Full onboarding utility guide and CLI reference |
| `references/prerequisites.md` | System binaries, PATs, K8s/Argo CD prereqs |
| `references/non-subscriber-mode.md` | Clone/replace/push workflow for non-subscribers |

## Prerequisites

- `curl` — for API calls
- `ESSESSEFF_API_KEY` — from your essesseff team account settings
- For the onboarding utility: `bash` 4.0+, `git`, `jq`; `kubectl` for Argo CD setup

## Quick Start — API

```bash
export ESSESSEFF_API_KEY=ess_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export ACCOUNT=my-team
export ORG=my-apps-org
BASE=https://www.essesseff.com/api/v1

# List global templates
curl -H "X-API-Key: $ESSESSEFF_API_KEY" "$BASE/global/templates"

# Create an app
curl -X POST "$BASE/accounts/$ACCOUNT/organizations/$ORG/apps?app_name=my-app" \
  -H "X-API-Key: $ESSESSEFF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "My Go app",
    "programming_language": "go",
    "template": {
      "template_org_login": "essesseff-hello-world-go-template",
      "source_template_repo": "hello-world",
      "is_global_template": true,
      "replacement_string": "hello-world"
    }
  }'

# Check QA environment
curl -H "X-API-Key: $ESSESSEFF_API_KEY" \
  "$BASE/accounts/$ACCOUNT/organizations/$ORG/apps/my-app/environments/QA"

# Deploy STABLE image to PROD
curl -X POST \
  "$BASE/accounts/$ACCOUNT/organizations/$ORG/apps/my-app/environments/PROD/deploy-stable" \
  -H "X-API-Key: $ESSESSEFF_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"image_tag": "v1.2.3", "deployment_note": "CR#12345"}'
```

## Quick Start — Onboarding Utility

```bash
git clone https://github.com/essesseff/essesseff-onboarding-utility.git
cd essesseff-onboarding-utility
chmod +x essesseff-onboard.sh
cp essesseff-example.txt .essesseff
# fill in .essesseff, then:
./essesseff-onboard.sh --create-app --setup-argocd dev,qa,staging,prod --config-file .essesseff
```

## Security

- Never commit `.essesseff` files — they contain API keys and tokens.
- Delete `notifications-secret.yaml` after applying it to your cluster.
- API keys are only issuable to account owners and DevOps Engineers.

## License

MIT
