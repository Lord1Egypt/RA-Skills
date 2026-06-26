## Description: <br>
Interactive Pinboard bookmark management with tag auditing, dead link detection, and content timeliness checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niracler](https://clawhub.ai/user/niracler) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Pinboard users use this skill to audit and reorganize tags, detect broken links, and review older technical bookmarks for timeliness. The skill helps agents propose and apply bookmark cleanup actions through Pinboard API calls after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Pinboard API token with read and modify access. <br>
Mitigation: Install only when comfortable granting that access, treat the token like a password, and rotate it if exposure is suspected. <br>
Risk: Confirmed actions can update or delete Pinboard bookmarks. <br>
Mitigation: Review every proposed update or deletion before confirming and consider exporting a Pinboard backup before bulk cleanup. <br>
Risk: Bookmark data may be cached temporarily in /tmp/pinboard_all.json. <br>
Mitigation: Delete /tmp/pinboard_all.json after use when bookmarks are sensitive. <br>
Risk: Jina-based timeliness checks may send bookmarked URLs to an external reader service. <br>
Mitigation: Avoid Jina-based timeliness checks for private or internal URLs. <br>


## Reference(s): <br>
- [Pinboard](https://pinboard.in/) <br>
- [Tag Audit Mode](references/tag-audit.md) <br>
- [Dead Link Detection Mode](references/dead-link.md) <br>
- [Timeliness Check Mode](references/timeliness.md) <br>
- [User Configuration](references/user-config.md) <br>
- [Tag Convention Example](references/tag-convention.example.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and structured action summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reuse a temporary Pinboard bookmark cache at /tmp/pinboard_all.json during a session.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
