## Description:

Long Memory helps agents archive complete conversation histories, retrieve prior sessions semantically, and maintain continuity across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zyuanjia](https://clawhub.ai/user/zyuanjia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve long-running conversation context, search historical discussions, generate summaries and reports, and manage memory archives across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive conversation archives may be retained locally for long periods.

Mitigation: Install only when long-term local retention is acceptable, configure retention deliberately, and avoid storing secrets or regulated data unless the environment is approved.

Risk: The REST API can write chat archives and should not be exposed to untrusted callers.

Mitigation: Do not start the API unless it is isolated to trusted local use or protected by external access controls.

Risk: The advertised encryption should not be relied on for protecting secrets.

Mitigation: Use separate, reviewed secret-management or encryption controls for sensitive material and avoid placing credentials in memory archives.

Risk: Exports, reports, and Git backups may disclose archived conversations.

Mitigation: Review generated reports and exports before opening or sharing them, and configure backup remotes only when the destination is trusted.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and command-line guidance, with optional JSON, Markdown, text, and HTML files produced by the bundled tools.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local memory archives, indexes, summaries, exports, reports, logs, backups, and API responses depending on the command used.]

## Skill Version(s):

7.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
