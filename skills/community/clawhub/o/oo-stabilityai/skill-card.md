## Description: <br>
Operate Stability AI through OOMOL's oo CLI connector for supported actions such as text-to-audio generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to operate Stability AI through an OOMOL-connected account, inspect live connector schemas, and run supported Stability AI actions through the oo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented text_to_audio action can generate audio and upload a file even though the skill summary emphasizes searching and reading data. <br>
Mitigation: Treat generation as a write and cost-incurring action; require explicit user confirmation of the prompt, target action, and expected effect before running it. <br>
Risk: The skill depends on a connected OOMOL account and Stability AI credentials injected server-side. <br>
Mitigation: Use it only with an intended connected account and do not expose, request, or store raw API tokens in prompts, logs, or payload files. <br>
Risk: Generated files are uploaded to connector transit storage. <br>
Mitigation: Review where generated files are stored or shared before treating outputs as private or reusable artifacts. <br>


## Reference(s): <br>
- [Stability AI homepage](https://stability.ai) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-stabilityai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference connector JSON responses and generated audio files stored in connector transit storage.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
