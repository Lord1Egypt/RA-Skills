## Description: <br>
Control an Icom IC-7610 transceiver over USB/LAN. Get/set frequency, mode, power, S-meter, SWR. CW keying and beacon mode. Remote power on/off. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morozsm](https://clawhub.ai/user/morozsm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Amateur radio operators and station automation developers use this skill to inspect and control an Icom IC-7610 transceiver over USB or LAN. It supports radio status checks, configuration changes, CW keying, beacon workflows, and remote power control when the required station software and safety checks are in place. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change radio state and initiate transmissions. <br>
Mitigation: Keep transmit, CW, beacon, high-power, and power-state actions under explicit operator control. <br>
Risk: Improper frequency, power, or antenna conditions can create regulatory or equipment risk. <br>
Mitigation: Verify license privileges, jurisdiction, frequency, mode, power, and SWR before transmitting; refuse out-of-band transmissions and SWR above documented limits. <br>
Risk: The documented retry helper uses eval-style command execution. <br>
Mitigation: Do not adapt the retry helper for untrusted command strings unless it is rewritten without eval. <br>


## Reference(s): <br>
- [Full IC-7610 Reference](references/FULL-REFERENCE.md) <br>
- [ClawHub listing](https://clawhub.ai/morozsm/icom-7610) <br>
- [wfview download](https://wfview.org/download) <br>
- [flrig help](http://www.w1hkj.com/flrig-help/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local station configuration and external radio-control tools such as rigctl, curl, and python3.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
