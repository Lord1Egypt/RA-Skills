## Description: <br>
Human Distill helps an agent research a public creator, expert, founder, or coach and produce an evidence-labeled persona dossier from web sources, optional Douyin browser collection, and optional deep research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, knowledge workers, and agent users use this skill to turn public creator or expert material into a structured markdown profile with confirmed, inferred, and conflicting claims clearly labeled. It is useful for repeatable persona research across web sources and, when available, Douyin public video text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Logged-in browser sessions may expose personal account state while collecting Douyin public content. <br>
Mitigation: Use a dedicated browser profile, confirm the expected account before browsing, and avoid collecting private or paid material. <br>
Risk: Generated memory and people files can retain profile notes about public individuals longer than needed. <br>
Mitigation: Review saved dossiers for necessity and delete generated memory or people files when the research task is complete. <br>
Risk: Search snippets and short-form captions can lead to unsupported persona claims. <br>
Mitigation: Keep confirmed, inferred, and conflicting claims labeled and verify high-impact conclusions against primary sources before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/spikesubingrui-design/human-distill) <br>
- [Search Query Templates](references/search-queries.md) <br>
- [Sample Persona Excerpt](examples/sample-persona-excerpt.md) <br>
- [Launch Notes](docs/LAUNCH.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, configuration] <br>
**Output Format:** [Markdown files with evidence labels, source tables, transcript notes, and a final persona dossier] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are written to workspace memory files and may include a people entry for knowledge-base use.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
