"""
Archive manager for ovitalmap parcel database.

Handles scanning existing archives, appending new parcels, duplicate detection,
backup creation, coordinate correction, single-parcel export extraction, and
cadastre code updates.

CLI usage — subcommands via stdin JSON with `"action"` key:

    # Scan archive for a given country code
    echo '{"action":"scan","country_code":"CN","date":"260610"}' | python3 scripts/archive_manager.py

    # Append parcels
    echo '{"action":"append","country_code":"CN","rows":[{...}]}' | python3 scripts/archive_manager.py

    # Check for duplicate by coordinates
    echo '{"action":"check_duplicate","country_code":"CN","vertices":[[114.13,22.50],...]}' | python3 scripts/archive_manager.py

    # Backup archives for a given country code
    echo '{"action":"backup","country_code":"CN"}' | python3 scripts/archive_manager.py

    # Correct coordinates for an existing parcel
    echo '{"action":"correct","country_code":"CN","parcel_code":"CN-260610-001","new_vertices":[[...]]}' | python3 scripts/archive_manager.py

    # Extract a single parcel's CSVs from a batch export
    echo '{"action":"extract_single","country_code":"CN","parcel_code":"CN-260610-001"}' | python3 scripts/archive_manager.py

    # Update cadastre_code for an existing parcel
    echo '{"action":"update_cadastre","country_code":"CN","parcel_code":"CN-260610-001","cadastre_code":"PE12345"}' | python3 scripts/archive_manager.py
"""

import json
import sys
import shutil
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from utils import (
    read_csv, append_csv, write_csv,
    read_json_stdin, write_json_stdout,
    parse_boundary_coords, build_boundary_string, boundaries_equal,
    get_workspace_root,
)

WORKSPACE_ROOT = get_workspace_root()

ARCHIVE_DIR = WORKSPACE_ROOT / 'ovitalmap_archive'
BACKUP_DIR = WORKSPACE_ROOT / 'ovitalmap_backups'
EXPORTS_DIR = WORKSPACE_ROOT / 'ovitalmap_exports'

PER_COUNTRY_HEADERS = [
    'parcel_code', 'provider_name', 'archive_date',
    'boundary_coords', 'provider_notes', 'cadastre_code',
]

MASTER_HEADERS = [
    'CC', 'parcel_code', 'provider_name', 'archive_date',
    'boundary_coords', 'provider_notes', 'cadastre_code',
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _archive_path(country_code):
    return ARCHIVE_DIR / f'{country_code}_parcels.csv'


def _master_path():
    return ARCHIVE_DIR / 'master.csv'


def _today_str():
    return datetime.now().strftime('%Y-%m-%d')


def _backup_timestamp():
    return datetime.now().strftime('%y%m%d_%H%M')


# ---------------------------------------------------------------------------
# Scan
# ---------------------------------------------------------------------------

def scan_archive(country_code, date_hint=None):
    """Scan the per-country archive and return existing codes, max SEQ, and providers.

    Args:
        country_code: alpha-2 country code (e.g. 'CN').
        date_hint: YYMMDD string for computing today's max SEQ (e.g. '260610').
                   Defaults to today.

    Returns:
        dict with keys: all_codes, today_max_seq, all_providers, archive_exists
    """
    if date_hint is None:
        date_hint = datetime.now().strftime('%y%m%d')

    filepath = _archive_path(country_code)
    headers, rows = read_csv(str(filepath))

    if headers is None:
        return {
            'all_codes': [],
            'today_max_seq': 0,
            'all_providers': [],
            'archive_exists': False,
        }

    all_codes = [r.get('parcel_code', '') for r in rows]

    # Find today's max SEQ
    today_prefix = f'{country_code}-{date_hint}-'
    today_seqs = []
    for code in all_codes:
        if code.startswith(today_prefix):
            try:
                seq = int(code.split('-')[-1])
                today_seqs.append(seq)
            except (ValueError, IndexError):
                pass
    today_max_seq = max(today_seqs) if today_seqs else 0

    # Collect all unique provider names
    providers = set()
    for r in rows:
        pn = r.get('provider_name', '').strip()
        if pn and pn.lower() != 'unknown':
            providers.add(pn)

    return {
        'all_codes': all_codes,
        'today_max_seq': today_max_seq,
        'all_providers': sorted(providers),
        'archive_exists': True,
    }


# ---------------------------------------------------------------------------
# Append
# ---------------------------------------------------------------------------

def append_parcels(country_code, rows):
    """Append parcel rows to both per-country and master archives.

    Args:
        country_code: alpha-2 country code.
        rows: list of dicts with keys matching PER_COUNTRY_HEADERS.

    Returns:
        dict with paths written to.
    """
    # Per-country archive
    country_path = str(_archive_path(country_code))
    append_csv(country_path, PER_COUNTRY_HEADERS, rows)

    # Master archive
    master_path = str(_master_path())
    master_rows = []
    for r in rows:
        mr = {'CC': country_code}
        mr.update({k: r.get(k, '') for k in PER_COUNTRY_HEADERS})
        master_rows.append(mr)
    append_csv(master_path, MASTER_HEADERS, master_rows)

    return {
        'country_archive': country_path,
        'master_archive': master_path,
        'rows_appended': len(rows),
    }


# ---------------------------------------------------------------------------
# Duplicate check
# ---------------------------------------------------------------------------

def check_duplicate(country_code, new_vertices):
    """Check if a parcel with the same vertex set already exists in the archive.

    Args:
        country_code: alpha-2 country code.
        new_vertices: list of [lon, lat] pairs.

    Returns:
        dict with keys: match_found, matched_code (if found)
    """
    filepath = _archive_path(country_code)
    headers, rows = read_csv(str(filepath))

    if headers is None:
        return {'match_found': False}

    new_boundary = build_boundary_string(new_vertices)

    for row in rows:
        existing_boundary = row.get('boundary_coords', '')
        if boundaries_equal(new_boundary, existing_boundary):
            return {
                'match_found': True,
                'matched_code': row.get('parcel_code', ''),
                'matched_provider': row.get('provider_name', ''),
                'matched_cadastre_code': row.get('cadastre_code', ''),
                'matched_archive_date': row.get('archive_date', ''),
                'matched_boundary': existing_boundary,
            }

    return {'match_found': False}


# ---------------------------------------------------------------------------
# Extract single parcel from batch export
# ---------------------------------------------------------------------------

def extract_single(country_code, parcel_code, resolved_provider_name=None,
                   archive_date=None, cadastre_code=None):
    """Extract a single parcel's rows from existing batch export CSVs and
    regenerate single-parcel CSVs with updated Comment metadata.

    Searches through `ovitalmap_exports/{country_code}/` for any CSV file
    that contains rows for the given `parcel_code`. Extracts only those rows
    into dedicated single-parcel CSV files with Comment fields reflecting
    provider / date / cadastre info.

    Args:
        country_code: alpha-2 country code.
        parcel_code: the parcel code to extract.
        resolved_provider_name: provider name for Comment (optional).
        archive_date: archive date for Comment (optional).
        cadastre_code: cadastre code for Comment (optional).

    Returns:
        dict with keys: found, vertices_path, boundary_path, or error message.
    """
    export_dir = EXPORTS_DIR / country_code
    if not export_dir.is_dir():
        return {'found': False, 'error': f'Export directory not found: {export_dir}'}

    # Build Comment string
    comment_parts = []
    if resolved_provider_name:
        comment_parts.append(f'提供者:{resolved_provider_name}')
    if archive_date:
        comment_parts.append(f'归档日期:{archive_date}')
    if cadastre_code:
        comment_parts.append(f'地籍号:{cadastre_code}')
    comment = ' '.join(comment_parts)

    # Find all CSV files in the export directory (non-boundary files)
    all_csvs = sorted(export_dir.glob('*.csv'))
    batch_files = [f for f in all_csvs if '_boundary' not in f.name]

    vertex_coords = []
    boundary_rows = []

    for batch_file in batch_files:
        _, rows = read_csv(str(batch_file))
        if rows is None:
            continue
        matched = [r for r in rows if r.get('文件夹', '').strip() == parcel_code]
        if matched:
            for r in matched:
                try:
                    lon = float(r['经度'])
                    lat = float(r['纬度'])
                    vertex_coords.append([lon, lat])
                except (ValueError, KeyError):
                    pass
            # Find corresponding boundary file
            stem = batch_file.stem
            boundary_file = export_dir / f'{stem}_boundary.csv'
            if boundary_file.exists():
                _, b_rows = read_csv(str(boundary_file))
                if b_rows:
                    boundary_rows = [r for r in b_rows if r.get('文件夹', '').strip() == parcel_code
                                     and r.get('名称', '').strip() == parcel_code]
            break

    if not vertex_coords:
        return {'found': False, 'error': f'Parcel {parcel_code} not found in any export file under {export_dir}'}

    # Use csv_builder to regenerate single-parcel CSVs with updated Comment
    from csv_builder import build_single_csvs

    parcel_dict = {
        'parcel_code': parcel_code,
        'vertices': vertex_coords,
        'resolved_provider_name': resolved_provider_name,
        'archive_date': archive_date,
        'cadastre_code': cadastre_code,
    }

    result = build_single_csvs(parcel_dict, country_code)

    return {
        'found': True,
        'parcel_code': parcel_code,
        'vertices_path': result['vertices_path'],
        'boundary_path': result['boundary_path'],
        'vertices_count': result['vertices_count'],
    }


# ---------------------------------------------------------------------------
# Update cadastre code
# ---------------------------------------------------------------------------

def update_cadastre(country_code, parcel_code, cadastre_code):
    """Update the cadastre_code field for an existing parcel in both archives.

    Args:
        country_code: alpha-2 country code.
        parcel_code: parcel code to update.
        cadastre_code: new cadastre code value (e.g. official registration ID).

    Returns:
        dict with updated status.
    """
    updated_country = False
    updated_master = False

    # Update per-country archive
    country_path = str(_archive_path(country_code))
    existing_headers, rows = read_csv(country_path)
    if existing_headers and rows:
        for r in rows:
            if r.get('parcel_code') == parcel_code:
                old = r.get('cadastre_code', '')
                r['cadastre_code'] = cadastre_code
                r['provider_notes'] = (r.get('provider_notes', '') +
                                       f'; Cadastre updated: {old or "(empty)"} → {cadastre_code}').strip('; ')
                updated_country = True
                break
        if updated_country:
            write_csv(country_path, existing_headers, rows)

    # Update master archive
    master_path_str = str(_master_path())
    master_headers, master_rows = read_csv(master_path_str)
    if master_headers and master_rows:
        for r in master_rows:
            if r.get('parcel_code') == parcel_code:
                r['cadastre_code'] = cadastre_code
                existing_notes = r.get('provider_notes', '')
                r['provider_notes'] = (existing_notes +
                                       f'; Cadastre updated: {cadastre_code}').strip('; ')
                updated_master = True
                break
        if updated_master:
            write_csv(master_path_str, master_headers, master_rows)

    return {
        'parcel_code': parcel_code,
        'cadastre_code': cadastre_code,
        'updated_country': updated_country,
        'updated_master': updated_master,
    }


# ---------------------------------------------------------------------------
# Backup
# ---------------------------------------------------------------------------

def backup_archive(country_code):
    """Create timestamped backups of the per-country archive and master CSV."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = _backup_timestamp()
    backed_up = []

    # Per-country archive
    country_src = _archive_path(country_code)
    if country_src.exists():
        country_dst = BACKUP_DIR / f'{country_code}_parcels_{ts}.csv'
        shutil.copy2(str(country_src), str(country_dst))
        backed_up.append(str(country_dst))

    # Master archive
    master_src = _master_path()
    if master_src.exists():
        master_dst = BACKUP_DIR / f'master_{ts}.csv'
        shutil.copy2(str(master_src), str(master_dst))
        backed_up.append(str(master_dst))

    return {'backup_paths': backed_up, 'timestamp': ts}


# ---------------------------------------------------------------------------
# Correct coordinates
# ---------------------------------------------------------------------------

def correct_coordinates(country_code, parcel_code, new_vertices):
    """Update boundary_coords for an existing parcel in both archives.

    Args:
        country_code: alpha-2 country code.
        parcel_code: parcel code to update.
        new_vertices: list of [lon, lat] pairs (new coordinates).

    Returns:
        dict with keys: updated_country, updated_master, backup_paths
    """
    # Backup first
    backup_result = backup_archive(country_code)

    new_boundary = build_boundary_string(new_vertices)
    today = _today_str()
    backup_paths_str = ', '.join(backup_result['backup_paths'])
    backup_note = f"[{today}] Coordinates corrected. Original backup: {backup_paths_str}"

    # Update per-country archive
    country_path = str(_archive_path(country_code))
    country_headers, rows = read_csv(country_path)
    if country_headers and rows:
        for r in rows:
            if r.get('parcel_code') == parcel_code:
                existing = r.get('provider_notes', '')
                r['boundary_coords'] = new_boundary
                r['archive_date'] = today
                r['provider_notes'] = (existing + '; ' + backup_note).strip('; ')
                break
        write_csv(country_path, country_headers, rows)

    # Update master archive
    master_path_str = str(_master_path())
    master_headers, master_rows = read_csv(master_path_str)
    if master_headers and master_rows:
        for r in master_rows:
            if r.get('parcel_code') == parcel_code:
                existing = r.get('provider_notes', '')
                r['boundary_coords'] = new_boundary
                r['archive_date'] = today
                r['provider_notes'] = (existing + '; ' + backup_note).strip('; ')
                break
        write_csv(master_path_str, master_headers, master_rows)

    return {
        'parcel_code': parcel_code,
        'country_code': country_code,
        'new_boundary': new_boundary,
        'backup_paths': backup_result['backup_paths'],
    }


# ---------------------------------------------------------------------------
# CLI dispatcher
# ---------------------------------------------------------------------------

def main():
    data = read_json_stdin()
    action = data.get('action', '')

    if action == 'scan':
        result = scan_archive(
            data.get('country_code', data.get('iso3', '')),  # backward compat
            data.get('date'),
        )

    elif action == 'append':
        result = append_parcels(
            data['country_code'] if 'country_code' in data else data['iso3'],
            data['rows'],
        )

    elif action == 'check_duplicate':
        result = check_duplicate(
            data.get('country_code', data.get('iso3', '')),
            data['vertices'],
        )

    elif action == 'extract_single':
        result = extract_single(
            data.get('country_code', data.get('iso3', '')),
            data['parcel_code'],
        )

    elif action == 'update_cadastre':
        result = update_cadastre(
            data.get('country_code', data.get('iso3', '')),
            data['parcel_code'],
            data['cadastre_code'],
        )

    elif action == 'backup':
        result = backup_archive(data.get('country_code', data.get('iso3', '')))

    elif action == 'correct':
        result = correct_coordinates(
            data.get('country_code', data.get('iso3', '')),
            data['parcel_code'],
            data['new_vertices'],
        )

    else:
        result = {'error': f'Unknown action: {action!r}'}

    write_json_stdout(result)


if __name__ == '__main__':
    main()
