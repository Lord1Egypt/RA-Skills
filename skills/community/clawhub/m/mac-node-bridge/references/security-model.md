# Security Model

Use this file when designing or publishing a Linux-gateway-to-mac-node skill.

## 1. Authentication And Trust

- Use strong, scoped credentials.
- Prefer one SSH identity per gateway or per trust domain.
- Do not give every gateway the same private key if you can avoid it.
- Treat each Mac node as a separate trust boundary.
- The Mac side must prove identity before the Linux gateway accepts orchestration signals or wrapper execution.

Recommended baseline:

- dedicated SSH key for gateway-to-node wrappers
- non-root Mac account
- known-hosts pinning when feasible
- one wrapper per tool, not a generic remote shell

## 2. Least Privilege

Each gateway, agent, or wrapper should get only the permissions it needs.

Good examples:

- read-only wrapper for `remindctl lists`
- send-only wrapper for `imsg send`
- explicit binary path for `gh` or `brew`

Bad examples:

- unrestricted `ssh host bash`
- broad wrapper that forwards arbitrary shell input
- shared credentials reused across unrelated nodes

## 3. Auditing

Every cross-host action should be attributable.

At minimum, log:

- who created or rotated the wrapper
- when the wrapper was installed
- which node owns the tool
- which key or trust path was used
- what rollback command removes the integration

Published skills should also document:

- where the wrapper is installed
- where secrets live
- which host is authoritative

## 4. Rollback

A broken bridge should be removable without breaking the whole cluster.

Design for:

- deleting a single wrapper script
- revoking a single SSH key
- disabling one published skill without touching OpenClaw core
- leaving local node operation intact when remote orchestration is disabled

## 5. Compatibility Surface

Keep the gateway-to-node contract small and stable.

Recommended contract:

- one wrapper
- one explicit binary
- simple argv passthrough
- stable stdout/stderr behavior

Avoid:

- hidden environment coupling
- undocumented side effects
- tool discovery that changes behavior across nodes

## 6. Safe Failure Mode

If the Mac node is unavailable:

- fail with a clear error
- leave the gateway running
- do not block unrelated local tools
- prefer degraded local operation over total failure

Examples:

- `imsg` wrapper unavailable: iMessage automation pauses, gateway remains healthy
- `remindctl` wrapper unavailable: reminder workflows report unavailable, browser/system nodes continue

## 7. Publication Guidance

When publishing a community skill:

- document the trust model clearly
- state which parts are Linux-only, macOS-only, or mixed
- say exactly what the user must install on the Mac
- say exactly what the gateway must store
- do not imply that a Linux gateway natively supports a macOS CLI
