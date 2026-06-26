#!/usr/bin/env python3
"""Generate a dashboard extension scaffold and validation manifest."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

def slug(s): return re.sub(r'[^a-z0-9-]+','-',s.lower()).strip('-') or 'dashboard-extension'

def spec_from_args(args):
    if args.spec:
        try:
            spec=json.loads(Path(args.spec).read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            import sys
            print(f"Error: spec file '{args.spec}' contains invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        spec={}
    name=slug(spec.get('name') or args.name)
    return {
        'name': name,
        'tab': spec.get('tab') or args.tab or name.replace('-', ' ').title(),
        'slot': spec.get('slot') or args.slot,
        'api_route': spec.get('api_route') or args.api_route or f'/api/{name}',
        'theme': spec.get('theme') or 'system',
        'permissions': spec.get('permissions') or ['read:status'],
    }

def validate(spec):
    findings=[]
    if not re.fullmatch(r'[a-z0-9-]{3,63}', spec['name']): findings.append({'severity':'HIGH','code':'BAD_NAME','fix':'Use 3-63 lowercase letters/digits/hyphens.'})
    if not spec['api_route'].startswith('/api/'): findings.append({'severity':'MEDIUM','code':'BAD_ROUTE','fix':'Use /api/<extension> route namespace.'})
    if '*' in spec.get('permissions',[]): findings.append({'severity':'HIGH','code':'OVERBROAD_PERMISSION','fix':'Replace wildcard permission with least privilege scopes.'})
    return {'verdict':'REVIEW' if findings else 'READY','findings':findings,'spec':spec}

def write_scaffold(spec, out):
    out.mkdir(parents=True, exist_ok=True); (out/'frontend').mkdir(exist_ok=True); (out/'backend').mkdir(exist_ok=True)
    (out/'extension.json').write_text(json.dumps(spec, indent=2)+'\n', encoding='utf-8')
    (out/'frontend'/f"{spec['name']}.html").write_text(f"""<section data-extension=\"{spec['name']}\">\n  <h1>{spec['tab']}</h1>\n  <p>Mounted in slot: {spec['slot']}</p>\n  <pre id=\"status\">Loading...</pre>\n</section>\n""", encoding='utf-8')
    route_name=spec['name'].replace('-','_')
    (out/'backend'/f"{route_name}_route.py").write_text(f"""#!/usr/bin/env python3\n\"\"\"Backend route stub for {spec['name']}.\"\"\"\nimport json\n\ndef handle(request=None):\n    return {{"status":"ok","extension":"{spec['name']}","route":"{spec['api_route']}"}}\n\nif __name__ == "__main__":\n    print(json.dumps(handle(), indent=2))\n""", encoding='utf-8')

def main():
    p=argparse.ArgumentParser(description='Build Hermes dashboard extension scaffold.')
    p.add_argument('--name', default='agent-ops-tab'); p.add_argument('--tab'); p.add_argument('--slot', default='main-panel'); p.add_argument('--api-route')
    p.add_argument('--spec'); p.add_argument('--output-dir', default='dashboard-extension-out'); p.add_argument('--validate-only', action='store_true')
    args=p.parse_args(); spec=spec_from_args(args); report=validate(spec)
    if not args.validate_only: write_scaffold(spec, Path(args.output_dir)); Path(args.output_dir,'VALIDATION.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
if __name__=='__main__': main()
