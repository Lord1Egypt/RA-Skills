## Description:

Find and recommend free Linux Journey lessons on LabEx when the user wants to learn Linux fundamentals, Linux basics, command line concepts, filesystems, permissions, processes, networking, package management, shell usage, or beginner Linux skills through free lesson pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhuhang](https://clawhub.ai/user/huhuhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find a small set of relevant Linux Journey lesson pages for Linux fundamentals, command-line basics, filesystems, permissions, networking, package management, and related beginner Linux topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The refresh script can make outbound requests to a caller-supplied URL.

Mitigation: Refresh the lesson index only with the default LabEx sitemap or another reviewed trusted source; do not let untrusted prompts choose refresh arguments.

Risk: The refresh script can write generated Markdown to a caller-supplied output path.

Mitigation: Run refreshes in a controlled workspace and write only to the intended references/lessons.md destination.

Risk: Security evidence marks the release suspicious pending review of the maintenance script behavior.

Mitigation: Review and scan the skill before installation, and use the skill primarily for reading the bundled lesson index and recommending public LabEx lesson URLs.

## Reference(s):

- [Linux Journey lesson index](references/lessons.md)
- [Linux Journey on LabEx](https://labex.io/linuxjourney)
- [LabEx](https://labex.io)
- [Linux Journey lessons sitemap](https://labex.io/linuxjourney-lessons-sitemap.xml)
- [ClawHub skill page](https://clawhub.ai/huhuhang/skills/linux-journey)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with public lesson URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short recommendations focused on one to three Linux Journey lessons, or a concise beginner progression when requested.]

## Skill Version(s):

1.0.1 (source: server release evidence, created 2026-03-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
