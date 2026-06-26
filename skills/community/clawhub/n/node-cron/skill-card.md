## Description: <br>
Node.js cron job scheduling guidance for using the `cron` npm package to create recurring tasks, validate cron expressions, and manage timed callbacks in Node.js or TypeScript projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to schedule recurring Node.js tasks, choose correct six-field cron expressions, and manage CronJob behavior in Node.js or TypeScript projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled callbacks can run with broader side effects than intended if production jobs are copied without review. <br>
Mitigation: Keep callbacks narrowly scoped, add error handling, and ensure jobs can be stopped or disabled before deployment. <br>
Risk: The generated examples depend on the external `cron` npm package. <br>
Mitigation: Verify the dependency, pin versions, and keep the package updated according to the project's dependency policy. <br>


## Reference(s): <br>
- [Node Cron Full API Reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no credentials, hidden commands, or data access are required by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
