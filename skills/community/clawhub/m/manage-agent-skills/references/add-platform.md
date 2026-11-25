# Add a platform adapter

Use this guide when the user requests support for an unsupported agent platform.
Any agent with source editing and testing tools can perform this workflow; no
Codex-specific tool, identity, or external skill is required. A platform guide
alone is not executable support. Never guess another host's configuration.

## 1. Establish the target and development location

Record host product, surface (CLI/IDE/Desktop/cloud), version, OS, execution
location, and available file/shell tools. Distinguish current host from requested
target. Ask only for facts unavailable from trusted context. Do not treat model
vendor, installed directories or executable presence as current-host identity.

Work in an editable source checkout of
https://github.com/yunze7373/manage-agent-skills or a separate development copy.
Never patch an installed skill, marketplace cache or synced snapshot in place.
A release ZIP contains this guide and runtime, but not repository tests: obtain
an editable checkout to complete integration/testing. Without editing/shell or
source access, deliver an evidence-backed patch plan and state the limitation;
do not claim support was added. Do not install dependencies or write live host
configuration merely to identify the platform.

## 2. Research before coding

Read current official docs and, when needed, the exact host source/version.
Record URLs, date and observed version in the new adapter guide. Establish:

- Discovery roots and precedence, plugins, shared roots, snapshots and duplicates.
- Native identity: name, directory, path or plugin-qualified key.
- Native enable/disable controls and user/project/managed scope precedence.
- Permissions, global disable blockers, essential skills and refresh semantics.
- Config parsing/format, backup/recovery behavior and native CLI timeout/failures.

Do not infer an API from an example filename. If no supported enable/disable
mechanism is documented, implement read-only discovery and return an explicit
unsupported-operation blocker for mutations. Do not simulate disable by editing,
renaming, deleting or moving installed skill files. Distinguish unknown from off.

## 3. Implement the runtime contract

In skills/manage-agent-skills/scripts/skillctl.py implement a class with:

```python
class ExampleAdapter:
    name = "example"

    def __init__(self, cwd, config=None):
        # Accept explicit temporary config/root paths for tests.
        self.cwd = cwd
        self.config = config

    def available(self):
        # Return (bool, safe detail); do not mutate or expose config secrets.
        raise NotImplementedError

    def discover(self):
        # Return list[Skill]; use unknown when state cannot be established.
        raise NotImplementedError

    def mutate(self, action, targets, dry_run, force):
        # Implement only documented operations. A read-only adapter returns:
        return {"platform": self.name, "changed": False, "dry_run": dry_run,
                "blocked": [{"reason": "unsupported_operation"}]}
```

This is an interface sketch, not a working adapter. Implement discovery before
writes. Reuse Skill, bounded read_frontmatter/scan_roots, resolve_selectors,
write_atomic and existing parsers where their semantics actually match. Preserve
config fields; refuse malformed input. Dry-run and inspect must create no backup,
write, move or native mutating subprocess. Protected skills must be checked before
writes. Use finite CLI timeouts and bounded output, never serialize credentials.

Integration checklist (all paths relative to repository root):

1. Register the stable lowercase platform ID in PLATFORMS.
2. Add constructor arguments to build_parser, and an explicit branch in adapters.
   Never let an unknown ID fall through to an existing platform.
3. Add REFRESH_GUIDANCE; inspect_targets and post-mutation reporting use it.
4. Extend audit_payload only for genuinely platform-specific checks; ordinary
   metadata/duplicate diagnostics already work with Skill records.
5. Exercise status, doctor, search, index, inspect, enable/disable and presets.
   Read-only adapters must reject writes with zero side effects, including preset
   preflight. Keep reconcile/set or other host-only operations unsupported.
6. Add references/adapters/<id>.md, the SKILL.md routing row and platforms.md
   support row. adapter-guide derives its catalog from PLATFORMS.
7. Update README support claims and add tests/test_<id>_adapter.py. Do not hardcode
   a new host into the generic SKILL.md workflow or invent a universal env marker.

## 4. Verify in isolation

Use TemporaryDirectory for home, project, config and skill roots. Patch Path.home
and relevant environment overrides; mock native CLIs/network. Never read or write
real ~/.claude, ~/.codex, ~/.agents or another real agent home during tests.
Cover discovery precedence/duplicates, malformed configs, unknown state, exact
selectors, dry-run purity, protected targets, unrelated field preservation,
backup contents/history, blocked enables and unsupported operations. Compare
installed fixture bytes before/after every operation. Test native failures and
partial outcomes where relevant. Missing host CLI must not trigger installation.

Run from the development checkout:

```text
python -m unittest discover -s tests -v
python -m py_compile skills/manage-agent-skills/scripts/skillctl.py scripts/release.py
python skills/manage-agent-skills/scripts/skillctl.py adapter-guide <id> --json
```

Run the repository release package helper into a fresh temporary output directory
using the checkout's current version; inspect the ZIP for the guide and runtime.
Do not overwrite a previously released artifact. Include fixtures showing current
host default, explicit different target, unknown target, and cloud-without-local
access routing. Tests of guide links do not prove an agent follows instructions;
report any real-host validation separately, using read-only native inventory.

## 5. Deliver and activate deliberately

Report source diff, official evidence, supported/read-only operations, test results,
limits, and any unverified host behavior. A test pass is local implementation
proof, not live host invocation proof. Keep the development version separate from
installed copies. If installation is requested, use the host's supported workflow
and verify the new skill there; do not silently replace its own running package.
Publication, tags and marketplace submissions require release scope from the user
and the repository release gates. Adding a platform does not itself authorize
publishing or changing other installed platforms.

## Adapter guide template

Use these sections in references/adapters/<id>.md, replacing every placeholder:

- Host/surface and CLI platform ID; supported version evidence and date.
- Discovery roots, precedence, identities, duplicates and excluded caches.
- Supported operations and configuration scope; explicit unsupported operations.
- Relevant options and neutral-shell command examples with exact targets.
- Safety, blockers, backups and recovery.
- Refresh and native verification; distinguish local and live evidence.
- Official source links and known limitations.
