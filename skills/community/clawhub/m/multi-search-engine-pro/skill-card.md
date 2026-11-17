## Description:

Build auditable search URLs across Chinese and global engines with region/language filters, advanced operators, time scopes, privacy-first options, compare mode, and no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research agents use this skill to construct and compare search URLs across global, Chinese, privacy-oriented, and knowledge engines before deciding which results to open.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening generated search URLs can send query terms to third-party search engines that may log them.

Mitigation: Review generated URLs before opening them and avoid sensitive personal, credential, or confidential-business queries unless an appropriate privacy engine is intentionally selected.

Risk: Search engine URL parameters and regional availability can change over time.

Mitigation: Periodically smoke test important engines and time, language, region, and SafeSearch mappings before relying on generated links.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/multi-search-engine-pro)
- [ClawHub Homepage Metadata](https://clawhub.com/skills/multi-search-engine)
- [International Search Guide](references/international-search.md)
- [Search Operator Cheatsheet](resources/search-operator-cheatsheet.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Text, Markdown, or JSON search URL entries with optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API keys required; generated URLs may be inspected before any network access.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
