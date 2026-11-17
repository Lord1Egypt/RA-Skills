## Description:

Blog Writer helps an agent draft authentic, opinionated blog posts and long-form content in a specific writer's voice, from research review through Notion publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to draft and revise thought leadership, article, and blog content in a specific personal voice while incorporating provided research. The workflow also publishes drafts to a configured Notion database and saves finalized posts as future style examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drafts are required to be written to a fixed TS Notes Notion database.

Mitigation: Change the Notion destination to an approved database and require explicit confirmation before each publish.

Risk: Finalized posts may be retained as future style examples.

Mitigation: Confirm retention is intended and remove sensitive or private material before adding a post to the examples library.

Risk: The example pruning script can delete files outside its intended folder if its path is not constrained.

Mitigation: Avoid running pruning in execute mode until the path is constrained to the skill directory and deletion targets are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-blog-writer)
- [Skill setup guide](https://skillboss.co/skill.md)
- [Writing style guide](artifact/style-guide.md)
- [Radical Transparency Influence Methodology](artifact/2024-02-17-radical-transparency-sales.md)
- [Give Spotlight on Mac Superpowers with Raycast](artifact/2024-02-17-raycast-spotlight-superpowers.md)
- [How Short-form Content Is Changing Marketing & Storytelling Forever](artifact/2024-02-17-short-form-content-marketing.md)
- [The Amazing Benefits of Typing Very Fast](artifact/2024-02-17-typing-speed-benefits.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown blog drafts and Notion-flavored Markdown content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish drafts to a configured Notion database and save finalized posts as Markdown examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
