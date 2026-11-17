#!/usr/bin/env python3
"""Plan or explicitly apply Markdown image URL replacements for R2-compatible storage."""

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


INLINE_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
HTML_IMAGE_RE = re.compile(r"(<img\b[^>]*?\bsrc\s*=\s*)([\"']?)([^\"'>\s]+)(\2)", re.IGNORECASE)
IMAGE_REFERENCE_RE = re.compile(r"!\[[^\]]*\]\[([^\]]+)\]")
REFERENCE_DEF_RE = re.compile(r"^\[([^\]]+)\]\s*:\s*(.+)$", re.MULTILINE)
REMOTE_PREFIXES = ("http://", "https://", "data:", "mailto:")


def is_remote(value):
    return value.strip().lower().startswith(REMOTE_PREFIXES)


def split_target(value):
    text = value.strip()
    if text.startswith("<"):
        close = text.find(">")
        if close >= 0:
            return text[1:close].strip(), text[close + 1 :]
    pieces = text.split(maxsplit=1)
    return pieces[0], "" if len(pieces) == 1 else " " + pieces[1]


def find_markdown_files(target, recursive):
    if target.is_file():
        return [target]
    pattern = "**/*.md" if recursive else "*.md"
    return sorted(path for path in target.glob(pattern) if path.is_file())


def normalize_source(markdown_file, raw):
    value = urllib.parse.unquote(raw)
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = markdown_file.parent / candidate
    return candidate.resolve()


def safe_name(name):
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", name.strip())
    value = re.sub(r"-{2,}", "-", value).strip(".-")
    return value or "image"


def object_key(local_file, prefix):
    digest = hashlib.sha256(local_file.read_bytes()).hexdigest()[:16]
    base = f"{digest}-{safe_name(local_file.name)}"
    clean_prefix = prefix.strip("/")
    return f"{clean_prefix}/{base}" if clean_prefix else base


def public_url(base, key):
    return base.rstrip("/") + "/" + urllib.parse.quote(key, safe="/-_.~")


def replace_spans(text, spans):
    result = text
    for start, end, replacement in sorted(spans, reverse=True):
        result = result[:start] + replacement + result[end:]
    return result


def collect_occurrences(markdown_file, text):
    items = []
    used_reference_labels = {match.group(1).strip().lower() for match in IMAGE_REFERENCE_RE.finditer(text)}
    for match in INLINE_IMAGE_RE.finditer(text):
        raw, tail = split_target(match.group(1))
        items.append({"kind": "markdown", "start": match.start(1), "end": match.end(1), "raw": raw, "tail": tail})
    for match in HTML_IMAGE_RE.finditer(text):
        items.append({"kind": "html", "start": match.start(3), "end": match.end(3), "raw": match.group(3), "tail": ""})
    for match in REFERENCE_DEF_RE.finditer(text):
        if match.group(1).strip().lower() not in used_reference_labels:
            continue
        raw, tail = split_target(match.group(2))
        items.append({"kind": "reference", "start": match.start(2), "end": match.end(2), "raw": raw, "tail": tail})
    return items


def report_path(markdown_file):
    return markdown_file.with_suffix(markdown_file.suffix + ".image-publish-plan.json")


def read_url_map(path):
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("URL map must be a JSON object of local reference to public URL.")
    for source, target in payload.items():
        if not isinstance(source, str) or not isinstance(target, str) or not target.startswith(("http://", "https://")):
            raise ValueError("Every URL map entry must use a string source and an http or https public URL.")
    return payload


def environment_or_arg(value, name, default=None):
    return value or os.getenv(name) or default


def upload_config(args):
    account_id = environment_or_arg(args.account_id, "R2_ACCOUNT_ID")
    endpoint = environment_or_arg(args.endpoint, "R2_ENDPOINT")
    if not endpoint and account_id:
        endpoint = f"https://{account_id}.r2.cloudflarestorage.com"
    config = {
        "access_key_id": environment_or_arg(args.access_key_id, "R2_ACCESS_KEY_ID"),
        "secret_access_key": environment_or_arg(args.secret_access_key, "R2_SECRET_ACCESS_KEY"),
        "bucket": environment_or_arg(args.bucket, "R2_BUCKET"),
        "public_base_url": environment_or_arg(args.public_base_url, "R2_PUBLIC_BASE_URL"),
        "endpoint": endpoint,
        "region": environment_or_arg(args.region, "R2_REGION", "auto"),
        "key_prefix": environment_or_arg(args.key_prefix, "R2_KEY_PREFIX", "md-assets"),
    }
    missing = [name for name in ("access_key_id", "secret_access_key", "bucket", "public_base_url", "endpoint") if not config[name]]
    if missing:
        raise ValueError("Missing upload configuration: " + ", ".join(missing))
    return config


def signing_key(secret, date_text, region):
    def signed(key, value):
        return hmac.new(key, value.encode("utf-8"), hashlib.sha256).digest()

    date_key = signed(("AWS4" + secret).encode("utf-8"), date_text)
    region_key = signed(date_key, region)
    service_key = signed(region_key, "s3")
    return signed(service_key, "aws4_request")


def signed_headers(url, access_key_id, secret_access_key, region, content_type, payload):
    parsed = urllib.parse.urlsplit(url)
    now = dt.datetime.now(dt.timezone.utc)
    amz_time = now.strftime("%Y%m%dT%H%M%SZ")
    date_text = now.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(payload).hexdigest()
    canonical_headers = {
        "content-type": content_type,
        "host": parsed.netloc,
        "x-amz-content-sha256": payload_hash,
        "x-amz-date": amz_time,
    }
    header_names = ";".join(sorted(canonical_headers))
    canonical_header_text = "".join(f"{key}:{canonical_headers[key]}\n" for key in sorted(canonical_headers))
    query = urllib.parse.urlencode(sorted(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)))
    canonical_request = "\n".join(["PUT", parsed.path or "/", query, canonical_header_text, header_names, payload_hash])
    scope = f"{date_text}/{region}/s3/aws4_request"
    string_to_sign = "\n".join(["AWS4-HMAC-SHA256", amz_time, scope, hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()])
    signature = hmac.new(signing_key(secret_access_key, date_text, region), string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    return {
        "Content-Type": content_type,
        "Host": parsed.netloc,
        "X-Amz-Content-Sha256": payload_hash,
        "X-Amz-Date": amz_time,
        "Authorization": f"AWS4-HMAC-SHA256 Credential={access_key_id}/{scope}, SignedHeaders={header_names}, Signature={signature}",
    }


def put_object(config, local_file, key):
    payload = local_file.read_bytes()
    content_type = mimetypes.guess_type(str(local_file))[0] or "application/octet-stream"
    object_path = "/" + urllib.parse.quote(config["bucket"], safe="-_.~") + "/" + urllib.parse.quote(key, safe="/-_.~")
    target_url = config["endpoint"].rstrip("/") + object_path
    request = urllib.request.Request(
        target_url,
        data=payload,
        headers=signed_headers(target_url, config["access_key_id"], config["secret_access_key"], config["region"], content_type, payload),
        method="PUT",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            if response.status >= 300:
                raise RuntimeError(f"Unexpected upload status: {response.status}")
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Upload failed with HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Upload connection failed: {exc.reason}") from exc
    return public_url(config["public_base_url"], key)


def build_plan(markdown_file, project_root, allow_outside_root, base_url, prefix):
    text = markdown_file.read_text(encoding="utf-8")
    report = {
        "file": markdown_file.name,
        "mode": "plan",
        "project_root": ".",
        "key_prefix": prefix.strip("/"),
        "planned": [],
        "skipped_remote": [],
        "issues": [],
        "replacements": [],
    }
    seen = {}
    for occurrence in collect_occurrences(markdown_file, text):
        raw = occurrence["raw"]
        if is_remote(raw):
            report["skipped_remote"].append({"kind": occurrence["kind"], "source": raw})
            continue
        local_file = normalize_source(markdown_file, raw)
        if not local_file.is_file():
            report["issues"].append({"kind": occurrence["kind"], "source": raw, "reason": "local image not found"})
            continue
        if not allow_outside_root and project_root not in (local_file, *local_file.parents):
            report["issues"].append({"kind": occurrence["kind"], "source": raw, "reason": "local image is outside project root"})
            continue
        record = seen.setdefault(str(local_file), {"key": object_key(local_file, prefix), "sources": []})
        record["sources"].append({"kind": occurrence["kind"], "source": raw, "start": occurrence["start"], "end": occurrence["end"], "tail": occurrence["tail"]})
    for local_path, detail in sorted(seen.items()):
        report["planned"].append(
            {
                "local": str(Path(local_path).relative_to(project_root)) if project_root in (Path(local_path), *Path(local_path).parents) else str(Path(local_path)),
                "object_key": detail["key"],
                "planned_url": public_url(base_url, detail["key"]),
                "occurrences": len(detail["sources"]),
            }
        )
        for source in detail["sources"]:
            source["local_path"] = local_path
            source["object_key"] = detail["key"]
            report["replacements"].append(source)
    return text, report


def apply_plan(markdown_file, original, report, args, url_map):
    if report["issues"]:
        report["mode"] = "blocked"
        report["apply_reason"] = "Resolve all issues before any upload or rewrite."
        return False
    urls = {}
    if url_map is not None:
        for replacement in report["replacements"]:
            mapped = url_map.get(replacement["source"])
            if not mapped:
                report["issues"].append({"source": replacement["source"], "reason": "URL map has no replacement"})
            else:
                urls[replacement["local_path"]] = mapped
        if report["issues"]:
            report["mode"] = "blocked"
            report["apply_reason"] = "Complete the URL map before rewriting."
            return False
        report["mode"] = "apply-url-map"
    else:
        try:
            config = upload_config(args)
        except ValueError as error:
            report["issues"].append({"reason": str(error)})
            report["mode"] = "blocked"
            report["apply_reason"] = "Supply the required upload configuration before uploading or rewriting."
            return False
        report["mode"] = "apply-upload"
        uploaded = {}
        for replacement in report["replacements"]:
            local_path = replacement["local_path"]
            if local_path not in uploaded:
                try:
                    uploaded[local_path] = put_object(config, Path(local_path), replacement["object_key"])
                except RuntimeError as error:
                    report["issues"].append({"source": replacement["source"], "reason": str(error)})
                    report["apply_reason"] = "One or more uploads failed; Markdown was left unchanged."
                    return False
            urls[local_path] = uploaded[local_path]
    spans = []
    for replacement in report["replacements"]:
        replacement["public_url"] = urls[replacement["local_path"]]
        spans.append((replacement["start"], replacement["end"], urls[replacement["local_path"]] + replacement["tail"]))
    updated = replace_spans(original, spans)
    if updated == original:
        report["apply_reason"] = "No local references required rewriting."
        return True
    backup = markdown_file.with_suffix(markdown_file.suffix + ".bak")
    shutil.copy2(markdown_file, backup)
    markdown_file.write_text(updated, encoding="utf-8")
    report["backup"] = str(backup)
    report["apply_reason"] = "Uploaded or mapped public URLs and rewrote local references."
    return True


def write_report(path, report):
    clean = json.loads(json.dumps(report))
    for replacement in clean["replacements"]:
        for field in ("start", "end", "tail", "local_path"):
            replacement.pop(field, None)
    if "backup" in clean:
        clean["backup"] = Path(clean["backup"]).name
    path.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")


def process(markdown_file, args, project_root, base_url, url_map):
    original, report = build_plan(markdown_file, project_root, args.allow_outside_root, base_url, args.key_prefix or os.getenv("R2_KEY_PREFIX", "md-assets"))
    success = True
    if args.apply:
        success = apply_plan(markdown_file, original, report, args, url_map)
    report_file = report_path(markdown_file)
    write_report(report_file, report)
    print(f"[OK] {markdown_file.name}")
    print(f"  planned={len(report['planned'])} skipped_remote={len(report['skipped_remote'])} issues={len(report['issues'])}")
    print(f"  report={report_file}")
    return success and not report["issues"]


def parser():
    result = argparse.ArgumentParser(description="Plan or explicitly apply Markdown image URL replacements for R2-compatible storage.")
    result.add_argument("target", help="Markdown file or directory")
    result.add_argument("--recursive", action="store_true", help="Process Markdown recursively when target is a directory")
    result.add_argument("--project-root", help="Reviewed root for local images; defaults to the target directory")
    result.add_argument("--allow-outside-root", action="store_true", help="Allow local images outside the reviewed project root")
    result.add_argument("--apply", action="store_true", help="Allow an upload or a reviewed URL-map rewrite")
    result.add_argument("--confirm-upload", action="store_true", help="Confirm the external upload and Markdown rewrite path")
    result.add_argument("--confirm-write", action="store_true", help="Confirm the URL-map Markdown rewrite path")
    result.add_argument("--url-map", help="Reviewed JSON map from local image reference to public URL")
    result.add_argument("--key-prefix", help="Override R2_KEY_PREFIX")
    result.add_argument("--public-base-url", help="Override R2_PUBLIC_BASE_URL")
    result.add_argument("--endpoint", help="Override R2_ENDPOINT")
    result.add_argument("--account-id", help="Override R2_ACCOUNT_ID")
    result.add_argument("--bucket", help="Override R2_BUCKET")
    result.add_argument("--access-key-id", help="Override R2_ACCESS_KEY_ID")
    result.add_argument("--secret-access-key", help="Override R2_SECRET_ACCESS_KEY")
    result.add_argument("--region", help="Override R2_REGION")
    return result


def main():
    args = parser().parse_args()
    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        raise SystemExit(f"Target not found: {target}")
    if args.apply and args.url_map:
        if not args.confirm_write or args.confirm_upload:
            raise SystemExit("URL-map apply requires --apply --confirm-write and must not include --confirm-upload.")
    elif args.apply:
        if not args.confirm_upload or args.confirm_write:
            raise SystemExit("Upload apply requires --apply --confirm-upload and must not include --confirm-write.")
    elif args.confirm_upload or args.confirm_write or args.url_map:
        raise SystemExit("Confirmation and URL-map options require --apply.")
    url_map = read_url_map(Path(args.url_map).expanduser().resolve()) if args.url_map else None
    default_root = target if target.is_dir() else target.parent
    project_root = Path(args.project_root).expanduser().resolve() if args.project_root else default_root
    if not project_root.is_dir():
        raise SystemExit(f"Project root is not a directory: {project_root}")
    base_url = environment_or_arg(args.public_base_url, "R2_PUBLIC_BASE_URL", "https://example.invalid")
    files = find_markdown_files(target, args.recursive)
    if not files:
        print("No Markdown files found.")
        return 0
    outcomes = [process(markdown_file, args, project_root, base_url, url_map) for markdown_file in files]
    return 0 if all(outcomes) else 2


if __name__ == "__main__":
    sys.exit(main())
