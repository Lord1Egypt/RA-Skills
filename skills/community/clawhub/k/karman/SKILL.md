---
name: karman
description: Query Karman, a monitor for small Solar System bodies whose motion gravity does not explain (non-gravitational accelerations, interstellar visitors). Use when the user asks which asteroids or comets move anomalously, why an object got its label, how the evidence compares with JPL, what the watch has seen lately, or how the method was validated.
version: 0.1.1
homepage: https://karman.si
metadata:
  openclaw:
    requires:
      anyBins: [curl]
---


# Using Karman

Karman fits the orbit of a small body to public astrometry with gravity alone and against every ordinary
non-gravitational cause, then labels the most likely one on a ladder that demands more evidence the stranger the
cause. Its expected finds are dark comets, spent rocket stages and data errors.

## Tools (MCP server `karman`)

| To do this | Call |
|---|---|
| See what is flagged, strongest first | `list_anomalies` (filter with `cause`, `min_rung`) |
| Find an object by name or designation | `search_objects` |
| Everything about one object | `get_object_anomaly`, then `explain_cause` |
| The residuals behind a plot | `get_object_residuals` |
| New findings (flagged here, gravity-only at JPL) | `list_new_candidates` |
| How well it works | `get_validation`, `get_benchmark` |
| Interstellar visitors and the watch (runs on demand) | `watch_status`, `latest_alerts`, `subscribe` (feed links for a filter; pull-based) |
| How it works | `get_method` |

The server is hosted at `https://karman.si/mcp` (MCP over HTTP, read-only, no account or key). The Claude Code
plugin connects to it for you; any other MCP client can add that URL.

## Reading the answers

- **Evidence** is ΔBIC over gravity alone: 10 is strong. Each cause has its own bar (Yarkovsky 10, low density or
  outgassing 20, impulse 30).
- **False-alarm probability** is how often gravity alone, with that object's own observing history and noise,
  produces evidence that strong. It does not cover slow station-level systematics; the data-check rung does.
- **Rungs**: 1 gravity suffices, 2 data problem, 3 Yarkovsky, 4 radiation pressure, 5 low density or outgassing,
  6 outgassing, 7 impulse.
- JPL's own parameters are shown for comparison and are never read by the detector. JPL may use a different
  distance law, so compare signs and orders of magnitude.

## Rules to keep

1. Quote `status` and `limits` with any figure you report.
2. A label is the most likely cause on this evidence, not an identification.
3. "Unexplained" objects are only ever a count. Do not try to identify them, and never describe a candidate as more
   than a candidate needing checks.
4. Nothing is reported to the Minor Planet Center, JPL or anyone else, and you should not offer to.
