---
name: hashference-openclaw
description: "Set up, use, refresh, or troubleshoot Hashference as an OpenClaw inference provider. Covers secure sign-in, all live model IDs and prices, Chat/Responses/Messages routing, primary models, fallbacks and subagents. Use for hashference.com connections, model selection, missing models or billing errors."
homepage: https://hashference.com
license: MIT-0
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# Hashference for OpenClaw

## Access scope

The catalog helper uses a public HTTPS GET to https://hashference.com/v1/catalog, or reads the explicitly selected offline JSON with --input. It prints results to stdout and counts/errors to stderr. It reads no environment variables, credentials, account files or OpenClaw configuration, writes no files, executes no child processes, and sends no prompts or account data. Python bytecode caches, if enabled, are interpreter behavior; run with python3 -B to avoid them.

Provider setup, account checks and optional inference are separate host-tool operations: they require the user’s requested scope, the host’s permissions and its approved secret/config interfaces. Loading this skill grants no permissions or preapproved tools. If needed access is unavailable, report the specific blocker. See [security boundaries and release changes](references/SECURITY.md).

## 1. Inspect installation and goal

Establish whether the user wants an optional provider, primary model, fallback, cheaper subagents, model list or repair. Do not ask again when already stated. For catalog-only requests jump to step 3; do not authenticate or change config.

Inspect installed version, provider/runtime plugins, configured provider IDs and model metadata, target agent and current primary/fallbacks. Redact secrets before displaying config; never dump whole config/environment into chat. Reuse existing Hashference auth and provider IDs. Examples use local ID hashference; it is not an API requirement.

Use first-class tools and the installation's supported setup/custodian flow. When an OpenClaw session exposes the openclaw setup tool, delegate provider/config/auth/plugin changes to it with the exact merge and verification requirements. Otherwise read local docs and CLI help before validated config commands. Use only the host-approved configuration interface and retain all host approval requirements.

**Check:** agent, goal, existing route and preservation requirements are known. Branch details: [setup](references/setup.md).

## 2. Establish secret-safe auth

Reuse a working SecretRef. Otherwise use OpenClaw masked entry for the user's own Hashference API key or documented browser device flow. See [setup](references/setup.md) for device polling and storage requirements. The token response contains a key: send it directly to an approved secret sink, never a model-visible response, log, transcript or source file. Without a secret-safe sink, use masked entry; do not improvise a leaking login script.

For env auth, HASHFERENCE_API_KEY must exist in the **Gateway process environment**, not merely a temporary terminal. Bind it by SecretRef. An existing protected key file may be referenced, never copied or displayed. The public catalog helper requires no key.

Check GET https://hashference.com/v1/account through a secret-safe authenticated request. Report only auth success and relevant balance, not identifiers. Never use our account for another user. Purchases, staking, mining, software installation and paid inference need the user's authorization; device approval is not spend authorization. A subscription does not cover API bills.

**Check:** usable auth or a precise missing secret-entry step; no exposed credential.

## 3. Discover live models

Resolve these paths relative to this skill directory:

~~~bash
python3 scripts/catalog.py
python3 scripts/catalog.py --format json --include-aliases
python3 scripts/catalog.py --agents-only --format openclaw
~~~

Default: distinct live Chat-compatible models. JSON output retains complete metadata, including privacy, promotions, endpoints, cache rates and staking eligibility. Use --transport responses or --transport messages for other protocols; --include-aliases retains same_model_as entries. --model EXACT_ID can repeat. Offline: --input references/catalog-snapshot.json, explicitly labeled historical.

Read [model guidance](references/models.md) and live https://hashference.com/v1/capabilities. Filter by actual endpoints, not protocol label or model family. Agent use requires supports_tools true; long sessions need both context_length and max_input_tokens considered. Never invent IDs, infer image support from names or equate advertised tools with tested reliability.

**1,000 credits = USD 1**: divide catalog rates by 1,000 for USD per million tokens. Before paid use show exact selected ID, current prices, limits, privacy caveats and promotion expiry. If refresh fails, label stale metadata; do not quote snapshot rates as current. For “all models,” deliver the full catalog artifact, not just favorites.

**Check:** exact IDs, compatible endpoints, current prices and limits are known.

## 4. Merge provider and registrations

Default OpenClaw route: baseUrl https://hashference.com/v1 and api openai-completions. Other transports: [setup](references/setup.md). Helper --format openclaw prints **only model registrations to stdout**, not a complete config or installer. It has no file-output option and never creates or changes configuration files or handles credentials. Review the captured output before using the approved setup interface; do not redirect it into a configuration path.

Merge requested entries into models.providers.PROVIDER.models by ID. Preserve existing models, credentials, headers, compat overrides, other providers and routing. Refresh catalog-owned metadata only; review conflicts with user-authored limits. Do not blindly replace a provider or array. Missing catalog entries should be reported for review, not auto-deleted.

agents.defaults.models is not runtime registration. Current OpenClaw uses it for aliases/params, with modelPolicy for restrictions; older versions may differ. Check installed docs, preserve policies, never silently widen them.

Leave primary unchanged unless requested. Primary changes use the installation's live-tested default selector with the correct agent, not raw writes. Fallback requests append the chosen pair to the requested agent's existing chain. Subagents use an explicit provider/model through the supported delegation interface, leaving the main model unchanged.

**Check:** validated merged config registers requested models and changes only authorized routing.

## 5. Prove and report

Run installed version's read-only validation/lint and verify registration for the target agent. Config success and UI refresh are not inference proof.

With authorized spend, make one small fresh-context completion using the exact configured provider/model, prompt “Reply with exactly: HASHFERENCE-PROOF-OK” and a modest output cap. Prefer completion-only/no-tools testing; agent tests can invoke tools. Verify actual route, exact reply and elapsed time. If tooling is needed, separately test one harmless client function, return its result and check final output, with authorization for extra paid calls. One successful model does not prove all models.

Confirm target agent primary/fallback state and, if applicable, current session /status. Existing chats can retain overrides; /model default follows primary on supporting versions.

Report provider ID, chosen IDs/catalog artifact, SecretRef location (never value), validation/inference evidence, changed defaults/fallbacks and unverified scope. Without spend authorization say **paid inference not tested** after metadata/config checks. Failures: [troubleshooting](references/troubleshooting.md).

**Check:** every claim has evidence; auth/spend/runtime/UI blockers are explicit.

## Resources and maintenance

- [Offline public JSON snapshot](references/catalog-snapshot.json) and [readable model list](references/catalog-snapshot.md); refresh before use.
- [Sources and attribution](references/SOURCES.md), [release verification](references/VERIFICATION.md), [installation and sample requests](README.md).
- scripts/catalog.py performs public discovery/export; tests/test_catalog.py covers its behavior. Run python3 -m unittest discover -s tests -v after changes.
- See LICENSE for MIT-0 terms. No credentials, account exports or transcripts belong in this skill.
