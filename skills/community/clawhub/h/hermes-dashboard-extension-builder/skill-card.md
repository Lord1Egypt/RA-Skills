## Description: <br>
Generate and validate Hermes-style dashboard extension scaffolds: themes, plugins, custom tabs, slots, and backend API route manifests for OpenClaw/Hermes agent teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and dashboard integrators use this skill to generate a packaged Hermes/OpenClaw dashboard extension scaffold from CLI arguments or a JSON spec, then review the manifest, frontend stub, backend route stub, and validation report before integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated dashboard scaffold files could be integrated before their HTML, backend route, permissions, and API path are reviewed. <br>
Mitigation: Generate into a staging directory and inspect the frontend stub, backend Python, permissions, and API route values before using the scaffold in a real dashboard. <br>
Risk: A malformed or overbroad extension spec can produce a review-needed validation result. <br>
Mitigation: Use validate-only mode when checking specs and address validation findings such as bad names, non-/api routes, or wildcard permissions before writing or integrating output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stevojarvisai-star/hermes-dashboard-extension-builder) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Generated scaffold files with JSON manifests and validation report, plus command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes only to the selected output directory; validate-only mode checks a spec without writing scaffold files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
