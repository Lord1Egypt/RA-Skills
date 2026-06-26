## Description: <br>
Provides sem semantic-diff detection, install-on-first-use, and fallback patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when building or modifying agent skills that consume git diff output, so they can prefer sem semantic diffs when available and fall back to standard git diff patterns when it is not. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt installation of the third-party sem CLI when sem is not present. <br>
Mitigation: Approve sem CLI installation only if the Ataraxy-Labs source is trusted, or decline and use the standard git diff fallback. <br>
Risk: Broad triggers could activate the skill during unrelated git diff workflows. <br>
Mitigation: Invoke the skill explicitly or narrow triggers when accidental activation would be disruptive. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/athola/nm-leyline-sem-integration) <br>
- [Night Market leyline plugin](https://github.com/athola/claude-night-market/tree/master/plugins/leyline) <br>
- [sem project](https://github.com/Ataraxy-Labs/sem) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON schema examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose sem CLI installation or fall back to git diff output normalization.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
