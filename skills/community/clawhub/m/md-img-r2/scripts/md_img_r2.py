#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime as dt
import hashlib
import hmac
import json
import mimetypes
import os
import re
import shutil
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MD_IMAGE_RE = re.compile(r'!\[[^\]]*]\(([^)]+)\)')
HTML_IMG_RE = re.compile(r'(<img\b[^>]*?\bsrc\s*=\s*)(["\']?)([^"\'>\s]+)(\2)', re.IGNORECASE)
REF_DEF_RE = re.compile(r'^\[([^\]]+)]\s*:\s*(.+)$', re.MULTILINE)

URL_SCHEMES = ("http://", "https://", "data:", "mailto:")
DEFAULT_REGION = "auto"
DEFAULT_PREFIX = "md-assets"
SKILL_ROOT = Path(__file__).resolve().parent.parent
SKILL_DOTENV = SKILL_ROOT / ".env"


def is_remote(value: str) -> bool:
    return value.strip().startswith(URL_SCHEMES)


def parse_md_link_inner(inner: str) -> Tuple[str, str]:
    s = inner.strip()
    if s.startswith("<"):
        end = s.find(">")
        if end != -1:
            path = s[1:end].strip()
            tail = s[end + 1:]
            return path, tail

    parts = s.split(maxsplit=1)
    path = parts[0]
    tail = ""
    if len(parts) == 2:
        idx = s.find(parts[1])
        tail = s[idx - 1:] if idx > 0 else " " + parts[1]
    return path, tail


def parse_ref_definition_rhs(rhs: str) -> Tuple[str, str]:
    return parse_md_link_inner(rhs)


def find_md_files(target: Path, recursive: bool) -> List[Path]:
    if target.is_file():
        return [target]
    if not target.is_dir():
        raise FileNotFoundError(str(target))
    pattern = "**/*.md" if recursive else "*.md"
    return sorted(path for path in target.glob(pattern) if path.is_file())


def backup_file(path: Path) -> Path:
    backup = path.with_suffix(path.suffix + ".bak")
    shutil.copy2(path, backup)
    return backup


def resolve_local_path(md_path: Path, raw: str) -> Path:
    raw = raw.replace("%20", " ")
    path = Path(raw)
    if not path.is_absolute():
        path = (md_path.parent / path).resolve()
    return path


def replace_in_text(text: str, replacements: List[Tuple[int, int, str]]) -> str:
    if not replacements:
        return text
    replacements.sort(key=lambda item: item[0])
    out = []
    last = 0
    for start, end, new_value in replacements:
        out.append(text[last:start])
        out.append(new_value)
        last = end
    out.append(text[last:])
    return "".join(out)


def parse_dotenv_line(line: str) -> Optional[Tuple[str, str]]:
    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None
    if stripped.startswith("export "):
        stripped = stripped[len("export "):].strip()
    if "=" not in stripped:
        return None
    key, value = stripped.split("=", 1)
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    if value and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return key, value


def load_dotenv(path: Path) -> Dict[str, str]:
    data: Dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        parsed = parse_dotenv_line(line)
        if parsed:
            key, value = parsed
            data[key] = value
    return data


def discover_dotenv(target: Path, explicit_env_file: Optional[str]) -> Optional[Path]:
    if explicit_env_file:
        env_path = Path(explicit_env_file).expanduser()
        if not env_path.is_absolute():
            env_path = (Path.cwd() / env_path).resolve()
        if not env_path.is_file():
            raise SystemExit(f".env file not found: {env_path}")
        return env_path

    if SKILL_DOTENV.is_file():
        return SKILL_DOTENV

    search_root = target.parent if target.is_file() else target
    for directory in [search_root, *search_root.parents]:
        candidate = directory / ".env"
        if candidate.is_file():
            return candidate
    cwd_env = Path.cwd() / ".env"
    if cwd_env.is_file():
        return cwd_env
    return None


def env_or_arg(
    arg_value: Optional[str],
    env_name: str,
    dotenv: Dict[str, str],
    default: Optional[str] = None,
) -> Optional[str]:
    if arg_value:
        return arg_value
    env_value = os.getenv(env_name)
    if env_value:
        return env_value
    dotenv_value = dotenv.get(env_name)
    if dotenv_value:
        return dotenv_value
    return default


def default_endpoint(account_id: str) -> str:
    return f"https://{account_id}.r2.cloudflarestorage.com"


def build_missing_config_message(missing: List[str], dotenv_path: Optional[Path]) -> str:
    lines = [
        "Missing required config: " + ", ".join(missing),
        "You can provide them by either:",
        "1. shell environment variables",
        "2. a .env file near your markdown project",
        "3. --env-file /path/to/.env",
        "",
        "Start from this template:",
        "md-img-r2/r2-config.env",
    ]
    if dotenv_path:
        lines.extend(["", f"Detected .env file: {dotenv_path}"])
    return "\n".join(lines)


def resolve_config(args, dotenv: Dict[str, str], dotenv_path: Optional[Path]) -> dict:
    account_id = env_or_arg(args.account_id, "CF_R2_ACCOUNT_ID", dotenv)
    access_key_id = env_or_arg(args.access_key_id, "CF_R2_ACCESS_KEY_ID", dotenv)
    secret_access_key = env_or_arg(args.secret_access_key, "CF_R2_SECRET_ACCESS_KEY", dotenv)
    bucket = env_or_arg(args.bucket, "CF_R2_BUCKET", dotenv)
    public_base_url = env_or_arg(args.public_base_url, "CF_R2_PUBLIC_BASE_URL", dotenv)
    region = env_or_arg(args.region, "CF_R2_REGION", dotenv, DEFAULT_REGION)
    key_prefix = env_or_arg(args.key_prefix, "CF_R2_KEY_PREFIX", dotenv, DEFAULT_PREFIX) or DEFAULT_PREFIX
    endpoint = env_or_arg(args.endpoint, "CF_R2_ENDPOINT", dotenv)

    if not endpoint and account_id:
        endpoint = default_endpoint(account_id)

    if args.dry_run:
        return {
            "account_id": account_id,
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
            "bucket": bucket,
            "public_base_url": public_base_url,
            "region": region,
            "endpoint": endpoint,
            "key_prefix": key_prefix.strip("/"),
            "dotenv_path": str(dotenv_path) if dotenv_path else None,
        }

    required = {
        "CF_R2_ACCESS_KEY_ID": access_key_id,
        "CF_R2_SECRET_ACCESS_KEY": secret_access_key,
        "CF_R2_BUCKET": bucket,
        "CF_R2_PUBLIC_BASE_URL": public_base_url,
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise SystemExit(build_missing_config_message(missing, dotenv_path))
    if not endpoint:
        raise SystemExit(
            "Missing R2 endpoint. Set CF_R2_ENDPOINT or CF_R2_ACCOUNT_ID.\n"
            "You can fill it in your .env based on md-img-r2/r2-config.env"
        )

    return {
        "account_id": account_id,
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
        "bucket": bucket,
        "public_base_url": public_base_url,
        "region": region,
        "endpoint": endpoint,
        "key_prefix": key_prefix.strip("/"),
        "dotenv_path": str(dotenv_path) if dotenv_path else None,
    }


def sanitize_filename(name: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip())
    sanitized = re.sub(r"-{2,}", "-", sanitized).strip(".-")
    return sanitized or "file"


def build_object_key(path: Path, key_prefix: str) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    filename = sanitize_filename(path.name)
    key = f"{digest}-{filename}"
    if key_prefix:
        return f"{key_prefix}/{key}"
    return key


def guess_content_type(path: Path) -> str:
    content_type, _ = mimetypes.guess_type(str(path))
    return content_type or "application/octet-stream"


def sha256_hex(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def get_signature_key(secret_key: str, date_stamp: str, region_name: str, service_name: str) -> bytes:
    k_date = sign(("AWS4" + secret_key).encode("utf-8"), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    return sign(k_service, "aws4_request")


def build_public_url(public_base_url: Optional[str], object_key: str) -> str:
    base = (public_base_url or "https://example.invalid").rstrip("/")
    return base + "/" + urllib.parse.quote(object_key, safe="/-_.~")


def build_signed_headers(
    method: str,
    url: str,
    access_key_id: str,
    secret_access_key: str,
    region: str,
    content_type: str,
    payload_hash: str,
) -> dict:
    parsed = urllib.parse.urlsplit(url)
    host = parsed.netloc
    now = dt.datetime.now(dt.timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    canonical_uri = parsed.path or "/"
    canonical_querystring = urllib.parse.urlencode(sorted(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)))

    headers = {
        "content-type": content_type,
        "host": host,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_date,
    }
    signed_headers = ";".join(sorted(headers))
    canonical_headers = "".join(f"{key}:{headers[key]}\n" for key in sorted(headers))
    canonical_request = "\n".join(
        [
            method,
            canonical_uri,
            canonical_querystring,
            canonical_headers,
            signed_headers,
            payload_hash,
        ]
    )

    credential_scope = f"{date_stamp}/{region}/s3/aws4_request"
    string_to_sign = "\n".join(
        [
            "AWS4-HMAC-SHA256",
            amz_date,
            credential_scope,
            sha256_hex(canonical_request.encode("utf-8")),
        ]
    )
    signing_key = get_signature_key(secret_access_key, date_stamp, region, "s3")
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    authorization = (
        f"AWS4-HMAC-SHA256 Credential={access_key_id}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    return {
        "Content-Type": content_type,
        "Host": host,
        "X-Amz-Content-Sha256": payload_hash,
        "X-Amz-Date": amz_date,
        "Authorization": authorization,
    }


def upload_file(config: dict, local_path: Path, object_key: str) -> str:
    payload = local_path.read_bytes()
    content_type = guess_content_type(local_path)
    object_path = "/" + config["bucket"] + "/" + urllib.parse.quote(object_key, safe="/-_.~")
    url = config["endpoint"].rstrip("/") + object_path
    payload_hash = sha256_hex(payload)
    headers = build_signed_headers(
        method="PUT",
        url=url,
        access_key_id=config["access_key_id"],
        secret_access_key=config["secret_access_key"],
        region=config["region"],
        content_type=content_type,
        payload_hash=payload_hash,
    )
    request = urllib.request.Request(url=url, data=payload, headers=headers, method="PUT")
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            if response.status >= 300:
                raise RuntimeError(f"Unexpected R2 status: {response.status}")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace") if hasattr(error, "read") else ""
        raise RuntimeError(f"R2 HTTPError {error.code}: {body}") from error
    except Exception as error:
        raise RuntimeError(f"R2 upload error: {error}") from error
    return build_public_url(config["public_base_url"], object_key)


def process_one_file(md_file: Path, args, config: dict) -> dict:
    original = md_file.read_text(encoding="utf-8")
    report = {
        "file": str(md_file),
        "bucket": config["bucket"],
        "endpoint": config["endpoint"],
        "public_base_url": config["public_base_url"],
        "key_prefix": config["key_prefix"],
        "dotenv_path": config["dotenv_path"],
        "replaced": [],
        "skipped_remote": [],
        "missing_files": [],
        "upload_failed": [],
        "dry_run": bool(args.dry_run),
    }

    md_matches = []
    for match in MD_IMAGE_RE.finditer(original):
        inner = match.group(1)
        link, tail = parse_md_link_inner(inner)
        md_matches.append((match.start(1), match.end(1), link, tail))

    html_matches = []
    for match in HTML_IMG_RE.finditer(original):
        html_matches.append((match.start(3), match.end(3), match.group(3)))

    ref_matches = []
    for match in REF_DEF_RE.finditer(original):
        rhs = match.group(2).strip()
        link, tail = parse_ref_definition_rhs(rhs)
        ref_matches.append((match.start(2), match.end(2), link, tail))

    occurrences = []
    upload_plan: Dict[str, dict] = {}

    for start, end, link, tail in md_matches:
        if is_remote(link):
            report["skipped_remote"].append({"kind": "md", "link": link})
            continue
        abs_path = resolve_local_path(md_file, link)
        if not abs_path.exists():
            report["missing_files"].append({"kind": "md", "link": link, "resolved": str(abs_path)})
            continue
        upload_plan.setdefault(str(abs_path), {"object_key": build_object_key(abs_path, config["key_prefix"])})
        occurrences.append(("md", start, end, link, tail, str(abs_path)))

    for start, end, link in html_matches:
        if is_remote(link):
            report["skipped_remote"].append({"kind": "html", "link": link})
            continue
        abs_path = resolve_local_path(md_file, link)
        if not abs_path.exists():
            report["missing_files"].append({"kind": "html", "link": link, "resolved": str(abs_path)})
            continue
        upload_plan.setdefault(str(abs_path), {"object_key": build_object_key(abs_path, config["key_prefix"])})
        occurrences.append(("html", start, end, link, "", str(abs_path)))

    for start, end, link, tail in ref_matches:
        if is_remote(link):
            report["skipped_remote"].append({"kind": "ref", "link": link})
            continue
        abs_path = resolve_local_path(md_file, link)
        if not abs_path.exists():
            report["missing_files"].append({"kind": "ref", "link": link, "resolved": str(abs_path)})
            continue
        upload_plan.setdefault(str(abs_path), {"object_key": build_object_key(abs_path, config["key_prefix"])})
        occurrences.append(("ref", start, end, link, tail, str(abs_path)))

    uploaded_map: Dict[str, str] = {}
    for abs_path, meta in sorted(upload_plan.items()):
        object_key = meta["object_key"]
        if args.dry_run:
            uploaded_map[abs_path] = build_public_url(config["public_base_url"], object_key)
            continue
        try:
            uploaded_map[abs_path] = upload_file(config, Path(abs_path), object_key)
        except Exception as error:
            report["upload_failed"].append(
                {
                    "path": abs_path,
                    "object_key": object_key,
                    "error": str(error),
                }
            )

    spans: List[Tuple[int, int, str]] = []
    for kind, start, end, link, tail, abs_path in occurrences:
        url = uploaded_map.get(abs_path)
        if not url:
            continue
        if kind == "md":
            spans.append((start, end, f"{url}{tail}"))
        elif kind == "html":
            spans.append((start, end, url))
        else:
            spans.append((start, end, f"{url}{tail}"))
        report["replaced"].append(
            {
                "kind": kind,
                "from": link,
                "to": url,
                "resolved": abs_path,
                "object_key": upload_plan[abs_path]["object_key"],
            }
        )

    new_text = replace_in_text(original, spans)
    report_path = md_file.with_suffix(md_file.suffix + ".replace-report.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if (not args.dry_run) and new_text != original:
        backup_file(md_file)
        md_file.write_text(new_text, encoding="utf-8")

    return report


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Upload local images in Markdown directly to Cloudflare R2 and replace paths with public URLs."
    )
    parser.add_argument("target", help="Markdown file or directory")
    parser.add_argument("--recursive", action="store_true", help="If target is a directory, process *.md recursively")
    parser.add_argument("--dry-run", action="store_true", help="Do not modify files; only generate report")
    parser.add_argument("--key-prefix", default=None, help="Override CF_R2_KEY_PREFIX")
    parser.add_argument("--public-base-url", default=None, help="Override CF_R2_PUBLIC_BASE_URL")
    parser.add_argument("--endpoint", default=None, help="Override CF_R2_ENDPOINT")
    parser.add_argument("--bucket", default=None, help="Override CF_R2_BUCKET")
    parser.add_argument("--account-id", default=None, help="Override CF_R2_ACCOUNT_ID")
    parser.add_argument("--access-key-id", default=None, help="Override CF_R2_ACCESS_KEY_ID")
    parser.add_argument("--secret-access-key", default=None, help="Override CF_R2_SECRET_ACCESS_KEY")
    parser.add_argument("--region", default=None, help="Override CF_R2_REGION")
    parser.add_argument("--env-file", default=None, help="Path to a .env file. Defaults to searching upward from target.")
    return parser


def main() -> int:
    parser = build_arg_parser()
    args = parser.parse_args()
    target = Path(args.target).expanduser().resolve()
    dotenv_path = discover_dotenv(target, args.env_file)
    dotenv = load_dotenv(dotenv_path) if dotenv_path else {}
    config = resolve_config(args, dotenv, dotenv_path)
    md_files = find_md_files(target, args.recursive)
    if not md_files:
        print("No markdown files found.")
        return 0

    for md_file in md_files:
        report = process_one_file(md_file, args, config)
        print(f"[OK] {md_file}")
        print(
            "  "
            + f"replaced={len(report['replaced'])} "
            + f"skipped_remote={len(report['skipped_remote'])} "
            + f"missing={len(report['missing_files'])} "
            + f"upload_failed={len(report['upload_failed'])}"
        )
        print(f"  report={md_file.with_suffix(md_file.suffix + '.replace-report.json')}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
