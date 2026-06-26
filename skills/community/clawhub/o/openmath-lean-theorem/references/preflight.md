# OpenMath Lean Workspace Preflight

Run this immediately after `download_theorem.py` and before writing any proof.

## Command

```bash
python3 scripts/check_theorem_env.py <workspace>
```

Optional:

```bash
python3 scripts/check_theorem_env.py <workspace> --auto-install-skills --install-dir .codex/skills
python3 scripts/check_theorem_env.py <workspace> --skip-build
```

## Lean Flow

The Lean preflight does all of the following:

1. Detects the workspace from `lean-toolchain` / `lakefile.lean`
2. Checks `lean`, `lake`, and `elan`
3. Reads the expected Lean version from `lean-toolchain`
4. Checks that required proof skills are installed:
   - `lean-proof`
   - `mathlib-build`
5. Reports optional debugging/review skills if missing:
   - `lean-mwe`
   - `lean-bisect`
   - `nightly-testing`
   - `mathlib-review`
   - `mathlib-pr`
   - `lean-pr`
   - `lean-setup`
6. If mathlib is required, runs:
   ```bash
   lake exe cache get
   ```
7. Runs:
   ```bash
   lake build -q --log-level=info
   ```

If required Lean skills are missing, the preferred manual install is:

```bash
npx leanprover-skills install lean-proof
npx leanprover-skills install mathlib-build
```

The checker also prints explicit clone-and-copy steps for environments where you want to install from source into a chosen skills dir:

```bash
git clone --depth 1 https://github.com/leanprover/skills.git /tmp/leanprover-skills
cp -R /tmp/leanprover-skills/skills/<missing-skill> <install-dir>/
```

If you pass `--auto-install-skills`, it will only run the clone-and-copy flow when `--install-dir <path>` or `OPENMATH_LEAN_SKILL_INSTALL_DIR` is set. It will not silently choose a shared home-directory skills folder for you. Project-local paths such as `.codex/skills` or `.claude/skills` are safer than modifying a shared skills directory by accident.

## Skill Search Paths

By default, the checker searches common installed skill directories for the active agent plus project-local `.{agent}/skills`. If your setup uses a non-standard location, point to it explicitly instead of relying on ambient home-directory defaults.

Override this with:

```bash
OPENMATH_SKILL_DIRS=/path/one:/path/two python3 scripts/check_theorem_env.py <workspace>
```

Or add directories explicitly:

```bash
python3 scripts/check_theorem_env.py <workspace> --skills-dir /path/to/skills
```

To control where auto-install writes missing Lean skills:

```bash
python3 scripts/check_theorem_env.py <workspace> --auto-install-skills --install-dir /path/to/skills
```

Without `--install-dir` or `OPENMATH_LEAN_SKILL_INSTALL_DIR`, auto-install will refuse to write anywhere.
