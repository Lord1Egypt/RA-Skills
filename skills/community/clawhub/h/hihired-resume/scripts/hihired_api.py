#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import tempfile
from pathlib import Path
from urllib import request, error

DEFAULT_BASE = os.environ.get("HIHIRED_BASE_URL", "http://18.190.155.165")
DEFAULT_TIMEOUT = int(os.environ.get("HIHIRED_TIMEOUT", "120"))


def parse_json_response(resp):
    raw = resp.read().decode("utf-8", errors="replace")
    raw = raw.lstrip("\ufeff").strip()
    return json.loads(raw)


def post_json(base_url: str, endpoint: str, payload: dict):
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        f"{base_url.rstrip('/')}{endpoint}",
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        return parse_json_response(resp)


def post_multipart(base_url: str, endpoint: str, file_path: str, field_name: str = "resume"):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(file_path)

    boundary = "----OpenClawHiHiredBoundary7MA4YWxkTrZu0gW"
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    file_bytes = path.read_bytes()

    parts = []
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(
        f'Content-Disposition: form-data; name="{field_name}"; filename="{path.name}"\r\n'.encode()
    )
    parts.append(f"Content-Type: {content_type}\r\n\r\n".encode())
    parts.append(file_bytes)
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(parts)

    req = request.Request(
        f"{base_url.rstrip('/')}{endpoint}",
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        return parse_json_response(resp)


def cmd_parse_resume(args):
    return post_multipart(args.base_url, "/api/resume/parse", args.file)


def cmd_cover_letter(args):
    payload = {
        "resumeData": load_json_arg(args.resume_data),
        "jobDescription": args.job_description or "",
        "companyName": args.company_name or "",
        "position": args.position or "",
        "letterType": args.letter_type or "",
    }
    return post_json(args.base_url, "/api/cover-letter/generate", payload)


def cmd_summary(args):
    payload = {
        "experience": args.experience or "",
        "education": args.education or "",
        "skills": load_json_arg(args.skills, default=[]),
        "existingSummary": args.existing_summary or "",
        "jobDescription": args.job_description or "",
        "matchedSkills": load_json_arg(args.matched_skills, default=[]),
        "missingSkills": load_json_arg(args.missing_skills, default=[]),
    }
    return post_json(args.base_url, "/api/ai/summary", payload)


def cmd_resume_advice(args):
    payload = {
        "resumeData": load_json_arg(args.resume_data),
        "jobDescription": args.job_description or "",
    }
    return post_json(args.base_url, "/api/resume/analyze-advice", payload)


def cmd_auto_skills(args):
    payload = {
        "resumeData": load_json_arg(args.resume_data),
        "jobDescription": args.job_description or "",
        "existingSkills": load_json_arg(args.existing_skills, default=[]),
    }
    return post_json(args.base_url, "/api/skills/auto-generate", payload)


def cmd_categorize_skills(args):
    payload = {
        "skillsText": args.skills_text,
        "jobDescription": args.job_description or "",
    }
    return post_json(args.base_url, "/api/skills/categorize", payload)


def cmd_modify_resume(args):
    payload = {
        "text": args.text,
        "existingData": load_json_arg(args.existing_data, default={}),
    }
    return post_json(args.base_url, "/api/assistant/resume/modify", payload)


def cmd_template_pref(args):
    return post_json(args.base_url, "/api/template/preference", {"text": args.text})


def load_json_arg(raw, default=None):
    if raw is None:
        if default is None:
            raise ValueError("JSON argument required")
        return default
    raw = raw.strip()
    if not raw:
        if default is None:
            raise ValueError("JSON argument required")
        return default
    if raw.startswith("@"):
        return json.loads(Path(raw[1:]).read_text(encoding="utf-8"))
    return json.loads(raw)


def write_temp_json(data):
    fd, path = tempfile.mkstemp(prefix="hihired_", suffix=".json")
    os.close(fd)
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def build_parser():
    parser = argparse.ArgumentParser(description="Call HiHired public API endpoints")
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("parse-resume")
    p.add_argument("file")
    p.set_defaults(func=cmd_parse_resume)

    p = sub.add_parser("cover-letter")
    p.add_argument("--resume-data", required=True, help="JSON string or @file.json")
    p.add_argument("--job-description")
    p.add_argument("--company-name")
    p.add_argument("--position")
    p.add_argument("--letter-type")
    p.set_defaults(func=cmd_cover_letter)

    p = sub.add_parser("summary")
    p.add_argument("--experience")
    p.add_argument("--education")
    p.add_argument("--skills", default="[]", help="JSON array or @file.json")
    p.add_argument("--existing-summary")
    p.add_argument("--job-description")
    p.add_argument("--matched-skills", default="[]")
    p.add_argument("--missing-skills", default="[]")
    p.set_defaults(func=cmd_summary)

    p = sub.add_parser("resume-advice")
    p.add_argument("--resume-data", required=True, help="JSON string or @file.json")
    p.add_argument("--job-description")
    p.set_defaults(func=cmd_resume_advice)

    p = sub.add_parser("auto-skills")
    p.add_argument("--resume-data", required=True, help="JSON string or @file.json")
    p.add_argument("--job-description")
    p.add_argument("--existing-skills", default="[]")
    p.set_defaults(func=cmd_auto_skills)

    p = sub.add_parser("categorize-skills")
    p.add_argument("--skills-text", required=True)
    p.add_argument("--job-description")
    p.set_defaults(func=cmd_categorize_skills)

    p = sub.add_parser("modify-resume")
    p.add_argument("--text", required=True)
    p.add_argument("--existing-data", default="{}")
    p.set_defaults(func=cmd_modify_resume)

    p = sub.add_parser("template-preference")
    p.add_argument("--text", required=True)
    p.set_defaults(func=cmd_template_pref)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        result = args.func(args)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        print(json.dumps({"ok": False, "status": exc.code, "error": body}, ensure_ascii=False))
        sys.exit(1)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
