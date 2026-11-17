## Description:

Baidu Qianfan (qianfan.cloud.baidu.com). Use this skill for ANY Baidu Qianfan request — reading, creating, updating, and deleting data. Whenever a task involves Baidu Qianfan, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to access Baidu Qianfan through an OOMOL-connected account. It supports reading and managing Qianfan data and running text, search, embedding, OCR, batch, image, video, and file actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded CLI software, and the CLI can install and synchronize other agent skills; the installer and hosted connector implementation were not verified.

Mitigation: Review and verify the CLI and its installation behavior before allowing installation, including any automatic installation or synchronization of other skills.

Risk: Some potentially chargeable AI requests may be treated as reads by the skill's safety guidance.

Mitigation: Before submitting content, confirm the exact payload and obtain clear approval for potential generation charges.

## Reference(s):

- [Baidu Qianfan homepage](https://qianfan.cloud.baidu.com)
- [Baidu Qianfan API documentation](https://cloud.baidu.com/doc/qianfan-api/s/3m7of64lb)
- [OOMOL oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Files, Images, Embeddings, Video task results]

**Output Format:** [JSON action responses and agent-readable text; some actions return generated or extracted media and file data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response contents depend on the selected Qianfan action.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
