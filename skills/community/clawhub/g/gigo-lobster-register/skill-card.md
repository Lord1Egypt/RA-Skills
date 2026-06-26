## Description: <br>
Runs the GIGO Lobster benchmark in share-page mode, producing a personal result page without entering the leaderboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigolab](https://clawhub.ai/user/gigolab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to run a full GIGO Lobster agent benchmark and publish a shareable personal result page without leaderboard entry. It is intended for users who want benchmark evidence and share links rather than competitive ranking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may execute benchmark tests and commands with local workspace authority. <br>
Mitigation: Run it in a dedicated workspace or container and review generated logs and outputs before sharing results. <br>
Risk: The skill can read broad local profile or secrets files while preparing a benchmark run. <br>
Mitigation: Remove broad secrets.env files and unnecessary credentials from the workspace before running the skill. <br>
Risk: The skill may contact GIGO cloud services and upload benchmark responses to create a share page. <br>
Mitigation: Use it only when cloud registration is intended, and choose a local or skip-upload mode in companion tools when upload is not desired. <br>
Risk: External agent execution may be enabled through GIGO_V2_AGENT_COMMAND. <br>
Mitigation: Leave GIGO_V2_AGENT_COMMAND unset unless intentionally launching a specific external agent command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gigolab/gigo-lobster-register) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/gigolab) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [GIGO Lobster skill family README](artifact/README.md) <br>
- [GIGO Lobster Taster v2 task bundle](artifact/bundle/README.md) <br>
- [Task bundle integration guide](artifact/bundle/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command shapes and generated benchmark result artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs may create local logs, reports, certificates, and share-page registration output.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
