## Description:

Leadership Coach provides a Chinese-language local CLI with leadership and team management guidance across leadership laws, productivity practices, employee retention, execution-system design, and anti-abusive-leadership topics.

This skill is for research and development only.

## Publisher:

[1126053051-lgtm](https://clawhub.ai/user/1126053051-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Managers, team leads, and individual contributors use this skill to retrieve structured Chinese-language guidance for leadership growth, team execution, employee retention, productivity, and healthier management practices. The CLI can list solution libraries, show detailed frameworks, match a user problem to a relevant solution, plan toward a management goal, or run a leadership-related diagnostic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious because it disables sandbox isolation for a local CLI.

Mitigation: Install only after reviewing the files, run it in a controlled local environment, or require the publisher to enable sandboxing before deployment.

Risk: The release declares an unused unpinned PyYAML dependency.

Mitigation: Remove the dependency if it remains unused, or pin and review it before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1126053051-lgtm/skills/leadership-coach)
- [Publisher Profile](https://clawhub.ai/user/1126053051-lgtm)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text CLI output and Markdown usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output from a local Python command-line tool]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
