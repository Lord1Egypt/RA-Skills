## Description: <br>
Fetches Hugging Face Daily Papers through the HF API, reads the results, and helps score papers into a formatted digest with commentary for daily paper requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godiao](https://clawhub.ai/user/godiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical readers use this skill to fetch Hugging Face Daily Papers for a target date, inspect the generated paper data, and produce a scored daily research digest with concise commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Hugging Face token may be exposed if pasted into shared chats, screenshots, shell history, or committed files. <br>
Mitigation: Use a read-only token, provide it through the HF_TOKEN environment variable, and avoid storing real tokens in shared or versioned material. <br>
Risk: The fetch script creates or overwrites hf_results.json in the directory where it is run. <br>
Mitigation: Run the script from a dedicated working directory or review existing files before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/godiao/hf-daily-papers) <br>
- [Hugging Face Daily Papers](https://huggingface.co/papers) <br>
- [Hugging Face Access Tokens](https://huggingface.co/settings/tokens) <br>
- [arXiv Abstract Pages](https://arxiv.org/abs/{paper_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown digest guidance, shell commands, and a JSON results file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The fetch script reads HF_TOKEN from the environment and writes hf_results.json in the working directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
