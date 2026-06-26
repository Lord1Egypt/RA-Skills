## Description: <br>
LiteParse parses, extracts text from, and screenshots PDF and document files locally using the LiteParse CLI (`lit`) for document and vision workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alfred-intel-handler-source](https://clawhub.ai/user/alfred-intel-handler-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and coding agents use LiteParse to extract text, JSON, and page screenshots from local PDFs and documents for review, prompt context, batch conversion, or vision model inputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes local/offline parsing, but OCR may download English language data on first run. <br>
Mitigation: For strict offline or sensitive-document workflows, run with `--no-ocr` when possible or preinstall and cache OCR language data before processing documents. <br>
Risk: Broad input folders or unclear output paths may process or write more private document data than intended. <br>
Mitigation: Use explicit file and output paths, and avoid broad private folders unless the batch scope is intentional. <br>
Risk: The skill depends on the external `@llamaindex/liteparse` npm package and optional local conversion tools. <br>
Mitigation: Verify the package source before installing and confirm required local dependencies such as LibreOffice or ImageMagick for non-PDF formats. <br>


## Reference(s): <br>
- [LiteParse documentation](https://developers.llamaindex.ai/liteparse/) <br>
- [LiteParse output examples](references/output-examples.md) <br>
- [LiteParse ClawHub release](https://clawhub.ai/alfred-intel-handler-source/liteparse) <br>
- [LlamaParse Cloud](https://cloud.llamaindex.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; LiteParse outputs plain text, JSON, and PNG screenshot files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output may include page metadata, text items, bounding boxes, font data, and document metadata; screenshot output creates one PNG file per rendered page.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
