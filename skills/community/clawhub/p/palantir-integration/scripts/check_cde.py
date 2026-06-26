import argparse
from mss_client import api_get


def check_cde(target_id, weapon_type):
    data = api_get(f"/targets/{target_id}/cde", params={"weapon": weapon_type})

    print(f"CDE ASSESSMENT — Target {target_id} — Weapon: {weapon_type}\n")
    print(f"  CDE Score: {data['cde_score']}")
    print(f"  Risk Level: {data['risk_level']}")
    print(f"  Blast Radius: {data['blast_radius_m']}m")
    print(f"  Estimated Civilian Population: {data['estimated_civilian_population']}")
    print(f"  No-Fire Zone Conflict: {'YES' if data['no_fire_zone_conflict'] else 'No'}")

    structures = data.get("civilian_structures_in_radius", [])
    if structures:
        print(f"\n  Nearby Civilian Structures ({len(structures)}):")
        for s in structures:
            print(f"    - {s['name']} ({s['type']}) at {s['distance_m']}m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--weapon", default="hellfire")
    args = parser.parse_args()
    check_cde(args.id, args.weapon)
