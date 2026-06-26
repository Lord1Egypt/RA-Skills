## Description: <br>
Kaizen provides local continuous improvement guidance and a note tracker for Kaizen events, PDCA, gemba walks, A3 reports, and daily improvement records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operations teams, and process-improvement facilitators can use this skill to access Kaizen reference guidance and maintain local notes for improvement activities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-provided notes locally and can export them to files in the current directory. <br>
Mitigation: Avoid entering confidential operational or personnel data; review exported files before sharing. <br>
Risk: Remove and export actions can delete entries or create additional copies of locally stored data. <br>
Mitigation: Confirm the target entry or export format before running those commands, and keep backups when notes matter. <br>
Risk: The documentation presents reference-style commands that do not fully match the bundled script behavior. <br>
Mitigation: Treat the script help output as the executable behavior and review commands before use. <br>


## Reference(s): <br>
- [Kaizen ClawHub listing](https://clawhub.ai/xueyetianya/kaizen) <br>
- [Publisher profile](https://clawhub.ai/user/xueyetianya) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local text, JSONL, or CSV outputs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses KAIZEN_DIR when configured; otherwise stores local data under ~/.kaizen and can export kaizen-export.json or kaizen-export.csv in the current directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
