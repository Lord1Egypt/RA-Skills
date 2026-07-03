## Description: <br>
Complete guide to local AI image generation with Ollama - no API keys, 100% private. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amrree](https://clawhub.ai/user/amrree) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and local-AI users use this skill to set up local image generation with Ollama, choose models, craft prompts, and run common image-generation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included flux-gen helper script can remove PNG files from the user's home folder without warning. <br>
Mitigation: Review or remove scripts/flux-gen before use, delete the command that removes $HOME/*.png, and restrict image cleanup and discovery to a dedicated tool-owned output directory. <br>
Risk: The documentation includes a curl-to-shell installation path for Ollama. <br>
Mitigation: Prefer a package manager or inspect the installer before running it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/amrree/skills/image-gen-guide) <br>
- [README](README.md) <br>
- [Full Technical Guide](guide/full-guide.md) <br>
- [Prompt Examples Gallery](examples/prompts.md) <br>
- [Ollama Image Generation](https://ollama.com/blog/image-generation) <br>
- [FLUX.1 Documentation](https://blackforestlabs.ai/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local setup steps, model recommendations, prompt examples, troubleshooting guidance, and helper-script usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
