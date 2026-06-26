## Description: <br>
Living ADR helps developers draft, number, update, and supersede Architecture Decision Record Markdown files from git diffs, PR descriptions, or plain-English decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to keep ADR documentation current by generating proposed ADR files, marking superseded decisions, and maintaining an ADR index from repository context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated ADRs, supersession edits, or README index changes may misstate a team's architecture decisions. <br>
Mitigation: Review all generated Markdown and repository diffs before committing. <br>
Risk: The skill inspects repository context and git history to infer architectural decisions. <br>
Mitigation: Use it only in repositories where that local context is appropriate for agent review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PHY041/phy-living-adr) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown ADR drafts and status summaries with inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update docs/adr/*.md and docs/adr/README.md when used by an agent with file access.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
