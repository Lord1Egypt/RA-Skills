import argparse
from mss_client import api_get


def deconfliction_check(target_id, radius_km):
    data = api_get("/deconfliction/check", params={"target_id": target_id, "radius_km": radius_km})

    clear = data["all_clear"]
    print(f"DECONFLICTION — Target {target_id} — Radius {radius_km}km")
    print(f"STATUS: {'ALL CLEAR' if clear else 'CONFLICTS DETECTED'}")
    print("=" * 40)

    friendly = data.get("friendly_forces", [])
    if friendly:
        print(f"\nFRIENDLY FORCES ({len(friendly)}):")
        for f in friendly:
            print(f"  {f['unit']} at {f['distance_km']}km ({f['heading']}) - {f['status']}")

    no_fire = data.get("no_fire_zones", [])
    if no_fire:
        print(f"\nNO-FIRE ZONES ({len(no_fire)}):")
        for nf in no_fire:
            print(f"  {nf['name']} at {nf['distance_km']}km - {nf['reason']}")

    airspace = data.get("restricted_airspace", [])
    if airspace:
        print(f"\nRESTRICTED AIRSPACE ({len(airspace)}):")
        for a in airspace:
            print(f"  Zone {a['zone_id']}: {a['altitude_range']} ft | Active until: {a['active_until']}")

    missions = data.get("active_missions", [])
    if missions:
        print(f"\nACTIVE MISSIONS ({len(missions)}):")
        for m in missions:
            print(f"  [{m['mission_id']}] {m['type']} by {m['asset']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--radius_km", default="10")
    args = parser.parse_args()
    deconfliction_check(args.id, args.radius_km)
