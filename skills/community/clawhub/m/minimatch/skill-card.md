## Description: <br>
Use minimatch, a glob pattern matching library, for file path matching with patterns such as *.js and **/*.ts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need an agent to recommend minimatch usage for glob-based file path matching, filtering file lists, escaping patterns, or generating regular expressions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using untrusted user text directly as minimatch patterns can expose applications to regular expression denial-of-service or unintended matching behavior. <br>
Mitigation: Treat user text as data, not as a glob pattern; validate patterns against an allowlist or escape literal input before matching. <br>
Risk: Production projects can receive behavior or security changes if the minimatch dependency is left floating. <br>
Mitigation: Pin or lock the npm dependency version and review release notes before upgrading. <br>
Risk: Regular expressions generated after aggressive level 2 optimization may not match strings that were not processed the same way. <br>
Mitigation: Prefer Minimatch.match() for optimized matching, or ensure paths are processed consistently before using a generated RegExp. <br>


## Reference(s): <br>
- [minimatch ClawHub release page](https://clawhub.ai/openlark/minimatch) <br>
- [minimatch Optimization Levels](references/optimization.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable artifact is produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
