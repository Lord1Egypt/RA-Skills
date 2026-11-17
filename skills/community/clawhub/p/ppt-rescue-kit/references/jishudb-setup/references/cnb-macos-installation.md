# macOS CNB installation transport

The canonical macOS helper defaults to CNB for signed macOS ARM64 releases.
Use `--release-source github` to select GitHub explicitly. CNB requires Node.js 22 or
newer for the bundled Ed25519 catalog verifier; GitHub mode retains its existing
zsh/JXA requirements. The helper does not install Node automatically.

```sh
zsh scripts/install-macos.sh plan --release-source cnb \
  --client workbuddy --config-target /absolute/path/to/mcp-config.json

zsh scripts/install-macos.sh download \
  --plan /absolute/path/to/install-plan.json --plan-sha256 APPROVED_SHA256

zsh scripts/install-macos.sh execute \
  --plan /absolute/path/to/install-plan.json --plan-sha256 APPROVED_SHA256
```

Use the returned plan path and its approved digest unchanged. Repeat `download`
with that same plan while the result is `download_pending`. Execute only after
the result is `downloaded`. Selection is stable-channel only; candidate flags
are not supported with CNB. There is no automatic fallback to GitHub.

The bundled `scripts/release-mirror-trust.json` defines the anonymous catalog
entry, independently approved public key, minimum version and sequence, and
bootstrap redirect paths. Neither a downloaded catalog nor a command-line
argument can supply a replacement trust key. Public mirror publication and
real macOS acceptance are separate release gates; configuring this entry does
not prove that the catalog or packages are available.

The plan embeds the exact signed catalog, its digest and transport binding.
Its canonical GitHub release and asset IDs remain provenance fields. In CNB
mode those identities are resolved only to signed mirror locations: catalog
discovery, sidecars, download and pre-install checks make no GitHub requests.
Each download/execute invocation verifies the approved catalog signature,
expiry, embedded release floors and artifact bindings again. A newer mutable
channel pointer does not silently replace an approved selection. The original
plan and catalog must both remain unexpired; retries never extend either.

New plan discovery retains the highest accepted sequence/version in the private
`~/.cache/jishudb-agent-install/cnb-release-state.json` file. Reusing a sequence
for different signed contents fails as catalog equivocation. A state lock blocks
concurrent or interrupted discovery; it is not silently removed or reset.

Downloads request at most 16 MiB for 20 seconds per step. Only exact HTTP 206
ranges can extend the private cache; timeout prefixes are retained only after
range validation. Complete size and SHA-256 must match before execution.
Metadata authentication failure, invalid signature, stale catalog, rollback,
blocked origin, invalid range, digest mismatch and plan expiry are separate
errors. None triggers a different source, release or renewed approval.

CNB transport does not relax Developer ID, exact TeamIdentifier, Gatekeeper,
notarization, mounted/staged/installed app checks, fresh-install boundaries,
or the original application and data paths. macOS prompts, browser consent,
owner verification and client trust remain user-presence steps.

Source verification covers injected CNB HTTP responses, blocked GitHub access,
signature/catalog changes, expiry, rollback, bounded resume, range validation,
digest checks and the actual embedded JXA plan logic. Real zsh/JXA orchestration
and signed installation still require macOS arm64 device acceptance.
