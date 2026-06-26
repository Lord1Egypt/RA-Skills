#!/usr/bin/env python3
"""Heuristic scanner for common NVIDIA training-stack anti-patterns."""

from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


PYTHON_EXTENSIONS = {".py"}
TEXT_EXTENSIONS = {
    ".py",
    ".cu",
    ".cuh",
    ".cpp",
    ".cc",
    ".cxx",
    ".h",
    ".hpp",
    ".hxx",
    ".yaml",
    ".yml",
    ".sh",
}


TEXT_RULES = [
    (
        re.compile(r"\bcudaDeviceSynchronize\s*\("),
        "warning",
        "cuda-device-synchronize",
        "Potential full-device synchronization. Verify it is not in a hot path.",
    ),
    (
        re.compile(r"\bcudaMemcpy(?:Async)?\s*\("),
        "info",
        "cuda-memcpy",
        "CUDA memcpy detected. Verify transfer placement and overlap behavior.",
    ),
    (
        re.compile(r"\bNCCL_DEBUG\s*="),
        "info",
        "nccl-debug-env",
        "NCCL_DEBUG is set in this file. Confirm it is intended beyond debugging.",
    ),
    (
        re.compile(r"@triton\.jit"),
        "info",
        "triton-kernel",
        "Triton kernel detected. Review masking, launch parameters, and validation strategy.",
    ),
    (
        re.compile(r"\b(?:tl|triton\.language)\.load\s*\("),
        "info",
        "triton-load",
        "Triton load detected. Verify masks and bounds assumptions when shapes are ragged.",
    ),
    (
        re.compile(r"\b(?:tl|triton\.language)\.store\s*\("),
        "info",
        "triton-store",
        "Triton store detected. Verify masks and bounds assumptions when shapes are ragged.",
    ),
    (
        re.compile(r"\b(?:tl|triton\.language)\.(?:device_print|device_assert|static_print|static_assert)\s*\("),
        "info",
        "triton-debug-op",
        "Triton debug op detected. Confirm it is not left in a performance path.",
    ),
    (
        re.compile(r"\btorch\.cuda\.amp\b"),
        "warning",
        "deprecated-amp-text",
        "Deprecated torch.cuda.amp usage detected in source text.",
    ),
]


@dataclass
class Finding:
    path: str
    line: int
    severity: str
    code: str
    message: str


def iter_files(paths: Iterable[str]) -> list[Path]:
    files: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_file() and path.suffix in TEXT_EXTENSIONS:
            files.append(path)
            continue
        if path.is_dir():
            files.extend(
                sorted(
                    p
                    for p in path.rglob("*")
                    if p.is_file() and p.suffix in TEXT_EXTENSIONS and ".git" not in p.parts
                )
            )
    return files


def dotted_name(node: ast.AST) -> str:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return ".".join(reversed(parts))


class PythonScanner(ast.NodeVisitor):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.findings: list[Finding] = []
        self.loop_depth = 0
        self.seen_compile = False
        self.seen_autocast = False
        self.seen_sdpa = False
        self.seen_fsdp = False
        self.seen_ddp = False

    def add(self, node: ast.AST, severity: str, code: str, message: str) -> None:
        self.findings.append(
            Finding(str(self.path), getattr(node, "lineno", 1), severity, code, message)
        )

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name = alias.name
            if name == "torch.cuda.amp" or name.startswith("torch.cuda.amp."):
                self.add(node, "warning", "deprecated-amp", "Use torch.amp APIs instead of torch.cuda.amp.")
            lowered = name.lower()
            if "fsdp" in lowered:
                self.seen_fsdp = True
            if "distributeddataparallel" in lowered:
                self.seen_ddp = True
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        module = node.module or ""
        if module == "torch.cuda.amp" or module.startswith("torch.cuda.amp."):
            self.add(node, "warning", "deprecated-amp", "Use torch.amp APIs instead of torch.cuda.amp.")
        lowered = module.lower()
        if "fsdp" in lowered:
            self.seen_fsdp = True
        if "distributeddataparallel" in lowered or module == "torch.nn.parallel":
            for alias in node.names:
                if alias.name == "DistributedDataParallel":
                    self.seen_ddp = True
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_While(self, node: ast.While) -> None:
        self.loop_depth += 1
        self.generic_visit(node)
        self.loop_depth -= 1

    def visit_Call(self, node: ast.Call) -> None:
        name = dotted_name(node.func)

        if name.endswith("DataLoader"):
            self.scan_dataloader(node)
        if name == "torch.compile" or name.endswith(".compile"):
            self.seen_compile = True
        if name.endswith("autocast"):
            self.seen_autocast = True
        if name.endswith("scaled_dot_product_attention"):
            self.seen_sdpa = True
        if "FullyShardedDataParallel" in name or name.endswith(".FSDP"):
            self.seen_fsdp = True
        if "DistributedDataParallel" in name or name.endswith(".DDP"):
            self.seen_ddp = True
        if "checkpoint" in name:
            self.add(
                node,
                "info",
                "checkpoint-detected",
                "Checkpointing detected. Verify FSDP/ZeRO-style sharding was evaluated first.",
            )
        if self.loop_depth > 0 and isinstance(node.func, ast.Attribute):
            attr = node.func.attr
            if attr in {"item", "cpu", "numpy"}:
                self.add(
                    node,
                    "warning",
                    f"host-sync-{attr}",
                    f"Potential host synchronization via .{attr}() inside a loop.",
                )

        self.generic_visit(node)

    def scan_dataloader(self, node: ast.Call) -> None:
        keywords = {kw.arg: kw.value for kw in node.keywords if kw.arg}

        if "pin_memory" not in keywords:
            self.add(node, "warning", "dataloader-pin-memory", "DataLoader is missing pin_memory=... for CUDA feeding.")
        elif isinstance(keywords["pin_memory"], ast.Constant) and keywords["pin_memory"].value is False:
            self.add(node, "warning", "dataloader-pin-memory", "DataLoader explicitly disables pin_memory.")

        if "num_workers" not in keywords:
            self.add(node, "info", "dataloader-workers", "DataLoader does not set num_workers explicitly.")

        if "persistent_workers" not in keywords:
            self.add(node, "info", "dataloader-persistent-workers", "DataLoader does not set persistent_workers explicitly.")
        elif isinstance(keywords["persistent_workers"], ast.Constant) and keywords["persistent_workers"].value is False:
            self.add(node, "info", "dataloader-persistent-workers", "DataLoader disables persistent_workers.")

        if "prefetch_factor" not in keywords:
            self.add(node, "info", "dataloader-prefetch", "DataLoader does not set prefetch_factor explicitly.")


def scan_python_file(path: Path) -> list[Finding]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        return [Finding(str(path), exc.lineno or 1, "error", "syntax-error", str(exc))]

    scanner = PythonScanner(path)
    scanner.visit(tree)
    if not scanner.seen_compile:
        scanner.findings.append(
            Finding(str(path), 1, "info", "compile-not-seen", "No torch.compile usage found in this file.")
        )
    if not scanner.seen_autocast:
        scanner.findings.append(
            Finding(str(path), 1, "info", "autocast-not-seen", "No autocast usage found in this file.")
        )
    if not scanner.seen_sdpa:
        scanner.findings.append(
            Finding(str(path), 1, "info", "sdpa-not-seen", "No scaled_dot_product_attention usage found in this file.")
        )
    if any(f.code == "checkpoint-detected" for f in scanner.findings) and not scanner.seen_fsdp:
        scanner.findings.append(
            Finding(
                str(path),
                1,
                "info",
                "fsdp-not-seen",
                "Checkpointing appears in this file, but no FSDP marker was found nearby.",
            )
        )
    if scanner.seen_ddp and not scanner.seen_fsdp:
        scanner.findings.append(
            Finding(
                str(path),
                1,
                "info",
                "ddp-detected",
                "DDP detected. Confirm the model actually fits per rank and does not want FSDP instead.",
            )
        )
    return scanner.findings


def scan_text_file(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError as exc:
        return [Finding(str(path), 1, "error", "read-error", str(exc))]

    for lineno, line in enumerate(lines, start=1):
        for pattern, severity, code, message in TEXT_RULES:
            if pattern.search(line):
                findings.append(Finding(str(path), lineno, severity, code, message))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    findings: list[Finding] = []
    for path in iter_files(args.paths):
        findings.extend(scan_text_file(path))
        if path.suffix in PYTHON_EXTENSIONS:
            findings.extend(scan_python_file(path))

    findings.sort(key=lambda item: (item.path, item.line, item.code))
    if args.json:
        print(json.dumps([asdict(finding) for finding in findings], indent=2))
        return 0

    for finding in findings:
        print(
            f"{finding.path}:{finding.line}: {finding.severity.upper()} {finding.code} - {finding.message}"
        )
    print(f"\nTotal findings: {len(findings)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
