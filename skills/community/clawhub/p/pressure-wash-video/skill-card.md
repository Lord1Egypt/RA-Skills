## Description: <br>
Generate vertical satisfying pressure-wash shorts with WeryAI from text prompts or dirty-surface images, emphasizing rinse motion and a moving clean/dirty line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and agent operators use this skill to turn cleaning briefs or dirty-surface reference images into short vertical pressure-washing video generations through WeryAI. It helps assemble valid prompts and parameters, confirm them with the user, run the Node.js CLI, and return playable video URLs or actionable API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a WERYAI_API_KEY and sends generation requests to WeryAI services. <br>
Mitigation: Install only from a trusted publisher, keep the API key out of source control, and run generation in a controlled environment. <br>
Risk: Using a local image path can cause the script to read that file and upload it to WeryAI. <br>
Mitigation: Prefer public HTTPS image URLs; use local files only after explicit user consent and review of the selected file. <br>
Risk: Successful generation runs can consume WeryAI credits. <br>
Mitigation: Confirm the expanded prompt and parameters before running the CLI, and avoid repeated runs unless the user approves the cost. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/pressure-wash-video) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md) <br>
- [WeryAI video API host](https://api.weryai.com) <br>
- [WeryAI models and upload API host](https://api-growth-agent.weryai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON command payloads and returned video URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, network access, and WeryAI credits for successful generation runs.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
