## Description:

Exports JD.com product reviews from a product page into local Markdown and JSON files, using the user's logged-in Chrome session to collect reviewer names, dates, SKUs, review text, merchant replies, and usefulness counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatmind](https://clawhub.ai/user/fatmind)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and operators use this skill to collect JD.com product review data from a supplied product URL for product selection, review analysis, and local reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives a logged-in Chrome session on JD.com.

Mitigation: Install only when comfortable with that browser access, and prefer a dedicated browser profile for collection.

Risk: The release includes an obfuscated executable helper.

Mitigation: Review and scan the helper before installation, and run the skill only in an environment appropriate for suspicious third-party code.

Risk: Logged-in JD account identifiers can be passed through the local LLM classification path.

Mitigation: Keep the LLM endpoint local unless intentionally trusting another endpoint.

Risk: The skill writes fixed default filenames in the selected output directory.

Mitigation: Choose an output directory where overwriting reviews.md, data.md, or res.json would not matter.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fatmind/skills/jd-review-export)
- [webclaw3 browser automation dependency](https://clawhub.ai/fatmind/skills/webclaw3-browser-automation)

## Skill Output:

**Output Type(s):** [markdown, json, text]

**Output Format:** [Local Markdown tables, JSON metadata, and one-line stdout JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reviews.md, data.md, and res.json to the configured output directory; partial results are marked when the requested review count is not met.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
