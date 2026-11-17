## Description:

NewsCatcher (newscatcherapi.com). Use this skill for ANY NewsCatcher request — searching and reading data. Whenever a task involves NewsCatcher, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search NewsCatcher's global news index, retrieve recent headlines, list indexed sources, and check subscription allowance through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance directs users to run a downloaded CLI installer, while the installer and runtime have not been verified.

Mitigation: Review setup first; use a verified, pinned CLI installation and require approval before running downloaded installers.

Risk: NewsCatcher access through the connected OOMOL account may consume credits.

Mitigation: Check the subscription allowance and monitor account usage before making repeated requests.

## Reference(s):

- [NewsCatcher API documentation](https://www.newscatcherapi.com/docs/news-api/api-reference/overview)
- [NewsCatcher homepage](https://www.newscatcherapi.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [News search results, headlines, source listings, or subscription details returned as JSON and summarized in text as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [NewsCatcher results may include source and publication details.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
