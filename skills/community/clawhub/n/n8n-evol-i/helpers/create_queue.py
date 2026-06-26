#!/usr/bin/env python3
"""Copy queue primitive templates from harness/primitives into the workspace and register them."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from helpers.workspace import workspace_root
# Import the lock helpers' generic primitive-copy + create-workflow registration
# functions directly. They are key-agnostic (each takes a `key` argument), so
# duplicating them into a queue-specific module would buy nothing. Marked as
# leading-underscore for cohesion within create_lock.py's module, but Python
# doesn't enforce privacy and these are the canonical implementations.
# Refactor target: extract `_copy_primitive` + `_register_via_create_workflow`
# into `helpers/_primitive_install.py` so create_lock + create_queue both import
# from a shared module instead of one importing from the other.
from helpers.create_lock import _copy_primitive, _register_via_create_workflow


_PRIMITIVES = {
    "queue_publish": "Queue Publish",
    "queue_pop": "Queue Pop",
    "queue_ack": "Queue Ack",
}
_ERROR_HANDLER = ("error_handler_queue_cleanup", "Error Handler Queue Cleanup")
# Sample-test pair: a webhook-triggered producer that publishes 5 tagged messages
# (3 happy / 1 transient_fail_once / 1 poison) and a schedule-polled consumer
# that simulates per-tag behaviour. Together they exercise XAUTOCLAIM retry,
# the semaphore cap, and DLQ routing — without the operator hand-writing test
# scaffolding. Tier 1 (callers) since they invoke the queue primitives.
_SAMPLE_TEST = {
    "queue_sample_producer": "Queue Sample Producer",
    "queue_sample_consumer": "Queue Sample Consumer",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--include-error-handler", action="store_true", dest="include_error_handler")
    parser.add_argument("--with-sample-test", action="store_true", dest="with_sample_test",
                        help="Also copy a paired producer+consumer test that exercises happy / "
                             "transient-retry / poison-DLQ paths against a 'test-stream'. Useful for "
                             "first-time end-to-end validation after install.")
    parser.add_argument("--force-overwrite", action="store_true", dest="force_overwrite")
    args = parser.parse_args()

    ws = workspace_root(args.workspace)

    primitives = dict(_PRIMITIVES)
    if args.include_error_handler:
        key, name = _ERROR_HANDLER
        primitives[key] = name

    # Sample-test workflows register at Tier 1 (callers) not Tier 0a, since
    # they depend on the queue primitives being deployed first.
    sample_test = dict(_SAMPLE_TEST) if args.with_sample_test else {}

    # Two-pass copy → register, mirroring create_lock.py. If a registration
    # fails (transient n8n API hiccup, expired key) the workspace still has
    # all template files on disk so a retry can resume cleanly.
    for key in (*primitives.keys(), *sample_test.keys()):
        _copy_primitive(ws, key, force_overwrite=args.force_overwrite)

    failures: list[tuple[str, Exception]] = []
    for key, name in primitives.items():
        try:
            _register_via_create_workflow(ws, key, name, "Tier 0a: leaves")
        except SystemExit as e:
            failures.append((key, e))
            print(f"  WARNING: registration failed for '{key}'; continuing.", file=sys.stderr)
    for key, name in sample_test.items():
        try:
            _register_via_create_workflow(ws, key, name, "Tier 1")
        except SystemExit as e:
            failures.append((key, e))
            print(f"  WARNING: registration failed for '{key}'; continuing.", file=sys.stderr)

    total = len(primitives) + len(sample_test)
    if failures:
        print(
            f"create-queue partial: {total - len(failures)}/{total} registered. "
            f"Re-run after fixing the underlying issue (commonly: invalid N8N_API_KEY).",
            file=sys.stderr,
        )
        sys.exit(1)
    if args.with_sample_test:
        print(
            "create-queue complete. Sample-test workflows installed:\n"
            "  - queue_sample_producer (webhook /queue-sample-producer; publishes 5 tagged messages)\n"
            "  - queue_sample_consumer (schedule 10s; pops + simulates per-tag behaviour)\n"
            "Deploy with deploy_all, then POST to the producer's webhook and watch the consumer drain."
        )
    else:
        print("create-queue complete.")


if __name__ == "__main__":
    main()
