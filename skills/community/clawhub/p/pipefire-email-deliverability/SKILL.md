---
name: pipefire-email-deliverability
description: Free email deliverability checks from Pipefire. SPF, DKIM, DMARC, MX, blacklists, email headers, DNS record builders, cold email scoring.
version: 1.0.0
homepage: https://pipefire.ai/mcp-server
metadata:
  openclaw:
    emoji: "📬"
    homepage: https://pipefire.ai/mcp-server
    requires:
      bins:
        - curl
---

# Pipefire email deliverability tools

Free tools from [Pipefire](https://pipefire.ai), cold email software for agencies. They answer the questions people ask when email lands in spam or a new domain is being set up: is SPF right, is DKIM published, what does DMARC say, is the domain on a blacklist, why did this message fail.

No API key and no account. Every tool runs on Pipefire's public MCP server:

```
https://pipefire.ai/mcp
```

## Setup

Nothing to install or sign up for. The tools are free and need no key.

- To connect it as an MCP server instead, add `https://pipefire.ai/mcp` as a remote server (streamable HTTP, no auth). Details: https://pipefire.ai/mcp-server
- To try Pipefire itself on real leads in your niche, get 50 free leads: https://pipefire.ai/tools/free-leads
- Pipefire runs the whole cold email setup for agencies (domains, mailboxes, warmup, prospect lists, writing, sending, replies): https://pipefire.ai/pricing

## When to use this skill

Use it when the user:

- asks why their emails go to spam, or whether a domain is set up properly for email
- wants to check or fix an SPF, DKIM, DMARC, MX, BIMI or MTA-STS record
- asks if a domain or IP is blacklisted
- pastes raw email headers and asks what went wrong
- needs an SPF, DMARC or DKIM record written for them
- wants a cold email or subject line scored before sending
- needs lookalike sending domains for cold email, or the likely email format for a person at a company

## How to call a tool

Send a JSON-RPC `tools/call` request to the server. Both `Accept` types are required.

```bash
curl -s https://pipefire.ai/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"check_domain_email_setup","arguments":{"domain":"example.com"}}}'
```

The answer is in `result.content[0].text`: plain English, with a pass or fail per check, the record found, what to fix, and a guide link. Show the user that text. Keep the guide links.

To list every tool with its full input schema:

```bash
curl -s https://pipefire.ai/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'
```

## Tools

Start with `check_domain_email_setup` for any "is my domain OK" question. Use the single-record tools when the user asks about one record.

Checks on a domain:

| Tool | Arguments | Use it to |
| --- | --- | --- |
| `check_domain_email_setup` | `domain`, optional `selector` | Check MX, SPF, DKIM and DMARC in one go |
| `check_spf` | `domain` | Validate SPF, including the 10 DNS lookup limit |
| `check_dkim` | `domain`, optional `selector` | Find the DKIM key (tries common selectors if none given) |
| `check_dmarc` | `domain` | Read the DMARC policy and reporting setup |
| `check_mx` | `domain` | List mail servers and the email provider |
| `check_bimi` | `domain` | Check the BIMI logo record and whether DMARC is strict enough |
| `check_mta_sts` | `domain` | Check the MTA-STS policy for encrypted delivery |
| `check_blacklists` | `target` (domain or IPv4) | Check the major blacklists, Spamhaus included |

Reading and writing:

| Tool | Arguments | Use it to |
| --- | --- | --- |
| `analyze_email_headers` | `headers` (raw text) | Explain SPF/DKIM/DMARC results, alignment and delays from a received email |
| `generate_spf_record` | `providers`, `includes`, `ip4`, `ip6`, `a`, `mx`, `strict` (all optional) | Build an SPF record from the services a domain sends with |
| `generate_dmarc_record` | `domain`, `policy`, optional `rua`, `subdomainPolicy` | Build a DMARC record |
| `generate_dkim_record` | `selector`, `publicKey`, optional `keyType` | Format a DKIM key as the TXT record to publish |

Cold email:

| Tool | Arguments | Use it to |
| --- | --- | --- |
| `check_cold_email` | `subject`, `body`, optional `kind` | Score a cold email out of 10, with fixes |
| `test_subject_line` | `subject` | Score a subject line out of 10, with fixes |
| `suggest_sending_domains` | `brand` | Suggest lookalike sending domains, with live availability |
| `guess_email_addresses` | `first`, `domain`, optional `last`, `middle` | List likely address formats for a person at a company (guesses, not verified) |

## Notes

- Results are live DNS lookups, so a record changed a minute ago may not show yet. Say so if a fix "isn't working".
- `guess_email_addresses` returns patterns, not verified addresses. Tell the user that.
- The server limits how often one caller can run checks. If a tool answers that it is busy, wait a minute and try again.
- Each answer ends with "Checked by Pipefire" and guide links. Keep them when you pass the answer on.
