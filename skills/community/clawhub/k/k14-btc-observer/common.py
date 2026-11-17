from dataclasses import asdict, is_dataclass
from decimal import Decimal
from pathlib import Path
import hashlib
import json
import re
import time

D = Decimal
ZERO = D('0')
UNITS = D('1000000')

def dec(value):
    if isinstance(value, bool):
        raise ValueError('boolean is not money')
    n = D(str(value))
    if not n.is_finite():
        raise ValueError('non-finite number')
    return n

def jsonable(obj):
    if is_dataclass(obj): return jsonable(asdict(obj))
    if hasattr(obj, 'model_dump'): return obj.model_dump(mode='json')
    if isinstance(obj, dict): return {str(k): jsonable(v) for k,v in obj.items()}
    if isinstance(obj, (list,tuple)): return [jsonable(v) for v in obj]
    if isinstance(obj, (Decimal,Path)): return str(obj)
    return obj

def canonical(obj):
    return json.dumps(jsonable(obj), ensure_ascii=False, sort_keys=True, separators=(',',':'), allow_nan=False)

def digest(obj): return hashlib.sha256(canonical(obj).encode()).hexdigest()
def now_ms(): return time.time_ns() // 1000000

def address(value):
    if not isinstance(value,str) or not re.fullmatch(r'0x[0-9a-fA-F]{40}', value):
        raise ValueError('complete EVM address required')
    return value.lower()

def same_condition(a,b):
    a,b=str(a).lower(),str(b).lower()
    if not all(re.fullmatch(r'0x(?:[0-9a-f]{62}|[0-9a-f]{64})',v) for v in (a,b)):return False
    return a==b or (len(a)==64 and b==a+'00') or (len(b)==64 and a==b+'00')

def redact(obj):
    if isinstance(obj,dict):
        return {k: '[REDACTED]' if any(x in k.lower() for x in ('secret','private_key','privatekey','api_key','apikey','passphrase','signature','authorization','mnemonic','seed_phrase')) else redact(v) for k,v in obj.items()}
    if isinstance(obj,list): return [redact(v) for v in obj]
    if isinstance(obj,str) and ('sk_live_' in obj or obj.startswith('Bearer ')): return '[REDACTED]'
    return obj

def atomic_json(path, obj):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temporary=path.with_suffix(path.suffix+'.tmp')
    temporary.write_text(json.dumps(jsonable(obj),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    temporary.replace(path)
