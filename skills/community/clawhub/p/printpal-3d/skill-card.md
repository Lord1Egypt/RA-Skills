## Description: <br>
Generate 3D models for 3D printing from images or text prompts using PrintPal API, plus SEO product listing generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plebbyd](https://clawhub.ai/user/plebbyd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, makers, and marketplace sellers use this skill to turn image or text inputs into printable 3D model files and to generate SEO product listing assets for 3D printed items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be used with paid services and credits. <br>
Mitigation: Use dedicated PrintPal, WaveSpeed, and OpenRouter keys with spending limits and rotate or revoke them if exposed. <br>
Risk: Images, prompts, and product details may be sent to third-party services. <br>
Mitigation: Avoid sensitive images, customer data, or proprietary product details unless those disclosures are acceptable. <br>
Risk: The SEO workflow may start a local download server and terminate matching serve_files.py processes on the selected port. <br>
Mitigation: Review the workflow before running it, keep the server bound to localhost unless network access is required, and choose a port that does not conflict with other work. <br>
Risk: The Bambu printer guide covers commands that can physically control printer hardware. <br>
Mitigation: Use the separate Bambu CLI only after confirming printer readiness, LAN credentials, and physical safety conditions. <br>


## Reference(s): <br>
- [PrintPal API Reference](references/api-reference.md) <br>
- [Bambu Lab Printer Control Guide](references/bambu-printer-guide.md) <br>
- [PrintPal API Keys](https://printpal.io/api-keys) <br>
- [WaveSpeed Access Keys](https://wavespeed.ai/accesskey) <br>
- [OpenRouter API Keys](https://openrouter.ai/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [3D model files, generated image files, ZIP packages, JSON status output, Markdown guidance, and local download URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default 3D output is STL in printpal-output; SEO output includes metadata text, product photos, and a ZIP package.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
