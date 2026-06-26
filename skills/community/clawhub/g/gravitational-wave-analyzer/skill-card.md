## Description: <br>
Fetches public LIGO/Virgo/KAGRA events from GWOSC, downloads detector strain data, runs signal analysis, classifies merger types, and produces plots and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yash-kavaiya](https://clawhub.ai/user/yash-kavaiya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, educators, and technical users use this skill to query public GWOSC catalogs, analyze detector strain for gravitational wave events, classify BBH/BNS/NSBH mergers, and generate plots, JSON summaries, and text reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads public data from GWOSC and may fail or return incomplete results if the network service is unavailable or an event/catalog input is invalid. <br>
Mitigation: Run with network access only when needed, confirm event and catalog inputs, and review generated summaries against GWOSC metadata. <br>
Risk: The skill writes plots, JSON summaries, and text reports to a local directory. <br>
Mitigation: Use a fresh Python environment and a dedicated output directory, then inspect generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [GWOSC](https://gwosc.org/) <br>
- [ClawHub Release Page](https://clawhub.ai/yash-kavaiya/gravitational-wave-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and shell commands; generated artifacts can include PNG plots, JSON summaries, and text reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes user-directed analysis outputs to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
