## Description: <br>
Gigo Lobster Local runs the GIGO Lobster benchmark in local mode for OpenClaw users, producing local report and certificate artifacts without registering a personal result page or leaderboard entry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigolab](https://clawhub.ai/user/gigolab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run a local-mode GIGO Lobster evaluation, inspect local report, certificate, and log artifacts, and avoid leaderboard or personal result-page registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local-mode wording may lead users to expect a strictly offline run, but security evidence says the skill may contact GIGO cloud endpoints and send evaluation data for judging. <br>
Mitigation: Run in an isolated workspace with deliberate network policy, and review generated reports and logs before sharing results. <br>
Risk: The skill may read ambient secrets.env values or other sensitive environment variables during execution. <br>
Mitigation: Use a minimal environment for benchmark runs and avoid exposing unrelated credentials to the OpenClaw workspace. <br>
Risk: The skill may bootstrap Python packages at runtime. <br>
Mitigation: Use a disposable virtual environment or container and review package installation behavior before running in a trusted workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gigolab/gigo-lobster-local) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [User README](artifact/README.md) <br>
- [Bundle README](artifact/bundle/README.md) <br>
- [Task schema](artifact/bundle/specs/task-schema.md) <br>
- [Judge protocol](artifact/bundle/specs/judge-protocol.md) <br>
- [Scoring spec](artifact/bundle/specs/scoring.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, files, guidance] <br>
**Output Format:** [Console progress plus local HTML, PNG or SVG certificate, and log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default output directory is ~/.openclaw/workspace/outputs/gigo-lobster-local unless an output directory is supplied.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence and artifact/manifest.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
