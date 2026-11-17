## Description:

Fetches GPON status and device information from a SmartAX MA5671A / OpenWrt SFP local admin page and returns an icon-enhanced text table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wowrouter](https://clawhub.ai/user/wowrouter)

### License/Terms of Use:

MIT-0

## Use Case:

Network operators and device owners use this skill to check local GPON registration, optical power, temperature, link, reboot, boot partition, and firmware details from a known SmartAX MA5671A / OpenWrt SFP admin interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses a local device admin page as root over unencrypted HTTP with a blank password and session cookie reuse.

Mitigation: Use only on a trusted, isolated local network; confirm the IP belongs to the intended GPON/OpenWrt device; avoid logging cookies or credentials; prefer HTTPS or a read-only monitoring account if supported.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wowrouter/skills/gpon-status)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown table with icons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes device information, GPON status, optical power, temperature, link rate, reboot count, and boot partition when available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
