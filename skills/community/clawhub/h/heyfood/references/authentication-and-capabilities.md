# Authentication and capabilities

Credentials never reach you. On the local surface they stay inside heyfood's
native credential backend; on the remote surface they are held by the host's
MCP client. Neither returns them through a tool result.

When authentication is missing:

1. Preserve the structured error code and user-facing handoff.
2. Ask the user to complete authorization using the exact mechanism named by
   the result — the login or registration command on the local surface, or the
   host's own MCP authorization step on the remote surface.
3. Never ask the user to paste tokens, API keys, device codes, or refresh
   material into chat.
4. Retry only after the user reports completion and a status or capability read
   confirms readiness. On the remote surface, where no status tool exists,
   retry the original tool once and accept its answer.

When scopes are missing, present the exact required scopes and the
authorization upgrade path. OAuth refresh cannot widen authority. A remote
authorization is granted a fixed scope set at connection time; a tool outside
that set will keep refusing, and repeating the call will not change it.

Treat these states distinctly:

- unauthenticated;
- authenticated but insufficient scope;
- capability not advertised;
- capability deferred by the client;
- capability absent from this surface entirely (see the boundaries table in
  SKILL.md — Grocery and Menu Watch are remote-absent, not remote-unauthorized);
- service unreachable; and
- uncertain credential rotation or reconciliation.

Never guess one into another. In particular, never report a capability that
does not exist on your surface as a permission problem the user could fix by
authorizing again.
