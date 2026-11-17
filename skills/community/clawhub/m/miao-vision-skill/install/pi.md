# Pi

Install the Miao Vision Pi package:

```bash
pi install npm:@miao-vision/pi
```

Start Pi in the working directory, then invoke `/skill:miao-vision`. Use
`/miao-viewer` when you want to monitor a run, compare versions, request a
scoped revision, or export a selected version.

The package checks for the CLI version pinned by `cli-compatibility.json`. It
does not download or upgrade the CLI without approval. The Review Viewer binds
only to `127.0.0.1`; its URL is not a public sharing URL.

## Global CLI and exports

All workflows use the compatible global `miao-viz` on PATH. If it is missing
or incompatible, approve installation of the fixed recommended npm version.
The package never installs a CLI or browsers silently.

Run `/miao-viewer setup` for PNG/PDF and existing deck PPTX export. After
confirmation it reuses Pi dependencies, or installs fixed Playwright into
`~/.miao-vision/playwright`, and prepares matching Chromium. It does not modify
your working project's dependencies. Run `/miao-viewer status` to see the actual
CLI path, export environment, and current Viewer URL. The port changes on restart.
