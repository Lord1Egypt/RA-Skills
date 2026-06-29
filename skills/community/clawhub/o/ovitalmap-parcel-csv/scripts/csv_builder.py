"""
Build Ovitalmap-compatible Vertex and Boundary CSVs from structured parcel data.

CLI usage:
    echo '{"parcels":[{...}],"first_code":"CN-260610-001","count":2,"country_code":"CN"}' | python3 scripts/csv_builder.py
    # Outputs paths of generated CSV files.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import read_json_stdin, write_json_stdout, write_csv, build_boundary_string, validate_coordinates, check_duplicate_vertices, get_workspace_root

WORKSPACE_ROOT = get_workspace_root()
EXPORTS_DIR = WORKSPACE_ROOT / 'ovitalmap_exports'


def _export_ts():
    return datetime.now().strftime('%y%m%d_%H%M%S')

VERTICES_HEADERS = [
    '文件夹', '名称', '经度', '纬度', '海拔', '文本显示风格', '图标样式', 'Comment',
]

BOUNDARY_HEADERS = [
    '文件夹', '名称', '经纬度[经度+纬度]', '线条宽度', '线条颜色',
    '线条不透明度', '闭合', '线型', '轨迹风格', 'Comment',
]


def _build_comment(parcel):
    """Build Comment field: 提供者 + 归档日期 + 地籍号(if available).
    Applies to ALL parcels uniformly — archive-hit and new alike."""
    parts = []
    if parcel.get('resolved_provider_name'):
        parts.append(f'提供者:{parcel["resolved_provider_name"]}')
    if parcel.get('archive_date'):
        parts.append(f'归档日期:{parcel["archive_date"]}')
    if parcel.get('cadastre_code'):
        parts.append(f'地籍号:{parcel["cadastre_code"]}')
    return ' '.join(parts)


def build_vertices_rows(parcels):
    """Build all rows for the Vertices CSV.

    Args:
        parcels: list of dicts, each with:
            - parcel_code (str)
            - vertices (list of [lon, lat])
            - altitude (list of float or empty list, optional)
            - resolved_provider_name, archive_date, cadastre_code (for Comment)

    Returns:
        list of dicts ready for CSV writing.
    """
    rows = []
    for parcel in parcels:
        code = parcel['parcel_code']
        vertices = parcel.get('vertices', [])
        altitudes = parcel.get('altitude', [])
        comment = _build_comment(parcel)
        for i, (lon, lat) in enumerate(vertices):
            vertex_name = f'{code}_A{i + 1:02d}'
            altitude = ''
            if i < len(altitudes) and altitudes[i] is not None:
                altitude = str(altitudes[i])
            rows.append({
                '文件夹': code,
                '名称': vertex_name,
                '经度': str(lon),
                '纬度': str(lat),
                '海拔': altitude,
                '文本显示风格': '',
                '图标样式': '1',
                'Comment': comment,
            })
    return rows


def build_boundary_rows(parcels):
    """Build all rows for the Boundary CSV.

    Each parcel produces one row. The boundary name is just the parcel_code
    (no _A01 suffix).

    Args:
        parcels: list of parcel dicts, each with:
            - parcel_code (str)
            - vertices (list of [lon, lat])
            - resolved_provider_name, archive_date, cadastre_code (for Comment)

    Returns:
        list of dicts ready for CSV writing.
    """
    rows = []
    for parcel in parcels:
        code = parcel['parcel_code']
        vertices = parcel.get('vertices', [])
        boundary_str = build_boundary_string(vertices, close_polygon=True)
        comment = _build_comment(parcel)
        rows.append({
            '文件夹': code,
            '名称': code,
            '经纬度[经度+纬度]': boundary_str,
            '线条宽度': '3',
            '线条颜色': '0X00FF0000',
            '线条不透明度': '50',
            '闭合': '1',
            '线型': '0',
            '轨迹风格': '1',
            'Comment': comment,
        })
    return rows


def build_csvs(parcels, first_code, count, country_code):
    """Build both CSV files and return their paths.

    Args:
        parcels: list of parcel dicts.
        first_code: parcel_code of the first parcel.
        count: total number of parcels.
        country_code: alpha-2 country code.

    Returns:
        dict with vertices_path, boundary_path, vertices_rows, boundary_rows,
        validation_errors, duplicate_vertex_warnings
    """
    # Detect and deduplicate vertices per parcel
    all_dup_warnings = []
    for parcel in parcels:
        verts = parcel.get('vertices', [])
        deduped, dup_warnings = check_duplicate_vertices(verts)
        if dup_warnings:
            for w in dup_warnings:
                all_dup_warnings.append(f'[{parcel["parcel_code"]}] {w}')
        parcel['vertices'] = deduped

    vertices_rows = build_vertices_rows(parcels)
    boundary_rows = build_boundary_rows(parcels)

    # Validate all coordinates
    all_errors = []
    for parcel in parcels:
        code = parcel['parcel_code']
        errors = validate_coordinates(parcel.get('vertices', []))
        for e in errors:
            all_errors.append(f'[{code}] {e}')

    # Naming collision check
    seen_folders = set()
    for r in boundary_rows:
        folder = r['文件夹']
        name = r['名称']
        key = (folder, name)
        if key in seen_folders:
            all_errors.append(f'Naming collision: {folder} / {name}')
        seen_folders.add(key)

    # Write CSVs
    safe_first = first_code.replace('/', '_').replace('\\', '_')
    ts = _export_ts()
    base = f'{safe_first}_N{count}_{ts}'
    export_dir = EXPORTS_DIR / country_code
    export_dir.mkdir(parents=True, exist_ok=True)

    vertices_path = export_dir / f'{base}.csv'
    boundary_path = export_dir / f'{base}_boundary.csv'

    write_csv(str(vertices_path), VERTICES_HEADERS, vertices_rows)
    write_csv(str(boundary_path), BOUNDARY_HEADERS, boundary_rows)

    return {
        'vertices_path': str(vertices_path),
        'boundary_path': str(boundary_path),
        'vertices_count': len(vertices_rows),
        'boundary_count': len(boundary_rows),
        'validation_errors': all_errors,
        'duplicate_vertex_warnings': all_dup_warnings,
    }


def build_single_csvs(parcel, country_code):
    """Build single-parcel CSV files (used for archive-hit regenerated exports).

    Args:
        parcel: single parcel dict with parcel_code, vertices, resolved_provider_name,
                archive_date, cadastre_code.
        country_code: alpha-2 country code.

    Returns:
        dict with vertices_path, boundary_path.
    """
    vertices_rows = build_vertices_rows([parcel])
    boundary_rows = build_boundary_rows([parcel])

    export_dir = EXPORTS_DIR / country_code
    export_dir.mkdir(parents=True, exist_ok=True)

    safe_code = parcel['parcel_code'].replace('/', '_').replace('\\', '_')
    ts = _export_ts()
    vertices_path = export_dir / f'{safe_code}_N1_{ts}.csv'
    boundary_path = export_dir / f'{safe_code}_N1_{ts}_boundary.csv'

    write_csv(str(vertices_path), VERTICES_HEADERS, vertices_rows)
    write_csv(str(boundary_path), BOUNDARY_HEADERS, boundary_rows)

    return {
        'vertices_path': str(vertices_path),
        'boundary_path': str(boundary_path),
        'vertices_count': len(vertices_rows),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    data = read_json_stdin()
    parcels = data['parcels']
    first_code = data['first_code']
    count = data['count']
    country_code = data.get('country_code', data.get('iso3', ''))

    result = build_csvs(parcels, first_code, count, country_code)
    write_json_stdout(result)


if __name__ == '__main__':
    main()
