## Description: <br>
Google Keep notes via gkeepapi. List, search, create, manage notes. Add items to notes. Supports authorization via OAuth 2.0 Token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PromptingPufferfish](https://clawhub.ai/user/PromptingPufferfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to list, search, read, create, and update Google Keep notes through a local CLI wrapper. It is suited for personal note workflows where the user can authorize Google Keep access and confirm note IDs before changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to Google Keep notes and uses a manual Google token extraction flow. <br>
Mitigation: Only install it when comfortable granting note access, treat ~/.config/gkeep/token.json and printed token output like passwords, and avoid sharing setup logs or screenshots. <br>
Risk: The skill can modify or trash notes through create, archive, delete, add, check, pin, and unpin actions. <br>
Mitigation: Confirm note IDs and requested actions before commands that delete, archive, add to, check, pin, or unpin notes. <br>
Risk: The security verdict is suspicious because of the authentication flow and note-modification capability. <br>
Mitigation: Remove or revoke the Google token if exposed and review the skill before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PromptingPufferfish/gkeep-notes) <br>
- [Google Embedded Setup](https://accounts.google.com/EmbeddedSetup) <br>
- [Google app passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a local Google Keep token file at ~/.config/gkeep/token.json.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
