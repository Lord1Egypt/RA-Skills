import json
import urllib.request
import urllib.error
import ssl
import sys
from pathlib import Path


def load_config():
    """Load GitLab credentials using secure credential manager"""
    try:
        from credential_loader import load_credentials
        host, token = load_credentials(allow_prompt=False)
        return {"host": host, "access_token": token}
    except ImportError:
        # Fallback to legacy method with warning
        print("⚠️  Warning: credential_loader not found, using legacy config")
        config_path = Path(__file__).parent / "config.json"
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)


def fetch_projects(host, token, page=1, per_page=100):
    url = (
        f"{host}/api/v4/projects"
        f"?membership=true&per_page={per_page}&page={page}"
        f"&order_by=updated_at&sort=desc"
    )
    req = urllib.request.Request(url, headers={"PRIVATE-TOKEN": token})
    # Create SSL context that doesn't verify certificates (for internal GitLab instances)
    ssl_context = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ssl_context) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        total_pages = resp.headers.get("x-total-pages", "1")
        return data, int(total_pages)


def main():
    config = load_config()
    host = config["host"].rstrip("/")
    token = config["access_token"]

    if not token or not token.strip() or len(token) < 10:
        print("Error: Invalid access token")
        sys.exit(1)

    all_projects = []
    page = 1
    while True:
        projects, total_pages = fetch_projects(host, token, page=page)
        all_projects.extend(projects)
        if page >= total_pages:
            break
        page += 1

    if not all_projects:
        print("未找到任何仓库")
        return

    print(f"共 {len(all_projects)} 个仓库:\n")
    print(f"{'名称':<40} {'可见性':<10} {'URL'}")
    print("-" * 100)
    for p in all_projects:
        name = p.get("path_with_namespace", p.get("name", "unknown"))
        visibility = p.get("visibility", "unknown")
        web_url = p.get("web_url", "")
        print(f"{name:<40} {visibility:<10} {web_url}")


if __name__ == "__main__":
    main()
