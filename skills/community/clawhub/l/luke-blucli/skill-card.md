## Description: <br>
BluOS CLI (blu) for discovery, playback, grouping, and volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[banalit](https://clawhub.ai/user/banalit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent control Bluesound and NAD BluOS players through the blu CLI for discovery, playback, grouping, TuneIn, and volume tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to change playback, grouping, or volume on BluOS devices. <br>
Mitigation: Confirm the target device before playback, volume, or grouping changes. <br>
Risk: The skill declares installation of an external Go CLI module. <br>
Mitigation: Review or pin the upstream Go module when reproducible or audited installs are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/banalit/luke-blucli) <br>
- [blucli homepage](https://blucli.sh) <br>
- [blucli Go module](https://github.com/steipete/blucli) <br>
- [Publisher profile](https://clawhub.ai/user/banalit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose commands that control playback, grouping, and volume on selected BluOS devices.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
