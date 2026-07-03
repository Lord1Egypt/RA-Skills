## Description: <br>
Scans a user's local WorkBuddy skill assets, presents discovered skills as selectable Markdown cards, and guides optional multi-platform distribution after confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingmuhuijianghu](https://clawhub.ai/user/qingmuhuijianghu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WorkBuddy users and skill creators use this agent to find locally stored Skill assets, review metadata, select candidates for distribution, and receive guidance for publishing through a separate matrix publishing assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request broad local file, drive, chat-history, memory, and session access during discovery. <br>
Mitigation: Narrow the scan scope to specific folders or drives, keep chat-history and memory searches disabled unless needed, and require explicit confirmation before any deeper scan. <br>
Risk: The skill can guide users toward upload or multi-platform distribution workflows after discovery. <br>
Mitigation: Require a fresh confirmation of selected skills and destination platforms before any upload or distribution step. <br>
Risk: Scan results can expose local paths and metadata about private or unpublished skills. <br>
Mitigation: Review scan output before sharing it, and avoid exposing full paths or sensitive metadata outside the local session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingmuhuijianghu/lobster-skill-radar) <br>
- [Publisher profile](https://clawhub.ai/user/qingmuhuijianghu) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown cards, confirmation prompts, SQL snippets, shell commands, and distribution status tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local scan summaries and publishing guidance; distribution actions require user confirmation and a separate publishing assistant.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
