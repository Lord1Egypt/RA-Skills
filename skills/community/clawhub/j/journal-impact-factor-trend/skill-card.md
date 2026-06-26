## Description: <br>
Show journal impact factor and quartile trends over 5 years. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and agents use this skill to summarize recent impact-factor and quartile movement for one journal or a list of journals. It is suited to bounded evidence-insight tasks where assumptions, inputs, and validation needs should be explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Impact-factor or quartile results may be incomplete, stale, or unsuitable as authoritative research or business evidence. <br>
Mitigation: Verify journal metrics against an authoritative source before using the output for research, publication, or business decisions. <br>
Risk: The local script reads journal-name files and prints or saves output in the workspace. <br>
Mitigation: Run without elevated privileges and provide only intended journal-name files from the working directory. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/journal-impact-factor-trend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with optional plain-text trend table output from the Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports a single journal name or a journal-list file; defaults to a 5-year analysis window.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
