"""
Handlebars-style template engine using Python stdlib only.
Supports {{variable}}, {{#if}}, {{#each}}, and {{#unless}} blocks.
Also includes personality blending utilities.
"""

import json
import re
from pathlib import Path

TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "templates"
PROFILES_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "personality-profiles"
COMMUNITY_DIR = Path(__file__).resolve().parent.parent.parent / "assets" / "community-templates"


def _resolve_var(name, context):
    """Resolve dotted variable name from context dict."""
    parts = name.strip().split(".")
    val = context
    for p in parts:
        if isinstance(val, dict):
            val = val.get(p)
        else:
            return None
        if val is None:
            return None
    return val


def render(template_str, context):
    """Render a Handlebars-style template string with the given context."""
    result = template_str

    # Process {{#each items}} ... {{/each}} blocks
    each_pattern = re.compile(
        r"\{\{#each\s+([\w.]+)\}\}(.*?)\{\{/each\}\}", re.DOTALL
    )
    while each_pattern.search(result):
        def replace_each(m):
            list_name = m.group(1)
            body = m.group(2)
            items = _resolve_var(list_name, context)
            if not items or not isinstance(items, list):
                return ""
            output = []
            for item in items:
                if isinstance(item, dict):
                    rendered = render(body, {**context, **item, "this": item})
                else:
                    rendered = render(body, {**context, "this": str(item)})
                output.append(rendered)
            return "".join(output)
        result = each_pattern.sub(replace_each, result)

    # Process {{#if var}} ... {{else}} ... {{/if}} blocks
    if_else_pattern = re.compile(
        r"\{\{#if\s+([\w.]+)\}\}(.*?)\{\{else\}\}(.*?)\{\{/if\}\}", re.DOTALL
    )
    while if_else_pattern.search(result):
        def replace_if_else(m):
            var_name = m.group(1)
            true_block = m.group(2)
            false_block = m.group(3)
            val = _resolve_var(var_name, context)
            if val and val != "none" and val is not False:
                return render(true_block, context)
            return render(false_block, context)
        result = if_else_pattern.sub(replace_if_else, result)

    # Process {{#if var}} ... {{/if}} blocks (no else)
    if_pattern = re.compile(
        r"\{\{#if\s+([\w.]+)\}\}(.*?)\{\{/if\}\}", re.DOTALL
    )
    while if_pattern.search(result):
        def replace_if(m):
            var_name = m.group(1)
            body = m.group(2)
            val = _resolve_var(var_name, context)
            if val and val != "none" and val is not False:
                return render(body, context)
            return ""
        result = if_pattern.sub(replace_if, result)

    # Process {{#unless var}} ... {{/unless}} blocks
    unless_pattern = re.compile(
        r"\{\{#unless\s+([\w.]+)\}\}(.*?)\{\{/unless\}\}", re.DOTALL
    )
    while unless_pattern.search(result):
        def replace_unless(m):
            var_name = m.group(1)
            body = m.group(2)
            val = _resolve_var(var_name, context)
            if not val or val == "none" or val is False:
                return render(body, context)
            return ""
        result = unless_pattern.sub(replace_unless, result)

    # Replace simple {{variable}} tokens
    def replace_var(m):
        var_name = m.group(1).strip()
        val = _resolve_var(var_name, context)
        if val is None:
            return ""
        if isinstance(val, list):
            return ", ".join(str(v) for v in val)
        return str(val)

    result = re.sub(r"\{\{([\w.]+)\}\}", replace_var, result)

    return result


def load_template(name):
    """Load a template file from the assets/templates directory."""
    path = TEMPLATE_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Template not found: {path}")
    return path.read_text(encoding="utf-8")


def render_template(name, context):
    """Load and render a template by name."""
    template_str = load_template(name)
    return render(template_str, context)


# --- Personality Blending ---

def load_profile(name):
    """Load a personality profile by name from profiles or community templates."""
    path = PROFILES_DIR / f"{name}.json"
    if not path.exists():
        path = COMMUNITY_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Profile not found: {name}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def blend_profiles(archetypes):
    """
    Blend multiple archetype profiles with weights.

    Args:
        archetypes: list of {"name": "companion", "weight": 0.7} dicts

    Returns:
        A merged profile dict with weighted trait/style merging.
    """
    if not archetypes:
        raise ValueError("At least one archetype required for blending")

    # Normalize weights
    total = sum(a.get("weight", 1.0) for a in archetypes)
    weighted = [(a["name"], a.get("weight", 1.0) / total) for a in archetypes]

    # Load all profiles
    profiles = [(load_profile(name), weight) for name, weight in weighted]

    # Start with first profile as base
    result = json.loads(json.dumps(profiles[0][0]))

    # Blend traits: collect all unique traits, weighted by presence
    trait_scores = {}
    for profile, weight in profiles:
        for trait in profile.get("traits", []):
            trait_scores[trait] = trait_scores.get(trait, 0) + weight
    # Sort by weight descending, keep top traits
    sorted_traits = sorted(trait_scores.items(), key=lambda x: -x[1])
    result["traits"] = [t for t, _ in sorted_traits[:6]]

    # Blend communication style (numeric fields use weighted average)
    comm = {}
    for key in ("brevity",):
        val = sum(
            p.get("communication", {}).get(key, 3) * w
            for p, w in profiles
        )
        comm[key] = round(val)

    # Boolean/enum fields: use highest-weight profile's value
    primary_profile = max(profiles, key=lambda x: x[1])[0]
    primary_comm = primary_profile.get("communication", {})
    comm["humor"] = primary_comm.get("humor", False)
    comm["swearing"] = primary_comm.get("swearing", "never")
    comm["banOpeningPhrases"] = primary_comm.get("banOpeningPhrases", True)
    result["communication"] = comm

    # Blend boundaries: use primary for booleans, weighted for emotional depth
    depth_map = {"none": 0, "low": 1, "medium": 2, "high": 3}
    depth_reverse = {0: "none", 1: "low", 2: "medium", 3: "high"}
    depth_val = sum(
        depth_map.get(p.get("boundaries", {}).get("emotionalDepth", "none"), 0) * w
        for p, w in profiles
    )
    primary_bounds = primary_profile.get("boundaries", {})
    result["boundaries"] = {
        "petNames": primary_bounds.get("petNames", False),
        "flirtation": primary_bounds.get("flirtation", False),
        "emotionalDepth": depth_reverse.get(round(depth_val), "low"),
        "protective": primary_bounds.get("protective", True),
    }

    # Blend vibe summaries
    vibes = []
    for profile, weight in profiles:
        vibe = profile.get("vibeSummary", "")
        if vibe:
            vibes.append(vibe)
    if len(vibes) > 1:
        result["vibeSummary"] = " ".join(vibes)
    elif vibes:
        result["vibeSummary"] = vibes[0]

    # Blend brevity/swearing descriptions from primary
    result["brevityDesc"] = primary_profile.get("brevityDesc", "")
    result["swearingDesc"] = primary_profile.get("swearingDesc", "")

    # Combine platform notes
    all_notes = []
    seen = set()
    for profile, _ in profiles:
        for note in profile.get("platformNotes", []):
            if note not in seen:
                all_notes.append(note)
                seen.add(note)
    result["platformNotes"] = all_notes

    # Set archetype to "blend"
    result["archetype"] = "blend"
    result["blendSources"] = [{"name": n, "weight": w} for n, w in weighted]

    return result
