# Proof Loop Examples

Start here if you want proof instead of prose.

| Example | What it shows |
| --- | --- |
| [`demo-repo/`](demo-repo/) | A small runnable task with a real file check and passing proof artifacts. |
| [`example-task/`](example-task/) | A completed task folder with spec, verdict, evidence, and problems files. |
| [`role-briefs/`](role-briefs/) | Copy-paste briefs for orchestrator, spec freezer, builder, verifier, and fixer roles. |

Fast path:

```bash
make test
bin/proof-loop check examples/demo-repo/.agent/tasks/nav-labels-proof
bin/proof-loop report examples/demo-repo/.agent/tasks/nav-labels-proof --format md
```
