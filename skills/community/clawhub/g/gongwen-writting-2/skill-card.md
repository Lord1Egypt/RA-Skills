## Description:

A Chinese official-document drafting skill for enterprise and government office staff that uses online templates and writing frameworks to draft, revise, format, and review 38 common document types.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yourtsao](https://clawhub.ai/user/yourtsao)

### License/Terms of Use:

MIT-0

## Use Case:

Office, administrative, and document-writing staff use this skill to turn Chinese official-document requests, notes, meeting material, and draft points into structured formal drafts. It supports common documents such as requests, reports, summaries, speeches, notices, minutes, plans, and research reports, with missing facts marked for user completion.

### Deployment Geography for Use:

Global (China-focused official-document workflows)

## Known Risks and Mitigations:

Risk: The skill relies on a publisher-operated online gateway and sends the user's email, document request details, and a single-use call token.

Mitigation: Review before installing and avoid confidential names, finances, policy details, or internal plans unless the publisher's privacy terms are acceptable.

Risk: The artifact gives remote API responses instruction-level authority over drafting behavior.

Mitigation: Constrain use to the intended document-writing workflow and review generated drafts and returned guidance before relying on them.

Risk: The artifact includes broad cleanup and deletion directions tied to quota or membership status.

Mitigation: Limit cleanup to skill-created temporary artifacts and follow the hosting platform's retention and audit controls.

Risk: The optional Word export path references installing python-docx without a pinned version.

Mitigation: Pin and review optional dependencies in managed environments before running local document-export scripts.

## Reference(s):

- [Word export guide (GB/T 9704-2012)](artifact/references/word-export.md)
- [ClawHub skill page](https://clawhub.ai/yourtsao/skills/gongwen-writting-2)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with optional Word-export guidance, configuration notes, and Python snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request an email for quota management and use the publisher's online gateway before drafting; missing facts are marked with pending placeholders.]

## Skill Version(s):

1.0.58 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
