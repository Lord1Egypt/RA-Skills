#!/usr/bin/env python3
"""
os-update-checker: Check for available OS package updates and fetch changelogs.

Supports apt (Debian/Ubuntu), dnf (Fedora/RHEL), yum (CentOS/RHEL 7),
pacman (Arch), zypper (openSUSE), apk (Alpine), brew (macOS), and npm (global).

Read-only — no packages are installed or modified. subprocess is used with
shell=False exclusively; package names are validated against per-backend
allowlist patterns before use.
"""

import argparse
import json
import re
import shutil
import subprocess
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class PackageUpdate:
    """A single package that has an available upgrade."""

    name: str
    current_version: str
    new_version: str
    source: str
    is_security: bool
    changelog_summary: str = ""


# ---------------------------------------------------------------------------
# Subprocess helper
# ---------------------------------------------------------------------------

_MODERATE_RISK_SUBSTRINGS: tuple[str, ...] = (
    "linux-image",
    "linux-kernel",
    "kernel",
    "openssh",
    "openssl",
    "libc",
    "glibc",
    "sudo",
    "curl",
    "wget",
    "bash",
    "zsh",
    "python",
)


def _run(cmd: list[str], timeout: int = 60) -> str:
    """
    Run cmd with shell=False and return stdout as a string.

    shell=False is required — arguments are passed as a list, never
    interpolated into a shell string, preventing injection. Returns an
    empty string on any error rather than raising.
    """
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,  # explicit: never interpret cmd as a shell string
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return ""
    except FileNotFoundError:
        return ""
    except OSError:
        return ""


def _which(binary: str) -> bool:
    """Return True if `binary` is available on PATH."""
    return shutil.which(binary) is not None


# ---------------------------------------------------------------------------
# Package manager backends
# ---------------------------------------------------------------------------


class Backend(ABC):
    """Abstract base for a package manager backend."""

    # Regex each package name must fully match before use in a command.
    NAME_PATTERN: re.Pattern[str]

    def sanitize(self, name: str) -> str | None:
        """Return name if valid, else None."""
        if self.NAME_PATTERN.fullmatch(name):
            return name
        return None

    @abstractmethod
    def list_upgradable(self) -> list[PackageUpdate]:
        """Return packages that have available upgrades."""

    @abstractmethod
    def fetch_changelog(self, package_name: str) -> str:
        """Return the most recent changelog entry for package_name."""

    def classify_risk(self, pkg: PackageUpdate) -> str:
        """Return a risk label for pkg."""
        if pkg.is_security:
            return "🔴 security"
        name_lower = pkg.name.lower()
        if any(sub in name_lower for sub in _MODERATE_RISK_SUBSTRINGS):
            return "🟡 moderate"
        return "🟢 low"


# ---- apt (Debian / Ubuntu) ------------------------------------------------


class AptBackend(Backend):
    """Backend for apt-based systems (Debian, Ubuntu, Mint, etc.)."""

    NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9.+\-]*")

    def list_upgradable(self) -> list[PackageUpdate]:
        """Parse `apt list --upgradable` into PackageUpdate objects."""
        output = _run(["apt", "list", "--upgradable"])
        packages: list[PackageUpdate] = []

        for line in output.splitlines():
            if line.startswith("Listing") or not line.strip():
                continue
            try:
                parts = line.split()
                if len(parts) < 2:
                    continue
                name_field = parts[0]
                new_version = parts[1]
                name = name_field.split("/")[0]
                source = name_field.split("/")[1] if "/" in name_field else "unknown"
                old_version = ""
                if "upgradable from:" in line:
                    old_version = line.split("upgradable from:")[-1].strip().rstrip("]")
                is_security = "-security" in source
                packages.append(PackageUpdate(
                    name=name,
                    current_version=old_version,
                    new_version=new_version,
                    source=source,
                    is_security=is_security,
                ))
            except (IndexError, ValueError):
                continue

        return packages

    def fetch_changelog(self, package_name: str) -> str:
        """Fetch the most recent apt changelog entry for package_name."""
        safe = self.sanitize(package_name)
        if safe is None:
            return "Skipped: package name failed validation."

        raw = _run(["apt", "changelog", safe], timeout=90)
        if not raw:
            return "No changelog available."

        entry_lines: list[str] = []
        in_entry = False
        for line in raw.splitlines():
            is_header = bool(line) and not line.startswith(" ") and "(" in line
            if not in_entry and is_header:
                in_entry = True
                entry_lines.append(line)
                continue
            if in_entry:
                if is_header:
                    break
                entry_lines.append(line)
                if len(entry_lines) >= 40:
                    break

        summary = "\n".join(entry_lines).strip()
        return summary if summary else "No changelog available."


# ---- dnf (Fedora / RHEL 8+ / Rocky / Alma) --------------------------------


class DnfBackend(Backend):
    """Backend for dnf-based systems (Fedora, RHEL 8+, Rocky, AlmaLinux)."""

    NAME_PATTERN = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._\-]*")

    def list_upgradable(self) -> list[PackageUpdate]:
        """Parse `dnf check-update` output into PackageUpdate objects."""
        # dnf check-update exits 100 when updates are available — that's normal.
        try:
            result = subprocess.run(
                ["dnf", "check-update", "--quiet"],
                capture_output=True,
                text=True,
                timeout=60,
                shell=False,
            )
            output = result.stdout.strip()
        except subprocess.TimeoutExpired:
            return []
        except FileNotFoundError:
            return []
        except OSError:
            return []

        packages: list[PackageUpdate] = []
        for line in output.splitlines():
            line = line.strip()
            if not line or line.startswith("Last metadata") or line.startswith("Obsoleting"):
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            try:
                name_arch = parts[0]
                name = name_arch.split(".")[0]
                new_version = parts[1]
                source = parts[2]
                is_security = "security" in source.lower()
                packages.append(PackageUpdate(
                    name=name,
                    current_version="",
                    new_version=new_version,
                    source=source,
                    is_security=is_security,
                ))
            except (IndexError, ValueError):
                continue

        return packages

    def fetch_changelog(self, package_name: str) -> str:
        """Fetch recent RPM changelog entries for package_name."""
        safe = self.sanitize(package_name)
        if safe is None:
            return "Skipped: package name failed validation."

        raw = _run(["rpm", "-q", "--changelog", safe])
        if not raw:
            return "No changelog available."

        # Return first 20 lines of the RPM changelog
        lines = raw.splitlines()[:20]
        return "\n".join(lines)


# ---- yum (CentOS 7 / RHEL 7) -----------------------------------------------


class YumBackend(Backend):
    """Backend for yum-based systems (CentOS 7, RHEL 7)."""

    NAME_PATTERN = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._\-]*")

    def list_upgradable(self) -> list[PackageUpdate]:
        """Parse `yum check-update` output into PackageUpdate objects."""
        try:
            result = subprocess.run(
                ["yum", "check-update", "--quiet"],
                capture_output=True,
                text=True,
                timeout=60,
                shell=False,
            )
            output = result.stdout.strip()
        except subprocess.TimeoutExpired:
            return []
        except FileNotFoundError:
            return []
        except OSError:
            return []

        packages: list[PackageUpdate] = []
        for line in output.splitlines():
            line = line.strip()
            if not line or line.startswith("Loaded") or line.startswith("*"):
                continue
            parts = line.split()
            if len(parts) < 3:
                continue
            try:
                name_arch = parts[0]
                name = name_arch.split(".")[0]
                new_version = parts[1]
                source = parts[2]
                is_security = "security" in source.lower()
                packages.append(PackageUpdate(
                    name=name,
                    current_version="",
                    new_version=new_version,
                    source=source,
                    is_security=is_security,
                ))
            except (IndexError, ValueError):
                continue

        return packages

    def fetch_changelog(self, package_name: str) -> str:
        """Fetch recent RPM changelog entries for package_name."""
        safe = self.sanitize(package_name)
        if safe is None:
            return "Skipped: package name failed validation."

        raw = _run(["rpm", "-q", "--changelog", safe])
        if not raw:
            return "No changelog available."

        lines = raw.splitlines()[:20]
        return "\n".join(lines)


# ---- pacman (Arch Linux) ---------------------------------------------------


class PacmanBackend(Backend):
    """Backend for pacman-based systems (Arch Linux, Manjaro, EndeavourOS)."""

    NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9@._+\-]*")

    def list_upgradable(self) -> list[PackageUpdate]:
        """Parse `checkupdates` output into PackageUpdate objects."""
        # checkupdates is from pacman-contrib; fall back to pacman -Qu
        output = _run(["checkupdates"]) or _run(["pacman", "-Qu"])
        packages: list[PackageUpdate] = []

        for line in output.splitlines():
            # checkupdates: "name old_ver -> new_ver"
            # pacman -Qu:   "name old_ver -> new_ver"
            parts = line.split()
            if len(parts) < 4:
                continue
            try:
                name = parts[0]
                old_version = parts[1]
                new_version = parts[3]
                packages.append(PackageUpdate(
                    name=name,
                    current_version=old_version,
                    new_version=new_version,
                    source="arch",
                    is_security=False,
                ))
            except (IndexError, ValueError):
                continue

        return packages

    def fetch_changelog(self, package_name: str) -> str:
        """Return package info from pacman as a changelog substitute."""
        safe = self.sanitize(package_name)
        if safe is None:
            return "Skipped: package name failed validation."

        raw = _run(["pacman", "-Si", safe])
        if not raw:
            return "No package info available."

        # Extract the most relevant lines
        keep = ("Version", "Description", "URL", "Build Date", "Packager")
        lines = [
            line for line in raw.splitlines()
            if any(line.startswith(k) for k in keep)
        ]
        return "\n".join(lines) if lines else "No info available."


# ---- zypper (openSUSE) -----------------------------------------------------


class ZypperBackend(Backend):
    """Backend for zypper-based systems (openSUSE Leap, Tumbleweed, SLES)."""

    NAME_PATTERN = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9._\-]*")

    def list_upgradable(self) -> list[PackageUpdate]:
        """Parse `zypper list-updates` XML-like output into PackageUpdate objects."""
        output = _run(["zypper", "--non-interactive", "list-updates"])
        packages: list[PackageUpdate] = []

        for line in output.splitlines():
            # Table format: "| name | old | new | arch | repo |"
            if not line.startswith("|") or "Name" in line or "---" in line:
                continue
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 4:
                continue
            try:
                name = parts[0]
                old_version = parts[1]
                new_version = parts[2]
                source = parts[4] if len(parts) > 4 else "unknown"
                is_security = "security" in source.lower()
                packages.append(PackageUpdate(
                    name=name,
                    current_version=old_version,
                    new_version=new_version,
                    source=source,
                    is_security=is_security,
                ))
            except (IndexError, ValueError):
                continue

        return packages

    def fetch_changelog(self, package_name: str) -> str:
        """Return zypper package info as a changelog substitute."""
        safe = self.sanitize(package_name)
        if safe is None:
            return "Skipped: package name failed validation."

        raw = _run(["zypper", "info", safe])
        if not raw:
            return "No package info available."

        lines = raw.splitlines()[:20]
        return "\n".join(lines)


# ---- apk (Alpine Linux) ----------------------------------------------------


class ApkBackend(Backend):
    """Backend for apk-based systems (Alpine Linux)."""

    NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9._\-]*")

    def list_upgradable(self) -> list[PackageUpdate]:
        """Parse `apk list --upgradable` output into PackageUpdate objects."""
        output = _run(["apk", "list", "--upgradable"])
        packages: list[PackageUpdate] = []

        for line in output.splitlines():
            # Format: "name-version-rN [repo] {origin} (license) [upgradable from: old]"
            if not line.strip():
                continue
            try:
                first = line.split()[0]
                # Alpine names are "name-version-release"; split on last two dashes
                parts_dash = first.rsplit("-", 2)
                name = parts_dash[0] if len(parts_dash) >= 3 else first
                new_version = "-".join(parts_dash[1:]) if len(parts_dash) >= 3 else ""
                old_version = ""
                if "upgradable from:" in line:
                    old_version = line.split("upgradable from:")[-1].strip().rstrip("]")
                packages.append(PackageUpdate(
                    name=name,
                    current_version=old_version,
                    new_version=new_version,
                    source="alpine",
                    is_security=False,
                ))
            except (IndexError, ValueError):
                continue

        return packages

    def fetch_changelog(self, package_name: str) -> str:
        """Return apk package info as a changelog substitute."""
        safe = self.sanitize(package_name)
        if safe is None:
            return "Skipped: package name failed validation."

        raw = _run(["apk", "info", "-a", safe])
        if not raw:
            return "No package info available."

        lines = raw.splitlines()[:15]
        return "\n".join(lines)


# ---- brew (macOS / Linux Homebrew) ----------------------------------------


class BrewBackend(Backend):
    """Backend for Homebrew (macOS and Linux)."""

    NAME_PATTERN = re.compile(r"[a-z0-9][a-z0-9._@+\-]*")

    def list_upgradable(self) -> list[PackageUpdate]:
        """Parse `brew outdated --verbose` output into PackageUpdate objects."""
        output = _run(["brew", "outdated", "--verbose"])
        packages: list[PackageUpdate] = []

        for line in output.splitlines():
            if not line.strip():
                continue
            # Format: "name (old) < new"  or  "name old -> new"
            try:
                if " < " in line:
                    name_part, new_version = line.split(" < ", 1)
                    name = name_part.split("(")[0].strip()
                    old_part = name_part.split("(")[-1].rstrip(")")
                    old_version = old_part.strip() if "(" in name_part else ""
                elif " -> " in line:
                    parts = line.split()
                    name = parts[0]
                    old_version = parts[1] if len(parts) > 1 else ""
                    new_version = parts[3] if len(parts) > 3 else ""
                else:
                    parts = line.split()
                    name = parts[0]
                    old_version = parts[1] if len(parts) > 1 else ""
                    new_version = parts[-1] if len(parts) > 1 else ""

                packages.append(PackageUpdate(
                    name=name.strip(),
                    current_version=old_version.strip(),
                    new_version=new_version.strip(),
                    source="homebrew",
                    is_security=False,
                ))
            except (IndexError, ValueError):
                continue

        return packages

    def fetch_changelog(self, package_name: str) -> str:
        """Return brew info output as a changelog substitute."""
        safe = self.sanitize(package_name)
        if safe is None:
            return "Skipped: package name failed validation."

        raw = _run(["brew", "info", safe])
        if not raw:
            return "No package info available."

        lines = raw.splitlines()[:15]
        return "\n".join(lines)


# ---- npm (global packages) ------------------------------------------------


class NpmBackend(Backend):
    """Backend for npm global packages (`npm outdated -g`)."""

    NAME_PATTERN = re.compile(r"[a-zA-Z0-9]([a-zA-Z0-9._\-]*[a-zA-Z0-9])?|@[a-zA-Z0-9\-]+/[a-zA-Z0-9._\-]+")

    def list_upgradable(self) -> list[PackageUpdate]:
        """Parse `npm outdated -g --json` into PackageUpdate objects."""
        raw = _run(["npm", "outdated", "-g", "--json"], timeout=60)
        if not raw:
            return []

        try:
            data: dict = json.loads(raw)
        except ValueError:
            return []

        packages: list[PackageUpdate] = []
        for name, info in data.items():
            if not isinstance(info, dict):
                continue
            try:
                current = info.get("current", "")
                wanted = info.get("wanted", "")
                latest = info.get("latest", "")
                # Use latest if it's ahead of wanted, otherwise wanted
                new_version = latest if latest and latest != current else wanted
                if not new_version or new_version == current:
                    continue
                packages.append(PackageUpdate(
                    name=name,
                    current_version=current,
                    new_version=new_version,
                    source="npm",
                    is_security=False,
                ))
            except (KeyError, TypeError):
                continue

        return packages

    def fetch_changelog(self, package_name: str) -> str:
        """Fetch package metadata from the npm registry as a changelog substitute."""
        safe = self.sanitize(package_name)
        if safe is None:
            return "Skipped: package name failed validation."

        # URL-encode scoped packages (@scope/name → %40scope%2Fname)
        encoded = safe.replace("@", "%40").replace("/", "%2F")
        url = f"https://registry.npmjs.org/{encoded}/latest"

        try:
            req = urllib.request.Request(url, headers={"Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                meta: dict = json.loads(resp.read().decode())
        except (urllib.error.URLError, OSError, ValueError):
            return "No changelog available (registry unreachable)."

        lines: list[str] = []
        version = meta.get("version", "")
        description = meta.get("description", "")
        homepage = meta.get("homepage", "")

        if version:
            lines.append(f"Latest version: {version}")
        if description:
            lines.append(f"Description: {description}")
        if homepage:
            lines.append(f"Homepage: {homepage}")

        # Pull changelog/release notes URL if present in the dist-tags or repository
        repo = meta.get("repository", {})
        if isinstance(repo, dict):
            repo_url = repo.get("url", "")
            if repo_url:
                lines.append(f"Repository: {repo_url}")

        return "\n".join(lines) if lines else "No metadata available."

    def classify_risk(self, pkg: PackageUpdate) -> str:
        """npm global packages are all low risk by default (no OS-level security advisories)."""
        name_lower = pkg.name.lower()
        if any(sub in name_lower for sub in _MODERATE_RISK_SUBSTRINGS):
            return "🟡 moderate"
        return "🟢 low"


# ---------------------------------------------------------------------------
# Detection
# ---------------------------------------------------------------------------


def detect_backends() -> list[Backend]:
    """
    Auto-detect all available package managers and return matching backends.

    npm is always checked independently alongside the OS package manager, since
    a system may have both apt and npm installed simultaneously.
    Returns an empty list if no supported package manager is found.
    """
    backends: list[Backend] = []

    # OS package managers (mutually exclusive — pick first match)
    if _which("apt"):
        backends.append(AptBackend())
    elif _which("dnf"):
        backends.append(DnfBackend())
    elif _which("yum"):
        backends.append(YumBackend())
    elif _which("pacman"):
        backends.append(PacmanBackend())
    elif _which("zypper"):
        backends.append(ZypperBackend())
    elif _which("apk"):
        backends.append(ApkBackend())
    elif _which("brew"):
        backends.append(BrewBackend())

    # npm global packages — always check independently if available
    if _which("npm"):
        backends.append(NpmBackend())

    return backends


def detect_backend() -> Backend | None:
    """
    Legacy single-backend detection. Returns the first OS backend found, or
    NpmBackend if only npm is available. Use detect_backends() for full coverage.
    """
    backends = detect_backends()
    return backends[0] if backends else None


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------


def format_text(packages: list[PackageUpdate], backend: Backend) -> str:
    """Format the package list as a human-readable text report."""
    if not packages:
        return "✅ System is up to date — no packages to upgrade."

    security_count = sum(1 for p in packages if p.is_security)
    header = f"📦 {len(packages)} package(s) upgradable"
    if security_count:
        header += f" — ⚠️ {security_count} security update(s)"

    lines: list[str] = [header, ""]

    for pkg in packages:
        risk = backend.classify_risk(pkg)
        lines.append(f"**{pkg.name}** {pkg.current_version} → {pkg.new_version}")
        lines.append(f"  Source: {pkg.source}  |  Risk: {risk}")
        if pkg.changelog_summary:
            lines.append("  Changelog:")
            for cl_line in pkg.changelog_summary.splitlines()[:12]:
                lines.append(f"    {cl_line}")
        lines.append("")

    return "\n".join(lines)


def format_json(packages: list[PackageUpdate], backend: Backend) -> str:
    """Format the package list as a JSON string."""
    data: dict = {
        "total": len(packages),
        "security_count": sum(1 for p in packages if p.is_security),
        "packages": [
            {
                "name": p.name,
                "current_version": p.current_version,
                "new_version": p.new_version,
                "source": p.source,
                "is_security": p.is_security,
                "risk": backend.classify_risk(p),
                "changelog_summary": p.changelog_summary,
            }
            for p in packages
        ],
    }
    return json.dumps(data, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    """Parse arguments, detect package manager, fetch updates, print report."""
    parser = argparse.ArgumentParser(
        description=(
            "Check for OS/npm package updates with per-package changelog summaries. "
            "Supports apt, dnf, yum, pacman, zypper, apk, brew, and npm (global)."
        ),
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--no-changelog",
        action="store_true",
        help="Skip fetching changelogs for faster output",
    )
    args = parser.parse_args()

    backends = detect_backends()
    if not backends:
        print("❌ No supported package manager found (apt/dnf/yum/pacman/zypper/apk/brew/npm).")
        return

    all_packages: list[tuple[PackageUpdate, Backend]] = []
    for backend in backends:
        pkgs = backend.list_upgradable()
        for pkg in pkgs:
            if not args.no_changelog:
                pkg.changelog_summary = backend.fetch_changelog(pkg.name)
            all_packages.append((pkg, backend))

    if args.format == "json":
        # Merge all backends into a single JSON structure
        merged_packages = [p for p, _ in all_packages]
        # Use first backend for classify_risk fallback; each pkg carries its own source
        primary_backend = backends[0]
        # Build JSON manually to preserve per-backend risk classification
        data: dict = {
            "total": len(merged_packages),
            "security_count": sum(1 for p in merged_packages if p.is_security),
            "packages": [
                {
                    "name": p.name,
                    "current_version": p.current_version,
                    "new_version": p.new_version,
                    "source": p.source,
                    "is_security": p.is_security,
                    "risk": b.classify_risk(p),
                    "changelog_summary": p.changelog_summary,
                }
                for p, b in all_packages
            ],
        }
        print(json.dumps(data, indent=2))
    else:
        if not all_packages:
            print("✅ System is up to date — no packages to upgrade.")
            return
        security_count = sum(1 for p, _ in all_packages if p.is_security)
        header = f"📦 {len(all_packages)} package(s) upgradable"
        if security_count:
            header += f" — ⚠️ {security_count} security update(s)"
        lines: list[str] = [header, ""]
        for pkg, backend in all_packages:
            risk = backend.classify_risk(pkg)
            lines.append(f"**{pkg.name}** {pkg.current_version} → {pkg.new_version}")
            lines.append(f"  Source: {pkg.source}  |  Risk: {risk}")
            if pkg.changelog_summary:
                for cl_line in pkg.changelog_summary.splitlines()[:12]:
                    lines.append(f"    {cl_line}")
            lines.append("")
        print("\n".join(lines))


if __name__ == "__main__":
    main()
