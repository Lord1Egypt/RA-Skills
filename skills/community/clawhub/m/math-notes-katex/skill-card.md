## Description: <br>
Render math-heavy notes to PNG using KaTeX and headless Brave when high-quality formula layout is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rokokol](https://clawhub.ai/user/rokokol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn UTF-8 math notes with LaTeX inline and display formulas into clean PNG images, especially when normal chat formatting is insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering notes starts a local browser with weakened sandboxing and local file access. <br>
Mitigation: Run the skill as an unprivileged user and use it only for local math-note image rendering. <br>
Risk: Untrusted note content may be rendered through the local browser workflow. <br>
Mitigation: Avoid rendering notes from untrusted sources. <br>


## Reference(s): <br>
- [Input note format](references/formatting.md) <br>
- [Troubleshooting: KaTeX to PNG](references/troubleshooting.md) <br>
- [ClawHub skill page](https://clawhub.ai/rokokol/math-notes-katex) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Markdown, Guidance] <br>
**Output Format:** [PNG image files generated from UTF-8 markdown-like notes with LaTeX math] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce a single PNG or a sequence of page PNGs; requires local Node.js, KaTeX, and a Brave or Chromium-compatible browser.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
