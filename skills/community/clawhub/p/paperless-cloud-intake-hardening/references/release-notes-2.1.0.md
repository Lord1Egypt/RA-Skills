# Release Notes - 2.1.0

## Scope

This is a 2.1.0-class hardening update for `paperless-cloud-intake-hardening` because 2.0.0 is already visible in the registry. The update does not redesign the Paperless intake pattern; it documents the constrained macOS helper/node boundary and tightens nudge governance.

## Provenance

Developed from agent-assisted testing and review in a constrained macOS/OpenClaw environment; published by `@Talonpoint`.

## Tested Boundary

This guidance was retested after tightening OpenClaw node/helper control boundaries. Broad Node permissions were not restored, no new Node or helper-app permissions were added for the retest, the connected macOS node had no Accessibility or Screen Recording grant, and `system.run` plus `screen.snapshot` were not advertised. Quick Look automation remained deprecated and was not used.

Most helper-app boundary work was environment/security architecture work, not a large skill rewrite. The reusable skill change is guidance-level: classify the provider, prove readability before delivery, avoid broad runtimes for privacy-gated actions, deprecate Quick Look automation, and leave unreadable placeholders pending when constrained hydration is unavailable.

## Platform Notes

Linux and Windows users can still use the Paperless pattern: stage before consume, validate bytes, deduplicate, deliver atomically, verify Paperless ingestion, and keep retry/reconciliation paths. Replace macOS-specific File Provider, Finder, iCloud, Quick Look, and TCC/helper instructions with platform-specific provider and permission controls.

## Requested Feedback

Useful edits include provider-specific commands, placeholder/read-failure signatures, permission-boundary guidance, and causal tests that prove pre-delivery read failure and post-nudge read success.
