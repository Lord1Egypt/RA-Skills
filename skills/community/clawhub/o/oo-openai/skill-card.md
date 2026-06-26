## Description: <br>
OpenAI (openai.com). Use this skill for ANY OpenAI request — reading, creating, and updating data. Whenever a task involves OpenAI, use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate an OOMOL-connected OpenAI account through the oo CLI for model lookup, Responses API calls, batches, embeddings, image generation, moderation, transcription, translation, and speech synthesis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a user's OOMOL-connected OpenAI account and run write actions that create or modify OpenAI resources. <br>
Mitigation: Review exact payloads before approving write actions, avoid sending sensitive data unless intended, and reserve first-time setup steps for actual authentication or connection failures. <br>
Risk: The first-time setup path installs the oo CLI through a remote installer when the CLI is missing. <br>
Mitigation: Inspect the oo CLI installer before using that setup path. <br>


## Reference(s): <br>
- [ClawHub OpenAI skill page](https://clawhub.ai/oomol/oo-openai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OpenAI API](https://openai.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Configuration guidance] <br>
**Output Format:** [Markdown guidance with oo CLI commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before execution and returns connector data with execution metadata when actions run.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
