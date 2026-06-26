import argparse
import os


def save_env(api_key, endpoint):
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")

    lines = []
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if not line.startswith("MSS_API_KEY=") and not line.startswith("MSS_API_ENDPOINT="):
                    lines.append(line)

    lines.append(f"MSS_API_KEY={api_key}\n")
    lines.append(f"MSS_API_ENDPOINT={endpoint}\n")

    with open(env_path, "w") as f:
        f.writelines(lines)

    print(f"Configuration saved. Endpoint: {endpoint}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True)
    parser.add_argument("--endpoint", default="https://mss.palantir.mil/api/v1")
    args = parser.parse_args()
    save_env(args.key, args.endpoint)
