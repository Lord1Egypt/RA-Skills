## Description:

End-to-end LoRA training pipeline covering reference photo collection, face verification, dataset scraping, quality checks, WD14 captioning, and RunPod-based training.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskwang](https://clawhub.ai/user/iskwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to assemble LoRA-ready subject image datasets, verify and clean face images, generate captions, and train model outputs. It should be used only for datasets the user has rights and consent to process.

### Deployment Geography for Use:

Global; the RunPod training phase recommends EU zones and avoids Canada.

## Known Risks and Mitigations:

Risk: The workflow handles face datasets through scraping and biometric matching without enough consent and provenance safeguards.

Mitigation: Use only datasets the user has rights and consent to process, keep source records, and avoid login bypass, mirror scraping, or other collection methods that evade site access controls.

Risk: RunPod training uploads the prepared dataset to a third-party compute environment.

Mitigation: Treat RunPod upload as disclosure of the full dataset, obtain user confirmation before upload, use secure cloud settings where available, and delete remote pods and temporary data after retrieving outputs.

Risk: ZIP extraction, broad file operations, and generated training commands can modify or expose local workspace data.

Mitigation: Inspect ZIP inputs in a sandbox, validate the expected dataset folder structure before training, keep image and caption contents opaque to the agent, and review file-moving or deletion commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iskwang/skills/lora-pipeline)
- [Skill definition](artifact/SKILL.md)
- [Reference collection and verification phase](artifact/phases/01-reference.md)
- [Dataset scraping phase](artifact/phases/02-scraping.md)
- [Verify and clean dataset phase](artifact/phases/03-verify.md)
- [WD14 captioning phase](artifact/phases/04-caption.md)
- [RunPod LoRA training phase](artifact/phases/05-training.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown phase instructions with inline Python, JavaScript, and shell command blocks; helper scripts produce caption files, TOML configuration, and LoRA model files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local dataset folders, caption text files, RunPod training commands, and downloaded .safetensors outputs when executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
