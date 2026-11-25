## Description:

Generates WeChat Channels commerce videos with QH AI video models and supports storyboard scripting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External WeChat private traffic operators and livestream commerce teams use this skill to create product, recommendation, educational, and livestream promotion videos for WeChat Channels and related placements.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security scan flags unpinned package versions that can change between runs.

Mitigation: Pin the qhkit package version and review package updates before installing or upgrading.

Risk: Credentials and reference media may be exposed to external services.

Mitigation: Do not share API keys in chat, and upload only media you are authorized to send after assessing trust in the service.

Risk: The scan was partial because several local references were missing.

Mitigation: Retrieve and review the missing references before relying on guidance that depends on them.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Videos, Storyboard scripts, Shell commands, Configuration guidance]

**Output Format:** [Generated video files or URLs, storyboard text, and JSON-formatted CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to portrait 9:16 and Simplified Chinese when supported; video models and options are checked at runtime.]

## Skill Version(s):

0.1.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
