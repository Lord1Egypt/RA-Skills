#!/usr/bin/env python3
"""Evaluate Wolfram Language expressions with exact/numeric output and verification."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from concurrent.futures import TimeoutError as FutureTimeoutError
from dataclasses import dataclass
from typing import Any

EXIT_OK = 0
EXIT_DEPENDENCY = 3
EXIT_EVALUATION = 4

UNSAFE_SYMBOLS = (
    "Import",
    "Export",
    "URLRead",
    "URLExecute",
    "URLFetch",
    "URLSave",
    "Run",
    "RunProcess",
    "StartProcess",
    "Install",
    "Get",
    "Put",
    "OpenRead",
    "OpenWrite",
    "Read",
    "Write",
    "ReadString",
    "BinaryRead",
    "BinaryWrite",
    "DeleteFile",
    "RenameFile",
    "CopyFile",
    "CreateFile",
    "CreateDirectory",
    "SetDirectory",
    "ResetDirectory",
    "SystemOpen",
    "ExternalEvaluate",
    "SocketConnect",
)


class DependencyError(RuntimeError):
    """Raised when runtime dependencies are unavailable."""


class EvaluationError(RuntimeError):
    """Raised when Wolfram evaluation fails."""


class EvaluationTimeoutError(EvaluationError):
    """Raised when Wolfram evaluation exceeds the configured timeout."""


@dataclass
class ResultPayload:
    expr: str
    exact: str
    numeric: str
    verified: bool | None
    precision: int
    version: str
    warnings: list[str]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate a Wolfram Language expression with reliability checks."
    )
    parser.add_argument("--expr", required=True, help="Wolfram Language expression")
    parser.add_argument(
        "--precision",
        type=int,
        default=50,
        help="Numeric precision for N[..., p] (default: 50)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-evaluation timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="as_json",
        help="Emit JSON output",
    )
    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip exact-vs-numeric consistency verification",
    )
    parser.add_argument(
        "--allow-unsafe",
        action="store_true",
        help=(
            "Allow expressions containing filesystem/network/process symbols "
            "(disabled by default for safety)."
        ),
    )

    args = parser.parse_args(argv)

    if not args.expr.strip():
        parser.error("--expr cannot be empty")
    if args.precision <= 0:
        parser.error("--precision must be a positive integer")
    if args.timeout <= 0:
        parser.error("--timeout must be > 0")

    return args


def evaluate_with_timeout(session: Any, expr: Any, timeout: float) -> Any:
    future = session.evaluate_future(expr)
    try:
        return future.result(timeout=timeout)
    except FutureTimeoutError as exc:
        try:
            session.terminate()
        except Exception:
            pass
        raise EvaluationTimeoutError(f"Evaluation exceeded timeout: {timeout}s") from exc


def find_unsafe_symbols(expr_text: str) -> list[str]:
    hits: list[str] = []
    for symbol in UNSAFE_SYMBOLS:
        pattern = rf"(?<![A-Za-z0-9$`]){re.escape(symbol)}(?![A-Za-z0-9$`])"
        if re.search(pattern, expr_text):
            hits.append(symbol)
    return hits


def render_input_form(session: Any, wlexpr: Any, expr_text: str, timeout: float) -> str:
    rendered = evaluate_with_timeout(
        session,
        wlexpr(f"ToString[Evaluate[({expr_text})], InputForm]"),
        timeout,
    )
    return str(rendered)


def verify_consistency(
    session: Any,
    wlexpr: Any,
    expr_text: str,
    precision: int,
    timeout: float,
) -> tuple[bool | None, str | None]:
    tolerance_digits = min(20, max(6, precision // 2))
    verification_expr = (
        "Quiet@Check["
        "Module[{exact = Evaluate[("
        + expr_text
        + ")], numeric = Evaluate[N[("
        + expr_text
        + "), "
        + str(precision)
        + "]], recomputed, diff, vals, tol},"
        "recomputed = N[exact, "
        + str(precision)
        + "];"
        "diff = N[recomputed - numeric, "
        + str(precision)
        + "];"
        "vals = Flatten[{diff}];"
        "tol = 10^(-"
        + str(tolerance_digits)
        + ");"
        "If[AllTrue[vals, NumericQ], Max[Abs[vals]] <= tol, Missing[\"NonNumeric\"]]"
        "],"
        "Missing[\"VerificationFailed\"]"
        "]"
    )

    result = evaluate_with_timeout(session, wlexpr(verification_expr), timeout)
    if isinstance(result, bool):
        return result, None

    as_text = str(result)
    if "NonNumeric" in as_text:
        return None, "Verification skipped: result is not directly numeric-comparable."
    return None, "Verification skipped: consistency check could not be completed."


def build_payload(args: argparse.Namespace) -> ResultPayload:
    if not args.allow_unsafe:
        blocked = find_unsafe_symbols(args.expr)
        if blocked:
            blocked_text = ", ".join(sorted(set(blocked)))
            raise EvaluationError(
                "Expression blocked by safety policy (unsafe symbols detected): "
                f"{blocked_text}. Use --allow-unsafe only in an isolated environment."
            )

    kernel = shutil.which("WolframKernel")
    if not kernel:
        raise DependencyError("WolframKernel not found in PATH.")

    try:
        from wolframclient.evaluation import WolframLanguageSession
        from wolframclient.language import wl, wlexpr
    except Exception as exc:
        raise DependencyError(f"wolframclient is not available: {exc}") from exc

    warnings: list[str] = []

    with WolframLanguageSession(kernel=kernel) as session:
        version = evaluate_with_timeout(session, wlexpr("$Version"), args.timeout)

        exact_value = evaluate_with_timeout(session, wlexpr(args.expr), args.timeout)
        failed_exact = evaluate_with_timeout(
            session,
            wl.SameQ(exact_value, wlexpr("$Failed")),
            args.timeout,
        )
        if bool(failed_exact):
            raise EvaluationError("Exact evaluation returned $Failed (invalid expression or runtime error).")

        numeric_value = evaluate_with_timeout(
            session,
            wl.N(wlexpr(args.expr), args.precision),
            args.timeout,
        )
        failed_numeric = evaluate_with_timeout(
            session,
            wl.SameQ(numeric_value, wlexpr("$Failed")),
            args.timeout,
        )
        if bool(failed_numeric):
            raise EvaluationError("Numeric evaluation returned $Failed (invalid expression or runtime error).")

        verified: bool | None = None
        if args.no_verify:
            warnings.append("Verification disabled by --no-verify.")
        else:
            verified, warning = verify_consistency(
                session=session,
                wlexpr=wlexpr,
                expr_text=args.expr,
                precision=args.precision,
                timeout=args.timeout,
            )
            if warning:
                warnings.append(warning)

        exact_text = render_input_form(session, wlexpr, args.expr, args.timeout)
        numeric_text = render_input_form(
            session,
            wlexpr,
            f"N[({args.expr}), {args.precision}]",
            args.timeout,
        )

        return ResultPayload(
            expr=args.expr,
            exact=exact_text,
            numeric=numeric_text,
            verified=verified,
            precision=args.precision,
            version=str(version),
            warnings=warnings,
        )


def print_text(payload: ResultPayload) -> None:
    print(f"Exact: {payload.exact}")
    print(f"Numeric: {payload.numeric}")
    print(f"Verified: {payload.verified}")
    print(f"Version: {payload.version}")
    if payload.warnings:
        print("Warnings:")
        for item in payload.warnings:
            print(f"- {item}")


def print_json(payload: ResultPayload) -> None:
    print(
        json.dumps(
            {
                "expr": payload.expr,
                "exact": payload.exact,
                "numeric": payload.numeric,
                "verified": payload.verified,
                "precision": payload.precision,
                "version": payload.version,
                "warnings": payload.warnings,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    try:
        payload = build_payload(args)
    except DependencyError as exc:
        print(f"[DEPENDENCY ERROR] {exc}", file=sys.stderr)
        return EXIT_DEPENDENCY
    except EvaluationError as exc:
        print(f"[EVALUATION ERROR] {exc}", file=sys.stderr)
        return EXIT_EVALUATION
    except Exception as exc:
        print(f"[EVALUATION ERROR] {exc}", file=sys.stderr)
        return EXIT_EVALUATION

    if args.as_json:
        print_json(payload)
    else:
        print_text(payload)

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
