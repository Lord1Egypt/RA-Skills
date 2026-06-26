## Description: <br>
Massive (Polygon.io) (massive.com). Use this skill for ANY Massive (Polygon.io) request -- searching and reading data. Whenever a task involves Massive (Polygon.io), use this skill instead of calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Polygon.io market data through an OOMOL-connected account, including ticker lookup, ticker details, exchange discovery, ticker type discovery, market status, aggregate bars, and previous-day OHLC bars. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected Polygon.io account and may consume account credits. <br>
Mitigation: Run connector actions only for intentional market-data requests, and approve setup, connection repair, or billing steps only when the user explicitly wants that account access used. <br>
Risk: Access can fail when the oo CLI is missing, authentication is expired, the Polygon.io connection is not ready, or account credits are insufficient. <br>
Mitigation: Follow the documented first-time setup path only after a matching command failure, and avoid repeating login or connection steps proactively. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-polygon-io) <br>
- [Massive (Polygon.io) homepage](https://massive.com/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides schema-first connector calls and returns read-only market data responses through the oo CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
