## Description: <br>
Provides openEuler-specific RPM packaging guidance for spec files, package splitting, changelog entries, macros, review checks, and upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weidongkl](https://clawhub.ai/user/weidongkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and packaging engineers use this skill when creating, modifying, reviewing, or upgrading openEuler RPM specs that need openEuler-specific package splits, changelog format, macros, and review checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destructive-looking command examples may remove files if adapted outside the intended RPM buildroot context. <br>
Mitigation: Run packaging snippets only in an RPM build environment, verify variables such as RPM_BUILD_ROOT before execution, and review generated spec changes before use. <br>
Risk: openEuler packaging rules can diverge from generic RPM conventions. <br>
Mitigation: Cross-check official openEuler policy when exact compliance matters, especially for changelog format, package splitting, and openEuler-specific macros. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weidongkl/openeuler-rpm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with RPM spec snippets and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the rpm skill for baseline RPM packaging guidance.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata; artifact frontmatter reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
