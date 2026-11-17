## Description:

Panda Data Skill wraps PandaAI financial data APIs as LLM-callable tools for querying equities, indices, futures, market reference data, financial reports, trading calendars, and related factors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandaai-tech](https://clawhub.ai/user/pandaai-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to help agents call PandaAI market-data tools for financial data lookup, including price history, fundamentals, index data, futures data, trading calendars, and formatted query results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires PandaAI account credentials, and setup guidance can lead users to expose a username and password to an assistant or local .env file.

Mitigation: Do not paste credentials into chat; prefer securely set environment variables or a restricted local secret store and keep .env files out of unrelated projects.

Risk: Runtime packages that handle credentials are external and unpinned in the artifact setup guidance.

Mitigation: Install the skill in a dedicated virtual environment, pin and review panda_data and panda-data-tools before use, and update only after review.

## Reference(s):

- [Panda Data Skill on ClawHub](https://clawhub.ai/pandaai-tech/skills/panda-data-skill)
- [Panda Data Tools on PyPI](https://pypi.org/project/panda-data-tools/)
- [PandaAI website](https://www.pandaai.online)
- [Installation guide](INSTALL_GUIDE.md)
- [API reference](api_reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples; tool calls return formatted table strings or JSON error text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PandaAI credentials and the external panda_data and panda-data-tools Python packages at runtime.]

## Skill Version(s):

4.0.0 (source: release evidence; artifact frontmatter says 3.0.0 and artifact README/CHANGELOG mention 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
