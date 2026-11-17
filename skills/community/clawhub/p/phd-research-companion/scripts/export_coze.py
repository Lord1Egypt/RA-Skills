#!/usr/bin/env python3
"""Export this skill into a Coze-loadable skill package.

Why a script and not a copy: the two platforms share a directory shape but not
a metadata contract. Hand-copying means the next version bump silently ships a
stale Coze package. This regenerates it from the live tree and fails loudly when
a Coze-specific requirement is not met.

Coze requirements enforced here (from docs.coze.cn/cozespace/create_skill):
  - skill folder name / skill_id : lowercase letters, digits, underscore
  - SKILL.md is mandatory and carries name / version / description / tags
  - optional dirs: scripts/ references/ assets/
  - store listing name <= 20 characters (enforced in COZE_STORE.md)

Usage:
    python scripts/export_coze.py --check-only
    python scripts/export_coze.py
    python scripts/export_coze.py --out dist
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COZE_SKILL_ID = "phd_research_companion"          # <-= the uploaded folder name
COZE_STORE_NAME = "博士科研全流程助手"                # <= 20 characters, enforced
COZE_STORE_DESC = ("覆盖开题到投稿的科研全流程：真实文献检索、可编译 LaTeX 骨架、"
                   "证明台账、新颖性优先查重、精确有理数证书与投稿前审计。"
                   "核心承诺是不伪造结果——查不到就报告缺口。")

# Files that belong to WorkBuddy/ClawHub publishing, not to the skill itself.
EXCLUDE_NAMES = {
    "_skillhub_meta.json",     # local install state, contains absolute paths
    "_meta.json",              # ClawHub registry metadata
    "score-history.json",      # regenerable
    "score-report.md",         # regenerable
    "score-selftest-report.md",
    "install_verify.sh",       # bash-only; Coze sandboxes have no bash
    "run",
    "MANIFEST.txt",            # would duplicate on re-export
}
EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", ".git", ".github", "dist", ".idea", "tests"}
EXCLUDE_SUFFIX = {".pyc", ".pyo", ".sha256"}

# Self-scoring machinery: it measures THIS repo's publishing hygiene. A user who
# installs the skill on Coze has no repo to score, so shipping it would be dead
# weight -- but it stays in the ClawHub artifact on purpose.
COZE_DROP = {"scripts/self_score.py", "scripts/score_selftest.py",
             "scripts/package_skill.py", "tests/test_skill.py",
             # this exporter: it is a maintainer tool bound to this repo's
             # dist/ layout, and shipping it inside the artifact it produces is
             # a self-reference with no runtime value.
             "scripts/export_coze.py"}

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
SLUG_RE = re.compile(r"\A[a-z0-9_]+\Z")


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise SystemExit("SKILL.md has no YAML frontmatter")
    body = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            body[k.strip()] = v.strip()
    return body, text[m.end():]


def _version() -> str:
    fm, _ = _parse_frontmatter(_read(ROOT / "SKILL.md"))
    return fm.get("version", "0.0.0")


def _shipped(root: Path) -> list[Path]:
    out = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        if p.name in EXCLUDE_NAMES or p.suffix in EXCLUDE_SUFFIX:
            continue
        if rel in COZE_DROP:
            continue
        out.append(p)
    return out


def build_skill_md(version: str) -> str:
    """Coze frontmatter: skill_id-shaped name plus tags; body is reused as-is.

    The description is rewritten in Chinese because the store audience is
    Chinese, while the body keeps the English command reference so the agent
    still matches `run.py <command>` exactly.
    """
    _, body = _parse_frontmatter(_read(ROOT / "SKILL.md"))
    fm = (
        "---\n"
        f"name: {COZE_SKILL_ID}\n"
        f"version: {version}\n"
        "description: 科研全流程管理技能，面向 CS 博士生与理论机器学习研究者。"
        "提供真实文献检索（arXiv/DBLP/OpenAlex/Semantic Scholar）、可编译 LaTeX 骨架、"
        "证明台账（claim DAG）、新颖性优先查重、精确有理算术证书、修订追踪与投稿前审计。"
        "核心原则是绝不伪造结果：来源不可达、PDF 无法解析、命题未证明时一律报告缺口而非填补。"
        "支持 --track=theory（证明优先）与 --track=empirical（实验优先）双轨。"
        "当用户需要初始化研究项目、检索文献、检查选题新颖性、"
        "或做投稿前自查时使用本技能。\n"
        'tags: ["科研管理", "文献检索", "LaTeX", "机器学习", "理论证明", "论文投稿"]\n'
        "---\n"
    )
    return fm + body


def validate(dst: Path) -> list[str]:
    """Fail loudly rather than shipping a package Coze will reject."""
    errs: list[str] = []

    if not SLUG_RE.match(COZE_SKILL_ID):
        errs.append(f"skill_id {COZE_SKILL_ID!r} is not lowercase/digit/underscore")
    if len(COZE_STORE_NAME) > 20:
        errs.append(f"store name is {len(COZE_STORE_NAME)} chars, Coze allows 20")
    if len(COZE_STORE_DESC) > 200:
        errs.append(f"store description is {len(COZE_STORE_DESC)} chars, Coze allows 200")

    skill_md = dst / "SKILL.md"
    if not skill_md.exists():
        errs.append("SKILL.md missing")
        return errs

    fm, _ = _parse_frontmatter(_read(skill_md))
    for key in ("name", "version", "description", "tags"):
        if key not in fm:
            errs.append(f"frontmatter key {key!r} missing")
    if not SLUG_RE.match(fm.get("name", "")):
        errs.append(f"frontmatter name {fm.get('name')!r} is not slug-shaped")
    if len(fm.get("description", "")) > 1024:
        errs.append("frontmatter description exceeds 1024 chars")

    # Every module must parse, or the Coze sandbox will fail at first call.
    for p in dst.rglob("*.py"):
        try:
            ast.parse(_read(p))
        except SyntaxError as e:
            errs.append(f"{p.relative_to(dst)}: {e}")

    # The real invariant: every REQUIRED command must resolve to a module that
    # exists in the package. Dropped scripts are legal inside OPTIONAL_COMMANDS
    # because run.py degrades those to "not available in this build".
    run = dst / "run.py"
    if run.exists():
        try:
            tree = ast.parse(_read(run))
        except SyntaxError as e:
            errs.append(f"run.py: {e}")
            tree = None
        if tree is not None:
            tables: dict[str, dict[str, str]] = {}
            for node in tree.body:
                if not isinstance(node, ast.Assign):
                    continue
                tgt = node.targets[0]
                if not (isinstance(tgt, ast.Name)
                        and tgt.id in ("COMMANDS", "OPTIONAL_COMMANDS")):
                    continue
                table: dict[str, str] = {}
                for key, val in zip(node.value.keys, node.value.values):
                    parts = val.elts if isinstance(val, ast.List) else [val]
                    # the path is ROOT / "x" or SCRIPTS / "x"
                    segs = [p.value for p in parts if isinstance(p, ast.Constant)]
                    table[key.value] = segs[-1] if segs else ""
                tables[tgt.id] = table

            for name, rel in tables.get("COMMANDS", {}).items():
                if not list(dst.rglob(rel)):
                    errs.append(f"run.py COMMANDS[{name!r}] -> {rel} not in package")
            # a dropped stem must never be reachable through a required command
            dropped = {Path(r).name for r in COZE_DROP}
            for name, rel in tables.get("COMMANDS", {}).items():
                if Path(rel).name in dropped:
                    errs.append(f"run.py COMMANDS[{name!r}] points at dropped {rel}")

    for d in ("scripts", "references", "assets"):
        if (dst / d).exists() and not any((dst / d).iterdir()):
            errs.append(f"{d}/ is present but empty")

    return errs


def store_metadata(version: str) -> str:
    icon = ROOT / "_icon.png"
    return f"""# Coze 商店上架元信息 (phd-research-companion {version})

由 `scripts/export_coze.py` 生成。字段值与 [上架配置项说明](https://docs.coze.cn/cozespace/create_skill#0d51dbd7) 一一对应。

## 基础展示信息

| 配置项 | 填写内容 | 约束 | 校验 |
|---|---|---|---|
| 技能名称 | `{COZE_STORE_NAME}` | ≤ 20 字符 | {len(COZE_STORE_NAME)} ✅ |
| 一句话描述 | {COZE_STORE_DESC} | ≤ 200 字 | {len(COZE_STORE_DESC)} ✅ |
| 封面图 | 上架界面手动上传（建议 16:9） | — | 见下方说明 |
| 详细介绍 | 见下方「详细介绍文案」 | — | ✅ |
| 分类 | 按商店当期分类树选最贴近的一项 | — | 需人工确认 |
| 精选案例 | **3 个**，见下方 | 必须是真实任务分享链接 | ⚠️ 需先在扣子里跑 3 次 |
| 是否开源 | **关闭** | 默认关闭 | ✅ 保持关闭 |

> 分类树会变动，`export_coze.py` 无法代填——上架时按当期列表人工选择。

## 精选案例（必须先在扣子里真实跑出来）

官方要求 3 个**公开任务分享链接**。以下 3 个场景直接对应技能的三条主线，
每个跑一次、复制分享链接、截图关键输出即可：

1. **文献检索 + BibTeX 产出**
   `run.py search -q "regression data selection" -s arxiv openalex -l 30`
   → 配图：生成的 `search-results-*.bibtex` 与 `search-summary-*.md`

2. **证明台账 + 依赖门禁**
   `run.py ledger -d ./proj/02-methodology-dev --init` 后逐条 `--add`，
   再试 `--set T1 --to proven`（依赖未证时应被拒绝）
   → 配图：终端里"依赖未证明，拒绝置为 proven"的返回码与提示

3. **投稿前审计**
   `run.py check -p ./proj`
   → 配图：BLOCKERS / WARNINGS 分级输出，以及 theory 轨把实验项标为 N/A 而非 FAIL

> 链接若含中文参数，先删掉中文部分，只保留 `http` 开头的地址。

## 详细介绍文案

```
{COZE_STORE_DESC}

【解决什么问题】
博士研究最常见的三个坑：文献没查全就写 related work、证明链条断了却把
结论写成已证、投稿前才发现 claim 与证据对不上。本技能用可执行脚本把这三件事
变成流程门禁，而不是靠自觉。

【核心能力】
· 真实文献检索：arXiv / DBLP / OpenAlex / Semantic Scholar，带限流退避；
  响应 Content-Type 不符直接拒收，绝不把反爬 HTML 当数据解析
· 可编译 LaTeX 骨架：IEEEtran / ACM / NeurIPS / ICLR / JMLR / article
· 证明台账：lemma -> theorem 依赖 DAG，依赖未证时拒绝标记为 proven
· 新颖性优先查重：主张 novelty 前必须留下带 URL 证据的裁决记录
· 精确有理算术证书：扫描 float 污染，要求脚本输出 CERTIFIED / REFUTED
· 投稿前审计：每项检查要么已实现，要么标 UNVERIFIED——未验证不算通过

【双轨设计】
--track=theory  以证明台账与证书为主产物（baseline/ablation 标 N/A 而非失败）
--track=empirical 以实验设计与对照为主产物

【一条硬规则】
本技能永不编造结果。来源不可达、PDF 无法解析、命题未证明时，它报告缺口。
被报告的缺口是有用的，被悄悄填上的缺口是负债。
```

## 上架前检查清单

- [ ] 技能已创建并**完成部署**（部署是上架的硬前提）
- [ ] 已单独申请**技能上架资质**并通过（`我的技能` → ⋮ → 申请技能上架资质）
- [ ] 用**网页端或桌面端**操作（移动端不支持上架）
- [ ] 确认自己是**技能所有者**
- [ ] 3 个精选案例链接均为真实跑出来的
- [ ] 「是否开源」保持**关闭**
- [ ] 同意开发者协议并提交
- [ ] 审核结果在**站内信**查看

## 付费设置

**建议：免费。** 理由见 README「为什么不走付费」。

Coze 的「按次付费」**仅适用于通过调用 API 提供功能的技能**（官方原文），
本技能是 CLI + 工作流方法论，没有对外 HTTP 接口，走不了按次计费；
「一次买断」从月度档位自动推季度/年度价，受众为博士生时订阅制是负资产。

若日后坚持付费，先完成商户入驻：<https://code.coze.cn/merchant-management>
结算规则见 <https://docs.coze.cn/cozespace/skill_revenue_settlement>
（支付宝 / 抖音支付；购买后 30 天结算；**iOS 渠道扣 30% 佣金及代扣个税**）。
"""


def build(out_dir: Path, include_reports: bool = False) -> dict:
    version = _version()
    dst = out_dir / COZE_SKILL_ID
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)

    for p in _shipped(ROOT):
        rel = p.relative_to(ROOT)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)

    (dst / "SKILL.md").write_text(build_skill_md(version), encoding="utf-8")

    # assets/ is a Coze-documented directory; give it the icon so the folder is
    # not empty (export_coze.py fails the build on an empty assets/).
    assets = dst / "assets"
    assets.mkdir(exist_ok=True)
    icon = ROOT / "_icon.png"
    if icon.exists():
        shutil.copy2(icon, assets / "icon.png")

    errs = validate(dst)
    meta = store_metadata(version)
    (out_dir / "COZE_STORE.md").write_text(meta, encoding="utf-8")

    if errs:
        raise SystemExit("Coze package validation failed:\n  - " + "\n  - ".join(errs))

    zip_path = out_dir / f"{COZE_SKILL_ID}-coze.zip"
    # Enumerate ONLY what this run actually wrote. Rglobbing out_dir looks
    # tempting but picks up leftovers from a previous export whose file set has
    # since changed -- the manifest then lists files the zip does not contain
    # and every downstream sha256 verification fails on a missing path.
    written: list[Path] = []
    for p in sorted(dst.rglob("*")):
        if p.is_file() and p.suffix not in EXCLUDE_SUFFIX:
            written.append(p)
    meta_path = out_dir / "COZE_STORE.md"
    written.append(meta_path)
    written.sort()

    # Write the manifest BEFORE archiving so it travels inside the zip: a
    # verifier who only has the archive can still check every file. It cannot
    # list itself, so it is written last and excluded from its own entries.
    man_path = out_dir / "MANIFEST.txt"
    header = [f"# {COZE_SKILL_ID} {version} (coze export)",
              f"# {len(written)} files (+ this manifest)"]
    for p in written:
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        header.append(f"{h}  {p.relative_to(out_dir).as_posix()}")
    man_path.write_text("\n".join(header) + "\n", encoding="utf-8")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in written + [man_path]:
            z.write(p, p.relative_to(out_dir).as_posix())

    # The manifest must describe the archive exactly, or the sha256 file below
    # is a claim nobody can check.
    with zipfile.ZipFile(zip_path) as z:
        expect = {p.relative_to(out_dir).as_posix() for p in written + [man_path]}
        if set(z.namelist()) != expect:
            raise SystemExit("manifest/archive mismatch: rerun with a clean --out")

    return {"version": version, "skill_id": COZE_SKILL_ID,
            "files": len(written) + 1, "zip": str(zip_path),
            "sha256": hashlib.sha256(zip_path.read_bytes()).hexdigest(),
            "store_name": COZE_STORE_NAME, "store_desc_len": len(COZE_STORE_DESC)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "dist" / "coze"),
                    help="output directory (default: dist/coze)")
    ap.add_argument("--check-only", action="store_true",
                    help="validate without writing the zip")
    a = ap.parse_args()

    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    if a.check_only:
        version = _version()
        tmp = out / "_check"
        if tmp.exists():
            shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        try:
            (tmp / COZE_SKILL_ID).mkdir()
            for p in _shipped(ROOT):
                t = tmp / COZE_SKILL_ID / p.relative_to(ROOT)
                t.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, t)
            (tmp / COZE_SKILL_ID / "SKILL.md").write_text(
                build_skill_md(version), encoding="utf-8")
            a_ = tmp / COZE_SKILL_ID / "assets"
            a_.mkdir(exist_ok=True)
            if (ROOT / "_icon.png").exists():
                shutil.copy2(ROOT / "_icon.png", a_ / "icon.png")
            errs = validate(tmp / COZE_SKILL_ID)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        if errs:
            print("FAIL\n  - " + "\n  - ".join(errs))
            return 1
        print(f"OK  coze package valid ({COZE_SKILL_ID} {version})")
        return 0

    info = build(out)
    print(f"exported {info['files']} files -> {info['zip']}")
    print(f"skill_id {info['skill_id']}")
    print(f"version {info['version']}")
    print(f"store name {info['store_name']} ({len(info['store_name'])}/20 chars)")
    print(f"sha256  {info['sha256']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
