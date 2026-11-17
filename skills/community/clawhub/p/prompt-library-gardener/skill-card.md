## Description:

Clean, tag, and index a user-provided prompt collection so the right prompt can be found, reused, and improved quickly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to organize prompt collections they provide in the conversation. It creates a cleaned library with job-based groups, consistent names, practical tags, duplicate decisions, reuse notes, and a maintenance checklist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A user may ask the skill to find prompts in notes, chat history, cloud drives, browser history, email, or local files.

Mitigation: Use only prompt text and context the user deliberately pastes, uploads, or summarizes in the conversation.

Risk: Prompt libraries may contain confidential business details, personal data, credentials, or other sensitive content.

Mitigation: Ask users to redact secrets or use placeholders, and keep the work limited to the current conversation.

Risk: Automated grouping, tagging, and duplicate decisions can be wrong when prompt intent or usage history is unclear.

Mitigation: Mark uncertain classifications as provisional and ask for user decisions before treating variants as merged, stale, or archived.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/prompt-library-gardener)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tables and concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include prompt inventories, job groups, duplicate review logs, naming rules, tag rules, reuse notes, and maintenance checklists.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
