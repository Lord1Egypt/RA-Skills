## Description: <br>
Guides agents through calculating and interpreting viral coefficient, K-factor, invite conversion, cycle time, and stability across growth waves. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, founders, investors, product managers, and growth teams use this skill to test claims of virality by calculating K = i x c, separating invite and conversion levers, and checking whether viral growth remains stable across waves. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce misleading growth conclusions if users calculate K on signups rather than activated users or omit cohort and time-window definitions. <br>
Mitigation: Require activated-user definitions, invite events, conversion events, cohort windows, cycle time, and wave-by-wave K checks in the analysis. <br>
Risk: Invitation mechanics can create consent, platform, or deliverability risk when they rely on aggressive address-book imports or non-consensual sharing. <br>
Mitigation: Keep recommendations consent-based and review any proposed invite mechanic for platform policy and user-consent requirements before launch. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deciqai/skills/k-factor-viral) <br>
- [Sources - k-factor-viral](references/sources.md) <br>
- [Hotmail, 1996-1998](examples/hotmail-1996-1998.md) <br>
- [DFJ](https://www.dfj.com/) <br>
- [Viral Marketing - The Science Of Sharing](https://www.forentrepreneurs.com/lessons-learnt-viral-marketing/) <br>
- [Andrew Chen](https://andrewchen.com/) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis, Markdown] <br>
**Output Format:** [Markdown analysis template with structured fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use stepwise coaching prompts that stop for user input before continuing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
