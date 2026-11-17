## Description:

Helps agents summarize public js.design project and share pages, including page lists, component annotations, and design resource links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and agents use this skill to inspect public js.design project or share pages and produce concise summaries of pages, updates, components, annotations, and resource links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide private or restricted design content to a public-page summarization workflow.

Mitigation: Use only links and content the user is authorized to inspect, and avoid private team content unless organizational policy permits that use.

Risk: Summaries of dynamically loaded public pages may be incomplete if the page has not finished loading or is accessed too frequently.

Mitigation: Wait for page content to load before extracting fields and apply reasonable frequency controls for repeated access.

## Reference(s):

- [js.design](https://js.design/)
- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/js-design)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries with extracted fields and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should be limited to publicly accessible content and may include page names, update times, owners if displayed, component measurements, color values, annotations, and resource links.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
