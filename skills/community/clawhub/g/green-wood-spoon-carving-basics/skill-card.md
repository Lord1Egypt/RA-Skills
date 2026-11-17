## Description:

Guides an agent in helping users plan, template, track, and document green-wood spoon and utensil carving while leaving all physical carving, finishing, and safety decisions to the human.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn local green hardwood into custom spoons, spatulas, and small utensils by having the agent identify wood options, calculate drying and shrinkage schedules, generate templates, and maintain progress, inventory, and barter records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unpinned npx install command creates supply-chain exposure.

Mitigation: Prefer a trusted or pinned ClawHub installer when available and avoid running the install command in a shell with unnecessary secrets.

Risk: The skill may request GPS/photos and maintain local tracking files.

Mitigation: Provide only photos and location details you are comfortable storing in project files, and keep filesystem tracking limited to the carving workspace.

Risk: Green-wood carving uses sharp hand tools and can cause injury if the human follows unsafe technique.

Mitigation: Keep physical carving decisions with the human, follow the skill's knife-safety checkpoints, use protective practices, and stop if technique, workspace, or physical strain is unsafe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/howtousehumans/skills/green-wood-spoon-carving-basics)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command and structured text templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ready-to-trace templates, checklists, drying logs, reminders, inventory cards, and barter templates, and may maintain progress files in the local carving workspace.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
