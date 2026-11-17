# Test plan

| ID | Test | Pass |
|----|------|------|
| T1 | Import kernel modules | no exception |
| T2 | P0 allows benign, quarantines obvious abuse | verdicts correct |
| T3 | Mycelium store/list | file grows |
| T4 | Health endpoint shape | json keys present |
| T5 | Limb help/status | ok true |
| T6 | Chat if Ollama up | non-empty reply OR clear cold message |
| T7 | Portal files exist | index.html |
| T8 | Config load | smart_disk.json |
| T9 | Disk free > 0 after install | true |
| T10 | self_check exit 0 | true |
