## Description: <br>
Add, refine, calibrate, or migrate OpenClaw Control UI themes by patching the installed bundled frontend assets in dist/control-ui/assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ailough](https://clawhub.ai/user/ailough) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add custom OpenClaw Control UI themes, tune component styling, or migrate an existing custom theme across OpenClaw upgrades while preserving backups and verifying the live bundle structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit installed OpenClaw UI bundles and a mistaken path or patch point could break the local UI. <br>
Mitigation: Confirm the active OpenClaw install before patching, create backups first, and restore the original JS/CSS bundles if the UI degrades. <br>
Risk: Theme migration can fail if old bundle structures are reused after an OpenClaw upgrade. <br>
Mitigation: Rediscover the new bundle's allowed set, card list, alias map, and resolver before editing; avoid broad heuristic replacements. <br>
Risk: Untrusted or malformed theme ids can increase the chance of unsafe or incorrect bundle edits. <br>
Mitigation: Use trusted, simple, stable theme ids and verify the resulting theme selection, light/dark toggle, and built-in themes after patching. <br>


## Reference(s): <br>
- [Bundle Patch Points](references/patch-points.md) <br>
- [Theme Migration Checklist](references/theme-migration-checklist.md) <br>
- [Theme Input to Token Mapping](references/token-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, CSS and JavaScript snippets, and file path summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include patched bundle paths, theme ids, CSS selectors, backup directories, and verification notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
