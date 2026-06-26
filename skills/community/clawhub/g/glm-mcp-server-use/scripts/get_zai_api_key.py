#!/usr/bin/env python3
import argparse
import os

ENV_CANDIDATES = ["Z_AI_API_KEY", "ZAI_API_KEY", "GLM_API_KEY", "ZHIPU_API_KEY"]


def get_key() -> str | None:
    for key_name in ENV_CANDIDATES:
        value = os.getenv(key_name)
        if value:
            return value.strip()
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve Z.AI API key from environment variables")
    parser.add_argument("--masked", action="store_true", help="print masked value")
    args = parser.parse_args()

    key = get_key()
    if not key:
        return 1

    if args.masked:
        if len(key) <= 8:
            print("*" * len(key))
        else:
            print(f"{key[:4]}***{key[-4:]}")
    else:
        print(key)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
