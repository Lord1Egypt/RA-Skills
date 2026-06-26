## Description: <br>
Audits Go code for denial-of-service and resource-exhaustion patterns involving goroutines, channels, HTTP handlers, allocation, decoding, and panic recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhy0](https://clawhub.ai/user/yhy0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to review Go projects for denial-of-service and resource-exhaustion risks, including goroutine leaks, unbounded reads or allocations, channel deadlocks, decoder abuse, and panic handling gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to search through a selected Go repository, which can surface sensitive code paths or internal implementation details. <br>
Mitigation: Run the audit only against repositories the user intends to inspect, and review findings before sharing excerpts outside the project context. <br>
Risk: Pattern-based DoS checks can produce false positives when code has lifecycle controls, trusted inputs, or bounded resources that are not obvious from a grep match. <br>
Mitigation: Validate each candidate with source-to-sink tracing and confirm missing limits, timeouts, cancellation, or recovery before reporting it as a vulnerability. <br>


## Reference(s): <br>
- [Go DoS/Resource Exhaustion real-world cases](references/cases.md) <br>
- [ClawHub release page](https://clawhub.ai/yhy0/go-vuln-dos) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown audit guidance with checklists and inline grep commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code or hidden access is bundled.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
