## Description: <br>
Helps identify, scope, and plan safe handling of deprecated project content such as legacy logic, old APIs, obsolete documentation, and cleanup candidates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fjmjulzl](https://clawhub.ai/user/fjmjulzl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use this skill to review deprecated or legacy project content, assess references and impact, and decide whether to delete, preserve compatibility, migrate, or mark content as deprecated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad cleanup or legacy-content requests could lead to deleting or replacing content that is still used. <br>
Mitigation: Define the deprecated scope clearly and review proposed deletions, replacements, or migration steps before edits are allowed. <br>
Risk: Deprecated content may still be referenced by runtime features, builds, configuration, scripts, or documentation. <br>
Mitigation: Trace definitions, references, call chains, and build or documentation dependencies before classifying content for deletion, compatibility, migration, or deprecation marking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fjmjulzl/order-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/fjmjulzl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown response in Chinese with conclusions, impact scope, recommended actions, and optional code snippets for deprecation markers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory output; file edits are only performed after an explicit user request.] <br>

## Skill Version(s): <br>
0.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
