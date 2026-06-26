## Description: <br>
Convert documents between Markdown, DOCX, PDF, HTML, EPUB, PPTX, ODT, RTF, LaTeX, CSV/TSV, Jupyter, and related formats using the Pandoc CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tridefender](https://clawhub.ai/user/tridefender) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical writers, and document maintainers use this skill to plan and run Pandoc conversions, generate DOCX/PDF/HTML/EPUB outputs, create slide decks, extract document text, and configure document formatting options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pandoc examples can fetch remote content or use remote templates/styles. <br>
Mitigation: Use trusted local inputs by default and avoid URL inputs, remote templates, and remote styles unless the source and command are verified. <br>
Risk: Pandoc filters, Lua filters, server mode, pandoc -l, and TeX shell escape can execute local code or expose networked behavior. <br>
Mitigation: Avoid --filter, --lua-filter, server mode, pandoc -l, and TeX shell escape unless the exact files and commands have been reviewed. <br>


## Reference(s): <br>
- [Pandoc Advanced Reference](references/advanced.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tridefender/pandoc-convert) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Pandoc commands that read input files, write converted files, fetch URLs, or invoke filters depending on user-selected options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
