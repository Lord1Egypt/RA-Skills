## Description:

Helps agents manage IMA knowledge bases and notes, upload and export content, and package local videos as single-file HTML for import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwqww1](https://clawhub.ai/user/wwqww1)

### License/Terms of Use:

MIT-0

## Use Case:

IMA users and developers use this skill to organize knowledge bases and notes, import files and webpages, export content, and prepare videos for import. It requires IMA API credentials and Node.js; video conversion also requires Python.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to expose API keys in chat.

Mitigation: Obtain keys through the official flow, supply them through a secret manager or environment variables, and rotate any exposed keys.

Risk: Exports and account-changing operations can proceed without script-level confirmation and may be irreversible.

Mitigation: Review or dry-run exports, permission and tag changes, knowledge-base joins, and note appends before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wwqww1/skills/ima-plus-skill)
- [IMA API credential application](https://ima.qq.com/agent-interface)
- [Knowledge base API reference](artifact/knowledge-base/references/api.md)
- [Notes API reference](artifact/notes/references/api.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown guidance and commands; JSON responses, exported ZIP archives, and video HTML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [IMA operations require IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY; video conversion requires Python.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
