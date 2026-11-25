#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kb-distiller 产物 skill 机械化校验脚本（纯 stdlib，Windows 兼容）。

用法:
    python validate_skill.py <产物目录> [--keywords kw1,kw2,...]

退出码: 0 = 全部通过; 1 = 存在失败项。
本脚本是 pre-filter: 通过不代表内容正确，仍需 agent 抽查来源标注与内容真实性。
"""
import argparse
import os
import re
import sys

MAX_NAME_LEN = 64
MAX_DESC_LEN = 1024
MAX_LINES = 2000
MAX_TOTAL_BYTES = 2 * 1024 * 1024
KEYWORD_COVERAGE_RATIO = 0.8

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"


def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        sys.stdout.buffer.write((text + "\n").encode("utf-8", errors="replace"))


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, name, detail=""):
        self.items.append((level, name, detail))
        mark = {"PASS": "[PASS]", "FAIL": "[FAIL]", "WARN": "[WARN]"}[level]
        safe_print("{} {}{}".format(mark, name, (" - " + detail) if detail else ""))

    @property
    def failed(self):
        return any(level == FAIL for level, _, _ in self.items)

    def summary(self):
        total = len(self.items)
        passed = sum(1 for lv, _, _ in self.items if lv == PASS)
        failed = sum(1 for lv, _, _ in self.items if lv == FAIL)
        warned = sum(1 for lv, _, _ in self.items if lv == WARN)
        safe_print("")
        safe_print("==== 校验摘要: {} 项, 通过 {}, 失败 {}, 警告 {} ====".format(total, passed, failed, warned))
        return failed == 0


def parse_frontmatter(text):
    """解析 SKILL.md frontmatter。返回 (meta_dict, error)。只支持平铺 key: value。"""
    if not text.startswith("---"):
        return None, "文件不以 '---' 开头, 缺少 frontmatter"
    lines = text.splitlines()
    if len(lines) < 2:
        return None, "frontmatter 为空"
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None, "frontmatter 未闭合 (缺少第二个 '---')"
    meta = {}
    for line in lines[1:end_idx]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$", line)
        if not m:
            return meta, "无法解析的 frontmatter 行: {!r}".format(line)
        key, value = m.group(1), m.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        meta[key] = value
    return meta, None


def read_utf8(path):
    with open(path, "rb") as f:
        raw = f.read()
    try:
        return raw.decode("utf-8-sig"), None
    except UnicodeDecodeError as e:
        return None, "非 UTF-8 编码: {}".format(e)


def find_nested_skill_md(root):
    """查找产物目录内除根 SKILL.md 外的其他 SKILL.md。"""
    found = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn == "SKILL.md":
                full = os.path.join(dirpath, fn)
                if os.path.normcase(os.path.abspath(full)) != os.path.normcase(
                    os.path.abspath(os.path.join(root, "SKILL.md"))
                ):
                    found.append(os.path.relpath(full, root))
    return found


def main():
    parser = argparse.ArgumentParser(description="kb-distiller 产物校验")
    parser.add_argument("skill_dir", help="产物 skill 目录 (内含 SKILL.md 与 kb/)")
    parser.add_argument("--keywords", default="", help="逗号分隔的 description 关键词")
    args = parser.parse_args()

    report = Report()
    root = args.skill_dir

    if not os.path.isdir(root):
        report.add(FAIL, "目录存在", "目录不存在: {}".format(root))
        sys.exit(1)
    report.add(PASS, "目录存在", root)

    skill_md = os.path.join(root, "SKILL.md")
    if not os.path.isfile(skill_md):
        report.add(FAIL, "SKILL.md 存在", "缺少 {}".format(skill_md))
        safe_print("==== 校验失败 ====")
        sys.exit(1)
    report.add(PASS, "SKILL.md 存在")

    # frontmatter
    text, err = read_utf8(skill_md)
    if err:
        report.add(FAIL, "SKILL.md 编码", err)
        safe_print("==== 校验失败 ====")
        sys.exit(1)
    report.add(PASS, "SKILL.md UTF-8 编码")

    meta, fm_err = parse_frontmatter(text)
    if meta is None:
        report.add(FAIL, "frontmatter 可解析", fm_err or "未知错误")
        safe_print("==== 校验失败 ====")
        sys.exit(1)
    if fm_err:
        report.add(WARN, "frontmatter 内容", fm_err)
    else:
        report.add(PASS, "frontmatter 可解析")

    # name
    name = meta.get("name", "")
    if not name:
        report.add(FAIL, "name 存在", "frontmatter 缺少 name")
    else:
        ok = re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) is not None
        if not ok:
            report.add(FAIL, "name 格式", "须为小写字母数字+连字符: {!r}".format(name))
        elif len(name) > MAX_NAME_LEN:
            report.add(FAIL, "name 长度", "{} > {} 字符".format(len(name), MAX_NAME_LEN))
        else:
            folder = os.path.basename(os.path.normpath(root))
            if name != folder:
                report.add(FAIL, "name 与目录同名", "name={!r} 但目录名={!r}".format(name, folder))
            else:
                report.add(PASS, "name 合规", name)

    # description
    desc = meta.get("description", "")
    if not desc:
        report.add(FAIL, "description 存在", "缺失 description 的 skill 会被加载器过滤, 永远不生效")
    elif len(desc) < 20:
        report.add(FAIL, "description 长度", "过短 ({} 字符), 须说明做什么+何时触发".format(len(desc)))
    elif len(desc) > MAX_DESC_LEN:
        report.add(FAIL, "description 长度", "{} > {} 字符".format(len(desc), MAX_DESC_LEN))
    else:
        report.add(PASS, "description 合规", "长度 {}".format(len(desc)))

    # 关键词覆盖
    if args.keywords:
        kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        missing = [k for k in kws if k not in desc]
        ratio = 1 - len(missing) / len(kws) if kws else 1
        if ratio < KEYWORD_COVERAGE_RATIO:
            report.add(FAIL, "关键词覆盖", "覆盖率 {:.0f}% < {:.0f}%, 缺失: {}".format(
                ratio * 100, KEYWORD_COVERAGE_RATIO * 100, ", ".join(missing)))
        else:
            report.add(PASS, "关键词覆盖", "覆盖率 {:.0f}%{}".format(
                ratio * 100, (" (缺失: " + ", ".join(missing) + ")") if missing else ""))

    # kb 目录
    kb_dir = os.path.join(root, "kb")
    if not os.path.isdir(kb_dir):
        report.add(FAIL, "kb/ 目录存在", "缺少 kb/ 知识库目录")
        kb_files = []
    else:
        kb_files = sorted(
            os.path.join(kb_dir, fn) for fn in os.listdir(kb_dir)
            if fn.endswith(".md") and os.path.isfile(os.path.join(kb_dir, fn))
        )
        if not kb_files:
            report.add(FAIL, "kb 文件存在", "kb/ 内没有 .md 文件")
        else:
            report.add(PASS, "kb 文件存在", "{} 个文件".format(len(kb_files)))

    # 每个 kb 文件
    for path in kb_files:
        rel = os.path.relpath(path, root)
        body, enc_err = read_utf8(path)
        if enc_err:
            report.add(FAIL, "kb 编码 [{}]".format(rel), enc_err)
            continue
        if not body.strip():
            report.add(FAIL, "kb 非空 [{}]".format(rel), "文件为空")
            continue
        n_lines = len(body.splitlines())
        if n_lines > MAX_LINES:
            report.add(FAIL, "kb 行数 [{}]".format(rel), "{} 行 > {} 行, 须在蒸馏阶段拆分".format(n_lines, MAX_LINES))
        else:
            report.add(PASS, "kb 行数 [{}]".format(rel), "{} 行".format(n_lines))
        if "来源索引" not in body and not re.search(r"^#+\s*来源", body, re.M):
            report.add(FAIL, "kb 来源索引 [{}]".format(rel), "缺少必需的「来源索引」小节")
        else:
            report.add(PASS, "kb 来源索引 [{}]".format(rel))
        # 法则小节检查（subdomain kb 必须有「## 法则」；横切文件跳过）
        fm_block = re.match(r"^---\s*\n(.*?\n)---", body, re.S)
        if fm_block and re.search(r"^subdomain\s*:", fm_block.group(1), re.M):
            if not re.search(r"^##\s*法则", body, re.M):
                report.add(FAIL, "kb 法则小节 [{}]".format(rel), "subdomain kb 缺少「## 法则」小节")
            else:
                law_count = len(re.findall(r"\[[A-Z]{2,5}-\d+\]", body))
                report.add(PASS, "kb 法则小节 [{}]".format(rel), "{} 条编号条款".format(law_count))

    # laws.md 全局宪法（默认横切文件）
    laws_md = os.path.join(kb_dir, "laws.md")
    if os.path.isfile(laws_md):
        laws_body, _laws_err = read_utf8(laws_md)
        n_laws = len(set(re.findall(r"LAW-\d+", laws_body or "")))
        if n_laws == 0:
            report.add(WARN, "laws.md 宪法条款", "存在但未发现 LAW-N 编号条款")
        else:
            report.add(PASS, "laws.md 宪法条款", "{} 条 LAW 条款".format(n_laws))
    else:
        report.add(WARN, "laws.md 存在", "缺少全局宪法 kb/laws.md（默认横切文件）")

    # 总体积
    total = 0
    for dirpath, _dn, filenames in os.walk(root):
        for fn in filenames:
            total += os.path.getsize(os.path.join(dirpath, fn))
    if total > MAX_TOTAL_BYTES:
        report.add(FAIL, "总体积", "{} KB > {} KB (上下文经济性红线)".format(total // 1024, MAX_TOTAL_BYTES // 1024))
    else:
        report.add(PASS, "总体积", "{} KB / {} KB".format(total // 1024, MAX_TOTAL_BYTES // 1024))

    # 嵌套 SKILL.md
    nested = find_nested_skill_md(root)
    if nested:
        report.add(FAIL, "嵌套 SKILL.md 检查", "发现多余 SKILL.md: {}".format(", ".join(nested)))
    else:
        report.add(PASS, "嵌套 SKILL.md 检查", "仅根 SKILL.md")

    ok = report.summary()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
