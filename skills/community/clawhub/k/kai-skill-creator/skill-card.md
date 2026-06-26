## Description: <br>
Create new OpenClaw skills that pass ClawHub validation on first attempt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill authors use this skill to create, validate, enable, and publish OpenClaw skills with the expected metadata, script structure, and pre-publish checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that the skill teaches users to omit external API URLs from documentation to avoid scanner flags. <br>
Mitigation: Document external services and data flows honestly, and treat scanner findings as prompts to clarify behavior rather than hide risk-relevant links. <br>
Risk: The helper script copies an existing local template and writes a new skill, which can carry unrelated code or placeholder content into a release. <br>
Mitigation: Review all copied files, remove unrelated code and TODOs, run syntax checks, and rescan the generated skill before enabling or publishing it. <br>
Risk: The workflow guides persistent skill installation, configuration, and publishing. <br>
Mitigation: Confirm required binaries, environment variables, permissions, and generated files before copying to the global skills directory or publishing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ogdegenblaze/kai-skill-creator) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/ogdegenblaze) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes an optional shell helper that creates a new skill directory from a local template.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
