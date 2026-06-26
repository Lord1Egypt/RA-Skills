#!/usr/bin/env python3
"""Render full Kitchen upload instructions from a recipe JSON spec.

Usage:
  python3 scripts/render_kitchen_instructions.py \
    --recipe /path/to/recipe.json \
    --out /path/to/kitchen-instructions.md
"""

import argparse
import json
from pathlib import Path


def fmt_bool(v):
    return "true" if bool(v) else "false"


def main():
    ap = argparse.ArgumentParser(description="Render Kitchen instructions from recipe JSON")
    ap.add_argument("--recipe", required=True, help="Path to recipe JSON")
    ap.add_argument("--out", required=True, help="Output markdown path")
    args = ap.parse_args()

    recipe_path = Path(args.recipe)
    data = json.loads(recipe_path.read_text())

    lines = []
    lines.append(f"# Kitchen Upload Instructions — {data.get('name', 'Recipe')}\n")

    lines.append("## Basics")
    lines.append(f"- Name: `{data.get('name', '')}`")
    lines.append(f"- Description: `{data.get('description', '')}`\n")

    onboarding = data.get("onboarding", {})
    lines.append("## Onboarding")
    ic = onboarding.get("inputContext")
    if isinstance(ic, list):
        lines.append("### inputContext entries")
        for i, item in enumerate(ic, 1):
            lines.append(f"{i}. **{item.get('id', f'field_{i}')}**")
            for k in ["label", "prompt", "required", "formatHint"]:
                if k in item:
                    val = item[k]
                    if isinstance(val, bool):
                        val = fmt_bool(val)
                    lines.append(f"   - {k}: `{val}`")
    else:
        lines.append(f"- inputContext: `{ic or ''}`")

    pft = onboarding.get("prefilledFirstText", "")
    lines.append("\n### prefilledFirstText")
    lines.append(f"`{pft}`\n")

    lines.append("## Integrations")
    req = data.get("integrations", {}).get("required", [])
    if req:
        for i, integ in enumerate(req, 1):
            lines.append(f"### Required {i}")
            for k in ["type", "name", "url", "transport", "authentication", "shareWithUsers", "notes"]:
                if k in integ:
                    val = integ[k]
                    if isinstance(val, bool):
                        val = fmt_bool(val)
                    lines.append(f"- {k}: `{val}`")
    else:
        lines.append("- No required integrations specified")

    autos = data.get("automations", [])
    lines.append("\n## Automations")
    if autos:
        for i, a in enumerate(autos, 1):
            lines.append(f"### {i}) {a.get('name', 'Automation')} ({a.get('id', 'no-id')})")
            sch = a.get("schedule", {})
            if sch:
                for k in ["description", "timezone", "cron", "day", "time"]:
                    if k in sch:
                        lines.append(f"- schedule.{k}: `{sch[k]}`")
            if "actionText" in a:
                lines.append(f"- actionText: `{a['actionText']}`")
    else:
        lines.append("- None")

    st = data.get("sandboxTestPrompts") or data.get("publishNotes", {}).get("sandboxChecklist", [])
    lines.append("\n## Sandbox checks")
    if st:
        for i, s in enumerate(st, 1):
            lines.append(f"{i}. {s}")
    else:
        lines.append("1. Add at least 5 sandbox checks/prompts")

    lines.append("\n## CLI bootstrap")
    lines.append("```bash")
    lines.append("npx poke@latest login")
    for integ in req:
        url = integ.get("url", "<MCP_URL>")
        name = integ.get("name", "Integration")
        lines.append(f'npx poke@latest mcp add {url} -n "{name}"')
    lines.append("```")

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()
