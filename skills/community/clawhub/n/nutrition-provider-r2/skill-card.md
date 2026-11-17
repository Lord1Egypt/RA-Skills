## Description:

Crawls Vietnam nutritional portal foods and prepared-dish JSON records with scrapling-official and uploads each raw provider record to Cloudflare R2 with stable object keys and page pacing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snailb1007](https://clawhub.ai/user/snailb1007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to ingest raw records from the Vietnam nutrition foods and prepared-dish lookup APIs into a controlled Cloudflare R2 bucket while preserving provider data and crawl metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud storage credentials could grant broader access than the ingestion task requires.

Mitigation: Use R2 credentials scoped to the target bucket and prefix, and avoid exposing unrelated secrets in the environment.

Risk: Unexpected provider payloads could be uploaded without review.

Mitigation: Review fetched payloads before upload and preserve raw provider fields without schema inference.

Risk: Repeated runs could duplicate or overwrite records across provider sources.

Mitigation: Use stable record identifiers, enable skip-existing behavior when appropriate, and keep separate R2 namespaces for foods and prepared dishes.

Risk: High crawl or upload throughput could overload the provider.

Mitigation: Run page-sequential crawls and enforce the documented minimum 60 second crawl-plus-upload window for each page.

Risk: Unpinned helper dependencies can reduce repeatability.

Mitigation: Prefer pinned or locked Python dependencies for repeatable runs.

## Reference(s):

- [Source Notes](references/source-notes.md)
- [Vietnam Nutrition Food Lookup](https://viendinhduong.vn/vi/cong-cu-va-tien-ich/gia-tri-dinh-duong-thuc-pham)
- [Vietnam Nutrition Prepared-Dish Lookup](https://viendinhduong.vn/vi/cong-cu-va-tien-ich/gia-tri-dinh-duong-mon-an)
- [ClawHub Skill Release](https://clawhub.ai/snailb1007/skills/nutrition-provider-r2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs agents to preserve raw provider records, use stable R2 object keys, and upload one JSON object per provider record.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
