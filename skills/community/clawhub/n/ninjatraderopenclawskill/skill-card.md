## Description: <br>
NinjaTrader 8 NinjaScript development reference: using directives, lifecycle, indicators, order mgmt, compile errors, deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmdeep](https://clawhub.ai/user/gmdeep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building NinjaTrader 8 NinjaScript strategies and indicators use this skill as a reference for C# using directives, lifecycle placement, indicator setup, order management, validation, and deployment checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Deployment examples include remote-copy commands to a specific SSH/SCP host and a local NinjaTrader path. <br>
Mitigation: Review all deployment commands before execution, replace the host and destination with an explicitly authorized target, and keep backups before overwriting strategy files. <br>
Risk: Generated or edited NinjaScript strategy code can affect trading behavior if deployed without review. <br>
Mitigation: Compile in the NinjaTrader 8 editor, address errors before enabling a strategy, and test on a chart or non-production setup before live use. <br>


## Reference(s): <br>
- [Source repository](https://github.com/GMDEEP/NinjatraderOpenClawSkill) <br>
- [ClawHub skill page](https://clawhub.ai/gmdeep/ninjatraderopenclawskill) <br>
- [Publisher profile](https://clawhub.ai/user/gmdeep) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with C# and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes checklists, reference tables, code templates, and deployment command examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
