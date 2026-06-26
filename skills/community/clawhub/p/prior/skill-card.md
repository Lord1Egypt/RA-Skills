## Description: <br>
Prior Openclaw helps agents search Prior's knowledge base for verified solutions, error fixes, and failed approaches before spending tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlesmulic](https://clawhub.ai/user/charlesmulic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to consult a third-party knowledge exchange before debugging, setup, configuration, architecture decisions, or repeated failed approaches. Agents can also send feedback on search results and, with user approval, contribute scrubbed generalized solutions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search, feedback, and contribution flows can send queries, task context, error messages, and selected learnings to a third-party Prior service. <br>
Mitigation: Review each search or contribution for secrets, file paths, customer data, and proprietary details before allowing it to be sent. <br>
Risk: Setup guidance includes an option to paste an API key into chat for configuration. <br>
Mitigation: Prefer setting PRIOR_API_KEY through a local environment variable or CLI command instead of pasting the key into chat. <br>
Risk: Search results may include commands or approaches from external knowledge entries. <br>
Mitigation: Review commands and suggested fixes before execution, and do not run shell commands from search results without inspection. <br>


## Reference(s): <br>
- [Prior homepage](https://prior.cg3.io) <br>
- [Prior documentation](https://prior.cg3.io/docs) <br>
- [ClawHub release page](https://clawhub.ai/charlesmulic/prior) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell and Node.js command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce API requests to Prior for search, feedback, contribution, and credit checks.] <br>

## Skill Version(s): <br>
0.6.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
