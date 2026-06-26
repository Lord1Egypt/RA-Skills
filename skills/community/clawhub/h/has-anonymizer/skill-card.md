## Description: <br>
HaS (Hide and Seek) provides on-device text and image anonymization for multilingual sensitive-entity scanning, semantic text replacement and restoration, and visual masking of privacy categories such as faces, IDs, passports, license plates, QR codes, and barcodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuanwuskill](https://clawhub.ai/user/xuanwuskill) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scan, anonymize, and restore sensitive text locally before sharing it or sending it to cloud LLMs. They also use it to detect and mask privacy-relevant regions in images such as faces, ID cards, passports, license plates, QR codes, and barcodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mapping JSON files can restore original sensitive text. <br>
Mitigation: Store mapping files as secrets, restrict access to them, and delete them when restoration is no longer required. <br>
Risk: The skill downloads declared models and Python dependencies before use. <br>
Mitigation: Install only in environments where those downloads are acceptable and review dependency/model provenance through the listed references. <br>
Risk: The reference evaluation workflow can save original text and mappings in its work directory. <br>
Mitigation: Use synthetic or approved test data for evaluation, or run it only where saved originals and mappings are permitted. <br>
Risk: Image masking is irreversible once the masked output replaces a workflow copy. <br>
Mitigation: Keep original images separate and review masked outputs before publishing or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuanwuskill/has-anonymizer) <br>
- [HaS text model Q8](https://huggingface.co/xuanwulab/HaS_Text_0209_0.6B_Q8/resolve/main/has_text_model.gguf) <br>
- [HaS image model FP32](https://huggingface.co/xuanwulab/HaS_Image_0209_FP32/resolve/main/sensitive_seg_best.pt) <br>
- [HaS text model mirror](https://modelscope.cn/models/TencentXuanwu/HaS_Text_0209_0.6B_Q8) <br>
- [HaS image model mirror](https://modelscope.cn/models/TencentXuanwu/HaS_Image_0209_FP32) <br>
- [Evaluation script](references/eval/eval.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text operations can produce anonymized text files and mapping JSON files; image operations can produce masked image files and JSON detection summaries.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
