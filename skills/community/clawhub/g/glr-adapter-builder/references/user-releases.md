# Deliver a trained stage to users

Developer wheels, reproduction bundles, and end-user installers are distinct.
`glr package export` is source-only. A `glr.model-bundle.v1` verifies provenance
and checksums; it does not install the adapter or inference runtime.

## Freeze a version

Assign a release ID, semantic version, training stage, supported environment/game
content version, observation/action contract, and model digest. `MODEL_CARD.md`
records measured capabilities, limitations, prerequisites and licenses. A release
may support only one stage; never imply general gameplay completion. Distinguish
synthetic evaluation from live acceptance.

Default to frozen inference: no optimizer updates, automatic training, or model
writes. Capture normalization and recurrent-state conventions and copy a stable
checkpoint. Continued training is a separate explicit mode with separate data
ownership and dependencies. A newer stage is a new immutable release.

## Assemble the runtime

Build application/adapter wheels, then freeze the inference launcher and pinned
dependencies using an appropriate maintained application packager. The launcher
uses bundled GLR for lifecycle operations, not another trainer/recovery control
plane. Users must not require Git, a compiler, source checkout, VX, or system
Python. Copying an editable development virtual environment is not freezing.

Stage only reviewed redistributable files:

```text
payload/
  app.exe                    # application-owned frozen inference launcher
  glr.exe                    # exact supported GLR release
  glr-hostd.exe               # matching host
  ...                        # runtime DLLs, installed application, configuration
  model/manifest.json        # verified glr.model-bundle.v1
  model/inputs/...
  model/artifacts/...
  LICENSE.txt
  MODEL_CARD.md
  evaluation.json
```

`evaluation.json` includes `stage`, `environment_id`, `protocol_version`, and
`evidence_kind` (`synthetic` or `live`), plus actual application evaluation results.
The builder checks identity, not the truth or adequacy of evaluation claims.
Scrub model inputs/source snapshots as well as outer configuration. Exclude private
endpoints, credentials, user logs and nonredistributable game files. Document game
and GPU-driver prerequisites rather than silently installing them.

## Build the Windows installer

Use the build-time SDK with a trusted pinned Inno Setup compiler:

```python
from pathlib import Path

from game_learning_runtime.user_release import (
    compile_windows_installer,
    prepare_windows_installer,
)

prepare_windows_installer(
    Path("payload"),
    Path("dist/stage-1"),
    release_id="example-player",
    version="1.0.0",
    stage="stage-1",
    launcher="app.exe",
)
installer = compile_windows_installer(
    Path("dist/stage-1"), compiler=Path("build-tools/Inno Setup 6/ISCC.exe")
)
```

Preparation snapshots and hashes files without executing them. Compilation
rechecks the payload and generated script. The installer is per-user, versioned,
and creates a shortcut. It does not auto-launch, download dependencies, modify
PATH, or recursively delete user data on uninstall. Sign and hash the final EXE
before publication; compiler success is not signing or installed-app acceptance.

This API packages a prepared runtime. It does not automatically freeze Python,
convert weights, supply a game bridge, or produce Linux/macOS installers. Do not
invent a `glr release` command; configure project build tasks using these APIs.

## Acceptance and migration

1. Verify wheel installation, then test the frozen launcher without the source
   checkout and with system Python/GLR removed from PATH.
2. Compile the actual installer, verify its signature/hash, install as a standard
   user into a path with spaces/non-ASCII characters, and test offline startup.
3. Check doctor, missing-prerequisite diagnostics, deterministic inference parity,
   absence of learner updates/model writes, and optional monitoring disabled.
4. Perform separate authorized live acceptance for supported targets. A synthetic
   fixture or mocked executable is not live or real-application acceptance.
5. Install a newer version side-by-side and test old-version launch and uninstall.
   Keep mutable user data outside versioned binaries and verify its preservation.
6. Record compiler/installer versions, digests, revision, dependency inventory,
   prerequisites and gate results. Missing startup/live evidence remains explicit.

Before upgrading, read `ARCHITECTURE.md`, `FRAMEWORK_MIGRATION.md`, and
`MIGRATIONS.md`. Validate model/adapter/config compatibility, dry-run state
conversion into a new destination, preserve old versions and data, and record
rollback effects on post-upgrade writes. Installation must not implicitly migrate
user data or begin training.

References: [Inno compiler](https://jrsoftware.org/ishelp/topic_compilercmdline.htm)
and [per-user installation](https://jrsoftware.org/ishelp/topic_setup_privilegesrequired.htm).
