# Runbook Reference

Base is the active production-candidate validation chain. BSC remains reviewed historical empty-scope context only, and `allowMainnetExecution` stays `false` by default.

Operator sequence:

1. verify registry
2. snapshot current state
3. generate plan
4. verify pinned `erc-mandated-mcp` install, official factory address, and required tool surface
5. collect signature outside host
6. execute via MCP
7. reconcile and archive report
