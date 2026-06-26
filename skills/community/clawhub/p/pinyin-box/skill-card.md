## Description: <br>
Pinyin Box helps agents convert Chinese text, or text extracted from images, into pinyin grid or mizige practice sheets as PNG or PDF files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanglinzhen](https://clawhub.ai/user/yanglinzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn Chinese text or OCR-extracted image text into printable handwriting practice materials. It supports pinyin-grid and mizige worksheet generation with PNG output by default and PDF output on request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external pinyin-box package installation. <br>
Mitigation: Install it in a virtual environment when possible and review the dependency before use. <br>
Risk: Image OCR and generated worksheet files may save sensitive text in the workspace output directory. <br>
Mitigation: Use only text or images intended for worksheet generation, and avoid sensitive images unless saved OCR text and output files are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanglinzhen/pinyin-box) <br>
- [pinyin-box 1.0.0 package artifact](https://github.com/yanglinzhen/pinyin-box/releases/download/v1.0.0/pinyin_box-1.0.0-py3-none-any.whl) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG or PDF file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files are saved to the workspace output directory; image inputs may require OCR before worksheet generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
