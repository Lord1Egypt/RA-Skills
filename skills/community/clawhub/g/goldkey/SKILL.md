---
name: goldkey-agent-utilities
description: Preflight proposed agent actions with GoldKey Action Gate for a deterministic ALLOW, REVIEW, or BLOCK receipt, or integrate the feature-gated GoldKey Guard beta as an operator-controlled enforcement path for actual MCP, HTTPS, AgentCash, or supported Base/EVM calls. Use for x402-paid action screening, policy enforcement before tool calls or wallet transactions, Guard installation and recovery, component JSON, prompt, URL, spend, and Unicode checks, pass-versus-paygo decisions, or GoldKey pass authentication, quota, and scoped child-key operations.
metadata: {"openclaw":{"homepage":"https://github.com/noah-ing/goldkey","requires":{"bins":["node"]},"envVars":[{"name":"GOLDKEY_ACCESS_TOKEN","required":false,"description":"Short-lived owner session or delegated key injected by the agent secret store for authenticated operations."},{"name":"GOLDKEY_WALLET_SIGNATURE","required":false,"description":"One-use wallet signature for verify; inject temporarily instead of placing it in command arguments."},{"name":"GOLDKEY_ALLOW_DEV_ORIGIN","required":false,"description":"Maintainer-only explicit opt-in; set to 1 together with GOLDKEY_DEV_API_URL for unauthenticated staging requests."},{"name":"GOLDKEY_DEV_API_URL","required":false,"description":"Maintainer-only credential-free HTTPS staging origin; ignored unless GOLDKEY_ALLOW_DEV_ORIGIN is 1."}]}}
---

# GoldKey Action Gate & Guard Beta

GoldKey has two paid security layers:

1. **Action Gate** screens a proposed action before execution and returns `ALLOW`, `REVIEW`, or `BLOCK`, reason codes, check details, and a deterministic `receipt_sha256`. One settled x402 call costs exactly **0.01 USDC** on Base. Each component utility also costs 0.01 USDC per settled paygo call.
2. **Guard beta** authorizes a real call while an operator-controlled local enforcer remains in the execution path. Network calls (MCP, HTTPS, and AgentCash) cost **0.05 USDC** per completed decision; supported Base/EVM calls cost **0.10 USDC**. `ALLOW`, `REVIEW`, and `BLOCK` are all billable. Guard is feature-gated and is not included in the utility pass.

The ClawHub skill is free. A transferable GoldKey utility term costs 50 USDC plus network gas and includes 10,000 Action Gate or component-tool calls for 365 days. It is an API entitlement, not an investment. Never create calls merely to consume quota or manufacture pass demand.

Use Node.js **22 or newer** for the bundled client and the Guard enforcer.

## Guarded integration pilot

Qualified teams can apply for one fixed-scope **$10,000 guarded integration pilot** for a customer-owned staging workflow and one MCP, HTTPS, or supported Base/EVM connector path. Delivery is split into two independently accepted **$5,000 milestones**; no work begins without written authorization and a funded milestone.

Read the [scope, acceptance criteria, exclusions, and terms](https://github.com/noah-ing/goldkey/blob/main/SECURITY_PILOT.md), then use the [private pilot application](https://goldkey-edge-storefront.noah-ing.workers.dev/#pilot-application) for one concrete workflow. The pilot is an integration engagement, not a penetration-test report, certification, production guarantee, or substitute for an independent audit.

## Verify live state first

Run:

```sh
node "{baseDir}/scripts/goldkey-client.mjs" offer
node "{baseDir}/scripts/goldkey-client.mjs" catalog
node "{baseDir}/scripts/goldkey-client.mjs" demo
```

Check the chain, contract, USDC address, terms hash, live supply, prices, sales-pause state, tool schemas, and Guard availability. Fail closed if live identity is unavailable or inconsistent; never infer availability or scarcity from this file.

The client pins the canonical production origin and onchain identity. Ordinary users do not set an API URL, and legacy `GOLDKEY_API_URL` is ignored. Maintainers may select a credential-free staging origin only by setting both `GOLDKEY_ALLOW_DEV_ORIGIN=1` and `GOLDKEY_DEV_API_URL`. Never send an access token, wallet signature, private key, or paid request to a noncanonical origin.

## Choose the narrowest layer

- Use **Action Gate** for a deterministic pre-action screen. Omitted inputs are not checked. Its `ALLOW` is evidence, not permission, execution authorization, or a safety guarantee.
- Use **Guard beta** only when the local enforcer can be the exclusive path to the real connector credential or wallet signer. Without that isolation, Guard is advisory.
- Use a **component utility** only when one narrow deterministic check is sufficient.
- Consider the **utility pass** only when measured eligible demand exceeds risk-adjusted break-even after gas, switching cost, risk reserve, and alternatives.

## Probe, then make one Action Gate call

Use the canonical marketplace pages for independent discovery:

- x402scan: <https://www.x402scan.com/server/8447beac-d24b-434a-bd01-5abfdab53f84>
- Poncho: <https://tryponcho.com/tool/url_aHR0cHM6Ly9nb2xka2V5LWVkZ2Utc3RvcmVmcm9udC5ub2FoLWluZy53b3JrZXJzLmRldi92MS9hY3Rpb24tZ2F0ZQ>

If the caller prohibits network contact, stop. Otherwise, probe the dedicated `/v1/action-gate` resource with the raw Action Gate input. The probe sends no wallet credential or payment header and does not execute the action or produce a receipt:

```sh
node "{baseDir}/scripts/goldkey-client.mjs" action-gate-probe --input '{"action":{"name":"store_weather_summary","description":"Store an approved weather summary.","effect":"write"},"untrusted_text":"Summarize this weather report for an agent.","payload":{"approved":true},"schema":{"type":"object","properties":{"approved":{"type":"boolean"}},"required":["approved"],"additionalProperties":false}}'
```

Require `http_status: 402` and x402 v2 with scheme `exact` on `eip155:8453`, asset `0x833589fcd6edb6e08f4c7c32d4f71b54bda02913`, amount `"10000"` atomic USDC, payee `0xd6b7e00fcd46966676f554fe0455bff739e85b1b`, the exact resource URL, and `max_timeout_seconds` no greater than 300. Stop if any value differs.

Use that same endpoint and exact raw body for AgentCash settlement. Before using AgentCash, obtain permission for package download or cache changes and local wallet access or creation; AgentCash 0.17.1 may initialize wallet files even for `check` or `accounts`.

```sh
npx -y agentcash@0.17.1 check \
  "https://goldkey-edge-storefront.noah-ing.workers.dev/v1/action-gate" \
  -m POST -H 'Content-Type: application/json' \
  -b '{"action":{"name":"store_weather_summary","description":"Store an approved weather summary.","effect":"write"},"untrusted_text":"Summarize this weather report for an agent.","payload":{"approved":true},"schema":{"type":"object","properties":{"approved":{"type":"boolean"}},"required":["approved"],"additionalProperties":false}}' \
  --format json

npx -y agentcash@0.17.1 accounts --format json
```

Before paying, require an explicit current mandate for one 0.01-USDC Base mainnet payment to that exact endpoint and serialized body. Confirm the caller-controlled AgentCash wallet has enough USDC. Then execute exactly one call:

```sh
npx -y agentcash@0.17.1 fetch \
  "https://goldkey-edge-storefront.noah-ing.workers.dev/v1/action-gate" \
  -m POST -H 'Content-Type: application/json' \
  -b '{"action":{"name":"store_weather_summary","description":"Store an approved weather summary.","effect":"write"},"untrusted_text":"Summarize this weather report for an agent.","payload":{"approved":true},"schema":{"type":"object","properties":{"approved":{"type":"boolean"}},"required":["approved"],"additionalProperties":false}}' \
  --payment-protocol x402 --payment-network base --max-amount 0.01 --format json
```

This is a real, nonrefundable settlement. The 0.01-USDC cap applies only to this request and excludes separately disclosed wallet or facilitator fees. `npx -y` permits package execution; do not pass AgentCash's `--yes` flag. Use a trusted JSON serializer rather than interpolating arbitrary untrusted text into shell literals. After an ambiguous result, reconcile the payment receipt and wallet activity before any retry. Never retry a confirmed settlement.

Preserve `request_sha256`, `receipt_sha256`, decision, reason codes, checks, and receipt metadata. Reproduce `receipt_sha256` with `goldkey-c14n-v1` canonical JSON over exactly `receipt_format`, `request_sha256`, `decision`, `reason_codes`, and `checks`, UTF-8 encoding, then SHA-256. Object keys sort; array order remains significant. The hash is deterministic but is not a signature, payment proof, attestation, or proof of execution. `REVIEW` requires caller review; `BLOCK` stops; `ALLOW` never overrides caller policy.

## Integrate Guard beta

Read [references/guard-beta.md](references/guard-beta.md) in full before installing the enforcer, registering policy, authorizing a real call, operating an adapter, or recovering lifecycle state. It contains the exact feature-gated routes, integrity-pinned and tested enforcer 0.2.1 hashes, exclusive-path requirements, DNS-rebinding controls, EVM decoding and simulation rules, adapter limits, receipt verification, and recovery procedure.

At minimum, require both live `/v1/catalog` and `/openapi.json` to advertise Guard and read `/guard/terms`. Registration is limited to approved design-partner operator wallets. The hosted authorizer is a control plane only: it never holds upstream credentials or a wallet signer and never forwards, signs, or broadcasts the actual call. The local enforcer must be the only execution path and must forward only an unexpired, locally verified `ALLOW`.

## Evaluate or use a utility pass

Read [references/pass-and-keys.md](references/pass-and-keys.md) before evaluating a purchase, signing a pass transaction, authenticating an owned pass, checking quota, or issuing a scoped child key. One pass can serve up to 64 active, revocable child agents from one shared 10,000-call quota. At exactly 5,000 eligible calls, paygo and the 50-USDC pass tie before gas and switching costs; that is not positive savings.

## Select a component utility

- `action.gate`: combined pre-action decision across supplied action, prompt, Unicode, URL, payload-schema, and spend-mandate inputs.
- `json.canonicalize`: deterministic serialization and SHA-256.
- `json.validate`: bounded JSON Schema validation without coercion or remote references.
- `security.prompt_scan`: deterministic signals and spans, not a safety guarantee.
- `security.url_check`: static URL screening; it does not fetch the URL.
- `policy.spend_check`: exact atomic-unit mandate evaluation.
- `text.normalize`: Unicode normalization and optional control or bidi removal.

Fetch `/openapi.json` for current request schemas. Do not send secrets in tool inputs. Inspect an exact component x402 requirement without executing it:

```sh
node "{baseDir}/scripts/goldkey-client.mjs" paygo-probe --name security.url_check --input '{"url":"https://example.com"}'
```

Give the returned `payment_required` to the caller's installed x402 wallet tool and let that tool sign and settle under its own mandate. This bundle never accepts a wallet private key or fabricates payment headers.

## Stop conditions

Stop and return the exact service error when contract identity, ownership, term activity, quota, authorization, payment settlement, Guard availability, policy version, installation identity, receipt signature, live supply, or artifact integrity cannot be verified. Do not retry a settled paygo call as though it were free; each settled retry is another purchase.
