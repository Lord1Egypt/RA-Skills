## Description: <br>
Intern Report generates structured internship daily reports, weekly reports, summaries, reflection notes, defense presentation outlines, and career-planning reflection templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, interns, and career-support users use this skill to turn internship activities into structured Chinese-language reports, weekly logs, summaries, reflections, defense outlines, and career-planning drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: scripts/script.sh stores command arguments in a local history.log file. <br>
Mitigation: Avoid passing secrets, private file paths, or sensitive personal data to scripts/script.sh. <br>
Risk: Generated internship reports include placeholders and generic writing guidance that may be incomplete or inaccurate if submitted without review. <br>
Mitigation: Review the generated text, replace placeholders, and verify details against the user's real internship record before submission. <br>


## Reference(s): <br>
- [Usage tips](artifact/tips.md) <br>
- [ClawHub skill listing](https://clawhub.ai/ckchzh/intern-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-like terminal text with structured report templates and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated templates contain placeholders that the user is expected to replace with internship-specific details.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
