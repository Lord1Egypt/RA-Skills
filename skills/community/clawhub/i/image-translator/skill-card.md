## Description: <br>
Translates text and extracts and translates text from images or image URLs using Xiangji/Tosoiot translation services with multiple engine options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leoking](https://clawhub.ai/user/leoking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to translate text, local images, or batches of image URLs across supported source and target languages. It is intended for workflows that need OCR-style image translation or multi-engine text translation through the Xiangji/Tosoiot service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected text, images, and image URLs to third-party translation APIs. <br>
Mitigation: Use it only with providers approved for the data being translated, and avoid confidential, regulated, personal, internal-only, or secret-bearing content unless that use is approved. <br>
Risk: Service keys are supplied on the command line and may be exposed through shell history, shared logs, or process inspection. <br>
Mitigation: Use revocable service keys, avoid running commands in shared shells or logs, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/leoking/image-translator) <br>
- [Xiangji Translation website](https://www.xiangjifanyi.com/) <br>
- [Xiangji API documentation](https://openapi-doc.xiangjifanyi.com/) <br>
- [Language support reference](references/languages.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON responses and terminal text from command-line translation scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Xiangji/Tosoiot API credentials and explicit source and target language codes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
