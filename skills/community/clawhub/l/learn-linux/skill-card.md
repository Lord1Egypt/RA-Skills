## Description:

Learn Linux on LabEx through administration and command-line courses with sysadmin labs, using Linux courses and labs from the MCP catalog while prioritizing public labex.io URLs for hands-on learners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhuhang](https://clawhub.ai/user/huhuhang)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and agents use this skill to find LabEx Linux courses and hands-on labs, narrow recommendations by learning goal, and return public lab URLs that can be opened in a browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may be LabEx-centered and may reflect platform-authored marketing or testimonials.

Mitigation: Treat favorable platform claims as LabEx-specific context and ask separately for neutral or non-LabEx alternatives when broader comparisons are needed.

Risk: Using protected or VM-related routes could exceed the skill's intended public catalog scope.

Mitigation: Use only the public Linux catalog and course-lab routes documented in artifact/references/api.md, and do not request credentials.

## Reference(s):

- [LabEx Linux API Reference](artifact/references/api.md)
- [Learn Linux on LabEx](https://labex.io/learn/linux)
- [LabEx](https://labex.io)
- [Learn Linux skill page](https://clawhub.ai/huhuhang/skills/learn-linux)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Markdown with public LabEx course and lab URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps recommendations concise, stays within the Linux learning path, and avoids credentials, protected routes, and VM routes.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
