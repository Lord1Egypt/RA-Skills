## Description: <br>
Buddy is an OpenClaw virtual pet skill for hatching, interacting with, viewing stats for, muting, and unmuting a deterministic companion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwin19861218](https://clawhub.ai/user/edwin19861218) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use Buddy to keep a local virtual pet companion whose species, rarity, attributes, and personality are shown through command responses and ASCII sprites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The reviewed package can execute JavaScript from a separate local Buddy extension that is not included in the package. <br>
Mitigation: Install only if you trust the existing ~/.openclaw/extensions/buddy-companion installation, especially its sprites.js file. <br>
Risk: The skill uses local OpenClaw identity or host/user-derived data and stores or reads Buddy state locally. <br>
Mitigation: Review the local state behavior before use and avoid sharing generated Buddy output if identity-derived personalization is sensitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/edwin19861218/openclaw-claude-buddy) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text with ASCII art] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Node and local OpenClaw files; no API-key environment variables were detected in the reviewed artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
