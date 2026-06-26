## Description: <br>
Generates a playful MBTI-style personality report from recent user interaction patterns with the Claw agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyang0807](https://clawhub.ai/user/xiaoyang0807) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ClawHub users invoke this skill to receive a light MBTI-style personality report based on recent natural-language conversations with their agent. The output is intended for personal entertainment and sharing, not clinical or employment assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses recent conversations and memory to infer personality traits without a clear opt-in in the artifact. <br>
Mitigation: Use it only with informed user consent and make clear that the result is an entertainment-oriented personality report. <br>
Risk: Generated reports are formatted for sharing and may reveal inferred traits or interaction patterns. <br>
Mitigation: Review and redact generated reports before sharing them outside the conversation. <br>
Risk: The artifact includes a GitHub pull or clone installation command for a third-party repository. <br>
Mitigation: Prefer the ClawHub install path unless the GitHub repository has been reviewed and is trusted. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/xiaoyang0807/myagent-mbti) <br>
- [Publisher profile](https://clawhub.ai/user/xiaoyang0807) <br>
- [Project homepage](https://github.com/xiaoyang0807/claw-mbti) <br>
- [Artifact README](artifact/README.md) <br>
- [Diagnostic reference manual](artifact/reference.md) <br>
- [Personality type catalog](artifact/types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown personality report with optional inline shell commands for installation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a diagnostic evidence table, sharing prompt, and installation or update guidance.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence; artifact frontmatter states 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
