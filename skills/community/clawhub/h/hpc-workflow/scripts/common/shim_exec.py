"""Stream a shell script through an existing exec/push shim, preserving its auth."""
import argparse
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import uuid


def run_script(shim, source):
    # Large scripts never travel in Windows process arguments.
    destination = '~/.local/state/hpc-core-staging/' + uuid.uuid4().hex + '/script.sh'
    setup = 'umask 077; mkdir -p "$HOME/.local/state/hpc-core-staging/' + destination.split('/')[-2] + '"'
    with tempfile.TemporaryDirectory(prefix='hpc-shim-script-') as temporary:
        path = Path(temporary) / 'script.sh'; path.write_bytes(source)
        digest = hashlib.sha256(source).hexdigest()
        subprocess.run(shim + ['exec', 'bash', '-c', setup], check=True)
        subprocess.run(shim + ['push', str(path), destination, '600'], check=True)
        verify = ('import hashlib,os,sys; p=os.path.expanduser(sys.argv[1]); '
                  'assert hashlib.sha256(open(p,"rb").read()).hexdigest()==sys.argv[2],"Staged script hash mismatch"; '
                  'os.execv("/bin/bash",["bash",p])')
        subprocess.run(shim + ['exec', 'python3', '-c', verify, destination, digest], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('shim', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    shim = args.shim[1:] if args.shim[:1] == ['--'] else args.shim
    if not shim: parser.error('Supply an existing exec/push shim argv after --')
    run_script(shim, sys.stdin.buffer.read())


if __name__ == '__main__': main()
