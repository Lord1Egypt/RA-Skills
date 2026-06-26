## Description: <br>
NovelCraft is a fully autonomous book-authoring skill that creates complete novels from idea through Markdown, PDF, and EPUB publication using modular concept, chapter, review, optional image, and publication workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kesuek](https://clawhub.ai/user/kesuek) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External authors and developers use NovelCraft to generate fiction projects with structured concept development, sequential chapter drafting, automated review, optional image planning, and publication-ready outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run and terminate subagents and modify project files during autonomous writing and publication workflows. <br>
Mitigation: Install it in a dedicated workspace, begin in step-by-step mode, and confirm backups before allowing reset/delete, overwrite, or final-promotion actions. <br>
Risk: Optional image generation can send book-derived prompts to a configured image provider, including a hard-coded HTTP endpoint noted by the security evidence. <br>
Mitigation: Keep images disabled until the provider is reviewed, replace the endpoint with a scoped configuration, and avoid sending sensitive content to external providers. <br>
Risk: Hard-coded local paths may not match the installer's environment and can cause writes to unintended or unavailable locations. <br>
Mitigation: Replace hard-coded /home/felix paths with workspace-specific paths before running the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kesuek/novelcraft) <br>
- [Security Considerations](SECURITY.md) <br>
- [Configuration Reference](references/CONFIG.md) <br>
- [Configuration Setup Guide](references/config-setup.md) <br>
- [Getting Started Guide](GETTING-STARTED.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with configuration snippets and generated novel project files, including Markdown chapters and optional PDF/EPUB outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create and update local project files; optional image generation can send prompts to a configured provider.] <br>

## Skill Version(s): <br>
3.2.3 (source: ClawHub release evidence; artifact manifests and changelog list 3.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
