## Description: <br>
AI polaroid photo generator that creates retro instant-film photos with vintage color, film grain, and 1970s-1980s aesthetics through the Neta AI image generation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blammectrappora](https://clawhub.ai/user/blammectrappora) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate retro Polaroid-style image URLs from text prompts, optionally selecting image dimensions or supplying a reference image UUID for style inheritance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and related generation inputs are sent to the Neta service. <br>
Mitigation: Avoid confidential or regulated content unless the provider's privacy and retention terms are acceptable. <br>
Risk: The API token is passed on the command line, which can expose it through shell history or process listings. <br>
Mitigation: Prefer short-lived or restricted tokens and avoid sharing logs, command history, or terminal output containing token values. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blammectrappora/polaroid-photo-generator) <br>
- [Neta API token page](https://www.neta.art/open/) <br>
- [Neta image generation endpoint](https://api.talesofai.com/v3/make_image) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text image URL printed to stdout, with progress and errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Neta API token; accepts a prompt, size option, and optional reference image UUID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
