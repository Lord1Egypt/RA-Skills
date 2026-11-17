## Description:

Auto-generated skill for google-search tools via OneKey Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Google Custom Search queries through OneKey Gateway from CLI or Python workflows, returning configurable search results with pagination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation uses unpinned third-party npm and Python packages.

Mitigation: Install in an isolated environment, avoid global npm installation where possible, and pin and review dependencies before deployment.

Risk: The script can fall back to a shared built-in gateway key.

Mitigation: Provide a user-controlled DEEPNLP_ONEKEY_ROUTER_ACCESS key and do not rely on the demo fallback for normal use.

Risk: Search queries and JSON payload files are sent to an external gateway and search service.

Mitigation: Avoid sending sensitive, confidential, or regulated data in search queries or payload files.

## Reference(s):

- [ClawHub Google Search Skill](https://clawhub.ai/ai-hub-admin/skills/google-search-onekey-gateway)
- [OneKey MCP Router Documentation](https://www.deepnlp.org/doc/onekey_mcp_router)
- [OneKey Gateway Documentation](https://deepnlp.org/doc/onekey_agent_router)
- [OneKey Gateway Keys](https://www.deepnlp.org/workspace/keys)
- [Google Custom Search JSON API](https://www.googleapis.com/customsearch/v1)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Code, Configuration]

**Output Format:** [JSON search results and Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPNLP_ONEKEY_ROUTER_ACCESS for normal use; the artifact documents a demo key fallback.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
