## Description: <br>
AI image generation and editing for agents across text-to-image and image-to-image workflows, video generation, audio generation, and image-to-3D asset creation through one zero-setup hosted runtime. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgwilson](https://clawhub.ai/user/danielgwilson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Image Skill to generate or edit images, video, audio, and 3D assets through a hosted CLI/API that returns durable media URLs, recoverable job records, cost receipts, and structured JSON envelopes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live media creation and credit top-ups can spend real money through prepaid credits, x402, or Stripe flows. <br>
Mitigation: Use guide or dry-run flows first, inspect payment guidance, cap spend with budget flags, and run live create or payment commands only when spend is authorized. <br>
Risk: The hosted service stores and uses a restricted Image Skill token, and uploads, feedback, prompts, and generated media are sent to the hosted service. <br>
Mitigation: Treat IMAGE_SKILL_TOKEN as a credential, prefer stdin or saved config handoff over exposing raw tokens, and avoid sending secrets or sensitive payment credentials to the service. <br>
Risk: Retrying a failed paid create can duplicate provider work or debits if prior job state is not checked. <br>
Mitigation: Use returned job, asset, and trace IDs with jobs/activity recovery commands before retrying, and follow error recovery guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/danielgwilson/image-skill) <br>
- [Image Skill Homepage](https://image-skill.com) <br>
- [Canonical Skill Contract](https://image-skill.com/skill.md) <br>
- [LLM Contract](https://image-skill.com/llms.txt) <br>
- [CLI Documentation](https://image-skill.com/cli.md) <br>
- [Hosted API](https://api.image-skill.com) <br>
- [Local CLI Reference](references/cli.md) <br>
- [Local Command Manifest](references/commands.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce hosted media-generation commands that return durable media URLs, job IDs, asset IDs, trace IDs, and cost receipts.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
