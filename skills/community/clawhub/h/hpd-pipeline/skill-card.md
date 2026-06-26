## Description: <br>
Use when the HPD lab needs a repeatable Planner -> Designer -> conditional Developer -> Tester flow for an approved idea, with Lobster-first and sequential fallback behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[omermesebuken1](https://clawhub.ai/user/omermesebuken1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HPD lab users and project builders use this skill to turn an approved idea into a structured Turkish-language project package with planning, design, conditional development, testing, and handoff sections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to use an unspecified Gemini API fallback for image generation, which may run unclear code or send project details outside the workspace. <br>
Mitigation: Review the fallback script, account or API key, and data sharing behavior before allowing the agent to run it. <br>
Risk: The release security verdict is suspicious. <br>
Mitigation: Review before installing and only deploy after confirming the image-generation path and any external service usage. <br>


## Reference(s): <br>
- [HPD Pipeline project contract](references/project-pipeline.md) <br>
- [ClawHub skill page](https://clawhub.ai/omermesebuken1/hpd-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Notion-first Markdown sections in Turkish, with artifact paths and code snippets when produced.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include mandatory HPD sections; render images, CAD, source code, and firmware paths are only reported when actually produced.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
