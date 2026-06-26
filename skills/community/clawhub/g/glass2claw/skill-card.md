## Description: <br>
Ray-Ban glasses to voice command to WhatsApp to OpenClaw auto-routes your photo into the right database for hands-free life logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JonathanJing](https://clawhub.ai/user/JonathanJing) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill as a routing protocol for sending photos from Meta Ray-Ban glasses through WhatsApp into OpenClaw, where images are classified and routed to configured specialist agents and databases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically forward personal photos from WhatsApp into configured agents, channels, or databases without per-item confirmation. <br>
Mitigation: Use private ingress channels, allowlist destination session keys, and add a review step before posting images or writing records. <br>
Risk: Connected services such as databases or Discord channels may receive sensitive or third-party photos. <br>
Mitigation: Use least-privilege database tokens and avoid processing sensitive or third-party photos without consent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JonathanJing/glass2claw) <br>
- [README](artifact/README.md) <br>
- [Vision Hub sample routing logic](artifact/SAMPLE_AGENT.md) <br>
- [Wine Specialist sample persona](artifact/SAMPLE_SOUL_WINE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands] <br>
**Output Format:** [Markdown with inline shell commands and sample agent instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes routing templates for forwarding images to configured sessions and destination databases.] <br>

## Skill Version(s): <br>
2.3.3 (source: frontmatter, skill.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
