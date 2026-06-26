## Description: <br>
Pressure-tests product, internal-tool, or OSS concepts through a Working Backwards PRFAQ gauntlet before committing to a spec, producing a binary pass/fail verdict and, on pass, a concept brief for brainstorm-beagle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product builders, internal-tool teams, and OSS maintainers use this skill to test whether a concept has a concrete customer, real stakes, and defensible answers before moving into specification work. It guides the user through Ignition, Press Release, Customer FAQ, Internal FAQ, and Verdict stages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may scan project documents through its analysis companion and create or update files under .beagle/concepts/<slug>/. <br>
Mitigation: Review the intended workspace scope before running it, especially when project documents contain sensitive customer, market, or strategy information. <br>
Risk: The workflow can invoke outbound web research after distilling a concept-specific research question. <br>
Mitigation: Avoid including confidential details in the concept or review the companion research behavior before using it in a sensitive workspace. <br>


## Reference(s): <br>
- [PRFAQ Document Template](references/prfaq-template.md) <br>
- [Companion Invocation Contract](references/companion-contract.md) <br>
- [Stage 2: Press Release](references/press-release.md) <br>
- [Stage 3: Customer FAQ](references/customer-faq.md) <br>
- [Stage 4: Internal FAQ](references/internal-faq.md) <br>
- [Stage 5: Verdict, Brief, Fail Feedback](references/verdict.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Analysis, Guidance] <br>
**Output Format:** [Markdown files and concise conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes PRFAQ artifacts under .beagle/concepts/<slug>/; on pass writes brief.md, and on fail writes targeted verdict feedback without a brief.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
