# Third-Party Plugin Evaluation: hermes-weather-plugin

**Date**: 2026-05-28
**Repo**: https://github.com/FahrenheitResearch/hermes-weather-plugin
**Version evaluated**: 2.1.0

## Summary

Professional-grade Hermes weather plugin with 13 tools across 3 categories: data (7), imagery (3), calculations (3). Pure Python data tools + Rust-backed image/calc tools.

## Architecture

```
Plugin (Python)
  |- Data: requests -> NWS / SPC / METAR / Open-Meteo APIs
  |- Model images: rusbie -> wrf-rust
  |- Radar: rustdar or bundled nexrad-render-cli
  `- Calculations: metrust + ecape-rs
```

## Dependency Analysis

### Python deps (pip-installable)
- `requests` ✓ (already present)
- `numpy` ✓ (already present)
- `metrust` ✓ (on PyPI, v0.4.7)
- `rusbie` ✗ (GitHub-only, unpublished to PyPI)
- `rustweather` ✗ (GitHub-only)
- `wrf-rust` ✗ (GitHub-only)
- `cfrust` ✗ (GitHub-only)

### Rust binaries (need cargo to build)
- `radar-render` from `rustdar`
- `run_case` from `ecape-rs`
- `nexrad-render-cli` (bundled source)

## Install Result

**Failed.** `pip install git+https://github.com/FahrenheitResearch/hermes-weather-plugin.git` failed because `rustplots>=0.1.0` (a dependency of `rustweather`) is not published to PyPI. Even with Rust toolchain present, the build would fail.

## Tools Breakdown

### Data tools (would work if install succeeded)
| Tool | API | Reach equivalent |
|------|-----|-----------------|
| `wx_conditions` | NWS API | `noaa_nws` |
| `wx_forecast` | NWS API | `noaa_nws` |
| `wx_alerts` | NWS API | `noaa_nws` |
| `wx_metar` | METAR | Partial `noaa_nws` |
| `wx_brief` | Composite | Composite |
| `wx_global` | Open-Meteo | `open_meteo` |
| `wx_severe` | SPC | No direct equivalent |

### Image tools (require Rust binaries)
| Tool | Backend | Status |
|------|---------|--------|
| `wx_model_image` | wrf-rust / rusbie | ✗ Broken dep chain |
| `wx_radar_image` | rustdar / nexrad | ✗ No cargo |
| `wx_storm_image` | radar backend | ✗ No cargo |

### Calc tools (require Rust binaries)
| Tool | Backend | Status |
|------|---------|--------|
| `wx_calc` | metrust | ✓ Would work (pure Python) |
| `wx_sounding` | metrust | ✓ Would work |
| `wx_ecape` | ecape-rs | ✗ No cargo |

## Overlap with ocas-reach

7 of 13 tools duplicate existing reach sources:
- `wx_conditions`, `wx_forecast`, `wx_alerts` → `noaa_nws`
- `wx_global` → `open_meteo`
- `wx_calc`, `wx_sounding` → could use `noaa_nws` data + metrust

The unique value is:
- `wx_severe` (SPC outlook/watches — not in reach)
- `wx_metar` (aviation weather — not in reach)
- Image tools (if Rust deps were fixable)
- `wx_ecape` (if Rust deps were fixable)

## Decision

**Did not install.** Reasons:
1. Broken dependency chain (`rustplots` not on PyPI) makes even `pip install` fail
2. 7 of 13 tools duplicate existing ocas-reach sources
3. Serveriting features (6 tools) require Rust which isn't installed
4. The plugin author would need to publish `rustplots` to PyPI and ensure all Rust deps compile cleanly

## Recommendation for Future

If the plugin author fixes the dependency chain:
- `wx_severe` (SPC) is the only genuinely unique data tool worth adding to ocas-reach as a new source
- Image/calc tools would still require Rust — consider them optional enhancements, not core features
- Prefer adding SPC as a reach source over installing the full plugin
