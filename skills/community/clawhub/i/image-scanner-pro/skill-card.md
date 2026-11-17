## Description:

Scans image folders and uses Gemini 2.0 Flash to analyze and categorize photos by photography attributes such as composition, lighting, mood, and style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrxolin](https://clawhub.ai/user/mrxolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, photographers, and content teams use this skill to batch scan image folders, classify photo content, and produce structured analysis reports for organizing or reviewing photo collections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected image files may be sent to Google's Gemini service for visual analysis.

Mitigation: Use the skill only on images appropriate for external API processing, avoid private or regulated image folders, and confirm data handling requirements before scanning.

Risk: Providing an API key on the command line can expose it through shell history or process listings.

Mitigation: Prefer the GEMINI_API_KEY environment variable over the --api-key option.

Risk: The dependency lockfile may need review before sensitive use.

Mitigation: Review or update package-lock.json and dependencies before using the skill in a sensitive environment.

## Reference(s):

- [Image Scanner Pro on ClawHub](https://clawhub.ai/mrxolin/skills/image-scanner-pro)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command examples and optional JSON report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report summarizes scanned files, image metadata, style and subject counts, and per-image analysis when a Gemini API key is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
