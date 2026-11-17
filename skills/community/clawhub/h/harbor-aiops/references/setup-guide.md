# Setup

Install from the local source with `uv sync --dev`, then run `uv run harbor-aiops init`. The wizard requests a Harbor hostname, username or robot account, optional CA PEM, and a hidden password. It writes `~/.harbor-aiops/config.yaml` and encrypted `secrets.enc`. Run `uv run harbor-aiops doctor` to check access.

For an existing config, use `uv run harbor-aiops secret set <target>`. HTTPS and certificate validation are the defaults. A loopback HTTP lab can be configured manually; do not send Basic credentials over plaintext networks.

A read-only Harbor account may not access system volumes or GC history. `harbor_diagnose` will mark those probes as failed rather than saying the instance has no volume or GC data. Scan, tag creation and tag deletion require project write permissions; use a narrowly scoped robot account when testing them.
