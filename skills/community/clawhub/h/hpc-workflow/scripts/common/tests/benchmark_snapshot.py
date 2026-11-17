"""Measure generated snapshot helpers on disposable synthetic data; no GPU needed."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time
from test_profiles import profile, renderer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--size-mib', type=int, default=256)
    parser.add_argument('--files', type=int, default=10000)
    args = parser.parse_args()
    if args.size_mib < 1 or args.files < 1: parser.error('Use positive sizes')
    with tempfile.TemporaryDirectory(prefix='hpc-snapshot-scale-') as temporary:
        root = Path(temporary); base = root / 'base'; work = base / 'workspace'; cache = base / 'cache/uv'
        work.mkdir(parents=True); cache.mkdir(parents=True)
        required = args.size_mib * 1024**2 * 5 + args.files * 4096 * 5
        disk = os.statvfs(str(root))
        if disk.f_bavail * disk.f_frsize < required: raise RuntimeError('Insufficient disposable disk budget')
        source_hash = hashlib.sha256()
        with (cache / 'synthetic.cache').open('wb') as stream:
            for _ in range(args.size_mib):
                chunk = os.urandom(1024**2); stream.write(chunk); source_hash.update(chunk)
        for n in range(args.files):
            (work / ('file-%05d' % n)).write_bytes(os.urandom(2048))
        (work / '.venv').mkdir(); (work / '.venv/excluded').write_text('excluded')
        helper = root / 'msi-local-snapshot'
        helper.write_text(renderer.render(profile('msi'))['bin/msi-local-snapshot']); helper.chmod(0o700)
        archive = root / 'persistent/work.tar.zst'
        env = dict(os.environ, fixture=str(root), SLURM_JOB_ID='900001', MSI_LOCAL_SNAPSHOT_MAX_INCREMENTAL_RATIO='0')
        code = 'source <(sed \'$d\' "$1"); shift; local_base() { echo "$fixture/base"; }; main "$@"'
        timings = {}
        def run(operation):
            start = time.monotonic()
            result = subprocess.run(['bash', '-c', code, 'probe', str(helper), operation, str(archive)],
                                    env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=600)
            if result.returncode: raise RuntimeError(result.stdout)
            timings[operation] = round(time.monotonic() - start, 3)
        run('save'); run('verify')
        marker = work / 'file-00000'; marker.write_text('changed')
        removed = work / 'file-00001' if args.files > 1 else work / 'removed'
        if removed.exists(): removed.unlink()
        run('incsave'); run('compact')
        marker.write_text('uncommitted')
        (work / '.venv/excluded').unlink(); (work / '.venv').rmdir()
        run('restore')
        assert marker.read_text() == 'changed' and not removed.exists() and not (work / '.venv').exists()
        expected = source_hash.hexdigest()
        digest = hashlib.sha256()
        with (cache / 'synthetic.cache').open('rb') as stream:
            for part in iter(lambda: stream.read(1024**2), b''): digest.update(part)
        assert digest.hexdigest() == expected
        print(json.dumps(dict(size_mib=args.size_mib, small_files=args.files, timings_seconds=timings,
                              archive_bytes=archive.stat().st_size, restore_content='verified', exclusions='verified',
                              scope='synthetic single-host local filesystem; not an HPC quota or throughput guarantee')))


if __name__ == '__main__': main()
