## Description:

判断某个字符串是否是数字和指定特定字符组成

This skill is ready for commercial/non-commercial use.

## Publisher:

[wahahasssss](https://clawhub.ai/user/wahahasssss)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to check whether user-provided text is composed only of integer-number segments separated by a specified special character.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper echoes the full command argument list before reporting validation results, which may expose user-provided input in logs or transcripts.

Mitigation: Avoid using sensitive input with this skill unless argument echoing is acceptable in the deployment context.

Risk: The artifact documentation is in Chinese and the printed output may be confusing because non-numeric segments are emitted as a comma-separated list after the echoed arguments.

Mitigation: Confirm downstream agents interpret an empty result line as success and non-empty listed segments as validation failures.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wahahasssss/skills/numbers-judge)
- [Publisher profile](https://clawhub.ai/user/wahahasssss)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper prints the full argument list and then a comma-separated list of segments that are not valid integers; an empty final line indicates all checked segments parsed as integers.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
