## Description: <br>
Jd Writer helps create and review job descriptions, including requirements, benefits, salary benchmarks, optimization suggestions, and inclusivity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams, recruiters, hiring managers, and developers use this skill to draft job descriptions, refine requirements and benefits, compare salary guidance, and check for discriminatory language before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An included auxiliary script logs user prompts to a local history file without clear disclosure. <br>
Mitigation: Prefer the documented Python JD workflow, avoid entering confidential hiring drafts or proprietary text into scripts/script.sh, and review or delete the local jd-writer history file if that script is used. <br>
Risk: Generated job descriptions, salary benchmarks, and legal references may be inaccurate or inappropriate for a specific role, location, or hiring policy. <br>
Mitigation: Have HR or legal reviewers verify generated content, salary guidance, and local hiring requirements before publication. <br>


## Reference(s): <br>
- [Jd Writer ClawHub release page](https://clawhub.ai/ckchzh/jd-writer) <br>
- [Publisher profile: ckchzh](https://clawhub.ai/user/ckchzh) <br>
- [JD-Writer tips and best practices](artifact/tips.md) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and plain text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local Python and shell workflows; no external dependencies documented.] <br>

## Skill Version(s): <br>
2.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
