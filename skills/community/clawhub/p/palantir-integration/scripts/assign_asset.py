import argparse
from mss_client import api_post


def assign_asset(target_id, asset_id):
    data = api_post(f"/targets/{target_id}/assign", payload={"asset_id": asset_id})

    print(f"Asset {asset_id} assigned to target {target_id}")
    print(f"  Mission ID: {data['mission_id']}")
    print(f"  Status: {data['status']}")
    print(f"  ETA: {data['eta_minutes']} minutes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--asset", required=True)
    args = parser.parse_args()
    assign_asset(args.id, args.asset)
