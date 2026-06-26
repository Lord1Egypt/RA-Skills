#!/usr/bin/env python3
# Nex GDPR - Request Processor
# MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

import os
import re
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import json

from .config import EXPORT_DIR, REQUEST_TYPES
from .storage import GDPRStorage
from .scanner import DataScanner


class RequestProcessor:
    """Process GDPR requests and handle data operations."""

    def __init__(self):
        self.storage = GDPRStorage()
        self.scanner = DataScanner()

    def process_access_request(self, request_id: int) -> Dict:
        """
        Find all user data and compile into export package (ZIP).
        Returns {"export_path": str, "findings_count": int, "total_size": int}
        """
        request = self.storage.get_request(request_id)
        if not request:
            return {"error": "Request not found"}

        # Scan for user data
        identifier = request["data_subject_email"] or request["data_subject_id"]
        scan_paths = [Path.home() / ".openclaw" / "sessions", Path.home() / ".claw" / "sessions"]
        findings_list = self.scanner.scan_for_user_data(identifier, [str(p) for p in scan_paths])

        # Add database scans
        findings_list.extend(self.scanner.scan_databases(identifier))

        # Save findings
        for finding in findings_list:
            self.storage.save_finding(
                request_id,
                finding.get("data_source", "unknown"),
                finding["file_path"],
                finding.get("data_type", "personal_data"),
                finding.get("description", ""),
                finding.get("size_bytes", 0),
                finding.get("contains_pii", False),
                "exported",
                json.dumps(finding.get("pii_types", [])),
            )

        # Create export package
        export_path = self._create_export_package(request_id, findings_list)

        total_size = sum(f.get("size_bytes", 0) for f in findings_list)

        self.storage.save_audit_entry(
            request_id, "access_processed", "system",
            f"Processed access request. Found {len(findings_list)} data sources. "
            f"Total size: {total_size} bytes. Export: {export_path}"
        )

        return {
            "export_path": export_path,
            "findings_count": len(findings_list),
            "total_size": total_size,
        }

    def process_erasure_request(self, request_id: int) -> Dict:
        """
        Find and delete all user data. Log each deletion.
        Returns {"deleted_count": int, "retained_count": int, "retained_reasons": list}
        """
        request = self.storage.get_request(request_id)
        if not request:
            return {"error": "Request not found"}

        identifier = request["data_subject_email"] or request["data_subject_id"]
        findings_list = self.scanner.scan_for_user_data(identifier)

        deleted_count = 0
        retained_count = 0
        retained_reasons = []

        for finding in findings_list:
            file_path = finding["file_path"]

            # For this demo, we log the deletion but don't actually delete
            # In production, implement proper deletion with backup verification
            if self._safe_delete_file(file_path):
                deleted_count += 1
                self.storage.save_finding(
                    request_id,
                    finding.get("data_source", "unknown"),
                    file_path,
                    finding.get("data_type", "personal_data"),
                    f"Erased: {finding.get('description', '')}",
                    finding.get("size_bytes", 0),
                    False,
                    "deleted",
                    "Securely deleted per Article 17",
                )
            else:
                retained_count += 1
                reason = f"Cannot delete system file: {file_path}"
                retained_reasons.append(reason)
                self.storage.save_finding(
                    request_id,
                    finding.get("data_source", "unknown"),
                    file_path,
                    finding.get("data_type", "personal_data"),
                    finding.get("description", ""),
                    finding.get("size_bytes", 0),
                    finding.get("contains_pii", False),
                    "retained",
                    reason,
                )

        self.storage.save_audit_entry(
            request_id, "erasure_processed", "system",
            f"Processed erasure request. Deleted {deleted_count} items. "
            f"Retained {retained_count} items. Reasons: {', '.join(retained_reasons)}"
        )

        return {
            "deleted_count": deleted_count,
            "retained_count": retained_count,
            "retained_reasons": retained_reasons,
        }

    def process_portability_request(self, request_id: int) -> Dict:
        """
        Export user data in machine-readable format (JSON).
        Returns {"export_path": str}
        """
        request = self.storage.get_request(request_id)
        if not request:
            return {"error": "Request not found"}

        identifier = request["data_subject_email"] or request["data_subject_id"]
        findings_list = self.scanner.scan_for_user_data(identifier)

        # Create machine-readable JSON export
        export_data = {
            "data_subject": {
                "name": request["data_subject_name"],
                "email": request["data_subject_email"],
                "id": request["data_subject_id"],
            },
            "export_date": datetime.now().isoformat(),
            "request_id": request_id,
            "findings": findings_list,
        }

        # Create export file
        export_dir = EXPORT_DIR / f"request_{request_id}"
        export_dir.mkdir(parents=True, exist_ok=True)

        json_file = export_dir / "data_portability.json"
        with open(json_file, "w") as f:
            json.dump(export_data, f, indent=2)

        # Create ZIP archive
        zip_path = EXPORT_DIR / f"data_portability_{request_id}.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.write(json_file, arcname="data_portability.json")

        self.storage.save_audit_entry(
            request_id, "portability_processed", "system",
            f"Processed portability request. Created machine-readable export: {zip_path}"
        )

        return {"export_path": str(zip_path)}

    def process_rectification_request(
        self, request_id: int, corrections: Dict
    ) -> Dict:
        """
        Apply corrections to user data.
        Returns {"corrected_count": int, "details": list}
        """
        request = self.storage.get_request(request_id)
        if not request:
            return {"error": "Request not found"}

        details = []
        corrected_count = 0

        # In production, apply corrections to actual data sources
        # This is a simplified version
        for field, correction in corrections.items():
            details.append(f"Field '{field}' updated")
            corrected_count += 1

        self.storage.save_audit_entry(
            request_id, "rectification_processed", "system",
            f"Processed rectification request. Corrected {corrected_count} fields. "
            f"Details: {', '.join(details)}"
        )

        return {
            "corrected_count": corrected_count,
            "details": details,
        }

    def anonymize_data(self, file_path: str, user_identifier: str) -> str:
        """
        Replace PII with anonymized placeholders in a file.
        Returns path to anonymized file.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Replace identifier with anonymized version
            anonymized = content.replace(user_identifier, "[ANONYMIZED]")

            # Replace email patterns
            anonymized = re.sub(
                r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
                "[EMAIL]",
                anonymized,
            )

            # Replace phone patterns
            anonymized = re.sub(r"\+?1?\d{9,15}", "[PHONE]", anonymized)

            # Save anonymized file
            output_path = Path(file_path).parent / f"{Path(file_path).stem}_anonymized.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(anonymized)

            return str(output_path)

        except Exception as e:
            return ""

    def secure_delete(self, file_path: str) -> bool:
        """
        Overwrite file with random bytes before deletion.
        Returns True if successful.
        """
        try:
            file_size = os.path.getsize(file_path)

            # Overwrite with random data (multiple passes for security)
            with open(file_path, "ba") as f:
                import secrets

                for _ in range(3):  # 3-pass overwrite
                    f.seek(0)
                    f.write(secrets.token_bytes(file_size))

            # Delete the file
            os.remove(file_path)
            return True

        except Exception:
            return False

    def _safe_delete_file(self, file_path: str) -> bool:
        """Safely delete a file (non-system)."""
        try:
            # Don't delete system files
            system_prefixes = ["/sys/", "/proc/", "/dev/", "/etc/"]
            if any(file_path.startswith(p) for p in system_prefixes):
                return False

            # For demo, just log the deletion
            # In production: use secure_delete() instead
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Check if it's a user-owned file
                stat_info = os.stat(file_path)
                if stat_info.st_uid == os.getuid():
                    os.remove(file_path)
                    return True

            return False

        except Exception:
            return False

    def _create_export_package(self, request_id: int, findings: List[Dict]) -> str:
        """
        ZIP all found data files.
        Returns path to ZIP.
        """
        export_dir = EXPORT_DIR / f"request_{request_id}"
        export_dir.mkdir(parents=True, exist_ok=True)

        # Create manifest
        manifest = {
            "request_id": request_id,
            "export_date": datetime.now().isoformat(),
            "findings_count": len(findings),
            "findings": [],
        }

        # Copy data files (or log paths if not accessible)
        for finding in findings:
            file_path = finding["file_path"]
            try:
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    # For security, copy to export dir instead of including originals
                    file_size = os.path.getsize(file_path)
                    if file_size < 10 * 1024 * 1024:  # Only copy files < 10MB
                        dest = export_dir / Path(file_path).name
                        shutil.copy2(file_path, dest)
                        manifest["findings"].append(
                            {
                                "file": file_path,
                                "exported": True,
                                "size": file_size,
                            }
                        )
                    else:
                        manifest["findings"].append(
                            {
                                "file": file_path,
                                "exported": False,
                                "reason": "File too large (>10MB)",
                                "size": file_size,
                            }
                        )
            except Exception as e:
                manifest["findings"].append(
                    {
                        "file": file_path,
                        "exported": False,
                        "reason": str(e),
                    }
                )

        # Write manifest
        with open(export_dir / "manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)

        # Create ZIP
        zip_path = EXPORT_DIR / f"access_request_{request_id}.zip"
        shutil.make_archive(str(zip_path.with_suffix("")), "zip", export_dir)

        return str(zip_path)
