## Description: <br>
Analyze test coverage gaps by comparing test files against source modules to identify untested code paths and critical functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jk625x](https://clawhub.ai/user/jk625x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to compare source modules with test files, identify untested exports and orphaned tests, and prioritize coverage gaps by risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on reading local source and test files and may use shell-based inspection. <br>
Mitigation: Review the proposed inspection commands and restrict execution to repositories where source and test files may be read. <br>
Risk: Coverage gap reports can miss behavior that is tested indirectly or recommend tests for intentionally untested internals. <br>
Mitigation: Validate the report against project testing policy and prioritize public APIs, data mutation paths, and error handling before acting on recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jk625x/ljkhlk) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown coverage gap report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sorted by risk level with source files, untested exports, and suggested test outlines.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
