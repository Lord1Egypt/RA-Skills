import argparse
from mss_client import api_get


def check_logistics(base_id):
    data = api_get(f"/logistics/bases/{base_id}")
    base = data["base_info"]
    fuel = data["fuel"]

    print(f"LOGISTICS — {base['name']} ({base_id.upper()})")
    print(f"Region: {base['region']} | Status: {base['operational_status']}")
    print("=" * 40)

    print("\nFUEL:")
    print(f"  JP-8: {fuel['jp8_percent']}% ({fuel['jp8_gallons']} gal)")
    print(f"  Diesel: {fuel['diesel_percent']}% ({fuel['diesel_gallons']} gal)")

    munitions = data.get("munitions", [])
    if munitions:
        print("\nMUNITIONS:")
        for m in munitions:
            print(f"  {m['type']}: {m['count']} units [{m['status']}]")

    resupply = data.get("resupply")
    if resupply:
        print(f"\nRESUPPLY:")
        print(f"  Next delivery: {resupply['eta']}")
        print(f"  Contents: {resupply['contents']}")

    alerts = data.get("alerts", [])
    if alerts:
        print("\nALERTS:")
        for alert in alerts:
            print(f"  WARNING: {alert}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    check_logistics(args.base)
