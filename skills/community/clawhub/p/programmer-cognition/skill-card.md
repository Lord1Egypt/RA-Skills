## Description: <br>
Programmer Cognition adapts the SOUL five-rule method to software development through four-direction code review, debugging discipline, deployment checks, and CI-oriented self-verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofzhao](https://clawhub.ai/user/kingofzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to structure code review, debugging, deployment readiness checks, and confidence labeling for software changes. It is most useful when an agent needs a repeatable checklist for identifying unknowns, reviewing failure modes, and verifying changes through tests and human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can shape code review, debugging, and deployment decisions, so incorrect guidance may lead to faulty changes or missed edge cases. <br>
Mitigation: Treat outputs as review guidance, require human engineering review, and verify changes with unit tests, integration tests, CI, and production-safe rollout checks. <br>
Risk: The artifact emphasizes avoiding hardcoded secrets, skipped tests, direct production database changes, and unsafe deletion, which are concrete failure modes for agent-assisted development. <br>
Mitigation: Use environment variables for credentials, catch specific exceptions, back up or sandbox database operations, prefer recoverable deletion workflows, and block deployment when tests or required checks fail. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofzhao/programmer-cognition) <br>
- [Publisher project homepage](https://github.com/KingOfZhao/AGI_PROJECT) <br>
- [A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046) <br>
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255) <br>
- [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564) <br>
- [Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with checklists, code examples, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes code-review prompts, debugging records, confidence labels, and deployment readiness checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
