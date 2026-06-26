## Description: <br>
Use MSX when a user asks to scout market opportunities, decide what to build, identify a market gap, find recent demand signals, or run MSX market intelligence through an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tornikeo](https://clawhub.ai/user/tornikeo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use MSX to scout market opportunities, identify market gaps, gather recent demand signals, and request market intelligence through the MSX API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends market research prompts, product descriptions, and related business context to the third-party MSX service. <br>
Mitigation: Avoid submitting sensitive business information unless the user is comfortable sharing it with MSX. <br>
Risk: The skill requires storing and using an MSX API key. <br>
Mitigation: Store the API key securely, keep device codes private, and avoid exposing credentials in conversation or logs. <br>
Risk: The skill can initiate a Stripe checkout flow for paid MSX usage. <br>
Mitigation: Create checkout only after the API indicates a subscription is required and the user explicitly agrees. <br>
Risk: The installed artifact defers to a mutable hosted MSX skill file. <br>
Mitigation: Re-check the hosted MSX instructions before sensitive use. <br>


## Reference(s): <br>
- [MSX homepage](https://msx.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and cited market opportunity summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an MSX API key, device authentication, and a paid MSX subscription for continued use.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
