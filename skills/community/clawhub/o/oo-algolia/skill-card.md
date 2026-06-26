## Description: <br>
Algolia (algolia.com). Use this skill for ANY Algolia request: reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Algolia indices, search or browse records, and manage records, rules, and synonyms through an OOMOL-connected Algolia account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change Algolia records, rules, and synonyms. <br>
Mitigation: Review the exact action schema and payload with the user before running write actions. <br>
Risk: The skill can delete records by filter. <br>
Mitigation: Require explicit approval for the target index and filter before running destructive delete operations. <br>
Risk: The skill requires sensitive Algolia credentials through the OOMOL connector. <br>
Mitigation: Use a least-privilege Algolia API key and install only when OOMOL is trusted as the connector provider. <br>


## Reference(s): <br>
- [ClawHub Algolia Skill](https://clawhub.ai/oomol/oo-algolia) <br>
- [OOMOL Publisher Profile](https://clawhub.ai/user/oomol) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Algolia](https://www.algolia.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector responses may include JSON data and an execution id when actions are run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
