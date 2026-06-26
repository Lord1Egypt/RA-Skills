# Installation

This page covers production installs, local development setup, and common environment issues.

## Requirements

- Python `>=3.8`
- `pip` (latest stable recommended)
- Network access to Peerberry API endpoints at runtime

## Choose Your Install Mode

## Standard Install (PyPI)

```bash
pip install peerberry-sdk
```

Use this for normal application usage when you do not need optional two-factor helpers.

## Install With OTP Support

```bash
pip install "peerberry-sdk[otp]"
```

This adds `pyotp`, required only when you pass `tfa_secret` to the client.

## Install With Documentation Tooling

```bash
pip install "peerberry-sdk[docs]"
```

Use this if you want to build the local documentation site with Zensical.

## Recommended Virtual Environment Setup

Create and activate an isolated environment before installation:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install peerberry-sdk
```

## Verify Installation

```python
from peerberry_sdk import PeerberryClient

print(PeerberryClient)
```

If the import succeeds, installation is complete.

## Local Development Install (Repository)

From repository root:

```bash
pip install -e ".[otp,docs]"
```

This enables editable mode for package development plus optional extras.

## Build Documentation Locally

After installing docs dependencies:

Zensical uses the native `zensical.toml` configuration in this repository.

```bash
zensical build
```

Useful alternatives:

```bash
zensical serve
```

## Troubleshooting

## `ModuleNotFoundError: No module named pyotp`

Cause: Using `tfa_secret` without OTP extras.

Fix:

```bash
pip install "peerberry-sdk[otp]"
```

## `zensical: command not found`

Cause: Docs extras not installed in current environment.

Fix:

```bash
pip install "peerberry-sdk[docs]"
```

## Importing wrong interpreter/environment

Cause: `pip` and `python` are from different environments.

Fix: use interpreter-coupled install commands:

```bash
python -m pip install peerberry-sdk
python -c "from peerberry_sdk import PeerberryClient; print(PeerberryClient)"
```

## Next Steps

1. [Quickstart](quickstart.md)
2. [Authentication Guide](../guides/authentication.md)
3. [Configuration Guide](../guides/configuration.md)
