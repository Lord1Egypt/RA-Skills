## Description: <br>
Ml Visualizer is a command-line tool for recording ML and data workflow notes, searches, summaries, and exports in local plaintext logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to keep a lightweight local journal of ML data ingestion, transformation, validation, profiling, visualization requests, and pipeline activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered workflow notes are stored as plaintext local logs and can be searched or exported. <br>
Mitigation: Avoid entering secrets, credentials, or sensitive dataset details; set ML_VISUALIZER_DIR to an appropriate protected location when needed. <br>
Risk: The visualizer branding may imply model diagnostics or chart generation beyond the artifact behavior. <br>
Mitigation: Treat the skill as a workflow logger and validate any actual model analysis or visualization with separate tools. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bytesagain-lab/ml-visualizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text CLI output plus local log and export files in JSON, CSV, or TXT.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes logs under ~/.local/share/ml-visualizer by default; ML_VISUALIZER_DIR can override the data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
