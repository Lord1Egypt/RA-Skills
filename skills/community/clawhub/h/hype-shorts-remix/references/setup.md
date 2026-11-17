# Setup

Use a Skill-capable agent with local files, a terminal and a way to view media. Check:

```sh
node --version
ffmpeg -version
ffprobe -version
```

Node.js 22 or newer is required. FFmpeg needs H.264 encoding and the `subtitles` filter for
captioned renders. Prepare a normal FFmpeg build through the host's supported installation path
if missing. The package's scripts use Node built-ins; there is no npm installation step.

Set `SKILL_DIR` to the directory containing this `SKILL.md`. Run project commands from the user's
chosen production directory. Keep source material and original files intact.

A useful project layout is:

```text
reference.mp4
brief.md
reference-analysis.md
script.md
analysis/
requests/
jobs/
assets/
edit.json
final.mp4
final.mp4.render.json
```

`inspect` creates its own new analysis directory. Prepare `requests`, `jobs` and `assets` as needed.
Job receipts may contain signed media URLs; keep them private, out of source control and shared
deliverables. The final editable project can refer to downloaded media instead.

For generation, use an [APIsRouter account](https://apisrouter.com) with a valid key and available
balance. Have the host's secret facility expose the key as `APISROUTER_API_KEY` to the Node process.
Avoid raw keys in command arguments, `.env` files shipped with the project, terminal history or chat.
The API runner calls `https://api.apisrouter.com/v1`.

To try local composition, render the supplied example to a new output file:

```sh
node "$SKILL_DIR/scripts/media.mjs" render \
  --project "$SKILL_DIR/examples/edit.json" --output ./rain-remix.mp4
```

Local inspection and rendering do not generate API charges. Model discovery reads the account's
catalogue; it does not prove that a generation will succeed. Read current account pricing and the
requested generation scope before submitting a paid request.
