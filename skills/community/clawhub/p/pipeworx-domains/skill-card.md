## Description: <br>
Search registered domain names by keyword and TLD to find what is already taken via Domainsdb.info. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, brand researchers, and analysts use this skill to search registered domains by keyword and optional TLD for brand research, competitive analysis, domain squatting analysis, and domain brainstorming. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports that the skill can create, publish, and roll back other skills, including modes that can change future agent behavior automatically. <br>
Mitigation: Review the skill before deployment, start in manual mode, and inspect proposed diffs before publishing changes. <br>
Risk: Captured workflows or autonomous behavior could expose sensitive workspace context. <br>
Mitigation: Keep secrets out of captured workflows and avoid autonomous mode in sensitive workspaces. <br>


## Reference(s): <br>
- [Pipeworx Domains Pack](https://pipeworx.io/packs/domains) <br>
- [Pipeworx Domains MCP endpoint](https://gateway.pipeworx.io/domains/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-domains) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/brucegutman) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JSON snippets; tool responses contain domain records with dates and timestamps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the documented direct API example.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
