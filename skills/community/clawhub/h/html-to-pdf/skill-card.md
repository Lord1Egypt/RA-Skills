## Description: <br>
Convert HTML files and URLs to PDF using Puppeteer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HankAgent](https://clawhub.ai/user/HankAgent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to convert local HTML documents, web pages, and reports into PDF files with configurable page size, orientation, margins, headers, footers, page ranges, and scaling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converting untrusted URLs or HTML files causes Chromium to load that content and write a PDF to a user-provided path. <br>
Mitigation: Convert only trusted content where possible, use an isolated environment for untrusted inputs, and review output paths before running the script. <br>
Risk: Disabling Chromium sandboxing or removing macOS quarantine protections weakens browser and platform safeguards. <br>
Mitigation: Keep Chromium sandboxing enabled and avoid no-sandbox or quarantine-removal workarounds unless the environment is isolated and the risk is understood. <br>
Risk: Puppeteer installation downloads or uses a Chromium binary from the configured package environment. <br>
Mitigation: Install Puppeteer from a trusted npm environment and use a trusted Chrome or Chromium executable when overriding the default download. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [Setup & Requirements](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with bash and JavaScript examples; PDF file output when the conversion script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated PDF path is chosen by the user, and Puppeteer PDF options control layout and rendering.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
