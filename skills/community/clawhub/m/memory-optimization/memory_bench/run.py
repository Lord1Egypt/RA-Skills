#!/usr/bin/env python3
"""Main benchmark runner."""

import argparse
from memory_bench.agents.nanobot_base import run as run_base
from memory_bench.agents.nanobot_with_memory import run as run_with_memory
from memory_bench.report import generate


def main():
    parser = argparse.ArgumentParser(description="Memory optimization benchmark")
    parser.add_argument("task", help="Task description")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout in seconds")
    args = parser.parse_args()

    print("Running baseline (nanobot native memory)...")
    base_result = run_base(args.task, args.timeout)

    print("Running with memory-optimization skill...")
    memory_result = run_with_memory(args.task, args.timeout)

    report = generate(base_result, memory_result, args.task)
    print(report)


if __name__ == "__main__":
    main()
