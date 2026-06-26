"""Generate text comparison report."""


def generate(base_result: tuple, memory_result: tuple, task: str) -> str:
    base_duration, base_response = base_result
    mem_duration, mem_response = memory_result
    diff = base_duration - mem_duration
    diff_pct = (diff / base_duration) * 100 if base_duration > 0 else 0

    return f"""
# Benchmark Report: {task}

## nanobot native memory
Duration: {base_duration:.2f}s
Response: {base_response[:200]}...

## nanobot + memory-optimization skill
Duration: {mem_duration:.2f}s
Response: {mem_response[:200]}...

## Comparison
Time saved: {diff:.2f}s ({diff_pct:.1f}%)
Faster: {"memory-optimization" if diff > 0 else "native memory"}
"""
