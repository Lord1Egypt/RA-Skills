## Description: <br>
Privacy-first interactive AI persona workshop for creating and maintaining local persona files with preset styles, dual-mode behavior, voice mapping, and consistency checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sallyface0](https://clawhub.ai/user/sallyface0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to design, customize, and maintain local AI persona files such as SOUL.md, IDENTITY.md, and AGENTS.md. It guides users through preset or custom persona choices, voice-personality mapping, and optional consistency checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad proactive activation can steer future assistant behavior before the user clearly opts in. <br>
Mitigation: Install only when a proactive persona-management assistant is desired, confirm intent before persona creation, and review the proposed persona content before allowing it to influence future sessions. <br>
Risk: Generated persona files may capture sensitive personal preferences or overwrite existing local persona settings. <br>
Mitigation: Confirm the exact file path, inspect the preview or diff before write, keep backups for overwrites, and avoid storing sensitive preferences unless they are intended to shape future assistant behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sallyface0/nora-persona-framework) <br>
- [README.md](artifact/README.md) <br>
- [PRIVACY.md](artifact/PRIVACY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance and proposed local Markdown files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes or updates local persona files only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.4.1 (source: server release evidence, SKILL.md frontmatter, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
