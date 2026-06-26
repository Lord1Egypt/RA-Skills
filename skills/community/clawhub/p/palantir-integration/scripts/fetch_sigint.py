import argparse
from mss_client import api_get


def fetch_sigint(target_id, radius_km, hours):
    data = api_get("/intelligence/sigint", params={
        "target_id": target_id,
        "radius_km": radius_km,
        "hours_back": hours,
    })

    intercepts = data.get("intercepts", [])
    if not intercepts:
        print(f"No SIGINT data near target {target_id} within {radius_km}km / last {hours}h.")
        return

    print(f"SIGINT REPORT — Target {target_id}")
    print(f"Radius: {radius_km}km | Window: last {hours}h")
    print(f"Total intercepts: {len(intercepts)}\n")

    for i, item in enumerate(intercepts, 1):
        print(f"  [{i}] {item['timestamp']} | {item['frequency']} MHz | Type: {item['type']} | Confidence: {item['confidence']}")
        print(f"      {item['summary']}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--radius_km", default="5")
    parser.add_argument("--hours", default="12")
    args = parser.parse_args()
    fetch_sigint(args.id, args.radius_km, args.hours)
