#!/usr/bin/env python3
"""Export the canonical skill and its listing documents without local caches."""
import argparse
from pathlib import Path
import shutil


def export(destination):
    source=Path(__file__).resolve().parents[1]
    target=Path(destination).expanduser().resolve()
    if target.exists():raise ValueError('Choose a destination that does not already exist.')
    if target==source or source in target.parents:raise ValueError('Export outside the source skill folder.')
    # Only distribute known source directories; never copy arbitrary runtime state.
    target.mkdir(parents=True)
    try:
        for name in ('SKILL.md','README.md','CARD.md','CHANGELOG.md','PRIVACY.md','PUBLISHING.md'):
            document=source/name
            if document.is_file():shutil.copy2(document,target/name)
        for folder in ('scripts','assets','references','tests'):
            shutil.copytree(source/folder,target/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc','*.pyo','*.pyd'))
        # SKILL.md already declares the runtime. Preserve it byte-for-byte so
        # GitHub imports and exported bundles have the same version/metadata.
    except Exception:
        shutil.rmtree(target)
        raise
    return target

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination',help='New output folder, normally /path/to/publish/gmail-connect')
    args=parser.parse_args()
    try:print(export(args.destination))
    except (ValueError,OSError) as error:parser.exit(1,str(error)+'\n')
