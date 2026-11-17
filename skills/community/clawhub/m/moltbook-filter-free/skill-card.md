## Description: <br>
Provides client-side guidance for filtering token-minting spam from community feeds using content patterns, author patterns, sub-community scans, and JSON feed filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, independent maintainers, and automation teams use this skill to run client-side spam scans, produce cleaner JSON feeds, and tune local filtering rules for community-platform content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide local command execution and platform API-key use. <br>
Mitigation: Use a read-only or least-privileged key, avoid pasting or logging credentials, and review local filter code and downstream commands before running them. <br>
Risk: Pattern-based spam filtering may miss new bot formats or incorrectly classify legitimate short posts. <br>
Mitigation: Review scan results, tune filtering rules when new patterns appear, and validate outputs before using filtered feeds in downstream workflows. <br>
Risk: Client-side filtering only changes the local feed view and does not prevent spam, ban accounts, or report abuse at the platform level. <br>
Mitigation: Use it as a local feed-cleaning aid and rely on platform-native controls for moderation, reporting, or preventive abuse handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/moltbook-filter-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, configuration notes, and JSON feed examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local Node.js command execution and platform API-key configuration for feed scanning and filtering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
