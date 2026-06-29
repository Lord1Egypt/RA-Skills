## Description: <br>
Improve important deliverables by looping them through multiple isolated AI reviewers, each evaluating from a different angle, until all reviewers give full approval (Score 120). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ariesshin](https://clawhub.ai/user/ariesshin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, writers, planners, and other agent users use this skill to improve important deliverables through isolated multi-perspective review, revision, and final approval checks. It is intended for work where a single-pass answer is not enough and the user wants a stricter quality gate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Multi-pass review can be slower and more expensive than a normal single-pass agent response. <br>
Mitigation: Use explicit invocation for important deliverables where the additional review cost is justified. <br>
Risk: Local review artifacts such as manifests, ledgers, and reviewer outputs may contain sensitive deliverable content. <br>
Mitigation: Avoid sensitive documents unless you trust the platform's subagent isolation and are comfortable with those local files being created. <br>
Risk: Subagent isolation may be unavailable or unverified in some runtimes, reducing the independence of the review perspectives. <br>
Mitigation: Run the runtime mapping and isolation probe, disclose degraded fallback when isolation is unavailable, and avoid claiming full approval unless the final reviewers pass with Score 120. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ariesshin/skills/loop-anything-skill) <br>
- [README](artifact/README.md) <br>
- [Runtime Compatibility](artifact/references/runtime-compatibility.md) <br>
- [Facet Patterns](artifact/references/facet-patterns.md) <br>
- [Evidence Guide](artifact/references/evidence-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown workflow guidance with reviewer packet templates, reviewer output templates, manifest requirements, and shell validation commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local review artifacts such as a run manifest, reviewer outputs, an issue ledger, and a final summary when file I/O is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
