## Description: <br>
Find trending topics, create editorial-style social media graphics, and post to X/Twitter and Instagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ashmonmc](https://clawhub.ai/user/ashmonmc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media creators and operators use this skill to research viral topics, generate editorial carousel graphics, and prepare or publish content to Instagram and X/Twitter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish content to real social media accounts. <br>
Mitigation: Review every caption and media file before posting, and use a dedicated or low-risk account where possible. <br>
Risk: The skill handles social account credentials, API keys, and an Instagram session file. <br>
Mitigation: Prefer environment variables or a secret manager over command-line passwords, and remove ~/.openclaw/ig_session.json when the Instagram session is no longer needed. <br>
Risk: Untrusted prompts or queries could lead to misleading content or unintended posting behavior. <br>
Mitigation: Avoid running the workflow on untrusted prompts or queries, and keep human review in the publishing loop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ashmonmc/insta-content-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke OpenAI image generation, Brave Search, the bird CLI, and Instagram posting tools when configured with the required credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
