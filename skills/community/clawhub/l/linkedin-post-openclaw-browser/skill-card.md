## Description: <br>
Draft, prepare, and publish LinkedIn feed posts through OpenClaw browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yonghyeokrhee](https://clawhub.ai/user/yonghyeokrhee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to standardize a prepare-then-publish workflow for LinkedIn feed posts. It helps an agent finalize post copy, open the LinkedIn share composer, fill approved content, preview link unfurls, and publish only after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can publish a public LinkedIn feed post from an already logged-in browser profile. <br>
Mitigation: Use prepare-only mode first, confirm the exact post text, link preview, selected account, and timing, and run --publish only after explicit approval. <br>
Risk: The workflow controls a browser session that may already have access to a LinkedIn account. <br>
Mitigation: Use the intended browser profile, keep gateway tokens scoped to the OpenClaw environment, and verify the active account before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yonghyeokrhee/linkedin-post-openclaw-browser) <br>
- [LinkedIn feed share composer](https://www.linkedin.com/feed/?shareActive=true) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown instructions with bash examples and JSON helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw CLI, browser automation, a LinkedIn-authenticated browser profile, and a gateway token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
