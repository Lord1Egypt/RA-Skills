## Description:

Generate structured agendas for mentor-student one-on-one meetings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Mentors, managers, educators, and career advisors use this skill to create structured one-on-one mentorship meeting agendas with timed sections, discussion prompts, optional topics, and follow-up tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output option can overwrite arbitrary writable files if given an unsafe path.

Mitigation: Run the skill without elevated privileges and pass only a safe workspace-relative output filename until output path validation and overwrite protection are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/mentorship-meeting-agenda)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Plain text agenda suitable for Markdown file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated agenda includes the student name, current date, career phase, timed discussion sections, prompts, optional topic list, and notes placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
