## Description:

Provides an MBTI personality-test service that lets an AI assistant guide a user through a test and present result analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to start an MBTI test, submit 1-5 answer scores, check progress, and calculate a final MBTI result through the XiaoBenYang service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the XiaoBenYang API key in a local plaintext .env file.

Mitigation: Use only trusted environments, avoid committing .env, restrict file permissions, and consider a secret store before deployment.

Risk: The artifact contains gaokao naming and configuration mismatches that may confuse reviewers or operators.

Mitigation: Review or fix the mismatched names and configuration before installing or publishing the skill.

Risk: The skill sends test-session data and scores to the XiaoBenYang API service.

Mitigation: Use the skill only if the deployment is allowed to rely on that third-party service and endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/mbit-test)
- [XiaoBenYang API key site](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown or text summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key; tool calls return success, raw, and message fields.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
