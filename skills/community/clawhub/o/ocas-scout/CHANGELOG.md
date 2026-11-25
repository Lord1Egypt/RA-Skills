## [4.1.0] - 2026-09-16

### Added
- **Dossier storage** — intermediate OSINT research stored at `{agent_root}/commons/data/ocas-scout/dossiers/{SUBJECT}.md` (one per research subject, prior-to-brief); documented in `references/storage-layout.md`.
- **`MCPDiscoveryRecord` standard** — discovery probes cached per normalized query with a strict 24-hour TTL; documented in `references/scout_mcp_discovery.md` per `spec-ocas-skill-improvements.md`.

## [2.10.0] - 2026-04-12

### Added
- Handle extraction phase: after Tier 1 collection, Scout identifies high-confidence handles (@ prefixes, URL path usernames, labeled aliases)
- Sherlock expansion: calls `sherlock(handle)` when Sherlock skill is installed; falls back to targeted `sift.search("site:platform 'handle'")` queries when not
- Tiered verification: top 3 Sherlock results verified immediately via sift.extract; 2-3 sampled; remainder surfaced on request
- Identity gate (invariant 7): requires 2+ overlapping data points from seed to mark a profile `verified`; username match alone is `unverified_lead`
- Recursive discovery capped at 2 total Sherlock passes (alias chain following)
- Social Graph section in brief output: verified profiles with evidence, unverified leads listed separately
- Near-match flag: profiles matching name but contradicting seed attributes are surfaced for user review rather than silently dropped

### Removed
- `python3` from `requires_binaries` (no Python scripts in Scout package)

## [2026-04-05] Hunter.io parallel OSINT integration

### Added
- Hunter.io fires in parallel with all Scout research sources when `HUNTER_API_KEY` is set
- Three parallel Hunter queries per research run: domain-search, email-finder, author-finder
- Professional Contacts section added to output brief format
- `scout.init` step 8: browser-guided free Hunter.io account creation and API key setup

### Changed
- Source waterfall updated: all configured sources now fire in parallel (no sequential escalation)

### Validation
- ✓ Version: 2.7.2 → 2.8.0

## [2026-04-04] Spec Compliance Update

### Changes
- Added missing SKILL.md sections per ocas-skill-authoring-rules.md
- Updated skill.json with required metadata fields
- Ensured all storage layouts and journal paths are properly declared
- Aligned ontology and background task declarations with spec-ocas-ontology.md

### Validation
- ✓ All required SKILL.md sections present
- ✓ All skill.json fields complete
- ✓ Storage layout properly declared
- ✓ Journal output paths configured
- ✓ Version: 2.7.1 → 2.7.2

# CHANGELOG

## [2.9.1] - 2026-04-08

### Storage Architecture Update

- Replaced $OCAS_DATA_ROOT variable with platform-native {agent_root}/commons/ convention
- Replaced intake directory pattern with journal payload convention
- Added errors/ as universal storage root alongside journals/
- Inter-skill communication now flows through typed journal payload fields
- No invented environment variables — skills ask the agent for its root directory


## [2.9.0] - 2026-04-08

### Multi-Platform Compatibility Migration

- Adopted agentskills.io open standard for skill packaging
- Replaced skill.json with YAML frontmatter in SKILL.md
- Replaced hardcoded ~/openclaw/ paths with {agent_root}/commons/ for platform portability
- Abstracted cron/heartbeat registration to declarative metadata pattern
- Added metadata.hermes and metadata.openclaw extension points
- Compatible with both OpenClaw and Hermes Agent


## [2.7.1] - 2026-04-02

### Changed
- Aligned Tier 1 platform search with Sift's shared search stack (agent-reach now provided by Sift)
- Scout no longer implements its own parallel search — delegates to Sift infrastructure

## [2.7.0] - 2026-04-02

### Added
- Tier 1 parallel search with agent-reach: Tavily/DuckDuckGo + platform search (Twitter/X, Reddit, LinkedIn, GitHub, Weibo, etc.)
- Deduplication by URL and content hash for merged search results
- Source waterfall updated to document parallel execution model

## [2.6.0] - 2026-04-02

### Added
- `user_relevance` field on all emitted Elephas signals (default `agent_only` for research, `user` when user-requested)
- Structured entity observations in journal payloads (`entities_observed` with relevance tags)

## 2.5.0 — 2026-03-30

### Added
- `references/plans/contact-enrichment.plan.md` — bundled workflow plan: Weave lookup → Scout research → Weave social graph update
- Ontology mapping: Scout extracts Entity/Person, Entity/AI, and Thing/DigitalArtifact types
- Weave cooperative read interface documented in Optional skill cooperation

## Prior

See git log for earlier history.
