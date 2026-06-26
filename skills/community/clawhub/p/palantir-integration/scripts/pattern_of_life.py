import argparse
from mss_client import api_get


def pattern_of_life(target_id, days):
    data = api_get("/intelligence/pol", params={"target_id": target_id, "days": days})

    print(f"PATTERN OF LIFE — Target {target_id} — Last {days} days")
    print("=" * 40)

    print(f"\nSUMMARY: {data['summary']}\n")

    activity = data.get("activity_windows", [])
    if activity:
        print("ACTIVITY WINDOWS:")
        for w in activity:
            print(f"  {w['time_range']}: {w['activity']} (observed {w['frequency']}x)")
        print()

    movements = data.get("movement_patterns", [])
    if movements:
        print("MOVEMENT PATTERNS:")
        for m in movements:
            print(f"  Route: {m['route']} | Freq: {m['frequency']}x | Last seen: {m['last_observed']}")
        print()

    associates = data.get("associated_entities", [])
    if associates:
        print("ASSOCIATED ENTITIES:")
        for a in associates:
            print(f"  [{a['id']}] {a['relation']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--days", default="7")
    args = parser.parse_args()
    pattern_of_life(args.id, args.days)
