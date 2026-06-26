## Description: <br>
Knowledge Engine helps an agent search, add, link, distill, and visualize locally stored personal concepts and beliefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zabr1314](https://clawhub.ai/user/zabr1314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a local personal knowledge base: search previous concepts, add and link new concepts, track beliefs, run periodic distillation, and generate graph visualizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently delete deprecated stored concepts when prune runs without --dry-run. <br>
Mitigation: Run prune with --dry-run first and keep backups of the memory directory before allowing deletion. <br>
Risk: The generated visualization loads D3 from the internet despite the skill's no-network claim. <br>
Mitigation: Open generated visualizations only where CDN loading is acceptable, or replace the D3 CDN reference with a local copy before use. <br>


## Reference(s): <br>
- [Knowledge Engine Skill Page](https://clawhub.ai/zabr1314/knowledge-engine) <br>
- [Publisher Profile](https://clawhub.ai/user/zabr1314) <br>
- [Concept Card Schema](artifact/resources/concept-schema.md) <br>
- [Belief Card Schema](artifact/resources/belief-schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell and Python snippets; helper scripts produce local JSON, SQLite, Markdown, and HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and mutates local memory data under memory/; graph visualization writes an HTML file to the user's Desktop.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
