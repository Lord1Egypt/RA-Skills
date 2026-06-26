---
name: project
description: Explain, compare, and choose geographic coordinate reference systems and map projections, including CRS selection, EPSG codes, datum differences, axis order, units, and reprojection planning. Use when the user asks about 地理坐标系, 坐标参考系, 地图投影, CRS, EPSG, WGS84, Web Mercator, UTM, CGCS2000, GCJ-02, BD-09, or 坐标转换/投影转换.
metadata:
  openclaw:
    emoji: "🧭"
---

# Project

Use this skill for geographic coordinate system and projection questions.

## Scope

- Explain what a CRS/projection is and why it matters.
- Compare common systems such as `EPSG:4326`, `EPSG:3857`, UTM zones, `CGCS2000`, `GCJ-02`, and `BD-09`.
- Recommend a target CRS based on the task: storage, web map display, measurement, analysis, or exchange.
- Review conversion plans and call out likely mistakes such as swapped axis order, wrong units, or datum mismatch.

## Workflow

1. Identify the source coordinate system, target coordinate system, and the actual job to be done.
2. State whether the user needs a geographic CRS, projected CRS, or a provider-specific offset system.
3. Call out the important differences: datum, units, axis order, extent, and whether the transform is exact or approximate.
4. Give a concrete recommendation with an EPSG code or named system when possible.
5. If the request involves local files or batch conversion, hand off execution details to `qgis`.

## Answer Checklist

- Name the source and target CRS explicitly.
- State units clearly: degrees vs meters.
- Mention whether the CRS is suitable for measurement, display, storage, or exchange.
- Warn when web map tiles use `EPSG:3857` but input data is `EPSG:4326`.
- Warn that `GCJ-02` and `BD-09` are offset systems, not drop-in replacements for standard global CRS definitions.
- If accuracy matters, state whether a datum shift or local transformation model is required.

## Common Rules

- Prefer `EPSG:4326` for interoperable storage and API exchange unless another CRS is required.
- Prefer a projected CRS in meters for distance, area, and buffering.
- Prefer the correct local projected CRS over Web Mercator for engineering or survey-style measurement.
- Do not guess a UTM zone from country alone; derive it from longitude and hemisphere.
- Do not assume all software uses the same axis order for `EPSG:4326`; some APIs expect `lon,lat`, others advertise `lat,lon`.

## When Not to Use

- Reverse geocoding or coordinates-to-address lookup: use `geocode`.
- Deterministic GIS execution on files: use `qgis`.
- CesiumJS globe rendering or camera/data-layer code: use `cesium`.
- Navigation routing, turn-by-turn directions, or POI reviews.

## OpenClaw + ClawHub Notes

- Keep examples generic and portable. Do not hardcode private datasets, machine paths, or tokens.
- Prefer standards-based names and EPSG identifiers over vendor-specific jargon.
- For clawhub.ai publication, keep examples reproducible and changelog/version updates semver-driven.

## Reference Docs In This Skill

- Read `{baseDir}/references/common-systems.md` when you need quick guidance on common CRS and projection tradeoffs.
