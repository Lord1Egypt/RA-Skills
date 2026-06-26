## Description: <br>
Parse PDF or Markdown files into structured HTML posters with multi-modal output formats, or generate poster and slide images through configured LLM and image-generation providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuriyanzexuan](https://clawhub.ai/user/yuriyanzexuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content automation users can use this skill to convert PDFs or Markdown into styled HTML posters and export them as PDF, PNG, DOCX, or PPTX. Users can also generate poster and slide images when approved LLM and image-generation providers are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full PDFs, Markdown, tables, captions, and images may be sent to configured third-party LLM or image-generation providers. <br>
Mitigation: Use only approved providers for the data being processed, avoid confidential or regulated documents unless those providers are authorized, and choose simple or local rendering when remote processing is unnecessary. <br>
Risk: The installer can make broad local system changes, including Python, UV, system libraries, and Playwright Chromium setup. <br>
Mitigation: Review install.sh before execution, prefer trusted or pinned installation paths, and run the skill in an isolated environment. <br>
Risk: API keys and endpoint values are required for remote model modes. <br>
Mitigation: Review .env carefully, keep credentials out of version control, and scope keys to the minimum permissions needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuriyanzexuan/mm-output) <br>
- [Artifact README](artifact/README.md) <br>
- [MM Output README](artifact/mm_output/README.md) <br>
- [OpenAI API endpoint](https://api.openai.com/v1) <br>
- [Astral UV](https://github.com/astral-sh/uv) <br>
- [Marker PDF](https://github.com/Hadlay-Zhang/marker.git) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown and command-line workflow guidance that produces local HTML, PDF, PNG, DOCX, PPTX, and image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.12+, UV, Playwright Chromium, document inputs, output directory selection, and provider API keys for LLM or image-generation modes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
