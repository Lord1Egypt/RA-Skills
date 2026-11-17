## Description:

Provides guidance for operating Huawei Cloud Graph Database GES from a terminal, including Cypher and GQL queries, schema management, graph edits, and graph data import and export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to query and manage Huawei Cloud GES graph instances, edit graph data, and run asynchronous imports or exports using Python or Node.js.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This version may expose cloud credentials and graph data through insecure connections.

Mitigation: Keep it away from production credentials and important graphs until secure transport is fixed; use narrowly scoped credentials and disposable test data.

Risk: Destructive-operation safeguards and OBS dry-run handling need review; the verification example can modify an existing v1 node, and live cloud behavior was not tested.

Mitigation: Use disposable graphs, inspect verification steps before running them, and restrict storage bucket access. Keep production use on hold until the documented issues are fixed.

## Reference(s):

- [Cypher and GQL usage guide](references/cypher-gql-guide.md)
- [CLI and runtime installation guide](references/cli-installation-guide.md)
- [IAM permission policies](references/iam-policies.md)
- [Authentication guide](references/user-guide-authentication.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Chaining protocol](references/chaining-protocol.md)
- [Huawei GES graph data format documentation](https://support.huaweicloud.com/usermanual-ges/ges_01_0153.html)
- [Huawei GES business API access guide](https://support.huaweicloud.com/api-ges/ges_03_0112.html)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON query results or asynchronous job IDs, with Markdown guidance and Python or Node.js examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operations may return asynchronous job IDs for long queries and graph imports or exports.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
