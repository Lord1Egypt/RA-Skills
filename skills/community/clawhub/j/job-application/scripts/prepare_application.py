#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
from pathlib import Path

from common import OUTPUT_DIR, PROFILE_DIR, ValidationError, load_json, validate_cv_selection


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new application directory outside the skill installation.")
    parser.add_argument("--slug", required=True, help="Directory name in yyyy-mm-company-role form")
    parser.add_argument("--output-root", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--reuse", action="store_true", help="Return an existing directory instead of failing")
    parser.add_argument("--base-application", type=Path,
                        help="Existing application folder whose cv_selection.json is validated before creation")
    parser.add_argument("--profile-dir", type=Path, default=PROFILE_DIR,
                        help="Profile directory used to validate the base selection")
    args = parser.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-[a-z0-9][a-z0-9-]*", args.slug):
        raise SystemExit("Slug must match yyyy-mm-company-role using lowercase letters, digits, and hyphens")

    try:
        if args.base_application:
            base_dir = args.base_application.expanduser().resolve()
            selection_path = base_dir / "cv_selection.json"
            if not base_dir.is_dir() or not os.access(base_dir, os.R_OK | os.X_OK):
                raise ValidationError(f"Base application directory is not readable: {base_dir}")
            if not selection_path.is_file() or not os.access(selection_path, os.R_OK):
                raise ValidationError(f"Base application is missing a readable cv_selection.json: {base_dir}")
            validate_cv_selection(load_json(selection_path), args.profile_dir.expanduser().resolve())

        output_root = args.output_root.expanduser().resolve()
        application_dir = output_root / args.slug
        if application_dir.exists() and not args.reuse:
            raise ValidationError(f"Application directory already exists: {application_dir}")
        output_root.mkdir(parents=True, exist_ok=True)
        application_dir.mkdir(exist_ok=args.reuse)
    except (OSError, ValidationError) as error:
        parser.error(str(error))
    print(application_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
