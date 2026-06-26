## Description: <br>
Enforce release discipline for AI agents and developers. Prevents version spam, forces quality checks before publishing, and maintains a 24-hour cooldown between releases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill before publishing, releasing, deploying, or bumping versions to apply a release-readiness checklist with cooldown, documentation, feedback, quality, kill-criteria, and principle-consistency gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may slow or block publishing when its release-readiness gates fail. <br>
Mitigation: Install it only where release discipline is desired, and treat block or warning decisions as review prompts before publishing. <br>
Risk: Release logs could capture sensitive internal notes if users include them in release summaries. <br>
Mitigation: Review the release log periodically and avoid storing secrets, private customer details, or sensitive internal notes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mupengi-bot/mupeng-release-discipline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown checklist results and release-log entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May block or warn on release actions when checklist gates fail.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
