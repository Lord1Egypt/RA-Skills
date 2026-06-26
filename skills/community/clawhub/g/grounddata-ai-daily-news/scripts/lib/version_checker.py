"""
version_checker.py — Version upgrade policy check

Responsibilities:
- Compare current version with version policy in manifest
- Return whether force upgrade or recommend upgrade is needed
"""

from lib.schemas import CURRENT_VERSION, VersionError


def check_version(client_policy: dict) -> dict:
    """
    Check if version needs upgrade.

    Parameters:
        client_policy: client_policy field from manifest

    Returns:
        {
            "current": str,
            "latest": str,
            "min_supported": str,
            "needs_upgrade": bool,
            "force_upgrade": bool,
            "message": str,
            "url": str,
        }
    """
    current = CURRENT_VERSION
    latest = client_policy.get("latest_version", current)
    min_supported = client_policy.get("min_supported_version", current)
    upgrade_url = client_policy.get("upgrade_url", "")
    upgrade_msg = client_policy.get("upgrade_message", "")

    force_upgrade = _version_lt(current, min_supported)
    needs_upgrade = _version_lt(current, latest) or force_upgrade

    message = ""
    if force_upgrade:
        message = f"Force upgrade: Current version {current} below minimum supported {min_supported}. {upgrade_msg}"
    elif needs_upgrade:
        message = f"Recommended upgrade: Latest version {latest} available (current {current}). {upgrade_msg}"

    return {
        "current": current,
        "latest": latest,
        "min_supported": min_supported,
        "needs_upgrade": needs_upgrade,
        "force_upgrade": force_upgrade,
        "message": message,
        "url": upgrade_url,
    }


def _version_lt(a: str, b: str) -> bool:
    """Compare two version numbers v1.2.3, return True if a < b"""
    def _parse(v):
        v = v.lstrip("v")
        try:
            return tuple(int(x) for x in v.split("."))
        except ValueError:
            return (0, 0, 0)
    return _parse(a) < _parse(b)
