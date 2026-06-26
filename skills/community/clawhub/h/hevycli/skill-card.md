## Description: <br>
Access and analyze Hevy fitness tracking data from the command line, including workouts, routines, exercise templates, JSON exports, and progress summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nsampre](https://clawhub.ai/user/nsampre) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve read-only Hevy fitness data, export it as structured JSON, and analyze training history, volume, frequency, and routines. It is useful when a user has Hevy Pro, a configured API key, and wants command-line access to their workout records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hevy API keys can expose access to private fitness data if pasted into shared terminals or chats. <br>
Mitigation: Configure API keys only in trusted local environments and avoid sharing command history, screenshots, or transcripts that include credentials. <br>
Risk: Exported workout JSON files may contain personal fitness history. <br>
Mitigation: Store exported files privately, limit retention, and review them before sharing with other people or tools. <br>
Risk: The skill depends on an external CLI project. <br>
Mitigation: Install only from trusted sources and prefer a pinned or reviewed version when possible. <br>


## Reference(s): <br>
- [Hevy skill page](https://clawhub.ai/nsampre/hevycli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Hevy data access; table and JSON CLI output formats are supported.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
