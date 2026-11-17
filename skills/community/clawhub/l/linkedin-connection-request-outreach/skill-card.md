## Description:

Writes short LinkedIn connection notes and follow-up messages that fit the platform's character limits and stay inside its terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US B2B founders, sales development representatives, and recruiters use the skill to draft concise LinkedIn connection notes and follow-up messages, and to check outreach details before sending.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The optional Windows toolkit is unsigned and separate from the bundled Python workflow.

Mitigation: Prefer the bundled Python workflow; treat the toolkit as a separate software trust decision, since a matching checksum does not establish that it is safe.

Risk: The checker overwrites length-check.md in its output directory and measures the whole input file rather than extracting note_draft.

Mitigation: Use a dedicated output directory and check the final message length separately before sending.

## Reference(s):

- [LinkedIn outreach limits and US outreach rules](artifact/references/linkedin-outreach-rules.md)
- [ClawHub release](https://clawhub.ai/rapidworker1/skills/linkedin-connection-request-outreach)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Labeled Markdown containing outreach messages and a profile checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short outreach drafts with platform character limits and non-contact guardrails.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
