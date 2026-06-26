## Description: <br>
Generate publication-quality sequence logos for DNA or protein motifs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to generate and review motif logo representations from DNA or protein sequence inputs, including ASCII summaries or WebLogo command guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security guidance describes this as a lightweight local prototype with capability and documentation gaps. <br>
Mitigation: Verify the actual command-line help and run a small local test before relying on generated results. <br>
Risk: The skill can read sequence files and write output files in the local workspace. <br>
Mitigation: Run it in an isolated Python environment and keep input and output paths inside the workspace. <br>
Risk: WebLogo mode emits shell commands for a user to copy into a shell. <br>
Mitigation: Inspect generated commands before execution and invoke external tools only from trusted environments. <br>


## Reference(s): <br>
- [Motif Logo Generator on ClawHub](https://clawhub.ai/aipoch-ai/motif-logo-generator) <br>
- [WebLogo](https://weblogo.berkeley.edu/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Plain text or Markdown with command snippets; optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write an ASCII logo or WebLogo command plan to a user-specified output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
