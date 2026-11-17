## Description:

Manage a personal travel Markdown database for food finds, places, guides, screenshots, preferences, Notion synchronization, and trip planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jichengkai](https://clawhub.ai/user/jichengkai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to capture travel tips, organize a local Markdown travel database, check duplicates, sync selected records with Notion, and produce recommendations or itinerary drafts grounded in saved travel knowledge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save screenshots, OCR text, preferences, trip dates, and places as private travel data on disk or in Notion.

Mitigation: Review and limit the travel database location before installation, keep sensitive records local when possible, and treat Notion export as an explicit user-approved action.

Risk: Travel queries or records may be sent to external search, map, or Notion services when enrichment or sync features are used.

Mitigation: Use dry runs first, require explicit approval before external searches or Notion writes, and clearly separate local knowledge from newly checked external information.

Risk: Misplaced Notion or map API credentials could expose private account access.

Mitigation: Store tokens and API keys in a local secret store or environment file, never in chat or travel-db files, and rotate any token that appears in chat.

Risk: Apply-mode commands can create, update, sync, or overwrite travel records.

Mitigation: Run validation and dry-run commands before using --apply, and use strict sync behavior to block overwrites when Notion-side edits may conflict with local records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jichengkai/skills/personal-travel-butler)
- [Travel Database Schema](references/database-schema.md)
- [Ingestion Workflow](references/ingestion-workflow.md)
- [Recommendation Workflow](references/recommendation-workflow.md)
- [Notion Sync Folder Standard](references/notion-sync-folder-standard.md)
- [Notion Integration Guide](references/notion-integration.md)
- [Notion Sync Schema](references/notion-sync-schema.md)
- [Travel Search System](scripts/SEARCH_README.md)
- [Notion API versioning](https://developers.notion.com/reference/versioning)
- [Notion request limits](https://developers.notion.com/reference/request-limits)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown entries, JSONL records, command suggestions, configuration guidance, and concise travel planning text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local travel-db Markdown and JSONL files, refresh indexes, and use Notion or search APIs when configured and approved.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
