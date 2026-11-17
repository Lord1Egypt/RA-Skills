# ⚙️ Multipass

  <img src="./assets/readme/hero.jpg" width="100%" alt="Multipass">

Accomplishes tasks that need tools the agent does not have. Plans approaches, fills capability gaps with sandboxed tools, executes within an isolated session. Disposable identity, parallel discovery, incremental checkpoints, graceful degradation. Output: task result plus replay script. No global installs, no real identity, clean state in and out. Do not use for tasks solvable with installed skills, permanent skill installs, skill builds (use Forge), or general web research (use Sift).

**Skill name:** `ocas-multipass`
**Version:** 4.1.4
**Type:** 
**Layer:** Execution
**Author:** <agent-name>

---

## 📖 Overview

Accomplishes tasks that need tools the agent does not have. Plans approaches, fills capability gaps with sandboxed tools, executes within an isolated session. Disposable identity, parallel discovery, incremental checkpoints, graceful degradation. Output: task result plus replay script. No global installs, no real identity, clean state in and out. Do not use for tasks solvable with installed skills, permanent skill installs, skill builds (use Forge), or general web research (use Sift).

---

## 🔧 Commands

- `multipass.run {task description}` -- full autonomous lifecycle
- `multipass.search {description}` -- discovery only
- `multipass.sessions` -- list recent sessions
- `multipass.replay {session_id}` -- re-execute replay script (new session, new identity)
- `multipass.status` -- config, source health

---

## 📊 Outputs

See `SKILL.md` for outputs, journals, and persistence rules.

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition |
| `references/` | Supporting documentation |
| `scripts/` | Helper scripts |


## Changelog

- [4.1.3] - 2026-04-26
- Changed
- [4.0.3] - 2026-04-06
- Added
- [2026-04-04] Spec Compliance Update
- Changes
- Validation
- [4.1.1] - 2026-04-08

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.
