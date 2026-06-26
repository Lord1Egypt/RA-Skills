import argparse
from mss_client import api_get, fmt_json


def fetch_target(target_id):
    data = api_get(f"/targets/{target_id}")
    print(fmt_json(data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    args = parser.parse_args()
    fetch_target(args.id)
