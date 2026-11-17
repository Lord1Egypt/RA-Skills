## Description:

Searches Kongfz auction listings for Ankang-related books and documents using the fixed keywords Ankang, Lai Lu Tang, and Xing'an Prefecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobemsk](https://clawhub.ai/user/tobemsk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Kongfz auction pages for Ankang-region literature, books, and historical-document listings, then summarize and prioritize relevant results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates Kongfz pages through xbrowser.

Mitigation: Use an isolated, logged-out browser profile and review browser actions before using the skill with accounts or sensitive sessions.

Risk: Weak keyword input handling may make command construction or page interaction unreliable.

Mitigation: Restrict keywords to the intended search terms or escape user-provided input before running the included script.

Risk: Installation guidance is imprecise.

Mitigation: Pin the installer and repository source before installation and review the installed files against the release evidence.

## Reference(s):

- [Kongfz Structure Reference](references/kongfz_structure.md)
- [Kongfz Actual Structure Update](references/kongfz_actual_structure.md)
- [Kongfz Skill Page](https://clawhub.ai/tobemsk/skills/kongfz-ankang-search)
- [Kongfz Advanced Auction Search](https://search.kongfz.com/adv.html?type=pm)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown search summaries with optional shell command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries classify auction results by relevance and may include title, location, price, time remaining, and listing links when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
