## Description:

Control an Icom IC-7610 transceiver over USB/LAN. Get/set frequency, mode, power, S-meter, SWR. CW keying and beacon mode. Remote power on/off.

This skill is ready for commercial/non-commercial use.

## Publisher:

[morozsm](https://clawhub.ai/user/morozsm)

### License/Terms of Use:


## Use Case:

External amateur radio operators and station maintainers use this skill to guide agent-assisted setup and operation of an Icom IC-7610, including status checks, configuration, frequency and mode changes, power control, CW keying, and beacon workflows.

### Deployment Geography for Use:

Global, subject to local amateur radio regulations.

## Known Risks and Mitigations:

Risk: The skill can guide an agent to control real radio hardware, including power, frequency, CW keying, and beacon actions.

Mitigation: Use it only with an operator who is comfortable supervising radio hardware control, and require explicit review before power, frequency, transmit, or beacon actions.

Risk: Some examples source local environment files or use inline shell/Python snippets that may be unsafe when copied directly into scripts.

Mitigation: Replace sourced .env, eval-style command construction, and Python -c examples with safer argument-based parsing before automation.

Risk: Transmit or beacon operations can violate band, mode, power, SWR, or local regulatory limits.

Mitigation: Require operator confirmation for all RF transmission, run pre-transmit checks, refuse out-of-band or high-SWR transmissions, and confirm local amateur radio rules before use.

Risk: Network control endpoints could expose radio control beyond the intended workstation or trusted LAN.

Mitigation: Keep FLRIG_URL and rigctld bound to trusted local addresses and avoid exposing control ports to untrusted networks.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/morozsm/icom-7610)
- [ClawHub skill page](https://clawhub.ai/morozsm/skills/icom-7610)
- [Full reference](references/FULL-REFERENCE.md)
- [wfview downloads](https://wfview.org/download)
- [flrig help](http://www.w1hkj.com/flrig-help/)
- [Icom firmware and driver support](https://www.icomjapan.com/support/firmware_driver/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that control radio hardware; transmit and beacon actions require operator confirmation.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
