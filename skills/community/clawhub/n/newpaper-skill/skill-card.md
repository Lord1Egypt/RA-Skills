## Description: <br>
Converts academic paper PDFs into editable PowerPoint posters and HTML files using OpenAI-compatible APIs such as UniAPI or MiniMax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caoxinran102-sys](https://clawhub.ai/user/caoxinran102-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and students use this skill to set up Paper2Poster, configure API credentials, and generate academic poster files from a supplied paper PDF. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs external Paper2Poster code. <br>
Mitigation: Use a disposable directory or container, review or pin the repository before execution, and confirm before cloning, installing, or running code. <br>
Risk: The skill stores API credentials locally in a .env file. <br>
Mitigation: Use a dedicated low-limit API key and keep .env out of version control. <br>
Risk: Paper content may be sent to configured API or search providers. <br>
Mitigation: Avoid confidential or unpublished papers unless the configured providers are trusted for that data. <br>


## Reference(s): <br>
- [Paper2Poster project page](https://paper2poster.github.io/) <br>
- [Paper2Poster arXiv paper](https://arxiv.org/abs/2505.21497) <br>
- [Paper2Poster dataset](https://huggingface.co/datasets/Paper2Poster/Paper2Poster) <br>
- [Paper2Poster Hugging Face paper page](https://huggingface.co/papers/2505.21497) <br>
- [Paper2Poster Hugging Face Spaces demo](https://huggingface.co/spaces/camel-ai/Paper2Poster) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Files, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands and generated PPTX/HTML file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided paper PDF path, OpenAI-compatible API credentials, and an optional logo path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
