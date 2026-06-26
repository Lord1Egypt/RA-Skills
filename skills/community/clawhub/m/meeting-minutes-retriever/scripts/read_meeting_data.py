import argparse
import os

import requests


REQUEST_TIMEOUT = 20
LOCAL_ENCODINGS = ("utf-8", "utf-8-sig", "cp936", "latin-1")


def read_meeting_data(location: str) -> str:
    """
    Read meeting text from a local path or URL.
    Return the raw text on success, or an error string prefixed with 'ERROR:'.
    """
    if location.startswith(("http://", "https://")):
        try:
            response = requests.get(location, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.text
            if response.status_code == 403:
                return "ERROR: URL access was denied (403 Forbidden). Check permissions."
            if response.status_code == 404:
                return f"ERROR: URL not found (404 Not Found): {location}"
            return f"ERROR: URL fetch failed with status code {response.status_code}"
        except requests.exceptions.Timeout:
            return f"ERROR: Request timed out after {REQUEST_TIMEOUT}s. Check the network or link."
        except Exception as exc:
            return f"ERROR: Network request failed: {exc}"

    try:
        abs_path = os.path.abspath(location)
        if not os.path.exists(abs_path):
            return f"ERROR: Local file does not exist: {abs_path}"
        if not os.path.isfile(abs_path):
            return f"ERROR: Local path is not a file: {abs_path}"

        for encoding in LOCAL_ENCODINGS:
            try:
                with open(abs_path, "r", encoding=encoding) as handle:
                    return handle.read()
            except UnicodeDecodeError:
                continue

        tried = ", ".join(LOCAL_ENCODINGS)
        return f"ERROR: Failed to decode local file with supported encodings: {tried}"
    except PermissionError:
        return f"ERROR: Permission denied when reading local file: {location}"
    except Exception as exc:
        return f"ERROR: Failed to read local file: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Read meeting text from a path or URL.")
    parser.add_argument("location", help="Local file path or URL")
    args = parser.parse_args()
    print(read_meeting_data(args.location))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
