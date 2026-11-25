## Description:

iHatePosting schedules social media and chat posts across 15 channels and lets agents discover channel rules, upload media, create or manage posts, and review analytics from the command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayankkasavala](https://clawhub.ai/user/mayankkasavala)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and social media operators use the CLI to discover connected channels and their rules, upload media, create or manage scheduled posts, and review analytics across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence notes that the scanner found a possible post deletion capability; confidence is medium and the scan was partial because some local references could not be resolved.

Mitigation: Review unresolved references and confirm the target and scope before deletion. The skill documentation says post deletion removes the full thread.

## Reference(s):

- [iHatePosting ClawHub release](https://clawhub.ai/mayankkasavala/skills/ihateposting)
- [iHatePosting agent documentation](https://ihateposting.com/ai-agents)
- [iHatePosting npm package](https://www.npmjs.com/package/ihateposting)
- [iHatePosting Agent repository reference](https://github.com/iHatePostingOrg/iHatePosting-Agent)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and settings vary by connected platform; responses may include post status, media references, and analytics.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
