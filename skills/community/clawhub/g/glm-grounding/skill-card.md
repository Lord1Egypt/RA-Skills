## Description:

Use GLM-4.7V's multimodal grounding capability to detect and locate objects or text in images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qijimrc](https://clawhub.ai/user/qijimrc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to locate requested objects, text, UI elements, or regions in images with GLM-4.7V and convert model responses into normalized bounding boxes and annotated image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and prompts may be sent to a configured model endpoint over plaintext HTTP.

Mitigation: Use only approved endpoints and network paths, or require transport and access controls appropriate for the submitted image content.

Risk: The skill instructs users to bypass proxies for internal model calls.

Mitigation: Deploy only where the proxy bypass is reviewed and approved by the environment owner.

Risk: Sensitive screenshots, documents, or personal images may expose confidential content to model infrastructure.

Mitigation: Avoid sensitive inputs unless retention, logging, access control, and network protections have been reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, API-call examples, and bounding-box coordinate examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bounding boxes are normalized to a 0-1000 coordinate range and can be converted to pixel coordinates for image annotation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
