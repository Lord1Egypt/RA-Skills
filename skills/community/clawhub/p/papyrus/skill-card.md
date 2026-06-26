## Description: <br>
Papyrus turns arXiv papers and local PDFs into bilingual, annotation-rich study PDFs with preserved original text, Chinese translation, expert commentary, figures, formulas, and academic typesetting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zanechen76](https://clawhub.ai/user/zanechen76) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and students use Papyrus to convert academic papers into bilingual deep-read study documents with original English, Chinese translation, figures, formulas, and commentary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Formula content may be sent to external rendering services when local LaTeX rendering is unavailable. <br>
Mitigation: Prefer local LaTeX rendering and avoid private or sensitive manuscripts unless remote formula rendering is disabled. <br>
Risk: Downloaded paper sources and extracted files are processed by local scripts. <br>
Mitigation: Run Papyrus in a disposable workspace or container and use public papers from trusted sources. <br>
Risk: Platform adapters refer to a unified SCRIPTS/papyrus entry point that is not present in the artifact file list. <br>
Mitigation: Confirm the installed CLI entry point before relying on the platform adapters; otherwise invoke the bundled scripts directly. <br>
Risk: Web-researched commentary can introduce inaccurate or unsourced interpretations. <br>
Mitigation: Review generated commentary against the original paper and reputable sources before using or publishing the PDF. <br>


## Reference(s): <br>
- [Papyrus ClawHub Page](https://clawhub.ai/zanechen76/papyrus) <br>
- [README](artifact/README.md) <br>
- [Standard Operating Procedure](artifact/SOP.md) <br>
- [Quality Control Checklist](artifact/PROMPTS/qc_checklist.md) <br>
- [arXiv](https://arxiv.org/) <br>
- [CodeCogs LaTeX Equation Renderer](https://latex.codecogs.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated HTML/PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a bilingual PDF workflow that may also create intermediate HTML, formula PNGs, extracted paper sources, and figure images.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
