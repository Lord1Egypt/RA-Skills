## Description: <br>
Scans Node.js, Python, Go, and Java projects for common memory leak patterns and guides optional local Node.js heap-diff confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect application source code for likely memory leak patterns, prioritize findings by severity, and get concrete cleanup guidance. Node.js users can also run local heap-diff checks to confirm whether a suspected leak grows under load. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad scans can inspect repository content outside the intended review scope. <br>
Mitigation: Run scans only on repositories or directories the user intends to inspect. <br>
Risk: Optional heap/profiler examples can create local load, background processes, and profiler files. <br>
Mitigation: Run runtime confirmation only in a local or test environment against harmless endpoints, then clean up background Node.js, profiler, and load-test artifacts. <br>
Risk: Static pattern matching can produce false positives or incomplete fixes. <br>
Mitigation: Review each finding and proposed code change before applying fixes or enforcing CI thresholds. <br>


## Reference(s): <br>
- [Phy Memory Leak Detector on ClawHub](https://clawhub.ai/PHY041/phy-memory-leak-detector) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports static findings with file, line, severity, explanation, and suggested fix; optional Node.js heap-diff guidance may generate local profiler output.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
