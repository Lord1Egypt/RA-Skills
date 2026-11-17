## Description:

Helps an agent analyze untrusted scripts or code before execution to detect malicious, suspicious, or unintended behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoyuwang99](https://clawhub.ai/user/haoyuwang99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Safe Exec to have an agent inspect untrusted scripts, external files, or third-party skill code before deciding whether to execute them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may make an agent more conservative with unfamiliar or ambiguous code, causing false positives or blocked execution.

Mitigation: Treat the verdict as an advisory review aid and ask for user confirmation or deeper review before blocking legitimate ambiguous scripts.

Risk: Intent analysis can miss novel or indirect malicious behavior despite a clean release scan.

Mitigation: Use this skill alongside normal controls such as sandboxing, least privilege, and scanner results before running untrusted code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haoyuwang99/skills/haoyuwang99-safe-exec)
- [ClawHub publisher profile](https://clawhub.ai/user/haoyuwang99)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style intent analysis with a verdict, summary, findings, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; the skill provides advisory review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
