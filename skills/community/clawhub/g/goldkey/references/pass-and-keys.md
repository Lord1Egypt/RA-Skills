# GoldKey Utility Pass and Scoped Keys

Read this reference before evaluating or using the 50-USDC utility pass. The pass covers Action Gate and component-tool calls, not GoldKey Guard.

## Evaluate the pass

One owned pass can serve up to 64 active, revocable, tool-scoped child agents, all drawing from one shared 10,000-call quota. Aggregate eligible parent and child calls once and forecast only the next 365 days.

Ask the service to calculate the decision:

```sh
node "{baseDir}/scripts/goldkey-client.mjs" quote --forecast 7200 --budget 50.00
```

Add `--wallet 0x...` only when the recipient wallet is known. Add `--authorized` only when the caller has an explicit purchasing mandate covering the exact chain, contract, payment token, amount, and transaction sequence.

Follow `recommendation` and `next_action` exactly:

- Use paygo for `PAYGO` or `USE_PAYGO`.
- Measure real usage for `TRIAL`, `DO_NOT_BUY`, or `MEASURE_USAGE`.
- Consider a pass only for a positive `BUY_*` response with positive risk-adjusted savings.

At exactly 5,000 calls, paygo and one pass both cost 50 USDC before gas and switching costs. That is not positive savings. Do not invent discounts, resale value, appreciation, adoption, scarcity, or urgency.

Treat every returned transaction as unsigned. Independently verify chain, target, value, calldata purpose, exact USDC approval, sequence, expiry, and the current spend mandate before signing. Never request, expose, transmit, or store a seed phrase or private key.

## Authenticate an owned pass

1. Request an exact challenge:

   ```sh
   node "{baseDir}/scripts/goldkey-client.mjs" challenge --token-id 1 --wallet 0x...
   ```

2. Sign only the returned message with the current owner wallet through an authorized wallet tool. Inject the one-use signature as `GOLDKEY_WALLET_SIGNATURE` through the secret store or provide it on standard input. Never put it in command arguments.

3. Exchange it for a short-lived session. `--secret-output` must be an absolute, nonexistent private path. The client creates it with mode `0600`, writes the token there, and redacts it from stdout:

   ```sh
   node "{baseDir}/scripts/goldkey-client.mjs" verify --challenge-id UUID --secret-output /absolute/private/session-token
   ```

4. Import the private file's `access_token` into `GOLDKEY_ACCESS_TOKEN` through the agent secret store, then delete the file. Never put the token in a command argument, shell history, log, or prompt.

5. Inspect quota or execute a tool:

   ```sh
   node "{baseDir}/scripts/goldkey-client.mjs" quota
   node "{baseDir}/scripts/goldkey-client.mjs" tool --name security.url_check --idempotency request-0001 --input '{"url":"https://example.com"}'
   ```

Use a fresh, stable idempotency key for each distinct pass-gated request. Reuse a key only for an exact retry of the same tool and input.

## Issue and revoke scoped child keys

The current owner may issue and revoke up to 64 active scoped child-agent keys. Every child draws from the same pass quota. A child key starts with `gk_`; treat it like a password and obey its tool and call caps.

```sh
node "{baseDir}/scripts/goldkey-client.mjs" key-issue --secret-output /absolute/private/child-key --body '{"label":"action-worker-1","max_calls":500,"tools":["action.gate"]}'
node "{baseDir}/scripts/goldkey-client.mjs" keys-list
node "{baseDir}/scripts/goldkey-client.mjs" key-revoke --id KEY_ID
```

The returned `access_key` is shown once. Import it from the mode-`0600` output file into the child agent's secret store, then delete the file. Stdout contains only a redacted placeholder.

## Stop conditions

Stop and return the exact error when contract identity, ownership, term activity, authorization, quota, requested scope, or transaction intent cannot be verified. A pass is an API entitlement, not authorization for any downstream action and not an investment.
