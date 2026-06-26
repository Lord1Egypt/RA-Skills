## Description: <br>
Operate Hemlane using HAR-derived GraphQL patterns and browser session artifacts for analyzing Hemlane HAR files, extracting GraphQL operations, documenting mutations and queries, and performing or reconstructing workflows such as referrals, tenant replies, work orders, transactions, requests, and maintenance updates from saved browser captures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[earlvanze](https://clawhub.ai/user/earlvanze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and authorized property-operations engineers use this skill to inspect Hemlane browser captures, rebuild GraphQL calls, and run MCP or CLI workflows for tenant messaging, maintenance, work orders, referrals, financials, rent roll, and lease-related tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture live browser session credentials and expose them through local files or terminal output. <br>
Mitigation: Install only in a controlled environment for an authorized Hemlane account, store auth artifacts ephemerally, avoid shared logs, and keep cookies, CSRF tokens, bearer tokens, and session identifiers out of committed files. <br>
Risk: Write workflows can create real Hemlane side effects, including tenant messages, referrals, maintenance comments, lease creation, and e-sign packet creation. <br>
Mitigation: Prefer read-only tools and dry runs first, verify target IDs and payloads before submission, and enable write tools only for an authorized operator who understands the caller gate and production impact. <br>
Risk: HAR-derived GraphQL operations may become stale or may not match a current Hemlane session. <br>
Mitigation: Refresh captures when behavior changes, regenerate the operation catalog from current authorized traffic, and validate reconstructed requests before live replay. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/earlvanze/hemlane) <br>
- [README.md](README.md) <br>
- [HAR summary](references/har-summary.md) <br>
- [GraphQL operations](references/graphql-operations.md) <br>
- [Operation catalog](references/operation-catalog.json) <br>
- [Runbooks](references/runbooks.md) <br>
- [Replay scaffold](references/replay-scaffold.md) <br>
- [Financials HAR summary](references/financials-har-summary.md) <br>
- [Rent roll integration](references/rent-roll-integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON MCP responses, Python scripts, shell commands, and configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime Hemlane credentials are supplied through environment variables or local auth files; read tools return JSON-like results, while write tools can perform live Hemlane account actions when authorized.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
