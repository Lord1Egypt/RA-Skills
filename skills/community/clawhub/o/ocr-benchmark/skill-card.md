## Description: <br>
Ocr Benchmark runs multi-model OCR on local images, compares model accuracy against human-verified ground truth with fuzzy line-level scoring, and generates ranked reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingfengli](https://clawhub.ai/user/yingfengli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and evaluation teams use this skill to run OCR across configured providers, compare accuracy, cost, and speed against human-verified ground truth, and generate JSON, terminal, and PPTX reports for OCR quality review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images may be sent to AWS Bedrock, Google AI Studio, or a configured PaddleOCR endpoint. <br>
Mitigation: Run only on images the user is allowed to share with the selected providers, and disable providers whose data handling is not acceptable for the workload. <br>
Risk: Provider credentials and OCR service permissions can create cost or access exposure. <br>
Mitigation: Use least-privileged credentials, install in a virtual environment, and monitor cloud usage while benchmarking. <br>
Risk: Generated JSON and PPTX reports may contain sensitive text extracted from source images. <br>
Mitigation: Store, share, and retain benchmark outputs according to the sensitivity of the input images and extracted OCR text. <br>
Risk: OCR model outputs can be inaccurate and should not be treated as ground truth. <br>
Mitigation: Use human-verified ground truth for scoring and manually review benchmark findings before relying on them. <br>


## Reference(s): <br>
- [Ground Truth Format](references/ground-truth-format.md) <br>
- [Model Registry](references/models.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; benchmark runs produce JSON results, terminal reports, scores.json, and optional PPTX reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs require local image paths and provider credentials for selected cloud or external OCR services.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
