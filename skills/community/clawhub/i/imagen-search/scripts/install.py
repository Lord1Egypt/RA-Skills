#!/usr/bin/env python3
"""Explicit, standard-library installer. No credentials, telemetry or auto-update."""
import argparse
import hashlib
import io
import json
import os
import re
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import zipfile

SOURCE = 'https://imagen.chat/downloads/imagen-search-release.json'

def fetch(url):
    u = urlparse(url)
    if u.username or u.password or not (u.scheme == 'https' and u.hostname == 'imagen.chat' or u.scheme == 'http' and u.hostname in ('127.0.0.1', 'localhost')):
        raise ValueError('Only official HTTPS or loopback test sources are allowed')
    with urlopen(Request(url, headers={'User-Agent': 'ImagenSearchInstaller/1.1 (+https://imagen.chat/zh/skills/imagen-search)'}), timeout=30) as response:
        if response.geturl() != url:
            raise ValueError('Unexpected redirect')
        body = response.read(8 * 1024 * 1024 + 1)
        if len(body) > 8 * 1024 * 1024:
            raise ValueError('Release exceeds size limit')
        return body

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def install(skills_dir, source=SOURCE, upgrade=False):
    release = json.loads(fetch(source))
    if not isinstance(release.get('version'), str) or not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', release['version']) or not release.get('files'):
        raise ValueError('Invalid release manifest')
    parent = Path(skills_dir).expanduser().resolve()
    target = parent / 'imagen-search'
    if target.is_symlink():
        raise ValueError('Refusing a symlink installation')
    if target.exists() and not upgrade:
        raise ValueError('Already installed. Review the release and explicitly use --upgrade')
    if target.exists():
        local = target / 'release.json'
        if local.exists() and json.loads(local.read_text(encoding='utf-8')).get('version') == release['version']:
            return {'status': 'already-current', 'version': release['version'], 'path': str(target)}
        if local.exists():
            current = json.loads(local.read_text(encoding='utf-8')).get('version', '')
            if re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', current) and tuple(map(int, current.split('.'))) > tuple(map(int, release['version'].split('.'))):
                raise ValueError('Refusing a downgrade; use the retained backup for explicit rollback')
        inventory = target / '.installed-files.json'
        if inventory.is_symlink():
            raise ValueError('Refusing a symlink inventory')
        if inventory.exists():
            for name, expected in json.loads(inventory.read_text(encoding='utf-8')).items():
                p = target / name
                if not p.is_file() or p.is_symlink() or digest(p) != expected:
                    raise ValueError('Package files were locally modified. Preserve and review before upgrading')
        # Legacy versions had no inventory: preserve their complete directory as backup.
    archive = fetch(release['download_url'])
    if hashlib.sha256(archive).hexdigest() != release['sha256']:
        raise ValueError('ZIP SHA256 mismatch; installation unchanged')
    files = {}
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        total = 0
        for entry in z.infolist():
            parts = PurePosixPath(entry.filename).parts
            mode = entry.external_attr >> 16
            if entry.is_dir() or not parts or parts[0] != 'imagen-search' or len(parts) < 2 or any(p in ('..', '.') for p in parts) or '\\' in entry.filename or ':' in entry.filename or stat.S_ISLNK(mode):
                raise ValueError('Unsafe ZIP entry')
            name = '/'.join(parts[1:])
            if name in files or name not in release['files']:
                raise ValueError('Unexpected or duplicate ZIP entry')
            total += entry.file_size
            if total > 8 * 1024 * 1024:
                raise ValueError('Unpacked release exceeds size limit')
            content = z.read(entry)
            if hashlib.sha256(content).hexdigest() != release['files'][name]:
                raise ValueError('Package file hash mismatch')
            files[name] = content
    if set(files) != set(release['files']) or json.loads(files['release.json'])['version'] != release['version']:
        raise ValueError('Incomplete or inconsistent package')
    parent.mkdir(parents=True, exist_ok=True)
    backup = None
    with tempfile.TemporaryDirectory(prefix='.imagen-stage-', dir=parent) as temp:
        staged = Path(temp) / 'imagen-search'
        if target.exists():
            shutil.copytree(target, staged, symlinks=True)
        else:
            staged.mkdir()
        previous_files = json.loads((target / '.installed-files.json').read_text(encoding='utf-8')) if target.exists() and (target / '.installed-files.json').exists() else None
        for name, content in files.items():
            p = staged / name
            if previous_files is not None and name not in previous_files and p.exists():
                raise ValueError('New package file conflicts with a user file; preserve and review before upgrading')
            if any(part.is_symlink() for part in [p, *p.parents] if part != parent):
                raise ValueError('Refusing package file symlinks')
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(content)
        (staged / '.installed-files.json').write_text(json.dumps(release['files'], indent=2), encoding='utf-8')
        if target.exists():
            backup = Path(tempfile.mkdtemp(prefix='imagen-search.backup-', dir=parent))
            backup.rmdir()
            target.rename(backup)
        try:
            staged.rename(target)
        except Exception:
            if backup:
                backup.rename(target)
            raise
    return {'status': 'upgraded' if backup else 'installed', 'version': release['version'], 'path': str(target), 'backup': str(backup) if backup else None, 'next': 'Refresh your client, then run imagen.mjs start --query "ancient Rome" --out NEW_WORKSPACE_FOLDER'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-dir', required=True)
    parser.add_argument('--source', default=SOURCE)
    parser.add_argument('--upgrade', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(install(args.skills_dir, args.source, args.upgrade), indent=2))
    except Exception as error:
        parser.exit(1, str(error) + '\n')
