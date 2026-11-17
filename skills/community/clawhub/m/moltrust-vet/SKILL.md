---
name: moltrust-vet
version: 1.0.0
description: Check any agent skill against ten versioned, CWE-mapped security checks before you install it, and get a verdict a third party can recompute.
license: MIT-0
author: did:moltrust:157224190be24072
homepage: https://moltrust.ch/skills.html
---

# moltrust-vet

Vet a skill before installing it. The verdict comes from a published check list
with a version number and a checksum, over a canonical hash of the skill file,
so anyone can run the same check and get the same answer.

## Why this differs from reading the file yourself

A checklist you eyeball gives a different answer on Tuesday than on Friday. This
runs ten fixed checks, each mapped to a CWE identifier, each with a stated
deduction, and reports the auditor version alongside the score. Two people
auditing the same bytes get the same number, and can say which check fired.

The check list is public: `https://api.moltrust.ch/guard/audit/checks` returns
every check with its severity, deduction and CWE reference. Its version and
checksum come from `https://api.moltrust.ch/guard/audit/version`.

## Usage

```
vet <github-url-or-slug>
```

Examples:

```
vet https://github.com/someone/their-skill
vet someone/their-skill
```

## What the agent does

1. Resolve the argument to a repository URL. A bare `owner/repo` becomes
   `https://github.com/owner/repo`.

2. Request the audit:

```
GET https://api.moltrust.ch/guard/skill/audit?url=<repository-url>
```

   No API key. No account. The endpoint allows five audits per hour per IP.
   Add `&profile=claude_skill` when vetting a Claude Agent Skill, which
   downgrades the agent-card check to informational.

3. Report to the user:
   - `audit.score` out of 100 and whether `passed` is true
   - every entry in `audit.findings`: severity, category, description, deduction
   - `audit.auditorVersion`, so the verdict can be reproduced later
   - `skillHash`, the canonical hash of the file that was actually read
   - `ecosystem_trust_score`, or that it is `null` when the skill declares no
     MolTrust author

4. State the score without softening it. A skill scoring 62 is not "mostly
   fine". Report the number, the findings, and let the user decide.

## Reading the response

| Field | Meaning |
|---|---|
| `passed` | score at least 70 and no hard failure |
| `audit.score` | 100 minus the deductions that fired |
| `audit.findings[]` | which checks fired, with severity and deduction |
| `audit.vc_issuable` | whether a signed credential could be issued for this |
| `skillHash` | canonical SHA-256 over the normalised file |
| `ecosystem_trust_score` | cross-skill reputation, `null` for unknown authors |

Status codes worth distinguishing: `404 skill_md_not_found` means the repository
has no SKILL.md, which is a fact about the target and not an error on our side.
`429 rate_limited` means the five-per-hour allowance is used up.

## First run

On first use the agent may register a MolTrust identity, so that skills it later
publishes carry an author other tools can resolve. This is optional; vetting
works without it.

Registration is keyless — no API key, no signup, no email:

1. `GET https://api.moltrust.ch/identity/register-challenge` returns a challenge
   string and a proof-of-work seed with a difficulty in bits.
2. Generate an Ed25519 keypair. Keep the private key local; it is never sent.
3. Find a nonce whose SHA-256 over seed plus nonce has at least the stated
   number of leading zero bits.
4. Sign the challenge string with the private key.
5. `POST https://api.moltrust.ch/identity/register-pop` with the public key, the
   challenge, the signature, the nonce, a display name, and
   `platform` set to `clawhub`.

The response carries a `did:moltrust:` identifier and a signed credential. Put
that identifier in the `author:` field of your own SKILL.md frontmatter. The free
tier holds no spendable credits and keeps no request history.

Store the private key wherever the host keeps its own secrets. This skill does
not choose that location and does not transmit the key.

## What this skill does not do

It does not install, modify or execute the skill it is asked to vet — it reads
one file over HTTPS and reports what the checks say.

It does not issue a credential. That is a separate, paid endpoint
(`POST /guard/vc/skill/issue`, 5 USDC via x402) for when you need a verdict to
show someone else rather than to decide for yourself. A vetting run never
triggers it.

A passing score is not a guarantee of safety. It means ten specific checks found
nothing, over the version of the file that was fetched at that moment.

## Network calls

Two hosts, both stated up front:

- `api.moltrust.ch` — the audit, and registration if you opt into it
- `github.com` / `raw.githubusercontent.com` — reached by the audit service, not
  by this skill, to read the target SKILL.md

Nothing else is contacted. Nothing about your machine is transmitted.

## Verify this skill

This skill is subject to its own checks:

```
GET https://api.moltrust.ch/guard/skill/audit?url=https://github.com/MoltyCel/moltrust-vet
```

Its published credential, if one has been issued, resolves by hash:

```
GET https://api.moltrust.ch/guard/skill/verify/<skillHash>
```

## License

Apache-2.0. See LICENSE in the repository.
