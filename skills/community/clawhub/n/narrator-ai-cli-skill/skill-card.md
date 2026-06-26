## Description: <br>
AI解说大师 Narrator AI Skill helps agents use narrator-ai-cli to create AI movie and drama narration videos, manage narration tasks, browse media resources, and automate video production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4myhime](https://clawhub.ai/user/4myhime) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agent operators use this skill to guide an AI agent through Narrator AI video narration workflows, including material selection, script generation, dubbing, BGM selection, task polling, and final video retrieval. It is intended for users who have a Narrator AI API key and explicitly approve cloud processing of selected media inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected media, subtitles, prompts, and task metadata are sent to the Narrator AI cloud API for processing. <br>
Mitigation: Use the skill only for intended Narrator AI workflows, get user approval for selected inputs, and avoid uploading sensitive or unauthorized media. <br>
Risk: The NARRATOR_APP_KEY grants access to the user's Narrator AI account and may be stored in local CLI configuration. <br>
Mitigation: Keep the key private, do not commit local config files, and prefer environment variables or locked-down local configuration where appropriate. <br>
Risk: Task creation, batch work, uploads, and video synthesis can consume paid account balance. <br>
Mitigation: Check balance and budget estimates before task creation, verify materials first, and require explicit confirmation before batch or expensive work. <br>
Risk: File deletion and account-key management actions can be disruptive. <br>
Mitigation: Require a separate user confirmation before deletion or account-key changes, and verify target identifiers before running the CLI command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/4myhime/narrator-ai-cli-skill) <br>
- [Narrator AI CLI repository](https://github.com/GridLtd-ProductDev/narrator-ai-cli) <br>
- [Narrator AI API endpoint](https://openapi.jieshuo.cn) <br>
- [Narrator AI resource preview](https://ceex7z9m67.feishu.cn/wiki/WLPnwBysairenFkZDbicZOfKnbc) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown guidance with shell commands, JSON request examples, configuration steps, and task result handling notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide agents to call narrator-ai-cli, parse JSON responses, poll asynchronous tasks, and return generated video URLs or file identifiers.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence, plugin.json, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
