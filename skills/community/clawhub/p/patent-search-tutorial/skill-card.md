## Description:

A hands-on patent search tutorial using your own topic, explaining keywords, quotes, AND/OR, applicant and IPC search step by step with live results, ending with a one-page search note.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Teach new patent searchers to build and refine searches using keywords, exact phrases, Boolean operators, applicant and IPC fields, then capture the lessons in a concise search note.

### Deployment Geography for Use:

The tutorial uses Chinese patent examples; the documentation describes PatentMax coverage in China, the United States, Europe, Japan, South Korea, and WIPO.

## Known Risks and Mitigations:

Risk: The client may expose API keys through redirects or allow crafted patent numbers to access files outside its cache.

Mitigation: Prefer waiting for fixes that restrict credential destinations and contain cache paths; if evaluating this release, use an isolated environment and public example topics.

Risk: Queries are sent to PatentMax, usage can incur charges, and the credential workflow may retain a key for future sessions.

Mitigation: Use trial access rather than a paid key while evaluating this release, and set an explicit spending limit before paid use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ip930/skills/patent-search-tutorial)
- [PatentMax search interface](https://app.ip930.com/)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Step-by-step lessons with live patent search results and a one-page Markdown search note.]

**Output Parameters:** [A patent topic and the learner's experience level; if no topic is supplied, the tutorial uses a documented example topic.]

**Other Properties Related to Output:** [The tutorial focuses on PatentMax search syntax and uses Chinese patents in its examples.]

## Skill Version(s):

1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
