import argparse
from mss_client import api_get


def get_timeline(target_id):
    data = api_get(f"/targets/{target_id}/timeline")
    events = data.get("events", [])

    print(f"TIMELINE — Target {target_id} — {len(events)} events")
    print("=" * 40)

    for e in events:
        print(f"\n  [{e['timestamp']}] {e['type'].upper()}")
        print(f"    By: {e['actor']}")
        if e.get("detail"):
            print(f"    {e['detail']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    get_timeline(args.id)
