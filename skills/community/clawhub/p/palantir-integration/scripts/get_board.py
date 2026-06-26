import argparse
from mss_client import api_get


def get_board(filter_str):
    params = {}
    if filter_str and filter_str.lower() != "all":
        params["filter"] = filter_str

    data = api_get("/board", params=params)
    columns = data.get("columns", {})

    if not columns:
        print("Board is empty.")
        return

    total = sum(len(targets) for targets in columns.values())
    print(f"KANBAN BOARD — {total} targets\n")

    for stage, targets in columns.items():
        print(f"=== {stage.upper()} ({len(targets)}) ===")
        for t in targets:
            print(f"  [{t['id']}] {t['type']} | Threat: {t['threat_level']} | Grid: {t['grid']} | Updated: {t['last_updated']}")
        print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", default="all")
    args = parser.parse_args()
    get_board(args.filter)
