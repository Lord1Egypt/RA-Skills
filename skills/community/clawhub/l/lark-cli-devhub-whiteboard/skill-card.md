## Description: <br>
Use when creating or updating Feishu/Lark Whiteboards through lark-cli or feishu-cli for a development knowledge hub, including architecture maps, bug investigation paths, task maps, dependency maps, and project knowledge graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afengzi](https://clawhub.ai/user/afengzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create and update Lark/Feishu whiteboards for development knowledge hubs, including architecture maps, bug investigation paths, release flows, task dependency maps, and project knowledge graphs. Durable whiteboards are paired with Base artifact records so future agents can discover the map without visual inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated whiteboard update commands can overwrite or modify Lark/Feishu boards. <br>
Mitigation: Use dry-run output first, review generated diagrams and payloads, and scope WHITEBOARD_TOKEN to a board that is acceptable to modify. <br>
Risk: Generated visual maps can be incomplete, misleading, or hard for future agents to discover. <br>
Mitigation: Keep diagrams small enough for human scanning, validate locally when possible, and maintain the paired Base Artifacts record with summary and search keywords. <br>
Risk: External CLI and npm tooling runs local commands and depends on the user's authenticated environment. <br>
Mitigation: Install only when lark-cli, npx, and the Lark/Feishu account context are trusted for the target workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/afengzi/lark-cli-devhub-whiteboard) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with diagram source and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires lark-cli and npx; whiteboard updates should use a scoped WHITEBOARD_TOKEN and dry-run review before writes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
