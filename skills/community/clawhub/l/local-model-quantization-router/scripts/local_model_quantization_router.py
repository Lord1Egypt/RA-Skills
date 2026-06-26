#!/usr/bin/env python3
"""Recommend local model and quantization routes."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def choose(args, hw):
    vram=float(hw.get('vram_gb', args.vram_gb)); ram=float(hw.get('ram_gb', args.ram_gb)); cpu_only=bool(hw.get('cpu_only', False))
    reasons=[]; complexity=args.complexity; privacy=args.privacy; ctx=args.context_tokens
    if privacy in ('high','regulated'): route='local-only'; reasons.append('privacy requires local processing')
    elif complexity == 'critical': route='hybrid'; reasons.append('critical task needs cloud-quality fallback')
    else: route='local-first'; reasons.append('routine workload can start local to reduce spend')
    if cpu_only or vram < 4:
        model='qwen2.5:3b-instruct'; quant='Q4_K_M'; reasons.append('low/no VRAM favours small Q4 model')
    elif vram < 8:
        model='qwen2.5:7b-instruct'; quant='Q4_K_M'; reasons.append('4-8GB VRAM supports 7B Q4')
    elif vram < 16:
        model='qwen2.5:14b-instruct'; quant='Q4_K_M'; reasons.append('8-16GB VRAM supports 14B Q4')
    else:
        model='qwen2.5:32b-instruct'; quant='Q5_K_M'; reasons.append('16GB+ VRAM supports larger Q5 quality')
    if ctx > 32768:
        reasons.append('large context may exceed local model comfort zone')
        if privacy not in ('high','regulated'): route='hybrid'
    if complexity == 'critical' and privacy not in ('high','regulated'):
        fallback='cloud premium model with human review'
    elif ctx > 32768:
        fallback='chunking/RAG before escalation'
    else:
        fallback='next-larger local quantization or cloud standard model'
    if ram < 16 and vram < 8:
        route='local-first' if privacy not in ('high','regulated') else 'local-only'; reasons.append('limited RAM: keep prompts short and monitor latency')
    return {'route':route,'model':model,'quantization':quant,'endpoint':'ollama-compatible local endpoint','fallback':fallback,'reasons':reasons,'inputs':{'task':args.task,'complexity':complexity,'privacy':privacy,'vram_gb':vram,'ram_gb':ram,'context_tokens':ctx}}

def main():
    p=argparse.ArgumentParser(description='Route tasks to local quantized models or fallback.')
    p.add_argument('--task', default='summarise routine support tickets'); p.add_argument('--complexity', choices=['simple','standard','complex','critical'], default='standard')
    p.add_argument('--privacy', choices=['low','normal','high','regulated'], default='normal'); p.add_argument('--vram-gb', type=float, default=8); p.add_argument('--ram-gb', type=float, default=32)
    p.add_argument('--context-tokens', type=int, default=8192); p.add_argument('--hardware'); p.add_argument('--output')
    args=p.parse_args()
    if args.hardware:
        try:
            hw=json.loads(Path(args.hardware).read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            import sys
            print(f"Error: hardware file '{args.hardware}' contains invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        hw={}
    result=choose(args, hw); data=json.dumps(result, indent=2)
    if args.output: Path(args.output).write_text(data+'\n', encoding='utf-8')
    print(data)
if __name__=='__main__': main()
