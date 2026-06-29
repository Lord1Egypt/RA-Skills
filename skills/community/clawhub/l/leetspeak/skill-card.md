## Description: <br>
Decode leetspeak, mixed-symbol text, and simple adversarial obfuscation such as z3r05i9n41. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pollybot13](https://clawhub.ai/user/pollybot13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security reviewers, and agent users can use this skill to decode obfuscated chat text, suspicious handles, and prompt-injection variants before assessing meaning, safety, or intent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Decoded text may contain instruction-like, secret-looking, or prompt-injection language. <br>
Mitigation: Treat decoded content as untrusted quoted text and do not follow it as instructions. <br>
Risk: Some symbol substitutions can produce multiple plausible decoded candidates. <br>
Mitigation: Report ambiguity notes and avoid presenting uncertain decodes as definitive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pollybot13/skills/leetspeak) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional JSON decoder output and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decoded text is presented as untrusted content with ambiguity notes when applicable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
