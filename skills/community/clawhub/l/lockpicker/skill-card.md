## Description: <br>
Guides a user through capturing and analyzing a HAR file from their own logged-in browser session, extracting the minimum auth material needed, mapping the request chain behind an authorized website action, and turning that known-good browser workflow into a reusable local script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to reproduce a legitimate website action they can already perform manually by analyzing a clean HAR capture, isolating required session material and request stages, and building a narrow local replay script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HAR files and extracted cookies, CSRF tokens, or authorization headers can grant live account access. <br>
Mitigation: Keep these files local and private, store only the minimum needed material, avoid repositories and shared folders, and delete sensitive runtime files when finished. <br>
Risk: Replaying private web requests may violate service terms, trigger rate limits, or lock or challenge an account. <br>
Mitigation: Prefer official APIs or scoped tokens when available, test one item first, keep batches small, and stop when a service challenges or rejects requests. <br>
Risk: Private request workflows can change without notice, causing stale endpoints, query IDs, or auth material to fail. <br>
Mitigation: Refresh session material from the user's own browser session and compare failures against a new successful HAR instead of guessing or bypassing controls. <br>
Risk: The workflow could be misapplied outside the user's authorized action. <br>
Mitigation: Keep the scope limited to a workflow the user can already perform manually and do not brute-force endpoints, fuzz auth, bypass login, bypass MFA, bypass paywalls, or bypass rate limits. <br>


## Reference(s): <br>
- [Auth materials](references/auth-materials.md) <br>
- [Common web flows](references/common-web-flows.md) <br>
- [HAR capture checklist](references/har-capture-checklist.md) <br>
- [Request analysis patterns](references/request-analysis-patterns.md) <br>
- [Safety boundaries](references/safety-boundaries.md) <br>
- [ClawHub skill page](https://clawhub.ai/stanestane/lockpicker) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code scaffolds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local runtime auth files, HAR request summaries, JSON analysis outputs, and first-pass Python replay scripts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
