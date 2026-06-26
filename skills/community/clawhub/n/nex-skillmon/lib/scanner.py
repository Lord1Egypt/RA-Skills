#!/usr/bin/env python3
# Nex SkillMon - Scanner Module
# MIT-0 License - Copyright 2026 Nex AI

import hashlib
import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from urllib.request import urlopen
from urllib.error import URLError
import time

from .config import SKILLS_BASE_DIR, CLAWHUB_API_URL, API_TIMEOUT_SECONDS
from .storage import get_storage

logger = logging.getLogger(__name__)


class Scanner:
    """Scan and analyze installed skills."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir or SKILLS_BASE_DIR)
        self.storage = get_storage()

    def scan_installed_skills(self) -> List[Dict[str, Any]]:
        """Scan the skills directory for installed skills."""
        skills = []

        if not self.base_dir.exists():
            logger.warning(f"Skills directory does not exist: {self.base_dir}")
            return skills

        # Find all SKILL.md files
        skill_md_files = list(self.base_dir.glob("*/SKILL.md"))

        for skill_md in skill_md_files:
            skill_dir = skill_md.parent
            skill_info = self._parse_skill_metadata(skill_md)

            if skill_info:
                skill_info["skill_path"] = str(skill_dir)
                skill_info["file_hash"] = self._calculate_directory_hash(skill_dir)
                skill_info["install_date"] = self._get_install_date(skill_dir)

                skills.append(skill_info)
                logger.info(f"Found skill: {skill_info['name']}")

        return skills

    def _parse_skill_metadata(self, skill_md_path: Path) -> Optional[Dict[str, Any]]:
        """Parse SKILL.md frontmatter."""
        try:
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract YAML frontmatter
            match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
            if not match:
                logger.warning(f"No frontmatter found in {skill_md_path}")
                return None

            frontmatter_text = match.group(1)

            # Simple YAML parsing
            skill_info = {"version": "unknown", "description": ""}

            for line in frontmatter_text.split("\n"):
                if ":" not in line:
                    continue

                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip().strip('"\'')

                if key == "name":
                    skill_info["name"] = value
                elif key == "version":
                    skill_info["version"] = value
                elif key == "description":
                    skill_info["description"] = value
                elif key == "homepage":
                    skill_info["homepage"] = value
                elif key == "author":
                    skill_info["author"] = value

            if "name" not in skill_info:
                logger.warning(f"No name found in {skill_md_path}")
                return None

            return skill_info

        except Exception as e:
            logger.error(f"Error parsing {skill_md_path}: {e}")
            return None

    def _calculate_directory_hash(self, directory: Path) -> str:
        """Calculate SHA256 hash of directory contents."""
        hasher = hashlib.sha256()

        for file_path in sorted(directory.rglob("*")):
            if file_path.is_file() and not file_path.name.startswith("."):
                try:
                    with open(file_path, "rb") as f:
                        hasher.update(f.read())
                except Exception as e:
                    logger.warning(f"Could not hash {file_path}: {e}")

        return hasher.hexdigest()

    def _get_install_date(self, directory: Path) -> str:
        """Get directory creation/modification date."""
        try:
            stat = directory.stat()
            return datetime.fromtimestamp(stat.st_mtime).isoformat()
        except Exception:
            return datetime.now().isoformat()

    def check_for_updates(self, skill_name: str, current_version: str) -> Dict[str, Any]:
        """Check if newer version exists on ClawHub."""
        try:
            url = f"{CLAWHUB_API_URL}/skills/{skill_name}/latest"
            response = urlopen(url, timeout=API_TIMEOUT_SECONDS)
            data = json.loads(response.read().decode())

            latest_version = data.get("version", current_version)
            has_update = self._compare_versions(current_version, latest_version) < 0

            return {
                "update_available": has_update,
                "current_version": current_version,
                "latest_version": latest_version,
                "changelog": data.get("changelog", ""),
            }

        except URLError as e:
            logger.warning(f"Could not check for updates for {skill_name}: {e}")
            return {
                "update_available": False,
                "current_version": current_version,
                "latest_version": current_version,
                "changelog": "",
            }

    def check_security_flags(self, skill_name: str) -> Dict[str, Any]:
        """Check if skill has been flagged on ClawHub."""
        try:
            url = f"{CLAWHUB_API_URL}/skills/{skill_name}/flags"
            response = urlopen(url, timeout=API_TIMEOUT_SECONDS)
            data = json.loads(response.read().decode())

            return {
                "flagged": data.get("flagged", False),
                "severity": data.get("severity", "info"),
                "reason": data.get("reason", ""),
                "checked_at": datetime.now().isoformat(),
            }

        except URLError as e:
            logger.warning(f"Could not check security flags for {skill_name}: {e}")
            return {
                "flagged": False,
                "severity": "unknown",
                "reason": "Could not verify",
                "checked_at": datetime.now().isoformat(),
            }

    def verify_file_integrity(
        self, skill_path: str, stored_hash: Optional[str] = None
    ) -> Dict[str, Any]:
        """Verify file integrity by comparing hashes."""
        skill_dir = Path(skill_path)
        current_hash = self._calculate_directory_hash(skill_dir)

        return {
            "integrity_ok": (current_hash == stored_hash) if stored_hash else True,
            "current_hash": current_hash,
            "stored_hash": stored_hash,
        }

    def detect_stale_skills(self, days: int = 30) -> List[Dict[str, Any]]:
        """Find skills not triggered in N days."""
        return self.storage.get_stale_skills(days=days)

    def full_health_check(self) -> Dict[str, Any]:
        """Run all checks on all skills."""
        skills = self.scan_installed_skills()
        results = {
            "checked_at": datetime.now().isoformat(),
            "total_skills": len(skills),
            "checks": [],
        }

        for skill in skills:
            skill_checks = {
                "name": skill["name"],
                "updates": None,
                "security": None,
                "integrity": None,
                "stale": None,
            }

            # Check for updates
            skill_checks["updates"] = self.check_for_updates(
                skill["name"], skill.get("version", "unknown")
            )

            # Check security flags
            skill_checks["security"] = self.check_security_flags(skill["name"])

            # Check file integrity
            skill_checks["integrity"] = self.verify_file_integrity(
                skill["skill_path"], skill.get("file_hash")
            )

            # Check staleness
            db_skill = self.storage.get_skill_by_name(skill["name"])
            if db_skill:
                stale = self.storage.get_stale_skills(days=30)
                skill_checks["stale"] = any(s["id"] == db_skill["id"] for s in stale)

            results["checks"].append(skill_checks)

            # Save security check if needed
            if skill_checks["security"]["flagged"]:
                db_skill = self.storage.get_skill_by_name(skill["name"])
                if db_skill:
                    self.storage.save_security_check(
                        db_skill["id"],
                        "flagged",
                        skill_checks["security"]["severity"],
                        skill_checks["security"]["reason"],
                    )

            if not skill_checks["integrity"]["integrity_ok"]:
                db_skill = self.storage.get_skill_by_name(skill["name"])
                if db_skill:
                    self.storage.save_security_check(
                        db_skill["id"],
                        "hash_changed",
                        "critical",
                        f"File hash mismatch: {skill_checks['integrity']['current_hash']} vs {skill_checks['integrity']['stored_hash']}",
                    )

            if skill_checks["updates"]["update_available"]:
                db_skill = self.storage.get_skill_by_name(skill["name"])
                if db_skill:
                    self.storage.save_security_check(
                        db_skill["id"],
                        "update_available",
                        "info",
                        f"Update available: {skill_checks['updates']['latest_version']}",
                    )

        return results

    @staticmethod
    def _compare_versions(v1: str, v2: str) -> int:
        """Compare two semantic versions. Returns -1 if v1 < v2, 0 if equal, 1 if v1 > v2."""
        try:
            parts1 = [int(x) for x in v1.split(".")]
            parts2 = [int(x) for x in v2.split(".")]

            # Pad with zeros
            max_len = max(len(parts1), len(parts2))
            parts1 += [0] * (max_len - len(parts1))
            parts2 += [0] * (max_len - len(parts2))

            if parts1 < parts2:
                return -1
            elif parts1 > parts2:
                return 1
            else:
                return 0
        except Exception:
            return 0
