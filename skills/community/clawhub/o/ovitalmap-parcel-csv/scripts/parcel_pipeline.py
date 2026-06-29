"""
End-to-end parcel processing pipeline for ovitalmap.

This is the main orchestrator that the LLM calls.  It accepts a JSON description
of one or more parcels (with WGS84 coordinates already parsed by the LLM) and
runs through the complete flow:

    1. Country localization  (LLM-determined from coordinates + context)
    2. Provider matching     (fuzzy dedup with ambiguous flag)
    2b. Duplicate detection  (coordinate-based, order-independent)
        → archive hits reuse existing parcel_code + metadata
    3. Code assignment       (sequential, only for genuinely new parcels)
    4. CSV generation        (vertices + boundary for ALL parcels)
    5. Archive append        (per-country + master, only for new parcels)

CLI usage:
    echo '{
      "parcels": [{
        "vertices": [[114.13472, 22.50422], [114.13564, 22.50411]],
        "provider_name": "张三",
        "official_id": null,
        "altitude": []
      }],
      "date": "260610"
    }' | python3 scripts/parcel_pipeline.py --step 1

    Steps:
      --step 1   → country + provider match (read-only, no file writes)
      --step 2b  → duplicate check: reuse matched_codes for hits, identify new
      --step 2   → code assignment for new parcels only (reads archive)
      --step 3   → CSV build for ALL parcels + archive for new only
      --step all → run everything (interactive — waits for user between steps)
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(SCRIPT_DIR))

from utils import read_csv, get_workspace_root

WORKSPACE_ROOT = get_workspace_root()

from country_locator import locate_country
from archive_manager import scan_archive, check_duplicate, append_parcels, update_cadastre
from csv_builder import build_csvs, build_single_csvs
from provider_matcher import fuzzy_match


_TODAY = datetime.now().strftime('%Y-%m-%d')
STATE_FILE = WORKSPACE_ROOT / 'ovitalmap_archive' / '.pipeline_state.json'


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {}


# ---------------------------------------------------------------------------
# Step 1: Country + Provider match
# ---------------------------------------------------------------------------

def step1_country_and_provider(parcels):
    """Determine country and check provider names for all parcels.

    Returns:
        dict with: country_code, country_name, provider_results, existing_providers
    """
    all_vertices = []
    for p in parcels:
        all_vertices.extend(p.get('vertices', []))

    country_result = locate_country(all_vertices)
    country_code = country_result.get('country_code')

    for p in parcels:
        p['country_code'] = country_code

    if country_code:
        archive_scan = scan_archive(country_code)
        existing_providers = archive_scan.get('all_providers', [])
        # Also scan master.csv for cross-country providers (SKILL §7.4)
        master_path = WORKSPACE_ROOT / 'ovitalmap_archive' / 'master.csv'
        _, master_rows = read_csv(str(master_path))
        if master_rows:
            master_providers = set()
            for r in master_rows:
                pn = r.get('provider_name', '').strip()
                if pn and pn.lower() != 'unknown':
                    master_providers.add(pn)
            existing_providers = sorted(set(existing_providers) | master_providers)
    else:
        archive_scan = {}
        existing_providers = []

    provider_results = []
    for p in parcels:
        provider_name = p.get('provider_name', '')
        if provider_name:
            match_result = fuzzy_match(provider_name, existing_providers)
            provider_results.append({
                'input_name': provider_name,
                'exact_match': match_result.get('exact_match'),
                'candidates': match_result.get('candidates', []),
                'ambiguous': match_result.get('ambiguous', False),
            })
        else:
            provider_results.append({
                'input_name': '',
                'exact_match': None,
                'candidates': [],
                'ambiguous': False,
            })

    return {
        'country_code': country_code,
        'country_name': country_result.get('country_name'),
        'method': country_result.get('method'),
        'per_vertex': country_result.get('per_vertex', []),
        'country_code_counts': country_result.get('country_code_counts', {}),
        'provider_results': provider_results,
        'archive_exists': archive_scan.get('archive_exists', False),
        'existing_providers': existing_providers,
    }


# ---------------------------------------------------------------------------
# Step 2b: Duplicate check (runs BEFORE code assignment)
# ---------------------------------------------------------------------------

def step2b_check_duplicates(parcels, country_code, resolved_provider_name):
    """Check each parcel against the archive by coordinates.  Archive hits reuse
    the existing parcel_code and carry over archive metadata.  Non-hits remain
    for code assignment in step 2.

    Args:
        parcels: list of parcel dicts (vertices, provider_name, official_id).
        country_code: alpha-2 country code.
        resolved_provider_name: confirmed provider name for the batch.

    Returns:
        dict with: duplicate_results, archive_hit_parcels, new_parcels,
                   all_parcels_ordered (preserving original input order for step 3)
    """
    duplicate_results = []
    archive_hit_parcels = []
    new_parcels = []
    all_parcels_ordered = []

    for i, p in enumerate(parcels):
        result = check_duplicate(country_code, p.get('vertices', []))
        match_found = result.get('match_found', False)
        matched_code = result.get('matched_code')
        matched_provider = result.get('matched_provider')
        matched_cadastre = result.get('matched_cadastre_code', '')
        matched_archive_date = result.get('matched_archive_date', '')

        dup_entry = {
            'index': i,
            'match_found': match_found,
        }

        if match_found:
            # Reuse the archived parcel_code — do NOT assign a new one
            p['parcel_code'] = matched_code
            p['resolved_provider_name'] = matched_provider or resolved_provider_name
            p['archive_date'] = matched_archive_date
            # Prefer the new official_id over the old cadastre if provided
            p['cadastre_code'] = p.get('official_id') or matched_cadastre
            p['is_archive_hit'] = True

            # Check if we should update cadastre_code in the archive files
            existing_is_date_code = bool(
                matched_code and not matched_cadastre and
                len(matched_code.split('-')[-1]) == 3 and matched_code.split('-')[-1].isdigit()
            )
            dup_entry['matched_code'] = matched_code
            dup_entry['matched_provider'] = matched_provider
            dup_entry['matched_cadastre_code'] = matched_cadastre
            dup_entry['existing_is_date_code'] = existing_is_date_code
            dup_entry['needs_cadastre_update'] = existing_is_date_code and bool(p.get('official_id'))

            # Update the archive files if the match had a date-code and user now provides an official ID
            if existing_is_date_code and p.get('official_id'):
                update_result = update_cadastre(
                    country_code, matched_code, p.get('official_id')
                )
                dup_entry['cadastre_update_result'] = update_result

            archive_hit_parcels.append(p)
        else:
            p['is_archive_hit'] = False
            p['resolved_provider_name'] = resolved_provider_name
            p['archive_date'] = _TODAY
            p['cadastre_code'] = p.get('official_id', '')
            new_parcels.append(p)

        duplicate_results.append(dup_entry)
        all_parcels_ordered.append(p)

    return {
        'duplicate_results': duplicate_results,
        'archive_hit_parcels': archive_hit_parcels,
        'new_parcels': new_parcels,
        'all_parcels_ordered': all_parcels_ordered,
    }


# ---------------------------------------------------------------------------
# Step 2: Code assignment (only for new parcels)
# ---------------------------------------------------------------------------

def step2_assign_codes(new_parcels, country_code, date_hint):
    """Assign parcel_codes.  Uses official_id (format 1) when available,
    otherwise falls back to sequential (format 2).

    Args:
        new_parcels: list of parcel dicts that are NOT archive hits.
        country_code: alpha-2 country code.
        date_hint: YYMMDD string.

    Returns:
        dict with: assigned_codes (list), warnings (list)
    """
    if not new_parcels:
        return {'assigned_codes': [], 'warnings': [], 'message': 'No new parcels to assign codes to.'}

    archive_scan = scan_archive(country_code, date_hint)
    existing_codes = set(archive_scan.get('all_codes', []))
    today_max_seq = archive_scan.get('today_max_seq', 0)
    seq = today_max_seq

    assigned = []
    warnings = []

    for i, p in enumerate(new_parcels):
        official_id = p.get('official_id')
        is_sequential = True

        if official_id:
            # Format 1: {CC}-{OFFICIAL_ID}
            candidate = f'{country_code}-{official_id}'
            if candidate in existing_codes:
                warnings.append(f'Parcel {i + 1}: Official ID {candidate} already exists in archive. Falling back to sequential.')
                candidate = None
            else:
                is_sequential = False
        else:
            candidate = None

        # Format 2: {CC}-{YYMMDD}-{SEQ} (fallback)
        if candidate is None:
            seq += 1
            candidate = f'{country_code}-{date_hint}-{seq:03d}'
            while candidate in existing_codes:
                seq += 1
                candidate = f'{country_code}-{date_hint}-{seq:03d}'

        existing_codes.add(candidate)
        p['parcel_code'] = candidate
        if official_id:
            p['cadastre_code'] = official_id
        assigned.append({
            'index': i,
            'parcel_code': candidate,
            'is_sequential': is_sequential,
        })

    return {
        'assigned_codes': assigned,
        'warnings': warnings,
        'today_max_seq': today_max_seq,
        'new_max_seq': seq,
    }


# ---------------------------------------------------------------------------
# Step 3: Build CSVs (ALL parcels) + Archive (new parcels only)
# ---------------------------------------------------------------------------

def step3_build_and_archive(all_parcels, new_parcels, country_code):
    """Generate CSVs for every parcel (including archive hits). Archive only new ones.

    Archive-hit parcels get single-parcel CSV exports regenerated with fresh
    Comment metadata (provider, date, cadastre).

    Args:
        all_parcels: every parcel (new + archive hits), each with parcel_code,
                     vertices, resolved_provider_name, archive_date, cadastre_code.
        new_parcels: subset that needs archiving (not archive hits).
        country_code: alpha-2 country code.

    Returns:
        dict with: new_csv_result, hit_csv_results, archive_result
    """
    from utils import build_boundary_string

    # --- Archive-hit parcels: generate individual single-parcel CSVs ---
    hit_csv_results = []
    for p in all_parcels:
        if not p.get('is_archive_hit'):
            continue
        result = build_single_csvs(p, country_code)
        hit_csv_results.append(result)

    # --- New parcels: batch CSV + archive ---
    new_csv_result = None
    archive_result = None

    if new_parcels:
        first_code = new_parcels[0]['parcel_code']
        count_new = len(new_parcels)
        new_csv_result = build_csvs(new_parcels, first_code, count_new, country_code)

        today = datetime.now().strftime('%Y-%m-%d')
        archive_rows = []
        for p in new_parcels:
            archive_rows.append({
                'parcel_code': p['parcel_code'],
                'provider_name': p.get('resolved_provider_name', p.get('provider_name', 'Unknown')),
                'archive_date': today,
                'boundary_coords': build_boundary_string(p.get('vertices', [])),
                'provider_notes': p.get('provider_notes', ''),
                'cadastre_code': p.get('cadastre_code', ''),
            })

        archive_result = append_parcels(country_code, archive_rows)

    return {
        'new_csv_result': new_csv_result,
        'hit_csv_results': hit_csv_results,
        'archive_result': archive_result,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Ovitalmap parcel pipeline')
    parser.add_argument('--step', choices=['1', '2b', '2', '3', 'all'], default='all',
                        help='Pipeline step to run (2b=duplicate check, 2=codes, 3=CSV+archive)')
    args = parser.parse_args()

    data = json.load(sys.stdin)
    parcels = data.get('parcels', [])
    date_hint = data.get('date', datetime.now().strftime('%y%m%d'))
    country_code = data.get('country_code', data.get('iso3'))
    resolved_provider_name = data.get('resolved_provider_name')

    step = args.step

    if step == 'all':
        result = {}
    else:
        result = load_state()
        if not country_code:
            country_code = result.get('step1', {}).get('country_code')
        if not resolved_provider_name:
            resolved_provider_name = result.get('resolved_provider_name')

    if step in ('1', 'all'):
        s1 = step1_country_and_provider(parcels)
        result['step1'] = s1
        country_code = country_code or s1.get('country_code')

    if step in ('2b', 'all'):
        if not country_code:
            country_code = result.get('step1', {}).get('country_code')
        if country_code:
            s2b = step2b_check_duplicates(parcels, country_code, resolved_provider_name)
            result['step2b'] = s2b
        else:
            result['step2b'] = {'error': 'No country_code available. Run step 1 first.'}

    if step in ('2', 'all'):
        if not country_code:
            country_code = result.get('step1', {}).get('country_code')
        new_parcels = result.get('step2b', {}).get('new_parcels', [])
        if not new_parcels:
            all_ordered = result.get('step2b', {}).get('all_parcels_ordered', [])
            new_parcels = [p for p in all_ordered if not p.get('is_archive_hit')]
        if not new_parcels:
            new_parcels = parcels
        if country_code:
            s2 = step2_assign_codes(new_parcels, country_code, date_hint)
            result['step2'] = s2
        else:
            result['step2'] = {'error': 'No country_code available.'}

    if step in ('3', 'all'):
        if not country_code:
            country_code = result.get('step1', {}).get('country_code')
        if country_code:
            all_parcels = result.get('step2b', {}).get('all_parcels_ordered', [])
            if not all_parcels:
                all_parcels = parcels
            new_parcels = result.get('step2b', {}).get('new_parcels', [])
            if not new_parcels:
                new_parcels = [p for p in all_parcels if not p.get('is_archive_hit')]
            s3 = step3_build_and_archive(all_parcels, new_parcels, country_code)
            result['step3'] = s3
        else:
            result['step3'] = {'error': 'No country_code available.'}

    if step != 'all':
        result['resolved_provider_name'] = resolved_provider_name
        save_state(result)

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
