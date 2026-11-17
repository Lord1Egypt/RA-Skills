## Description:

Generates original instrumental or vocal music from prompts and style parameters, with requested durations from 5 seconds to 10 minutes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, developers, and teams use this skill to ask an agent for original music drafts, soundtrack cues, podcast intros, loops, or vocal song concepts. Users should avoid copyrighted source material and review generated audio before commercial release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad shell execution and file write access for a loosely specified media workflow.

Mitigation: Run it only in a constrained workspace, allow known media tools explicitly, and require user confirmation before command execution or file mutation.

Risk: Generated music or user-provided prompts may raise copyright or licensing concerns.

Mitigation: Use original prompts, avoid copyrighted source material, and review rights and attribution requirements before public or commercial use.

Risk: API keys or credentials may be needed in some agent environments.

Mitigation: Store credentials in environment variables, keep them out of prompts and source files, and avoid running the skill in sensitive directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/music-gen-cellcog-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with prompts, configuration notes, and optional JSON-style result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated music prompts, status descriptions, command guidance, and file-writing instructions depending on the agent environment.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
