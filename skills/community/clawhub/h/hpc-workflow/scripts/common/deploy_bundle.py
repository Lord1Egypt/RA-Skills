"""Deploy one frozen profile bundle over its already-authenticated exec route."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import subprocess

REMOTE = (Path(__file__).resolve().parent / 'install-release.py').read_text(encoding='utf-8')


def freeze(directory):
    root = Path(directory)
    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
    payload = dict(site=manifest['site'], manifest=manifest, hashes=manifest['files'], files={})
    if not isinstance(manifest.get('site'), str) or '/' in manifest['site'] or '..' in manifest['site']:
        raise ValueError('Invalid bundle namespace')
    for name, expected in manifest['files'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('Invalid bundle member')
        data = (root / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('Bundle changed: ' + name)
        payload['files'][name] = base64.b64encode(data).decode()
    profile = json.loads(base64.b64decode(payload['files']['profile.json']))
    if profile['name'] != manifest['site']:
        raise ValueError('Profile and manifest identity differ')
    payload['archive'] = profile['storage']['archive']
    return profile, payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle'); parser.add_argument('--apply', action='store_true')
    parser.add_argument('--rollback', metavar='REMOTE_BACKUP', help='Restore an exact prior installation; requires --apply')
    args = parser.parse_args()
    profile, payload = freeze(args.bundle)
    if args.rollback:
        payload['rollback'] = args.rollback
    if not args.apply:
        print(json.dumps(dict(site=profile['name'], exec_argv=profile['transport']['exec_argv'], files=sorted(payload['files']),
                              action='rollback' if args.rollback else 'deploy', applied=False)))
        return
    encoded = base64.b64encode(json.dumps(payload).encode()).decode()
    script = "python3 - <<'HPC_INSTALL_PY'\nPAYLOAD = " + repr(encoded) + '\n' + REMOTE + '\nHPC_INSTALL_PY\n'
    subprocess.run(profile['transport']['exec_argv'], input=script.encode(), check=True)


if __name__ == '__main__':
    main()
