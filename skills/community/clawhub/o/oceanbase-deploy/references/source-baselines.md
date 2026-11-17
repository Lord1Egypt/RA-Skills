# Evidence Baselines

Use this reference to keep documentation, inspected source, and installed runtime evidence separate. Do not bind an OBD product version or RPM release to a source commit or implementation behavior without immutable provenance for that exact artifact. Installed command, plugin, workflow, schema, registered state, and selected artifacts remain the runtime authority.

## Evidence Escalation

Begin with the applicable Skill workflow, then use installed public help/schema surfaces, released examples, registered state, public command output, and actual runtime or data-plane results. Use version-matched official documentation to interpret that evidence. Inspect an installed packaged plugin or workflow only when those layers cannot explain an execution-critical field, side effect, selector, confirmation path, or partial state.

Do not repeat source analysis merely to reconfirm behavior already captured by the Skill. Do not decompile or disassemble binaries, modify OBD or its plugins, execute extracted implementation code, or treat a development checkout as the default diagnostic interface. When packaged implementation inspection is necessary, keep it read-only, identify the exact installed artifact, and limit the conclusion to that evidence.

## Installed Plugins and Frozen Controller Code

Distinguish readable installed component code from the controller executable before interpreting a search result:

- packaged component plugins, workflows, and helper modules may be installed as readable Python. A read-only inspection of those exact files is installed-artifact evidence when the controller identity, package NEVRA or artifact hash, and inspected path are recorded;
- the OBD launcher or controller core may be packaged as a frozen executable, including a PyInstaller ELF. Failure to find a symbol or string with `rg`, `grep`, or filesystem traversal is then inconclusive and must never be reported as proof that the behavior does not exist;
- an online repository's default branch, including `master`, is development evidence. Do not fetch or use it to explain an installed build merely because the frozen core is not readable.

When controller-core behavior remains execution-critical after public help, schema, trace, registered state, and runtime evidence are exhausted, first identify the exact installed `obd` build and package or executable checksum. Consult source only when an immutable official tag or commit is provenance-mapped to that exact artifact. If no exact mapping exists, label any source comparison as a hypothesis, keep the installed runtime authoritative, and do not use the comparison alone to authorize a mutation, declare a capability unsupported, or prescribe a workaround.

## Documentation Baseline

Official OBD documentation can establish the commands, options, schemas, and behavior documented by that publication. It does not prove the implementation of an installed package, map an RPM release to a source commit, or classify a whole product version as affected or fixed. Reconcile every execution-sensitive claim with the installed artifact.

<a id="source-evidence-boundary"></a>

## Source Evidence Boundary

A source path, symbol, or behavior in this revision refers only to the inspected `ob-deploy` checkout at commit `4ef23088b04cbba82793dbc718d3b844bcd0fdb5`. That hash identifies review evidence only; it is not mapped to an OBD product version or RPM release. Do not relabel the observation as released-version evidence or infer that another package, RPM revision, branch, or product version contains the same implementation. Use the installed implementation as the runtime authority for behavior that depends on it.

## Evidence Maintenance Rule

Record the exact inspected checkout for a source observation, but do not infer a package mapping from its branch, tag, or version-like name. Label source-only behavior clearly and prefer the Skill, installed public help, registered/runtime behavior, and version-matched released documentation for operational decisions.
