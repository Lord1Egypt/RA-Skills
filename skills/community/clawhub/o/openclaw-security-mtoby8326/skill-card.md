## Description: <br>
OpenClaw Security scans OpenClaw session content for sensitive personal data across CN, US, AU, UK, DE, FR, SG, MY, TH, and ID regions and records masked local audit events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtoby8326](https://clawhub.ai/user/mtoby8326) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to audit user input, prompts, conversation context, and knowledge-base content for PII before or during OpenClaw workflows. It is intended for local privacy audits where masked findings, risk level, source type, and audit status need to be retained as NDJSON records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session, prompt, context, or knowledge-base content may contain sensitive personal data. <br>
Mitigation: Enable the skill only for authorized content sources and review audit scope before starting background scans. <br>
Risk: Passing sensitive content through command-line arguments can expose it in process metadata. <br>
Mitigation: Use file-based scans with --delete-after-read for background or automated audits; reserve --text for short manual tests. <br>
Risk: Sampling and cache behavior can skip repeated or sampled content when full coverage is required. <br>
Mitigation: Use --no-cache when complete scan coverage matters. <br>
Risk: Local audit records and retention settings may not match the deployment's privacy requirements. <br>
Mitigation: Review the audit directory, configure retention, and run cleanup.py --dry-run before deleting records. <br>
Risk: Inputs longer than 32,768 characters are truncated before scanning. <br>
Mitigation: Split larger content into smaller authorized files when full-content scanning is required. <br>


## Reference(s): <br>
- [Detection Patterns Reference](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON scan summaries, local NDJSON audit records, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local-only audit records store masked previews and content hashes; input is capped at 32,768 characters and audit retention defaults to 7 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
