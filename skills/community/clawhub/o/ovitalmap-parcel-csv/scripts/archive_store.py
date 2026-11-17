"""Low-level storage for the country and master parcel archives."""

import os
import shutil
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

from utils import read_csv, validate_country_code, write_csv

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows fallback
    fcntl = None


COUNTRY_HEADERS = [
    "parcel_code", "provider_name", "archive_date",
    "boundary_coords", "provider_notes", "cadastre_code",
]
MASTER_HEADERS = [
    "CC", "parcel_code", "provider_name", "archive_date",
    "boundary_coords", "provider_notes", "cadastre_code",
]


class ArchiveStore:
    """Own paths, schemas, locking, backups, and atomic two-file commits."""

    def __init__(self, workspace_root):
        self.workspace_root = Path(workspace_root).resolve()
        self.archive_dir = self.workspace_root / "ovitalmap_archive"
        self.backup_dir = self.workspace_root / "ovitalmap_backups"

    def country_path(self, country_code):
        code = validate_country_code(country_code)
        return self.archive_dir / f"{code}_parcels.csv"

    @property
    def master_path(self):
        return self.archive_dir / "master.csv"

    @contextmanager
    def locked(self):
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        with (self.archive_dir / ".archive.lock").open("a+") as handle:
            if fcntl:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                if fcntl:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def read_country(self, country_code):
        return self._read(self.country_path(country_code), COUNTRY_HEADERS)

    def read_master(self):
        return self._read(self.master_path, MASTER_HEADERS)

    def commit(self, country_code, country_rows, master_rows):
        country_path = self.country_path(country_code)
        staged_country = self._stage(country_path, COUNTRY_HEADERS, country_rows)
        staged_master = self._stage(self.master_path, MASTER_HEADERS, master_rows)
        originals = {
            country_path: country_path.read_bytes() if country_path.exists() else None,
            self.master_path: (
                self.master_path.read_bytes() if self.master_path.exists() else None
            ),
        }
        try:
            os.replace(staged_country, country_path)
            os.replace(staged_master, self.master_path)
        except Exception:
            for path, content in originals.items():
                self._restore(path, content)
            raise
        finally:
            for temporary in (staged_country, staged_master):
                if temporary.exists():
                    temporary.unlink()

    def backup(self, country_code):
        code = validate_country_code(country_code)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
        paths = []
        for source, filename in (
            (self.country_path(code), f"{code}_parcels_{timestamp}.csv"),
            (self.master_path, f"master_{timestamp}.csv"),
        ):
            if source.exists():
                destination = self.backup_dir / filename
                shutil.copy2(source, destination)
                paths.append(str(destination))
        return {"backup_paths": paths, "timestamp": timestamp}

    @staticmethod
    def _read(path, expected_headers):
        headers, rows = read_csv(str(path))
        if headers is None:
            return list(expected_headers), []
        if headers != expected_headers:
            raise ValueError(f"Unexpected archive headers in {path}")
        return headers, rows

    @staticmethod
    def _stage(path, headers, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(
            prefix=f".{path.name}.",
            dir=path.parent,
        )
        os.close(descriptor)
        write_csv(temporary, headers, rows)
        return Path(temporary)

    @staticmethod
    def _restore(path, content):
        if content is None:
            if path.exists():
                path.unlink()
            return
        descriptor, temporary = tempfile.mkstemp(
            prefix=f".{path.name}.restore.",
            dir=path.parent,
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
        os.replace(temporary, path)
