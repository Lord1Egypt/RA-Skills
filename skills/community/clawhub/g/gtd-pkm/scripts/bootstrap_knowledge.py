#!/usr/bin/env python3
"""Scaffold a GTD-oriented knowledge repository for OpenClaw."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from textwrap import dedent

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None


DIRS = [
    "00-收集箱",
    "10-工作/01-主业",
    "10-工作/02-副业",
    "10-工作/03-AI",
    "20-项目",
    "30-记录/01-日志",
    "30-记录/02-灵感",
    "30-记录/03-周报",
    "30-记录/04-会议",
    "40-学习/01-读书笔记",
    "40-学习/02-课程笔记",
    "40-学习/03-技术",
    "40-学习/04-方法论",
    "40-学习/05-开源仓库",
    "50-知识输出/01-文章",
    "98-归档/01-工作归档",
    "98-归档/02-项目归档",
    "98-归档/03-记录归档",
    "99-资源库/00-模板",
    "99-资源库/01-书籍",
    "99-资源库/02-文章",
    "99-资源库/03-课程",
    "99-资源库/04-视频",
    "99-资源库/05-规范",
    "99-资源库/06-OpenClaw配置备份",
]


@dataclass
class FileTemplate:
    path: str
    content: str


def now_text(timezone_name: str) -> str:
    if ZoneInfo is None:
        return datetime.now().strftime("%Y-%m-%d")
    return datetime.now(ZoneInfo(timezone_name)).strftime("%Y-%m-%d")


def build_templates(owner_name: str, today: str) -> list[FileTemplate]:
    return [
        FileTemplate(
            "README.md",
            dedent(
                f"""\
                ---
                title: {owner_name}的 GTD 个人知识库
                date: {today}
                tags:
                  - 知识库
                  - GTD
                ---

                # {owner_name}的 GTD 个人知识库

                > 知识流向：收集 → 澄清 → 组织 → 复盘 → 输出

                ## 顶层目录

                - `00-收集箱`：一切未澄清输入
                - `10-工作`：工作职责相关事项
                - `20-项目`：需要持续推进的独立项目
                - `30-记录`：日志、灵感、会议、周报
                - `40-学习`：消化后的学习笔记
                - `50-知识输出`：文章、分享、成品
                - `98-归档`：已完结或暂停内容
                - `99-资源库`：原始资料、模板、规范

                ## 默认工作流

                1. 把碎片和外部输入先放进 `00-收集箱` 或 `99-资源库`
                2. 每天至少一次做澄清和分类
                3. 把要执行的事情推进到 `10-工作` / `20-项目`
                4. 把真正消化过的内容沉淀到 `40-学习`
                5. 定期从 `40-学习` 和 `20-项目` 提炼到 `50-知识输出`

                ## 快速入口

                - [待阅读队列](99-资源库/待阅读队列.md)
                - [标签体系](99-资源库/05-规范/标签体系.md)
                - [文件命名规范](99-资源库/05-规范/文件命名规范.md)
                - [GTD 工作流规范](99-资源库/05-规范/GTD工作流规范.md)
                """
            ),
        ),
        FileTemplate(
            "00-收集箱/README.md",
            dedent(
                """\
                # 收集箱说明

                所有没有被判断清楚的输入，都先落在这里。

                典型内容：

                - 临时想法
                - 链接与截图说明
                - 待分类材料
                - 还没判断是否可执行的事项

                每天至少清空一次，不让收集箱长期堆积。
                """
            ),
        ),
        FileTemplate(
            "99-资源库/待阅读队列.md",
            dedent(
                """\
                ---
                title: 待阅读队列
                date: YYYY-MM-DD
                tags:
                  - 队列
                  - 资源库
                ---

                # 待阅读队列

                这里记录已经入库，但还没有形成观点和笔记的材料。

                | 标题 | 来源 | 添加日期 | 状态 | 下一步 |
                | --- | --- | --- | --- | --- |
                | 示例：某篇文章 | 微信文章 | YYYY-MM-DD | 待阅读 | 写到 40-学习 |
                """
            ),
        ),
        FileTemplate(
            "99-资源库/05-规范/标签体系.md",
            dedent(
                """\
                ---
                title: 标签体系
                date: YYYY-MM-DD
                tags:
                  - 规范
                  - 标签
                ---

                # 标签体系

                标签只回答“它是什么”，不要回答“它放哪儿”。

                ## 内容类型标签

                - 日志
                - 会议
                - 灵感
                - 项目
                - 读书笔记
                - 课程笔记
                - 文章笔记
                - 知识输出

                ## 领域标签

                - 人工智能
                - 编程
                - 方法论
                - 写作
                - 游戏
                - 职场
                - 历史
                - 心理学

                ## 来源标签

                - 微信文章
                - 知乎
                - B站
                - 开源项目
                - 原创

                ## 状态标签

                只在必要时使用：

                - 待处理
                - 进行中
                - 等待中
                - 已归档

                ## 使用原则

                - 每篇笔记控制在 2-4 个标签
                - 优先用中文标签
                - 避免同义词并存
                """
            ),
        ),
        FileTemplate(
            "99-资源库/05-规范/文件命名规范.md",
            dedent(
                """\
                ---
                title: 文件命名规范
                date: YYYY-MM-DD
                tags:
                  - 规范
                ---

                # 文件命名规范

                ## 推荐规则

                - 日志：`YYYY-MM-DD：周X记录.md`
                - 会议：`YYYY-MM-DD：会议主题.md`
                - 文章笔记：`YYYY-MM-DD-标题.md`
                - 原始文章：`来源-标题.md`
                - 模板：`XX模板.md`
                - 规范：`XX规范.md` 或 `XX体系.md`

                ## 注意事项

                - 避免双引号、尖括号、问号、星号等跨平台不友好的字符
                - 标题不用追求绝对短，先保证可读和可搜索
                """
            ),
        ),
        FileTemplate(
            "99-资源库/05-规范/GTD工作流规范.md",
            dedent(
                """\
                ---
                title: GTD 工作流规范
                date: YYYY-MM-DD
                tags:
                  - 规范
                  - GTD
                ---

                # GTD 工作流规范

                ## Capture

                - 碎片输入先到 `00-收集箱`
                - 外部资料先到 `99-资源库`

                ## Clarify

                每次处理输入都判断：

                1. 这是资料、行动、项目还是记录？
                2. 是否需要形成观点？
                3. 是否需要归档或等待？

                ## Organize

                - 工作事项 → `10-工作`
                - 独立项目 → `20-项目`
                - 日志/会议/灵感 → `30-记录`
                - 消化后的学习笔记 → `40-学习`
                - 输出成品 → `50-知识输出`

                ## Reflect

                - 每日：清空收集箱、看 TODO、写日志
                - 每周：项目回顾、等待项回顾、归档
                - 每月：标签收敛、结构瘦身、输出复盘

                ## Engage

                优先把已经形成明确观点的内容，推进到 `50-知识输出`。
                """
            ),
        ),
        FileTemplate(
            "99-资源库/00-模板/文章笔记模板.md",
            dedent(
                """\
                ---
                title: 文章笔记模板
                date: YYYY-MM-DD
                tags:
                  - 规范
                  - 模板
                ---

                # 文章笔记模板

                ## 基本信息

                - 原文标题：
                - 来源：
                - 阅读日期：
                - 标签：

                ## 核心观点

                - 

                ## 我的理解

                - 

                ## 可执行动作

                - [ ]

                ## 原文引用

                - [原文链接](../02-文章/来源-标题.md)
                """
            ),
        ),
        FileTemplate(
            "99-资源库/00-模板/日记模板.md",
            dedent(
                """\
                ---
                title: YYYY-MM-DD：周X记录
                date: YYYY-MM-DD
                tags:
                  - 日志
                ---

                # YYYY-MM-DD：周X记录

                ## 今日概览

                -

                ## 重要事件

                -

                ## 推进中的工作/项目

                -

                ## 学到的东西

                -

                ## 明日关注

                - [ ]
                """
            ),
        ),
        FileTemplate(
            "99-资源库/00-模板/周回顾模板.md",
            dedent(
                """\
                ---
                title: 周回顾模板
                date: YYYY-MM-DD
                tags:
                  - 模板
                  - 复盘
                ---

                # 周回顾模板

                ## 本周完成

                -

                ## 卡点与风险

                -

                ## 待推进项目

                -

                ## 待归档内容

                -

                ## 下周重点

                - [ ]
                """
            ),
        ),
        FileTemplate(
            "98-归档/README.md",
            dedent(
                """\
                # 归档说明

                已结束、暂停、长期不活跃的内容，不要删除，优先归档。

                归档不代表没价值，而是从“活跃面板”中移走。
                """
            ),
        ),
    ]


def write_file(path: Path, content: str, force: bool, results: list[str]) -> None:
    if path.exists() and not force:
        results.append(f"跳过文件 {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    results.append(f"写入文件 {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--knowledge-root", required=True, help="知识库根目录")
    parser.add_argument("--owner-name", default="用户", help="知识库所有者名称")
    parser.add_argument("--timezone", default="Asia/Shanghai", help="日期使用的时区")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的模板文件")
    args = parser.parse_args()

    root = Path(args.knowledge_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    results: list[str] = []

    for rel in DIRS:
        target = root / rel
        target.mkdir(parents=True, exist_ok=True)
        results.append(f"创建目录 {target}")

    today = now_text(args.timezone)
    for template in build_templates(args.owner_name, today):
        content = template.content.replace("YYYY-MM-DD", today)
        write_file(root / template.path, content, args.force, results)

    print("初始化完成：")
    for line in results:
        print(f"- {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
