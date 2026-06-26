import json

def synthesize_dream_report(dream_data):
    """
    Synthesizes dream elements into a Jungian four-phase structure.
    
    Args:
        dream_data (dict): Keys: setting, conflict, resolution, symbols, dreamer_context
    
    Returns:
        dict: Structured Jungian report
    """
    report = {
        "exposition": dream_data.get("setting"),
        "dramatic_arc": {
            "complication": dream_data.get("conflict"),
            "lysis": dream_data.get("resolution")
        },
        "amplification_map": {},
        "archetypal_hits": [],
        "interpretation_level": dream_data.get("interpretation_level", "subjective"),
        "dream_type": "little_dream"  # Updated to "big_dream" if numinous signals detected
    }

    symbols = dream_data.get("symbols", [])
    
    ARCHETYPE_MAP = {
        "shadow": ["dark figure", "pursuer", "stranger", "enemy", "shadow", "monster"],
        "anima": ["woman", "goddess", "muse", "feminine", "siren", "witch"],
        "animus": ["man", "hero", "authority", "warrior", "masculine"],
        "wise old man": ["sage", "wizard", "mentor", "grandfather", "wise"],
        "great mother": ["grandmother", "mother", "nature", "ocean", "earth"],
        "self": ["mandala", "circle", "gold", "light", "sun", "eye", "center"],
        "hero": ["quest", "battle", "journey", "sword", "threshold"]
    }

    NUMINOUS_SIGNALS = ["eclipse", "cosmic", "thunder", "spoke", "god", "eye of god", "eternal", "apocalypse"]

    for sym in symbols:
        sym_lower = sym.lower()
        matched = []
        for archetype, keywords in ARCHETYPE_MAP.items():
            if any(kw in sym_lower for kw in keywords):
                matched.append(archetype)
        if matched:
            report["archetypal_hits"].append({"symbol": sym, "archetypes": matched})
        
        # Check for Big Dream signals
        if any(signal in sym_lower for signal in NUMINOUS_SIGNALS):
            report["dream_type"] = "big_dream"

    # Build amplification placeholders
    for sym in symbols:
        report["amplification_map"][sym] = {
            "personal_association": "[Ask dreamer: What does this symbol mean to you personally?]",
            "archetypal_parallel": "[Identify myth/fairy tale/religious parallel]"
        }

    return report


def format_report_as_text(report):
    """Formats the structured report into readable analysis text."""
    lines = [
        "=== JUNGIAN DREAM ANALYSIS ===",
        f"\nDream Type: {'BIG DREAM (Numinous/Collective)' if report['dream_type'] == 'big_dream' else 'Little Dream (Personal)'}",
        f"Interpretation Level: {report['interpretation_level'].capitalize()}",
        f"\n--- EXPOSITION ---\n{report['exposition']}",
        f"\n--- DRAMATIC ARC ---",
        f"Complication (Peripeteia): {report['dramatic_arc']['complication']}",
        f"Resolution (Lysis): {report['dramatic_arc']['lysis']}",
        "\n--- ARCHETYPAL HITS ---"
    ]
    
    if report["archetypal_hits"]:
        for hit in report["archetypal_hits"]:
            lines.append(f"  • {hit['symbol']} → {', '.join(hit['archetypes'])}")
    else:
        lines.append("  No direct archetypal matches detected. Proceed with amplification.")

    lines.append("\n--- AMPLIFICATION MAP ---")
    for sym, amp in report["amplification_map"].items():
        lines.append(f"\n  Symbol: {sym}")
        lines.append(f"    Personal: {amp['personal_association']}")
        lines.append(f"    Archetypal: {amp['archetypal_parallel']}")

    return "\n".join(lines)


# Example usage
if __name__ == "__main__":
    example_dream = {
        "setting": "An old library with no exits",
        "conflict": "A dark figure is burning books",
        "resolution": "Finding a golden key in a hollowed book",
        "symbols": ["Dark figure", "Burning books", "Golden key", "Library"],
        "dreamer_context": "Highly rational academic who dismisses emotions"
    }
    
    report = synthesize_dream_report(example_dream)
    print(json.dumps(report, indent=2))
    print("\n")
    print(format_report_as_text(report))
