# Rendering Notes

If `drawio`/`draw.io` CLI is installed, image export runs locally.

If local CLI is unavailable, the script tries Docker image `jgraph/drawio` unless `--no-docker-fallback` is set.

Typical local CLI export command:

```bash
drawio -x -f png -o /path/out.png /path/in.drawio
```
