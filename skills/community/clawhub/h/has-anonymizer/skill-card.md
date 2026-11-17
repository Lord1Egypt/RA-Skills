## Description:

HaS Anonymizer helps agents scan, anonymize, and restore sensitive text locally, and scan or mask privacy-relevant regions in images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanwuskill](https://clawhub.ai/user/xuanwuskill)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, developers, and support teams use this skill to reduce exposure of private data before sharing text, logs, documents, messages, photos, or screenshots. Agents can scan first, then anonymize text with restore mappings or mask image regions such as faces, identity documents, plates, QR codes, and barcodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable model downloads and open-ended Python dependencies can change after release.

Mitigation: Pin dependency versions and verify downloaded model checksums before deploying the skill in sensitive environments.

Risk: Text mapping files and restored outputs can reveal the original private data.

Mitigation: Store mappings and restored files in access-controlled locations, avoid sharing them with downstream services, and delete them when they are no longer needed.

Risk: Image masking is irreversible once written to an output file.

Mitigation: Keep originals separate, review masked outputs before publication, and use scan mode before hide mode when the target categories are uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanwuskill/skills/has-anonymizer)
- [HaS text model download](https://huggingface.co/xuanwulab/HaS_Text_0209_0.6B_Q8/resolve/main/has_text_model.gguf)
- [HaS image model download](https://huggingface.co/xuanwulab/HaS_Image_0209_FP32/resolve/main/sensitive_seg_best.pt)
- [HaS text model mirror](https://modelscope.cn/models/TencentXuanwu/HaS_Text_0209_0.6B_Q8)
- [HaS image model mirror](https://modelscope.cn/models/TencentXuanwu/HaS_Image_0209_FP32)
- [Text anonymization evaluation script](artifact/references/eval/eval.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing commands invoke local text and image anonymization tools; batch operations may return skipped-file summaries.]

## Skill Version(s):

1.0.3 (source: server release metadata, created 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
