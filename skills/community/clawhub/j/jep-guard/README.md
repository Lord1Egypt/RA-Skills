# JEP Guard 3.0.0 — repair candidate

This local policy gate only protects execution paths that explicitly call its hooks. It is not an OS sandbox. Processes sharing the service's OS account can access its credentials; use separate OS accounts/containers for mutually untrusted code.

Install using `npm ci --ignore-scripts`, build using `npm run build`. There is no install/uninstall lifecycle execution. Start manually with `node dist/cli/index.js daemon --mode full`. Use `node dist/cli/index.js init` to create a new configuration; it never overwrites existing configuration.

## Migration

The private state directory is `~/.jep-guard` (0700). Files below it must be 0600 and owned by the service user. The socket has moved from shared `/tmp` to `~/.jep-guard/guard.sock` (0600). The daemon refuses to unlink an existing socket; confirm no daemon is using it before removing a stale socket manually.

Set `config.json` to `{"version":"3.0.0","mode":"full"}` to protect hook calls. Explicit `passive` mode does not protect execution. A missing configuration is passive. Invalid configuration in an installed setup fails closed. In full mode, missing daemon, timeout, malformed response, `review`, `block`, and invalid capability signatures all prevent execution. Missing/corrupt policy fails closed. No percentage of operations is automatically approved.

An operator must provision each skill's Ed25519 key pair out of band. Place its base64 32-byte signing seed in `keys/SKILL_ID.json` as `{"seed":"..."}`. IDs allow letters, digits, dot, hyphen and underscore (1–128 characters, starting alphanumeric). Protect the keys directory with 0700. Configure `allowed-skills.json` as an array of `{"name":"SKILL_ID","version":"1","pubkey":"BASE64_RAW_32_BYTE_PUBLIC_KEY","capabilities":["read"]}`. The package contains no working private key or default credential. Registry changes require operator action and daemon restart; network requests cannot replace keys or capabilities.

Configure `policy.json` as an ordered array, for example `[{"id":"read-work","match":{"skill":"SKILL_ID","action":"read","target":"/work/*"},"decision":"allow"}]`. First matching rule wins; default is deny. `review` remains blocked. Rules with unsupported rate limits are rejected. Allow decisions must also fit the identity's assigned capabilities.

The daemon creates a persistent signing seed and pinned public key in the same private directory on first manual startup. Clients sign a fresh socket challenge plus the complete request. Capabilities are Ed25519-signed, expire in 60 seconds, and bind the requester and exact execution parameters. This is a local capability envelope, not a JWS interoperability claim. Events use a signed local JEP-like profile; the daemon is the signer and requester is explicit signed metadata. Completion reports are authenticated client statements, not independently verified execution facts.

Legacy cross-skill socket forwarding is disabled until an authenticated recipient adapter exists. AEGIS/global kernel and other optional integrations are not loaded automatically. The unused extension stubs are not production attestation implementations. This release does not claim TEE, cognitive attestation, automatic reputation-based protection or network consensus.

## Data and limits

The daemon writes signed event metadata and hashes to `~/.jep-guard/audit-stream.jep`; it does not transmit them externally. Request context crosses the local socket to the daemon for evaluation. Logs stop at 16 MiB and the core stops at 10,000 events; archive securely and restart rather than silently discard security state. Replay protection for commands uses a fresh per-connection challenge. Capabilities are single pre-execution authorizations for the cooperating runtime, not independently consumable network bearer tokens.

The CLI exports only the requested filter results from its bounded in-memory window (up to 10,000 recent records), never all historical records by implication. Output files use 0600 and exclusive creation. Local host administrators can alter/delete logs; externally anchor exports if rollback/deletion detection is required. Back up keys and logs securely. This package does not implement legal compliance certification or automatic retention deletion.

## Verification

`npm run build` and `npm test -- --runInBand` check the core, policy, identity, capabilities and export behavior. Run `RUN_IPC_TESTS=1 npm test -- --runInBand` on Linux/macOS allowing Unix sockets for five end-to-end IPC tests. They could not execute in the repair workspace (`listen EPERM`); release approval requires those tests and a real OpenClaw integration check. SDK import smoke test is `node -e "require('./dist/sdk')"`.

No existing runtime configuration is automatically modified. Operator registration of hooks with OpenClaw must follow the actual host version's integration contract; that integration has not been verified in this workspace.
