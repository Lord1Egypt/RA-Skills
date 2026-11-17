# Hui-Yi 1.2.13

This release includes the unreleased 1.2.12 security fixes and the 1.2.13 compatibility and recall improvements.

## Changes

- Harden Python and TypeScript file operations against linked paths, traversal, hard links and unexpected file replacement. Preserve Windows file permissions and protect configuration backups before writing their content.
- Keep diagnostic output free of conversation text, raw identifiers and matching terms by default. Explicit retrieval and feedback retain their documented content contracts.
- Repair Chinese natural-language matching, Latin word boundaries, duplicate-query weighting and relevance-first ranking. Repeated use cannot admit an unrelated result. Hui-Yi archive search excludes explicit fixtures, inactive and superseded entries.
- Preserve full summaries, nested paths, lifecycle metadata and real activation deduplication during index rebuilds. New notes start with zero actual conversation activations.
- Add a source-verified tool for annotating existing primary-memory bullets with trigger metadata. It preserves fact text and counts and makes permission-preserving backups.
- Add an optional OpenClaw 2026.9.5 integration using the public memory-host-search SDK. After explicit setup, the adapter injects related trusted primary-memory evidence before private WebChat answers. The setup grants the required conversation-hook permissions, enables native dreaming, and disables the overlapping built-in recall entry and legacy hook.
- Handle cold memory-manager initialization and reuse the host's shared manager. Optional diagnostics record selected and actual model-input block/reference counts only.

## Validation

Windows validation: 100 Python tests passed with one POSIX-only skip; 40 legacy hook tests and 21 native adapter tests passed. The skill metadata and archive consistency checks passed. The adapter was tested through the actual host PluginInstance loader.

A controlled private WebChat query selected one primary-memory entry; the actual model-input callback observed its memory block and source reference, and the final answer cited the correct source. The agent also used normal memory_search to verify details. This proves that recall path, not universal accuracy or retrieval-free answers.

The native daily dreaming job was confirmed enabled at 03:00 Asia/Shanghai. New-message extraction and promotion are asynchronous; the subsequent scheduled run was not claimed as already verified. Existing source facts were preserved during the controlled cache repair.

## Upgrade boundaries

Follow [native-memory.md](native-memory.md) to preview and explicitly apply native integration. Installing or loading the skill alone does not enable collection or change host configuration. Host-configured model and embedding services may perform network requests and incur costs.

The adapter currently supports the reviewed OpenClaw 2026.9.5 runtime and fails closed after an unreviewed host upgrade. Automatic recall is restricted to configured private WebChat agents; external channels require separate identity and isolation review. This is a shared workspace archive, not per-user storage isolation. The runtime hash check does not pin all transitive dependencies.

File checks are application-level protections, not a kernel sandbox against a malicious same-account process. Updating existing Windows files through the legacy TypeScript hook preserves permissions but is not crash atomic.

Publication is separate from ClawHub's independent security review. See the historical [1.2.12 security report](security-upgrade-1.2.12.md) for the original findings and remediation boundaries.
