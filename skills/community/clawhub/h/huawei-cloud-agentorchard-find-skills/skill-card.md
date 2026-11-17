## Description:

Searches Huawei Cloud AI Gallery for skills, returns matching or popular listings, and directs users to review and subscribe to selected skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users can search Huawei Cloud AI Gallery with natural-language keywords, browse popular skills, and open a candidate's detail page before subscribing through the gallery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested skills and the live gallery service were outside this artifact review.

Mitigation: Review each candidate's details and contents before installing or relying on it.

Risk: Generic skill-finding requests can still produce Huawei-specific AI Gallery results.

Mitigation: Use focused keywords and confirm that the candidate is from the intended catalog.

## Reference(s):

- [Clawhub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-agentorchard-find-skills)
- [Publisher profile](https://clawhub.ai/user/huaweicloudskill)
- [Huawei Cloud AI Gallery skill search API](https://devdata.huaweicloud.com/rest/aiasset/user_system/v1/aihub/contents)
- [Environment requirements and installation guide](artifact/references/cli-installation-guide.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)
- [Verification methods](artifact/references/verification-method.md)
- [Acceptance criteria](artifact/references/acceptance-criteria.md)
- [IAM policy notes](artifact/references/iam-policies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, URLs]

**Output Format:** [Natural-language search results with skill names, descriptions, and detail links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the current public catalog; the user reviews and subscribes to selected skills on the gallery site.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
