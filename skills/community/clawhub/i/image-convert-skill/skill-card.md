## Description: <br>
Uses Pillow to convert and compress common image formats, including PNG, JPEG, GIF, BMP, TIFF, and WebP, with quality controls, resizing, and lossless options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KanoCifer](https://clawhub.ai/user/KanoCifer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert, resize, and compress local image files or batches of image files from command-line workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing Pillow from an untrusted package source could introduce supply-chain risk. <br>
Mitigation: Install Pillow from a trusted package source before using the skill. <br>
Risk: Batch conversions using directories, globs, or broad input patterns may process or overwrite unintended images. <br>
Mitigation: Review glob and directory inputs before execution and use explicit output directories. <br>
Risk: Image conversion and compression can remove EXIF data, alter color modes, resize images, or reduce visual quality depending on the selected options. <br>
Mitigation: Keep source images when fidelity or metadata matters, and choose lossless, quality, and max-size settings deliberately. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KanoCifer/image-convert-skill) <br>
- [Publisher profile](https://clawhub.ai/user/KanoCifer) <br>
- [WebP settings reference](artifact/references/webp_settings.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown/text guidance with CLI commands and generated local image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on Pillow support, selected quality or compression settings, input file validity, and the chosen output paths.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
