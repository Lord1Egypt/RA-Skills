## Description:

OpenSpender lets agents use a user-funded allowance to discover, price, and call paid web search, model, media-generation, and x402/MPP catalog APIs while respecting the user's budget caps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openspender](https://clawhub.ai/user/openspender)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent pay per request for cataloged APIs when no existing key, subscription, or free path is available, with price checks, budget caps, and spend reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can spend from a user-funded allowance for paid API calls.

Mitigation: Use budget caps, inspect prices before paid calls, and report spend or policy denials clearly.

Risk: Setup may modify local agent harness configuration.

Mitigation: Review the setup path before running it and pin or review installer versions.

Risk: The skill includes behavior for uploading local files to public storage.

Mitigation: Require explicit user approval before uploading any local file to a public URL.

Risk: Automatic remote skill refreshes can change behavior after installation.

Mitigation: Avoid automatic refreshes unless the updated skill content has been reviewed.

## Reference(s):

- [OpenSpender Skill Page](https://clawhub.ai/openspender/skills/openspender)
- [OpenSpender Homepage](https://openspender.com)
- [OpenSpender Protocol Reference](https://openspender.com/llms.txt)
- [OpenSpender Canonical Skill](https://openspender.com/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown with inline shell commands and API call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid calls should report price, policy denials, and total task spend when applicable.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and changelog body reference 1.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
