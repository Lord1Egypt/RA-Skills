# Multi-channel, dependencies, and per-channel visibility

## Multi-channel fan-out

```bash
poke --remind "Deploy done." --once 5m \
  --channel discord,slack --target "user:123,user:456,#deploys"
```

- `--channel` and `--target` accept comma-separated values.
- Delivers to all channel × target combinations (Cartesian product).
- Same reminder ID, single state file — fan-out is at delivery time only.

If you want different content per channel, schedule separate reminders;
multi-channel is for "say the same thing in multiple places."

## Dependencies (DAG)

```bash
poke --remind "Merge PR." --depends-on tr-abc123 \
  --channel CH --target TGT
```

- Won't fire until the dependency reminder is `confirmed` or `cancelled`.
- Comma-separated for multiple deps: `--depends-on tr-a,tr-b,tr-c`.
- **Validated at create time** — unknown IDs error immediately.
- Re-checked every minute while waiting.
- Once all deps resolve, `state.depends_on` is cleared and the reminder
  fires.

Mental model: "Don't fire this until *every* dep has been answered."
A cancelled dep counts as resolved (the upstream work was abandoned;
the downstream still proceeds). This is intentional — if you want
"only fire if upstream succeeded" semantics, you need a `--post-task`
or `--post-cmd` chained off the upstream.

`--urgent` does NOT bypass dependency resolution. Pipelines stay
pipelines regardless of urgency.

## Per-channel visibility

Channel-level filter, independent of any specific reminder:

```bash
poke --visibility-set matrix urgent     # only urgent reminders for matrix
poke --visibility-set matrix all        # deliver everything (default)
poke --visibility                       # show current settings
```

Modes:

- `all` — deliver everything (default)
- `urgent` — only deliver reminders marked `--urgent`

Useful when one channel is quieter than another (e.g. work matrix room
should only see urgent pages; personal discord can see everything).

Stored in `.runtime/state/visibility.json`.
