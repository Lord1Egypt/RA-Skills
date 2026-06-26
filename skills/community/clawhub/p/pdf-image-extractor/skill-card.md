## Description: <br>
Extract images from PDF files with three modes: original quality, 800x800 standard output, and compressed files under 50KB for social sharing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jnbno1163](https://clawhub.ai/user/jnbno1163) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and business operators use this skill to extract product or marketing images from PDF catalogs and prepare them for print, e-commerce, websites, or social media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF images can contain sensitive or private information and are written to the configured output folder. <br>
Mitigation: Test on non-sensitive PDFs first and use private documents only when the user is comfortable with extracted images being saved locally. <br>
Risk: The scripts use hard-coded input and output folders by default. <br>
Mitigation: Edit the configured PDF and output folders before running the extraction scripts. <br>
Risk: Installing dependencies directly into a shared Python environment can affect other projects. <br>
Mitigation: Install PyMuPDF and Pillow in a virtual environment. <br>


## Reference(s): <br>
- [Configuration Parameters](references/config.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jnbno1163/pdf-image-extractor) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/jnbno1163) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown instructions with inline shell commands and Python script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local image files in per-PDF output folders when the referenced scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
