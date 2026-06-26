## Description: <br>
Smart Scheduler classifies user requests as simple or complex, routes simple tasks quickly, and decomposes complex tasks through resource lookup and debate-style verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timo2026](https://clawhub.ai/user/timo2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route user tasks between fast direct handling and deeper multi-step processing with local resources, installed skills, ClawHub-style skill lookup, and optional verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan says the skill under-discloses local service data sharing and persistent input logging. <br>
Mitigation: Review localhost service calls and JSONL statistics logging before deployment, and avoid sending secrets or sensitive business data unless logging is disabled or redacted. <br>
Risk: The security scan says the skill makes unsupported sandbox and network safety claims. <br>
Mitigation: Treat execution and network behavior as requiring independent review, and confirm contacted services and code execution boundaries before enabling automatic routing. <br>


## Reference(s): <br>
- [Smart Scheduler ClawHub listing](https://clawhub.ai/timo2026/openclaw-smart-scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, guidance, configuration] <br>
**Output Format:** [Structured Python results and human-readable text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task complexity, response text, latency, selected skill, subtasks, and summary statistics.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
