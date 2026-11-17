## Description:

Fetches Hugging Face trending resources from the public HF-Mirror API and generates a structured Chinese Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddongcui](https://clawhub.ai/user/ddongcui)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users tracking Hugging Face ecosystem activity use this skill to fetch public HF-Mirror trending data and summarize popular models, datasets, and Spaces in Chinese Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Markdown includes text from public HF-Mirror data and may contain misleading names, links, or embedded instructions.

Mitigation: Treat the report as untrusted public web data, avoid following embedded links or instructions automatically, and review it before sharing or acting on it.

Risk: Running the fetch mode writes a Markdown report to disk.

Mitigation: Run the script with an explicit output path in a normal workspace.

## Reference(s):

- [HF-Mirror Trending API](https://hf-mirror.com/api/trending)
- [ClawHub Skill Page](https://clawhub.ai/ddongcui/skills/hfmirror-trending)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Chinese Markdown report with tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write the generated report to an explicit Markdown output path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
