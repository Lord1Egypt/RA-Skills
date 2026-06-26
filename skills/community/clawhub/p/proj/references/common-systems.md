# Common Coordinate Systems

Use this reference only when the user needs concrete CRS comparison or projection advice.

## Core mental model

- Geographic CRS: coordinates are angular, usually longitude and latitude in degrees.
- Projected CRS: coordinates are planar, usually eastings and northings in meters.
- Datum: defines the earth model and reference frame behind the coordinates.
- Projection: defines how geographic coordinates are mapped onto a flat surface.

## Common systems

### WGS 84

- Typical identifier: `EPSG:4326`
- Type: geographic CRS
- Units: degrees
- Best for: storage, interchange, GPS-like coordinate exchange, many APIs
- Watch out for: not ideal for direct distance or area calculations; axis-order handling varies by software

### Web Mercator

- Typical identifier: `EPSG:3857`
- Type: projected CRS
- Units: meters
- Best for: slippy maps and web tiles
- Watch out for: convenient for display, poor choice for accurate measurement, especially at high latitudes

### UTM

- Typical identifiers: zone-specific projected CRS, often `EPSG:326xx` or `EPSG:327xx`
- Type: projected CRS
- Units: meters
- Best for: regional measurement and analysis within one zone
- Watch out for: wrong zone selection, cross-zone datasets, hemisphere mistakes

### CGCS2000

- Type: China geodetic reference framework
- Common use: national mapping and domestic GIS workflows in China
- Watch out for: multiple projected variants exist; you still need the exact CRS/projection definition, not just the datum name

### GCJ-02

- Type: encrypted offset coordinate system used by many consumer map services in China
- Common use: domestic consumer mapping apps and SDKs
- Watch out for: not a standard EPSG-defined global CRS for general GIS interchange; transforms can be policy-sensitive and implementation-specific

### BD-09

- Type: Baidu offset system derived from GCJ-02 style coordinates
- Common use: Baidu map ecosystem
- Watch out for: extra offset relative to GCJ-02; do not treat it as ordinary WGS 84

## Selection rules

- Data exchange between systems: default to `EPSG:4326` unless a partner explicitly requires another CRS.
- Web basemaps and browser tiles: `EPSG:3857` is usually the display CRS.
- Distance, buffering, and area analysis: choose a local projected CRS in meters.
- City/regional analysis: a correct local projected CRS or UTM is usually safer than Web Mercator.
- National or regulatory workflows: use the CRS required by the governing data specification.

## Frequent mistakes

- Using `EPSG:3857` for precise area or distance analysis.
- Treating `GCJ-02` or `BD-09` as if they were plain WGS 84.
- Forgetting axis order and sending `lat,lon` to a system expecting `lon,lat`.
- Reprojecting data without verifying the source CRS first.
- Mixing datasets with different datums and assuming they align exactly.
