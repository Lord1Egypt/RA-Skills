## Description: <br>
Creates, reads, and revises HTML documents designed for iterative LLM-human review cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ljn-hust](https://clawhub.ai/user/ljn-hust) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, and reviewers use this skill to create self-contained HTML review drafts, extract human feedback from annotated documents, and produce revised HTML versions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or overwrite local HTML documents during review workflows. <br>
Mitigation: Confirm the target path before writing, keep revisions in a versioned folder, and save sensitive or uncertain revisions to a new file instead of overwriting the original. <br>
Risk: Full document text, reviewer comments, edits, and screenshot summaries may appear in the chat transcript. <br>
Mitigation: For sensitive documents, summarize instead of pasting full contents and avoid including raw screenshot or base64 data in the conversation. <br>
Risk: html-collab can become the default format for review drafts, which may be inappropriate for finished presentation HTML. <br>
Mitigation: Use plain HTML mode when the user asks for a clean final document or does not want collab-data, review UI, data-cid attributes, or the engine script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ljn-hust/html-collab) <br>
- [html-collab live demo](https://ljn-hust.github.io/html-collab/) <br>
- [Bundled HTML template](artifact/assets/template.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Self-contained HTML files, markdown context blocks, and occasional shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated and revised documents use collab-data JSON, stable data-cid block identifiers, and screenshot handling that avoids pasting raw base64 in text-only contexts.] <br>

## Skill Version(s): <br>
0.1.5 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
