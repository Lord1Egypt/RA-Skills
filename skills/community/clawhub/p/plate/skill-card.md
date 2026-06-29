## Description: <br>
Plate reviews outward-facing prose before publication to flag identity leaks, infrastructure leaks, authorship disclosures, and writing-convention issues for user-approved cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and maintainers use Plate as a final review pass before publishing a blog post, social post, README section, PR or issue body, commit message, or release note. It reports each finding with a proposed replacement and waits for user confirmation before applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may flag AI-use or authorship disclosure lines that a workplace, publisher, or project requires to remain visible. <br>
Mitigation: Review every proposed deletion or rewrite before confirming changes. <br>
Risk: Automated prose cleanup can alter a user's wording or remove intentional examples such as local endpoints or private-network placeholders. <br>
Mitigation: Treat findings as recommendations, confirm ambiguous cases, and inspect the diff after approved edits. <br>


## Reference(s): <br>
- [Plate on ClawHub](https://clawhub.ai/solomonneas/plate) <br>
- [content-guard](https://github.com/solomonneas/content-guard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown findings table with proposed replacements, confirmation prompts, optional shell commands, and a diff after approved edits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Edits are proposed for review before application; ambiguous cases are flagged rather than silently changed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
