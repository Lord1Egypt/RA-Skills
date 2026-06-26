## Description: <br>
Analyzes local AI conversation history across coding agents to find framework sentences, activity patterns, and profile material for a Promptfolio portrait. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billc8128](https://clawhub.ai/user/billc8128) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external Promptfolio users use this skill to analyze recent local AI coding-agent conversations, identify framework sentences and activity patterns, review the generated portrait, and sync structured results after confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects broad private AI conversation histories and local coding-agent telemetry. <br>
Mitigation: Run it only with informed user consent, limit sources to the intended tools, and avoid unknown-source scanning unless that scope is explicitly desired. <br>
Risk: Generated profile artifacts can contain direct quotes, project summaries, activity data, and behavioral fingerprints. <br>
Mitigation: Review _pf_parts files and promptfolio_payload.json before syncing, remove sensitive material, and treat the generated artifacts as private data. <br>
Risk: Structured profile results may persist beyond the local analysis step once synced. <br>
Mitigation: Sync only after user review and confirmation, and keep or publish the profile according to the user's privacy preference. <br>


## Reference(s): <br>
- [Conversation Analysis Guidelines](analysis-prompt.md) <br>
- [Promptfolio service](https://promptfolio.club) <br>
- [ClawHub release page](https://clawhub.ai/billc8128/promptfolio-summarize) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON profile artifacts, shell commands, and a structured sync payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local _pf_parts JSON files and promptfolio_payload.json for user review before sync.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
