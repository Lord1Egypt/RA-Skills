## Description:

Unified web search skill with fallback across Brave web_search, DuckDuckGo, and a claude.ai browser session, with automatic caching of search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to run web research through available search providers, falling back from Brave to DuckDuckGo and then to a claude.ai browser workflow when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, result summaries, and extracted insights are automatically saved under memory/research/, which can expose secrets, personal data, confidential research, or regulated information.

Mitigation: Avoid sensitive queries unless a no-cache mode, deletion or retention controls, and clear user confirmation are added before caching.

Risk: The claude.ai fallback can use a logged-in browser session and submit research prompts through that account.

Mitigation: Prefer Brave or DuckDuckGo for routine searches, require confirmation before the logged-in browser fallback, and disable the fallback where authenticated browser use is not acceptable.

Risk: External search results and summarized web content can be stale, manipulated, incomplete, or wrong.

Mitigation: Verify important claims against primary sources before relying on the generated research output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/mupeng-web-claude)
- [claude.ai browser endpoint](https://claude.ai/new)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline commands and cached search-result notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results may be saved under memory/research/.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
