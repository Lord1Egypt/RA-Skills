## Description: <br>
Olares Dashboard (olares-cli dashboard) helps agents query Olares Dashboard Overview and Applications data from the command line, including runtime metrics, resource rankings, JSON envelopes, watch polling, windowed queries, and hardware capability gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olares](https://clawhub.ai/user/olares) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to inspect Olares Dashboard resource usage and health from `olares-cli`, including CPU, memory, disk, pods, network, fan, GPU, rankings, applications, and live polling output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan verdict is suspicious and reports high-impact maintainer-style guidance in the bundle. <br>
Mitigation: Install only when you need this Olares Dashboard workflow, trust the publisher and local repo context, and review commands before use. <br>
Risk: Dashboard commands can query active Olares profile data and `--user` cross-user queries require platform-admin privileges. <br>
Mitigation: Confirm the active Olares profile and role before running commands, avoid `--user` unless explicitly needed, and handle 401/403 authentication errors by refreshing or reselecting the profile. <br>
Risk: Watch mode repeatedly polls upstream services and can add load or continue through transient failures. <br>
Mitigation: Use the CLI's recommended poll interval, set iteration or timeout limits when appropriate, and stop polling on hard-gated states such as `not_olares_one`. <br>


## Reference(s): <br>
- [Olares Dashboard on ClawHub](https://clawhub.ai/olares/olares-dashboard) <br>
- [dashboard overview](references/olares-dashboard-overview.md) <br>
- [dashboard --watch / windows / NDJSON contract](references/olares-dashboard-watch.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/NDJSON contract details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires `olares-cli`; dashboard JSON output uses stable `kind`, `meta`, `items`, and `sections` envelopes.] <br>

## Skill Version(s): <br>
4.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
