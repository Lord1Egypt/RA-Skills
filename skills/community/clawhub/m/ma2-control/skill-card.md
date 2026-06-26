## Description: <br>
Controls a physical grandMA2 lighting console over Telnet through a local bridge script for fixture selection, dimming, cue storage, playback, and status queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[y1035211-cloud](https://clawhub.ai/user/y1035211-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Lighting programmers, show operators, and agents use this skill to translate grandMA2 control requests into bridge-script commands for selecting fixtures, setting intensity or attributes, storing cues, controlling playback, and querying console state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send commands to a real grandMA2 lighting console and may affect live output or show data. <br>
Mitigation: Install only for intentional console control, use it on a trusted show network, verify the target IP and port before use, and require operator confirmation before live output or playback commands. <br>
Risk: Commands such as Store, Assign, Delete, Move, overwrite, noconfirm, or broad fixture ranges can change show data without clear built-in safeguards. <br>
Mitigation: Review the local ma2_bridge scripts and require manual confirmation before any show-data-changing command, destructive command, no-confirm option, or broad fixture-range operation. <br>


## Reference(s): <br>
- [Ma2 Control ClawHub page](https://clawhub.ai/y1035211-cloud/ma2-control) <br>
- [MA2 command syntax](references/MA2_COMMAND_SYNTAX.md) <br>
- [MA2 command templates](references/MA2_TEMPLATES.md) <br>
- [MA2 troubleshooting guide](references/MA2_TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and grandMA2 command strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, curl, nc, the local ~/ma2_bridge/ma2_cmd.sh script, and MA2_IP_EXPECTED/MA2_TELNET_PORT_EXPECTED network configuration.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
