#!/usr/bin/env python3
"""
TurboQuant Server - Persistent Python process for fast compression.

Run once: python3 turboquant-server.py
Then: Send JSON to stdin, receive JSON from stdout

Commands:
  {"cmd": "compress", "e": [...], "b": 3}
  {"cmd": "similarity", "q": [...], "c": "base64..."}
"""

import sys
import json
import base64
import numpy as np

# Pre-import (slow first time, fast after)
sys.path.insert(0, '/home/homelab/projects/turboquant_pkg')
from turboquant import TurboQuantProd

# Cache quantizers by dimension and bits
_quantizers = {}

def get_quantizer(dimension: int, bits: int):
    key = (dimension, bits)
    if key not in _quantizers:
        _quantizers[key] = TurboQuantProd(dimension, bits, seed=42)
    return _quantizers[key]

def compress(embedding: list, bits: int = 3) -> dict:
    arr = np.array(embedding, dtype=np.float32)
    arr = arr / np.linalg.norm(arr)
    
    q = get_quantizer(len(embedding), bits)
    compressed = q.quantize(arr)
    
    return {
        'i': base64.b64encode(compressed['mse_indices'].numpy().tobytes()).decode(),
        's': base64.b64encode(compressed['qjl_signs'].numpy().tobytes()).decode(),
        'r': float(compressed['residual_norm']),
        'd': len(embedding),
        'b': bits,
    }

def similarity(query: list, compressed: dict) -> float:
    q = np.array(query, dtype=np.float32)
    q = q / np.linalg.norm(q)
    
    c = {
        'mse_indices': np.frombuffer(base64.b64decode(compressed['i']), dtype=np.int64),
        'qjl_signs': np.frombuffer(base64.b64decode(compressed['s']), dtype=np.uint8),
        'residual_norm': compressed['r'],
    }
    
    quantizer = get_quantizer(compressed['d'], compressed['b'])
    ip = quantizer.inner_product(q.unsqueeze(0), c)
    return float(ip[0])

def main():
    # Ready signal
    print(json.dumps({'status': 'ready'}), flush=True)
    
    for line in sys.stdin:
        try:
            data = json.loads(line)
            cmd = data.get('cmd')
            
            if cmd == 'compress':
                result = compress(data['e'], data.get('b', 3))
                result['cmd'] = 'compressed'
                print(json.dumps(result), flush=True)
                
            elif cmd == 'similarity':
                score = similarity(data['q'], data['c'])
                print(json.dumps({'cmd': 'score', 's': score}), flush=True)
                
            elif cmd == 'ping':
                print(json.dumps({'cmd': 'pong'}), flush=True)
                
            else:
                print(json.dumps({'error': f'Unknown command: {cmd}'}), flush=True)
                
        except Exception as e:
            print(json.dumps({'error': str(e)}), flush=True)

if __name__ == '__main__':
    main()