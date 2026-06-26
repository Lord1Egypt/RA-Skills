# Mandated MCP Install UX Design

## Goal

Make `mandated-vault` and vault-overlay setup understandable for non-expert users by explicitly surfacing the external MCP dependency, while still offering a one-click path to install `erc-mandated-mcp` and auto-fill `ERC_MANDATED_MCP_COMMAND`.

## Current State

- PredictClaw integrates with the mandated-vault control plane through `lib/mandated_mcp_bridge.py`.
- The bridge starts an external subprocess from `ERC_MANDATED_MCP_COMMAND` rather than embedding the MCP runtime into the skill process.
- `lib/config.py` already provides a default launcher name of `erc-mandated-mcp`.
- Docs already explain that pure `mandated-vault` requires a working MCP command, but the product UX still assumes users understand how to install and wire that dependency.

## Problem

Users hear that PredictClaw "supports" mandated-vault and assume the MCP runtime is already bundled. In reality, the skill only knows how to talk to the runtime once it exists on the machine. That mismatch creates three failure modes:

1. Users select `mandated-vault` and hit a missing-binary error later in the flow.
2. Users believe they must manually fill `ERC_MANDATED_MCP_COMMAND`, even when the default command name would work after install.
3. Users cannot tell which settings can be auto-filled and which vault credentials still require explicit confirmation.

## Product Constraints

- Recommended UX path: explicit prompt plus one-click install plus automatic backfill.
- One-click install only covers the MCP runtime itself.
- Missing prerequisites such as Node, npm, uvx, or other host tooling should fail clearly, but should not be auto-installed.
- Vault identity, derivation inputs, authority/executor keys, and chain settings remain explicit user-controlled values.
- The system must fail closed if the MCP command is unavailable, unhealthy, or missing required tools.

## Options Considered

### Option A: Explicit prompt + one-click install + auto-backfill (recommended)

When the user selects pure `mandated-vault` or `predict-account + ERC_MANDATED_*` overlay, OpenClaw immediately checks whether a usable MCP command exists. If not, it explains the dependency and offers a one-click install for `erc-mandated-mcp`. On success, it writes the resolved launcher back into `ERC_MANDATED_MCP_COMMAND` and resumes the flow.

Pros:
- Best balance of usability and explicitness.
- Keeps failure messages local to mode selection instead of surfacing them later during vault actions.
- Avoids making users hand-edit the command in the common case.

Cons:
- Requires host-side installer and detection logic.

### Option B: Explicit prompt + manual install only

The host explains the dependency and stops. Users must install `erc-mandated-mcp` themselves and then fill or confirm the launcher.

Pros:
- Smallest implementation surface.
- Lowest automation risk.

Cons:
- High drop-off for non-expert users.
- More support burden because the most common case still feels broken.

### Option C: Silent automatic install + silent backfill

The host installs the MCP runtime as soon as users select the mode, with minimal explanation.

Pros:
- Lowest apparent friction.

Cons:
- Too implicit for a control-plane dependency.
- Harder to reason about failures, PATH issues, and security expectations.
- Violates the desired product boundary for sensitive vault flows.

## Recommended Design

Use Option A.

The UX should treat the mandated MCP as an external runtime dependency that PredictClaw can detect and optionally install, not as an invisible built-in component.

### User Flow

1. User selects `mandated-vault` or overlay mode.
2. Host displays a short explanation:
   - PredictClaw includes the bridge logic.
   - This mode still requires an external mandated-vault MCP runtime.
   - The host can install that runtime now and auto-fill the command entry.
3. Host checks for a usable launcher in this order:
   - Explicit `ERC_MANDATED_MCP_COMMAND` from current config
   - Default launcher `erc-mandated-mcp`
4. If a launcher works, host stores that resolved command and continues.
5. If no launcher works, host offers a one-click install of `erc-mandated-mcp`.
6. After successful install, host re-runs detection and writes the resolved launcher into `ERC_MANDATED_MCP_COMMAND`.
7. Host continues into vault-specific configuration.

### Auto-Fill Boundaries

Auto-fill:
- `ERC_MANDATED_MCP_COMMAND` after successful detection or install

Do not auto-fill:
- `ERC_MANDATED_VAULT_ADDRESS`
- derivation tuple fields
- authority/executor private keys
- chain-sensitive vault parameters unless the user explicitly confirms them

### Error Handling

#### Missing command

Show: mandated-vault mode needs an external MCP runtime and none was found.

Action:
- install now
- retry detection
- switch back to another wallet mode

#### Missing prerequisite

Show:
- MCP install could not continue because a prerequisite is missing
- exactly which prerequisite is missing
- the recommended manual install command

Do not auto-install the prerequisite.

#### Command starts but runtime is unhealthy

Show:
- launcher was found but the MCP runtime failed its health check or is missing required tools
- short stderr or missing-tool summary

Do not proceed with vault mode.

## Copy Recommendations

### Mode-selection prompt

"This mode uses PredictClaw's mandated-vault bridge and an external MCP runtime. We can install `erc-mandated-mcp` now and auto-fill the command entry for you."

### Success copy

"Mandated MCP runtime is ready. `ERC_MANDATED_MCP_COMMAND` has been set to `<resolved command>`. Continue with vault configuration."

### Failure copy

"PredictClaw can talk to a mandated-vault MCP runtime, but none is currently available. Install `erc-mandated-mcp` now, or switch to another wallet mode."

## Implementation Notes

- Reuse the existing bridge and config default instead of inventing a second launcher setting.
- Add a host-side preflight before users reach any pure `mandated-vault` command flow.
- Store the resolved command exactly as executed so custom launchers remain supported.
- Keep documentation aligned: "integrated bridge" must never be phrased as "bundled runtime".

## Verification Expectations

- Selecting `read-only`, `eoa`, or plain `predict-account` does not trigger MCP installation.
- Selecting pure `mandated-vault` triggers MCP detection immediately.
- Successful install backfills `ERC_MANDATED_MCP_COMMAND`.
- Missing prerequisites produce explicit guidance and no hidden installs.
- Broken MCP runtime fails closed with actionable diagnostics.
