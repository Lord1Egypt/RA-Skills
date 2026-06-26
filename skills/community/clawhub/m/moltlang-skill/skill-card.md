## Description: <br>
Translates between English and MoltLang, a compact AI-agent language for reducing token usage in common operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasonlnheath](https://clawhub.ai/user/jasonlnheath) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to translate operational instructions between English and MoltLang, validate MoltLang snippets, list supported tokens, and estimate token savings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send user-provided text to a public MoltLang API. <br>
Mitigation: Avoid translating confidential or regulated content through the public API unless the operator and privacy practices are trusted. <br>
Risk: Local use depends on external MoltLang packages or repository code that is not bundled with the skill. <br>
Mitigation: Verify the package source and repository before installing or executing local code. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jasonlnheath/moltlang-skill) <br>
- [MoltLang API](https://moltlang.up.railway.app) <br>
- [MoltLang GitHub Repository](https://github.com/jasonlnheath/moltlang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with translated text, validation results, efficiency estimates, and optional install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use a public API or locally installed moltlang package depending on the selected workflow.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
