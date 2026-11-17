## Description:

GLM-V-Grounding uses GLM-V native grounding to locate prompt-specified targets in images or videos, extract normalized coordinates, and create bounding-box or tracking visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredforreal](https://clawhub.ai/user/jaredforreal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to ground prompt-described targets in images and videos, convert GLM-V responses into coordinate structures, and optionally generate visual overlays for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local images or videos can be sent to Zhipu's GLM-V API.

Mitigation: Use only approved media inputs, avoid sensitive local paths, and run the skill in a workspace or sandbox that cannot read unrelated secrets.

Risk: API-key setup can expose secrets through command-line arguments or a weakly protected .env file.

Mitigation: Prefer environment variables over the documented --api-key form, restrict .env permissions, and keep .env out of version control.

## Reference(s):

- [GLM-V-Grounding homepage](https://github.com/zai-org/GLM-V/tree/main/skills/glmv-grounding)
- [Zhipu API key setup](https://www.bigmodel.cn/usercenter/proj-mgmt/apikeys)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with Python-style coordinate lists, JSON-like detection and tracking structures, and optional visualization file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates are normalized to a 0-1000 range; optional image or video visualizations may be written to a local output directory.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
