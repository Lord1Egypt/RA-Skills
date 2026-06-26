---
name: heliospice
description: Query positions of spacecraft, planets, moons, and asteroids in the solar system
---

# Heliospice

Query spacecraft and planetary ephemeris data using SPICE kernels.

## Setup

```bash
pip install heliospice
```

## What You Can Query

**Spacecraft (36+)**: Parker Solar Probe, Solar Orbiter, Juno, Cassini, Voyager 1/2, Mars 2020, MRO, New Horizons, Europa Clipper, Psyche, BepiColombo, JUICE, Lucy, Galileo, Dawn, MESSENGER, and more...

**Planets**: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto

**Moons**: Moon, Titan, Europa, Ganymede, Io, Phobos, Deimos, and many more

**Other**: Sun, asteroids, comets, Solar System Barycenter

## Tools

- `get_spacecraft_ephemeris` — Position at single time or timeseries (with optional velocity)
- `compute_distance` — Distance between two bodies over time range (min/max/mean, closest approach)
- `transform_coordinates` — Transform vectors between coordinate frames (RTN, J2000, ECLIPJ2000, etc.)
- `list_spice_missions` — List all supported spacecraft
- `list_coordinate_frames` — List available coordinate frames
- `manage_kernels` — Check status, download, load, or purge kernel cache

## Examples

- "Where is Parker Solar Probe right now?"
- "What's Earth's distance from the Sun?"
- "Show me Juno's trajectory for January 2024"
- "When did Mars get closest to Jupiter in 2024?"
- "Convert this RTN vector to J2000 frame"
- "What's the current Moon position?"
