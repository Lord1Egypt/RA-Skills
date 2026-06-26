## Description: <br>
Generate a grounded nuclear energy policy brief from live news using Apify and Contextual. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ab-naidu](https://clawhub.ai/user/ab-naidu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Policy analysts and energy teams use this skill to turn recent public nuclear policy and regulatory news into a concise brief with changes, implications, risks, recommended actions, and source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search terms, topics, and retrieved source material to Apify and Contextual. <br>
Mitigation: Use scoped API keys, monitor provider usage, and avoid confidential information in queries or topics. <br>
Risk: Changing the default Apify actor can alter the data source and trust boundary. <br>
Mitigation: Use the default actor or only override it with an actor the operator trusts. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ab-naidu/global-nuclear-brief) <br>
- [Apify run-sync dataset items API](https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items) <br>
- [Contextual generation API](https://api.contextual.ai/v1/generate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style structured brief with source titles and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live public news retrieval and grounded synthesis; output is capped by the script's max-token setting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
