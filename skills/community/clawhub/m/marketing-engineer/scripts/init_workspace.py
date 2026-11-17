#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Marketing Engineer 工作区脚手架。

用法:
    python3 init_workspace.py <目标目录> [--product <产品名>] [--with-dashboard]

在目标目录创建 Marketing Engineer 标准营销工作区骨架:
shared-knowledge + 五个垂直域 + launch-campaigns + raw，每个目录带 README 骨架（含 TODO 提示）。
已存在的文件不覆盖。

--with-dashboard：一并部署驾驶舱三件套（scripts/scan_workspace.py、build_dashboard.py、
serve_dashboard.py）并生成 dashboard.html —— 之后「工作区全景」即可用（左目录树 / 右文件列表，
每个文件可点开看，支持明亮/暗夜）。
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

README_ROOT = """# {product} 营销工作区

> 方法论：Marketing Engineer（知识层 → 垂直域 → 工单管线 → 审核闭环 → 数据回流）

## 铁律

1. 先读后写：任何产出前先查 shared-knowledge；没有的事实先调研入库（带来源+日期）再动笔。
2. 证据留痕：事实带来源+日期；未核实标 [未验证]，不流入成品。
3. 发布必须人工审批；台账以线上实际发布版本为准。
4. 口径一致性：术语/域名/免费表述等全渠道唯一且一致。
5. 密钥只进 .env。
6. 产出归位：草稿/成品/台账按目录约定存放。
7. 不点名竞品贬损；定价未定稿不出现具体价格。
8. 优先调用已装增强 skill（外部研究 / 方案质询 / 规格冻结 / 工单拆分 / 调研落档），
   清单与接入点见 shared-knowledge/toolchain.md；其产出仍是草稿，必须走人审。

## 结构

见 shared-knowledge/README.md 与各垂直域 README。

## 驾驶舱（建议随第一批内容一起建）

根目录的 dashboard.html 是单文件视图：**左边选目录、右边看文件**，每个文件可点开查看
（Markdown 渲染 / 图片预览 / 代码一键复制），支持明亮与暗夜两种模式。

- 手动刷新：`python3 scripts/build_dashboard.py .`
- 实时扫描：`python3 scripts/serve_dashboard.py . 8799` → http://127.0.0.1:8799/dashboard.html
- 铁律：**看板是视图不是源**，从台账/工单/渠道/周报派生；新增文件无需登记，扫描器自动归类。
"""

README_SK = """# shared-knowledge —— 唯一可引用来源

| 文件 | 说明 | 状态 |
|---|---|---|
| product-and-offer.md | 产品事实：定位/模块/官方话术/Offer/内部数据 | TODO |
| positioning.md | 定位与差异化（含待验证假设区） | TODO |
| brand-voice.md | 语音/术语表/视觉规范/审核自查清单 | TODO |
| audience.md | 受众画像 | TODO |
| channels.md | 自有渠道清单 + 分组打法 | TODO |
| toolchain.md | 外部增强 skill 工具链：来源/许可/审计结论/接入点 | TODO |

规则：本目录之外的来源不得直接对外引用；新增事实必须带来源+日期。
"""

TOOLCHAIN_MD = """# 外部增强 skill 工具链

> 规则：安装任何第三方 skill 前必须做安全检查（审查 SKILL.md 与全部 bundled files），
> 并在此登记来源、许可、风险等级与接入点。未安装时按降级路径执行，不阻塞流程。

## 已安装

| Skill | 来源 / 许可 | 用途 | 风险等级 | 接入的工作流环节 |
|---|---|---|---|---|
| （示例）last30days | github.com/mvanhorn/last30days-skill · MIT | 近 30 天跨平台真实讨论与互动数据 | P1（cookie 能力默认关闭） | 选题 / 竞品监控 / 关键词调研 |
| （示例）grilling、to-spec、to-tickets、research | github.com/mattpocock/skills · MIT | 方案质询 / 规格冻结 / 工单拆分 / 调研落档 | P2 | 送审前压测、工单管线 |

## 接入点纪律

- skill 产出仍是草稿 → 必须走人审；台账以线上实际发布版本为准。
- cookie / 本地凭据读取类能力默认关闭，须用户显式授权；API key 只进 `.env`。
- 降级路径：研究类用多路搜索采样（结论标 [未验证]）；规格/工单类按工作区骨架手写。
"""

README_V = """# {domain}

TODO: 本垂直域的产出按「先读 shared-knowledge → 工单/计划 → 送审 → 归位」流程管理。
"""

RAW_GITKEEP = ""

FOLDERS_JSON = """{
  "_说明": "可选：定制驾驶舱里每个目录的中文名/角色/一句话说明。键=目录相对路径（'' 表示根目录）。",
  "": ["__PRODUCT__ 营销工作区", "根层", "分层：定稿口径 → 垂直域 → 结构方案 → 构建 → 记忆。"],
  "shared-knowledge": ["唯一可引用来源", "根层", "品牌、产品、渠道的定稿口径；改这里 = 改全局。"]
}
"""

DIRS = [
    "content",
    "geo-seo/knowledge",
    "geo-seo/workflows",
    "geo-seo/plans",
    "geo-seo/results-and-learnings",
    "outbound",
    "competitor-intel/research",
    "launch-campaigns",
    "shared-knowledge/assets",
]

SKILL_SCRIPTS = ['scan_workspace.py', 'build_dashboard.py', 'serve_dashboard.py']


def deploy_dashboard(root: Path, product: str):
    """把驾驶舱三件套复制进工作区 scripts/，并生成 dashboard.html。"""
    src_dir = Path(__file__).resolve().parent
    dst_dir = root / 'scripts'
    dst_dir.mkdir(parents=True, exist_ok=True)
    for name in SKILL_SCRIPTS:
        s, d = src_dir / name, dst_dir / name
        if s.exists():
            shutil.copy2(s, d)
            print(f"  + scripts/{name}")
    # 骨架放 .cache/（扫描器会跳过该目录，不污染工作区语义）
    sk_src = src_dir.parent / 'assets' / 'dashboard-skeleton.html'
    if sk_src.exists():
        (root / '.cache').mkdir(parents=True, exist_ok=True)
        shutil.copy2(sk_src, root / '.cache' / 'dashboard-skeleton.html')
        print("  + .cache/dashboard-skeleton.html")
    fj = root / 'workspace-folders.json'
    if not fj.exists():
        fj.write_text(FOLDERS_JSON.replace('__PRODUCT__', product), encoding='utf-8')
        print("  + workspace-folders.json（可定制目录说明）")
    py = sys.executable or 'python3'
    r = subprocess.run([py, str(dst_dir / 'build_dashboard.py'), str(root), '--title', product],
                       capture_output=True, text=True)
    print((r.stdout or '').strip() or (r.stderr or '').strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--product", default="产品")
    ap.add_argument("--with-dashboard", action="store_true",
                    help="一并部署驾驶舱三件套并生成 dashboard.html")
    args = ap.parse_args()

    root = Path(args.target).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    def write(path: Path, content: str):
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"  + {path.relative_to(root)}")
        else:
            print(f"  . {path.relative_to(root)} (已存在，跳过)")

    write(root / "README.md", README_ROOT.format(product=args.product))
    write(root / "shared-knowledge" / "README.md", README_SK)
    write(root / "shared-knowledge" / "toolchain.md", TOOLCHAIN_MD)
    for name in ["product-and-offer", "positioning", "brand-voice", "audience", "channels"]:
        write(root / "shared-knowledge" / f"{name}.md",
              f"# {name}\n\n> TODO: 按 shared-knowledge/README.md 的说明填写。所有事实带来源+日期。\n")
    for d in DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
    for d in ["content", "geo-seo", "outbound", "competitor-intel", "launch-campaigns"]:
        write(root / d / "README.md", README_V.format(domain=d))
    write(root / "raw" / ".gitkeep", RAW_GITKEEP)
    print(f"\n✅ 工作区就绪：{root}")
    if args.with_dashboard:
        print("\n部署驾驶舱：")
        deploy_dashboard(root, args.product)
    print("\n下一步：先填 shared-knowledge 五件套（+ toolchain.md 登记外部 skill），再启动第一个 campaign。")

if __name__ == "__main__":
    main()
