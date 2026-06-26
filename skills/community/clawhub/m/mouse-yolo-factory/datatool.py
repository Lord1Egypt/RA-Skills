import argparse
from DatasetManager import DatasetManager

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--new_data", type=str, required=True)
    parser.add_argument("--yolo_db", type=str, required=True)
    parser.add_argument("--desc", type=str, default="Auto merge")
    args = parser.parse_args()

    dm = DatasetManager()
    dm.merge_and_generate(args.new_data, args.yolo_db, args.desc)