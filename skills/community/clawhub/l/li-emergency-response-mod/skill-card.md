## Description:

Provides structured, evidence-driven corporate incident response guidance with single-agent and multi-agent modes for traditional IT, database, and AI infrastructure scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, incident commanders, analysts, and engineers use this skill to coordinate authorized incident response, evidence collection, timeline reconstruction, containment planning, recovery, and post-incident reporting. It is suited for enterprise incidents, CTF-style response exercises, and AI infrastructure security events where actions need auditability and human approval for high-impact steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled handbook material includes reverse-shell, C2, tunneling, payload-generation, deletion, and credential-file command examples that could be unsafe if executed directly.

Mitigation: Treat those sections as lab-only reference material, require explicit human approval before any agent executes high-risk commands, and prefer safer playbooks plus WAL/report scripts for normal incident response.

Risk: Incident response recommendations can disrupt business services or damage forensic evidence if containment or eradication steps are taken too early.

Mitigation: Preserve evidence before response, require HITL review for isolation, account blocking, deletion, reboot, recovery, and broad blocking actions, and record decisions in the WAL.

Risk: Generated findings can be misleading if conclusions are not reproducible from evidence.

Mitigation: Use VBR practices: attach evidence references, command outputs, hashes, logs, or timeline entries before reporting conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-emergency-response-mod)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Compatibility guide](artifact/COMPATIBILITY.md)
- [Multi-agent architecture](artifact/multi_agent/ARCHITECTURE.md)
- [Multi-agent deployment guide](artifact/multi_agent/DEPLOYMENT_GUIDE.md)
- [Common incident response quick reference](artifact/playbooks/常见事件处置速查.md)
- [Forensics and evidence standard](artifact/playbooks/取证与证据规范.md)
- [AI infrastructure incident response handbook](artifact/playbooks/AI基础设施应急响应手册.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands, JSON/YAML configuration examples, and generated report or timeline files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the incident context and should preserve evidence, cite reproducible findings, and route high-impact actions through human approval.]

## Skill Version(s):

1.0.0 (source: server release and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
