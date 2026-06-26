## Description: <br>
Paper Analyzer turns a paper link, PDF, attachment, or pasted paper text into a rigorous Markdown research report and, when requested, a polished method diagram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wooonster](https://clawhub.ai/user/wooonster) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, developers, and technical reviewers use this skill to read academic papers, produce structured critiques, and create optional architecture diagrams for methods or pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate broadly whenever paper content is shared. <br>
Mitigation: Use it in contexts where automatic paper analysis is intended, and review whether the trigger behavior matches the workspace's expectations. <br>
Risk: The skill writes report and diagram files by design. <br>
Mitigation: Review output paths and generated files before relying on them or sharing them. <br>
Risk: The skill may fetch arXiv pages and may use local browser rendering for PNG output when requested. <br>
Mitigation: Run it with network and browser permissions appropriate for the environment, and inspect generated diagrams before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wooonster/paper-reading) <br>
- [README](README.md) <br>
- [Chinese README](README_zh.md) <br>
- [Diagram design guide](references/diagram-design.md) <br>
- [Chinese diagram labels](references/diagram-labels-cn.md) <br>
- [Chinese report structure](references/output-cn.md) <br>
- [Venue tiers](references/venue-tiers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Code, Guidance] <br>
**Output Format:** [Markdown reports plus optional HTML, SVG, or PNG diagram files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes report files and requested diagram assets to /mnt/user-data/outputs/ or a workspace outputs/ fallback.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
