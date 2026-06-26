import argparse

from generate_meeting_audio import read_text_source


def main() -> int:
    parser = argparse.ArgumentParser(description="Read meeting text from a local path or URL.")
    parser.add_argument("--location", required=True, help="Local file path or URL containing meeting text")
    args = parser.parse_args()

    result = read_text_source(args.location)
    print(result)
    return 0 if not result.startswith("ERROR:") else 1


if __name__ == "__main__":
    raise SystemExit(main())
