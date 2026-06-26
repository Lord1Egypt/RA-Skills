import argparse
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import TypedDict


BASE_DIR = Path(__file__).resolve().parent
CATALOG_PATH = BASE_DIR / "catalog.json"
DEFAULT_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
SOURCE_PRIORITY = [
    "flatpak",
    "snap",
    "apt",
    "dnf",
    "zypper",
    "pacman",
    "aur",
    "nix",
    "appimage",
    "manual",
    "wine",
]


class Capabilities(TypedDict):
    flatpak: bool
    snap: bool
    apt: bool
    dnf: bool
    zypper: bool
    pacman: bool
    yay: bool
    paru: bool
    nix: bool
    wine: bool
    winetricks: bool
    native_manager: str | None
    aur_helper: str | None
    aur: bool


def load_catalog():
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_settings(config_path=None):
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError:
        return {"unsafe_community_installs": False}

    skill_settings = data.get("skills", {}).get("entries", {}).get("linux-installer", {})
    return {
        "unsafe_community_installs": bool(
            skill_settings.get("unsafeCommunityInstalls", False)
        )
    }


def normalize_name(value):
    return re.sub(r"[^a-z0-9]+", "", value.lower()).strip()


def tokenize(value):
    return [token for token in re.split(r"[^a-z0-9]+", value.lower()) if token]


def shell_join(parts):
    return " ".join(shlex.quote(expand_env(part)) for part in parts)


def expand_env(value):
    return os.path.expandvars(value)


def run_command(parts):
    return subprocess.run(parts, capture_output=True, text=True, check=False)


def guess_launch_binaries(package):
    guesses = []
    for candidate in [
        package,
        re.sub(r"-(bin|git|appimage)$", "", package),
    ]:
        cleaned = candidate.strip()
        if cleaned and cleaned not in guesses:
            guesses.append(cleaned)
    return guesses


def infer_launch_steps(candidate):
    explicit_launch = candidate.get("launch")
    if explicit_launch:
        return explicit_launch, True

    if candidate["source"] not in {"apt", "dnf", "zypper", "pacman", "aur", "nix"}:
        return None, False

    guesses = guess_launch_binaries(candidate["package"])
    for guess in guesses:
        if shutil.which(expand_env(guess)):
            return [guess], True

    if guesses:
        return [guesses[0]], False
    return None, False


def resolve_aur_install_steps(candidate, capabilities):
    if candidate["source"] != "aur":
        return candidate.get("install", [])

    helper = capabilities.get("aur_helper")
    package = candidate["package"]
    if helper:
        return [[helper, "-S", "--noconfirm", package]]
    return candidate.get("install", [])


def infer_source_url(source, package):
    if source == "flatpak":
        return f"https://flathub.org/apps/{package}"
    if source == "snap":
        return f"https://snapcraft.io/{package}"
    if source == "aur":
        return f"https://aur.archlinux.org/packages/{package}"
    return None


def detect_capabilities():
    capabilities: Capabilities = {
        "flatpak": shutil.which("flatpak") is not None,
        "snap": shutil.which("snap") is not None,
        "apt": shutil.which("apt-get") is not None,
        "dnf": shutil.which("dnf") is not None,
        "zypper": shutil.which("zypper") is not None,
        "pacman": shutil.which("pacman") is not None,
        "yay": shutil.which("yay") is not None,
        "paru": shutil.which("paru") is not None,
        "nix": shutil.which("nix") is not None,
        "wine": shutil.which("wine") is not None,
        "winetricks": shutil.which("winetricks") is not None,
        "native_manager": None,
        "aur_helper": None,
        "aur": False,
    }
    capabilities["native_manager"] = next(
        (name for name in ["apt", "dnf", "zypper", "pacman"] if capabilities[name]),
        None,
    )
    capabilities["aur_helper"] = next(
        (name for name in ["yay", "paru"] if capabilities[name]),
        None,
    )
    capabilities["aur"] = capabilities["aur_helper"] is not None
    return capabilities


def get_missing_tools(candidate, capabilities):
    source = candidate["source"]
    missing = []
    if source == "flatpak" and not capabilities["flatpak"]:
        missing.append("flatpak")
    elif source == "snap" and not capabilities["snap"]:
        missing.append("snapd")
    elif source in {"apt", "dnf", "zypper", "pacman", "nix"} and not capabilities.get(source, False):
        missing.append(source)
    elif source == "aur" and not capabilities.get("aur", False):
        missing.append("aur-helper")
    elif source == "wine":
        if not capabilities["wine"]:
            missing.append("wine")
        if not capabilities["winetricks"]:
            missing.append("winetricks")
    return missing


def build_tooling_steps(candidate, capabilities):
    native_manager = capabilities.get("native_manager")
    source = candidate["source"]
    if not native_manager:
        return []

    if source == "flatpak" and not capabilities["flatpak"]:
        if native_manager == "apt":
            return [
                ["sudo", "apt-get", "update"],
                ["sudo", "apt-get", "install", "-y", "flatpak"],
                [
                    "flatpak",
                    "remote-add",
                    "--if-not-exists",
                    "flathub",
                    "https://flathub.org/repo/flathub.flatpakrepo",
                ],
            ]
        if native_manager == "dnf":
            return [
                ["sudo", "dnf", "install", "-y", "flatpak"],
                [
                    "flatpak",
                    "remote-add",
                    "--if-not-exists",
                    "flathub",
                    "https://flathub.org/repo/flathub.flatpakrepo",
                ],
            ]
        if native_manager == "pacman":
            return [
                ["sudo", "pacman", "-S", "--noconfirm", "flatpak"],
                [
                    "flatpak",
                    "remote-add",
                    "--if-not-exists",
                    "flathub",
                    "https://flathub.org/repo/flathub.flatpakrepo",
                ],
            ]
        if native_manager == "zypper":
            return [
                ["sudo", "zypper", "install", "-y", "flatpak"],
                [
                    "flatpak",
                    "remote-add",
                    "--if-not-exists",
                    "flathub",
                    "https://flathub.org/repo/flathub.flatpakrepo",
                ],
            ]

    if source == "snap" and not capabilities["snap"]:
        if native_manager == "apt":
            return [
                ["sudo", "apt-get", "update"],
                ["sudo", "apt-get", "install", "-y", "snapd"],
                ["sudo", "systemctl", "enable", "--now", "snapd.socket"],
            ]
        if native_manager == "dnf":
            return [
                ["sudo", "dnf", "install", "-y", "snapd"],
                ["sudo", "systemctl", "enable", "--now", "snapd.socket"],
                ["sudo", "ln", "-sf", "/var/lib/snapd/snap", "/snap"],
            ]
        if native_manager == "pacman":
            helper = capabilities.get("aur_helper")
            if not helper:
                return []
            return [
                [helper, "-S", "--noconfirm", "snapd"],
                ["sudo", "systemctl", "enable", "--now", "snapd.socket"],
                ["sudo", "ln", "-sf", "/var/lib/snapd/snap", "/snap"],
            ]
        if native_manager == "zypper":
            return [
                ["sudo", "zypper", "install", "-y", "snapd"],
                ["sudo", "systemctl", "enable", "--now", "snapd.socket"],
                ["sudo", "ln", "-sf", "/var/lib/snapd/snap", "/snap"],
            ]

    if source == "wine" and (not capabilities["wine"] or not capabilities["winetricks"]):
        if native_manager == "apt":
            return [
                ["sudo", "apt-get", "update"],
                ["sudo", "apt-get", "install", "-y", "wine", "winetricks"],
            ]
        if native_manager == "dnf":
            return [["sudo", "dnf", "install", "-y", "wine", "winetricks"]]
        if native_manager == "pacman":
            return [["sudo", "pacman", "-S", "--noconfirm", "wine", "winetricks"]]
        if native_manager == "zypper":
            return [["sudo", "zypper", "install", "-y", "wine", "winetricks"]]

    return []


def is_candidate_supported(candidate, capabilities):
    source = candidate["source"]
    if source in {"appimage", "manual"}:
        return True
    if source == "wine":
        return bool(build_tooling_steps(candidate, capabilities)) or (
            capabilities["wine"] and capabilities["winetricks"]
        )
    if source == "aur":
        return capabilities.get("aur", False)
    return capabilities.get(source, False) or bool(build_tooling_steps(candidate, capabilities))


def infer_uninstall_steps(source, package, capabilities):
    if source == "flatpak":
        return [["flatpak", "uninstall", "-y", package]]
    if source == "snap":
        return [["sudo", "snap", "remove", package]]
    if source == "apt":
        return [["sudo", "apt-get", "remove", "-y", package]]
    if source == "dnf":
        return [["sudo", "dnf", "remove", "-y", package]]
    if source == "zypper":
        return [["sudo", "zypper", "remove", "-y", package]]
    if source == "pacman":
        return [["sudo", "pacman", "-Rns", "--noconfirm", package]]
    if source == "aur":
        helper = capabilities.get("aur_helper")
        if helper:
            return [[helper, "-Rns", "--noconfirm", package]]
        return []
    if source == "nix":
        return [["nix", "profile", "remove", package]]
    return []


def candidate_to_result(candidate, app_key, display_name, capabilities):
    warnings = list(candidate.get("warnings", []))
    missing_tools = get_missing_tools(candidate, capabilities)
    tooling_steps = build_tooling_steps(candidate, capabilities)
    source = candidate["source"]
    is_community = bool(candidate.get("community", False))
    is_unreviewed = bool(candidate.get("unreviewed", False))
    launch_steps, launch_verified = infer_launch_steps(candidate)
    install_steps = resolve_aur_install_steps(candidate, capabilities)
    uninstall_steps = candidate.get(
        "uninstall",
        infer_uninstall_steps(source, candidate["package"], capabilities),
    )
    if missing_tools and tooling_steps:
        warnings = [
            f"Missing tooling for {source}: {', '.join(missing_tools)}. The helper can install it first."
        ] + warnings
    if is_community:
        warnings = [
            "This recommendation is a curated community workaround and needs an extra confirmation."
        ] + warnings
    if is_unreviewed:
        warnings = [
            "This is an unreviewed community suggestion discovered dynamically. Treat it as research, not trusted install metadata."
        ] + warnings
    if launch_steps and not launch_verified:
        warnings = [
            "Launch command is an unverified guess based on the package name. It should be tested after install."
        ] + warnings
    return {
        "app_key": app_key,
        "display_name": display_name,
        "source": source,
        "package": candidate["package"],
        "community": is_community,
        "unreviewed": is_unreviewed,
        "community_label": candidate.get("community_label"),
        "upstream_name": candidate.get("upstream_name"),
        "requires_additional_confirmation": is_community or is_unreviewed,
        "requires_unsafe_mode": is_unreviewed,
        "missing_tools": missing_tools,
        "tooling_steps": tooling_steps,
        "tooling_command": " && ".join(shell_join(step) for step in tooling_steps),
        "install_steps": install_steps,
        "install_command": " && ".join(shell_join(step) for step in install_steps) or None,
        "launch_command": shell_join(launch_steps) if launch_steps else None,
        "launch_steps": launch_steps or [],
        "launch_verified": launch_verified,
        "uninstall_steps": uninstall_steps,
        "uninstall_command": " && ".join(shell_join(step) for step in uninstall_steps) or None,
        "summary": candidate.get("summary"),
        "source_url": candidate.get("source_url") or infer_source_url(source, candidate["package"]),
        "review_summary": candidate.get("review_summary"),
        "rating": candidate.get("rating"),
        "reason": candidate["reason"],
        "warnings": warnings,
        "manual_steps": candidate.get("manual_steps", []),
        "recipe": candidate.get("recipe"),
    }


def resolve_catalog_app(query, catalog):
    normalized = normalize_name(query)
    aliases = {normalize_name(key): value for key, value in catalog.get("aliases", {}).items()}
    if normalized in aliases:
        key = aliases[normalized]
        return key, catalog["apps"][key]

    for key, app in catalog.get("apps", {}).items():
        if normalized == normalize_name(key):
            return key, app
        if normalized == normalize_name(app.get("display_name", "")):
            return key, app
        for term in app.get("search_terms", []):
            if normalized == normalize_name(term):
                return key, app
    return None, None


def parse_flatpak_search(query):
    result = run_command(["flatpak", "search", "--columns=application,name,description", query])
    if result.returncode != 0:
        return []
    matches = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line or line.lower().startswith("application"):
            continue
        parts = [part.strip() for part in line.split("\t") if part.strip()]
        if len(parts) < 2:
            continue
        app_id = parts[0]
        name = parts[1]
        strong_match = normalize_name(query) in {normalize_name(app_id), normalize_name(name)}
        if strong_match:
            matches.append(
                {
                    "source": "flatpak",
                    "package": app_id,
                    "install": [["flatpak", "install", "-y", "flathub", app_id]],
                    "launch": ["flatpak", "run", app_id],
                    "reason": "Exact Flatpak search match.",
                    "warnings": [],
                    "summary": None,
                    "source_url": f"https://flathub.org/apps/{app_id}",
                    "review_summary": None,
                    "rating": None,
                }
            )
    return matches


def parse_snap_search(query):
    result = run_command(["snap", "find", query])
    if result.returncode != 0:
        return []
    matches = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("Name") or line.startswith("---"):
            continue
        parts = re.split(r"\s{2,}", line.strip())
        if not parts:
            continue
        package = parts[0]
        strong_match = normalize_name(query) == normalize_name(package)
        if strong_match:
            matches.append(
                {
                    "source": "snap",
                    "package": package,
                    "install": [["sudo", "snap", "install", package]],
                    "launch": ["snap", "run", package],
                    "reason": "Exact Snap search match.",
                    "warnings": [],
                    "summary": parts[-1] if len(parts) > 1 else None,
                    "source_url": f"https://snapcraft.io/{package}",
                    "review_summary": None,
                    "rating": None,
                }
            )
    return matches


def parse_apt_search(query):
    result = run_command(["apt-cache", "search", query])
    if result.returncode != 0:
        return []
    matches = []
    for raw_line in result.stdout.splitlines():
        if " - " not in raw_line:
            continue
        package, description = raw_line.split(" - ", 1)
        package = package.strip()
        if normalize_name(query) == normalize_name(package):
            matches.append(
                {
                    "source": "apt",
                    "package": package,
                    "install": [["sudo", "apt-get", "install", "-y", package]],
                    "launch": [package],
                    "reason": "Exact apt package match.",
                    "warnings": [],
                    "summary": description.strip(),
                    "source_url": None,
                    "review_summary": None,
                    "rating": None,
                }
            )
    return matches


def parse_dnf_search(query):
    result = run_command(["dnf", "search", "--quiet", query])
    if result.returncode != 0:
        return []
    matches = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("="):
            continue
        if ":" not in line or "." not in line.split(":", 1)[0]:
            continue
        package_arch, description = line.split(":", 1)
        package = package_arch.strip().rsplit(".", 1)[0]
        if normalize_name(query) == normalize_name(package):
            matches.append(
                {
                    "source": "dnf",
                    "package": package,
                    "install": [["sudo", "dnf", "install", "-y", package]],
                    "launch": [package],
                    "reason": "Exact dnf package match.",
                    "warnings": [],
                    "summary": description.strip(),
                    "source_url": None,
                    "review_summary": None,
                    "rating": None,
                }
            )
    return matches


def parse_pacman_search(query):
    result = run_command(["pacman", "-Ss", query])
    if result.returncode != 0:
        return []
    matches = []
    pending_description = None
    for raw_line in result.stdout.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        stripped = line.strip()
        if "/" in stripped and " " in stripped:
            repo_pkg = stripped.split(" ", 1)[0]
            if "/" not in repo_pkg:
                continue
            package = repo_pkg.split("/", 1)[1]
            pending_description = package
            if normalize_name(query) == normalize_name(package):
                matches.append(
                    {
                    "source": "pacman",
                    "package": package,
                    "install": [["sudo", "pacman", "-S", "--noconfirm", package]],
                    "launch": [package],
                    "reason": "Exact pacman package match.",
                        "warnings": [],
                        "summary": None,
                        "source_url": None,
                        "review_summary": None,
                        "rating": None,
                    }
                )
        elif pending_description and matches:
            matches[-1]["summary"] = stripped
            pending_description = None
    return matches


def parse_zypper_search(query):
    result = run_command(["zypper", "search", "--xmlout", "--match-exact", query])
    if result.returncode != 0:
        return []
    matches = []
    try:
        root = ET.fromstring(result.stdout)
    except ET.ParseError:
        return []

    for solvable in root.findall(".//solvable"):
        if solvable.attrib.get("kind") != "package":
            continue
        package = solvable.attrib.get("name")
        summary = solvable.attrib.get("summary")
        if not package or normalize_name(query) != normalize_name(package):
            continue
        matches.append(
            {
                "source": "zypper",
                "package": package,
                "install": [["sudo", "zypper", "install", "-y", package]],
                "launch": [package],
                "reason": "Exact zypper package match.",
                "warnings": [],
                "summary": summary.strip() if summary else None,
                "source_url": None,
                "review_summary": None,
                "rating": None,
            }
        )
    return matches


def parse_nix_search(query):
    result = run_command(["nix", "search", "--json", "nixpkgs", query])
    if result.returncode != 0:
        return []
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []
    matches = []
    for attribute_path, metadata in payload.items():
        package = attribute_path.rsplit(".", 1)[-1]
        if normalize_name(query) != normalize_name(package):
            continue
        matches.append(
            {
                "source": "nix",
                "package": package,
                "install": [["nix", "profile", "install", f"nixpkgs#{package}"]],
                "launch": [package],
                "reason": "Exact nixpkgs package match.",
                "warnings": [
                    "Nix profile commands manage the user's profile and may differ from system-level NixOS configuration."
                ],
                "summary": metadata.get("description"),
                "source_url": metadata.get("homepage"),
                "review_summary": None,
                "rating": None,
            }
        )
    return matches


def parse_aur_search(query, capabilities):
    helper = capabilities.get("aur_helper")
    if not helper:
        return []
    result = run_command([helper, "-Ss", query])
    if result.returncode != 0:
        return []
    matches = []
    pending_package = None
    for raw_line in result.stdout.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        stripped = line.strip()
        if "/" in stripped and " " in stripped:
            repo_pkg = stripped.split(" ", 1)[0]
            if "/" not in repo_pkg:
                continue
            repo, package = repo_pkg.split("/", 1)
            pending_package = None
            if repo != "aur":
                continue
            if normalize_name(query) == normalize_name(package):
                matches.append(
                    {
                        "source": "aur",
                        "package": package,
                        "install": [[helper, "-S", "--noconfirm", package]],
                        "launch": [package],
                        "reason": f"Exact AUR package match via {helper}.",
                        "warnings": [
                            "AUR packages are community-maintained Arch packages and may prompt for PKGBUILD review."
                        ],
                        "summary": None,
                        "source_url": f"https://aur.archlinux.org/packages/{package}",
                        "review_summary": None,
                        "rating": None,
                    }
                )
                pending_package = package
        elif pending_package and matches and matches[-1]["package"] == pending_package:
            matches[-1]["summary"] = stripped
            pending_package = None
    return matches


def discover_dynamic_candidates(query, capabilities):
    candidates = []
    if capabilities["flatpak"]:
        candidates.extend(parse_flatpak_search(query))
    if capabilities["snap"]:
        candidates.extend(parse_snap_search(query))
    if capabilities["apt"]:
        candidates.extend(parse_apt_search(query))
    if capabilities["dnf"]:
        candidates.extend(parse_dnf_search(query))
    if capabilities["zypper"]:
        candidates.extend(parse_zypper_search(query))
    if capabilities["pacman"]:
        candidates.extend(parse_pacman_search(query))
    if capabilities.get("aur"):
        candidates.extend(parse_aur_search(query, capabilities))
    if capabilities["nix"]:
        candidates.extend(parse_nix_search(query))
    return candidates


def score_unreviewed_match(query, *fields):
    query_tokens = set(tokenize(query))
    if not query_tokens:
        return 0
    combined = " ".join(field for field in fields if field)
    combined_tokens = set(tokenize(combined))
    score = len(query_tokens & combined_tokens)
    normalized_query = normalize_name(query)
    normalized_combined = normalize_name(combined)
    if normalized_query and normalized_query in normalized_combined:
        score += 3
    return score


def discover_unreviewed_flatpak_candidates(query):
    result = run_command(["flatpak", "search", "--columns=application,name,description", query])
    if result.returncode != 0:
        return []
    matches = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.strip()
        if not line or line.lower().startswith("application"):
            continue
        parts = [part.strip() for part in line.split("\t")]
        if len(parts) < 3:
            continue
        app_id, name, description = parts[:3]
        if score_unreviewed_match(query, app_id, name, description) < 2:
            continue
        matches.append(
            {
                "source": "flatpak",
                "package": app_id,
                "install": [["flatpak", "install", "-y", "flathub", app_id]],
                "launch": ["flatpak", "run", app_id],
                "summary": description,
                "source_url": f"https://flathub.org/apps/{app_id}",
                "review_summary": "No independent review summary fetched by the local resolver.",
                "rating": None,
                "reason": "Unreviewed Flatpak suggestion discovered from public package metadata.",
                "warnings": [
                    "Metadata comes from public Flatpak search results and has not been maintainer-reviewed."
                ],
                "unreviewed": True,
                "upstream_name": name or app_id,
            }
        )
    return matches


def discover_unreviewed_snap_candidates(query):
    result = run_command(["snap", "find", query])
    if result.returncode != 0:
        return []
    matches = []
    for raw_line in result.stdout.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("Name") or line.startswith("---"):
            continue
        parts = re.split(r"\s{2,}", line.strip())
        if len(parts) < 4:
            continue
        package = parts[0]
        summary = parts[-1]
        if score_unreviewed_match(query, package, summary) < 2:
            continue
        matches.append(
            {
                "source": "snap",
                "package": package,
                "install": [["sudo", "snap", "install", package]],
                "launch": ["snap", "run", package],
                "summary": summary,
                "source_url": f"https://snapcraft.io/{package}",
                "review_summary": "No independent review summary fetched by the local resolver.",
                "rating": None,
                "reason": "Unreviewed Snap suggestion discovered from public package metadata.",
                "warnings": [
                    "Metadata comes from public Snap search results and has not been maintainer-reviewed."
                ],
                "unreviewed": True,
                "upstream_name": package,
            }
        )
    return matches


def discover_unreviewed_candidates(query, capabilities):
    candidates = []
    if capabilities["flatpak"]:
        candidates.extend(discover_unreviewed_flatpak_candidates(query))
    if capabilities["snap"]:
        candidates.extend(discover_unreviewed_snap_candidates(query))
    return candidates


def sort_candidates(candidates):
    return sorted(candidates, key=lambda item: (SOURCE_PRIORITY.index(item["source"]), item["package"]))


def simplify_candidate(candidate):
    return {
        "source": candidate["source"],
        "package": candidate["package"],
        "community": candidate["community"],
        "unreviewed": candidate["unreviewed"],
        "community_label": candidate["community_label"],
        "upstream_name": candidate["upstream_name"],
        "requires_additional_confirmation": candidate["requires_additional_confirmation"],
        "requires_unsafe_mode": candidate["requires_unsafe_mode"],
        "missing_tools": candidate["missing_tools"],
        "tooling_command": candidate["tooling_command"],
        "install_command": candidate["install_command"],
        "launch_command": candidate["launch_command"],
        "launch_verified": candidate["launch_verified"],
        "uninstall_command": candidate["uninstall_command"],
        "summary": candidate["summary"],
        "source_url": candidate["source_url"],
        "review_summary": candidate["review_summary"],
        "rating": candidate["rating"],
        "reason": candidate["reason"],
        "warnings": candidate["warnings"],
        "manual_steps": candidate["manual_steps"],
        "recipe": candidate["recipe"],
    }


def build_resolution(query, config_path=None):
    catalog = load_catalog()
    capabilities = detect_capabilities()
    settings = load_settings(config_path)
    warnings = []

    app_key, catalog_app = resolve_catalog_app(query, catalog)
    candidates = []
    if catalog_app:
        for candidate in catalog_app.get("candidates", []):
            if is_candidate_supported(candidate, capabilities):
                candidates.append(
                    candidate_to_result(candidate, app_key, catalog_app["display_name"], capabilities)
                )
            else:
                warnings.append(
                    f"Skipped {candidate['source']} candidate because the required tooling is unavailable."
                )
    else:
        for candidate in discover_dynamic_candidates(query, capabilities):
            candidates.append(candidate_to_result(candidate, normalize_name(query), query, capabilities))

    candidates = sort_candidates(candidates)
    recommended = candidates[0] if candidates else None
    alternatives = [simplify_candidate(candidate) for candidate in candidates[1:]]

    if not recommended:
        unreviewed_candidates = sort_candidates(
            [
                candidate_to_result(candidate, normalize_name(query), query, capabilities)
                for candidate in discover_unreviewed_candidates(query, capabilities)
            ]
        )
        alternatives.extend(simplify_candidate(candidate) for candidate in unreviewed_candidates)
        if unreviewed_candidates:
            warnings.append(
                "No curated or official install path was found, but unreviewed community suggestions are available."
            )
        else:
            warnings.append("No safe automated path found for this app on the current host.")

    return {
        "app_query": query,
        "recommended_source": recommended["source"] if recommended else None,
        "recommended_package": recommended["package"] if recommended else None,
        "community": recommended["community"] if recommended else False,
        "unreviewed": recommended["unreviewed"] if recommended else False,
        "community_label": recommended["community_label"] if recommended else None,
        "upstream_name": recommended["upstream_name"] if recommended else None,
        "requires_additional_confirmation": (
            recommended["requires_additional_confirmation"] if recommended else False
        ),
        "requires_unsafe_mode": recommended["requires_unsafe_mode"] if recommended else False,
        "missing_tools": recommended["missing_tools"] if recommended else [],
        "tooling_command": recommended["tooling_command"] if recommended else None,
        "install_command": recommended["install_command"] if recommended else None,
        "launch_command": recommended["launch_command"] if recommended else None,
        "launch_verified": recommended["launch_verified"] if recommended else False,
        "uninstall_command": recommended["uninstall_command"] if recommended else None,
        "summary": recommended["summary"] if recommended else None,
        "source_url": recommended["source_url"] if recommended else None,
        "review_summary": recommended["review_summary"] if recommended else None,
        "rating": recommended["rating"] if recommended else None,
        "reason": recommended["reason"] if recommended else "No safe automated path found.",
        "alternatives": alternatives,
        "warnings": warnings + (recommended["warnings"] if recommended else []),
        "manual_steps": recommended["manual_steps"] if recommended else [],
        "recipe": recommended["recipe"] if recommended else None,
        "requires_confirmation": True,
        "unsafe_mode_enabled": settings["unsafe_community_installs"],
        "capabilities": capabilities,
    }


def locate_candidate(query, source, package):
    catalog = load_catalog()
    capabilities = detect_capabilities()
    app_key, catalog_app = resolve_catalog_app(query, catalog)
    if catalog_app:
        for candidate in catalog_app.get("candidates", []):
            if candidate["source"] == source and candidate["package"] == package:
                return candidate_to_result(candidate, app_key, catalog_app["display_name"], capabilities)

    for candidate in discover_dynamic_candidates(query, capabilities):
        if candidate["source"] == source and candidate["package"] == package:
            return candidate_to_result(candidate, normalize_name(query), query, capabilities)

    for candidate in discover_unreviewed_candidates(query, capabilities):
        if candidate["source"] == source and candidate["package"] == package:
            return candidate_to_result(candidate, normalize_name(query), query, capabilities)
    return None


def execute_steps(steps):
    if not steps:
        raise RuntimeError("No install steps are defined for this candidate.")
    for step in steps:
        expanded = [expand_env(part) for part in step]
        result = subprocess.run(expanded, text=True, check=False)
        if result.returncode != 0:
            raise RuntimeError(
                f"Install command failed with exit code {result.returncode}: {shell_join(step)}"
            )


def launch_candidate(candidate):
    launch_steps = candidate.get("launch_steps", [])
    if not launch_steps:
        raise RuntimeError("No launch command is defined for this candidate.")
    expanded = [expand_env(part) for part in launch_steps]
    process = subprocess.Popen(
        expanded,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    return process.pid


def execute_uninstall(candidate):
    uninstall_steps = candidate.get("uninstall_steps", [])
    if candidate["source"] in {"manual", "appimage", "wine"}:
        raise RuntimeError(
            "This candidate does not support safe automated uninstall. Return uninstall_command/manual_steps only."
        )
    if not uninstall_steps:
        raise RuntimeError("No uninstall steps are defined for this candidate.")

    executed = []
    execute_steps(uninstall_steps)
    executed.extend(shell_join(step) for step in uninstall_steps)
    return executed


def execute_install(candidate):
    tooling_steps = candidate["tooling_steps"]
    install_steps = candidate["install_steps"]
    if candidate["source"] == "manual":
        raise RuntimeError(
            "This candidate is a manual fallback. Follow manual_steps/source_url instead of using install."
        )
    if not install_steps:
        raise RuntimeError("No install steps are defined for this candidate.")

    executed = []
    if tooling_steps:
        execute_steps(tooling_steps)
        executed.extend(shell_join(step) for step in tooling_steps)
    execute_steps(install_steps)
    executed.extend(shell_join(step) for step in install_steps)
    return executed


def print_json(data):
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")


def handle_resolve(args):
    print_json(build_resolution(args.app, args.config))
    return 0


def handle_install(args):
    if not args.yes:
        print_json(
            {
                "status": "confirmation_required",
                "message": "Refusing to install without --yes after explicit user confirmation.",
            }
        )
        return 2

    settings = load_settings(args.config)
    candidate = locate_candidate(args.app, args.source, args.package)
    if not candidate:
        print_json(
            {
                "status": "not_found",
                "message": "Resolved candidate no longer matches current catalog/search results.",
            }
        )
        return 1

    if candidate["unreviewed"] and not settings["unsafe_community_installs"]:
        print_json(
            {
                "status": "unsafe_mode_disabled",
                "message": "This candidate is an unreviewed community suggestion. Enable skills.entries.linux-installer.unsafeCommunityInstalls in openclaw.json before installing it.",
                "source": candidate["source"],
                "package": candidate["package"],
                "source_url": candidate["source_url"],
                "warnings": candidate["warnings"],
            }
        )
        return 4

    if candidate["unreviewed"] and not args.allow_unsafe:
        print_json(
            {
                "status": "unsafe_confirmation_required",
                "message": "This candidate is unreviewed. Re-run with --allow-unsafe only after explicit unsafe-mode confirmation from the user.",
                "source": candidate["source"],
                "package": candidate["package"],
                "source_url": candidate["source_url"],
                "warnings": candidate["warnings"],
            }
        )
        return 5

    if candidate["community"] and not args.allow_community:
        print_json(
            {
                "status": "extra_confirmation_required",
                "message": "This candidate is a curated community workaround. Re-run with --allow-community only after explicit extra user confirmation.",
                "source": candidate["source"],
                "package": candidate["package"],
                "community_label": candidate["community_label"],
                "upstream_name": candidate["upstream_name"],
                "launch_command": candidate["launch_command"],
                "warnings": candidate["warnings"],
            }
        )
        return 3

    try:
        executed = execute_install(candidate)
    except RuntimeError as exc:
        print_json(
            {
                "status": "failed",
                "message": str(exc),
                "install_command": candidate["install_command"],
                "launch_command": candidate["launch_command"],
                "manual_steps": candidate.get("manual_steps", []),
                "source_url": candidate.get("source_url"),
                "warnings": candidate["warnings"],
            }
        )
        return 1

    print_json(
        {
            "status": "installed",
            "source": candidate["source"],
            "package": candidate["package"],
            "community": candidate["community"],
            "unreviewed": candidate["unreviewed"],
            "community_label": candidate["community_label"],
            "upstream_name": candidate["upstream_name"],
            "executed_commands": executed,
            "launch_command": candidate["launch_command"],
            "source_url": candidate.get("source_url"),
            "manual_steps": candidate.get("manual_steps", []),
            "warnings": candidate["warnings"],
        }
    )
    return 0


def handle_run_info(args):
    candidate = locate_candidate(args.app, args.source, args.package)
    if not candidate:
        print_json(
            {
                "status": "not_found",
                "message": "No run information is available for that source/package pair.",
            }
        )
        return 1

    print_json(
        {
            "status": "ok",
            "source": candidate["source"],
            "package": candidate["package"],
            "community": candidate["community"],
            "unreviewed": candidate["unreviewed"],
            "launch_command": candidate["launch_command"],
            "launch_verified": candidate["launch_verified"],
            "uninstall_command": candidate["uninstall_command"],
            "source_url": candidate["source_url"],
            "manual_steps": candidate["manual_steps"],
            "recipe": candidate["recipe"],
            "warnings": candidate["warnings"],
        }
    )
    return 0


def handle_run(args):
    candidate = locate_candidate(args.app, args.source, args.package)
    if not candidate:
        print_json(
            {
                "status": "not_found",
                "message": "No run information is available for that source/package pair.",
            }
        )
        return 1

    try:
        pid = launch_candidate(candidate)
    except RuntimeError as exc:
        print_json(
            {
                "status": "failed",
                "message": str(exc),
                "launch_command": candidate["launch_command"],
                "warnings": candidate["warnings"],
            }
        )
        return 1

    print_json(
        {
            "status": "launched",
            "source": candidate["source"],
            "package": candidate["package"],
            "pid": pid,
            "launch_command": candidate["launch_command"],
            "launch_verified": candidate["launch_verified"],
            "warnings": candidate["warnings"],
        }
    )
    return 0


def handle_uninstall(args):
    if not args.yes:
        print_json(
            {
                "status": "confirmation_required",
                "message": "Refusing to uninstall without --yes after explicit user confirmation.",
            }
        )
        return 2

    candidate = locate_candidate(args.app, args.source, args.package)
    if not candidate:
        print_json(
            {
                "status": "not_found",
                "message": "Resolved candidate no longer matches current catalog/search results.",
            }
        )
        return 1

    try:
        executed = execute_uninstall(candidate)
    except RuntimeError as exc:
        print_json(
            {
                "status": "manual_required",
                "message": str(exc),
                "uninstall_command": candidate.get("uninstall_command"),
                "manual_steps": candidate.get("manual_steps", []),
                "source_url": candidate.get("source_url"),
                "warnings": candidate["warnings"],
            }
        )
        return 1

    print_json(
        {
            "status": "uninstalled",
            "source": candidate["source"],
            "package": candidate["package"],
            "executed_commands": executed,
            "uninstall_command": candidate.get("uninstall_command"),
            "warnings": candidate["warnings"],
        }
    )
    return 0


def build_parser():
    parser = argparse.ArgumentParser(prog="linux-installer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve_parser = subparsers.add_parser("resolve", help="Resolve the best install path")
    resolve_parser.add_argument("app", help="App name to resolve")
    resolve_parser.add_argument("--config", help="Path to openclaw.json for skill settings")
    resolve_parser.set_defaults(handler=handle_resolve)

    install_parser = subparsers.add_parser("install", help="Install a resolved candidate")
    install_parser.add_argument("app", help="App name to install")
    install_parser.add_argument("--source", required=True, help="Resolved source")
    install_parser.add_argument("--package", required=True, help="Resolved package identifier")
    install_parser.add_argument("--config", help="Path to openclaw.json for skill settings")
    install_parser.add_argument(
        "--yes",
        action="store_true",
        help="Required confirmation flag after explicit user approval",
    )
    install_parser.add_argument(
        "--allow-community",
        action="store_true",
        help="Required extra confirmation flag for curated community workarounds",
    )
    install_parser.add_argument(
        "--allow-unsafe",
        action="store_true",
        help="Required extra confirmation flag for unreviewed community suggestions",
    )
    install_parser.set_defaults(handler=handle_install)

    run_info_parser = subparsers.add_parser("run-info", help="Show launch command")
    run_info_parser.add_argument("app", help="App name")
    run_info_parser.add_argument("--source", required=True, help="Resolved source")
    run_info_parser.add_argument("--package", required=True, help="Resolved package identifier")
    run_info_parser.add_argument("--config", help="Path to openclaw.json for skill settings")
    run_info_parser.set_defaults(handler=handle_run_info)

    run_parser = subparsers.add_parser("run", help="Launch an installed app")
    run_parser.add_argument("app", help="App name")
    run_parser.add_argument("--source", required=True, help="Resolved source")
    run_parser.add_argument("--package", required=True, help="Resolved package identifier")
    run_parser.add_argument("--config", help="Path to openclaw.json for skill settings")
    run_parser.set_defaults(handler=handle_run)

    uninstall_parser = subparsers.add_parser("uninstall", help="Uninstall a resolved candidate")
    uninstall_parser.add_argument("app", help="App name to uninstall")
    uninstall_parser.add_argument("--source", required=True, help="Resolved source")
    uninstall_parser.add_argument("--package", required=True, help="Resolved package identifier")
    uninstall_parser.add_argument("--config", help="Path to openclaw.json for skill settings")
    uninstall_parser.add_argument(
        "--yes",
        action="store_true",
        help="Required confirmation flag after explicit user approval",
    )
    uninstall_parser.set_defaults(handler=handle_uninstall)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
