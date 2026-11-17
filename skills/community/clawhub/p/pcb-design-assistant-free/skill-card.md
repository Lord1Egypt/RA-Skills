## Description: <br>
A JLC EDA/EasyEDA circuit-design assistant that helps agents create single-page schematics, search purchasable components, and run basic quality gate checks for board-ready designs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, hardware makers, electronics students, and engineers use this skill to turn a short circuit requirement into a single-page EasyEDA schematic workflow with component selection, net naming, and basic validation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to interact with a local EasyEDA bridge and create or export schematic artifacts. <br>
Mitigation: Install only for intended EasyEDA/JLC workflows and review prompts before allowing schematic creation or export actions. <br>
Risk: Generated schematics, component selections, and inventory assumptions may be incomplete or stale. <br>
Mitigation: Review the design in EasyEDA, verify critical nets and components, and rerun the documented quality checks before fabrication. <br>
Risk: The trigger wording is broader than ideal for a specialized EDA workflow. <br>
Mitigation: Invoke the skill only for EasyEDA/JLC schematic work and keep unrelated agent tasks outside this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/pcb-design-assistant-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, code examples, status summaries, component lists, checklists, and risk notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an EasyEDA/JLC workflow with a local bridge on localhost:3000; the free version is limited to single-page schematic design and basic quality checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: target metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
