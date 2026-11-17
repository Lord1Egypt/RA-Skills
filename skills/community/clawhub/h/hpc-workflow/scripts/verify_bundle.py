"""Verify a skill's packaged files without an external repository checkout."""
import hashlib
import json
from pathlib import Path


def verify(root):
    manifest = json.loads((root / 'bundle-manifest.json').read_text(encoding='utf-8'))
    for name, expected in manifest['files'].items():
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise ValueError('Invalid skill member: ' + name)
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Packaged file changed: ' + name)
    return dict(skill_version=manifest['skill_version'], core_version=manifest['core_version'], verified_files=len(manifest['files']))


if __name__ == '__main__':
    print(json.dumps(verify(Path(__file__).resolve().parents[1])))
