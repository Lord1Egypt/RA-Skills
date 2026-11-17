# CPU Parallelism Playbook

How to keep all cores busy for builds, tests, and data processing.

## Rule of thumb

- Worker count: 75-90% of logical cores leaves headroom for the system.
- Thread budget: N processes x T threads must satisfy N x T <= logical
  cores. When N > 1, set `OMP_NUM_THREADS=1` and `MKL_NUM_THREADS=1` in
  each worker, otherwise BLAS/OpenMP libraries inside every worker spawn
  `nproc` threads and the machine thrashes.

## Builds

```bash
# CMake / Make
cmake --build build -j"$(nproc)"
make -j"$(nproc)"

# Rust
cargo build --jobs "$(nproc)"

# Go (GOMAXPROCS defaults to core count; set for containers)
GOMAXPROCS="$(nproc)" go test ./...

# C# / .NET
dotnet build -m:"$(nproc)"

# Windows (PowerShell): nproc is also a cmdlet
cmake --build build -j (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
```

## Test suites

```bash
# Python - install pytest-xdist once, then
pytest -n auto --dist loadgroup     # loadgroup keeps xdist_group tests together
pytest -n auto                      # independent tests

# Rust
cargo nextest run -j "$(nproc)"     # nextest runs each test in its own process

# JS/TS (Jest / Vitest default to worker pools; make sure not to force -i)
npx jest --maxWorkers="75%"
npx vitest --pool=threads --poolSize="$(nproc)"
```

If a suite cannot be parallelized due to shared state (a database, ports,
global temp dirs), shard it by directory or marker instead:

```bash
pytest -n auto -m "not requires_db"
```

## Data preprocessing / file transformation

Shard by file and process concurrently:

```bash
# GNU parallel
ls chunks/*.json | parallel -j"$(nproc)" python process_one.py {}

# xargs alternative
find chunks -name '*.json' | xargs -P "$(nproc)" -I{} python process_one.py {}
```

Pure Python with multiprocessing (use it for CPU-bound work; threads only
help for I/O-bound work due to the GIL):

```python
from concurrent.futures import ProcessPoolExecutor
import os

def process_file(path: str) -> str:
    ...

with ProcessPoolExecutor(max_workers=int(os.cpu_count() * 0.75)) as pool:
    results = list(pool.map(process_file, input_paths))
```

Chunk very large single files by byte ranges or line counts so workers
share the load instead of one worker reading everything.

## Downloads

```bash
aria2c -x 16 -s 16 -i urls.txt          # multi-connection per file
cat urls.txt | xargs -P 8 -n 1 curl -LO # many files concurrently
```

## Verification

After launching, confirm the parallelism actually engaged:

```bash
top -b -n 1 | head -5          # load average ~ logical core count
htop                            # visual per-core view
```

Linux: load average near logical core count = saturated. Far below = still
serial somewhere; find the bottleneck before waiting.
