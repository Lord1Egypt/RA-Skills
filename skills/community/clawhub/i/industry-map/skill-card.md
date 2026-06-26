## Description: <br>
Generates comprehensive industry chain maps from a requested head node using deep research, discovered first-level categories, and structured CSV and Markdown outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MemoryF](https://clawhub.ai/user/MemoryF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research agents use this skill to create industry taxonomy maps for market, supply-chain, and sector-structure analysis. The skill guides research, category discovery, node naming, and generation of a CSV hierarchy plus a Markdown process record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated industry maps may contain inaccurate classifications, weak sourcing, or outdated sector information. <br>
Mitigation: Review the generated sources, category rationale, and CSV hierarchy before relying on the outputs for business or technical decisions. <br>
Risk: The skill can write generated CSV and Markdown outputs to a selected directory. <br>
Mitigation: Confirm output paths and generated files before integrating them into shared documentation or downstream workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MemoryF/industry-map) <br>
- [Publisher Profile](https://clawhub.ai/user/MemoryF) <br>
- [Skill Specification](SKILL.md) <br>
- [Reference README](README.md) <br>
- [Default CSV Template](assets/default_template.csv) <br>
- [Semiconductor Industry Map Example](半导体产业图谱.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, CSV, Guidance] <br>
**Output Format:** [CSV hierarchy files and Markdown process records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates an industry map CSV with id, name, level, parent, path, classification, and decision-basis fields; may also generate a Markdown research record unless disabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
