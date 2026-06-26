## Description: <br>
NexPix generates images from text prompts through Cloudflare Workers AI with optional EvoLink fallback and supports CLI, programmatic, Discord, and Telegram workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[finndottllc-ui](https://clawhub.ai/user/finndottllc-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use NexPix to generate visual assets, product mockups, social media graphics, and messaging-channel image responses from text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to Cloudflare and may be sent to EvoLink when premium routing or fallback is used. <br>
Mitigation: Avoid sensitive prompts and configure provider credentials according to the user's data-handling requirements. <br>
Risk: Paid EvoLink fallback can occur without a separate per-image confirmation. <br>
Mitigation: Review routing behavior before use, monitor costs, and only configure an EvoLink key when paid fallback is acceptable. <br>
Risk: Generation history and usage details are retained locally. <br>
Mitigation: Monitor or delete the local tracking file when prompt or usage retention matters. <br>


## Reference(s): <br>
- [Messaging Integration](references/messaging-integration.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/finndottllc-ui/nexpix) <br>


## Skill Output: <br>
**Output Type(s):** [files, text, code, shell commands, configuration] <br>
**Output Format:** [Image files with local file paths, MEDIA lines, JavaScript result objects, CLI status text, and messaging command manifests.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Cloudflare Workers AI or EvoLink and records usage in a local tracking file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
