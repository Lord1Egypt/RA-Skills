#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Huawei Cloud CES (Cloud Eye Service) Query Skill.

Queries CES monitoring metrics and metric data via the hcloud CLI.
Read-only operations only (ListMetrics / ShowMetricData). Authentication
uses AK/SK read dynamically from environment variables (never hardcoded).

Subcommands:
  list             List monitoring metrics with optional filters.
  show             Query monitoring metric data points for a specified period.
  capability-list  Print the capabilities supported by this skill.

Output: JSON to stdout (all API fields preserved).
Errors: JSON to stderr with non-zero exit codes.
"""

import argparse
import json
import os
import subprocess
import sys
import time

EXIT_OK = 0
EXIT_INVALID_INPUT = 2
EXIT_AK_SK_MISSING = 3
EXIT_API_ERROR = 4

HCLOUD_TIMEOUT = 30
DEFAULT_REGION = "cn-north-4"
VALID_FILTERS = ["average", "variance", "min", "max", "sum"]
VALID_PERIODS = [1, 60, 300, 1200, 3600, 14400, 86400]
VALID_ORDERS = ["asc", "desc"]


def _load_credentials():
    """Dynamically scan environment variables for AK/SK.

    No hardcoded variable names — matches any HUAWEI*/HW*/HWC* env var
    whose name contains ACCESS_KEY / SECRET_KEY or ends with _AK / _SK.
    """
    ak, sk = "", ""
    for key, val in os.environ.items():
        upper = key.upper()
        if not (upper.startswith("HUAWEI") or upper.startswith("HW") or upper.startswith("HWC")):
            continue
        if "ACCESS_KEY" in upper or upper.endswith("_AK") or upper == "AK":
            ak = val or ak
        if "SECRET_KEY" in upper or upper.endswith("_SK") or upper == "SK":
            sk = val or sk
    return ak, sk


def _emit_error(message, code=EXIT_API_ERROR, details=None):
    """Print a JSON error object to stderr and exit."""
    payload = {"error": message}
    if details is not None:
        payload["details"] = details
    json.dump(payload, sys.stderr, ensure_ascii=False)
    sys.stderr.write("\n")
    sys.exit(code)


def _parse_first_json(text):
    """Parse the first JSON object from text.

    hcloud may append diagnostic text after the JSON body on API errors,
    so a plain json.loads can fail. Fall back to raw_decode to grab just
    the leading JSON object.
    """
    if not text:
        return None
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    try:
        decoder = json.JSONDecoder()
        obj, _ = decoder.raw_decode(text)
        return obj
    except (json.JSONDecodeError, ValueError):
        return None


def _handle_api_error(err):
    """Emit an appropriate error for an hcloud API error object."""
    if isinstance(err, dict):
        msg = str(err.get("message", ""))
        code = str(err.get("code", ""))
    else:
        msg = str(err)
        code = ""
    blob = (msg + " " + code).lower()
    if any(s in blob for s in ("could not be found", "not found", "not exist", "404")):
        _emit_error(
            "Metric not found. The specified metric or dimension does not exist "
            "or is not accessible in this region.",
            code=EXIT_INVALID_INPUT,
            details=msg,
        )
    if any(s in blob for s in ("unauthorized", "invalid ak", "401", "forbidden", "403")):
        _emit_error(
            "Authentication failed. AK/SK is invalid or lacks CES read permission.",
            code=EXIT_AK_SK_MISSING,
            details=msg,
        )
    _emit_error("API call failed: %s" % (msg or code), code=EXIT_API_ERROR, details=code)


def _run_hcloud(service, operation, params):
    """Invoke hcloud CLI with AK/SK injected from the environment.

    Returns the parsed JSON response. Exits with an error on failure.

    hcloud may return exit 0 even on API errors, placing the error JSON in
    stdout (optionally followed by diagnostic text). We parse the first JSON
    object and inspect it for an "error" key before trusting the response.
    """
    ak, sk = _load_credentials()
    if not ak or not sk:
        _emit_error(
            "AK/SK credentials missing. Set Huawei Cloud AK and SK as "
            "environment variables (e.g. HUAWEICLOUD_SDK_AK / HUAWEICLOUD_SDK_SK) and retry.",
            code=EXIT_AK_SK_MISSING,
        )

    cmd = [
        "hcloud", service, operation,
        "--cli-access-key=" + ak,
        "--cli-secret-key=" + sk,
    ] + params

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=HCLOUD_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        _emit_error(
            "hcloud CLI timed out after %d seconds." % HCLOUD_TIMEOUT,
            code=EXIT_API_ERROR,
        )
    except FileNotFoundError:
        _emit_error(
            "hcloud CLI not found. Install KooCLI (see references/cli-installation-guide.md).",
            code=EXIT_API_ERROR,
        )

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()

    parsed = _parse_first_json(stdout)

    if isinstance(parsed, dict) and "error" in parsed:
        _handle_api_error(parsed["error"])

    if proc.returncode != 0:
        combined = stderr or stdout
        lower = combined.lower()
        if any(s in lower for s in ("not found", "not exist", "could not be found", "404")):
            _emit_error(
                "Metric not found. The specified metric or dimension does not exist "
                "or is not accessible in this region.",
                code=EXIT_INVALID_INPUT,
                details=combined[:500],
            )
        if any(s in lower for s in ("unauthorized", "invalid ak", "401", "forbidden", "403")):
            _emit_error(
                "Authentication failed. AK/SK is invalid or lacks CES read permission.",
                code=EXIT_AK_SK_MISSING,
                details=combined[:500],
            )
        _emit_error(
            "hcloud CLI failed (exit %d)." % proc.returncode,
            code=EXIT_API_ERROR,
            details=combined[:500],
        )

    if parsed is None:
        if not stdout:
            return {}
        _emit_error(
            "hcloud returned non-JSON output.",
            code=EXIT_API_ERROR,
            details=stdout[:500],
        )

    return parsed


def _validate_dimension(dim_str, position):
    """Validate a dimension string in key,value format."""
    if not dim_str:
        return None
    if "," not in dim_str:
        _emit_error(
            "Invalid dimension format for dim.%d. Expected 'key,value' (e.g. instance_id,xxx)." % position,
            code=EXIT_INVALID_INPUT,
        )
    parts = dim_str.split(",", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        _emit_error(
            "Invalid dimension format for dim.%d. Key and value must be non-empty." % position,
            code=EXIT_INVALID_INPUT,
        )
    return dim_str


def cmd_list(args):
    """List monitoring metrics with optional filters."""
    params = ["--cli-region=" + args.region]

    if args.namespace:
        params.append("--namespace=" + args.namespace)
    if args.metric_name:
        params.append("--metric_name=" + args.metric_name)
    if args.dim_0:
        validated = _validate_dimension(args.dim_0, 0)
        if validated:
            params.append("--dim.0=" + validated)
    if args.dim_1:
        validated = _validate_dimension(args.dim_1, 1)
        if validated:
            params.append("--dim.1=" + validated)
    if args.dim_2:
        validated = _validate_dimension(args.dim_2, 2)
        if validated:
            params.append("--dim.2=" + validated)
    if args.dim_3:
        validated = _validate_dimension(args.dim_3, 3)
        if validated:
            params.append("--dim.3=" + validated)
    if args.order:
        params.append("--order=" + args.order)
    if args.limit is not None:
        params.append("--limit=" + str(args.limit))
    if args.start:
        params.append("--start=" + args.start)

    result = _run_hcloud("CES", "ListMetrics", params)
    if isinstance(result, dict) and "metrics" in result:
        metrics = result.get("metrics") or []
        meta_data = result.get("meta_data", {})
        output = {
            "count": meta_data.get("count", len(metrics)),
            "total": meta_data.get("total", len(metrics)),
            "marker": meta_data.get("marker", ""),
            "metrics": metrics,
        }
    else:
        output = {"count": 0, "total": 0, "marker": "", "metrics": []}
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return EXIT_OK


def cmd_show(args):
    """Query monitoring metric data points for a specified period."""
    params = ["--cli-region=" + args.region]

    validated_dim = _validate_dimension(args.dim_0, 0)
    if validated_dim:
        params.append("--dim.0=" + validated_dim)
    if args.dim_1:
        validated = _validate_dimension(args.dim_1, 1)
        if validated:
            params.append("--dim.1=" + validated)
    if args.dim_2:
        validated = _validate_dimension(args.dim_2, 2)
        if validated:
            params.append("--dim.2=" + validated)
    if args.dim_3:
        validated = _validate_dimension(args.dim_3, 3)
        if validated:
            params.append("--dim.3=" + validated)

    params.append("--namespace=" + args.namespace)
    params.append("--metric_name=" + args.metric_name)
    params.append("--filter=" + args.filter)
    params.append("--period=" + str(args.period))
    params.append("--from=" + str(args.from_ts))
    params.append("--to=" + str(args.to_ts))

    result = _run_hcloud("CES", "ShowMetricData", params)
    if isinstance(result, dict):
        output = {
            "metric_name": result.get("metric_name", args.metric_name),
            "datapoints": result.get("datapoints") or [],
        }
    else:
        output = {"metric_name": args.metric_name, "datapoints": []}
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return EXIT_OK


CAPABILITIES = [
    {
        "operation": "list",
        "description": "List monitoring metrics with optional filters.",
        "filters": [
            "region", "namespace", "metric_name", "dim.0", "dim.1",
            "dim.2", "dim.3", "order", "limit", "start",
        ],
        "readonly": True,
        "api": "CES ListMetrics (GET /v2/{project_id}/metrics)",
    },
    {
        "operation": "show",
        "description": "Query monitoring metric data points for a specified period.",
        "params": [
            "namespace (required)", "metric_name (required)", "dim.0 (required)",
            "filter (required)", "period (required)", "from (required)",
            "to (required)", "region", "dim.1", "dim.2", "dim.3",
        ],
        "readonly": True,
        "api": "CES ShowMetricData (GET /v2/{project_id}/metric-data)",
    },
]


def cmd_capability_list(args):
    """Print supported capabilities."""
    output = {
        "skill": "huawei-cloud-ces-list",
        "service": "CES",
        "mode": "CLI (hcloud)",
        "operations": CAPABILITIES,
    }
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return EXIT_OK


def build_parser():
    parser = argparse.ArgumentParser(
        prog="huawei-cloud-ces-list",
        description="Query Huawei Cloud CES monitoring metrics (list / show). "
                    "Read-only. JSON output with all fields.",
    )
    sub = parser.add_subparsers(dest="command", metavar="{list|show|capability-list}")

    p_list = sub.add_parser("list", help="List monitoring metrics with optional filters.")
    p_list.add_argument("--region", default=DEFAULT_REGION,
                        help="Region (default: %s)." % DEFAULT_REGION)
    p_list.add_argument("--namespace",
                        help="Service namespace (e.g. SYS.ECS, SYS.OBS).")
    p_list.add_argument("--metric-name", dest="metric_name",
                        help="Metric name (e.g. cpu_util, capacity_archive).")
    p_list.add_argument("--dim.0", dest="dim_0",
                        help="First dimension, format: key,value (e.g. instance_id,xxx).")
    p_list.add_argument("--dim.1", dest="dim_1",
                        help="Second dimension, format: key,value.")
    p_list.add_argument("--dim.2", dest="dim_2",
                        help="Third dimension, format: key,value.")
    p_list.add_argument("--dim.3", dest="dim_3",
                        help="Fourth dimension, format: key,value.")
    p_list.add_argument("--order", choices=VALID_ORDERS,
                        help="Sort order: asc or desc (default: asc).")
    p_list.add_argument("--limit", type=int,
                        help="Max results per page (1-1000, default 1000).")
    p_list.add_argument("--start",
                        help="Pagination marker from previous response.")
    p_list.set_defaults(func=cmd_list)

    p_show = sub.add_parser("show", help="Query monitoring metric data points.")
    p_show.add_argument("--region", default=DEFAULT_REGION,
                        help="Region (default: %s)." % DEFAULT_REGION)
    p_show.add_argument("--namespace", required=True,
                        help="Service namespace (e.g. SYS.ECS, SYS.OBS).")
    p_show.add_argument("--metric-name", required=True, dest="metric_name",
                        help="Metric name (e.g. cpu_util).")
    p_show.add_argument("--dim.0", required=True, dest="dim_0",
                        help="First dimension, format: key,value (e.g. instance_id,xxx).")
    p_show.add_argument("--dim.1", dest="dim_1",
                        help="Second dimension, format: key,value.")
    p_show.add_argument("--dim.2", dest="dim_2",
                        help="Third dimension, format: key,value.")
    p_show.add_argument("--dim.3", dest="dim_3",
                        help="Fourth dimension, format: key,value.")
    p_show.add_argument("--filter", required=True, choices=VALID_FILTERS,
                        help="Aggregation method: average/variance/min/max/sum.")
    p_show.add_argument("--period", required=True, type=int, choices=VALID_PERIODS,
                        help="Aggregation granularity (seconds): 1/60/300/1200/3600/14400/86400.")
    p_show.add_argument("--from", required=True, type=int, dest="from_ts",
                        help="Start time (UNIX timestamp in milliseconds).")
    p_show.add_argument("--to", required=True, type=int, dest="to_ts",
                        help="End time (UNIX timestamp in milliseconds).")
    p_show.set_defaults(func=cmd_show)

    p_cap = sub.add_parser("capability-list", help="List supported operations.")
    p_cap.set_defaults(func=cmd_capability_list)

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return EXIT_OK
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
