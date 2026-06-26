import argparse
from mss_client import api_get


def generate_bda(target_id):
    data = api_get(f"/targets/{target_id}/bda")

    strike = data["strike_details"]
    damage = data["damage_assessment"]
    collateral = data["collateral_assessment"]
    restrike = data["restrike_recommendation"]

    print(f"BATTLE DAMAGE ASSESSMENT — Target {target_id}")
    print("=" * 40)

    print("\nSTRIKE DETAILS:")
    print(f"  Timestamp: {strike['timestamp']}")
    print(f"  Weapon: {strike['weapon']}")
    print(f"  Asset: {strike['asset_id']}")
    print(f"  Impact Coordinates: {strike['impact_coords']}")

    print("\nDAMAGE ASSESSMENT:")
    print(f"  Classification: {damage['classification']}")
    print(f"  Destruction: {damage['destruction_percent']}%")
    print(f"  Functional Kill: {damage['functional_kill']}")
    print(f"  Secondary Explosions: {damage['secondary_explosions']}")
    print(f"  Fires: {damage['fires_observed']}")

    print("\nCOLLATERAL ASSESSMENT:")
    print(f"  Civilian Damage: {collateral['civilian_damage']}")
    print(f"  Infrastructure Impact: {collateral['infrastructure_impact']}")

    print("\nRECOMMENDATION:")
    print(f"  Restrike Needed: {restrike['needed']}")
    print(f"  Reason: {restrike['reason']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    generate_bda(args.id)
