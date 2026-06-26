# Environment note

## Scope split

This skill covers **workflows after the official Obsidian CLI already works**.

That includes:
- read/query operations
- write/update operations
- post-write Git sync
- limited fallback file writing for supported write flows

It does not cover installing or adapting the official CLI runtime itself.

## Headless/server environments

For headless servers, VPS hosts, or root-heavy Linux environments, pair this skill with:

- `obsidian-official-cli-headless`
- Reference: https://clawhub.ai/DarinRowe/obsidian-official-cli-headless

Use that skill first when the environment still needs:
- official Obsidian installation
- non-root runtime setup
- Xvfb or virtual-display adaptation
- `obs` wrapper setup
- vault access wiring

After the official CLI is working, return to this skill for actual note workflows.

## Desktop environments

If the official CLI already works on desktop Linux, macOS, or Windows, use this skill directly. No server-specific setup is required here.
