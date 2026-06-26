## Description: <br>
Install the 5-package multi-chip software stack (vLLM, FlagTree, FlagGems, FlagCX, vllm-plugin-FL) inside a GPU container, with network mirror detection, dependency ordering, wheel selection, and per-package validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wbavon](https://clawhub.ai/user/wbavon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after GPU container setup to install and validate a multi-chip inference software stack in a running container. It helps select environment-specific package sources and produce a structured installation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill materially changes the target GPU container by installing packages, replacing triton, building remote code, and persisting environment settings. <br>
Mitigation: Run it only in a disposable or dedicated GPU container and keep a container snapshot or rebuild path available. <br>
Risk: The install flow clones repositories, uses package mirrors, and installs editable packages, which can introduce supply-chain integrity concerns. <br>
Mitigation: Review package sources and configured mirrors before execution when supply-chain integrity matters. <br>


## Reference(s): <br>
- [Network & Mirror Configuration](references/network-mirrors.md) <br>
- [Vendor Mappings for FlagCX](references/vendor-mappings.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wbavon/install-stack-flagos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and a final structured JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports package status, selected network mirrors, container environment details, gate result, and errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
