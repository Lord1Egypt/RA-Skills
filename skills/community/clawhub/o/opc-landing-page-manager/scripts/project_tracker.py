#!/usr/bin/env python3
"""
Landing page project tracker for opc-landing-page-manager.

Manages the project index, tracks versions, readiness scoring, and provides
project status.

Usage:
    python3 project_tracker.py [pages_dir]
    python3 project_tracker.py --index [pages_dir]
    python3 project_tracker.py --status [pages_dir]
    python3 project_tracker.py --list [pages_dir]
    python3 project_tracker.py --versions PROJECT_ID [pages_dir]
    python3 project_tracker.py --readiness [pages_dir]
    python3 project_tracker.py --json [pages_dir]

Options:
    --index         Rebuild INDEX.json from project directories
    --status        Show status summary of all projects
    --list          List all projects (one per line)
    --versions ID   Show version history for a project
    --readiness     Show publish-readiness report for all projects
    --json          Output as JSON instead of human-readable
    pages_dir       Path to landing-pages directory (default: ./landing-pages)

Exit codes:
    0   Success
    1   Error

Dependencies: Python 3.8+ stdlib only
"""

import argparse
import json
import sys
from datetime import date
from pathlib import Path


def find_projects(pages_dir: Path) -> list:
    """Find all project directories containing metadata.json."""
    projects = []
    if not pages_dir.is_dir():
        return projects

    for d in sorted(pages_dir.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith('.') or d.name == 'INDEX.json':
            continue

        meta_path = d / 'metadata.json'
        if meta_path.is_file():
            try:
                with open(meta_path, 'r') as f:
                    meta = json.load(f)
                meta['_dir'] = str(d)
                projects.append(meta)
            except (json.JSONDecodeError, OSError) as e:
                print(f"Warning: Could not read {meta_path}: {e}", file=sys.stderr)
        else:
            # Check for versioned subdirectories
            for vd in sorted(d.iterdir()):
                if vd.is_dir() and (vd / 'metadata.json').is_file():
                    try:
                        with open(vd / 'metadata.json', 'r') as f:
                            meta = json.load(f)
                        meta['_dir'] = str(vd)
                        projects.append(meta)
                    except (json.JSONDecodeError, OSError) as e:
                        print(f"Warning: Could not read {vd / 'metadata.json'}: {e}",
                              file=sys.stderr)

    return projects


def compute_readiness(project: dict) -> dict:
    """Compute publish-readiness score for a project."""
    score = 0
    details = {}
    blockers = project.get('publish_blockers', [])
    missing = project.get('missing_assets', [])

    # CTA target defined (15 points)
    cta_defined = project.get('cta_target_defined')
    if cta_defined is True:
        score += 15
        details['cta_target'] = 'defined'
    else:
        details['cta_target'] = 'not defined'

    # Privacy policy linked (10 points)
    privacy = project.get('privacy_policy_linked')
    if privacy is True:
        score += 10
        details['privacy_policy'] = 'linked'
    else:
        details['privacy_policy'] = 'missing'

    # Terms linked (10 points)
    terms = project.get('terms_linked')
    if terms is True:
        score += 10
        details['terms'] = 'linked'
    else:
        details['terms'] = 'missing'

    # Analytics status (0-10 points)
    analytics = project.get('analytics_status', 'none')
    if analytics == 'configured':
        score += 10
        details['analytics'] = 'configured'
    elif analytics == 'placeholder':
        score += 5
        details['analytics'] = 'placeholder'
    else:
        details['analytics'] = 'none'

    # Missing assets (0-20 points)
    if not missing:
        score += 20
        details['missing_assets'] = 'none'
    elif len(missing) <= 2:
        score += 10
        details['missing_assets'] = f'{len(missing)} items'
    else:
        details['missing_assets'] = f'{len(missing)} items'

    # Publish blockers (0-20 points)
    if not blockers:
        score += 20
        details['blockers'] = 'none'
    else:
        details['blockers'] = f'{len(blockers)} issues'

    # Status at least "build" (15 points)
    status = project.get('status', '')
    build_or_later = ['build', 'review', 'published']
    if status in build_or_later:
        score += 15
        details['status_progress'] = status
    else:
        details['status_progress'] = f'{status} (pre-build)'

    return {
        'score': score,
        'missing_assets': missing,
        'publish_blockers': blockers,
        'details': details,
        'page_type': project.get('page_type'),
        'evidence_tier': project.get('evidence_tier')
    }


def format_readiness_human(projects: list) -> str:
    """Format readiness report for human reading."""
    lines = []
    lines.append("READINESS REPORT")
    lines.append("")
    lines.append(f"  {'Product':<30s} {'Score':>5s}  {'Status':<12s} {'Blockers'}")
    lines.append("  " + "-" * 75)

    for pid, p in projects:
        readiness = compute_readiness(p)
        blockers = readiness['publish_blockers']
        blocker_str = ', '.join(blockers[:3]) if blockers else 'None'
        if len(blockers) > 3:
            blocker_str += f' (+{len(blockers) - 3} more)'
        name = p.get('product_name', pid)[:30]
        status = p.get('status', 'unknown')
        lines.append(
            f"  {name:<30s} {readiness['score']:>4d}%  {status:<12s} {blocker_str}"
        )

    return "\n".join(lines)


def build_index(pages_dir: Path) -> dict:
    """Build INDEX.json from all project metadata."""
    projects = find_projects(pages_dir)

    # Deduplicate: keep latest version per project_id
    latest = {}
    for p in projects:
        pid = p.get('project_id', '')
        version = p.get('version', 1)
        if pid not in latest or version > latest[pid].get('version', 1):
            latest[pid] = p

    index = {
        "generated_at": date.today().isoformat(),
        "total_projects": len(latest),
        "projects": []
    }

    status_counts = {}
    for pid in sorted(latest.keys()):
        p = latest[pid]
        status = p.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1

        entry = {
            "project_id": pid,
            "product_name": p.get('product_name', ''),
            "status": status,
            "version": p.get('version', 1),
            "created_at": p.get('created_at', ''),
            "updated_at": p.get('updated_at', ''),
            "conversion_goal": p.get('strategy', {}).get('conversion_goal', ''),
            "product_type": p.get('strategy', {}).get('product_type', ''),
            "directory": p.get('_dir', '')
        }

        # Include variant count
        variants = p.get('variants', [])
        if variants:
            entry["variant_count"] = len(variants)

        # Include lifecycle fields
        if p.get('page_type'):
            entry["page_type"] = p["page_type"]
        if p.get('evidence_tier'):
            entry["evidence_tier"] = p["evidence_tier"]
        if p.get('readiness_score') is not None:
            entry["readiness_score"] = p["readiness_score"]

        index["projects"].append(entry)

    index["status_summary"] = status_counts

    # Write INDEX.json
    index_path = pages_dir / 'INDEX.json'
    # Remove _dir from projects before writing
    for proj in index["projects"]:
        proj.pop('_dir', None)

    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)

    return index


def get_status_summary(pages_dir: Path) -> dict:
    """Get a status summary of all projects."""
    projects = find_projects(pages_dir)

    # Deduplicate by project_id
    latest = {}
    for p in projects:
        pid = p.get('project_id', '')
        version = p.get('version', 1)
        if pid not in latest or version > latest[pid].get('version', 1):
            latest[pid] = p

    summary = {
        "total": len(latest),
        "by_status": {},
        "projects": []
    }

    for pid in sorted(latest.keys()):
        p = latest[pid]
        status = p.get('status', 'unknown')
        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
        project_entry = {
            "project_id": pid,
            "product_name": p.get('product_name', ''),
            "status": status,
            "version": p.get('version', 1),
            "updated_at": p.get('updated_at', p.get('created_at', ''))
        }
        if p.get('page_type'):
            project_entry["page_type"] = p["page_type"]
        if p.get('readiness_score') is not None:
            project_entry["readiness_score"] = p["readiness_score"]
        blocker_count = len(p.get('publish_blockers', []))
        if blocker_count > 0:
            project_entry["publish_blockers_count"] = blocker_count
        summary["projects"].append(project_entry)

    return summary


def get_versions(pages_dir: Path, project_id: str) -> list:
    """Get all versions of a project."""
    projects = find_projects(pages_dir)
    versions = [p for p in projects if p.get('project_id') == project_id]
    versions.sort(key=lambda x: x.get('version', 1))
    return versions


def format_status_human(summary: dict) -> str:
    """Format status summary for human reading."""
    lines = []
    lines.append(f"Landing Page Projects: {summary['total']} total")
    lines.append("")

    if summary["by_status"]:
        lines.append("By Status:")
        status_order = ["strategy", "copy", "design", "build", "review", "published", "archived"]
        for status in status_order:
            count = summary["by_status"].get(status, 0)
            if count > 0:
                lines.append(f"  {status}: {count}")

    lines.append("")
    lines.append("Projects:")
    for p in summary["projects"]:
        version_str = f"v{p['version']}" if p.get('version', 1) > 1 else ""
        updated = f" (updated {p['updated_at']})" if p.get('updated_at') else ""
        lines.append(
            f"  [{p['status']:10s}] {p['product_name']}"
            f" {version_str}{updated}"
        )

    return "\n".join(lines)


def format_versions_human(versions: list, project_id: str) -> str:
    """Format version history for human reading."""
    if not versions:
        return f"No versions found for project: {project_id}"

    lines = [f"Version history for: {project_id}", ""]
    for v in versions:
        status = v.get('status', 'unknown')
        created = v.get('created_at', '')
        updated = v.get('updated_at', '')
        directory = v.get('_dir', '')
        lines.append(
            f"  v{v.get('version', 1):3d}  [{status:10s}]  "
            f"created: {created}  updated: {updated}"
        )
        if directory:
            lines.append(f"         dir: {directory}")

        # Show variant/experiment info if present
        variants = v.get('variants', [])
        for var in variants:
            var_type = var.get('variant_type', '')
            hypothesis = var.get('hypothesis', '')
            decision = var.get('decision', '')
            changed = var.get('changed_sections', [])
            parts = [f"type: {var_type}"]
            if hypothesis:
                parts.append(f"hypothesis: {hypothesis}")
            if changed:
                parts.append(f"changed: {', '.join(changed)}")
            if decision:
                parts.append(f"decision: {decision}")
            lines.append(f"         variant: {' | '.join(parts)}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Landing page project tracker."
    )
    parser.add_argument(
        'pages_dir',
        nargs='?',
        default='./landing-pages',
        help='Path to landing-pages directory (default: ./landing-pages)'
    )
    parser.add_argument(
        '--index',
        action='store_true',
        help='Rebuild INDEX.json from project directories'
    )
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show status summary of all projects'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all projects (one per line)'
    )
    parser.add_argument(
        '--versions',
        metavar='PROJECT_ID',
        help='Show version history for a project'
    )
    parser.add_argument(
        '--readiness',
        action='store_true',
        help='Show publish-readiness report for all projects'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()
    pages_dir = Path(args.pages_dir)

    if not pages_dir.is_dir():
        if args.json:
            print(json.dumps({"error": f"Directory not found: {pages_dir}"}))
        else:
            print(f"Directory not found: {pages_dir}", file=sys.stderr)
            print("No landing page projects found. Create your first project to get started.")
        sys.exit(0)

    try:
        if args.readiness:
            projects = find_projects(pages_dir)
            # Deduplicate
            latest = {}
            for p in projects:
                pid = p.get('project_id', '')
                version = p.get('version', 1)
                if pid not in latest or version > latest[pid].get('version', 1):
                    latest[pid] = p

            if args.json:
                readiness_data = []
                for pid in sorted(latest.keys()):
                    r = compute_readiness(latest[pid])
                    r['project_id'] = pid
                    r['product_name'] = latest[pid].get('product_name', '')
                    r['status'] = latest[pid].get('status', '')
                    readiness_data.append(r)
                print(json.dumps(readiness_data, indent=2))
            else:
                sorted_projects = [(pid, latest[pid]) for pid in sorted(latest.keys())]
                print(format_readiness_human(sorted_projects))

        elif args.index:
            index = build_index(pages_dir)
            if args.json:
                print(json.dumps(index, indent=2))
            else:
                print(f"Index rebuilt: {index['total_projects']} projects indexed.")

        elif args.versions:
            versions = get_versions(pages_dir, args.versions)
            if args.json:
                # Remove _dir for clean output
                clean = [{k: v for k, v in v_item.items() if k != '_dir'}
                         for v_item in versions]
                print(json.dumps(clean, indent=2))
            else:
                print(format_versions_human(versions, args.versions))

        elif args.list:
            projects = find_projects(pages_dir)
            # Deduplicate
            seen = {}
            for p in projects:
                pid = p.get('project_id', '')
                version = p.get('version', 1)
                if pid not in seen or version > seen[pid].get('version', 1):
                    seen[pid] = p

            if args.json:
                result = [{"project_id": pid, "product_name": p.get('product_name', '')}
                          for pid, p in sorted(seen.items())]
                print(json.dumps(result, indent=2))
            else:
                for pid in sorted(seen.keys()):
                    print(f"{pid}  {seen[pid].get('product_name', '')}")

        else:
            # Default: status summary
            summary = get_status_summary(pages_dir)
            if args.json:
                print(json.dumps(summary, indent=2))
            else:
                print(format_status_human(summary))

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
