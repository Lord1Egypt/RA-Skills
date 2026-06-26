## Description: <br>
Wiki helps an agent build and maintain a structured Markdown personal knowledge base, lint it for consistency, and serve it as a local MkDocs website. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nkhoit](https://clawhub.ai/user/nkhoit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual knowledge workers use this skill to turn durable conversation outputs and raw source material into a local Markdown wiki with topic pages, cross-links, linting, build logs, and a browsable static site. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent setup changes the local Python environment and creates an auto-starting localhost wiki server. <br>
Mitigation: Review the bootstrap behavior before installation and only run setup when a persistent local wiki service is desired. <br>
Risk: Git publication workflows can push wiki contents to a configured remote. <br>
Mitigation: Keep remote push disabled unless the destination and credentials have been reviewed. <br>
Risk: Optional heartbeat memory-gap detection can let memory notes influence wiki updates. <br>
Mitigation: Do not enable heartbeat memory-gap detection unless memory-note access is acceptable for the wiki workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nkhoit/llm-wiki) <br>
- [Heartbeat Integration](references/heartbeat-integration.md) <br>
- [Example Article Template](references/article-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown wiki files, MkDocs configuration, shell command usage, and concise agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates content under ~/wiki/; build output is a local static site served from 127.0.0.1 by default.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
