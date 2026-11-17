## Description:

Neta capability index and routing skill - help choose the appropriate Neta-related skill (neta-space / neta-creative / neta-community / neta-suggest).

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxiuhan](https://clawhub.ai/user/huxiuhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Neta to classify Neta-related requests, choose the appropriate focused sub-skill, and migrate older workflows away from the legacy monolithic Neta skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned remote `npx skills add` commands can install code that changes local agent behavior.

Mitigation: Verify trust in the `skills` npm package and the `talesofai/neta-skills` repository before installation, prefer pinned versions or commit hashes, and review each sub-skill before use.

## Reference(s):

- [Neta skill page on ClawHub](https://clawhub.ai/huxiuhan/skills/neta)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes the user to focused Neta sub-skills and may suggest optional installation commands.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
