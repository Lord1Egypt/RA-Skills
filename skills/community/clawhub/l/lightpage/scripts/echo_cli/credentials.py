import contextlib
import fcntl
import hashlib
import json
import os
import tempfile
import time
from pathlib import Path

from echo_cli.compat import unlink


def legacy_keyring():
    try:
        import keyring
    except ImportError:
        raise RuntimeError("Legacy migration requires the optional keyring package") from None
    return keyring


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def config_dir():
    path = Path(os.getenv("ECHO_CONFIG_DIR", "~/.config/echo")).expanduser()
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.is_symlink():
        raise RuntimeError("Credential directory must not be a symlink")
    path.chmod(0o700)
    return path


def atomic_json(path, value):
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".echo-")
    try:
        with os.fdopen(fd, "w") as output:
            json.dump(value, output, ensure_ascii=False)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def read_config():
    path = config_dir() / "config.json"
    return json.loads(path.read_text()) if path.exists() else {}


def save_config(value):
    atomic_json(config_dir() / "config.json", value)


class CredentialStore:
    def __init__(self, server, backend="file", *, directory=None):
        self.account = digest(server)
        self.backend = backend
        root = Path(directory).expanduser() if directory is not None else config_dir()
        root.mkdir(mode=0o700, parents=True, exist_ok=True)
        if root.is_symlink():
            raise RuntimeError("Credential directory must not be a symlink")
        root.chmod(0o700)
        self.path = root / f"credentials-{self.account}.json"
        self.pending_path = root / f"login-{self.account}.json"
        self.login_lock_path = root / f"login-{self.account}.lock"
        self.lock_path = root / f"credentials-{self.account}.lock"

    @contextlib.contextmanager
    def lock(self, *, login=False):
        lock_path = self.login_lock_path if login else self.lock_path
        if lock_path.is_symlink():
            raise RuntimeError("Credential lock must not be a symlink")
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            deadline = time.monotonic() + 30
            while True:
                try:
                    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise RuntimeError(
                            "Another CLI process is updating credentials; retry"
                        ) from None
                    time.sleep(0.1)
            yield
        finally:
            os.close(fd)

    def preflight(self):
        fd, probe = tempfile.mkstemp(dir=self.path.parent, prefix=".echo-check-")
        os.close(fd)
        os.unlink(probe)

    def pending(self):
        path = self.pending_path
        if not path.exists():
            return None
        if path.is_symlink() or path.stat().st_mode & 0o077:
            raise RuntimeError("Pending login must have mode 0600 and not be a symlink")
        return json.loads(path.read_text())

    def load(self):
        if self.backend == "keyring":
            try:
                value = legacy_keyring().get_password("echo", self.account)
            except Exception:
                raise RuntimeError(
                    "System keyring unavailable. Configure it or explicitly use --credential-store file"
                ) from None
            return json.loads(value) if value else None
        if not self.path.exists():
            return None
        if self.path.is_symlink() or self.path.stat().st_mode & 0o077:
            raise RuntimeError("Credential file must not be a symlink and must have mode 0600")
        return json.loads(self.path.read_text())

    def save(self, value):
        if self.backend == "keyring":
            try:
                legacy_keyring().set_password("echo", self.account, json.dumps(value))
            except Exception:
                raise RuntimeError(
                    "Cannot save to system keyring. Configure it or explicitly use --credential-store file"
                ) from None
        else:
            atomic_json(self.path, value)

    def delete(self):
        unlink(self.pending_path)
        if self.backend == "keyring":
            try:
                if legacy_keyring().get_password("echo", self.account):
                    legacy_keyring().delete_password("echo", self.account)
            except Exception:
                raise RuntimeError("Cannot remove credential from system keyring") from None
        else:
            unlink(self.path)


class PublishJournal:
    """Persist the exact request before sending, independently of access tokens."""

    def __init__(self, server, *, namespace="publish"):
        self.path = config_dir() / f"{namespace}-{digest(server)}"
        self.path.mkdir(mode=0o700, exist_ok=True)
        if self.path.is_symlink():
            raise RuntimeError("Publish journal must not be a symlink")
        self.path.chmod(0o700)

    def stage(self, key, body):
        path = self.path / f"{digest(key)}.json"
        value = {"idempotency_key": key, "body": body}
        # CredentialStore's per-origin lock serializes journal updates between CLI processes.
        if path.is_symlink():
            raise RuntimeError("Publish receipt must not be a symlink")
        if path.exists():
            existing = json.loads(path.read_text())
            if existing["body"] != body:
                raise RuntimeError("Idempotency key is already saved with a different request")
        else:
            atomic_json(path, value)
        return path
