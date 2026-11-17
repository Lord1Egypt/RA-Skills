<!--
SOURCE: github.com/XertroV/tm-plugin-skills — skills/openplanet-reviewer/references/evidence-precedents.md
AUTHOR: XertroV
LICENSE: CC0-1.0 OR Unlicense (public-domain equivalent; free to reuse, modify, redistribute)
ATTRIBUTION: imported into openplanet-plugin-dev (tomekdot) as a review-procedure reference.
NOTE: this file lists concrete project-local precedents (tm-bosslike, Map Together, Dips++) used
as fault probes when reviewing. Verify paths at a pinned revision before treating as evidence.
-->
# Evidence precedents and probes

Load only for branches that need concrete project-local Openplanet precedent.
Paths name sibling repositories used during skill development; verify them at a
pinned revision before treating them as independently inspectable evidence.

## UI actions

- `tm-draw-tests/src/Epp/ExtraEditorMenuItem.as:8-70,114-175`: strongest
  reusable component precedent; draw-time hit testing launches `startnew`, action
  exceptions are centralized, semantic/visual methods are overridable.
- `tm-bosslike/src/Game/Modes/SimpleRM.as:124-162`: stable map UID scope,
  `CoroutineFuncUserdata`, click-time object argument, and post-yield stale-state
  check.
- `tm-simple-room-admin/src/Interface.as:430-534`: copy selected scalar/UID rather
  than a mutable loop index.
- Typed multi-value carriers:
  `tm-bosslike/src/ChangeRoomParams.as:1-11`,
  `tm-cgf-library/src/Maps.as:126-156`.
- Counterexamples: `tm-editor-ui-toolbox/src/NvgButton.as:1-40` and
  `tm-map-info/src/NvgButton.as:1-41` invoke stored callbacks inline. Callback
  type alone does not isolate failure.

### Reported live UI exception fixture

`prototypes/issue-13-ui-exception-probe/Main.as:1-62`, Openplanet 1.29.0. The
fixture is bundled and mechanically gated by `SKILLPACK_PROBE_MODE`; the original
log is not bundled, so these are prior project observations until rerun:

- `Openplanet.log:26724-26727`: isolated coroutine exception;
  `:26746-26836`: later heartbeats continue.
- `Openplanet.log:27021-27027`: inline render exception reaches
  `RenderInterface()`, followed by `Unrolling dangling script UI stack` at the
  open window scope; no later probe heartbeat was captured while other plugins
  continued.

Use the fixture to recheck future versions. Do not broaden this into “every UI
exception always disables rendering.”

## Architecture

- Bosslike `src/Main.as:6-23` plus `src/OpenplanetCallbacks.as:5-67`: one runtime
  root and thin Openplanet adapters.
- `tm-bosslike/src/TM_State.as:1-155`: one normalized state snapshot and derived
  transition edges.
- `tm-bosslike/src/Game/Bosslike.as:3-182` plus
  `src/Game/Modes/SimpleRM.as:11-242`: invariant engine with small policy hooks.
- `tm-bosslike/src/Game/State/MapChanger.as:18-130`: environment differences
  behind real adapters.
- Editor++ `src/Exports/Callbacks_Shared.as:15-74`,
  `Callbacks.as:1-5`, `Callbacks_Impl.as:3-317`: minimal public contracts,
  registration, dispatch, removal, and lifecycle kill.

Watch for callback business logic, duplicate state normalizers, implicit boolean
state machines, ownerless coroutines, god objects, parallel arrays, mutable
public invariants, and cleanup only on success.

## Confirmed source invariant violations

- Map Together `src/EditorFeed.as:71-95,405-415`: editor patches can be enabled
  before readiness checks whose early returns bypass cleanup. Probe transition
  during initial delay and plugin unload; verify patch flags and editor behavior.
- Bosslike `src/Game/Modes/SimpleRM.as:344-402`: retained download reference is
  not released on timeout. Probe repeated timeout and ref/task stability.
- Bosslike `src/Game/Modes/SimpleRM.as:289-319`: throw can bypass the only
  `IsLoading = false`, while consumers wait at `:156-162,208-226`.
- Map Together `src/EditorFeed.as:312-343`: zero processed items can lead to
  `pendingUpdates[processed - 1]`.
- Map Together `src/Socket.as:527-578` advances expected `mapTree` before editor
  application in `EditorFeed.as:291-343` is known to succeed.

## Network workload contrast

Dips++ is a sampled JSON API/session client with resume. Map Together replicates
ordered, non-commutative editor mutations. The difference demands distinct retry,
ordering, queue, and reconciliation policies.

### Dips++ source hazards

- Inner JSON length need not equal the outer frame remainder:
  `Server/Socket.as:183-195`.
- Parse failure can dispatch stale reused JSON: `Socket.as:97-98,148-150,190-201`.
- Queue removes entries after reported write failure:
  `Socket.as:159-168`; `Server.as:284-290`.
- Queue survives reconnect without freshness classes:
  `Server.as:154-165,266-293`.
- Connect timeout retries without disposing previous socket: `Socket.as:31-49`.

### Map Together source hazards

- **Confirmed structural mismatch; runtime impact needs a variable-length probe:**
  variable player ID conflicts with fixed 46-byte tail assumptions:
  `Socket.as:3,841-846,1121-1131`.
- **Hypothesis pending protocol/server evidence:** unknown types discard a
  hard-coded 46 bytes: `Socket.as:896-900,1027-1059`.
- **Hypothesis pending socket full-write semantics:** frames use multiple writes
  with ignored return values: `Socket.as:441-519`.
- **Hypothesis pending ordering/atomicity guarantees:** multiple coroutines write
  one socket without a sole-writer queue:
  `EditorFeed.as:115-230,575-597`; `Socket.as:237-253`.
- **Hypothesis pending server inspection:** no visible operation ID, room epoch,
  sequence, or dedup field.
- Persistent update queue is effectively unbounded:
  `Socket.as:561`; `EditorFeed.as:259-343`.
- `PlayerEphemUpdates.as:106-108` compares `cur_obj != cur_obj`.

Server implementations were not inspected; label claims about server guarantees
as unknown unless protocol evidence proves their absence.

## Fault fixture matrix

Use a controllable proxy/server and assert stream alignment plus semantic state:

- fragment every boundary and delay final bytes;
- force zero/partial writes and ambiguous hangup;
- mutate lengths and metadata sizes;
- burst beyond queue/application capacity;
- duplicate, replay, reorder, delay, and drop each operation class;
- let old-connection responses arrive in a new generation;
- trigger all writers in one scheduling window; and
- poison expected state before reconciliation.

Require one framed-write owner, exact consumption, explicit limits, epochs and
operation IDs where needed, traffic-class retry policy, and deterministic tests
for malformed framing, reconnect ambiguity, replay, and overload.