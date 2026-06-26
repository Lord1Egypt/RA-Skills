# Non-Subscriber Mode Guide

Use `--non-essesseff-subscriber-mode` if you don't have an essesseff subscription. This mode:

- Does **not** use the essesseff API.
- Clones template repos from GitHub directly (they are public).
- Performs literal, case-sensitive string replacement on all repo contents.
- Creates new repos in your GitHub org using the GitHub API.
- Pushes the replaced content to the new repos.

## What Gets Replaced

The script performs two string replacements across all cloned file contents and filenames:

1. `template_org_login` (the template's GitHub org, e.g. `essesseff-hello-world-go-template`) → `GITHUB_ORG`
2. The template's `replacement_string` from `bundled-global-templates.json` (e.g. `hello-world`) → `APP_NAME`

Replacement is **literal and case-sensitive**. Variants like `HelloWorld`, `hello_world`, or `HELLO-WORLD` will not be replaced.

## After the Run

Cloned repos land in the current working directory. They are **not deleted** after push, so you can inspect them:

```bash
ls -d my-new-app*/
```

Check a repo to verify replacements:
```bash
grep -r "hello-world" my-new-app/ | head -20
```

If you see unexpected occurrences, the template may use naming variants not covered by the two replacement strings.

## Bundled Templates

Available templates are in `bundled-global-templates.json` in this repo. Filter by language:

```bash
./essesseff-onboard.sh --list-templates --language go --non-essesseff-subscriber-mode --config-file .essesseff
```

Languages available: `go`, `node`, `python`, `java`.
