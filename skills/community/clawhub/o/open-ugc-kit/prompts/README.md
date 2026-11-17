# Opening scenes (100 stills + 100 Seedance 2.5 prompts)

25 scenes per format. Each scene has a still (first frame) and a Seedance 2.5 I2V prompt. Fill brackets, generate 9:16, then run Seedance 2.5: **8s · 720×1280 · audio on · first frame = still**.

| Format | File | I2V master |
|---|---|---|
| Unboxing | [unboxing.md](unboxing.md) | Unboxing |
| Street interview | [street-interview.md](street-interview.md) | Street interview |
| Face-cam review | [face-cam-review.md](face-cam-review.md) | Face-cam review |
| Q&A / who sells more | [qa-who-sells-more.md](qa-who-sells-more.md) | Q&A |

See `docs/seedance-2.5.md`. To regenerate after editing `scripts/build_openings.py`:

```bash
python3 scripts/build_openings.py
```
