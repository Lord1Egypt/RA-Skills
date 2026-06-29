#!/usr/bin/env python3
"""Quick regression checks for team-name normalization and query expansion."""

from team_names import canonical_team, expand_team_query_aliases

EXPECTED = {
    "South Korea": ["South Korea", "Korea Republic", "Republic of Korea", "Korea Rep."],
    "Bosnia and Herzegovina": ["Bosnia", "Bosnia-Herzegovina", "Bosnia & Herzegovina", "Bosnia Herzegovina"],
    "Ivory Coast": ["Côte d'Ivoire", "Cote d'Ivoire", "Cote d Ivoire", "Cote D'Ivoire"],
    "DR Congo": ["Democratic Republic of Congo", "Democratic Republic of the Congo", "Congo DR", "DRC", "Congo-Kinshasa"],
    "Republic of the Congo": ["Congo", "Congo Republic", "Congo-Brazzaville"],
    "Cape Verde": ["Cabo Verde", "Republic of Cabo Verde"],
    "Czechia": ["Czech Republic"],
    "United Arab Emirates": ["UAE", "U.A.E."],
}


def main() -> int:
    for canonical, aliases in EXPECTED.items():
        resolved = {canonical_team(alias) for alias in [canonical, *aliases]}
        if resolved != {canonical}:
            raise SystemExit(f"canonicalization failed for {canonical}: {resolved}")

    for query, must_include in {
        "South Korea": ["South Korea", "Korea Republic", "Republic of Korea"],
        "Bosnia": ["Bosnia and Herzegovina", "Bosnia-Herzegovina"],
        "UAE": ["United Arab Emirates"],
    }.items():
        expanded = expand_team_query_aliases(query)
        missing = [item for item in must_include if item not in expanded]
        if missing:
            raise SystemExit(f"query expansion failed for {query}: missing {missing} in {expanded}")

    print("team-name normalization smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
