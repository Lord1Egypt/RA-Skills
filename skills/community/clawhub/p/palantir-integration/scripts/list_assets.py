import argparse
from mss_client import api_get


def list_assets(region):
    data = api_get("/assets", params={"region": region, "status": "available"})
    assets = data.get("assets", [])

    if not assets:
        print(f"No available assets in region: {region}")
        return

    print(f"AVAILABLE ASSETS — Region {region.upper()} — Total: {len(assets)}\n")

    for a in assets:
        munitions = a.get("munitions", [])
        mun_str = ", ".join(f"{m['type']}x{m['count']}" for m in munitions)

        print(f"  [{a['id']}] {a['platform']} ({a['type']})")
        print(f"    Location: {a['location']} | Readiness: {a['readiness']}")
        print(f"    Fuel: {a['fuel_percent']}% | Avg ETA: {a['avg_eta_minutes']} min")
        print(f"    Munitions: {mun_str}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", required=True)
    args = parser.parse_args()
    list_assets(args.region)
