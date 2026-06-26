from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .usage import Usage


def emit_result(
    *,
    tool: str,
    outputs: Iterable[Path],
    usage: Usage,
    json_output: bool,
) -> None:
    outputs_list = [str(p) for p in outputs]
    if json_output:
        payload = {
            "tool": tool,
            "outputs": outputs_list,
            "usage": usage.to_dict(),
        }
        print(json.dumps(payload, indent=2))
        return

    print(f"Tool: {tool}")
    if outputs_list:
        print("Outputs:")
        for out in outputs_list:
            print(f"- {out}")
    print("Usage:")
    _print_usage(usage)


def _print_usage(usage: Usage) -> None:
    print(f"  Success: {usage.success}")
    if usage.error:
        print(f"  Error: {usage.error}")
    print(f"  Duration (ms): {usage.duration_ms}")
    print(f"  CPU (ms): {usage.cpu_ms}")
    print(f"  Bytes in: {usage.bytes_in}")
    print(f"  Bytes out: {usage.bytes_out}")
    if usage.pages_in is not None:
        print(f"  Pages in: {usage.pages_in}")
    if usage.pages_out is not None:
        print(f"  Pages out: {usage.pages_out}")
    if usage.metrics:
        print("  Metrics:")
        for key, value in usage.metrics.items():
            print(f"    {key}: {value}")
