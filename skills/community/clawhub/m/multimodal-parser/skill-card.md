## Description: <br>
Unified multi-modal content parser for images, PDFs, DOCX files, and audio that performs OCR or transcription and returns text, Markdown, or structured output for LLM processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ayalili](https://clawhub.ai/user/Ayalili) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill as a preprocessing layer to extract content from images, PDFs, Word documents, and audio for document question answering, knowledge-base construction, OCR, transcription, and batch document parsing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parsed OCR, transcript, or document text may contain sensitive information or prompt-injection content. <br>
Mitigation: Use the skill only on files that are appropriate to bring into an agent conversation, and review extracted text before passing it to downstream prompts or tools. <br>
Risk: Parser behavior depends on local tools such as Tesseract, Poppler, Pandoc, Whisper, and ffmpeg. <br>
Mitigation: Install parser dependencies only from trusted package sources and verify the local runtime before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ayalili/multimodal-parser) <br>
- [Zod v3.22.4 module](https://deno.land/x/zod@v3.22.4/mod.ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Plain text, Markdown, or structured JSON object with metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns success status, detected file type, output format, parsed content, metadata, or an error message.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
