## Description: <br>
Checks an OpenClaw GIGO Lobster environment for gateway, Python dependency, task-bundle, and PNG certificate readiness without running the formal benchmark. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gigolab](https://clawhub.ai/user/gigolab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to run a preflight environment check before a GIGO Lobster benchmark. It verifies gateway availability, Python/runtime dependencies, task-bundle access, and certificate generation readiness without starting the formal tasting run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The doctor may contact the GIGO API, check a local OpenClaw gateway, and read OpenClaw secrets.env into its environment. <br>
Mitigation: Run it only in an environment where those credentials and network contacts are acceptable, and review the configured GIGO/OpenClaw endpoints before execution. <br>
Risk: The skill may create a managed Python runtime and install packages while performing diagnostics. <br>
Mitigation: Use an isolated workspace or virtual environment and review package/bootstrap behavior before running on sensitive systems. <br>
Risk: The packaged artifact includes broader benchmark runner code with shell execution and upload paths beyond the doctor label. <br>
Mitigation: Use the documented run_doctor.py entrypoint for environment checks, and avoid invoking main.py or setting GIGO_V2_AGENT_COMMAND unless broader benchmark execution is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gigolab/gigo-lobster-doctor) <br>
- [Publisher profile](https://clawhub.ai/user/gigolab) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [bundle/README.md](bundle/README.md) <br>
- [bundle/INTEGRATION.md](bundle/INTEGRATION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance, files] <br>
**Output Format:** [Markdown-style agent responses with inline shell commands, progress updates, and diagnostic result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write diagnostic logs and output artifacts under the configured OpenClaw workspace output directory.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
