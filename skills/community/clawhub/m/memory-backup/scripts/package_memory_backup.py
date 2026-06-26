#!/usr/bin/env python3
import argparse
import io
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path


def tarinfo_for_bytes(name: str, payload: bytes, mode: int = 0o644) -> tarfile.TarInfo:
    info = tarfile.TarInfo(name)
    info.size = len(payload)
    info.mtime = 0
    info.mode = mode
    return info


def add_manifest(tf: tarfile.TarFile, manifest: dict):
    payload = json.dumps(manifest, indent=2, sort_keys=True).encode('utf-8')
    tf.addfile(tarinfo_for_bytes('manifest.json', payload), fileobj=io.BytesIO(payload))


def add_path(tf: tarfile.TarFile, src: Path, arcname: str):
    tf.add(src, arcname=arcname, recursive=True, filter=_normalize_tarinfo)


def _normalize_tarinfo(info: tarfile.TarInfo) -> tarfile.TarInfo:
    info.uid = 0
    info.gid = 0
    info.uname = ''
    info.gname = ''
    info.mtime = 0
    return info


def archive_name_for(src: Path, workspace: Path, external_root: str = 'external') -> str:
    try:
        return str(src.relative_to(workspace))
    except ValueError:
        parts = [external_root] + [p for p in src.parts if p not in ('/', '')]
        return str(Path(*parts))


def main() -> int:
    parser = argparse.ArgumentParser(description='Create a deterministic memory backup archive from discovery JSON.')
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--discovery', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--systems', nargs='*', default=[])
    args = parser.parse_args()

    workspace = Path(args.workspace).expanduser().resolve()
    discovery_path = Path(args.discovery).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()

    discovery = json.loads(discovery_path.read_text())
    allowed_systems = set(args.systems) if args.systems else {
        key for key, value in discovery.get('detectedSystems', {}).items() if value.get('enabled') and value.get('present')
    }

    approved = []
    included_paths = []
    missing_paths = []
    include_sources: list[Path] = []

    seen = set()
    for item in discovery.get('candidates', []):
        system = item.get('system')
        if system not in allowed_systems:
            continue
        raw = item.get('path')
        if not raw:
            continue
        src = Path(raw).expanduser().resolve()
        if not src.exists():
            missing_paths.append({'path': item.get('displayPath', raw), 'reason': 'candidate missing at package time'})
            continue
        key = str(src)
        if key in seen:
            continue
        seen.add(key)
        include_sources.append(src)
        approved.append(system)
        included_paths.append({
            'path': item.get('displayPath', raw),
            'kind': item.get('kind', 'file'),
            'reason': item.get('reason', ''),
            'system': system,
        })

    manifest = {
        'createdAt': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'workspace': str(workspace),
        'configInspected': discovery.get('configInspected', []),
        'detectedSystems': discovery.get('detectedSystems', {}),
        'approvedSystems': sorted(set(approved)),
        'includedPaths': included_paths,
        'excludedPaths': discovery.get('excludedByDefault', []),
        'missingPaths': missing_paths,
        'notes': discovery.get('notes', []) + ['Config files were inspected for discovery only and were not included in the archive.'],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output, 'w:gz', format=tarfile.PAX_FORMAT) as tf:
        add_manifest(tf, manifest)
        for src in sorted(include_sources):
            add_path(tf, src, archive_name_for(src, workspace))

    print(str(output))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
