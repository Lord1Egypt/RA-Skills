# Morpho Base Operator

Use this skill to operate a Base-first Morpho mandated vault workflow in a registry-first way.

The active production-candidate validation chain is Base. BSC is retained only as reviewed historical empty-scope context, and `allowMainnetExecution` stays `false` by default.

## Required sequence

1. Load the configured registry file.
2. Verify registry addresses before planning.
3. Snapshot current state.
4. Build a deterministic plan for a registered market only.
5. Collect the authority signature outside the host.
6. Execute through the pinned mandated MCP stack.
7. Reconcile and archive the execution report.

Never perform dynamic market discovery in the write path.

Users must supply their own local configuration (RPC, operator private key, and any active vault identifiers) outside the published skill bundle.
