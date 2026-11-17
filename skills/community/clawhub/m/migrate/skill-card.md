## Description:

Export and import Clawdbot installations for migration between machines, including workspace files, configuration, WhatsApp sessions, managed skills, and optionally credentials or session transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrgoodb](https://clawhub.ai/user/mrgoodb)

### License/Terms of Use:


## Use Case:

Developers and Clawdbot operators use this skill to back up, migrate, or restore a Clawdbot installation between machines. It is intended for migration workflows where local workspace files and trusted Clawdbot configuration need to move together.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exports may contain active WhatsApp session data, private workspace files, managed skills, transcripts, and optionally credentials.

Mitigation: Treat generated archives as secrets, protect them during transfer and storage, and avoid shared or cloud storage unless appropriate access controls and encryption are in place.

Risk: Importing an archive can restore archive-controlled skills and configuration into trusted Clawdbot locations.

Mitigation: Only import archives you created and trust; review archive contents before import and use the force option only when overwriting the target installation is intentional.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides an agent to run export and import shell scripts that create or restore tar.gz archives.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
