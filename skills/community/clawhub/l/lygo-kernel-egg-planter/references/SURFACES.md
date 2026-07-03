# Legal, honest planting surfaces

| Surface | Flag | Who acts | Notes |
|---------|------|----------|-------|
| Local CA | `local` | User machine | `data/anchors/` — sovereign copy |
| Arweave Turbo | `turbo` | User machine | ≤100 KiB/tx; best-effort gateway |
| Registry file | `registry` | User machine | `data/kernel_eggs/registry.json` |
| GitHub Pages JSON | `pages` | **User** git push | `docs/KernelEggRegistry.json` |
| Node SOA API | `node` | User runs `node_api_server.py` | `:8787/kernel/eggs` |
| Book-brain stub | `stubs` | User copies refs | `reference/*.ref.txt` |
| HF dataset | — | **Maintainer only** | `hf_push_dataset.py` after user asks |
| ClawHub republish | — | **Maintainer only** | separate from plant |

**ClawHub catalog egg** contains only slugs, names, URLs from public `skills.json` — not full SKILL.md bodies (those stay on ClawHub).

**Scaling max:** many nodes pinning the same `registry_merkle_root` via gossip/TLS pins — optional future hook; not required for first plant.