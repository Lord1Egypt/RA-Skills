## Description:

Assists with creating, scripting, organizing, debugging, and packaging Garry's Mod addons, with guidance for Lua code, assets, and addon structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lzmjlrt](https://clawhub.ai/user/lzmjlrt)

### License/Terms of Use:


## Use Case:

Developers and creators use this skill to plan, write, troubleshoot, and package Garry's Mod addons. It helps organize addon folders, reason about client/server/shared Lua realms, and verify Garry's Mod API references before using them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trigger description may invoke the skill for Lua prompts where Garry's Mod is only loosely relevant.

Mitigation: Confirm that the user's task is for Garry's Mod addon development before applying GMod-specific file layout, realm, or API guidance.

Risk: Garry's Mod API URLs or Lua realm assumptions may be incorrect if guessed.

Mitigation: Use the Facepunch Garry's Mod wiki search/index flow and verify the target API page before relying on a function, hook, or realm-specific behavior.

Risk: Generated addon code or packaging advice may still fail in-game because of runtime errors, missing files, or client/server realm mismatches.

Mitigation: Test the addon in Garry's Mod, check console errors, and use the included common-error and Lua realm references to debug before distribution.

Risk: Models, textures, sounds, or other sourced content may have incompatible licenses.

Mitigation: Verify asset licenses and distribution rights before packaging or publishing an addon.

## Reference(s):

- [Lua Folder Structure](references/addon-structure.md)
- [Common Errors](references/common-error.md)
- [States / Realms](references/state-exp.md)
- [Garry's Mod Wiki](https://wiki.facepunch.com/gmod)
- [GMod Addon Maker on ClawHub](https://clawhub.ai/lzmjlrt/skills/gmod-addon-maker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Lua code snippets, file paths, commands, and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend API lookups, addon file layouts, in-game testing steps, and asset licensing checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
