r"""
template.py - LaTeX 模板生成器（template 模式）
模板库 + 按类型生成 + 自定义保存 + 内容注入

用法:
  # 按类型（兼容旧版）
  python scripts/template.py --type article --title "论文" --author "我"

  # 按模板名
  python scripts/template.py --template report --title "报告"

  # 注入自定义正文内容
  python scripts/template.py --template article --content "\\section{自定义}我的内容"

  # 列表/查看模板
  python scripts/template.py --list-templates
  python scripts/template.py --show-template article

  # 保存当前配置为新模板
  python scripts/template.py --template article --save-as my-thesis

  # 搜索模板
  python scripts/template.py --search 论文

  # 输出模式
  python scripts/template.py --template article --output-mode pdf
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# ── 内置数据（兼容旧版 --no-sample） ──────────────────────

BODY_SKELETON = r"""
% --- 标题 ---
\title{\timu{TITLE_PLACEHOLDER}}
\author{AUTHOR_PLACEHOLDER}
\date{\today}

\maketitle

\section{引言}

在此处撰写引言内容。

\section{主体}

在此处撰写主体内容。

\section{结论}

在此处撰写结论。
"""

# ── 工具函数 ──────────────────────────────────────────────

def find_skill_dir() -> str:
    return str(Path(__file__).resolve().parent.parent)


def templates_dir() -> str:
    return os.path.join(find_skill_dir(), "scripts", "templates")


def read_manifest(manifest_path: str) -> dict:
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)


def discover_components(manifest: dict) -> list:
    comps = manifest.get("components", [])
    if isinstance(comps, dict):
        new_list = []
        for key, val in comps.items():
            typ, name = (key.split("/", 1) + [""])[:2]
            new_list.append({
                "type": typ, "name": name,
                "path": val.get("file", f"{typ}/{name}.txt"),
                "description": val.get("desc", "")
            })
        return new_list
    return comps


# ── 模板库管理 ────────────────────────────────────────────

def list_templates() -> list:
    """列出所有可用模板"""
    td = templates_dir()
    if not os.path.isdir(td):
        return []
    results = []
    for fname in sorted(os.listdir(td)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(td, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            results.append({
                "name": data.get("name", fname[:-5]),
                "description": data.get("description", ""),
                "type": data.get("type", "custom"),
                "version": data.get("version", "?"),
                "file": fname,
            })
        except Exception:
            results.append({"name": fname[:-5], "description": "(加载失败)", "type": "unknown", "file": fname})
    return results


def load_template(name: str) -> dict:
    """按模板名加载模板定义"""
    td = templates_dir()
    # 直接尝试文件名
    for ext in ["", ".json"]:
        fpath = os.path.join(td, name + ext)
        if os.path.isfile(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                return json.load(f)
    return None


def save_template(name: str, data: dict) -> str:
    """保存模板定义到文件"""
    td = templates_dir()
    os.makedirs(td, exist_ok=True)
    data["name"] = name
    data["version"] = data.get("version", "1.0.0")
    data["type"] = "custom"
    fpath = os.path.join(td, name + ".json")
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return fpath


def search_templates(keyword: str) -> list:
    """在模板库中搜索"""
    keyword = keyword.lower()
    results = []
    for t in list_templates():
        if keyword in t["name"].lower() or keyword in t["description"].lower():
            results.append(t)
    return results


def show_template(name: str) -> dict:
    """显示模板详情"""
    data = load_template(name)
    if not data:
        return None
    return data


def generate_body_from_template(template: dict, params: dict, sample: bool = True) -> str:
    """根据模板定义生成 body.tex 内容"""
    if not sample:
        content = template.get("body_skeleton", template.get("body_template", ""))
    else:
        content = template.get("body_template", "")

    if not content:
        return ""

    # 如有示例章节模板，拼接示例内容
    if sample:
        sections = template.get("sample_sections", [])
        if sections:
            section_content = ""
            for sec in sections:
                heading = sec.get("heading", "")
                sec_content = sec.get("content", "")
                section_content += f"\\section{{{heading}}}\n\n{sec_content}\n\n"
            content = content.replace("__CONTENT__", section_content.strip())
        else:
            content = content.replace("__CONTENT__", "")

    # 替换占位符
    content = content.replace("__TITLE__", params.get("title", "文档标题"))
    content = content.replace("__AUTHOR__", params.get("author", "作者姓名"))
    content = content.replace("__ABSTRACT__", params.get("abstract", template.get("body_abstract", "")))
    # 注入自定义正文内容（如果提供了 --content）
    if "__CONTENT__" in content:
        injected = params.get("content", "")
        if injected:
            content = content.replace("__CONTENT__", injected)
        else:
            content = content.replace("__CONTENT__", "")

    return content


# ── compose / validate 调用 ──────────────────────────────

def call_compose(skill_dir: str, manifest_path: str, output_path: str,
                 engine: str, title: str = "", author: str = "") -> dict:
    compose_script = os.path.join(skill_dir, "scripts", "compose.py")
    if not os.path.exists(compose_script):
        return {"success": False, "error": f"compose.py not found: {compose_script}"}
    cmd = [
        sys.executable, compose_script,
        "--manifest", manifest_path,
        "--output", output_path,
        "--engine", engine,
    ]
    if title:
        cmd.extend(["--title", title])
    if author:
        cmd.extend(["--author", author])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "compose.py 超时（>120s）"}
    except Exception as e:
        return {"success": False, "error": f"compose.py 调用异常: {e}"}


def validate_tex(tex_path: str, engine: str = "lualatex") -> dict:
    try:
        proc = subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", tex_path],
            capture_output=True, text=True, timeout=120
        )
        pdf_path = Path(tex_path).with_suffix(".pdf")
        pdf_ok = pdf_path.exists() and pdf_path.stat().st_size > 0
        errors = []
        for line in proc.stdout.splitlines():
            if line.startswith("!"):
                errors.append(line[:150])
        return {"success": proc.returncode == 0 and pdf_ok, "errors": errors,
                "pdf_path": str(pdf_path) if pdf_ok else None, "returncode": proc.returncode}
    except Exception as e:
        return {"success": False, "errors": [str(e)], "pdf_path": None}


def cleanup_aux(tex_path: str):
    base = Path(tex_path).with_suffix("")
    for ext in [".log", ".aux", ".out", ".toc", ".lof", ".lot", ".bbl", ".blg"]:
        p = base.with_suffix(ext)
        if p.exists():
            try:
                from safe_write import safe_delete
                safe_delete(str(p), backup=False)
            except Exception:
                p.unlink()


# ── 主入口 ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="LaTeX 模板生成器（template 模式）— 模板库 + 自定义保存",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # 模板选择（互斥：--type 兼容旧版，--template 新方式）
    tg = parser.add_argument_group("模板选择")
    tg.add_argument("--type", default="", choices=["article", "report"],
                    help="文档类型: article(论文) / report(报告)（兼容旧版）")
    tg.add_argument("--template", default="",
                    help="从模板库按名称加载模板（优先级高于 --type）")
    tg.add_argument("--list-templates", action="store_true",
                    help="列出所有可用模板")
    tg.add_argument("--show-template", default="",
                    help="显示指定模板的详情")
    tg.add_argument("--search", default="",
                    help="搜索模板（匹配名称和描述）")

    # 内容参数
    cg = parser.add_argument_group("文档内容")
    cg.add_argument("--title", default="文档标题", help="文档标题")
    cg.add_argument("--author", default="作者姓名", help="作者")
    cg.add_argument("--abstract", default="", help="摘要内容（仅 article 模板有效）")
    cg.add_argument("--content", default="",
                    help="自定义正文内容（LaTeX 代码，会替换模板中的样本内容）")
    cg.add_argument("--no-sample", action="store_true",
                    help="不生成示例正文，只输出骨架")

    # 模板管理
    mg = parser.add_argument_group("模板管理")
    mg.add_argument("--save-as", default="",
                    help="将当前配置保存为新模板名称")
    mg.add_argument("--save-description", default="",
                    help="保存模板时的描述")

    # 输出参数
    og = parser.add_argument_group("输出控制")
    og.add_argument("--manifest", default="",
                    help="manifest.json 路径  默认: <skill>/scripts/components/manifest.json")
    og.add_argument("--output", "-o", default="template_output.tex",
                    help="输出 .tex 路径  默认: template_output.tex")
    og.add_argument("--engine", default="lualatex",
                    help="LaTeX 引擎 (lualatex/xelatex)  默认: lualatex")
    og.add_argument("--output-mode", default="tex", choices=["tex", "pdf"],
                    help="输出模式: tex(验证后保留代码) / pdf(保留 .tex+.pdf)  默认: tex")
    og.add_argument("--skip-validation", action="store_true",
                    help="跳过编译验证（快速迭代用）")

    args = parser.parse_args()

    skill_dir = find_skill_dir()

    # ── 模板库操作（不生成文档） ──────────────────────
    if args.list_templates:
        templates = list_templates()
        if not templates:
            print("[template] 模板库为空")
            return
        print(f"[template] 模板库 ({len(templates)} 个):")
        print(f"  {'名称':<20s} {'类型':<10s} {'描述'}")
        print(f"  {'-'*60}")
        for t in templates:
            print(f"  {t['name']:<20s} {t['type']:<10s} {t['description']}")
        return

    if args.show_template:
        data = show_template(args.show_template)
        if not data:
            print(f"[template] 模板不存在: {args.show_template}")
            sys.exit(1)
        print(f"[template] 模板详情: {data.get('name')}")
        print(f"  描述: {data.get('description', '(无)')}")
        print(f"  类型: {data.get('type', 'custom')}")
        print(f"  版本: {data.get('version', '?')}")
        styles = data.get("styles", {})
        if styles:
            print(f"  样式参数 ({len(styles)} 项):")
            for k, v in styles.items():
                print(f"    {k}: {v}")
        return

    if args.search:
        results = search_templates(args.search)
        if not results:
            print(f"[template] 未找到匹配 '{args.search}' 的模板")
            return
        print(f"[template] 找到 {len(results)} 个匹配模板:")
        for t in results:
            print(f"  {t['name']:<20s} {t['description']}")
        return

    # ── 确定使用哪个模板 ──────────────────────────────
    template_name = args.template or args.type or "article"
    template = load_template(template_name)

    if template is None and args.type:
        # --type 内置类型未找到模板文件，降级用旧版硬编码
        print(f"[template] 模板文件不存在，使用内置类型: {args.type}")
        template = None
    elif template is None:
        print(f"[template] 模板不存在: {template_name}")
        sys.exit(1)

    # 读取 manifest
    manifest_path = args.manifest
    if not manifest_path:
        manifest_path = os.path.join(skill_dir, "scripts", "components", "manifest.json")
    if not os.path.isfile(manifest_path):
        print(f"[ERROR] manifest.json not found: {manifest_path}")
        sys.exit(1)
    manifest = read_manifest(manifest_path)
    comps = discover_components(manifest)
    print(f"[template] 加载组件库: {len(comps)} 个组件")

    # ── 保存模板 ──────────────────────────────────────
    if args.save_as:
        if template:
            save_data = dict(template)  # 深拷贝
        else:
            save_data = {
                "name": args.save_as,
                "version": "1.0.0",
                "description": args.save_description or f"自定义模板: {args.save_as}",
                "type": "custom",
                "styles": {},
                "body_template": "",
                "body_skeleton": BODY_SKELETON.strip(),
            }
        save_data["description"] = args.save_description or save_data.get("description", "")
        path = save_template(args.save_as, save_data)
        print(f"[template] 模板已保存: {path}")
        # 保存后继续生成文档
        template = load_template(args.save_as)

    # 旧版 --type 兼容：如果没用模板文件，降级到硬编码
    using_builtin_fallback = template is None
    if using_builtin_fallback:
        if args.no_sample:
            body_content = BODY_SKELETON
            body_content = body_content.replace("TITLE_PLACEHOLDER", args.title)
            body_content = body_content.replace("AUTHOR_PLACEHOLDER", args.author)
        else:
            from types import SimpleNamespace
            fake_template = SimpleNamespace()
            if args.type == "report":
                fake_template.body = r"""
\title{\timu{TITLE}}
\author{AUTHOR}
\date{\today}

\maketitle
\thispagestyle{empty}
\newpage

\tableofcontents
\newpage

\section{项目概述}

本报告旨在对关键技术方案进行全面评估。

\section{技术方案}

\subsection{架构设计}

本方案采用微服务架构。

\section{总结}

本报告对项目的技术方案和实施计划进行了全面阐述。
"""
            else:
                fake_template.body = r"""
\title{\timu{TITLE}}
\author{AUTHOR}
\date{\today}

\begin{abstract}
本文基于模块化设计理念，提出了一种全新的文档生成方法。
\end{abstract}

\section{引言}

本文提出的模块化模板方案通过以下方式解决上述问题。

\section{方法}

\subsection{组件化架构}

本系统的核心思想是将 LaTeX 文档划分为若干独立组件。

\section{结论}

本文提出的模块化 LaTeX 文档生成方案，显著简化了文档编写流程。
"""
            body_content = fake_template.body
            body_content = body_content.replace("TITLE", args.title)
            body_content = body_content.replace("AUTHOR", args.author)
    else:
        # ── 正常模板模式 ──────────────────────────────
        print(f"[template] 使用模板: {template.get('name')} ({template.get('description')})")
        params = {
            "title": args.title,
            "author": args.author,
            "abstract": args.abstract,
            "content": args.content,
        }
        body_content = generate_body_from_template(template, params, sample=not args.no_sample)

    # ── 写入 body.tex ─────────────────────────────────
    components_dir = os.path.dirname(manifest_path)
    body_path = os.path.join(components_dir, "body.txt")
    with open(body_path, "w", encoding="utf-8") as f:
        f.write(body_content.lstrip("\n") + "\n")
    print(f"[template] body 已写入: {body_path}")

    # ── 调用 compose.py 组装 ─────────────────────────
    print(f"[template] 调用 compose.py 组装文档...")
    out_path = os.path.abspath(args.output)
    result = call_compose(skill_dir, manifest_path, out_path, args.engine,
                          title=args.title, author=args.author)

    if not result["success"]:
        print(f"[template] FAIL 组装失败:")
        if "error" in result:
            print(f"  {result['error']}")
        if result.get("stdout"):
            print(f"  stdout: {result['stdout'][:300]}")
        if result.get("stderr"):
            print(f"  stderr: {result['stderr'][:300]}")
        sys.exit(1)

    print(f"[template] OK 文档已生成: {out_path}")

    # ── 编译验证（默认执行） ──────────────────────────
    if args.skip_validation:
        print(f"[template] 跳过编译验证（--skip-validation）")
        print(f"[template] 输出: {out_path}")
    else:
        print(f"[template] 编译验证 ({args.engine})...")
        val_result = validate_tex(out_path, args.engine)
        if val_result["success"]:
            pdf_path = val_result.get("pdf_path")
            print(f"[template] OK 编译验证通过")
        else:
            print(f"[template] FAIL 编译验证失败:")
            for e in val_result.get("errors", []):
                print(f"  ! {e}")
            print(f"[template] 保留 .tex 和 .log 供调试: {out_path}")
            sys.exit(1)

        if args.output_mode == "tex":
            pdf_path = val_result.get("pdf_path")
            if pdf_path and os.path.exists(pdf_path):
                from safe_write import safe_delete
                safe_delete(pdf_path, backup=False)
            cleanup_aux(out_path)
            print(f"[template] 输出模式: tex（已验证代码，PDF 已清除）")
            print(f"[template] 输出: {out_path}")
        else:
            cleanup_aux(out_path)
            print(f"[template] 输出模式: pdf")
            print(f"[template] 输出: {out_path}")
            print(f"[template] 输出: {val_result.get('pdf_path')}")


if __name__ == "__main__":
    main()
