## Description: <br>
Use J&T Express (极兔速递) for shipment tracking, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer common J&T Express logistics questions, including shipment tracking, fee and delivery-time estimates, carrier comparison, outlet lookup, and parcel preparation. It can also guide users through local privacy controls when runtime storage features are used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local runtime features may persist shipment history, subscription records, saved addresses, encrypted helper files, and privacy exports under ~/.openclaw/data/jtexpress/. <br>
Mitigation: Use persistence only when needed, disclose the local storage path when privacy is relevant, and use the documented privacy info, privacy export, and privacy clear controls. <br>
Risk: Fee, delivery-time, or tracking guidance may be inaccurate when live carrier tools are unavailable or regional pricing varies. <br>
Mitigation: State assumptions, provide cautious ranges, and avoid claiming confirmed fees, statuses, or shipping actions unless live tools are available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrylabsj/jtexpress) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Concise Markdown guidance, estimates, comparisons, and privacy-control instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May provide cautious ranges and state assumptions when exact carrier fees, timing, or tracking status cannot be confirmed.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
