## Description: <br>
Audit GitHub Actions workflows that use self-hosted runners for untrusted trigger and credential-hardening risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daniellummis](https://clawhub.ai/user/daniellummis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and security engineers use this skill to review GitHub Actions workflows that run on self-hosted runners and identify risky trigger, permission, runner-label, and checkout-credential patterns before enabling or enforcing CI gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary notes missing explicit permission metadata. <br>
Mitigation: Review the skill text before running it and confirm the expected local access and required binaries, bash and python3. <br>
Risk: Pattern-based workflow auditing can produce findings that require human judgment. <br>
Mitigation: Review flagged workflow lines and severity scores before changing CI policy or enabling fail gates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daniellummis/github-actions-self-hosted-risk-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Text report or JSON summary with flagged workflows, severity scores, issue codes, and line references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can exit with status 1 when FAIL_ON_CRITICAL=1 and critical workflows are found.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
