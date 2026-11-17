## Description:

Behavior-driven taste model built from real consumption signals that scans email and calendar data, enriches entities with taste-relevant attributes via Google Maps, and generates discovery-focused recommendations that respect dietary restrictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Taste to build and query a personal preference model from consumption signals across email, calendar, Spotify, and transaction-derived restaurant data. It supports evidence-grounded recommendations, signal ingestion, entity enrichment, model status checks, and periodic taste summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad access to sensitive personal accounts and consumption records, including Gmail, Calendar, Spotify listening history, and transaction-derived restaurant data.

Mitigation: Install only after reviewing requested credentials and OAuth scopes, confirm the authenticated Google account before scans, and limit environment variables to the minimum workflows being used.

Risk: Credential fallback and auth-repair behavior can make it unclear which account or token source is active.

Mitigation: Run documented pre-flight checks, report token failures instead of silently skipping them, and verify the active account before reading email or calendar data.

Risk: Self-update and backup behavior can change local skill code or preserve sensitive personal data longer than expected.

Mitigation: Disable or tightly control update and backup commands before use, and review how stored signals, extractions, journals, and backups can be deleted.

Risk: Known scan and enrichment paths can produce misleading or corrupted preference data, including broken historical email dating and enrichment persistence issues.

Mitigation: Avoid documented broken historical scan paths, run verification scripts after Styx delta writes, and validate signal dates, deduplication, and enrichment persistence before trusting recommendation output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/indigokarasu/skills/ocas-taste)
- [API authentication patterns](references/api_auth.md)
- [Script inventory](references/script_inventory.md)
- [Storage layout](references/storage_layout.md)
- [Spotify sync](references/spotify_sync.md)
- [Styx delta ingestion](references/styx_delta.md)
- [Styx place_id deduplication](references/styx_delta_placeid_dedup.md)
- [Historical scan date bug](references/scan_historical_date_bug.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON/file updates, and structured recommendation text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or update local JSONL stores and journals when the host agent executes the described workflows.]

## Skill Version(s):

3.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
