## Description: <br>
Stores and retrieves successful image generation prompts by category, style, and keywords for quick reuse and recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acilgit](https://clawhub.ai/user/acilgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Image creators and agent users use this skill to preserve successful image generation prompts, search them by category, style, or keywords, and reuse prompt patterns in later image workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved prompt text and feedback may include sensitive, customer, or confidential details if users place them in image prompts. <br>
Mitigation: Avoid putting secrets or confidential data in prompts, and review or delete the local prompt_library.json file when prompt history should not be retained. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/acilgit/image-prompt-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Markdown guidance and structured JSON prompt-library entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local prompt_library.json file containing prompt text, style metadata, and user feedback.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
