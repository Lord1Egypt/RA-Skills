## Description:

Provides keyword search and random retrieval for Chinese xiehouyu using the Jike API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search for Chinese xiehouyu by keyword or retrieve a random xiehouyu for Chinese-language writing, explanation, or recommendation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A modified launch environment can redirect the API key and query text to another server.

Mitigation: Run the skill only in an environment you control and avoid setting JIKE_API_BASE_URL.

Risk: The Jike AppKey may be exposed if an untrusted process can alter the environment or observe full request URLs.

Mitigation: Use a dedicated API key, limit access to the execution environment, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-xiehouyu-query)
- [Jike API homepage](https://www.jikeapi.cn/)
- [Jike xiehouyu query endpoint](https://api.jikeapi.cn/v1/xiehouyu/query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Terminal table text by default, or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike API key provided through JIKE_XIEHOUYU_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
