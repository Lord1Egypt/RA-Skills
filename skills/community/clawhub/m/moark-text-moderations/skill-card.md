## Description: <br>
Perform text review on user-specified input text that may be inappropriate or offensive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fchange](https://clawhub.ai/user/fchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit text for moderation with the Gitee AI moark-text-moderation model, then receive the moderation result and a brief markdown summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Moderated text is sent to the external Gitee AI service. <br>
Mitigation: Avoid submitting secrets or regulated data unless Gitee AI's terms and data handling fit the intended use. <br>
Risk: Passing the API key on the command line can expose it through shell history or process listings. <br>
Mitigation: Prefer setting GITEEAI_API_KEY in the environment instead of using the --api-key argument. <br>
Risk: The skill depends on the Python openai package at runtime. <br>
Mitigation: Install dependencies in a trusted environment before running the bundled script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fchange/moark-text-moderations) <br>
- [Gitee AI API endpoint](https://ai.gitee.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with moderation result text or JSON extracted from command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITEEAI_API_KEY and sends submitted text to Gitee AI for moderation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
