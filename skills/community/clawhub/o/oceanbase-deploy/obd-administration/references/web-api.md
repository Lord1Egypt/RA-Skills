# OBD Web and Web API

OBD Web is a human-facing controller UI. Its HTTP API shares the service process but is a separate automation interface. Do not turn a request for one interface into permission to use the other, and do not make either interface part of an ordinary cluster operation by default.

## Human-Facing Web

When the user explicitly asks for OBD Web, the Agent may start or stop the exact Web process, verify that the page and its static resources are reachable through the intended address, and give the URL to the user. The Agent must not operate the graphical page on the user's behalf.

Before start, read the installed `obd web --help` and resolve the controller identity, `OBD_HOME`, process owner, bind address, port, foreground/background behavior, existing Web process, active tasks, and exact stop method. Preserve user-specified values; otherwise use only defaults proved by the installed build. OBD Web may lack reliable built-in access control. Confirm that its port is not exposed to an untrusted network, and never open a firewall/security-group port or configure a proxy as an implicit part of starting Web.

After start, verify the real process owner and listener plus successful retrieval of the root page and referenced static resources. Report the URL and actual listener scope. Do not interpret page availability as deployment health.

The Web process can hold controller or deployment locks for its lifetime in some builds. Before a conflicting CLI operation, identify the actual lock owner and active Web tasks. Never disable locking to bypass it. Stop only the exact Web process owned by the current task or one the user explicitly asked to stop, then verify listener and lock release.

## Credential-Bearing Requests

Verified 4.7-era source can log the full URL, query parameters, and raw request body. Before a credential-bearing request, prefer a supported secret reference or protected CLI path; otherwise minimize the payload, protect server and proxy logs, use scoped credentials, and rotate them when the logging boundary requires it. Never copy credential-bearing request bodies into reports or delete broad logs as cleanup.

## Explicit Web API Work

Invoke the Web API only when the user explicitly requests API work. Establish endpoints, methods, schemas, task states, and recovery actions from version-matched official documentation or an explicit route/schema surface in the installed server. Do not infer an API from another release or reverse-engineer bundled browser JavaScript merely to manufacture an unsupported automation path. If no reliable contract exists for the requested endpoint, report it as unsupported for that build.

For each mutation:

1. capture the exact resource and current state;
2. review the redacted payload and expected transition;
3. run a provided precheck when available;
4. obtain operation-specific authorization independently of listener-start authorization;
5. preserve the returned task ID and poll to a terminal state;
6. verify the resulting controller, deployment, component, or data-plane state outside the acceptance response.

An HTTP success or “accepted” response is not completion. If a request times out, errors, or leaves a non-terminal task, inspect server-side state before retrying; a duplicate-resource response can mean the first submission succeeded. Do not issue a conflicting CLI command while a Web/API task for the same resource is active, delete a server-side record to force a retry, or replay a non-idempotent request until final state is known.

Treat encrypted credential blobs as sensitive unless the protocol and logging design explicitly make their retention safe. Keep passwords, keys, image/repository credentials, API tokens, and credential-bearing payload fields out of reports and avoid logging them when the selected interface permits. When the scoped task ends, stop only the identified Web process unless the user explicitly requested persistence; service-manager creation or removal is a separate host mutation.

## Sources

- Official OBD V4.6.0 User Guide sections describing the graphical interface and asynchronous tasks.
- [Source-evidence boundary](../../references/source-baselines.md#source-evidence-boundary): `_cmd.py` `WebCommand`; `service/` listener, middleware, and task implementations in the exact inspected checkout.
