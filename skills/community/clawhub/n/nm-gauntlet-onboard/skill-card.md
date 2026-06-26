## Description: <br>
Guides a new developer through five staged challenge sets covering architecture, domain, patterns, and hardening. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to guide new contributors through staged codebase onboarding challenges and track readiness across architecture, domain, interfaces, patterns, and hardening topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is expected to examine a repository and track onboarding progress, which may expose codebase context during guided review. <br>
Mitigation: Install and use it only in codebases where agent-guided repository review and progress tracking are acceptable. <br>
Risk: Onboarding challenge feedback or progress summaries may be incomplete or misleading if the agent misunderstands the codebase. <br>
Mitigation: Review generated guidance and progress assessments before relying on them for contributor readiness decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-gauntlet-onboard) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/gauntlet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with staged challenge prompts and progress summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tracks onboarding stage, hints, mastery, advancement, and graduation status when used by an agent.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
