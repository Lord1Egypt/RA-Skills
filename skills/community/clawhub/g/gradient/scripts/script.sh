#!/usr/bin/env bash
# gradient/scripts/script.sh — CSS Gradient Generator & Palette Builder
# Data: ~/.gradient/data.jsonl
set -euo pipefail
VERSION="1.0.0"
DATA_DIR="$HOME/.gradient"
DATA_FILE="$DATA_DIR/data.jsonl"
mkdir -p "$DATA_DIR"
touch "$DATA_FILE"

CMD="${1:-help}"
shift 2>/dev/null || true

show_help() {
cat << 'HELPEOF'
Gradient — CSS Gradient Generator & Palette Builder  v1.0.0

Usage: bash scripts/script.sh <command> [options]

Commands:
  create      Create a new gradient with type, colors, angle, and name
  list        List all saved gradients
  get         Get full details and CSS code for a gradient
  update      Update an existing gradient
  delete      Remove a gradient by ID
  linear      Shortcut to generate a linear gradient
  radial      Shortcut to generate a radial gradient
  conic       Shortcut to generate a conic gradient
  random      Generate random gradients
  palette     Generate related gradients from a base color
  export      Export gradients as CSS, Tailwind, or SCSS
  preview     Generate an HTML preview page
  help        Show this help message
  version     Print the tool version
HELPEOF
}

case "$CMD" in
  create|list|get|update|delete|linear|radial|conic|random|palette|export|preview)
    SKILL_CMD="$CMD" SKILL_ARGV="$(printf '%s\n' "$@")" python3 << 'PYEOF'
import sys, json, os, uuid, datetime, colorsys, random as rng, re

DATA_DIR = os.path.expanduser("~/.gradient")
DATA_FILE = os.path.join(DATA_DIR, "data.jsonl")

def load_records():
    records = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return records

def save_records(records):
    with open(DATA_FILE, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

def append_record(record):
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")

def gen_id():
    return uuid.uuid4().hex[:8]

def now_iso():
    return datetime.datetime.now().isoformat()

def parse_args(args):
    parsed = {}
    i = 0
    while i < len(args):
        if args[i].startswith("--"):
            key = args[i][2:]
            if i + 1 < len(args) and not args[i+1].startswith("--"):
                parsed[key] = args[i+1]
                i += 2
            else:
                parsed[key] = True
                i += 1
        else:
            i += 1
    return parsed

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))

def rgb_to_hsl(r, g, b):
    r1, g1, b1 = r/255.0, g/255.0, b/255.0
    h, l, s = colorsys.rgb_to_hls(r1, g1, b1)
    return h*360, s*100, l*100

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360.0, l/100.0, s/100.0)
    return round(r*255), round(g*255), round(b*255)

def parse_stops(stops_str):
    """Parse stops like '#ff0000,#00ff00,#0000ff' or '#ff0000:0%,#00ff00:50%,#0000ff:100%'"""
    stops = []
    parts = stops_str.split(",")
    for i, part in enumerate(parts):
        part = part.strip()
        if ":" in part and not part.startswith("#") or (part.count(":") > 0 and "%" in part):
            # format: color:position
            segments = part.rsplit(":", 1)
            color = segments[0].strip()
            position = segments[1].strip()
            stops.append({"color": color, "position": position})
        else:
            # auto-distribute
            if len(parts) > 1:
                pct = round(i / (len(parts) - 1) * 100)
            else:
                pct = 0
            stops.append({"color": part, "position": f"{pct}%"})
    return stops

def build_css_linear(angle, stops):
    stop_strs = [f"{s['color']} {s['position']}" for s in stops]
    return f"linear-gradient({angle}deg, {', '.join(stop_strs)})"

def build_css_radial(shape, position, stops):
    stop_strs = [f"{s['color']} {s['position']}" for s in stops]
    return f"radial-gradient({shape} at {position}, {', '.join(stop_strs)})"

def build_css_conic(from_angle, stops):
    stop_strs = [f"{s['color']} {s['position']}" for s in stops]
    return f"conic-gradient(from {from_angle}deg, {', '.join(stop_strs)})"

def cmd_create(args):
    opts = parse_args(args)
    name = opts.get("name", f"gradient-{gen_id()[:4]}")
    grad_type = opts.get("type", "linear")
    angle = int(opts.get("angle", "135"))
    stops_str = opts.get("stops", "#667eea,#764ba2")
    shape = opts.get("shape", "circle")
    position = opts.get("position", "center")
    from_angle = int(opts.get("from", "0"))
    stops = parse_stops(stops_str)

    if grad_type == "linear":
        css = build_css_linear(angle, stops)
    elif grad_type == "radial":
        css = build_css_radial(shape, position, stops)
    elif grad_type == "conic":
        css = build_css_conic(from_angle, stops)
    else:
        print(json.dumps({"error": f"Invalid type: {grad_type}"}))
        sys.exit(1)

    record = {
        "id": gen_id(),
        "name": name,
        "type": grad_type,
        "angle": angle,
        "stops": stops_str,
        "css": css,
        "created_at": now_iso()
    }
    append_record(record)
    print(css)
    print(json.dumps({"saved": record["id"], "name": name}, indent=2), file=sys.stderr)

def cmd_list(args):
    records = load_records()
    if not records:
        print("No saved gradients.")
        return
    print(f"{'ID':<10} {'Name':<20} {'Type':<8} {'CSS (truncated)':<50}")
    print("-" * 88)
    for r in records:
        css_short = r.get("css", "")[:48]
        print(f"{r.get('id','?'):<10} {r.get('name','?'):<20} {r.get('type','?'):<8} {css_short:<50}")

def cmd_get(args):
    opts = parse_args(args)
    gid = opts.get("id", opts.get("name", ""))
    records = load_records()
    for r in records:
        if r.get("id") == gid or r.get("name") == gid:
            print(json.dumps(r, indent=2))
            return
    print(json.dumps({"error": f"Gradient '{gid}' not found"}))
    sys.exit(1)

def cmd_update(args):
    opts = parse_args(args)
    gid = opts.get("id", "")
    if not gid:
        print(json.dumps({"error": "Please provide --id"}))
        sys.exit(1)
    records = load_records()
    found = False
    for r in records:
        if r.get("id") == gid:
            found = True
            if "name" in opts:
                r["name"] = opts["name"]
            if "angle" in opts:
                r["angle"] = int(opts["angle"])
            if "stops" in opts:
                r["stops"] = opts["stops"]
                stops = parse_stops(opts["stops"])
                grad_type = r.get("type", "linear")
                if grad_type == "linear":
                    r["css"] = build_css_linear(r.get("angle", 135), stops)
                elif grad_type == "radial":
                    r["css"] = build_css_radial(opts.get("shape", "circle"), opts.get("position", "center"), stops)
                elif grad_type == "conic":
                    r["css"] = build_css_conic(r.get("angle", 0), stops)
            r["updated_at"] = now_iso()
            print(json.dumps(r, indent=2))
            break
    if not found:
        print(json.dumps({"error": f"Gradient '{gid}' not found"}))
        sys.exit(1)
    save_records(records)

def cmd_delete(args):
    opts = parse_args(args)
    gid = opts.get("id", "")
    if not gid:
        print(json.dumps({"error": "Please provide --id"}))
        sys.exit(1)
    records = load_records()
    new_records = [r for r in records if r.get("id") != gid]
    if len(new_records) == len(records):
        print(json.dumps({"error": f"Gradient '{gid}' not found"}))
        sys.exit(1)
    save_records(new_records)
    print(json.dumps({"deleted": True, "id": gid}))

def cmd_linear(args):
    opts = parse_args(args)
    angle = int(opts.get("angle", "90"))
    stops_str = opts.get("stops", "#667eea,#764ba2")
    name = opts.get("name", f"linear-{gen_id()[:4]}")
    stops = parse_stops(stops_str)
    css = build_css_linear(angle, stops)
    record = {"id": gen_id(), "name": name, "type": "linear", "angle": angle, "stops": stops_str, "css": css, "created_at": now_iso()}
    append_record(record)
    print(css)

def cmd_radial(args):
    opts = parse_args(args)
    shape = opts.get("shape", "circle")
    position = opts.get("position", "center")
    stops_str = opts.get("stops", "#00d2ff,#3a7bd5")
    name = opts.get("name", f"radial-{gen_id()[:4]}")
    stops = parse_stops(stops_str)
    css = build_css_radial(shape, position, stops)
    record = {"id": gen_id(), "name": name, "type": "radial", "shape": shape, "position": position, "stops": stops_str, "css": css, "created_at": now_iso()}
    append_record(record)
    print(css)

def cmd_conic(args):
    opts = parse_args(args)
    from_angle = int(opts.get("from", "0"))
    stops_str = opts.get("stops", "#ff0000,#00ff00,#0000ff,#ff0000")
    name = opts.get("name", f"conic-{gen_id()[:4]}")
    stops = parse_stops(stops_str)
    css = build_css_conic(from_angle, stops)
    record = {"id": gen_id(), "name": name, "type": "conic", "from_angle": from_angle, "stops": stops_str, "css": css, "created_at": now_iso()}
    append_record(record)
    print(css)

def cmd_random(args):
    opts = parse_args(args)
    count = int(opts.get("count", "1"))
    hue_range = opts.get("hue", "0-360")
    hue_parts = hue_range.split("-")
    hue_min, hue_max = int(hue_parts[0]), int(hue_parts[1])
    grad_type = opts.get("type", "")

    gradients = []
    for _ in range(count):
        h1 = rng.uniform(hue_min, hue_max)
        h2 = (h1 + rng.uniform(30, 180)) % 360
        s1, s2 = rng.uniform(50, 100), rng.uniform(50, 100)
        l1, l2 = rng.uniform(30, 70), rng.uniform(30, 70)
        c1 = rgb_to_hex(*hsl_to_rgb(h1, s1, l1))
        c2 = rgb_to_hex(*hsl_to_rgb(h2, s2, l2))
        angle = rng.choice([0, 45, 90, 135, 180, 225, 270, 315])
        gtype = grad_type if grad_type else rng.choice(["linear", "linear", "linear", "radial"])
        stops = parse_stops(f"{c1},{c2}")

        if gtype == "linear":
            css = build_css_linear(angle, stops)
        elif gtype == "radial":
            css = build_css_radial("circle", "center", stops)
        else:
            css = build_css_linear(angle, stops)

        name = f"random-{gen_id()[:4]}"
        record = {"id": gen_id(), "name": name, "type": gtype, "stops": f"{c1},{c2}", "css": css, "created_at": now_iso()}
        append_record(record)
        gradients.append({"name": name, "type": gtype, "css": css})

    print(json.dumps({"gradients": gradients}, indent=2))

def cmd_palette(args):
    opts = parse_args(args)
    color = opts.get("color", "#3498db")
    count = int(opts.get("count", "5"))
    r, g, b = hex_to_rgb(color)
    h, s, l = rgb_to_hsl(r, g, b)
    gradients = []

    for i in range(count):
        offset = (360 / count) * i
        h2 = (h + offset) % 360
        h3 = (h2 + 40) % 360
        c1 = rgb_to_hex(*hsl_to_rgb(h2, s, l))
        c2 = rgb_to_hex(*hsl_to_rgb(h3, min(s + 10, 100), min(l + 15, 85)))
        angle = 135
        stops = parse_stops(f"{c1},{c2}")
        css = build_css_linear(angle, stops)
        name = f"palette-{gen_id()[:4]}"
        record = {"id": gen_id(), "name": name, "type": "linear", "stops": f"{c1},{c2}", "css": css, "created_at": now_iso()}
        append_record(record)
        gradients.append({"name": name, "css": css})

    print(json.dumps({"base": color, "gradients": gradients}, indent=2))

def cmd_export(args):
    opts = parse_args(args)
    fmt = opts.get("format", "css")
    output = opts.get("output", f"gradients.{fmt}")
    records = load_records()

    if fmt == "css":
        lines = ["/* Generated Gradient Classes */"]
        for r in records:
            safe = re.sub(r'[^a-zA-Z0-9-]', '-', r.get("name", r.get("id", "")))
            lines.append(f".gradient-{safe} {{")
            lines.append(f"  background: {r.get('css', '')};")
            lines.append("}")
            lines.append("")
        content = "\n".join(lines)
    elif fmt == "tailwind":
        obj = {}
        for r in records:
            safe = re.sub(r'[^a-zA-Z0-9_]', '_', r.get("name", r.get("id", "")))
            obj[safe] = r.get("css", "")
        content = f"// Tailwind gradient config\nmodule.exports = {json.dumps(obj, indent=2)};"
    elif fmt == "scss":
        lines = ["// Generated Gradient SCSS Variables"]
        for r in records:
            safe = re.sub(r'[^a-zA-Z0-9-]', '-', r.get("name", r.get("id", "")))
            lines.append(f"$gradient-{safe}: {r.get('css', '')};")
            lines.append(f"@mixin gradient-{safe}() {{ background: $gradient-{safe}; }}")
            lines.append("")
        content = "\n".join(lines)
    else:
        content = json.dumps(records, indent=2)

    with open(output, "w") as f:
        f.write(content)
    print(json.dumps({"exported": output, "format": fmt, "count": len(records)}))

def cmd_preview(args):
    opts = parse_args(args)
    output = opts.get("output", "gradient_preview.html")
    records = load_records()

    cards = []
    for r in records:
        css = r.get("css", "")
        name = r.get("name", r.get("id", "?"))
        cards.append(f'''<div class="card">
  <div class="swatch" style="background:{css}"></div>
  <div class="info"><strong>{name}</strong><br><code>{css}</code></div>
</div>''')

    html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Gradient Preview</title>
<style>
body {{ font-family: -apple-system, sans-serif; background: #111; color: #eee; padding: 2rem; }}
h1 {{ text-align: center; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }}
.card {{ border-radius: 12px; overflow: hidden; background: #222; }}
.swatch {{ height: 160px; }}
.info {{ padding: 1rem; font-size: 0.85rem; }}
code {{ color: #8be9fd; word-break: break-all; }}
</style></head>
<body>
<h1>Gradient Preview ({len(records)} gradients)</h1>
<div class="grid">
{"".join(cards)}
</div>
</body></html>'''

    with open(output, "w") as f:
        f.write(html)
    print(json.dumps({"preview": output, "count": len(records)}))

# --- main dispatch ---
import shlex
_cmd = os.environ.get("SKILL_CMD", "")
_argv_raw = os.environ.get("SKILL_ARGV", "")
args = [_cmd] + [a for a in _argv_raw.split("\n") if a] if _cmd else []
cmd = args[0] if args else "help"
rest = args[1:]

dispatch = {
    "create": cmd_create,
    "list": cmd_list,
    "get": cmd_get,
    "update": cmd_update,
    "delete": cmd_delete,
    "linear": cmd_linear,
    "radial": cmd_radial,
    "conic": cmd_conic,
    "random": cmd_random,
    "palette": cmd_palette,
    "export": cmd_export,
    "preview": cmd_preview,
}

if cmd in dispatch:
    dispatch[cmd](rest)
else:
    print(f"Unknown command: {cmd}")
    sys.exit(1)
PYEOF
    ;;
  help)
    show_help
    ;;
  version)
    echo "gradient v${VERSION}"
    ;;
  *)
    echo "Error: Unknown command '$CMD'" >&2
    echo "Run 'bash scripts/script.sh help' for usage." >&2
    exit 1
    ;;
esac
