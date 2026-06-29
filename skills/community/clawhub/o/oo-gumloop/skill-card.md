## Description: <br>
Gumloop (gumloop.com). Use this skill for Gumloop requests that read, create, update, or run Gumloop resources through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Gumloop through the oo CLI with their OOMOL-connected account. It supports discovering connector schemas, listing saved flows and workbooks, reviewing run history and details, starting saved flow runs, and killing active runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start saved Gumloop flow runs, which may change Gumloop state or trigger downstream automation. <br>
Mitigation: Confirm the exact saved flow and JSON payload with the user before running start_flow_run. <br>
Risk: The skill can kill Gumloop flow runs and subflow runs, interrupting active work. <br>
Mitigation: Confirm the exact run target and expected effect before allowing kill_flow_run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-gumloop) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Gumloop homepage](https://www.gumloop.com) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector actions return JSON responses with data and execution metadata when run with --json.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
