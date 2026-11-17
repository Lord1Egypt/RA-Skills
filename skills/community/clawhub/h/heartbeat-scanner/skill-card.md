## Description:

Validates user-provided Turtle agent profiles with SHACL and classifies posting patterns as Agent, Human, Cron, or Hybrid using heartbeat analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darshanochandak](https://clawhub.ai/user/darshanochandak)

### License/Terms of Use:

MIT

## Use Case:

Developers and external ClawHub users use this skill to validate agent profile structure and run a local heuristic classification of posting rhythm signals. It is suited for profile self-checks, data-quality feedback, and lightweight Agent/Human/Cron/Hybrid classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency supply-chain exposure from installing rdflib and pyshacl.

Mitigation: Install in a virtual environment and pin reviewed dependency versions before operational use.

Risk: Profile contents may include information about user behavior or posting patterns.

Mitigation: Run the tool only on profiles or data the user is authorized to analyze.

Risk: Agent, Human, Cron, and Hybrid labels are heuristic and can be wrong or over-interpreted.

Mitigation: Treat the classification as an advisory signal, not reliable identity evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darshanochandak/skills/heartbeat-scanner)
- [W3C SHACL namespace](http://www.w3.org/ns/shacl#)
- [Mimicry ontology namespace](http://moltbook.org/mimicry/ontology#)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text CLI output with Markdown-styled result messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes validation status, classification, confidence, data-quality tier, and optional recommendations.]

## Skill Version(s):

2.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
