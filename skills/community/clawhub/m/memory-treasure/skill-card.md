## Description: <br>
Complete memory management tool to activate, organize, and back up an AI agent's local memory folder; it must be paired with memory-key for full function. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markma84](https://clawhub.ai/user/markma84) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI users use this skill to organize persistent local AI memory across hot, warm, and cold storage so an agent can reload principles, insights, todos, completed work, and archived conversations after restarts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to retain, reload, and back up potentially sensitive local memory and conversation data. <br>
Mitigation: Keep API keys, credentials, personal data, and confidential work out of the memory folder; define inspection, redaction, encryption, backup, and deletion procedures before relying on it. <br>
Risk: The artifact describes hourly archival behavior without clear user controls in the release evidence. <br>
Mitigation: Confirm whether any cron archival is enabled and review stored files before installing or activating automated memory backup behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/markma84/memory-treasure) <br>
- [Example memory concept template](artifact/examples/memory/00-概念模板.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance and memory folder conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory organization rules, startup loading guidance, retention guidance, backup trigger behavior, and a reusable memory template.] <br>

## Skill Version(s): <br>
4.3.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
