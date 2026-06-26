## Description: <br>
Lineage Code Mini builds a lightweight user profile from interaction history so agents can adapt response style, topic focus, timing, and recovery when replies stop landing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pablothethinker](https://clawhub.ai/user/pablothethinker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to inspect local interaction history, generate behavioral hints, and persist profile snippets that help future responses better match a user's communication preferences. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local interaction history and behavioral profiles that may contain sensitive preference or conversation signals. <br>
Mitigation: Review or delete the data directory periodically and avoid recording sensitive conversation content. <br>
Risk: Setup may install the lineage-code-mini npm dependency globally. <br>
Mitigation: Use a pinned local environment when dependency control matters. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/pablothethinker/lineage-mini) <br>
- [lineage-code-mini npm package](https://www.npmjs.com/package/lineage-code-mini) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON profile output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node; setup creates local JSON interaction and profile files and may install the lineage-code-mini npm package globally.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
