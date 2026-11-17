# Local Review Viewer

Use this reference when the user asks to monitor, review, or inspect a Miao
Vision generation run. The Viewer manages local deliverables, compares
versions, and prepares targeted revision requests. It also shows evidence
coverage, issues, and artifact previews.
Its loopback URL is not a public sharing URL.

The current Codex plugin registers the skill only. It does not configure the
Viewer MCP server or open the Viewer automatically. Start the connection
explicitly when the host supports it, then open the returned local URL in the
host's embedded browser. Do not describe the Viewer as active until it starts.

The Pi package includes an Extension that manages this MCP connection. In Pi,
use `/miao-viewer` to start or reconnect to the Viewer, `/miao-viewer status`
to inspect it, and `/miao-viewer stop` to stop it. Pi users do not configure the
Viewer MCP server separately. The command returns a loopback URL and does not
open an external browser automatically.

- `miao-viz review serve` starts only the local Viewer at
  `http://127.0.0.1:43179/` and returns its URL. Use `--port <n>` to override
  the fixed default, or `--port 0` to choose an available port.
- `miao-viz review mcp` starts the Viewer on the same fixed port and exposes the MCP tools
  `open_miao_vision_viewer` and `run_miao_viz` through stdio. This requires a
  separately configured MCP connection in the host.
- `open_miao_vision_viewer` returns the URL; it does not open a Codex browser
  panel by itself. `run_miao_viz` launches a report, deck, or article workflow
  and tracks it in the Viewer.
- For a CLI workflow started separately, pass `--review-url` and
  `--review-run-id` to publish progress to an already running Viewer. Pass
  `--review-parent-run-id` when revising an earlier run. These flags do not
  start a Viewer.

The Viewer may expose only the selected artifact root through its loopback
server. Keep source data local and continue the CLI workflow if the Viewer
stops or is unavailable. Deliver the primary artifact even if review events
could not be published.

## Sandbox and local network access

A running Viewer in a browser does not prove that a sandboxed CLI process
can reach it. Before a Viewer-backed render, request `<viewer-url>/api/health`
from the same execution environment as the render, with a short timeout
(for example, `curl --fail --silent --show-error --max-time 3
http://127.0.0.1:43179/api/health`). Use the actual returned Viewer URL;
the response must contain `ok: true`.

If sandbox policy blocks loopback access, use the host's supported permission
mechanism before rendering. In Codex, retry the probe with `exec_command`
using `sandbox_permissions: "require_escalated"` and a justification such as
"Access the local Review Viewer to register the generated artifact."
Once access is confirmed, execute the render with the same permission setting
and include `--review-url <viewer-url>` and `--review-run-id <stable-id>`.
Permission for a probe does not make later sandboxed commands unrestricted.
Do not change the port or bind the Viewer to `0.0.0.0` to work around policy.

A connection refusal can mean the Viewer is stopped or the URL is wrong;
check the Viewer process and returned URL rather than assuming a sandbox
denial. An HTTP error means a server responded and requires endpoint/service
diagnosis. A generic connection failure alone does not establish the cause.
If an already configured local MCP connection is available, `run_miao_viz`
can launch the render from that service; its process must also be able to
reach the Viewer.

After rendering, GET `<viewer-url>/api/runs/<encoded-run-id>` from the permitted
environment and confirm that the run's artifact points to the generated output.
CLI render success alone does not confirm publication: review network failures
currently do not fail rendering. If host permission is denied or unavailable,
deliver the HTML and explicitly report that Viewer registration was not
completed. Do not repeatedly rerender in the same blocked environment or claim
that the artifact is visible in the Viewer.

The version view compares any two runs in the same revision family. Review
history survives a Viewer process restart in a local cache. For reports, the
edit view maps titles, charts, and insights to Spec paths. Decks map each slide,
title, claim, and chart to `slides[n]` paths. Posters map semantic title,
subtitle, chart, and footer areas to their ReportSpec paths. Reviewers can select
multiple targets and one registered theme, enter one request, then inspect a
RevisionPlan listing the proposed changes, preserved content, validations, and
risks. Confirmation alone never changes a file.

After confirmation, an Agent reads the revision with
`get_miao_vision_revision` and submits an allowlisted `PatchSet` through
`apply_miao_vision_revision`. The local service rejects unknown paths, arbitrary
files, unregistered themes, and protected data, evidence, provenance, and
encoding paths. A successful application writes a versioned child Spec and
artifact linked to its parent run. The Viewer is not a PPT, canvas, drag-drop,
or direct Spec editor.

Choose an artifact in the sidebar, select a version, and use **Export version**
to download its rendered artifact:
reports support PDF and PNG; decks support PDF and image-based PPTX; posters
support PNG. Each PPTX slide is a full-slide image, so its individual text and
charts are not editable in PowerPoint. Export reuses the selected version's
HTML and does not rerun data analysis or queries. A report with the poster
layout is recognized as a poster even though its run kind is `report`.

## Export environment

Use the same global CLI path as ordinary generation; check with
`node scripts/check-miao-viz.mjs --viewer --print-path`. Pi users run
`/miao-viewer setup` and confirm installation when prompted. Other hosts run
`node scripts/setup-export.mjs --host <host>` to check, then add `--install`
only after approval. Pass its returned `root` as `MIAO_VIZ_PLAYWRIGHT_ROOT`
when launching the Viewer. Missing dependencies do not prevent HTML preview.
The export menu reports setup requirements. Export errors retain their specific
code and repair action; export requests never install dependencies.
