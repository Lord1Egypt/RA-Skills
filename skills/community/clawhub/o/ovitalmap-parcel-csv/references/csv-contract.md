# CSV Compatibility Contract

Do not change this contract without an explicit migration request.

## Encoding and filenames

- Encoding: UTF-8, comma-separated, no BOM.
- Directory: `ovitalmap_exports/{CC}/`.
- Every generated file contains exactly one parcel.
- Default boundary export: `{parcelCode}_{YYYYMMDD_HHMMSS}.csv`.
- Explicit vertex export: `{parcelCode}_{YYYYMMDD_HHMMSS}_vertices.csv`.
- Same-second collisions append `_02`, `_03`, and so on before `.csv` or `_vertices.csv`.

For multiple parcels, generate files in submitted `parcel_ref` order and do not combine them. Archive names remain `{CC}_parcels.csv` and `master.csv`.

The export modes are:

- `boundary` (default): boundary file only.
- `vertices`: vertex file only, and only after an explicit user request.
- `both`: both files, only after an explicit user request for both.

## Vertex CSV (顶点表)

Exact headers:

```text
文件夹,名称,经度,纬度,海拔,文本显示风格,图标样式,Comment
```

- 文件夹: parcel code.
- 名称: `{parcel_code}_A01`, restarting at A01 for each parcel.
- 经度/纬度: WGS84 longitude and latitude in original vertex order.
- 海拔: input altitude or empty.
- 文本显示风格: empty.
- 图标样式: `1`.
- Comment: `提供者:{provider} 归档日期:{YYYY-MM-DD}` and, when present, ` 地籍号:{cadastre_code}`.

## Boundary CSV

Exact headers:

```text
文件夹,名称,经纬度[经度+纬度],线条宽度,线条颜色,线条不透明度,闭合,线型,轨迹风格,Comment
```

- 文件夹 and 名称: parcel code.
- 经纬度: `lon,lat;lon,lat;...`; repeat the first point to close the polygon.
- 线条宽度: `3`.
- 线条颜色: `0X00FF0000`.
- 线条不透明度: `50`.
- 闭合: `1`.
- 线型: `0`.
- 轨迹风格: `1`.
- Comment: same as the vertex CSV.

## Archive schemas

Per-country:

```text
parcel_code,provider_name,archive_date,boundary_coords,provider_notes,cadastre_code
```

Master:

```text
CC,parcel_code,provider_name,archive_date,boundary_coords,provider_notes,cadastre_code
```
