## Description: <br>
Discover, store, and inspect AI model catalog entries from one or more sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoopan007](https://clawhub.ai/user/hoopan007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to sync OpenRouter model catalog entries into a local SQLite database and inspect newly discovered, recent, monthly, per-model, and aggregate catalog state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is third-party and should be matched to the intended package and publisher before installation. <br>
Mitigation: Verify the package page and publisher handle hoopan007 before use. <br>
Risk: The scan command fetches model catalog data from OpenRouter over the network and stores normalized and raw model metadata in SQLite. <br>
Mitigation: Run it only where outbound OpenRouter access and local database persistence are expected, and review the configured --db path before sharing outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/hoopan007/model-watcher) <br>
- [Publisher profile](https://clawhub.ai/user/hoopan007) <br>
- [Model Watcher schema](references/schema.md) <br>
- [OpenRouter model catalog endpoint](https://openrouter.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update a local SQLite database at the configured --db path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
