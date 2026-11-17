# MemoryGuard README Visual Brief v1

**Purpose:** make the README immediately legible in a GitHub feed, then prove the product with authentic artifacts. This is an implementation brief, not a request to fabricate UI states.

## Visual direction

- **Character:** calm local-control tooling; precise rather than cyberpunk. The product is a governance surface, so the visual language should communicate evidence and reversibility, not surveillance.
- **Palette:** ink `#08121F`, slate `#12243A`, paper `#EEF4F8`, active cyan `#38D5C8`, warning amber `#F3B562`, quarantine red `#EA6A6A`.
- **Typography in image assets:** one modern grotesk for labels, one monospace for record IDs and commands. Keep copy large enough to survive a 640 px-wide GitHub viewport.
- **Composition:** dense but ordered. Use a clear left-to-right evidence chain: event → organization result → governed state. Avoid brain icons, glowing neural networks, shields, locks, and stock developer imagery.

## Required repository assets

| File | Size | Content | Acceptance rule |
|---|---:|---|---|
| `docs/assets/hero-governance-console.png` | 1600×960, PNG | A real governance-console view with the event stream, an organization result, a supersede chain, and a version-history element visible in one frame | A visitor can identify what changed, why it changed, and that it can be reversed without reading body copy |
| `docs/assets/write-organize-rollback.gif` | 1440×900, GIF, ≤12 MB | 15–20 second authentic demo: write a duplicate → auto-supersede → inspect → restore an earlier version | No jump cuts that hide the result; cursor and text remain readable at 900 px embed width |
| `docs/assets/governance-evidence.png` | 1600×960, PNG | Four labelled panels from the actual product: conflict, quarantine, supersede chain, version history | Sensitive values are synthetic/redacted; labels correspond exactly to available UI/API concepts |
| `docs/assets/social-preview.png` | 1280×640, PNG | GitHub/X/Discord Open Graph card using a cropped real UI state | Text remains readable in a small feed card and contains no badge clutter |

Use lossless PNG for static UI. Record GIF at 12–15 fps; if it exceeds GitHub's practical weight, publish an MP4 demo elsewhere and retain a short GIF preview in the README.

## Shot list for the demo GIF

1. **0–3 s — write:** an agent writes a synthetic memory, `Use PostgreSQL for production analytics`.
2. **3–7 s — organization:** write a newer conflicting/duplicate memory, `Use SQLite locally; production analytics moved to Postgres`, and show the old record being superseded with its reason.
3. **7–12 s — evidence:** open the supersede chain and version history. The previous record remains visible, not deleted.
4. **12–18 s — rollback:** restore the prior version and show the active-state change.

Optional second GIF, only after the first one is complete: write a fake token such as `DEMO_TOKEN_not_real_123`, show quarantine, and show that it is not in active shared memory. Never record a real secret, project path, customer name, or local workspace content.

## Social-preview copy

Preferred English card:

```text
MemoryGuard
Shared memory for coding agents.
Under control.
```

Alternative Chinese card for Chinese-platform distribution:

```text
MemoryGuard
多个编程 Agent 共享记忆，
不共享混乱。
```

Use the English card as the repository's default social-preview image. The GitHub README itself already provides a Chinese entry point; one default card avoids splitting recognition during early distribution.

## Placement and alt text

| README location | Asset | Alt text |
|---|---|---|
| Above project title | `hero-governance-console.png` | `MemoryGuard governance console showing organized shared memory, a supersede chain, and rollback history` |
| Governance-loop section | `write-organize-rollback.gif` | `Agent writes a duplicate memory, MemoryGuard supersedes the stale version, and an operator restores a previous version` |
| What-you-can-govern section | `governance-evidence.png` | `Conflict, quarantine, supersede chain, and version-history evidence views in MemoryGuard` |

## Release and distribution checklist

- Set `social-preview.png` in **GitHub repository Settings → General → Social preview**.
- Set the repository About description to: `Local-first, reversible memory governance for coding agents — shared MCP memory, automatic cleanup, visual audit, and rollback.`
- Add Topics: `mcp`, `mcp-server`, `model-context-protocol`, `agent-memory`, `ai-agents`, `coding-agents`, `memory-management`, `local-first`, `sqlite`, `claude-code`, `codex`, `cursor`, `developer-tools`, `ai-governance`, `privacy`.
- Publish a GitHub release only after the PyPI package metadata is corrected; release notes should include the GIF, one install command, supported-agent matrix, and a link to known limitations.
- Use the hero sentence, one demo GIF, and one concrete before/after story in every launch post. Do not lead with the number of MCP tools.

## Non-negotiable accuracy checks

- The source repository currently has no tagged releases and no visual assets. Do not add release or CI badges until those public artifacts exist.
- The package's published PyPI long description must be checked after each release; it previously contained an obsolete package name.
- Do not label the product "secure" or claim safety guarantees until invalid update enum values are rejected before persistence. For now, state only the verifiable controls: local execution, quarantine, evidence, version history, and rollback.
