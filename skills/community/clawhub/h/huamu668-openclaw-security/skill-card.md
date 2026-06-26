## Description: <br>
Provides OpenClaw security guidance for root-enabled agents, including pre-install audits, permission tightening, hash baselines, high-risk operation controls, nightly checks, and Git-based backup practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huamu668](https://clawhub.ai/user/huamu668) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and security reviewers use this skill to assess and harden OpenClaw environments where agents may have root access or handle sensitive operations. It helps structure security audits, command guardrails, runtime file protections, nightly review, and backup practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide recommends persistent automation that can scan sensitive OpenClaw areas and push credentials, identity data, and state to a remote Git repository. <br>
Mitigation: Review the guide manually before use, approve privileged commands one by one, avoid committing credentials or identity files unless encrypted and intentional, and ensure any nightly cron job or reporting channel can be reviewed, disabled, and cleaned up. <br>
Risk: Following proposed command guardrails or backup steps automatically could introduce incorrect security guidance or expose sensitive local state. <br>
Mitigation: Treat the skill as advisory documentation, verify upstream sources, inspect generated scripts or cron entries before deployment, and keep human approval in the loop for high-risk operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huamu668/huamu668-openclaw-security) <br>
- [OpenClaw security practice guide referenced by skill](https://github.com/slowmist/openclaw-security-practice-guide) <br>
- [SlowMist](https://www.slowmist.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational security rules, audit steps, permission commands, hash-baseline practices, cron review guidance, and backup recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
