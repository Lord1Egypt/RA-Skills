#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
init_project.py — 一键生成长篇翻译项目骨架（含模板与操作清单）

解决两个常见痛点：
  1. 「配置项较多、初次使用要通读说明」→ 直接生成带注释的模板，填空即可，
     不用自己凭空造目录、造译者简报、造术语表。
  2. 「只想译几段却被整套流水线劝退」→ --scale light 生成精简版操作清单，
     只保留必要步骤，不强制切片/质检/术语表。

用法：
    python init_project.py <项目目录>                 # 完整流水线（默认，适合 300 页以上）
    python init_project.py <项目目录> --scale light   # 轻量模式（几段～几十页）
    python init_project.py <项目目录> --src en        # 指定源语言（默认 de）
    python init_project.py <项目目录> --no-copy       # 不拷贝脚本到项目内

产出：
    <项目目录>/
      source/           原文（解析后的 .md / .txt）
      work/chunks/      切片后的待译片段
      output/chunks/    译文片段 .md
      glossary/         术语表
      scripts/          本技能的脚本副本（便于按项目改 CONFIG）
      TRANSLATOR_BRIEF.md   译者简报模板（**开工前必须填**）
      glossary/术语对照.md   三语术语表模板
      RUNBOOK.md        本项目该跑哪些命令（按 scale 自动生成）
"""
import os
import sys
import shutil

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from _common import die, warn, opt
except ImportError:
    print("[出错] 找不到 _common.py —— 请确保它与本脚本在同一目录（scripts/）。",
          file=sys.stderr)
    sys.exit(1)

LANG_NAME = {
    "de": "德文", "en": "英文", "fr": "法文", "ja": "日文",
    "la": "拉丁文", "gr": "希腊文", "it": "意大利文", "ru": "俄文",
    "zh": "中文", "cn": "中文",
}

BRIEF_TMPL = """# 译者简报 · TRANSLATOR_BRIEF

> **开工前必填**。此文件是所有译者（含并行子代理）共同遵守的体例契约。
> 填好后，每个子代理的提示词都要写「先读 TRANSLATOR_BRIEF.md」。

## 0. 项目信息
- 原书：{title}
- 源语言：{src_name}　目标语言：{tgt_name}
- 规模：{scale_note}
- 参照外文版（如有）：（例：Oxford Handbook of Schleiermacher，用于术语核校）

## 1. 硬性体例（所有译者共守）

1. **页边码**：原书页码单独成行 `〔S. XXX〕`，保留以便核校与引用。
   （源文本页码常被打散成 `S. 5 3 3`，需还原为 `〔S. 533〕`）
2. **强调字体**：原文舒展字体（Sperrdruck / 斜体 / 逐字空格）还原为完整文句 + `**粗体**`，
   **绝不逐字直译**。
3. **脚注**：保留原编号，正文用上标 `⁷`，注文统一移到段末 `#### 原注` 小节。
4. **残句**：片段开头残句用 `> 〔承前页〕……`，结尾残句照译并以 `……` 收尾，**不编造补齐**。
5. **存疑必标**：任何不确定处加 `#### 译注`，格式：
   `N. 疑点。原文作「…」；对照版表述「…」；因…暂译作「…」，存疑。`
   **宁可多标，不可臆断。**
6. **文末三节**（每个片段文件都附，便于合并汇总）：
   ```
   #### 原注   （脚注译文）
   #### 译注   （存疑说明）
   #### 新术语 （本篇新定译名：原文 → 中文）
   ```

## 2. 术语约定
- 术语统一以 `glossary/术语对照.md` 为准：**同一原文词条全书唯一对应同一中文词**。
- 确需变通的，在 `#### 译注` 里说明理由，不要默默换词。
- 本篇新定的译名，务必写进文末 `#### 新术语`（合并时会自动汇总成全书总表）。

## 3. 本项目特殊约定
（按实际情况补充，例如：人名保留原文不译、书名用书名号、引文出处格式…）
- 
"""

GLOSSARY_TMPL = """# 术语对照表（{src_name} ⇄ 参照语言 ⇄ {tgt_name}）

> **铁律**：同一原文词条全书唯一对应同一中文词。
> 建表依据：原书缩写/索引表 + 参照外文版 + 学界通行译法。
> 译文中每片新定的译名，也要回填到这里（文末 `#### 新术语` 会自动汇总）。

| {src_name}原文 | 参照语言 | {tgt_name}定译 | 备注/出处 |
|---|---|---|---|
| 例：Dialektik | Dialectic | 辩证学 | 依 Oxford Handbook |
|  |  |  |  |

## 易混词
| 原文 | 定译 | 区分要点 |
|---|---|---|
|  |  |  |
"""

RUNBOOK_FULL = """# 操作清单 · {title}（完整流水线）

> 适用：300 页以上、需要术语全书统一、脚注保留的长篇译著。
> 所有命令在项目根目录下执行；脚本在本项目 `scripts/`（若报找不到，用 skill 自带那份）。

## 0. 开工前（一次性）
- [ ] 填好 `TRANSLATOR_BRIEF.md`（**必填**，体例契约）
- [ ] 建立 `glossary/术语对照.md`
- [ ] 安装依赖：`pip install markdown pypinyin`

## 1. 解析
- [ ] 把 PDF/图片转成文本，放 `source/`（可用 omni-reader 等 OCR 工具；有对照外文版一并解析）

## 2. 清洗切片
- [ ] 修 OCR 错字、删页眉页脚
- [ ] 按**原书结构**（篇章/页码区间）切片到 `work/chunks/`，写 manifest 记录每片起止页码
- [ ] **翻译开工前必跑**（防整段重复，代价最高的一步）：
      ```bash
      python scripts/overlap_check.py work/chunks --ext .txt
      ```

## 3. 并行翻译 → `output/chunks/*.md`
- [ ] 主线程译一批做样板，再派子代理并行译其余批（每片仅一个写者，批次严禁重叠）
- [ ] 子代理提示词必含：读 `TRANSLATOR_BRIEF.md` + 术语表 + 1 篇紧邻已译样本

## 4. 质检与修复
```bash
python scripts/qa_check.py output/chunks --expect <片段总数>
python scripts/dedup_boundary.py output/chunks           # 先 dry-run
python scripts/dedup_boundary.py output/chunks --apply   # 确认后再写盘
```
- [ ] 逐项清零或逐条确认可接受（注意：删除前先排除「结构性重复」）

## 5. 合并交付
```bash
python scripts/merge_build.py output/chunks output/<书名>   # 主稿 .md + 基础 .html
python scripts/build_reader.py                              # 增强阅读版 .html
```
（两个脚本用环境变量 `LB_BASE=<项目根目录>` 指定工作根）

## 6. 已知轻微接缝
切片边界常有 1–3 页页码接缝，**逐处强改代价高**，在交付说明中如实列出即可。
"""

RUNBOOK_LIGHT = """# 操作清单 · {title}（轻量模式）

> 适用：几段文字到几十页，**不需要**全书术语统一、不需要并行流水线。
> 轻量模式只保留必需步骤，跳过切片重叠检测与边界去重（片段少、无滑动窗口重叠风险）。

## 1. 准备
- [ ] 原文放 `source/`（或直接把待译文本贴进 `work/chunks/001.txt`）
- [ ] `TRANSLATOR_BRIEF.md` 至少填第 1 节的体例规则（页边码/脚注/存疑标注）

## 2. 翻译
- [ ] 直接译到 `output/chunks/001.md`（可按需分 002、003…）
- [ ] 保持文末三节：`#### 原注` / `#### 译注` / `#### 新术语`（没有就写「（无）」，
      这样后续若升级到完整流水线，脚本仍可直接用）

## 3. 可选质检（推荐跑一下，成本很低）
```bash
python scripts/qa_check.py output/chunks
```
主要看【3】未译残留 与【7】空文件；【5】页边码断档在少量片段下可忽略。

## 4. 合并输出
```bash
python scripts/merge_build.py output/chunks output/<书名>
python scripts/build_reader.py
```

## 什么时候该改用完整流水线？
- 篇幅超过 ~100 页，或
- 需要多人/多子代理并行，或
- 术语必须全书统一（学术出版级）
→ 重新跑 `python scripts/init_project.py . --scale full` 生成完整清单。
"""


def write(path, content, base=".", force=False):
    """写模板文件；base 用于打印「相对项目根」的短路径。"""
    try:
        show = os.path.relpath(path, base)
    except ValueError:          # 跨盘符时 relpath 会失败，退回文件名
        show = os.path.basename(path)
    if os.path.exists(path) and not force:
        warn("已存在，跳过（不覆盖）：%s" % show)
        return False
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✓ " + show)
    return True


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    proj = os.path.abspath(argv[0])
    scale = opt(argv, "--scale", default="full", cast=str,
                usage="python init_project.py <项目目录> --scale light")
    if scale not in ("full", "light"):
        die("--scale 只接受 full 或 light，收到：%r" % scale,
            "完整流水线：--scale full（300 页以上）",
            "轻量模式  ：--scale light（几段～几十页）")
    src = opt(argv, "--src", default="de", cast=str,
              usage="python init_project.py <项目目录> --src en")
    tgt = opt(argv, "--tgt", default="zh", cast=str,
              usage="python init_project.py <项目目录> --tgt zh")
    copy_scripts = "--no-copy" not in argv

    src_name = LANG_NAME.get(src, src)
    tgt_name = LANG_NAME.get(tgt, tgt)
    title = os.path.basename(proj) or "（未命名译著）"

    print("初始化项目：%s" % proj)
    print("  模式：%s（%s）" % (scale, "完整流水线" if scale == "full" else "轻量模式"))
    print("  语言：%s → %s\n" % (src_name, tgt_name))

    # 1. 目录骨架
    dirs = ["source", os.path.join("work", "chunks"),
            os.path.join("output", "chunks"), "glossary"]
    if scale == "full":
        pass  # 两个模式目录相同，差异体现在 RUNBOOK 与是否强调切片
    for d in dirs:
        p = os.path.join(proj, d)
        if not os.path.isdir(p):
            os.makedirs(p, exist_ok=True)
            print("  ✓ %s/" % d)
        else:
            print("  · %s/ （已存在）" % d)

    # 2. 模板文件
    print("\n模板文件：")
    scale_note = ("300 页以上长篇，完整流水线" if scale == "full"
                  else "轻量模式（几段～几十页），跳过并行与切片质检")
    write(os.path.join(proj, "TRANSLATOR_BRIEF.md"),
          BRIEF_TMPL.format(title=title, src_name=src_name,
                            tgt_name=tgt_name, scale_note=scale_note),
          base=proj)
    write(os.path.join(proj, "glossary", "术语对照.md"),
          GLOSSARY_TMPL.format(src_name=src_name, tgt_name=tgt_name),
          base=proj)
    tmpl = RUNBOOK_FULL if scale == "full" else RUNBOOK_LIGHT
    write(os.path.join(proj, "RUNBOOK.md"), tmpl.format(title=title),
          base=proj)

    # 3. 拷贝脚本
    if copy_scripts:
        here = os.path.dirname(os.path.abspath(__file__))
        dst = os.path.join(proj, "scripts")
        os.makedirs(dst, exist_ok=True)
        n = 0
        for f in os.listdir(here):
            if f.endswith(".py") and not f.startswith("__"):
                shutil.copy2(os.path.join(here, f), os.path.join(dst, f))
                n += 1
        print("\n脚本副本：%d 个 → %s" % (n, os.path.relpath(dst, proj)))
        print("  （按项目改各脚本顶部的 CONFIG 区即可；改用 --no-copy 可跳过）")

    # 4. 下一步
    print("\n" + "=" * 56)
    print("下一步：")
    print("  1. 打开 %s 填空（**开工前必填**）" %
          os.path.join(proj, "TRANSLATOR_BRIEF.md"))
    print("  2. 原文放 source/，按 RUNBOOK.md 的步骤推进")
    if scale == "full":
        print("  3. 切片后、翻译前，务必先跑 overlap_check.py（防整段重复）")
    print("=" * 56)


if __name__ == "__main__":
    main()
