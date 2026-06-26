## Description: <br>
Inspect PhantomBuster agents, automations, launches, and workflow data via the PhantomBuster API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect PhantomBuster agents, automations, launches, and output data, then manage or trigger workflows through ClawLink-mediated PhantomBuster API tools after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires brokered access to a PhantomBuster account through ClawLink. <br>
Mitigation: Install only when the user trusts ClawLink to handle PhantomBuster account access and verify the connected integration before using tools. <br>
Risk: Launching, updating, creating, or deleting automations can affect real PhantomBuster workflows and third-party rate limits. <br>
Mitigation: Use the required preview and explicit confirmation flow before any action that changes or triggers automations. <br>
Risk: PhantomBuster launch output may contain account or workflow data from the connected account. <br>
Mitigation: Limit requests to the needed agents, launches, and output fields, and avoid exposing returned data beyond the user's intended task. <br>


## Reference(s): <br>
- [PhantomBuster API Documentation](https://hub.phantombuster.com/reference) <br>
- [PhantomBuster](https://phantombuster.com/) <br>
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=phantombuster-automation) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/phantombuster-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PhantomBuster account data, automation run details, and launch output returned through ClawLink tools.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
