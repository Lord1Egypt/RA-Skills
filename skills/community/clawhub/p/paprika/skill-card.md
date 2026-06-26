## Description: <br>
Access recipes, meal plans, and grocery lists from Paprika Recipe Manager. Use when user asks about recipes, meal planning, or cooking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People who use Paprika Recipe Manager can ask an agent to find recipes, inspect ingredients, review meal plans, and show grocery lists through the Paprika CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access private recipe, meal plan, and grocery data after Paprika authentication. <br>
Mitigation: Install and use it only when the agent is allowed to view that Paprika account data. <br>
Risk: Paprika credentials can be exposed if passwords are placed in shared shell environments or logs. <br>
Mitigation: Prefer interactive authentication, and avoid exporting Paprika passwords in shared shells or logged sessions. <br>
Risk: The skill depends on a globally installed npm CLI package. <br>
Mitigation: Verify the global npm package before installing or running it. <br>


## Reference(s): <br>
- [Paprika Recipe Manager](https://www.paprikaapp.com) <br>
- [ClawHub Paprika Skill](https://clawhub.ai/mjrussell/paprika) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request JSON output from the Paprika CLI for programmatic use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
