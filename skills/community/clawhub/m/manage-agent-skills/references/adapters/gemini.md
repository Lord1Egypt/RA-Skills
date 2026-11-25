# Gemini CLI

[Gemini CLI](https://geminicli.com/docs/cli/skills/) is a separate host with native
skill management and user/workspace scopes. Do not treat it as Antigravity.
Version 1.1.1 adds a separate Gemini adapter; v1.0.1 did not include it.
It discovers user/workspace `.gemini/skills` and `.agents/skills`, honors
`GEMINI_CLI_HOME`, and edits `skills.disabled` in one selected JSON/JSONC file.
`--gemini-scope workspace` uses `<cwd>/.gemini/settings.json`. Global
`skills.enabled=false` in that file blocks enable. Built-in/extension roots,
system configuration and trust gates are not replicated. Settings-file edits
require a restart according to the [configuration reference](https://geminicli.com/docs/reference/configuration/);
`/skills reload` alone is not evidence that an externally edited config was read.

## Operational notes

`--platform gemini` manages `skills.disabled` in user settings;
`--gemini-scope workspace` selects `<cwd>/.gemini/settings.json`. Local workspace,
user and shared roots are indexed. Built-in/extension skills and other settings
layers require host verification. A global `skills.enabled=false` blocks enable.
