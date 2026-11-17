## Description:

HWPX 문서(.hwpx 파일)를 생성, 읽기, 편집, 템플릿 치환하는 스킬. 한글 HWPX 포맷을 다루며 양식 기반 템플릿 치환 워크플로우를 제공합니다.

This skill is ready for commercial/non-commercial use.

## Publisher:

[withakiss](https://clawhub.ai/user/withakiss)

### License/Terms of Use:

MIT

## Use Case:

Developers and document-automation users can use this skill to analyze HWPX templates, replace placeholders from mapping data, and create edited .hwpx files for Korean document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance references missing runtime files and dependency instructions.

Mitigation: Treat the package as incomplete until the publisher provides the missing install.sh or requirements.txt instructions and confirms the supported runtime setup.

Risk: The optional python-hwpx dependency is described without a canonical source or pinned version.

Mitigation: Install python-hwpx only from a verified source with a pinned version or commit and publisher-provided verification details.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/withakiss/skills/gonggong-hwpxskills-main)
- [Publisher Profile](https://clawhub.ai/user/withakiss)
- [Project Homepage](https://github.com/withakiss/hwpx_my)
- [Release v0.1.0](https://github.com/withakiss/hwpx_my/releases/tag/v0.1.0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands and JSON mapping examples; generated HWPX files may be written to an outputs directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Works with local HWPX template paths and mapping JSON inputs.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
