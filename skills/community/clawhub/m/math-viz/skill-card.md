## Description: <br>
Math Viz helps an agent turn abstract math problems into interactive HTML visualizations for geometry, functions, dynamic points, and related topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abill6688](https://clawhub.ai/user/abill6688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, educators, and learning agents use this skill to generate interactive Chinese-language math visualizations that help students explore geometric relationships, function behavior, trajectories, and real-time numerical changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated local HTML previews can include private problem text or data and may load visualization libraries from public CDNs. <br>
Mitigation: Review generated pages before previewing or sharing them, avoid placing sensitive private content in generated pages on shared machines, and use the skill only where public CDN loading is acceptable. <br>
Risk: The included verifier script performs local execution checks and has temporary-file hygiene caveats. <br>
Mitigation: Run the verifier only on files you intend to validate, avoid sensitive content until unique temporary files and cleanup are in place, and inspect results before relying on the visualization. <br>


## Reference(s): <br>
- [JSXGraph patterns](references/jsxgraph-patterns.md) <br>
- [Three.js patterns](references/threejs-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with generated HTML files and bash validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML may load JSXGraph or Three.js from public CDNs and should be checked with the included verifier before previewing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
