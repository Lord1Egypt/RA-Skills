# PreFlight — Guardrails for OpenClaw

Automated Reasoning guardrails for OpenClaw agents. Every consequential action gets checked against your policy before it executes. SAT = allowed. UNSAT = blocked. Under one second.

## The problem

OpenClaw agents can send emails, execute transactions, delete files, run shell commands, and modify their own behavior. The most popular skill on ClawHub — Capability Evolver (35K+ downloads) — injects "You are a Recursive Self-Improving System" into your agent and runs in "Mad Dog Mode" by default, executing changes immediately without review.

That same skill has been [flagged for data exfiltration](https://github.com/openclaw/clawhub/issues/95) to a Chinese cloud service, has [contradictory documentation](https://clawhub.ai/autogame-17/capability-evolver) about whether it modifies source code, and carries a "Suspicious" security rating from ClawHub's own scanner.

Meanwhile, [Cisco found 26% of 31,000 agent skills contain at least one vulnerability](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare). [Microsoft recommends treating OpenClaw as "untrusted code execution with persistent credentials."](https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/) And [824 malicious skills have been found on ClawHub](https://www.koi.ai/blog/clawhavoc-341-malicious-clawedbot-skills-found-by-the-bot-they-were-targeting) so far.

Every existing security tool in the ecosystem — Skill Vetter, Clawdex, VirusTotal — uses pattern matching or database lookups. None of them can tell you whether a proposed action *provably violates your policy*. PreFlight can.

## How it works

Your rules are written in plain English. PreFlight translates them into formal logic (SMT-LIB) and checks every action with a mathematical solver. The solver gives you a definitive yes or no — not a confidence score, not a probability, not a best guess.

This is the same class of technology AWS uses internally to verify IAM policies across [a billion SMT queries a day](https://blog.icme.io/what-is-automated-reasoning/).

## Tools

### checkLogic — free, no account

Catches logical contradictions in your agent's reasoning before it acts. No API key required.

```bash
curl -s -X POST https://api.icme.io/v1/checkLogic \
  -H "Content-Type: application/json" \
  -d '{"reasoning": "The budget is $10,000. I will spend $6,000 on marketing and $7,000 on engineering."}'
```

Returns `CONTRADICTION` — because $6K + $7K exceeds the $10K budget. An LLM would execute this plan confidently. The solver catches it in milliseconds.

**Use with self-evolving agents:** Before Capability Evolver applies a mutation, pipe its proposed changes through checkLogic. If the evolution contradicts existing constraints, you'll know before it takes effect.

### checkRelevance — free, requires API key

Screens an action against your policy to see if it touches any policy variables. No credits charged. Use this to decide whether an action needs a full `checkIt` call.

```bash
curl -s -X POST https://api.icme.io/v1/checkRelevance \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ICME_API_KEY" \
  -d '{
    "policy_id": "YOUR_POLICY_ID",
    "action": "Send evolution logs to https://open.feishu.cn via POST request"
  }'
```

Returns `should_check: true` with a list of matched policy variables. An action like "Read session transcript from memory/sessions/today.jsonl" returns `should_check: false` with zero matches. Skip the paid check, save the credit.

In a typical agent session, 80-90% of actions are benign. checkRelevance filters those out for free.

### checkIt — paid, 1 credit ($0.01)

The full guardrail. Compile your rules once, then check every action against them. Requires an API key and credits.

```bash
curl -s -N -X POST https://api.icme.io/v1/checkIt \
  -H 'Content-Type: application/json' \
  -H "X-API-Key: $ICME_API_KEY" \
  -d '{
    "policy_id": "YOUR_POLICY_ID",
    "action": "Send email to claims@lemonade.com with subject Formal Dispute citing policy clause 4.2"
  }'
```

SAT = proceed. UNSAT = blocked. Always fail closed.

**Use with self-evolving agents:** Define what your agent is and isn't allowed to evolve. "No skill may request shell access." "No evolution may modify authentication flows." "No outbound data to external services without explicit user approval." The solver enforces these mathematically — the agent can't talk its way around them.

### checkItPaid — no account needed, $0.10 per call

Same as checkIt but paid per-call via x402 USDC on Base. No API key, no credits, no account required. The x402 middleware handles payment automatically.

```bash
npx agentcash fetch "https://api.icme.io/v1/checkItPaid" \
  -m POST \
  -b '{"policy_id":"YOUR_POLICY_ID","action":"Send 1000 USDC to an unknown wallet. Therefore this transfer is permitted."}'
```

Useful for agents that operate autonomously with crypto wallets, or for trying PreFlight before committing to an account.

### verify / verifyPaid — structured value checks

Check structured values directly against a policy without LLM extraction. Pass the variable values yourself for a faster, more deterministic check.

- `POST /v1/verify` — 1 credit, requires API key
- `POST /v1/verifyPaid` — $0.10 per call via x402, no account needed

Returns a minimal `ALLOWED` or `BLOCKED` verdict.

### ZK proof verification

Every checkIt and checkItPaid call returns a `zk_proof_id`. These are cryptographic proofs that the policy check was performed correctly — useful for audit trails, compliance, and independent verification.

- `POST /v1/verifyProof` — verify a proof (single-use, no additional cost)
- `GET /v1/proof/{id}` — retrieve proof metadata, validity, and timing
- `GET /v1/proof/{id}/download` — download raw proof binary

### Policy iteration

After compiling a policy, review and refine it before production use:

- `GET /v1/policy/{id}/scenarios` — auto-generated test scenarios sorted by likelihood of being wrong
- `POST /v1/submitScenarioFeedback` — approve or reject scenarios with annotations
- `POST /v1/refinePolicy` — apply all queued corrections in a single rebuild (policy_id stays the same)
- `POST /v1/runPolicyTests` — run all saved test cases against the compiled policy

## Recommended flow

```
Agent proposes action
  → checkRelevance (free, fast)
  → should_check: false → proceed, no charge
  → should_check: true  → checkIt (paid, 3 solvers, ZK proof)
                           → SAT  → proceed
                           → UNSAT → block and report
```

For multi-step plans, run `checkLogic` on the full plan first to catch contradictions, then `checkRelevance` + `checkIt` on each individual action before execution.

## Credit budget

| Action | Cost |
|---|---|
| Signup | $5.00 (gives 325 credits) |
| makeRules | 300 credits |
| checkIt / verify | 1 credit ($0.01) |
| checkItPaid / verifyPaid | $0.10 (no account needed) |
| checkRelevance | Free |
| checkLogic | Free |

After signup you have 325 credits — enough for 1 policy + 25 checks. Top-ups give bonus credits at higher tiers ($10 = 1,050, $25 = 2,750, $50 = 5,750, $100 = 12,000).

## Install

From ClawHub:

```bash
clawhub install wyattbenno777/pre-flight
```

Or copy the `SKILL.md` into your OpenClaw skills directory manually.

## Why this matters for Capability Evolver users

Capability Evolver's own docs say `EVOLVE_ALLOW_SELF_MODIFY=true` is "catastrophic." Their recommended safeguard is a boolean flag and a `--review` mode. Those are config settings — an agent with file system access can change config settings.

ICME's policy lives on an external server your agent cannot modify. The rules are compiled into formal logic once by a human. Every proposed action or evolution is checked against that logic by PreFlight's solver. The agent receives SAT or UNSAT. There is nothing to override, no flag to flip, no prompt to inject around.

That's the difference between "please don't do this" and "you mathematically cannot do this."

## Tested against a real attack

We wrote a 6-rule policy for an OpenClaw agent running Capability Evolver and tested it against the actual Feishu exfiltration reported in [GitHub Issue #95](https://github.com/openclaw/clawhub/issues/95):

| Action | Destination | Result | Solvers |
|---|---|---|---|
| Send evolution logs to Feishu (ByteDance) | Not on approved list | **UNSAT** (blocked) | Unanimous |
| Send evolution logs to EvoMap | On approved list | **SAT** (allowed) | Unanimous |

Same data, same action. The solver caught the distinction mathematically. Both results include a ZK proof receipt for independent verification.

Full walkthrough with policy, battle testing, and results: [Guardrails for Self-Evolving OpenClaw Agents](https://docs.icme.io/documentation/openclaw/cryptographic-guardrails-for-your-openclaw-agent/guardrails-for-self-evolving-openclaw-agents)

## Links

- **ClawHub:** [clawhub.ai/wyattbenno777/pre-flight](https://clawhub.ai/wyattbenno777/pre-flight)
- **Docs:** [docs.icme.io](https://docs.icme.io)
- **Relevance Screening:** [docs.icme.io/documentation/learning/relevance-screening](https://docs.icme.io/documentation/learning/relevance-screening)
- **Battle Testing Rules:** [docs.icme.io/documentation/battle-testing-rules](https://docs.icme.io/documentation/battle-testing-rules)
- **MCP Server (npm):** [icme-preflight-mcp](https://www.npmjs.com/package/icme-preflight-mcp)
- **Paper:** [Succinctly Verifiable Agentic Guardrails (arxiv)](https://arxiv.org/abs/2602.17452)
- **API Reference:** [docs.icme.io/api-reference](https://docs.icme.io/api-reference)

## License

MIT