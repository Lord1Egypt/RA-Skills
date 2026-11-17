"""Toy autonomous loop — keelwright's circuit-breaker caps runaway iteration."""
import sys
from pathlib import Path

LOG = Path("loop.log")


def step(n: int) -> int:
    return n * 2


def main() -> int:
    val = 1
    for i in range(1000):  # breaker.py should stop this far before 1000
        val = step(val)
        LOG.write_text(f"iter={i} val={val}\n")
        if val > 1_000_000:
            break
    print(f"done at val={val}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
