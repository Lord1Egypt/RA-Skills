## Description: <br>
Databox (databox.com). Use this skill for ANY Databox request - reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Databox through an OOMOL-connected account, including listing accounts, checking dataset ingestion status, creating data sources and datasets, pushing dataset records, and deleting Databox resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The `push_dataset_data` action changes Databox data but is not marked for confirmation in the artifact's action list. <br>
Mitigation: Require explicit user confirmation of the target dataset and payload before running `push_dataset_data`. <br>
Risk: The skill requires sensitive Databox credentials through an OOMOL-connected account. <br>
Mitigation: Use the server-side credential flow and avoid exposing raw Databox tokens in prompts, files, or command arguments. <br>


## Reference(s): <br>
- [Databox homepage](https://databox.com/) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-databox) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions can read Databox data, write datasets and data sources, or delete Databox resources through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
