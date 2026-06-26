## Description: <br>
Generates structured comic script JSON from a one-line theme, including characters, scenes, dialogue, camera direction, and mood for Chinese-style comic drama workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and story-production agents use this skill to turn a short theme into a validated script.json for Chinese-style comic or drama storyboarding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled paid media API helpers can call external services, upload local media, and incur costs beyond the advertised script-generation flow. <br>
Mitigation: Run the skill in a controlled project folder and provide ARK_API_KEY only when deliberately using those helper paths. <br>
Risk: Fallback script generation requires ANTHROPIC_API_KEY and sends the prompt to an external model provider. <br>
Mitigation: Use direct agent-authored JSON when possible, provide ANTHROPIC_API_KEY only for intended fallback generation, and review generated script.json before downstream use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-comic-script) <br>
- [Volcengine Seedance documentation](https://www.volcengine.com/docs/82379/1520757) <br>
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/97465) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON files] <br>
**Output Format:** [JSON script data and Markdown usage guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or validates script.json; fallback generation requires ANTHROPIC_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
