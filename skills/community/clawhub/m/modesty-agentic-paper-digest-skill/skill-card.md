## Description: <br>
Fetches and summarizes recent papers from arXiv and Hugging Face, providing JSON digests and optional local API access for customizable research updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to configure and run an arXiv and Hugging Face paper-digest workflow, tune topics and fetch limits, and receive recent-paper summaries as JSON or through a local API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bootstrap and runtime use unpinned downloaded code that can receive a local API key. <br>
Mitigation: Review or pin the downloaded project before adding credentials, and run it in a fresh project directory. <br>
Risk: The skill requires a sensitive API key for LLM calls. <br>
Mitigation: Use a limited, revocable key and keep it in the configured environment file or shell rather than hardcoding it in source files. <br>
Risk: The optional API workflow exposes a local service and the stop script may terminate other processes on port 8000. <br>
Mitigation: Keep the API bound to localhost and avoid the stop script when another service may be using port 8000. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-agentic-paper-digest-skill) <br>
- [Agentic Paper Digest project homepage](https://github.com/matanle51/agentic_paper_digest) <br>
- [SkillBoss API Hub](https://api.skillboss.co/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration instructions, JSON digest output, and optional local API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI JSON output includes run metadata and paper counts; runtime data is stored in a local SQLite database under the configured project directory.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
