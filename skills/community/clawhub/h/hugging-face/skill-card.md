## Description: <br>
Discover, evaluate, and run Hugging Face models, datasets, and spaces with license checks, benchmark prompts, and reproducible integration plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI practitioners use this skill to shortlist Hugging Face models, datasets, or Spaces, verify license and access constraints, benchmark finalists, and prepare reproducible inference or integration plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected search terms, prompts, and inference inputs may be sent to Hugging Face services. <br>
Mitigation: Send only the minimum task data needed, avoid secrets or sensitive private content, and use local-only alternatives when external processing is not acceptable. <br>
Risk: A Hugging Face token may be required for gated models or hosted inference. <br>
Mitigation: Use a scoped HF_TOKEN, avoid printing tokens in logs or transcripts, and rotate credentials if exposure is suspected. <br>
Risk: Local notes under ~/hugging-face/ may persist preferences, shortlists, endpoint notes, and evaluation context. <br>
Mitigation: Review local memory before relying on it, keep durable notes minimal, and do not store raw secrets or private keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/hugging-face) <br>
- [Skill homepage](https://clawic.com/skills/hugging-face) <br>
- [Hugging Face model API](https://huggingface.co/api/models) <br>
- [Hugging Face dataset API](https://huggingface.co/api/datasets) <br>
- [Hugging Face Spaces API](https://huggingface.co/api/spaces) <br>
- [Hugging Face Inference API](https://api-inference.huggingface.co/models/{model_id}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, API request examples, evaluation notes, and local memory templates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference curl, jq, HF_TOKEN, and local files under ~/hugging-face/ when the user approves setup or execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
