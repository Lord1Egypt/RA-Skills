## Description: <br>
Generates single-file HTML study notes with handwritten notebook styling for technical content, vulnerability analysis, and knowledge summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unclecheng-li](https://clawhub.ai/user/unclecheng-li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical writers use this skill to turn technical content, vulnerability notes, and study summaries into polished single-file HTML notebook pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says one bundled template contains actionable exploit-style content. <br>
Mitigation: Review bundled templates before use and replace exploit-command examples with neutral placeholders or defensive-only content. <br>
Risk: Generated HTML can depend on external icon or font CDNs. <br>
Mitigation: Bundle fonts and icons locally or review the generated HTML before use in offline or privacy-sensitive environments. <br>
Risk: Broad trigger words can cause the skill to activate for routine note-taking requests. <br>
Mitigation: Narrow trigger words or explicitly confirm the intended note style before generating output. <br>


## Reference(s): <br>
- [ClawHub release: Note Skill](https://clawhub.ai/unclecheng-li/note-skill) <br>
- [Quality checklist](references/checklist.md) <br>
- [Component guide](references/components.md) <br>
- [Style A layout library](references/layouts.md) <br>
- [Style B layout library](references/layouts-journal.md) <br>
- [Lucide static CSS](https://unpkg.com/lucide-static@latest/font/lucide.min.css) <br>
- [Remix Icon CSS](https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets for generating a single-file HTML note.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser-openable single-file HTML using bundled templates; generated pages may reference external font and icon CDNs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
