"""Verify the bundled reviewed core before importing it."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def load():
    sys.dont_write_bytecode=True
    for rel,expected in json.loads((ROOT/'source-pins.json').read_text('utf8')).items():
        if hashlib.sha256((ROOT/'vendor'/rel).read_bytes()).hexdigest()!=expected:
            raise ValueError('Bundled core hash mismatch: '+rel)
    p=str(ROOT/'vendor/backend/src')
    if p not in sys.path:sys.path.insert(0,p)
load()
