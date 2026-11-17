# GoldKey Guard Beta

Read this reference before installing or operating GoldKey Guard.

## Contents

- Availability and economics
- Enforcement topology
- Exact routes
- Installation integrity
- Packaged adapters
- Authorization and execution lifecycle
- Payment recovery
- Guard-specific inspection commands
- Stop conditions

## Availability and economics

Treat Guard as unavailable unless both live `/v1/catalog` and `/openapi.json` advertise the `guard` beta and its exact routes. Read live `/guard/terms` before registration or payment. Discovery does not grant beta access: registration is restricted to explicitly approved design-partner operator wallets.

The 50-USDC utility pass does not include Guard. A completed network decision for MCP, HTTPS, or AgentCash costs exactly 0.05 USDC. A completed supported Base/EVM decision costs exactly 0.10 USDC. `ALLOW`, `REVIEW`, and `BLOCK` are billable. `REVIEW` requires operator review; `BLOCK` must never forward.

Repeating the exact installation-signed request and durable idempotency key while its receipt remains unexpired returns the stored authorization without another settlement. A changed call or expired key is a conflict, not a retry strategy.

## Enforcement topology

Use both components exactly:

- The hosted authorizer verifies an operator-signed immutable policy, a public-only Ed25519 installation identity with proof of possession, and the installation-signed exact call. After x402 settlement, it returns a short-lived signed `ALLOW`, `REVIEW`, or `BLOCK` authorization. It never receives upstream credentials, holds a wallet signer, forwards an actual request, signs a transaction, or broadcasts it.
- The operator-controlled local enforcer alone holds the connector credential or execution signer. It verifies the hosted receipt against the exact canonical call and pinned policy and forwards only an unexpired `ALLOW`.

Remove every direct credential, signer, MCP configuration, AgentCash route, and network route that could bypass the enforcer. If the guarded agent can reach the connector or signer directly, Guard is advisory rather than enforcement.

Keep the operator wallet key, installation Ed25519 private key, Guard payer, upstream connector credential, and execution signer local and appropriately separated. Never send any of them to the hosted authorizer.

## Exact routes

Use only the routes that live discovery advertises:

- `GET /guard/terms`: read the separate Guard beta terms.
- `POST /v1/guard/policies`: register the next monotonically versioned, operator-signed policy. Put MCP `arguments_schema` and HTTPS `query_schema` or `body_schema` constraints in policy when action-level limits are required. The agent cannot rewrite registered policy.
- `POST /v1/guard/installations`: bind a public Ed25519 installation key to the current policy with both the operator-wallet signature and installation-key Ed25519 `key_proof`.
- `POST /v1/guard/revocations`: submit an operator-signed policy or installation revocation.
- `POST /v1/guard/paygo/authorize/network`: authorize one exact MCP or HTTPS call for 0.05 USDC.
- `POST /v1/guard/paygo/authorize/evm`: decode and policy-check one exact supported EVM transaction for 0.10 USDC and simulate it when policy requires.
- `POST /v1/guard/executions/{executionId}/commit`: record installation-signed intent to forward after local receipt verification.
- `POST /v1/guard/executions/{executionId}/reconcile-commit`: recover only after ordinary commit returns the exact `guard_payment_not_settled` signal.
- `POST /v1/guard/executions/{executionId}/complete`: record installation-signed execution outcome.
- `GET /.well-known/goldkey-guard-keys.json`: obtain current and retained public receipt-verification keys.

There is no pass-funded Guard route and no execution-lookup route in v1.

## Installation integrity

Require Node.js 22 or newer. Obtain authorization before downloading or installing a package. Do not install a similarly named registry package.

The integrity-pinned and tested enforcer artifact is:

- Package: `@goldkey/enforcer`
- Version: `0.2.1`
- Size: `120073` bytes
- SHA-256: `62dbeb10684e075a9ca7d08862eaa99b30f2c2f958bba3f9cc8ecbd7c212d3e5`
- SHA-512 SRI: `sha512-y0qBohVxB/5F9DkzXBDKeerlpudXlpHaewj7D4coqLyC9IbBbH7vtZ1bBYyck31hdXiTaNTQOYvwAa/enm54wQ==`
- Manifest: `https://github.com/noah-ing/goldkey/releases/download/v0.2.1/goldkey-enforcer-0.2.1.tgz.integrity.json`
- Artifact: `https://github.com/noah-ing/goldkey/releases/download/v0.2.1/goldkey-enforcer-0.2.1.tgz`

Fetch the manifest and artifact without executing either. Require every manifest value above, compute SHA-256 over the downloaded tarball bytes, and compare before installing the local file with lifecycle scripts disabled:

```sh
npm install --ignore-scripts /absolute/private/goldkey-enforcer-0.2.1.tgz
```

Read the artifact's bundled README and packaged examples before configuration. Do not use an artifact whose size, package, version, SHA-256, or SRI differs from the values above.

## Packaged adapters

The artifact includes the config-driven `goldkey-mcp-stdio`, `goldkey-agentcash`, `goldkey-wallet`, and `goldkey-wallet-mcp` launchers plus the lower-level SDK. Combine the shared runtime with one operator-controlled adapter configuration. No separate customer authorization client is required.

Bind operator-owned connectors before use and remove the guarded agent's original route to the MCP server, AgentCash wallet, upstream credential, or execution signer. The package:

- validates the exact 0.05- or 0.10-USDC Guard challenge before its separate local payer signs;
- enforces a durable cumulative local payment budget;
- retries the identical authorization request at most once;
- never passes the payer signer to an agent connector;
- constructs, canonicalizes, signs, persists, and sends real Guard requests;
- performs DNS-rebinding-safe resolution and connection pinning for network calls;
- enforces decoded EVM intent and required simulation; and
- verifies the hosted authorization locally before forwarding.

Generic MCP and AgentCash purchases require a durable caller-supplied `_meta["com.goldkey/idempotency-key"]`. Missing keys fail before authorization or forwarding.

Use `goldkey-mcp-stdio --inspect CONFIG` only to start the pinned upstream and collect tool names and schema hashes through `initialize` and `tools/list`. GoldKey does not authorize, pay, or invoke tools during inspection, but the upstream process itself is not guaranteed side-effect-free.

`goldkey-agentcash --inspect CONFIG REQUEST` is offline. AgentCash 0.17.1 lacks socket pinning and redirect control, so its adapter is limited to fixed, query-free, vetted endpoints behind separate OS or container egress controls and a segregated, deliberately funded AgentCash wallet.

`goldkey-wallet probe --config CONFIG --request REQUEST` does not load RPC, either wallet, the runtime, or a payment path. Base execution requires a low-balance execution signer, a different Guard payer wallet, no signer reuse, and no concurrent funding.

## Authorization and execution lifecycle

Let the local enforcer own the entire lifecycle. Do not hand-roll it in an agent prompt and do not use the hosted authorizer as a proxy.

For an `ALLOW`, the enforcer must:

1. Verify the signed authorization against the exact canonical call, registered policy, installation, expiry, and current public keyset.
2. Durably persist `FORWARDING`.
3. Send the installation-signed ordinary commit.
4. Invoke the configured connector exactly once.
5. Send the installation-signed completion with the actual outcome.

Record ambiguous connector outcomes as `outcome_unknown` and never retry them automatically. `REVIEW` and `BLOCK` never enter the forwarding lifecycle.

## Payment recovery

For a paid authorization, the local SDK stores only the exact public x402 `PaymentPayload` it sent and the Base transaction hash from `PAYMENT-RESPONSE` in its private local outcome file. It always tries ordinary commit first.

Only the exact `guard_payment_not_settled` response may trigger `/reconcile-commit`. The origin then verifies the exact Base USDC EIP-3009 calldata, transaction receipt, and `Transfer` before allowing forwarding.

This is not universal crash recovery. A hard process death after transmitting payment but before receiving the transaction hash remains fail-closed and may require manual facilitator or onchain reconciliation. Never retry that payment automatically.

## Guard-specific inspection commands

The following bundled-client commands are Guard-specific discovery or zero-spend inspection only:

```sh
node "{baseDir}/scripts/goldkey-client.mjs" guard-keyset
node "{baseDir}/scripts/goldkey-client.mjs" guard-network-probe --request SIGNED_SYNTHETIC_GUARD_REQUEST_JSON
node "{baseDir}/scripts/goldkey-client.mjs" guard-evm-probe --request SIGNED_SYNTHETIC_GUARD_REQUEST_JSON
```

Use probes only with a non-secret synthetic request because command arguments may enter shell history. They send no wallet credential or payment header, validate the canonical x402 resource and fixed atomic-USDC price, and do not authorize or forward a new call. An exact unexpired replay is reported as already paid, but the probe deliberately does not return or verify its authorization.

Use the local enforcer, not these probes, for real calls, registration, revocation, receipt verification, or lifecycle transitions.

## Stop conditions

Stop on unavailable routes, rejected beta access, mismatched terms or prices, stale policy version, missing idempotency, unverified installation proof, artifact-integrity mismatch, receipt-verification failure, expired authorization, simulation failure, ambiguous connector outcome, or any possible bypass around the local enforcer. Preserve the exact error and fail closed.
