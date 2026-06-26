## Description: <br>
Write solid PHP avoiding type juggling traps, array quirks, and common security pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill as PHP coding guidance for avoiding common language traps, security mistakes, and PHP 8+ compatibility issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PHP code can mishandle authentication, database access, file uploads, or input validation if the guidance is applied incorrectly. <br>
Mitigation: Review generated PHP code before deployment, with focused checks for prepared SQL statements, output escaping, CSRF tokens, upload validation, session handling, and strict comparisons. <br>
Risk: PHP loose comparison and array behavior can create subtle authorization or data-handling defects. <br>
Mitigation: Prefer strict comparisons, strict in-array checks, explicit key existence checks, and careful array merge behavior as described in the skill references. <br>


## Reference(s): <br>
- [PHP skill page](https://clawhub.ai/ivangdavila/php) <br>
- [PHP quick reference](artifact/SKILL.md) <br>
- [Type traps](artifact/types.md) <br>
- [Array traps](artifact/arrays.md) <br>
- [OOP traps](artifact/oop.md) <br>
- [String traps](artifact/strings.md) <br>
- [Error traps](artifact/errors.md) <br>
- [Security traps](artifact/security.md) <br>
- [PHP 8+ traps](artifact/modern.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code] <br>
**Output Format:** [Markdown guidance with inline PHP examples and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PHP when commands or examples need local execution; the skill itself is markdown-only.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
