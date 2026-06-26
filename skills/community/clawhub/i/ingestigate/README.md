# Ingestigate — OpenClaw Skill

Investigative intelligence for AI agents. This skill gives OpenClaw agents the ability to search document corpuses, extract entities, trace relationship paths, and retrieve evidence — capabilities that are impossible for an agent working with raw files alone.

## Why This Exists

An AI agent can't OCR a scanned passport, parse a blockchain CSV, extract crypto addresses from a PDF, and map how those connect to shell companies in a DOCX — all in one session. The files are too varied, the formats too complex, and the cross-referencing too large for any context window.

Ingestigate handles all of that before the agent ever sees the data. It ingests documents in 1,000+ formats, automatically extracts 30+ entity types (people, organizations, emails, phones, crypto addresses, bank accounts, and more), and builds a relationship graph mapping connections across the entire corpus. The agent gets structured, evidence-backed results through a simple API — not raw files it can't process.

## What the Agent Can Do

- **Search** across all documents with full-text search and faceted filtering
- **Extract entities** — people, organizations, emails, phones, crypto addresses, dates, and 25+ more types
- **Trace relationships** — find connection paths between any two entities across the corpus
- **Retrieve evidence** — get the specific documents where two entities co-occur
- **Upload and process** new document sets through an automated ETL pipeline
- **Monitor processing** — real-time status of document ingestion, entity extraction, and graph building

## Setup

This skill requires two environment variables. Configure them only in your host platform's secure skill settings. Do not paste credential JSON or tokens into chat.

### Step 1: Create an account (if you don't have one)

Visit [app1.ingestigate.com/agentic-registration](https://app1.ingestigate.com/agentic-registration) and complete the registration form. You'll need to verify your email and set up multi-factor authentication (MFA) using an app like Microsoft Authenticator or Google Authenticator.

### Step 2: Generate credentials

Log in and visit [app1.ingestigate.com/search/agentic-token](https://app1.ingestigate.com/search/agentic-token). Click **Generate Credentials**. This produces a JSON containing your access token and API base URL.

### Step 3: Configure the environment variables

From the credential JSON, copy these two values into your host platform's secure skill settings:

| Variable | Value | Source field in credential JSON |
|----------|-------|-------------------------------|
| `INGESTIGATE_TOKEN` | Your access token | `access_token` |
| `INGESTIGATE_BASE_URL` | API base URL | `api_base_url` |

### Token expiry

The access token expires in **30 minutes**. When it expires, the agent will tell you. Generate a new token at the same URL and update `INGESTIGATE_TOKEN` in your platform settings.

### Advanced: Full developer guide

For advanced usage (upload workflows, NER processing, structured data endpoints, pagination), an authenticated agent can fetch the full developer guide from the API at `/api/agent/guide`. This is optional — the core investigative workflow is built into the skill.

## Plans

| Plan | Agentic API Calls/Day | Price |
|------|----------------------|-------|
| Trial | 50 | Free for 14 days |
| Starter | 300 | $49/month |
| Professional | Unlimited | $1,999/month |
| Enterprise | Unlimited | Custom |

## Security

- **No persistent API keys.** Short-lived access tokens only (30-minute expiry). When the token expires, it is worthless.
- **Organization-scoped data isolation.** Every agent action is scoped to the user's exact permissions. No cross-organization data leakage.
- **Full audit trail.** Every action the agent takes is traceable to a specific authenticated user.
- **MFA required.** All accounts use multi-factor authentication.
- **Processing-aware responses.** API responses include corpus readiness signals so agents never report conclusions from incomplete data.
- **Air-gapped deployment available** for government, defense, and regulated industries.

## Links

- [Ingestigate](https://ingestigate.com)
- [Agent Developer Guide](https://app1.ingestigate.com/api/agent/guide) (requires authentication)

## License

This skill wrapper is licensed under [MIT-0](https://opensource.org/license/mit-0) (MIT No Attribution). The Ingestigate platform and API are proprietary.
