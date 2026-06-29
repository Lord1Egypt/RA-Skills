# Pi Packages Reference

## Installation

```bash
pi install npm:@scope/pkg@1.0.0       # npm
pi install git:github.com/user/repo@v1 # git
pi install https://github.com/...      # URL
pi install /absolute/path              # local absolute path
pi install ./relative/path             # local relative path
pi install -l npm:@foo/bar             # project-level (-l = local)
pi remove npm:@foo/bar                 # uninstall
pi list                                # list
pi update                              # update all (skip pinned versions)
pi update --self                       # update pi
pi config                              # enable/disable resources
pi -e npm:@foo/bar                     # temporary trial (not saved to config)
```

## Package Creation

### Manifest Method

```json
{
  "name": "my-package",
  "keywords": ["pi-package"],
  "pi": {
    "extensions": ["./extensions"],
    "skills": ["./skills"],
    "prompts": ["./prompts"],
    "themes": ["./themes"],
    "video": "https://example.com/demo.mp4",
    "image": "https://example.com/screenshot.png"
  }
}
```

- `video`: MP4, hover auto-play on desktop, click for fullscreen
- `image`: PNG/JPEG/GIF/WebP static preview
- Paths support glob and `!exclusion`

### Convention Directory

When no manifest is present, auto-discovery: `extensions/` (ts/js), `skills/` (SKILL.md), `prompts/` (md), `themes/` (json)

## Dependencies

- Runtime dependencies go in `dependencies`
- Core packages (pi-ai, pi-agent-core, pi-coding-agent, pi-tui, typebox) go in `peerDependencies: {"*"}`, not bundled
- Other pi packages go in `dependencies` + `bundledDependencies`, referenced via `node_modules/` paths

## Resource Filtering

```json
{
  "packages": [
    "npm:simple",
    {
      "source": "npm:complex",
      "extensions": ["extensions/*.ts", "!extensions/legacy.ts"],
      "skills": [],
      "prompts": ["prompts/review.md"]
    }
  ]
}
```

- `+path` force-include, `-path` force-exclude, `!pattern` exclude match
- Filtering layers on top of manifest

## Scope & Deduplication

- Global + project same package → project-level wins
- npm deduped by package name, git by repo URL, local by absolute path
- git@ref pins tag/commit, `pi update` won't move
- Git packages install dependencies with `npm install --omit=dev`