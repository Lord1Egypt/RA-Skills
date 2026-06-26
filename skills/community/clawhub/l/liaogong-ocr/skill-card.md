## Description: <br>
LiaoGong-OCR helps agents extract text from user-provided images using EasyOCR and Tesseract, with preprocessing chains for screenshots, documents, Chinese posters, and phone photos of screens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jnbno1163](https://clawhub.ai/user/jnbno1163) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to extract text from images, screenshots, phone photos, and batches of local image files. It is useful when an agent needs OCR output it can summarize, compare, save, or pass into later analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OCR can extract secrets or personal data from screenshots and images. <br>
Mitigation: Only provide images whose text may be safely exposed to the agent, chat transcript, or output files. <br>
Risk: EasyOCR may download and cache model files on first use. <br>
Mitigation: Run first use in an approved environment and account for local model cache storage. <br>
Risk: OCR accuracy can be weak on degraded photos, dense Chinese characters, handwriting, or compressed screen captures. <br>
Mitigation: Review extracted text before using it for important decisions, and use cleaner screenshots or cross-validation workflows for critical numbers. <br>
Risk: Image-processing dependencies can carry normal dependency hygiene risks. <br>
Mitigation: Install in a locked and updated Python environment, especially for Pillow, numpy, EasyOCR, and pytesseract. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jnbno1163/liaogong-ocr) <br>
- [Benchmark Results](references/benchmark-results.md) <br>
- [Preprocessing Guide](references/preprocessing-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text OCR results, Markdown guidance, Python examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write extracted OCR text to local text files when invoked through CLI or batch workflows.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
