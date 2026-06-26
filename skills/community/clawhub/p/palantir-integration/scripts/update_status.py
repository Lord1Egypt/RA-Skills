import argparse
from mss_client import api_patch


VALID_STATUSES = ["detected", "review", "approved", "engaged", "completed", "rejected"]


def update_status(target_id, new_status):
    status_lower = new_status.lower()
    if status_lower not in VALID_STATUSES:
        print(f"ERROR: Invalid status '{new_status}'. Valid: {', '.join(VALID_STATUSES)}")
        return

    data = api_patch(f"/targets/{target_id}/status", payload={"status": status_lower})
    print(f"Target {target_id}: {data['previous_status']} -> {status_lower}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--status", required=True)
    args = parser.parse_args()
    update_status(args.id, args.status)
