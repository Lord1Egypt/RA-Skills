## Description: <br>
General PLC development, explanation, review, refactoring, debugging, and troubleshooting skill across IEC 61131-3 style industrial control work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[migo-ovo](https://clawhub.ai/user/migo-ovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and industrial control engineers use this skill to draft, explain, review, refactor, debug, and troubleshoot PLC logic with vendor-aware routing across common IEC 61131-3 languages and major PLC ecosystems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or reviewed PLC logic could be applied to live machinery with incomplete vendor, model, wiring, or field-condition evidence. <br>
Mitigation: Treat outputs as engineering drafts and require vendor/model confirmation, simulation or staging tests, safety review, and site change-control approval before deployment. <br>
Risk: Safety-sensitive PLC topics such as interlocks, emergency stops, forced outputs, and reset behavior can be hazardous when assumptions are wrong. <br>
Mitigation: Require site documentation and field verification for wiring, fail-safe behavior, actuator response, and safety architecture before accepting any final safety conclusion. <br>
Risk: Documented installation or maintenance commands such as forced updates or ownership changes can alter local skill files or permissions. <br>
Mitigation: Review commands before execution, avoid unnecessary force flags, and scope permission changes to the intended OpenClaw skill workspace. <br>


## Reference(s): <br>
- [PLC Skill ClawHub Release](https://clawhub.ai/migo-ovo/plc-skill) <br>
- [Skill Architecture](artifact/references/skill-architecture.md) <br>
- [Reference Map](artifact/references/reference-map.md) <br>
- [Common PLC Task Router](artifact/references/common/task-router.md) <br>
- [Vendor Routing](artifact/references/vendors/vendor-routing.md) <br>
- [Safety Boundaries](artifact/references/common/safety-boundaries.md) <br>
- [ST Output Style](artifact/references/common/st-output-style.md) <br>
- [Template Map](artifact/templates/common/template-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, shell commands] <br>
**Output Format:** [Markdown with Structured Text, Ladder/FBD/SFC guidance, review findings, checklists, templates, and occasional shell command blocks for installation or tooling tasks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are engineering drafts that should preserve vendor assumptions, separate confirmed facts from assumptions, and avoid unsupported safety conclusions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
