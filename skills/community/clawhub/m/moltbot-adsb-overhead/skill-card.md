## Description: <br>
ADS-B Overhead helps configure and operate aircraft-overhead alerts using a local ADS-B SBS/BaseStation feed, optional aircraft enrichment, and WhatsApp notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davestarling](https://clawhub.ai/user/davestarling) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to set up, tune, and troubleshoot a periodic Clawdbot watcher that detects nearby aircraft from a local readsb SBS/BaseStation feed and sends WhatsApp notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runtime configuration can reveal a home location, ADS-B feed host, and WhatsApp target. <br>
Mitigation: Keep the config file private, restrict file permissions, and confirm home coordinates, radius, photo settings, and notification target before enabling the watcher. <br>
Risk: Continuous cron or timer execution can keep sending aircraft notifications after the user no longer wants monitoring. <br>
Mitigation: Remove the cron entry, disable the config, or stop the timer when continuous monitoring is no longer desired. <br>
Risk: Incorrect SBS host, radius, cooldown, or quiet-hours settings can cause missed alerts or excessive notifications. <br>
Mitigation: Run a short manual checker test and review cooldown, listen time, radius, and quiet-hours settings before scheduled operation. <br>


## Reference(s): <br>
- [SBS/BaseStation MSG fields](references/sbs-fields.md) <br>
- [ADS-B Overhead ClawHub release](https://clawhub.ai/davestarling/moltbot-adsb-overhead) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime checker can emit plain text alerts or JSONL records; the notifier sends one WhatsApp message per aircraft alert.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
