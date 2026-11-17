## Description:

Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, or automating any browser task.

This skill is ready for commercial/non-commercial use.

## Publisher:

[handongpu16](https://clawhub.ai/user/handongpu16)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to automate browser workflows such as navigating pages, filling forms, clicking controls, capturing screenshots, and extracting page data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform broad browser actions, including clicks, form entry, downloads, tab changes, and dialog handling.

Mitigation: Run it in a sandboxed or low-privilege environment and require explicit confirmation before downloads, form submissions, payments, account changes, or handling private page content.

Risk: Installation requires external executable components and a Chromium download.

Mitigation: Prefer a pinned, verified release with documented source and Chromium provenance before using it in sensitive workflows.

Risk: Browser element indices become stale after navigation, form submissions, or dynamic page updates.

Mitigation: Refresh the page snapshot after page changes and act only on current element indices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/handongpu16/skills/my-browser-bot)
- [ClawHub publisher profile](https://clawhub.ai/user/handongpu16)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and browser automation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output may include page snapshots, element indices, screenshots, temporary file paths, page text, HTML, URLs, titles, values, attributes, counts, boxes, styles, and task-completion status.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
