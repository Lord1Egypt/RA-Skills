## Description: <br>
MONK-EYE Engine helps an agent generate forum-focused research queries and synthesize claimed forum intelligence into strategic reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[balkanblbn](https://clawhub.ai/user/balkanblbn) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to plan broad forum searches across regional communities and produce concise strategic research reports from the resulting findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports may overstate scan depth, completion, or evidence quality. <br>
Mitigation: Treat each report as untrusted unless it includes real, verifiable source URLs and supporting evidence. <br>
Risk: Hard-coded local paths can cause installation failures or dependency on files outside the bundled skill. <br>
Mitigation: Review paths before installing and prefer configurable paths that point to bundled files. <br>
Risk: Broad forum search behavior can produce noisy or unsupported conclusions. <br>
Mitigation: Require explicit source, language, and depth limits before relying on results. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text reports, plus JSON-formatted search query lists from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should be treated as untrusted unless they include real, verifiable source URLs and evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
