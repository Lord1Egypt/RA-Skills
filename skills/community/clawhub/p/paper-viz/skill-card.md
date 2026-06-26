## Description: <br>
Extracts experimental results from research paper PDFs, screenshots, or table images, selects appropriate chart types, generates deterministic Python plots, and exports PNG, PDF, and LaTeX outputs into a paper-named folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ghxianzhi](https://clawhub.ai/user/ghxianzhi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to convert readable experimental results from papers or screenshots into structured data, reproducible academic figures, and LaTeX insertion snippets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates local output folders and generated files, which may write into an unintended or sensitive location if the output root is ambiguous. <br>
Mitigation: Choose an explicit output directory before running and ask the agent to preview planned paths when persistent generated files are not desired. <br>
Risk: Generated files could overwrite existing files in the selected output location. <br>
Mitigation: Check the target folder before execution or require unique paper-named output folders for each run. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown summary plus JSON, Python plotting code when needed, PNG/PDF figures, and LaTeX snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates experimental_data.json, figure exports, and latex_codes.tex in a user-selected or current writable output folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
