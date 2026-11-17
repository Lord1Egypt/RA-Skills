# Network Identity and Client Access

Use this workflow for Observer/OBProxy access, SQL/RPC/obshell listeners, `ip`/`local_ip`/`devname`, firewall, and TLS boundaries.

## Resolve the Access Topology

Record each layer separately:

| Layer | Resolve |
|---|---|
| OBD management | controller-to-target SSH address, machine identity, route, SSH user/host-key policy |
| Observer | advertised/bound SQL, RPC, obshell addresses and ports; zone/server identity |
| OBProxy | community/commercial component key, backend discovery, listener, tenant routing, credentials/TLS |
| Config Server | endpoint and the exact OceanBase/OBProxy consumers that reference it |
| Client | source networks, proxy/direct endpoint, tenant/user syntax, TLS, allowlist/firewall |

Direct Observer SQL access is valid when it meets the request. Add OBProxy only for a required routing/availability outcome. Firewall policy is externally owned; inspect its boundary but do not mutate it without explicit scope.

## `ip`, `local_ip`, and `devname`

Treat these as related but distinct inputs and inspect the selected component plugin before use.

In verified OceanBase 4.2+ plugin behavior, the server stanza `ip` is OBD's management target and can be the default Observer address when neither `local_ip` nor `devname` is set; explicit `local_ip` controls Observer network configuration; `devname` selects or validates an interface when needed. These statements are version-specific and are not transferable to another plugin.

Use the smallest unambiguous configuration:

- use only server `ip` when management and Observer service identity are the same and plugin derivation is valid;
- set `local_ip` only for a different locally bindable Observer identity;
- set `devname` only when interface selection is required and the interface exists in the process's network namespace;
- when both are supplied, prove their intentional mapping and plugin precedence.

Never copy one node's network identity into every server or set `local_ip` to an address that is not locally bindable.

Before changing a configured network field, verify interfaces/addresses/namespaces/routes, duplicate IP ownership, firewall/TLS, peer connectivity, client/OCP/monitoring/Config Server references, and whether the installed distributed workflow permits reload, restart, or requires a separately reviewed redeploy. Adding, removing, replacing, or directly changing the identity of Observer servers in a registered distributed deployment is unsupported.

## Access and Security Gate

Build an approved source-to-destination matrix with protocol, address/port, authentication/TLS, allowlist/firewall owner, and health check. Preserve at least one reviewed management path before tightening access. Never expose database, obshell, proxy, OCP, or monitoring listeners broadly merely to pass a check.

Keep database and proxy credentials out of argv, YAML displays, and reports when the installed client offers a protected channel. If it accepts a required secret only in argv, disclose the exposure and use an approved permission-controlled local procedure; never call that path protected. A TCP connection does not prove authentication or routing to the intended tenant.

## Acceptance

Verify registered and generated configuration, actual bind/advertised listeners and process owners, product-side server addresses, peer RPC connectivity, OBProxy backend/route health when selected, and authenticated client access from an approved source. Where feasible verify rejection from a non-approved source without disrupting production.

Test direct Observer, OBProxy, OCP, and monitoring paths separately. Report which path was tested; one working endpoint does not prove all nodes or access layers.

On failure preserve the access matrix, routes, listeners, effective configuration, certificates, firewall state, and trace. Do not change `local_ip`, `devname`, firewall, or proxy topology as a generic response to an unrelated OBD error.
