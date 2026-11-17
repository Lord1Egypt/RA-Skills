# JishuDB automatic installation contract

Read this reference only for Desktop installation or installer-transaction
troubleshooting. The live helper output is authoritative for one transaction.

## Fixed trust inputs

- Release repository: `x-aijishu/jishudb-desktop-releases`
- Source repository: `x-aijishu/jishudb`
- GitHub REST API version: `2026-03-10`
- Release API origin: `https://api.github.com`
- Current release-asset redirect host: `release-assets.githubusercontent.com`
- Desktop bundle ID: `com.aijishu.jishudb`
- Desktop MCP endpoint: loopback HTTP with preferred port `8088`; fresh-install
  fallback is bounded to `8090` through `8104`, with `8089` reserved for LAN MCP
- Default profile: `default`

Changing any fixed trust input requires a reviewed Skill version. Never accept
a runtime override for a different repository, API origin, asset host, bundle
ID, or endpoint-selection boundary.

## Explicit release source

The default source for a new Windows plan is `github`. `plan -ReleaseSource cnb`
selects the packaged CNB catalog discovery URL and independently embedded
Ed25519 authority in `scripts/release-mirror-trust.json`. The catalog verifier is
`scripts/release-mirror-catalog.cjs`. All three files must travel together with
the installer helper. No publication token or private key belongs in a Skill.
There is no source fallback, environment-variable source override, or runtime
trust-key/host override. Unknown values fail as `invalid_release_source`.

In Windows `download` and `execute`, omission of `-ReleaseSource` uses the
approved plan's source. An explicit selector must match that source, otherwise
`release_source_mismatch` stops the transaction. Windows `check` remains a local
runtime check without a source option. Catalog publication, full CNB transfer,
and real installer acceptance are separate gates; source support does not
establish that a live catalog or an accepted installation exists.

### Catalog schema compatibility

Both platform helpers accept the signed catalog schema 1 (`jishudb-release-mirror-catalog-v1`)
and schema 2 (`jishudb-release-mirror-catalog-v2`) through the same packaged
verifier and independently embedded authority. The catalog schema does not
change the native installation-plan schema or package publisher identity.

Schema 2 separates the original application release (`canonicalRelease`) from
its renewed update policy (`policyRelease`). Installer, adjacent checksum and
candidate identities remain bound to the original application release and
source revision. Renewed `latest.yml`, `latest-mac.yml` and `SHA256SUMS.txt`
identify the policy release; its audit files are recorded separately in
`evidenceArtifacts`. These policy/audit files are not installer candidates.

CNB transport uses the signed immutable generation
`v<application-version>-policy.<sequence>`, while native release tags and GitHub
asset IDs remain the original application identity. Clients validate the
predecessor digest field format and the signed audit inventory/generation,
signature, expiry and selection floor. They do not independently check that
predecessor digest against an earlier catalog. The protected publisher verifies
the predecessor chain contents and unchanged installer bytes; clients do not
fetch GitHub or extend an approved transaction to reconstruct that audit.

A new renewal requires a newly reviewed plan. Existing exact approvals retain
their original catalog, transport, digests and expiry, even when discovery
advances to a newer policy generation. A renewal never extends an old approval
or allows source/transport substitution inside it. Same-sequence equivocation,
rollback, invalid signatures and expired catalogs remain terminal failures.

### Windows CNB approval envelope

GitHub plans retain their existing native v1/v2 schema. CNB plans instead use
`jishudb-agent-install-envelope-v1`, with these exact fields:

- `schema`: the outer envelope schema identifier.
- `nativePlan`: `{bytesBase64, sha256}`, binding the complete raw native-plan
  bytes, including creation/expiry, SID, paths, launch mode and canonical GitHub
  release/asset identity. Those identity URLs are never requested in CNB mode.
- `catalog`: `{bytesBase64, sha256}`, binding the exact authenticated signed
  catalog bytes selected during plan creation.
- `transport`: `{source: "cnb", assets: {installer, checksum, candidate}}`,
  binding the three exact mirror URLs to their signed catalog entries.

The printed `planSha256` authorizes the outer file's raw bytes. Every download
and execute reloads that file, compares the approved digest, verifies embedded
byte digests and catalog signature/freshness, and compares native release/asset
identity and transport to the authenticated catalog. Candidate and checksum
bytes are downloaded and independently checked during planning and execution.
There are no GitHub API, canonical asset or release revalidation requests in
CNB mode. Failure categories retain signature, freshness, rollback, source,
range, cache, digest and installer distinctions without automatic fallback.

The catalog bootstrap accepts only the packaged HTTPS discovery URL and bounded
redirects listed in packaged `bootstrapRedirectAllowlist`. Asset requests start
at the exact signed versioned URL and allow one redirect under the signed CNB
policy. User credentials and GitHub API headers are not forwarded to CNB.

New catalog selections enforce the embedded minimum version/sequence and a
private per-user high-water record at
`%LOCALAPPDATA%/JishuDBAgentInstall/release-floor.json`. Updates reverify the
signature and current floor under an exclusive lock. Equal-sequence different
payloads fail as equivocation. A previously approved exact catalog remains
usable until its original expiry even if a newer transaction advances the
selection floor; a mutable latest pointer cannot retarget that approval.

The existing native parser rejects mirror URLs and unknown fields. At execute,
the helper extracts only the already-approved native raw bytes into the private
`native-install-plan.json` sibling and passes its previously bound digest to
NSIS. Existing child bytes must match; the helper never computes a digest for a
changed child and promotes that new value to authorization. The outer plan is
reloaded immediately before invoking NSIS. Native SID/path/lifetime admission
and unsigned-publisher/user-presence requirements remain in force.

The private download snapshot and temporary redirect cache are bound to the
outer approval digest; the snapshot additionally binds the catalog digest.
Partial bytes without an approval snapshot cannot be resumed. Full-file size
and SHA-256 remain mandatory; valid ranges alone do not authenticate partial
bytes. CNB checks plan/catalog expiry again after each bounded range before
appending it. Expired approval never renews itself and cannot authorize execute.
No cross-plan partial-cache reuse is implemented.

macOS source behavior is specified by its packaged helper and platform-specific
contract. Windows envelope/native-plan semantics must not be passed to macOS.

## Eligible release
## Eligible release

Enumerate published releases with the versioned API and a bounded maximum of
five 100-item pages. Fail if the bound prevents complete selection. Select the
greatest numeric SemVer `vX.Y.Z` release satisfying all of these conditions:

- `draft=false`, `prerelease=false`, and `immutable=true`;
- exactly one installer, adjacent `.sha256`, and adjacent `.candidate.json`
  asset for the current supported platform;
- every asset is uploaded and has a positive size and API
  `digest=sha256:<64 lowercase hex>`;
- candidate product, version, platform, bundle ID, source repository, source
  revision, artifact filename, artifact digest, distribution mode, and
  authorization mode match the release and platform contract;
- the candidate binds the fixed source repository and a full lowercase source
  revision inside the digest-protected immutable release asset.

The source repository may be private. Automatic installation never requests a
GitHub source-repository credential or treats private commit-API availability
as an installation prerequisite. Provenance for this path is the immutable
release, its API asset digests, adjacent checksum, and candidate manifest.

Normal installation must not use the mutable `latest` endpoint, lexical version
ordering, `target_commitish` as a source revision, a prerelease, or a differently
named artifact. The explicit macOS candidate route below is a separate opt-in.

## Asset transport

Metadata and source-commit requests accept only a direct HTTPS `200` and never
follow redirects. An exact API asset request accepts either a direct `200` (metadata), a
validated `206` (bounded installer range), or
one `302` to HTTPS `release-assets.githubusercontent.com`. Validate the redirect
before the second request, send no credentials or unrelated headers to it, and
reject user information, fragments, another redirect, or another host.

Hash every downloaded byte stream against its API digest. The adjacent checksum
must contain exactly the installer SHA-256 and filename. The candidate artifact
digest must match both. Re-fetch the release by immutable release ID before the
installer download and again after it; tag, target commitish, immutable state,
asset IDs, names, sizes, states, and digests must remain unchanged.

## Transaction plan

The Windows helper exclusively creates schema `jishudb-agent-install-plan-v1`
as a regular file, successfully assigns the current SID as owner, and verifies
one explicit current-user FullControl DACL. It contains no credential and uses
exact fields for:

- creation/expiry time and operation `fresh-install`;
- platform and current user binding;
- release repository, ID, tag, version, target commitish, and source revision;
- installer/checksum/candidate asset IDs, names, sizes, API URLs, and digests;
- application/data destinations and ownership acknowledgement;
- client name, configuration target, connection name, the exact selected MCP
  URL, and profile;
- publisher identity, Developer ID TeamIdentifier when applicable, and
  Gatekeeper or SmartScreen expectation.

The helper prints the plan path, SHA-256, and a redacted approval envelope.
Plan mode selects a currently free port from the bounded Desktop set. Execution
rechecks that exact port before product mutation, exclusively creates the
current-user-only schema-1 `desktop-endpoint.json`, and launches Desktop only
after the endpoint selection is durable. Execution accepts only that exact path
and digest. Unknown fields, invalid types, expired plans, non-local or redirected
paths, DACL drift, changed release identity, or changed destination/client/endpoint
fail before product mutation.

Invoke the helpers with argument arrays equivalent to the following SkillHub-compatible
package commands:

```text
zsh scripts/install-macos.sh plan \
  --client <client-name> \
  --config-target <absolute-client-config-path> \
  --connection-name jishudb

zsh scripts/install-macos.sh download \
  --plan <absolute-plan-path> \
  --plan-sha256 <approved-lowercase-sha256>

zsh scripts/install-macos.sh execute \
  --plan <absolute-plan-path> \
  --plan-sha256 <approved-lowercase-sha256>

node scripts/install-windows.js check

node scripts/install-windows.js plan \
  -Client <client-name> \
  -ConfigTarget <absolute-client-config-path> \
  -ConnectionName jishudb

node scripts/install-windows.js download \
  -PlanPath <absolute-plan-path> \
  -PlanSha256 <approved-lowercase-sha256>

node scripts/install-windows.js execute \
  -PlanPath <absolute-plan-path> \
  -PlanSha256 <approved-lowercase-sha256>
```

The Windows helper requires Node.js 22 or later and runs entirely as packaged
JavaScript. It resolves only local, non-redirected absolute system paths for
`whoami.exe` and `icacls.exe`, using them for SID lookup, creation-time owner
assignment, and current-user-only DACL operations. It must not materialize,
invoke, or change policy for PowerShell. Do not use shell interpolation, a token
argument, or an unreviewed helper copy. Parse the helper's single JSON result. A non-zero
exit plus `status=failed` is terminal for that plan; do not regenerate or retry
under the old approval.

## Platform completion

### macOS arm64

After approval, run `download` repeatedly with the same plan path and digest.
The first invocation fetches and validates the immutable release; continuations
revalidate that private snapshot against the approved plan. Execute re-fetches
the release before installation. The snapshot is published atomically only after validation,
so an interrupted request cannot become a reusable snapshot. Each step requests at most 16 MiB for at most
20 seconds per network request. It accepts partial bytes only on a
bounded curl timeout with an exact HTTP 206 Content-Range for the requested
offset, end and approved total. An ignored range, changed length/encoding,
transport error, or zero progress is a failure; it never appends that response.

`download_pending` is successful progress: show byte counts and continue the
same plan on the next host tool call. Do not loop inside one short foreground
command, restart the download, or regenerate the plan for this state. Allow at
least 120 seconds per step for metadata and validation overhead. Cache and
scratch files are private, scoped to the plan directory, and guarded against
symlinks/hard links and concurrent execution. A leftover lock after a host kill
requires inspection, not automatic removal or overlapping retries.

Only exact complete size plus SHA-256 yields `downloaded`. Then call `execute`;
it requires that complete asset and rechecks it before any installation.
The approved-host signed URL is kept only in the private transaction directory
for at most five minutes between calls, revalidated before use, and removed
when download completes. It is never printed or copied into task records. This
avoids consuming GitHub's anonymous API quota on every chunk. A 403/429 with
rate-limit headers returns `download_waiting` and `retryAfterSeconds`; honor
that delay without restarting, rotating plans, or introducing credentials. A
403 for a cached CDN URL invalidates it and returns `download_waiting` with
`download_url_refresh_required` for one fresh lookup. A freshly issued URL
failing the same way is terminal; do not loop on authorization failures.
Partial downloads never authorize mounting, launching, or client setup. macOS
plans have a two-hour lifetime displayed in the approval envelope to cover slow
connections; do not extend or edit an approved plan. Windows plans retain their
30-minute lifetime. An expired plan needs a new plan and approval.

All helper failures include their actual stage. Diagnose timeout, network,
range validation, checksum, Gatekeeper, mount, copy, and launch failures
separately. Do not infer sandbox denial from exit 137 or report a verified DMG
merely because a partial file exists.

Install a fresh verified bundle to `~/Applications/JishuDB.app` without
elevation. Mount the DMG read-only and without Finder, require exactly one
regular JishuDB bundle, validate its identity/version/runtime/release manifest,
and reject every absolute, dangling, or bundle-escaping symlink. Preserve only
relative symlinks that resolve inside the verified bundle, revalidate them after
staging and installation without removing quarantine, and atomically rename the
staged bundle into a previously absent destination. Detach on every exit.
Revalidate the installed receipt, then launch once through Launch Services.
Persist the reviewed endpoint at
`~/Library/Application Support/JishuDB/desktop-endpoint.json` before launch.

### Windows x64

The helper recognizes existing HTTP/HTTPS proxy environment variables, preferring
lowercase forms when both are set. It validates HTTP(S) proxy URLs without
printing credentials and re-executes the same Node helper once with
`--use-env-proxy` before any network request. This initializes Node's fetch
proxy dispatcher at startup; setting an environment variable after fetch has
initialized is not treated as sufficient. Proxy-capable Node (22.21+ or 24.5+)
is required only when a proxy is configured. Unsupported runtimes return
`unsupported_proxy_runtime`; invalid proxy URLs return `invalid_proxy_configuration`.

The child-only environment retains the user's NO_PROXY exclusions and adds
localhost, 127.0.0.1 and IPv6 loopback. API metadata, sidecars and installer ranges
all use this same proxy-enabled process. No configured proxy keeps the default
network path; proxy failure never triggers a direct fallback. Proxy credentials
stay in environment variables, not arguments, plans, logs or client entries.
The existing sanitized installer/Desktop launch environment remains unchanged.
The helper does not read system/PAC proxy settings, change OS settings, or
disable TLS verification.

After approval, call `download` with the approved plan path and digest in separate
host invocations (allow at least 120 seconds each). Each call requests at most
16 MiB with a 20-second transfer deadline. Only an exact HTTP 206 Content-Range,
identity encoding, and matching declared length permit saving bytes. A bounded
transfer timeout may preserve its validated prefix; other network failures and
invalid responses never append bytes. `download_pending` reports progress and
continues the same plan. `download_waiting` requires honoring retryAfterSeconds.
A private five-minute CDN URL cache and validated release snapshot avoid repeated
GitHub API calls; execute re-fetches the immutable release before installation.
A cached URL rejected with 403 is discarded for one fresh lookup; a fresh URL
rejected without rate-limit headers is terminal.

The cache is private, restricted to the plan directory, and rejects reparse
points and hard links. Download and execute share an exclusive lock. If a host
kills an invocation and leaves `download.lock`, inspect the recorded PID and
confirm it has exited before manually removing only that lock; do not overlap
invocations or delete the partial installer. Malformed locks require inspection.
Existing files from an older interrupted helper can be continued under the same
unexpired, approved plan only after their paths and private ACLs validate.

Only complete size and SHA-256 produce `downloaded`. Then invoke `execute`, which
rechecks the complete cache and never starts another full installer download.
It preserves downloaded files on failure for diagnosis. It revalidates expiry
immediately before starting NSIS. The Windows plan still expires 30 minutes from
creation (displayed in the approval envelope); never edit or extend it. Expiry
requires a new reviewed plan and is not a successful installation. Download
errors retain their stage/category; a partial file is never installation proof.

Use the per-user NSIS Agent-plan path only. The installer-path helper validates
the plan schema/digest, current SID, expiry, release, canonical non-reparse
application/data paths, absence of foreign content, and explicit data ownership
acknowledgement before NSIS prepares any path. Generic silent mode is not the
Skill path. Preserve the ordinary interactive installer pages. Revalidate the
Start Menu receipt, runtime, version, and data bootstrap, then launch once.
Write the reviewed endpoint beside `data-location.json` as
`desktop-endpoint.json` before launch. The Skill helper uses Node.js HTTPS,
streaming SHA-256 validation, argument-array process launch, and Windows-native
SID/ACL tools; PowerShell and its execution policy are not prerequisites.
Identity and ACL calls use asynchronous child-process pipes with a 30-second
deadline and a combined 1 MiB output limit. Start failures preserve their OS
cause; nonzero exits, timeouts, interrupted processes and excessive output remain
distinct errors. No shell substitution, alternate executable or skipped ACL
check is a compatibility fallback.

`desktop-endpoint.json` stores a reusable port preference. `data-location.json`
stores the data directory and instance identity. Neither file alone proves that
the application is installed. Planning reuses a valid endpoint and resolves
retained data through the bootstrap and matching `.jishudb-data-root` marker.
Endpoint and data-inspection problems appear as `preflightWarnings`; they do
not prohibit release discovery or verified download. Download validates the
approved release and bytes without requiring an empty product directory or a
free port. Execute enforces the current path, ownership and port checks before
starting an installer. It never deletes or silently overwrites saved preferences.

Valid retained data selects `jishudb-agent-reinstall-plan-v1` with
`operation=reinstall-preserve-data`, `launchMode=interactive-installer`, the
existing data directory, and `retainedData` containing the instance ID plus
SHA-256 digests of the bootstrap and root marker. The same private-plan,
current-user, expiry, immutable-release, catalog and asset checks apply. This
helper-only plan is never passed to the native `/JISHUDB_AGENT_PLAN` parser:
released Windows installers accept only absent destinations on that silent path.

Reinstall execute requires application executables to be absent and verifies
that the retained location/ownership still matches approval. An absent or empty
application directory is accepted. A bounded tree containing only Python
`resources/runtime/python/**/__pycache__/*.pyc` uninstall residue is also accepted
without deleting it. Existing application markers (`JishuDB.exe`, `app.asar`, or
the service executable), unrecognized files, links and oversized residue trees
stop execution for review. These checks run again before starting the installer.
It asks the verified Windows desktop shell (`explorer.exe`) to open the
already verified installer in its ordinary interactive mode and waits for shell
dispatch to finish. This prevents a direct detached installer child from being
killed with the tool host's job. The helper returns `user_action_required`,
`launchStatus=requested`, the exact `installerPath`, and
`next=complete_interactive_reinstall_and_verify_existing_data`. The native
installer reads the retained bootstrap and validates data ownership. The user
confirms the approved application directory, keeps the existing data directory
selected, and completes the native pages. An exclusive
transaction receipt prevents a repeated execute from starting another installer.
Cancellation or launch failure requires inspection before another approved
attempt; never fall back to silent fresh installation or claim completion.
Confirm the actual installer window after the tool call returns: Explorer exit
codes 0 and 1 can both indicate dispatch, and neither establishes GUI visibility.
After user completion, verify the installed version/revision, bootstrap,
original data directory and instance identity, then continue normal health and
client checks. A directory without a valid bootstrap or matching marker needs
explicit recovery; the helper never guesses a database location.

Execute rechecks destinations and endpoint compatibility before starting NSIS
and checks the saved endpoint again before launch. If NSIS has already succeeded
but receipt verification or launch fails, the error includes
`installation.status=installer_completed` and
`installation.next=verify_existing_installation_before_launch`, retaining the
original error category. Do not repeat `execute` or reinstall over these files.
Verify the installed version/revision, runtime and data bootstrap against the
approved release, check the endpoint and process state, then continue the
previously approved launch of that exact application. An expired installation
plan never authorizes rerunning NSIS or overwriting existing state. Process
launch is not MCP readiness; continue the normal health, OAuth and host-tool
discovery checks, leaving human consent to the user.

## Stop conditions

Stop without retry or fallback when any trust input, plan field, digest,
candidate field, redirect, source-revision binding or release re-fetch is invalid
or ambiguous. Product-state inspection warnings do not block verified download,
but invalid installation receipts or endpoint/data identity block execution.
Never overwrite an
existing app, upgrade, select a different data directory, delete partial product
state, weaken OS security, or offer a manual unverified download under the old
approval.

## Agent background launch and runtime negotiation

The legacy `jishudb-agent-install-plan-v1` contract remains foreground-only.
A verified immutable candidate may optionally declare `agentBackgroundLaunch`
with the integer value `1`. This declares presentation/installer support only;
it does not enable owner creation or prove that OS verification is available.
Unknown marker values are rejected.

For this candidate, helpers produce `jishudb-agent-install-plan-v2` with the
additional exact field `launchMode: "agent-background"`. Both validators require
that pairing; v1 forbids the added field. The redacted approval envelope reports
the launch mode, and the existing SHA-256 binds it along with all destinations,
release assets and client settings. Execute revalidates the candidate marker
against the reviewed plan. Drift requires a new plan and approval.

The macOS executor uses `/usr/bin/open -g <approved-app> --args
--jishudb-agent-background`. The Windows executor passes the single argument
`--jishudb-agent-background` directly to the installed executable after the
silent plan-bound installer succeeds. It does not pass `--force-run` to NSIS;
the helper remains the single initial launch owner. Existing v1 executors keep
their ordinary launch. The Windows installer path helper validates both schemas.

After launch, verify health identity, then read local public
`/api/service/capabilities` and the `agentOnboarding` schema-1 object without
redirects or credentials. Route `initial-consent` or `owner-consent` only when
`supported` is true. `password-login` retains normal login; `password-setup`,
`unavailable`, missing or unknown capability means ordinary setup may be needed.
The new-account rollout flag is independent of support for existing unset
owners. Discovery does not substitute for owner verification, legal acceptance,
OAuth PKCE or explicit write consent. Never infer success from process launch.

Candidate workflows expose an explicit `agent_background_launch` opt-in that
defaults to false. Private onboarding builds also declare this presentation
support when `agent_onboarding` is selected. Windows public preparation preserves
the source candidate's marker; it cannot add support to older binaries.
New-owner creation uses a separate bundled policy and must still be discovered
at runtime. Package release, helper/Skill promotion and device acceptance have
their own recorded status; source support does not imply published availability.

### Signed macOS and Windows updater-release compatibility

For macOS, prefer `jishudb-desktop-X.Y.Z-darwin-arm64.dmg` when that release
contains signed assets, together with its exact adjacent `.sha256` and
`.candidate.json`. A partial signed asset set does not fall back to the unsigned
asset set in the same release. Schema-3 metadata requires Developer ID, matching
authorization/distribution TeamIdentifiers and complete notarization evidence.
The plan includes `publisher.identity=developer-id`, `gatekeeper=accepted` and
the exact TeamIdentifier, all bound by its digest. Legacy schema-2 unsigned
DMGs retain their existing explicit unsigned contract.

Before mounting a signed DMG, the helper verifies its signature, Developer ID
authority, TeamIdentifier and Gatekeeper assessment. It verifies the app at
the mounted, staged and installed paths as well. Failure stops installation or
launch; it never strips quarantine, disables Gatekeeper or changes the declared
publisher to obtain success. These checks use system `codesign` and `spctl`.

The current Windows public updater workflow uses Ed25519-signed manifests with
an explicitly unsigned NSIS executable. Public preparation emits the existing
schema-1 `<installer>.candidate.json` and exact `<installer>.sha256`, after
checking final installer bytes against the update candidate. Background support
is copied from that candidate. The installer helper continues to verify the
immutable GitHub API asset digests, checksum, source binding and explicit
unsigned-executable policy. It does not claim to verify an Authenticode
signature or consume the mutable updater feed. Authenticode-only rehearsal
artifacts are not converted into this unsigned contract.

Older immutable updater releases missing the required installer sidecars are
not retroactively changed. Do not substitute `latest.yml`, an update-candidate
file, or a locally invented manifest for a missing installer contract.

## Runtime preparation after installation

Installation success and MCP connection success do not establish retrieval
readiness. Supported fresh Agent onboarding discloses the built-in embedding
model, transfer/disk requirements and trusted Hugging Face/domestic mirror
sources on the browser consent page. The user authorizes bounded preparation
with the same consent submission; it is not authority contained in the installer
plan or launch flag. The owned service starts the job after committed consent,
without delaying OAuth code exchange. Preparation authority lasts seven days;
it does not grant administrator APIs or arbitrary model/provider changes.

The Skill observes `kb_get_readiness` and uses `kb_prepare_runtime` only when the
actual runtime advertises eligibility. Both tools belong to the existing MCP
server. Reuse valid models and bundled basic OCR. Ordinary manual installation
retains its current setup UI. A missing capability, external provider, expired
preparation authority or failed runtime probe must remain an explicit recovery
state, never an instruction to copy credentials or access Desktop data directly.

## Fresh Windows initial consent

Only a runtime advertising both `authorizationMethod=windows-fresh-install` and
`deviceVerification=not-required-for-fresh-install` on `initial-consent` uses the
compiled fresh-local-install authority instead of an OS identity prompt. The
user still accepts terms and permissions in the OAuth page; browser binding,
PKCE, private signed Desktop handoff and atomic one-time initialization remain
mandatory. This is not native physical-presence verification and cannot be
selected by a client parameter. Existing owners and later sensitive operations
retain verification. Ordinary direct installation retains normal password setup.

## Explicit macOS candidate rehearsal

For a user-authorized macOS test only, add both `--candidate-tag` and
`--candidate-revision` to the normal `plan` command. The tag must be exactly
`vX.Y.Z` (the protected publication workflow's prerelease tag) or
`vX.Y.Z-desktop-candidate.N` (positive N); the revision must be the approved full
40-character lowercase source SHA. Do not infer either value, select a newer
candidate, or use this mode because stable setup failed.

The helper fetches only that exact tag from the fixed official release repository.
It requires `draft=false`, `prerelease=true`, `immutable=true`, a signed/notarized
macOS artifact, the requested source revision, and background launch support.
There is no unsigned, stable or alternate-host fallback. The resulting plan uses
`jishudb-agent-install-plan-v3`, `releaseChannel=candidate`, and
`launchMode=agent-background`. The exact tag, source, artifact digests and signer
are part of the approved plan and its SHA-256; the approval envelope displays
the channel, tag and source explicitly.

Execute takes only the unchanged plan path and SHA-256. It rejects candidate
selection flags, rechecks the prerelease state and exact assets before and after
download, and retains all ordinary hash, signer, notarization, quarantine,
per-user path, endpoint and user-consent checks. Changing prerelease/stable state,
revision, tag, assets or launch policy invalidates the plan. Ordinary v1/v2
plans remain stable-only. This rehearsal mode does not change Windows plans.
