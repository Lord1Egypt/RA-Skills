#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材上传器 · upload_assets.py

把「指定路径」下的素材（含子文件夹）**原样复制**一份到目标目录（默认 /var/www/public/mv），
文件夹层级保持一致；**若目标目录/文件已存在，默认直接覆盖**（先整目录删除再写入，
可用 --no-overwrite-dir 关闭）；复制完成后生成「外网路径清单」（.md 表格 + .txt 纯链接），
**并在成功获得外链后删除源素材**（默认；加 --keep-source 可保留源文件）。

默认还会**清空整个源目录内容**（`--purge-project`，默认开）：上传成功、链接回显后，
把源目录里的文件 / 子文件夹 / 清单**全部删掉**；若清空后源目录已经空了，且它不是默认暂存目录
`assets/source` 本身，则**连源目录本身也一并删除**（即用 `--src` 指到项目文件夹时，传完整个
项目文件夹消失，只留暂存目录 `assets/source`）。外链只在终端输出（清单不再落盘）。
传完即清空项目，避免本地残留。
想保留空文件夹壳：加 `--keep-src-dir`。想保留源文件与清单：加 `--keep-source`，或 `--no-purge-project`。

标准库实现，零依赖，Python 3.8+ 直接跑。

默认映射（保留源文件夹名）：
    源   /x/我的项目/素材/图片/a.png
    目标 /var/www/public/mv/素材/图片/a.png
    外链 https://your-static-host.example.com/public/mv/素材/图片/a.png

用法：
    python3 scripts/material-uploader/upload_assets.py --src "/x/我的项目/素材"
    python3 scripts/material-uploader/upload_assets.py --src "/x/素材" --prefix 示例项目-第3期
    python3 scripts/material-uploader/upload_assets.py --src a.png          # 单文件
    python3 scripts/material-uploader/upload_assets.py --src "/x/素材" --keep-source   # 保留源素材
    python3 scripts/material-uploader/upload_assets.py --src "/x/素材" --keep-src-dir  # 保留源目录空壳（不删文件夹本身）
    python3 scripts/material-uploader/upload_assets.py --src "/x/素材" --no-purge-project  # 保留源目录内容+清单
    python3 scripts/material-uploader/upload_assets.py --src "/x/素材" --no-overwrite-dir  # 已存在则跳过，不覆盖
    python3 scripts/material-uploader/upload_assets.py --src "/x/素材" --dry-run
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import urllib.error
from datetime import datetime
from pathlib import Path, PurePosixPath

SKILL_ROOT = Path(__file__).resolve().parent
CONFIG_PATH = SKILL_ROOT / "config.json"
EXAMPLE_CONFIG_PATH = SKILL_ROOT / "config.example.json"
ENV_PATH = SKILL_ROOT.parent.parent / ".env"


def _load_env_file() -> None:
    if not ENV_PATH.is_file():
        return
    for raw in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


_load_env_file()

DEFAULTS = {
    "source_dir": "assets/source",
    "dest_dir": os.environ.get("ASSET_DEST_DIR", "/var/www/public/mv"),
    "url_base": os.environ.get("ASSET_URL_BASE", "https://your-static-host.example.com/public/mv"),
    "keep_root": True,
    "skip_hidden": True,
    "keep_source": False,
    "purge_project": True,
    "keep_src_dir": False,
    "overwrite_dir": True,
    "manifest_name": "素材外网路径",
}


def load_config() -> dict:
    cfg = dict(DEFAULTS)
    path = CONFIG_PATH if CONFIG_PATH.exists() else EXAMPLE_CONFIG_PATH
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                cfg.update({k: v for k, v in data.items() if k in DEFAULTS})
        except Exception as e:  # noqa: BLE001
            print(f"[warn] 读取 config.json 失败，改用默认值：{e}", file=sys.stderr)
    if os.environ.get("ASSET_DEST_DIR"):
        cfg["dest_dir"] = os.environ["ASSET_DEST_DIR"]
    if os.environ.get("ASSET_URL_BASE"):
        cfg["url_base"] = os.environ["ASSET_URL_BASE"]
    return cfg


def resolve_staging_dir(cfg: dict) -> Path:
    """解析默认暂存目录（config 的 source_dir）的绝对路径。"""
    raw = Path(cfg.get("source_dir", "assets/source")).expanduser()
    if not raw.is_absolute():
        raw = SKILL_ROOT / raw
    return raw.resolve()


def ensure_dir(target: Path, mode: int = 0o777) -> Path:
    """创建目录（含父级），并确保本次新建的每一层都是指定权限。"""
    target = Path(target)
    missing = []
    p = target
    while not p.exists():
        missing.append(p)
        if p.parent == p:
            break
        p = p.parent
    target.mkdir(parents=True, exist_ok=True)
    for d in missing:
        try:
            os.chmod(d, mode)
        except OSError:
            pass
    return target


def purge_dir_contents(target: Path, keep=()) -> int:
    """清空目录内容，保留目录本身；keep 为顶层需保留的文件/目录名。返回移除的条目数。"""
    target = Path(target)
    removed = 0
    for entry in sorted(target.iterdir()):
        if entry.name in keep:
            continue
        try:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry, ignore_errors=True)
            else:
                entry.unlink()
            removed += 1
        except OSError as e:  # noqa: BLE001
            print(f"  ✗ 清理失败 {entry}：{e}", file=sys.stderr)
    return removed


def is_under(path: Path, base: Path) -> bool:
    """判断 path 是否位于 base 之下（严格子路径，base 本身不算）。"""
    p = os.path.abspath(str(path))
    b = os.path.abspath(str(base))
    return p != b and p.startswith(b.rstrip(os.sep) + os.sep)


def count_files(target: Path) -> int:
    """统计目录/文件内的文件数（目录本身不计）。"""
    target = Path(target)
    if target.is_dir() and not target.is_symlink():
        return sum(len(names) for _root, _dirs, names in os.walk(target))
    return 1


def remove_target(target: Path, base_dest: Path) -> int:
    """整体删除目标文件/目录（用于「已存在即覆盖」）。返回清除的旧文件数。

    安全护栏：绝不删除 base_dest 本身，也绝不删除 base_dest 之外的路径。
    """
    target = Path(target)
    if not (target.exists() or target.is_symlink()):
        return 0
    if not is_under(target, base_dest):
        print(f"  ⚠ 跳过受保护路径（不做整目录覆盖）：{target}", file=sys.stderr)
        return 0
    if target.is_dir() and not target.is_symlink():
        n = count_files(target)
        shutil.rmtree(target, ignore_errors=False)
        return n
    target.unlink()
    return 1


def dir_stats(target: Path, skip_hidden: bool):
    """统计目录内文件数与总大小，返回 (文件数, 字节数)。"""
    count = 0
    total = 0
    for root, dirs, names in os.walk(target):
        if skip_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in names:
            if skip_hidden and name.startswith("."):
                continue
            try:
                total += (Path(root) / name).stat().st_size
                count += 1
            except OSError:
                pass
    return count, total


def human_size(n: int) -> str:
    f = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if f < 1024 or unit == "TB":
            return f"{int(f)}B" if unit == "B" else f"{f:.1f}{unit}"
        f /= 1024
    return f"{f:.1f}TB"


def collect_files(src: Path, skip_hidden: bool, exts):
    """递归收集源目录下的文件（稳定排序）。"""
    files = []
    for root, dirs, names in os.walk(src):
        dirs.sort()
        names.sort()
        if skip_hidden:
            dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in names:
            if skip_hidden and name.startswith("."):
                continue
            p = Path(root) / name
            if exts and p.suffix.lower() not in exts:
                continue
            files.append(p)
    return files


def parse_exts(raw):
    if not raw:
        return set()
    out = set()
    for piece in raw.replace("，", ",").split(","):
        piece = piece.strip().lower()
        if not piece:
            continue
        if not piece.startswith("."):
            piece = "." + piece
        out.add(piece)
    return out


def build_url(url_base: str, *segments: str, encode: bool) -> str:
    base = url_base.rstrip("/")
    tail = "/".join(s.strip("/") for s in segments if s and s != ".")
    full = f"{base}/{tail}" if tail else base
    if not encode:
        return full
    from urllib.parse import quote

    safe = "/:@!$&'()*+,;=~-._"
    if "://" in full:
        scheme, rest = full.split("://", 1)
        host, slash, path = rest.partition("/")
        return f"{scheme}://{host}/{quote(path, safe=safe)}"
    return quote(full, safe=safe)


def run_probe(dest_root: Path, rel_parts: list[str], url_base: str, encode: bool, quiet: bool) -> int:
    """落点探测：写一个 1KB 探测文件到目标命名空间，HEAD 它的外链，打印三行对照。"""
    import urllib.request

    probe_name = "_upload_probe.txt"
    url = build_url(url_base, *rel_parts, probe_name, encode=encode)
    ns = "/".join(rel_parts) if rel_parts else "(根)"
    print("-" * 60)
    print("[probe] 磁盘落点 :", dest_root / probe_name)
    print("[probe] 目标 URL  :", url)
    print("[probe] 命名空间  :", ns)
    print("[probe] URL 编码  :", "开" if encode else "关（裸中文，很多服务端会 404）")
    print("-" * 60)
    try:
        dest_root.mkdir(parents=True, exist_ok=True)
        (dest_root / probe_name).write_bytes(b"probe " + b"x" * 1024)
    except Exception as exc:  # noqa: BLE001
        print(f"[probe] ❌ 磁盘写入失败：{exc}", file=sys.stderr)
        print("        目标根不可写 → 确认挂载点（dest_dir）是否指向站点目录", file=sys.stderr)
        return 2

    code = "ERR"
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=10) as resp:
            code = resp.status
    except urllib.error.HTTPError as exc:
        code = exc.code
    except UnicodeEncodeError:
        code = "ERR:UnicodeEncodeError"
    except Exception as exc:  # noqa: BLE001
        code = f"ERR:{exc.__class__.__name__}"

    if code == 200:
        print("[probe] ✅ 外链可访问（200）→ 磁盘落点与 URL 映射一致，可以传全量")
        try:
            (dest_root / probe_name).unlink()
        except Exception:  # noqa: BLE001
            pass
        return 0
    if code == 404:
        print("[probe] ❌ 404：文件写进去了，但 URL 取不到", file=sys.stderr)
        print("        常见原因：dest_dir 与 url_base 不是同一层（多/少一层 mv）、"
              "站点 alias 未指向该目录、或 upload 到另一台机器", file=sys.stderr)
    elif code == 403:
        print("[probe] ❌ 403：目录存在但被挡（鉴权/防盗链/无读权限）→ Seedance 也取不到，改走 base64",
              file=sys.stderr)
    else:
        print(f"[probe] ❌ 失败：{code}", file=sys.stderr)
        print("        若是 UnicodeEncodeError，说明 URL 未编码却含中文", file=sys.stderr)
    return 1



def main() -> int:
    cfg = load_config()
    ap = argparse.ArgumentParser(
        description="把指定路径下的素材复制到 /var/www/public/mv、回显外链、并清空源目录（只做上传素材）。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--src", default=None,
                    help="源路径：文件夹或单个文件（默认取 config 的 source_dir，即 skill 的 assets/source）")
    ap.add_argument("--dest", default=cfg["dest_dir"], help=f"目标根目录（默认 {cfg['dest_dir']}）")
    ap.add_argument("--url-base", default=cfg["url_base"], help=f"外网根目录（默认 {cfg['url_base']}）")
    ap.add_argument("--prefix", default="", help="在目标根目录下再套一层命名空间文件夹（如项目名/期数）")
    ap.add_argument("--name", default="", help="覆盖源文件夹在目标中的名字（默认取源文件夹名）")
    ap.add_argument("--strip-root", action="store_true",
                    help="不保留源文件夹名，直接把源内层级铺到目标根下")
    ap.add_argument("--keep-root", action="store_true", help="保留源文件夹名（默认行为，可显式指定）")
    ap.add_argument("--manifest", default="", help="清单输出目录或文件前缀（默认写到源目录）")
    ap.add_argument("--overwrite", action="store_true",
                    help="覆盖目标已存在文件（默认已由 --overwrite-dir 默认覆盖；本开关用于 --no-overwrite-dir 时）")
    ap.add_argument("--overwrite-dir", dest="overwrite_dir", action="store_true", default=None,
                    help="目标目录已存在时整目录覆盖：先删旧目录再写入本次素材（默认开）")
    ap.add_argument("--no-overwrite-dir", dest="overwrite_dir", action="store_false", default=None,
                    help="关闭整目录覆盖，退回逐文件处理（默认跳过已存在，需 --overwrite 才覆盖）")
    ap.add_argument("--clear-source", "--clear", dest="clear_source", action="store_true",
                    help="仅清空源目录内容（文件/子目录/清单/隐藏文件），只保留源目录本身；不做上传，清完即退出")
    ap.add_argument("--keep-source", action="store_true",
                    help="上传成功后全保留源素材与目录（默认：上传成功后清空整个源目录）")
    ap.add_argument("--purge-project", dest="purge_project", action="store_true", default=None,
                    help="上传成功后清空整个源目录（文件/子目录/清单）；源目录若已空且非暂存目录，连目录本身一并删除（默认开）")
    ap.add_argument("--no-purge-project", dest="purge_project", action="store_false", default=None,
                    help="不做项目清空：已上传的源文件仍按默认删除，但保留目录本身、清单与隐藏文件")
    ap.add_argument("--keep-src-dir", dest="keep_src_dir", action="store_true", default=None,
                    help="清空后保留源目录的空文件夹壳（默认：源目录已空且非暂存目录 assets/source 时连目录一起删）")
    ap.add_argument("--rm-src-dir", dest="keep_src_dir", action="store_false", default=None,
                    help="清空后连源目录本身一起删除（默认行为，可显式指定）")
    ap.add_argument("--include-hidden", action="store_true", help="包含隐藏文件/文件夹（默认跳过）")
    ap.add_argument("--ext", default="", help="只处理这些扩展名，逗号分隔（如 .png,.jpg,.mp4）")
    ap.add_argument("--url-encode", dest="url_encode", action="store_true", default=True,
                    help="外链做百分号编码（中文/空格转义）。默认开启——裸中文 URL 很多服务端直接 404")
    ap.add_argument("--no-url-encode", dest="url_encode", action="store_false",
                    help="关闭百分号编码（仅当目标站点明确要求裸中文路径时用）")
    ap.add_argument("--probe", action="store_true",
                    help="只做落点探测：往目标命名空间写一个 1KB 探测文件并 HEAD 它的外链，"
                         "打印「磁盘落点 / 目标 URL / 命名空间」三行对照，通过才值得传全量")
    ap.add_argument("--verify", action="store_true", help="复制后对每条外链发 HEAD 请求核验（需网络）")
    ap.add_argument("--json", action="store_true", help="额外生成 素材外网路径.json")
    ap.add_argument("--dry-run", action="store_true", help="只预览，不复制、不写清单")
    ap.add_argument("--quiet", action="store_true", help="精简输出")
    args = ap.parse_args()

    # 源路径：显式 --src 优先；否则用 config 的 source_dir（默认 skill 的 assets/source 暂存目录）
    explicit_src = bool(args.src)
    staging_dir = resolve_staging_dir(cfg)
    if explicit_src:
        src = Path(args.src).expanduser().resolve()
    else:
        src = staging_dir

    if not src.exists():
        if not explicit_src and not args.clear_source:
            ensure_dir(src)
            print(f"[info] 默认暂存目录不存在，已创建：{src}")
            print("       请把要上传的素材放进该目录后重新运行。")
            return 0
        if args.clear_source:
            print(f"[info] 源目录不存在，无需清空：{src}")
            return 0
        print(f"[error] 源路径不存在：{src}", file=sys.stderr)
        return 2

    # ------- 仅清空源目录模式（不做上传） -------
    if args.clear_source:
        if not src.is_dir():
            print(f"[error] --clear-source 需要目录，收到的是文件：{src}", file=sys.stderr)
            return 2
        clear_skip_hidden = cfg["skip_hidden"] and not args.include_hidden
        keep_top = (".gitkeep",)
        entries = [e for e in src.iterdir()
                   if e.name not in keep_top and not (clear_skip_hidden and e.name.startswith("."))]
        if not entries:
            print(f"源目录已为空，无需清空：{src}")
            return 0
        count, total = dir_stats(src, clear_skip_hidden)
        if args.dry_run:
            print(f"[dry-run] 将清空源目录：{src}")
            print(f"          条目 {len(entries)} 个 · 文件 {count} 个 · 合计 {human_size(total)}（未实际删除）")
            return 0
        removed = purge_dir_contents(src, keep=keep_top)
        print(f"已清空源目录：{src}")
        print(f"  移除条目 {removed} 个 · 文件 {count} 个 · 释放 {human_size(total)}（仅保留目录本身）")
        return 0

    # 保留/去根：显式开关优先；默认暂存目录不保留「source」这一层，显式 --src 默认保留
    if args.keep_root:
        keep_root = True
    elif args.strip_root:
        keep_root = False
    elif explicit_src:
        keep_root = cfg.get("keep_root", True)
    else:
        keep_root = False
    skip_hidden = cfg["skip_hidden"] and not args.include_hidden
    exts = parse_exts(args.ext)
    manifest_name = cfg["manifest_name"]
    # 默认在上传成功、外链清单生成后删除源素材；--keep-source 或 config 可保留
    keep_source = args.keep_source or cfg.get("keep_source", False)
    # 项目清空：默认开；与 --keep-source 互斥（保留源时不删）
    if args.purge_project is None:
        purge_project = bool(cfg.get("purge_project", True))
    else:
        purge_project = args.purge_project
    purge = purge_project and not keep_source
    if keep_source and args.purge_project:  # 仅在显式要求清空、却又保留源时提示
        print("[warn] --keep-source 与项目清空互斥，已自动跳过清空。", file=sys.stderr)
    # 源目录本身是否连壳一起删：默认开（仅当清空后源目录已空、且不是暂存目录 assets/source）
    if args.keep_src_dir is None:
        keep_src_dir = bool(cfg.get("keep_src_dir", False))
    else:
        keep_src_dir = args.keep_src_dir
    rm_src_dir = purge and not keep_src_dir
    staging_disp = str(cfg.get("source_dir", "assets/source"))

    # 清单文件本身不被当作素材复制
    manifest_files = {f"{manifest_name}.md", f"{manifest_name}.txt", f"{manifest_name}.json"}

    is_dir = src.is_dir()
    root_name = ""
    if is_dir:
        if args.name:
            root_name = args.name
        elif keep_root:
            root_name = src.name
        else:
            root_name = ""

    # 目标目录相对段：prefix / root_name
    rel_parts = [p for p in [args.prefix.strip("/"), root_name] if p]
    dest_root = Path(args.dest).expanduser() / PurePosixPath(*rel_parts) if rel_parts else Path(args.dest).expanduser()

    # ------- 落点探测模式（不做全量上传） -------
    if args.probe:
        return run_probe(dest_root, rel_parts, args.url_base, args.url_encode, args.quiet)

    # ------- 收集待复制文件 -------
    if is_dir:
        files = collect_files(src, skip_hidden, exts)
        entries_src = [(f, f.relative_to(src).as_posix()) for f in files]
    else:
        if exts and src.suffix.lower() not in exts:
            print(f"[warn] 源文件扩展名不在 --ext 过滤内，仍将上传：{src.name}", file=sys.stderr)
        entries_src = [(src, src.name)]

    # 清单文件本身不作为素材上传
    entries_src = [(f, rel) for (f, rel) in entries_src if Path(rel).name not in manifest_files]

    if not entries_src:
        print(f"[warn] 源路径下没有可上传的文件：{src}", file=sys.stderr)
        print("       把素材放进该目录（含子文件夹）后重新运行。", file=sys.stderr)
        return 0

    # ------- 目标目录整体覆盖（默认开） -------
    # 上传时若目标目录已存在，直接覆盖：先整目录删除，再写入本次素材，
    # 避免上一次上传遗留的多余/改名文件残留。--no-overwrite-dir 关闭（退回逐文件 skip）。
    if args.overwrite_dir is None:
        overwrite_dir = bool(cfg.get("overwrite_dir", True))
    else:
        overwrite_dir = args.overwrite_dir
    overwrite_files = overwrite_dir or args.overwrite  # 整目录覆盖时文件一律重写

    base_dest = Path(args.dest).expanduser()
    replace_targets: list = []
    if overwrite_dir and is_dir:
        if dest_root != base_dest:
            # 本次上传有独立命名空间（prefix / 保留根名）→ 整个目标目录整体覆盖
            replace_targets = [dest_root]
        else:
            # 直接铺在目标根下 → 逐个顶层子目录整体覆盖（绝不整删目标根本身）
            seen: list = []
            for _f, rel in entries_src:
                parts = PurePosixPath(rel).parts
                if len(parts) >= 2:
                    cand = dest_root / parts[0]
                    if cand not in seen:
                        seen.append(cand)
            replace_targets = seen

    # ------- 复制 -------
    results = []  # dict: rel, src, dest, url, size, status
    ok = skipped = failed = 0
    total_bytes = 0
    replaced_dirs = 0
    replaced_old_files = 0

    if not args.quiet:
        print(f"源   ：{src}")
        print(f"目标 ：{dest_root}")
        print(f"外链 ：{args.url_base.rstrip('/')}/{'/'.join(rel_parts) if rel_parts else ''}".rstrip("/"))
        print(f"文件 ：{len(entries_src)} 个" + ("（dry-run 预览）" if args.dry_run else ""))
        pending = [t for t in replace_targets if t.exists() or t.is_symlink()]
        if overwrite_dir and pending:
            print(f"覆盖 ：目标目录已存在，将直接覆盖（{len(pending)} 个）")
            for t in pending:
                print(f"       ⟳ {t}")
        print("-" * 60)

    # 先删除待覆盖目录（dry-run 不动手）
    if not args.dry_run and replace_targets:
        for t in replace_targets:
            if not (t.exists() or t.is_symlink()):
                continue
            old_n = remove_target(t, base_dest)
            if not (t.exists() or t.is_symlink()):
                replaced_dirs += 1
                replaced_old_files += old_n
                if not args.quiet:
                    print(f"  ⟳ 覆盖已存在目录：{t}（清除旧内容 {old_n} 个文件）")

    for src_file, rel in entries_src:
        dest_file = dest_root / PurePosixPath(rel)
        url = build_url(args.url_base, *rel_parts, rel, encode=args.url_encode)
        size = src_file.stat().st_size
        status = "ok"

        if args.dry_run:
            status = "dry"
        elif dest_file.exists() and not overwrite_files:
            status = "skip"
            skipped += 1
        else:
            try:
                ensure_dir(dest_file.parent)
                shutil.copy2(src_file, dest_file)  # 保留时间/权限元数据
                ok += 1
            except Exception as e:  # noqa: BLE001
                status = "fail"
                failed += 1
                print(f"  ✗ 复制失败 {rel}：{e}", file=sys.stderr)

        if status in ("ok", "skip"):
            total_bytes += size

        results.append({
            "rel": rel,
            "src": str(src_file),
            "dest": str(dest_file),
            "url": url,
            "size": size,
            "status": status,
        })
        if not args.quiet and status in ("ok", "dry"):
            mark = "·" if status == "dry" else "✓"
            print(f"  {mark} {rel}  ({human_size(size)})")

    # ------- 核验（可选） -------
    if args.verify and not args.dry_run:
        import urllib.request

        if not args.quiet:
            print("-" * 60)
            print("核验外链：")
        bad = {"404": 0, "403": 0, "err": 0, "other": 0}
        for r in results:
            if r["status"] not in ("ok", "skip"):
                continue
            try:
                req_url = r["url"].replace(" ", "%20")
                req = urllib.request.Request(req_url, method="HEAD")
                with urllib.request.urlopen(req, timeout=10) as resp:
                    r["http"] = resp.status
            except Exception as e:  # noqa: BLE001
                r["http"] = f"ERR:{e}"
            h = str(r["http"])
            if h == "404":
                bad["404"] += 1
            elif h == "403":
                bad["403"] += 1
            elif h.startswith("ERR"):
                bad["err"] += 1
            elif h != "200":
                bad["other"] += 1
            if not args.quiet:
                print(f"  [{r['http']}] {r['url']}")
        total_bad = sum(bad.values())
        if total_bad:
            print("-" * 60, file=sys.stderr)
            if bad["404"]:
                print(f"❌ 404 × {bad['404']}：文件写进去了但 URL 取不到"
                      f"（dest_dir 与 url_base 不同层 / 站点 alias 不对 / 传到另一台机器）", file=sys.stderr)
            if bad["403"]:
                print(f"❌ 403 × {bad['403']}：目录被挡（鉴权/防盗链），Seedance 取不到 → 改走 base64",
                      file=sys.stderr)
            if bad["err"]:
                print(f"❌ 请求异常 × {bad['err']}：多为 URL 未编码或网络不通", file=sys.stderr)
            if bad["other"]:
                print(f"❌ 其它状态 × {bad['other']}", file=sys.stderr)
            print(f"   提示：先跑 --probe 确认落点与 URL 映射，再传全量", file=sys.stderr)


    # ------- 写清单 -------
    if args.dry_run:
        print("-" * 60)
        if is_dir and rm_src_dir and src != staging_dir:
            print(f"[dry-run] 清空后若源目录 {src} 已空，将连源目录本身一并删除（保留暂存目录 {staging_disp}）。")
        print("dry-run：未复制、未写清单" + ("（含未覆盖目标目录）" if replace_targets else "") + "。")
        return 0

    # 清单输出位置
    if args.manifest:
        mpath = Path(args.manifest).expanduser()
        if mpath.is_dir() or args.manifest.endswith(("/", os.sep)):
            out_dir = mpath
            prefix_name = manifest_name
        else:
            out_dir = mpath.parent if str(mpath.parent) else Path(".")
            prefix_name = mpath.stem or manifest_name
    else:
        out_dir = src if is_dir else src.parent
        prefix_name = manifest_name
    ensure_dir(out_dir)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dest_disp = str(dest_root)
    total = len(results)
    done_urls = [r for r in results if r["status"] in ("ok", "skip")]

    lines = []
    lines.append(f"# {prefix_name}")
    lines.append("")
    lines.append(f"- 外网根目录：{args.url_base.rstrip('/')}/")
    lines.append(f"- 源路径：{src}")
    lines.append(f"- 目标路径：{dest_disp}")
    lines.append(f"- 生成时间：{now}")
    if replaced_dirs:
        lines.append(f"- 覆盖目录：{replaced_dirs} 个（清除旧文件 {replaced_old_files} 个）")
    lines.append(f"- 文件总数：{total}（成功 {ok} · 跳过 {skipped} · 失败 {failed}）")
    lines.append(f"- 合计大小：{human_size(total_bytes)}")
    lines.append("")
    lines.append("| # | 相对路径 | 外网路径 |")
    lines.append("|---|----------|----------|")
    for i, r in enumerate(results, 1):
        rel = r["rel"].replace("|", "\\|")
        url = r["url"].replace("|", "\\|")
        lines.append(f"| {i} | {rel} | {url} |")
    if failed:
        lines.append("")
        lines.append("## 失败项")
        lines.append("")
        for r in results:
            if r["status"] == "fail":
                lines.append(f"- {r['rel']}（源：{r['src']}）")
    lines.append("")
    lines.append(f"> 外网路径 = 外网根目录 + 「{dest_disp}」之后的相对部分。")
    lines.append("")

    md_path = out_dir / f"{prefix_name}.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")

    txt_path = out_dir / f"{prefix_name}.txt"
    txt_path.write_text("\n".join(r["url"] for r in done_urls) + ("\n" if done_urls else ""), encoding="utf-8")

    written = [str(md_path), str(txt_path)]

    if args.json:
        json_path = out_dir / f"{prefix_name}.json"
        json_path.write_text(
            json.dumps({
                "url_base": args.url_base.rstrip("/") + "/",
                "src": str(src),
                "dest": dest_disp,
                "generated_at": now,
                "count": total,
                "ok": ok,
                "skipped": skipped,
                "failed": failed,
                "items": results,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        written.append(str(json_path))

    # ------- 清理源（默认：获得外链后删源；--purge-project 再清空整个源目录） -------
    deleted = 0
    purged = 0
    src_dir_removed = False
    if not keep_source:
        # 1) 删除已完成上传的源文件（开了 --verify 时核验未通过的保守保留）
        for r in results:
            if r["status"] not in ("ok", "skip"):
                continue
            if args.verify and not str(r.get("http", "")).startswith("2"):
                continue
            try:
                Path(r["src"]).unlink()
                r["source_deleted"] = True
                deleted += 1
            except Exception as e:  # noqa: BLE001
                print(f"  ✗ 删除源文件失败 {r['rel']}：{e}", file=sys.stderr)
        # 2) 项目清空：清空整个源目录内容（文件/子目录/隐藏文件/清单），只留源目录本身
        if is_dir and purge:
            purged = purge_dir_contents(src, keep=(".gitkeep",))
        elif is_dir:
            # 未开清空时：仅清理已被清空的子目录（自底向上），保留清单所在目录
            for root, _dirs, _names in os.walk(src, topdown=False):
                if Path(root) == src:
                    continue
                try:
                    os.rmdir(root)
                except OSError:
                    pass
        # 3) 清单若写到源目录之外，一并删除（项目清空时清单不留盘）
        if purge:
            for w in written:
                try:
                    Path(w).unlink()
                    purged += 1
                except FileNotFoundError:
                    pass
                except OSError as e:  # noqa: BLE001
                    print(f"  ✗ 删除清单失败 {w}：{e}", file=sys.stderr)
        # 4) 源目录本身：清空后若已完全为空、且不是暂存目录 assets/source，连目录一起删
        #    （--src 指到项目文件夹时，传完整个项目文件夹消失，只留暂存目录）
        if is_dir and rm_src_dir and src != staging_dir:
            try:
                if src.is_dir() and not any(src.iterdir()):
                    src.rmdir()
                    src_dir_removed = True
            except OSError as e:  # noqa: BLE001
                print(f"  ✗ 删除源目录失败 {src}：{e}", file=sys.stderr)
        if not args.quiet:
            if purge:
                src_label = f"{staging_disp}/" if src == staging_dir else f"{src.name}/"
                if src_dir_removed:
                    print(f"源项目：已清空并删除源目录（{src_label} 已移除，仅保留暂存目录 "
                          f"{staging_disp}/；清单未留盘）")
                else:
                    print(f"源项目：已清空源目录（{src_label} 仅保留目录本身；清单未留盘）")
            else:
                print(f"源素材：已删除 {deleted} 个（清单保留在源目录）"
                      if deleted else "源素材：无需删除")

    if not args.quiet:
        print("-" * 60)
        print(f"完成：成功 {ok} · 跳过 {skipped} · 失败 {failed}"
              + (f" · 覆盖目录 {replaced_dirs}" if replaced_dirs else "")
              + ("" if keep_source else f" · 已删源 {deleted}")
              + (f" · 已清空项目{'（含源目录）' if src_dir_removed else ''}" if purged else ""))
        if not purge:
            for w in written:
                print(f"清单：{w}")
        if not keep_source and deleted and not purge:
            print("提示：源素材已按外链清单删除；如需保留请加 --keep-source 重跑。")
        if purge and is_dir and src != staging_dir and keep_src_dir:
            print(f"提示：--keep-src-dir 生效，保留源目录空壳 {src}；去掉该开关可连目录一起删。")

    # ------- 外链清单（终端回显；清空项目后本地不再留盘） -------
    if not args.quiet and done_urls:
        print("-" * 60)
        print(f"外链清单（{len(done_urls)} 条）：")
        for r in done_urls:
            print(f"  {r['url']}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
