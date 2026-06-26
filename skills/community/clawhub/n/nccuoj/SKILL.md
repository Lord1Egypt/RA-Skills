---
name: nccuoj
description: "Solve competitive programming problems on NCCUOJ (https://nccuoj.ebg.tw). Use when: solving OJ problems, reading problem statements, writing solutions in C/C++/Python, submitting code, checking submission results."
argument-hint: "Problem ID or URL (e.g. '1001' or 'https://nccuoj.ebg.tw/problem/1001')"
---

# NCCUOJ Problem Solving

Solve competitive programming problems on [NCCUOJ](https://nccuoj.ebg.tw), a QDU-based Online Judge for NCCU CS.

## When to Use

- Read a problem statement from NCCUOJ
- Write a solution for a specific problem
- Submit code and check results
- Debug a wrong answer or time limit exceeded
- Solve contest problems

## Directory Structure

All generated files are organized under `.nccuoj/` at the workspace root:

```
.nccuoj/
├── cookies.txt                                  # Session cookies (auto-managed)
└── solution/
    ├── public/<problem_id>/                      # Public problem solutions
    │   ├── problem.md                            # Problem statement
    │   └── solution.cpp / solution.py / ...      # Solution code
    └── contest/<contest_id>/<problem_id>/        # Contest problem solutions
        ├── problem.md
        └── solution.cpp / solution.py / ...
```

**When writing solution code, always place files in the correct directory.** The scripts' `--save` flag and `get_solution_dir()` helper handle directory creation automatically.

## CSRF Token (Important)

All NCCUOJ API requests require a CSRF token. The provided scripts handle this automatically (via `GET /api/profile` on init). If making manual requests, see [./references/api.md](./references/api.md) for details.

## Scripts

Use these scripts to interact with NCCUOJ. They handle CSRF tokens and session management automatically.

| Script | Purpose |
|--------|--------|
| [get_problem.py](./scripts/get_problem.py) | Fetch problem statement as Markdown (supports `--username`/`--password`, `--contest`, `--raw`) |
| [submit.py](./scripts/submit.py) | Submit code (requires `--username` / `--password` CLI args) |
| [check_result.py](./scripts/check_result.py) | Check submission result, with optional `--poll` |

All scripts use only Python stdlib (no pip install needed).

Scripts are located in this skill's `./scripts/` directory. In the examples below, `$SCRIPTS` refers to the absolute path of that directory. Resolve it relative to this SKILL.md file before running commands.

## Mode A: Public Problem Solving

### 1. Fetch the Problem

Run [get_problem.py](./scripts/get_problem.py) to fetch the problem. **If the problem requires login (e.g. returns "Please login first"), ask the user for their credentials and pass `--username`/`--password`.**

```bash
# Public (no login)
python $SCRIPTS/get_problem.py <problem_id>

# With login
python $SCRIPTS/get_problem.py <problem_id> --username <username> --password <password>
```

Or if given a URL like `https://nccuoj.ebg.tw/problem/1001`, extract `1001` and pass it as the argument.

The output is **formatted Markdown** containing: title, metadata (internal ID, difficulty, time/memory limit, tags), description, input/output format, sample test cases, hint, allowed languages, and statistics. All URL-encoded HTML fields are automatically decoded and converted to Markdown.

Use `--raw` to get the original JSON instead.

### 2. Analyze the Problem

- Identify input/output format from `input_description` and `output_description`
- Study sample cases from `samples`
- Determine constraints (time/memory limits)
- Identify the algorithm or data structure needed

### 3. Write the Solution

Write the solution file in the correct directory:
- **Public**: `.nccuoj/solution/public/<problem_id>/solution.cpp` (or `.py`, `.java`, etc.)
- **Contest**: `.nccuoj/solution/contest/<contest_id>/<problem_id>/solution.cpp`

The supported languages are:

| Language   | API Name      | Notes         |
|------------|---------------|---------------|
| C          | `C`           | GCC, C17      |
| C++        | `C++`         | GCC, C++20    |
| Python     | `Python3`     | Python 3.12   |
| Java       | `Java`        | Temurin 21    |
| Go         | `Golang`      | Go 1.22       |
| JavaScript | `JavaScript`  | Node.js 20    |

**Default to C++ unless the user specifies otherwise.**

#### C/C++ Template

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    // solution
    return 0;
}
```

#### Python Template

```python
import sys
input = sys.stdin.readline

def solve():
    # solution
    pass

solve()
```

### 4. Test Locally

Before submitting, verify the solution against the sample cases. Run the code with each sample input and compare to expected output.

### 5. Submit (Optional)

**Before submitting, if the user has not provided their NCCUOJ username and password, ask them for it.** Then pass the credentials directly as CLI arguments.

```bash
# Submit (problem_id is the internal numeric ID from the problem JSON's "id" field)
python $SCRIPTS/submit.py <problem_internal_id> "C++" .nccuoj/solution/public/<problem_id>/solution.cpp --username <username> --password <password>

# Check result (with --poll to wait for judging)
python $SCRIPTS/check_result.py <submission_id> --username <username> --password <password> --poll
```

Result codes: `-2` (Compile Error), `-1` (Wrong Answer), `0` (Accepted), `1` (Time Limit Exceeded), `2` (Memory Limit Exceeded), `3` (Runtime Error), `4` (System Error), `6` (Pending), `7` (Judging), `8` (Partial Accepted).

### 6. Debug if Needed

If the submission is not Accepted:

- **Wrong Answer**: Re-examine edge cases, off-by-one errors, output format
- **Time Limit Exceeded**: Optimize algorithm complexity, reduce I/O overhead
- **Runtime Error**: Check array bounds, division by zero, stack overflow
- **Compile Error**: Check the error info in submission response
- **Memory Limit Exceeded**: Reduce data structure size, avoid unnecessary copies

## Mode B: Contest Problem Solving

Contest mode mirrors public mode but all API calls require the `contest_id` parameter.

### 1. Fetch Contest Problem

Run [get_problem.py](./scripts/get_problem.py) with `--contest`. **Contest problems always require login.**

```bash
python $SCRIPTS/get_problem.py <problem_id> --contest <contest_id> --username <username> --password <password>
```

The response format is the same as public problems.

### 2–4. Analyze, Write, Test

Same as Mode A steps 2–4.

### 5. Submit to Contest

**Before submitting, if the user has not provided their NCCUOJ username and password, ask them for it.**

```bash
python $SCRIPTS/submit.py <problem_internal_id> "C++" .nccuoj/solution/contest/<contest_id>/<problem_id>/solution.cpp --username <username> --password <password> --contest <contest_id>

# Check result
python $SCRIPTS/check_result.py <submission_id> --username <username> --password <password> --poll
```

### 7. Debug if Needed

Same as Mode A step 6. Note: contest submissions **cannot be shared** while the contest is underway.

## API Reference

See [./references/api.md](./references/api.md) for full API endpoint documentation.
