import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

LOG_FILE      = Path.home() / ".openclaw" / "logs" / "backup.log"
ENV_FILE_PKG  = Path(__file__).parent / ".env"
ENV_FILE_USER = Path.home() / ".config" / "workspace" / ".env"


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {message}"
    print(entry)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")


def load_env() -> dict:
    def parse_file(path: Path) -> dict:
        if not path.exists():
            return {}
        result = {}
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key, value = key.strip(), value.strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            if key:
                result[key] = value
        return result

    merged = parse_file(ENV_FILE_PKG)
    merged.update(parse_file(ENV_FILE_USER))  # user-level wins on conflict
    return merged


def load_workspaces() -> list:
    prefix = "WORKSPACE_"
    return [
        {"id": key[len(prefix):], "workspace": val}
        for key, val in load_env().items()
        if key.startswith(prefix) and len(key) > len(prefix) and val
    ]


def git(args: list, cwd: str, **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=cwd, capture_output=True, **kwargs)


def backup_workspace(path: str, branch: str, force: bool = False) -> bool:
    log(f"Starting backup for {branch} (path: {path})")

    if not Path(path).is_dir():
        log(f"WARNING: Directory does not exist: {path}")
        return True

    if git(["rev-parse", "--git-dir"], path).returncode != 0:
        log(f"WARNING: Not a git repository: {path}")
        return True

    git(["add", "-A"], path)

    if git(["diff", "--cached", "--quiet"], path).returncode == 0:
        log(f"No changes to commit for {branch}")
        return True

    r = git(["commit", "-m", f"Backup {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"], path, text=True)
    if r.returncode != 0:
        log(f"ERROR: Failed to commit for {branch}: {r.stderr.strip()}")
        return False

    push_args = ["push", "origin", branch] + (["--force"] if force else [])
    r = git(push_args, path, text=True)
    if r.returncode != 0:
        log(f"ERROR: Failed to push {branch}: {r.stderr.strip()}")
        return False

    log(f"Successfully backed up {branch}")
    return True


def cmd_backup(force: bool = False) -> int:
    log("========== Workspace Backup Started ==========")
    if force:
        log("Force push enabled")

    errors = sum(
        0 if backup_workspace(ws["workspace"], ws["id"], force=force) else 1
        for ws in load_workspaces()
    )

    log("========== Workspace Backup Completed ==========")
    return 1 if errors else 0


def cmd_status() -> int:
    print("=== Workspace Backup Status ===\n")

    for ws in load_workspaces():
        branch, path = ws["id"], ws["workspace"]
        print(f"--- {branch} ({path}) ---")
        if not Path(path).is_dir():
            print("Directory does not exist\n")
            continue
        r = git(["status", "--short"], path, text=True)
        print(r.stdout.strip() if r.stdout.strip() else "(clean)")
        print()

    print("=== Last Backup Log ===")
    if LOG_FILE.exists():
        print("\n".join(LOG_FILE.read_text().splitlines()[-20:]))
    else:
        print("No backup log found")

    return 0


def main():
    parser = argparse.ArgumentParser(prog="workspace", description="OpenClaw 工作空间备份工具")
    parser.add_argument("--backup", action="store_true", help="备份所有工作空间（默认行为）")
    parser.add_argument("--status", action="store_true", help="查看各工作空间 git 状态及最近备份日志")
    parser.add_argument("--force", action="store_true", help="强制推送（git push --force），与 --backup 配合使用")
    args = parser.parse_args()

    sys.exit(cmd_status() if args.status else cmd_backup(force=args.force))


if __name__ == "__main__":
    main()
