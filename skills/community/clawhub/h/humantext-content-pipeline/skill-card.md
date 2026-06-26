## Description: <br>
Detects AI-generated content and humanizes text to sound natural using the humantext.pro API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fyt84](https://clawhub.ai/user/fyt84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content teams use this skill to draft or revise text, check an AI-detection score, and optionally produce a more natural-sounding version with humantext.pro. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user writing to the third-party humantext.pro service. <br>
Mitigation: Use it only with text the user is comfortable sharing with humantext.pro, and avoid confidential, regulated, hiring, compliance, or similar sensitive content. <br>
Risk: The workflow can be used to conceal AI assistance or authorship where disclosure is expected. <br>
Mitigation: Do not use it in academic, platform, compliance, or other contexts where bypassing authorship or AI-use rules would violate policy or expectations. <br>
Risk: The MCP configuration requires a humantext.pro API key. <br>
Mitigation: Store HUMANTEXT_API_KEY only in the local MCP configuration or secret store and do not paste it into prompts, logs, or shared files. <br>
Risk: Humanization consumes paid word credits. <br>
Mitigation: Check balance before long or batch jobs and warn the user before processing credit-heavy text. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fyt84/humantext-content-pipeline) <br>
- [humantext.pro homepage](https://humantext.pro) <br>
- [humantext.pro API dashboard](https://humantext.pro/api) <br>
- [humantext.pro API docs](https://humantext.pro/api/docs) <br>
- [@humantext/mcp-server npm package](https://www.npmjs.com/package/@humantext/mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated or revised text, score summaries, and MCP setup snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HUMANTEXT_API_KEY, npx, an active humantext.pro account, and word credits for humanization.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
