## Description: <br>
Hugging Face CLI helps agents use the hf command to download, upload, search, and manage Hugging Face Hub resources, jobs, endpoints, webhooks, and local cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huggingface](https://clawhub.ai/user/huggingface) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ML practitioners use this skill when an agent needs to authenticate with Hugging Face and manage Hub models, datasets, Spaces, buckets, repos, jobs, endpoints, collections, papers, or webhooks through CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through broad Hugging Face account, token, repository, bucket, job, endpoint, webhook, and skill-install actions. <br>
Mitigation: Use it only for explicit Hugging Face tasks and require user confirmation before deletes, uploads, deployments, jobs, webhooks, skill installs, or other remote state changes. <br>
Risk: Authentication commands and options can expose or misuse Hugging Face access tokens. <br>
Mitigation: Avoid commands that print tokens, prefer HF_TOKEN or managed secret storage, and do not echo or persist tokens in logs or generated files. <br>
Risk: The artifact recommends installing tools through remote shell scripts. <br>
Mitigation: Prefer a pinned or verifiable package method when available, and review remote install scripts before execution. <br>
Risk: Several file, cache, bucket, repository, endpoint, and webhook operations can delete or overwrite local or remote resources. <br>
Mitigation: Prefer dry-run modes where supported and review planned changes before applying them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huggingface/skills/hf-cli) <br>
- [Hugging Face CLI Install Script](https://hf.co/cli/install.sh) <br>
- [hf-mount GitHub Repository](https://github.com/huggingface/hf-mount) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command snippets and option summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands support json, agent, quiet, table, or human-readable output modes.] <br>

## Skill Version(s): <br>
1.20.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
