## Description:

Track garden pests and diseases with treatments, treatment history, effectiveness monitoring, and control recommendations for home gardeners and small farmers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johstracke](https://clawhub.ai/user/johstracke)

### License/Terms of Use:


## Use Case:

External home gardeners and small farmers use this skill to log pest or disease issues, record treatments, search records, export Markdown summaries, and request treatment recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown export can overwrite files in broad home or temporary paths.

Mitigation: Use a dedicated export folder and avoid exporting over existing files.

Risk: Pesticide and fungicide recommendations may not reflect product labels, local rules, protective equipment needs, or edible-crop suitability.

Mitigation: Treat recommendations as general pointers; read product labels, follow local rules, use appropriate protective equipment, and confirm crop suitability.

Risk: Garden records are stored locally under ~/.openclaw/workspace.

Mitigation: Avoid recording sensitive personal information and manage local backups or deletion according to user needs.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text CLI responses and Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local garden records under ~/.openclaw/workspace and can export Markdown to user-selected paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
