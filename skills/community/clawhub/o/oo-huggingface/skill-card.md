## Description: <br>
Provides agent access to Hugging Face search, repository metadata, dataset previews, user information, inference endpoints, chat completions, and embeddings through an OOMOL-connected oo CLI workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search and inspect Hugging Face models, datasets, Spaces, files, endpoints, and account metadata. It also supports generation and embedding workflows when the user intends to call Hugging Face inference services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generation and embedding actions can send prompts or input text to external Hugging Face inference services and may affect account usage or billing. <br>
Mitigation: Confirm the prompt or input text, target model or provider, and possible account or billing impact before running generation or embedding actions. <br>
Risk: The security summary reports that the skill under-discloses generation actions and treats untagged actions as safe reads even though some can send data to inference services. <br>
Mitigation: Treat generation and embedding actions as external inference operations, not simple reads, and review payloads before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-huggingface) <br>
- [Hugging Face homepage](https://huggingface.co) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON connector results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live connector schemas before constructing action payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
