# Installation

`myl` is a Python package. There are several ways to install it; pick the first one that fits the user's environment.

## How OpenClaw handles this

This skill declares `requires.bins: ["myl"]` in `metadata.openclaw`. OpenClaw checks for `myl` on `PATH` at skill load time and **silently filters this skill out** if it's missing, preventing the agent from invoking it without a working binary.

It also declares an `install` block:

```json
{ "id": "pipx", "kind": "pipx", "package": "myl", "bins": ["myl"] }
```

In OpenClaw's macOS Skills UI this surfaces a one-click install button. From the CLI the user installs `myl` themselves with one of the methods below — the install block is hint metadata, not an automated runtime installer.

For non-OpenClaw runtimes (Claude Code, generic), there's no automatic gating. Run `bash scripts/check_myl.sh` first to confirm `myl` is present.

## Detect what's already there

Always check before installing:

```bash
bash scripts/check_myl.sh
```

Or inline:

```bash
if command -v myl >/dev/null 2>&1; then
  echo "myl is installed: $(command -v myl) ($(myl --version 2>/dev/null || echo 'version unknown'))"
else
  echo "myl is not on PATH"
fi
```

If `myl` is present, skip the rest of this file and move on to `authentication.md`.

## Install paths, in order of preference

### `pipx` — recommended

Isolates `myl` and its dependencies from system Python. This is what the upstream README recommends and what the skill's `install` metadata suggests.

```bash
# Install pipx itself if missing (Debian/Ubuntu)
sudo apt update && sudo apt install -y pipx
pipx ensurepath

# Install myl
pipx install myl
```

On macOS:

```bash
brew install pipx
pipx ensurepath
pipx install myl
```

After `pipx ensurepath`, the user may need to restart their shell or `source ~/.bashrc` / `source ~/.zshrc` for `myl` to appear on `PATH`.

### `pip --user` — fallback when `pipx` isn't available

```bash
pip install --user myl
```

The binary lands in `~/.local/bin`, which must be on `PATH`. If not:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Nix flake — for Nix users

```bash
# One-shot run without installing
nix run github:pschmitt/myl -- --help

# Or add to a flake
```

### From source

```bash
git clone https://github.com/pschmitt/myl.git
cd myl
pipx install .
```

## Sandboxed agent runs

If the agent runs inside a Docker sandbox (OpenClaw `agents.defaults.sandbox.docker`), `myl` must be installed **inside the container** as well — the host bin doesn't satisfy the in-sandbox requirement. Add to `setupCommand`:

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "setupCommand": "pipx install myl || pip install --user --break-system-packages myl"
        }
      }
    }
  }
}
```

Sandbox installs also need network egress, a writable root FS, and root user inside the container. See OpenClaw's sandboxing docs for details.

## Confirm before installing

`myl` is a third-party Python package (GPL-3.0, by Philipp Schmitt). Before running an install command, tell the user what's about to happen:

> "I'll install `myl` via `pipx install myl`. This is a third-party CLI from https://github.com/pschmitt/myl. OK to proceed?"

Skip this confirmation only if the user has already explicitly approved installing tools in this session.

## Verify the install worked

```bash
command -v myl && myl --help | head -20
```

If `command -v myl` succeeds but `myl --help` fails, there's likely a Python interpreter or dependency mismatch. See `troubleshooting.md`.

## Updating

```bash
pipx upgrade myl       # if installed via pipx
pip install --user --upgrade myl   # if installed via pip --user
```
