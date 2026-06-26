## Description: <br>
Use when building journal club or literature-report slides from research PDFs and you need a figure-first, audience-facing, visually polished deck that preserves paper logic, keeps crops safe, pairs main and supporting evidence correctly, and passes render-based QA. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0928wangyu](https://clawhub.ai/user/0928wangyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, researchers, educators, and developers use this skill to turn one or more research-paper PDFs into journal club, lab meeting, literature-review, or paper-report slide decks. It emphasizes faithful paper logic, readable figure and support-evidence pairing, polished academic design, and render-based QA before delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may process user-provided research PDFs and create local working artifacts such as extracted text, image crops, presentation files, and QA renders. <br>
Mitigation: Use it only with papers and local artifacts the user is comfortable processing, and remove sensitive workspace outputs when they are no longer needed. <br>
Risk: Incorrect figure pairing, unsafe crops, unreadable support panels, or render-only layout defects could make a slide deck misleading or unsuitable for presentation. <br>
Mitigation: Verify figure identity, conclusion-level support mapping, crop boundaries, text readability, and final rendered slides before relying on the deck. <br>
Risk: Generated commands, scripts, or configuration suggestions may install dependencies or transform local files. <br>
Mitigation: Review commands and generated code before execution, prefer an isolated local virtual environment, and inspect changed files before delivery. <br>


## Reference(s): <br>
- [Figure integrity deep-fix notes](references/figure-integrity-deep-fix-notes.md) <br>
- [MetaEdit journal-club mapping and crop notes](references/metaedit-jcslides-mapping-and-crop-notes.md) <br>
- [Multi-paper plasmid copy-number deck: session notes](references/multi-paper-plasmid-copy-number-deck.md) <br>
- [Python-pptx first-pass render QA lessons for paper journal-club decks](references/python-pptx-render-qa-first-pass.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with optional code blocks, shell commands, configuration notes, and local presentation artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of extracted text, rendered page images, figure crops, PowerPoint files, and rendered QA outputs in the user's local workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
