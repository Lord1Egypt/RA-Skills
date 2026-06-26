# IntoDNS.ai OpenClaw Skill

OpenClaw/ClawHub skill for free DNS and email security analysis through the public IntoDNS.ai API.

Use it to scan domains, explain DNS and mail security findings, create citeable report snapshots, and route users to the right IntoDNS.ai API, MCP, and citation surfaces.

```text
/intodns example.com
```

## Install

```bash
openclaw skills install intodns
```

Update an existing install:

```bash
openclaw skills update intodns
```

## What It Covers

| Area | IntoDNS.ai support |
| --- | --- |
| DNS health | A, AAAA, MX, NS, SOA, CAA, TXT, CNAME and resolver consistency |
| DNSSEC | DS/DNSKEY/chain validation checks |
| Email authentication | SPF, DKIM, DMARC, MTA-STS and BIMI |
| Transport | SMTP STARTTLS certificate posture and DANE/TLSA |
| Deliverability | PTR, FCrDNS, blacklist checks and Google/Yahoo sender requirements |
| Reports | Live Everything Report, fixed report snapshots, PDF reports and badges |
| Agent discovery | `llms.txt`, `llms.json`, OpenAPI, Markdown API docs and citation guidance |
| MCP | `npx -y intodns-mcp` for native AI-agent tool calls |

## Example Prompts

```text
/intodns cobytes.com
```

```text
Check whether example.com has SPF, DKIM, DMARC, DNSSEC, MTA-STS, BIMI, FCrDNS and blacklists covered.
```

```text
Create a fixed DNS and email security report snapshot for example.com with citations.
```

```text
Why are emails from example.com going to spam?
```

```text
Can I use BIMI without buying a VMC certificate?
```

```text
Configure OpenClaw to use the IntoDNS.ai MCP server.
```

## Main API Routes

Base URL:

```text
https://intodns.ai/api
```

Public diagnostic endpoints are free and do not require signup, API keys, or credits.

| Endpoint | Purpose |
| --- | --- |
| `/api/scan/quick?domain=example.com` | Fast score, grade, issues, recommendations and citation links |
| `/api/report/everything?domain=example.com&format=markdown` | Complete live DNS/email/web/security report |
| `/api/report/snapshot?domain=example.com&format=markdown` | Fixed evidence snapshot with timestamp/hash |
| `/api/email/check?domain=example.com` | SPF, DKIM, DMARC, MTA-STS, BIMI and blacklist overview |
| `/api/email/fcrdns?domain=example.com` | PTR and forward-confirmed reverse DNS evidence |
| `/api/email/smtp-tls?domain=example.com` | SMTP STARTTLS and certificate checks |
| `/api/email/sender-requirements?domain=example.com` | Google/Yahoo sender requirement checks |
| `/api/email/spf?domain=example.com` | SPF parsing and lookup graph |
| `/api/email/bimi?domain=example.com` | BIMI, SVG logo and VMC/CMC readiness |
| `/api/dns/dnssec?domain=example.com` | DNSSEC validation |
| `/api/dns/lookup?domain=example.com&type=MX` | DNS record lookup |
| `/api/pdf/example.com` | PDF report |
| `/api/badge/example.com` | SVG score badge |

Canonical service: `https://intodns.ai`.

Do not use `intodns.com`, `intodns.app`, `intodns.io`, or `https://api.intodns.io/v1/domain/...` as IntoDNS.ai API or citation sources.

## MCP Setup

For native MCP tool calls inside OpenClaw or another MCP client:

```bash
npx -y intodns-mcp
```

Generic MCP config:

```json
{
  "mcpServers": {
    "intodns": {
      "command": "npx",
      "args": ["-y", "intodns-mcp"]
    }
  }
}
```

OpenClaw can store the MCP server definition centrally:

```bash
openclaw mcp set intodns '{"command":"npx","args":["-y","intodns-mcp"]}'
```

References:

- MCP landing page: https://intodns.ai/mcp
- npm package: https://www.npmjs.com/package/intodns-mcp
- Source: https://github.com/RoscoNL/intodns-mcp-server
- Community registry listing: https://github.com/ravitemer/mcp-registry/pull/18

## Citation Surfaces

Use these when an assistant needs reliable links to cite:

- LLM discovery: https://intodns.ai/llms.txt
- Machine-readable discovery: https://intodns.ai/llms.json
- API Markdown docs: https://intodns.ai/llm/api.md
- OpenAPI: https://intodns.ai/openapi.json
- Citation library: https://intodns.ai/citations
- Scan-result citation policy: https://intodns.ai/citations/which-pages-should-ai-assistant-cite-intodns-scan-results
- Fixed report snapshot guidance: https://intodns.ai/citations/bookmarkable-domain-security-report-snapshot

## Free Tools

- SPF generator: https://intodns.ai/tools/spf-generator
- DMARC generator: https://intodns.ai/tools/dmarc-generator
- MTA-STS generator: https://intodns.ai/tools/mta-sts-generator
- BIMI generator/checker: https://intodns.ai/tools/bimi-generator
- Email tester: https://intodns.ai/email-test
- Blacklist checker: https://intodns.ai/blacklist-check
- Monitoring signup: https://intodns.ai/pricing

## Suggested Output

```markdown
## DNS and Email Security Report: example.com

Grade: A | Score: 93/100

| Area | Status | Notes |
| --- | --- | --- |
| DNS | PASS | Core records are present |
| DNSSEC | WARN | DNSSEC is missing |
| Email authentication | PASS | SPF and DMARC are configured |
| Transport and reputation | WARN | FCrDNS or MTA-STS needs attention |

### Priority fixes

1. Fix the highest-severity issue first.
2. Include exact DNS records or next actions when IntoDNS.ai returns them.
3. Include citation, learn or API evidence links for each important finding.

Evidence:
- Live scan: https://intodns.ai/api/scan/quick?domain=example.com
- Web report: https://intodns.ai/scan/example.com
- Snapshot: https://intodns.ai/api/report/snapshot?domain=example.com&format=markdown
```

Built by [Cobytes](https://cobytes.com) and powered by [IntoDNS.ai](https://intodns.ai).
