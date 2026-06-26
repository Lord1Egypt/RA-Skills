## Description: <br>
Create shopping lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to create fashion-related shopping lists and automate list tasks from provided input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact references a shopping_list_fashion.py script and LIST_API_KEY, but no executable script is included in the artifact. <br>
Mitigation: Verify that any script used with this skill comes from a trusted source and confirm what service the API key belongs to before installation or execution. <br>
Risk: API credentials may be exposed or over-scoped if LIST_API_KEY is configured carelessly. <br>
Mitigation: Use a limited-scope API key where possible and avoid placing credentials in shared logs, shell history, or committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/jpeng-shopping-list-fashion) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jpengcheng523-netizen) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses LIST_API_KEY when invoking the referenced shopping-list script.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
