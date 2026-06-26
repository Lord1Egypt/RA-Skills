## Description: <br>
Integrates with Google Keep through nodriver and Chrome so agents can create, read, update, archive, and delete notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RicardoReichert](https://clawhub.ai/user/RicardoReichert) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent manage Google Keep notes through a local Chrome session, including listing, reading, creating, updating, archiving, and deleting notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Google session material and can read or modify Google Keep notes through a persistent logged-in browser session. <br>
Mitigation: Install only when persistent agent access to the Google Keep account is acceptable, and prefer a dedicated Google account or Chrome profile. <br>
Risk: Update, archive, and delete actions can affect the wrong note if a title is ambiguous or the requested operation is misunderstood. <br>
Mitigation: Confirm exact note titles before destructive or replacing actions, and read the note before updating content. <br>
Risk: Saved Chrome profile and cookie data under ~/.config/google-keep-skill can expose account access if mishandled. <br>
Mitigation: Protect the session directory, never read or transmit its contents, and run logout when saved access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RicardoReichert/google-keep-skill) <br>
- [Google Keep](https://keep.google.com/) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the underlying CLI returns structured JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Chrome session and user-confirmed Google Keep account access.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter 1.0.0 and pyproject.toml 0.3.0 differ) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
