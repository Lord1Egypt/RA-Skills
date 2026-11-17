#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""End-to-end entry point: query CDN accelerated domains, export a local file,
then upload it to a Huawei Cloud OBS bucket/key (with overwrite protection and
optional read-back verification).

Pipeline:

    list_cdn.list_domains(...)          # hcloud CDN ListDomains  (SDK fallback)
        → export_results.export(...)    # local json / csv / md (atomic write)
        → upload_obs.upload_file(...)    # hcloud OBS cp          (SDK fallback)
              → upload_obs.verify_object(...)   # hcloud OBS stat read-back

The CDN side is strictly read-only; the only write is the single OBS object
upload. An already-existing target object is refused unless ``--overwrite``.

Usage:
    python3 scripts/cdn_export_obs.py --region cn-north-4 \
        --format md --bucket my-bucket --key inventory/cdn_domains.md
"""

import argparse
import json
import os
import sys

import export_results
import list_cdn
import upload_obs

DEFAULT_REGION = "cn-north-4"
DEFAULT_FORMAT = "json"


def _build_parser():
    parser = argparse.ArgumentParser(
        description="查询华为云 CDN 加速域名列表，导出本地文件并上传到 OBS（默认不覆盖）。")
    parser.add_argument("-r", "--region", default=DEFAULT_REGION,
                        help="目标 Region（默认 %s）" % DEFAULT_REGION)

    # CDN query filters (real server-side ListDomains parameters)
    parser.add_argument("--domain-name", dest="domain_name",
                        help="按加速域名过滤（服务端查询参数）")
    parser.add_argument("--domain-status", dest="domain_status",
                        help="按加速域名状态过滤（如 online/offline，服务端查询参数）")
    parser.add_argument("--business-type", dest="business_type",
                        help="按业务类型过滤（如 web/download/vod/live，服务端查询参数）")
    parser.add_argument("--service-area", dest="service_area",
                        help="按服务区域过滤（服务端查询参数）")
    parser.add_argument("--enterprise-project-id", dest="enterprise_project_id",
                        help="按企业项目 ID 过滤（服务端查询参数）")
    parser.add_argument("--page-size", type=int, default=list_cdn.DEFAULT_PAGE_SIZE,
                        dest="page_size",
                        help="分页大小（默认 %d）" % list_cdn.DEFAULT_PAGE_SIZE)

    # Export
    parser.add_argument("-f", "--format", default=DEFAULT_FORMAT,
                        choices=list(export_results.FORMATS),
                        help="导出格式：json（默认）/ csv / md")
    parser.add_argument("-o", "--output", default=None,
                        help="本地导出文件路径（默认 cdn_domains_<region>_<ts>.<ext>）")
    parser.add_argument("--summary", action="store_true",
                        help="Markdown 导出时追加汇总行（域名数量）")

    # OBS upload
    parser.add_argument("--bucket", default=None,
                        help="目标 OBS 桶名（上传必填；缺省则仅做本地导出）")
    parser.add_argument("--key", default=None,
                        help="目标 OBS 对象键（默认取导出文件名）")
    parser.add_argument("--endpoint", default=None,
                        help="自定义 OBS endpoint（默认 obs.<region>.myhuaweicloud.com）")
    parser.add_argument("--overwrite", action="store_true",
                        help="允许覆盖已存在的目标对象（默认拒绝覆盖）")
    parser.add_argument("--no-verify", action="store_true", dest="no_verify",
                        help="上传后不做回读校验")
    parser.add_argument("--export-only", action="store_true", dest="export_only",
                        help="仅查询并导出本地文件，不上传 OBS")
    parser.add_argument("--operation", default=list_cdn.ALLOWED_OPERATION,
                        help="hcloud CDN 操作名（仅允许只读 %s）"
                             % list_cdn.ALLOWED_OPERATION)
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="以 JSON 输出本次运行结果")
    return parser


def _guard(args, raw_argv):
    """CDN write-intent guard over the CDN-relevant arguments only.

    Local export flags (--output / --format / --summary), the OBS target
    (--bucket / --key / --endpoint / --overwrite) and the verify flags are NOT
    CDN operations and are excluded, so a local path like
    ``cdn-delete-report.md`` cannot trip the guard.
    """
    list_cdn.guard_operation(args.operation)
    for value in (args.domain_name, args.domain_status, args.business_type,
                  args.service_area, args.enterprise_project_id):
        if value:
            list_cdn.guard_write_intent(value)


def run(args):
    """Execute the query → export → upload pipeline; return a result dict."""
    domains = list_cdn.list_domains(
        args.region,
        domain_name=args.domain_name,
        business_type=args.business_type,
        domain_status=args.domain_status,
        service_area=args.service_area,
        enterprise_project_id=args.enterprise_project_id,
        limit=args.page_size,
    )

    local_path, _content = export_results.export(
        domains, fmt=args.format, output=args.output, region=args.region,
        summary=args.summary)

    result = {
        "region": args.region,
        "domain_count": len(domains),
        "format": args.format,
        "local_path": os.path.abspath(local_path),
        "upload": None,
    }

    if args.export_only or not args.bucket:
        result["upload"] = {
            "skipped": True,
            "reason": ("--export-only" if args.export_only
                       else "未指定 OBS 桶（--bucket），仅做本地导出"),
        }
        return result

    key = args.key or os.path.basename(local_path)
    upload = upload_obs.upload_file(
        args.region, local_path, args.bucket, key,
        endpoint=args.endpoint, overwrite=args.overwrite,
        verify=not args.no_verify,
    )
    result["upload"] = upload
    return result


def _render_human(result):
    lines = []
    lines.append("Region %s 的 CDN 加速域名列表（共 %d 个）已导出：%s"
                 % (result["region"], result["domain_count"], result["local_path"]))
    upload = result.get("upload") or {}
    if upload.get("skipped"):
        lines.append("OBS 上传：已跳过（%s）。" % upload.get("reason"))
    else:
        action = "已覆盖" if upload.get("overwritten") else "已上传"
        lines.append("%s到 %s（via %s）"
                     % (action, upload.get("object_url"), upload.get("uploaded_via")))
        verified = upload.get("verified")
        if verified:
            if verified.get("size_match") is True:
                lines.append("回读校验：对象存在，大小一致（%s 字节）。"
                             % verified.get("size"))
            elif verified.get("size") is None:
                lines.append("回读校验：对象存在。")
            else:
                lines.append("回读校验：对象存在，大小 %s。" % verified.get("size"))
        else:
            lines.append("回读校验：未执行。")
    return "\n".join(lines)


def main(argv=None):
    raw_argv = argv if argv is not None else sys.argv[1:]
    parser = _build_parser()
    args = parser.parse_args(argv)

    try:
        _guard(args, raw_argv)
        result = run(args)
    except (list_cdn.CdnListError, export_results.ExportError,
            upload_obs.ObsError) as exc:
        print("[错误] %s" % exc, file=sys.stderr)
        return 1

    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_render_human(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())