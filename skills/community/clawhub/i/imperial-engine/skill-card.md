## Description: <br>
Imperial Engine is an OpenClaw stress-testing skill for generating extreme token usage and throughput in controlled test environments. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[fr33b1rd8979-max](https://clawhub.ai/user/fr33b1rd8979-max) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to stress-test OpenClaw token throughput, tool invocation volume, budget controls, rate limits, and monitoring in isolated non-production environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rapidly create very high token usage and provider costs. <br>
Mitigation: Run only in disposable test environments with hard provider spending limits, explicit invocation controls, active monitoring, and a tested stop path. <br>
Risk: Browser, shell, and memory behavior can expand tool output and persist large local artifacts. <br>
Mitigation: Disable shell and browser unless needed, isolate or turn off memory persistence, and avoid running with valuable local state. <br>
Risk: Global enablement could trigger the skill during normal agent use. <br>
Mitigation: Do not enable globally; install only for a bounded test session and disable or uninstall immediately after testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fr33b1rd8979-max/imperial-engine) <br>
- [Publisher profile](https://clawhub.ai/user/fr33b1rd8979-max) <br>
- [README](artifact/README.md) <br>
- [Example configuration](artifact/config.example.yml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce high-volume LLM, browser, shell, and memory outputs when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
