"""Build and test the downstream wheel without editable/source-path imports."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
import venv
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--find-links", type=Path, help="Optional dependency wheelhouse")
    args = parser.parse_args()
    project = Path(__file__).resolve().parents[1]
    environment = {
        key: value
        for key, value in os.environ.items()
        if key.upper() not in {"PYTHONPATH", "PYTHONHOME"}
    }
    with tempfile.TemporaryDirectory(prefix="glr-wheel-check-") as directory:
        work = Path(directory).resolve()
        distributions = work / "dist"
        subprocess.run(
            [
                sys.executable,
                "-I",
                "-m",
                "build",
                "--wheel",
                "--no-isolation",
                "--outdir",
                str(distributions),
                str(project),
            ],
            cwd=work,
            env=environment,
            check=True,
        )
        wheels = list(distributions.glob("*.whl"))
        if len(wheels) != 1:
            raise RuntimeError("Expected exactly one newly built wheel")
        target = work / "venv"
        venv.EnvBuilder(with_pip=True).create(target)
        python = target / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        install = [str(python), "-I", "-m", "pip", "--isolated", "install"]
        if args.find_links is not None:
            install.extend(["--find-links", str(args.find_links.resolve())])
        subprocess.run(
            [*install, str(wheels[0]), "pytest>=8.3"],
            cwd=work,
            env=environment,
            check=True,
        )
        subprocess.run(
            [str(python), "-I", "-m", "pip", "--isolated", "check"],
            cwd=work,
            env=environment,
            check=True,
        )
        subprocess.run(
            [
                str(python),
                "-I",
                "-c",
                (
                    "import sys; from pathlib import Path; import @@PACKAGE@@ as package; "
                    "assert Path(package.__file__).resolve().is_relative_to(Path(sys.prefix)), "
                    "'Package was not loaded from the clean installation'"
                ),
            ],
            cwd=work,
            env=environment,
            check=True,
        )
        subprocess.run(
            [
                str(python),
                "-I",
                "-m",
                "pytest",
                "--import-mode=importlib",
                "-c",
                str(project / "pyproject.toml"),
                str(project / "tests"),
            ],
            cwd=work,
            env=environment,
            check=True,
        )


if __name__ == "__main__":
    main()
