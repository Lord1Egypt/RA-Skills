## Description:

Generate 3D-printable models from images or text prompts using PrintPal, optionally create source images with WaveSpeed, and generate SEO product-listing assets for marketplaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plebbyd](https://clawhub.ai/user/plebbyd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, makers, and sellers use this skill to turn images or prompts into 3D model files for printing, and to package product photos and SEO listing text for marketplace workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, images, and product descriptions may be sent to third-party services.

Mitigation: Do not use confidential designs unless sharing data with PrintPal, WaveSpeed, and OpenRouter is acceptable.

Risk: URL inputs and downloaded files may be untrusted.

Mitigation: Avoid untrusted URLs and review downloaded image inputs before generation.

Risk: The workflows write files and support user-controlled output locations or filenames.

Mitigation: Use a dedicated workspace output directory and avoid custom filenames from untrusted sources.

Risk: The SEO workflow can start a localhost download server.

Mitigation: Keep the server bound to localhost unless deliberate network sharing is required, and stop it after downloads complete.

Risk: Optional Bambu printer commands can control physical hardware.

Mitigation: Require deliberate user confirmation before running printer-control, heating, motion, calibration, or raw G-code commands.

Risk: The security review notes broad process cleanup behavior.

Mitigation: Review active processes before using the SEO workflow on shared systems.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/plebbyd/skills/printpal-3d)
- [PrintPal API Reference](references/api-reference.md)
- [Bambu Lab Printer Control Guide](references/bambu-printer-guide.md)
- [PrintPal API Keys](https://printpal.io/api-keys)
- [WaveSpeed Access Key](https://wavespeed.ai/accesskey)
- [OpenRouter API Keys](https://openrouter.ai/keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; scripts may return JSON and generated files such as 3D models, images, SEO metadata, and ZIP archives.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and PRINTPAL_API_KEY for 3D generation; WAVESPEED_API_KEY and OPENROUTER_API_KEY enable optional image and SEO workflows.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
