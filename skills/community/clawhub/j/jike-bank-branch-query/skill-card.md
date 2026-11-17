## Description:

Looks up bank branch names, branch routing codes, province and city details, and bank lists through JikeAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query bank branch routing information and bank lists from JikeAPI using a configured AppKey.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bank lookup queries and the AppKey are sent to the configured JikeAPI endpoint.

Mitigation: Install only if you trust JikeAPI with those queries and credentials.

Risk: Passing the AppKey with --key can expose it through shell history, process lists, or logs.

Mitigation: Prefer storing the AppKey in JIKE_BANK_BRANCH_QUERY_KEY or JIKE_APPKEY as an environment secret.

Risk: Overriding JIKE_API_BASE_URL can route credentials and lookup data to an unintended endpoint.

Mitigation: Do not set JIKE_API_BASE_URL unless the endpoint is fully trusted.

Risk: An exposed AppKey may continue to authorize requests.

Mitigation: Rotate the AppKey if it may have appeared in logs, process output, or shell history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-bank-branch-query)
- [JikeAPI homepage](https://www.jikeapi.cn/)
- [JikeAPI bank branch query endpoint](https://api.jikeapi.cn/v1/bank/branch/query)
- [Publisher profile](https://clawhub.ai/user/jikeapi-cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal tables or JSON, with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a JIKE_BANK_BRANCH_QUERY_KEY or JIKE_APPKEY environment secret.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
