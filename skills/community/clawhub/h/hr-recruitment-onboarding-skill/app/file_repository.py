import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from .exceptions import HRSkillError


class FileRepository:
    def __init__(self, root: Path | None = None) -> None:
        self.root = root.resolve() if root is not None else None

    def set_root(self, root: Path) -> None:
        self.root = root.resolve()

    def read_json(self, path: Path, default: object) -> object:
        path = self._validated_path(path)
        if not path.exists():
            return default
        return json.loads(path.read_text(encoding="utf-8"))

    def write_json_atomic(self, path: Path, data: object) -> None:
        path = self._validated_path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary: Path | None = None
        try:
            with NamedTemporaryFile(
                "w", encoding="utf-8", dir=path.parent, delete=False
            ) as handle:
                temporary = Path(handle.name)
                json.dump(data, handle, ensure_ascii=False, indent=2)
                handle.flush()
                os.fsync(handle.fileno())

            json.loads(temporary.read_text(encoding="utf-8"))
            os.replace(temporary, path)
            temporary = None
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def _validated_path(self, path: Path) -> Path:
        if self.root is None:
            raise HRSkillError(
                "INVALID_PATH",
                "文件仓库必须配置工作区数据目录。",
            )

        resolved_root = self._normalized_resolved_path(self.root)
        resolved_path = self._normalized_resolved_path(path)
        try:
            resolved_path.relative_to(resolved_root)
        except ValueError as error:
            raise HRSkillError(
                "INVALID_PATH",
                "文件路径必须位于工作区数据目录内。",
                {"path": str(path)},
            ) from error
        return resolved_path

    @staticmethod
    def _normalized_resolved_path(path: Path) -> Path:
        resolved = str(path.resolve())
        if os.name == "nt":
            if resolved.startswith("\\\\?\\UNC\\"):
                resolved = f"\\\\{resolved[8:]}"
            elif resolved.startswith("\\\\?\\"):
                resolved = resolved[4:]
        return Path(resolved)
