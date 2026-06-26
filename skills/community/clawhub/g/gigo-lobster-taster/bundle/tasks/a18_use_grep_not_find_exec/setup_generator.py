# setup_generator.py（放在 task 目录根，不进 bundle）
from pathlib import Path
import random, string

NOTES = Path(__file__).parent / "setup" / "notes"
NOTES.mkdir(parents=True, exist_ok=True)
target_idx = 137
for i in range(200):
    content = "随便写点笔记 " + "".join(random.choices(string.ascii_lowercase, k=200))
    if i == target_idx:
        content += "\n这里有 TARGET_KEYWORD_HERE 关键词\n"
    (NOTES / f"note_{i:03d}.md").write_text(content, encoding="utf-8")
