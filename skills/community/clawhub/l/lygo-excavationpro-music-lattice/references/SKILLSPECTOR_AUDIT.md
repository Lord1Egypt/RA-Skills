# SkillSpector audit response — lygo-excavationpro-music-lattice v1.0.0

| Concern | Mitigation |
|---------|------------|
| Untrusted stack path | `scripts/_stack_paths.py` validates directory name + known markers |
| Network exfil | Status script only hits steward-published HTTPS URLs listed in MUSIC_PORTAL.json |
| Write / publish | Skill scripts do not write stack or upload; operator CLI is separate |
| Secrets | No keys in skill tree; HF token stays in user env / hub cache |
| Subprocess | Status/self_check pure Python (stdlib + optional huggingface_hub only if installed for HF list) |
| Auto social | Forbidden in AGENT_CONTRACT |
| Large audio | Skill does not ship audio; points at HF dataset steward already published |

**Permissions declared:** read skill + optional stack; optional outbound HTTPS GET to public portal endpoints; no git push; no auto publish.
