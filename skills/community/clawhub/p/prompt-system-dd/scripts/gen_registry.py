# -*- coding: utf-8 -*-
"""R08:从 atoms/ 目录实证生成 atom-registry.yaml(注册制唯一机器真相源)。"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # scripts/ 的上级 = 项目根,不依赖盘符路径
OUT = ROOT / "references" / "registry" / "atom-registry.yaml"


def main():
    lines = [
        "# 原子注册中心(R08)—— 由 scripts 下生成脚本从 atoms/ 目录实证生成",
        "# 用途:跨 Skill 复用 atoms;门禁 RG001-RG003 校验本表与目录双向一致。",
        "# version: 原子内容变更时由维护者递增(语义化:结构变更+0.1,文案微调+0.0.1)。",
        "version: 1",
        "atoms:",
    ]
    n = 0
    for cat, ctype in (("core", "core"), ("domains", "domain"), ("outputs", "output")):
        d = ROOT / "references" / "atoms" / cat
        for f in sorted(d.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            head = text[:300]
            m = re.search(r"^id:\s*([a-z0-9-]+)\s*$", head, re.MULTILINE)
            aid = m.group(1) if m else f.stem
            title = re.search(r"^#\s+(\S+)\s+(.+)$", text, re.MULTILINE)
            desc = title.group(2).strip() if title else aid
            ver = "1.0.0"
            dm = re.search(r"^deps:\s*(\S+)\s*$", text, re.MULTILINE)
            deps = dm.group(1) if dm else "none"
            lines.append(f"  - id: {aid}")
            lines.append(f"    type: {ctype}")
            lines.append(f"    source: references/atoms/{cat}/{f.name}")
            lines.append(f"    version: {ver}")
            lines.append(f"    deps: {deps}")
            lines.append(f"    description: {desc}")
            n += 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print("registered atoms:", n)


if __name__ == "__main__":
    main()
