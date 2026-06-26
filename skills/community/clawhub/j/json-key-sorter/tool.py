import argparse
import json
import sys

def sort_json_keys(input_stream, output_stream):
    """Reads JSON from input_stream, sorts its keys, and writes to output_stream."""
    try:
        data = json.load(input_stream)
        # Use json.dumps with sort_keys=True and indent for readability
        sorted_json_str = json.dumps(data, sort_keys=True, indent=2)
        output_stream.write(sorted_json_str + '\n')
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error: Invalid JSON input: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred: {e}\n")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Sorts JSON keys alphabetically in a file or from stdin."
    )
    parser.add_argument(
        "input_file",
        nargs="?",  # Optional positional argument
        type=argparse.FileType("r", encoding="utf-8"),
        default=sys.stdin,
        help="Input JSON file. Reads from stdin if not specified."
    )
    parser.add_argument(
        "-o", "--output",
        type=argparse.FileType("w", encoding="utf-8"),
        default=sys.stdout,
        help="Output file for sorted JSON. Writes to stdout if not specified."
    )

    args = parser.parse_args()

    sort_json_keys(args.input_file, args.output)

    # Close files if they are not stdin/stdout
    if args.input_file is not sys.stdin:
        args.input_file.close()
    if args.output is not sys.stdout:
        args.output.close()

if __name__ == "__main__":
    main()
