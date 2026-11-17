## Description:

Supports querying digits of pi starting at a specified position and finding where a given digit sequence appears in pi, using the Jike API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to answer pi digit lookup requests, including retrieving digits from a position and locating short digit sequences in pi.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The configured Jike AppKey can be sent to an unexpected endpoint if JIKE_API_BASE_URL is controlled by an untrusted user or wrapper.

Mitigation: Run the skill only in environments where untrusted users cannot set JIKE_API_BASE_URL, and rotate the key if it may have been used with an unexpected API base URL.

Risk: Pi lookup requests and the configured AppKey are sent to the Jike API.

Mitigation: Install and use the skill only when sending those requests and credentials to Jike is acceptable for the deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-pi-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Pi query API endpoint](https://api.jikeapi.cn/v1/pi/find_number)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON returned by a Python command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Jike AppKey via JIKE_PI_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
