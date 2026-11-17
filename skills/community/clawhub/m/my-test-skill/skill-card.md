## Description:

Intelligent code security scanner with hybrid local-cloud detection that fingerprints packages, runs static behavioral analysis, and consults cloud threat intelligence for confidence scoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinxiaotian1](https://clawhub.ai/user/jinxiaotian1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to vet third-party code packages before installation by producing security scores, behavior tags, and install guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends source-derived evidence to NetEase Yidun cloud analysis by default.

Mitigation: For private repositories, proprietary packages, or code that may contain secrets, set YIDUN_SKILL_SEC_CLOUD=false before use or avoid the skill until cloud submission is opt-in.

Risk: Documentation does not reliably prove that extracted snippets cannot include sensitive material.

Mitigation: Review scanner output and payload handling before using the skill on sensitive code, and prefer test packages or local-only mode until stronger redaction and payload review are available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinxiaotian1/skills/my-test-skill)
- [Publisher profile](https://clawhub.ai/user/jinxiaotian1)
- [ClawHub ecosystem](https://clawhub.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown scan reports with scores, behavior tags, and suggested install decisions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and openssl; cloud threat intelligence is enabled by default and can be disabled with YIDUN_SKILL_SEC_CLOUD=false.]

## Skill Version(s):

0.0.1 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
