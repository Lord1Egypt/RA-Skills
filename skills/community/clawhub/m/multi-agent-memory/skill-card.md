## Description: <br>
Provides a multi-agent shared memory and project collaboration framework with isolated project state, shared knowledge, cross-project search, versioned documents, milestone tracking, weekly reports, and handoff documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucey0017-cloud](https://clawhub.ai/user/brucey0017-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multiple agents across projects by maintaining project-local state, shared knowledge, recurring status checks, weekly summaries, milestones, and handoff records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores, searches, and archives project information across projects under /root/.openclaw, which can expose secrets or private customer data if used without boundaries. <br>
Mitigation: Do not place secrets, credentials, or customer-private data in shared knowledge or logs; add retention and redaction rules before sensitive use. <br>
Risk: Project and phase names are used in filesystem paths by the bundled shell scripts, while evidence notes undefined path-safety controls. <br>
Mitigation: Use simple trusted project and phase names only, and add input validation before running the scripts in shared or sensitive workspaces. <br>
Risk: Cross-project search and shared knowledge can blur project boundaries and surface information outside the intended project context. <br>
Mitigation: Keep sensitive projects separate from the shared knowledge base and review search results before applying them to another project. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucey0017-cloud/multi-agent-memory) <br>
- [Package repository](https://github.com/brucey0017-cloud/multi-agent-memory.git) <br>
- [Package homepage](https://github.com/brucey0017-cloud/multi-agent-memory#readme) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and generated project-memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates files under /root/.openclaw when the bundled scripts are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; artifact files declare 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
