#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初始化长篇小说项目结构。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
REFERENCES_DIR = ROOT_DIR / "references"


def load_template(filename: str, fallback: str) -> str:
    path = REFERENCES_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8")
    return fallback


def build_task_log(project_name: str) -> str:
    return f"""# 创作进度日志

## 当前状态
- 创作阶段：规划中
- 书名：{project_name}
- 目标总字数：3000000
- 目标卷数：待定
- 最新章节：无
- 当前处理章节：无
- 当前卷：未开始
- 当前阶段：未开始
- 当前阶段目标：未记录
- 当前视角：
- 主角位置：
- 主角状态：
- 下一章目标：
- 最近阶段审计：未记录
- 最近阶段审计章节：0
- 最近卷审计：未记录
- 最近卷审计章节：0
- 设定变更待同步：无
- 累计完成章节：0
- 累计完成字数：0

## 最近三章摘要
- 暂无

## 活跃伏笔
| 伏笔名称 | 埋设章节 | 当前状态 | 关联章节 |
|----------|----------|----------|----------|

## 待处理
- [ ] 待回收伏笔
- [ ] 待出场角色
- [ ] 未解决矛盾

## 阶段审计记录
- 暂无

## 卷审计记录
- 暂无
"""


def build_worldview_template() -> str:
    return """# 世界观

## 前台逻辑层级
- 当前主要由哪一层逻辑驱动：
- 其他层级如何作为背景支撑：

## 题材基石
- 当前题材更偏：现实 / 历史 / 虚构
- 这一题材最需要优先研究或搭牢的规则：

## 空间尺度
- 当前故事主要发生在哪个尺度：
- 暂时不展开的更大空间：
- 当前更适合：扩展 / 升级 / 维持现状
- 当前世界更偏：开放 / 封闭 / 局部封闭远处开放

## 自然层

### 自然形态
- 地理环境：
- 关键资源：
- 生命形态：

### 自然规则
- 底层铁律：
- 可突破的表层规则：
- 打破表层规则的代价：

## 文明层

### 文明形态
- 势力结构：
- 社会结构：
- 制度与工具：

### 文明规则
- 权力逻辑：
- 分配逻辑：
- 价值观排序：
- 禁忌：

## 历史沉淀
- 旧战争 / 旧站队 / 旧恩怨：
- 这些历史如何塑造今天：

## 动态循环
- 自然如何限制文明：
- 文明如何改造自然：
- 当前系统最脆弱的地方：

## 从世界生长出的故事
- 最稀缺的资源/名额：
- 谁在控制它：
- 谁被排除在外：
- 主角当前站位：
- 主角一旦打破规则，世界会如何反应：
- 升级或成长的代价与天花板：

## 验证顺序
- 底层逻辑：
- 天然矛盾：
- 核心人物：
- 冲突升级路径：

## 扩展与升级规划
- 下一步是横向扩展还是纵向升级：
- 新空间将带来什么新规则或新矛盾：
- 如何自然过渡到新空间：
"""


def build_author_intent_template() -> str:
    return """# 作者意图

用于记录这本书长期想成为什么，而不是只记录下一章要写什么。

## 长期目标
- 这本书最终想让读者持续追什么：
- 这本书最核心的情绪承诺：
- 这本书最不能偏掉的卖点：

## 长线取舍
- 哪类剧情可以少写：
- 哪类剧情绝对不能多写：
- 哪些人物或关系不允许沦为工具人：

## 平台与商业约束
- 目标平台：
- 目标读者：
- 不碰的高风险内容：
"""


def build_current_focus_template() -> str:
    return """# 当前焦点

用于拉回未来 1-3 章的注意力。这里比作者意图短，只解决最近该优先写什么。

## 最近阶段最该拉住的主问题
- 

## 最近 1-3 章优先事项
- 

## 最近 1-3 章禁止偏航项
- 

## 最近必须回扣或推进的伏笔/关系/风险
- 
"""


def build_conflict_template() -> str:
    return """# 冲突设计

## 核心冲突
- [主角想要什么？什么阻止了他？]

## 冲突土壤

### 资源稀缺
- 稀缺的是什么：
- 谁在争：
- 为什么不够分：

### 规则压力
- 自然法则：
- 文明规则：
- 谁受益：
- 谁受损：

### 历史积怨
- 过去发生过什么：
- 现在谁还在承担后果：

## 三层冲突
| 层级 | 当前冲突 | 主要角色/势力 | 代价 |
|------|----------|----------------|------|
| 宏观 |  |  |  |
| 中观 |  |  |  |
| 微观 |  |  |  |
"""


def build_rules_template() -> str:
    return """# 法则

## 境界 / 等级体系

## 能力限制

## 冲突红线

## 不可违背规则
"""


def build_foreshadow_template() -> str:
    return """# 伏笔记录

## 活跃伏笔
| 伏笔名称 | 埋设章节 | 伏笔类型 | 关联章节 |
|----------|----------|----------|----------|

## 已回收伏笔
| 伏笔名称 | 埋设章节 | 回收章节 | 备注 |
|----------|----------|----------|------|
"""


def build_timeline_template() -> str:
    return """# 剧情时间线

## 第一卷

| 时间点/章节 | 事件节点 | 配角出场/情感转折 | 主角变化 | 备注 |
|-------------|----------|------------------|----------|------|
"""


def build_relationship_map_template() -> str:
    return """# 关系图

## 当前关系图谱
| 角色A | 角色B | 当前关系 | 隐性张力 | 变化方向 |
|------|------|----------|----------|----------|

## 高风险关系检查
- 是否存在合作与敌对并存的关系：
- 是否存在误解、依赖、利用或情感债：
- 这些关系会在第几卷/第几阶段发生变化：
"""


def build_ensemble_theme_template() -> str:
    return """# 群像主题拆分

## 主主题
- 这部作品最终想回答什么问题：

## 角色/阵营主题线
| 角色/阵营 | 主题命题 | 当前阶段 | 与主线关系 |
|-----------|----------|----------|------------|

## 轮转原则
- 哪条线负责主推进：
- 哪条线负责映照或对冲：
- 哪些角色不能长期只围着主角转：
"""


def build_pov_rotation_template() -> str:
    return """# POV轮转表

| 章节 | 主POV | 次POV（可选） | 主线任务 | 备注 |
|------|-------|---------------|----------|------|
| 第1章 | | | | |
| 第2章 | | | | |
"""


def build_series_constitution_template() -> str:
    return """# 全书宪法

用于 100 万字以上长篇连载的最高优先级约束。这里的内容默认高于卷纲、章纲和临场灵感。

## 项目定位
- 题材赛道：
- 目标平台：
- 目标读者：
- 核心卖点：
- 禁区与高风险项：

## 全书终局
- 最终抵达的结果：
- 主角最终赢什么 / 失去什么：
- 终局必须兑现的主命题：
- 绝对不能丢的结局锚点：

## 主角长期弧线
- 开局核心缺口：
- 中段必须经历的关键误判 / 崩塌：
- 后段必须完成的认知跃迁：
- 终局人物状态：

## 长线关系宪法
- 主关系线：
- 关系线不能越过的边界：
- 必须发生的关系阶段变化：
- 禁止为了短期爽点牺牲的长期关系逻辑：

## 世界与法则宪法
- 绝对不可违背的底层规则：
- 可以升级但不能推翻的表层规则：
- 战力 / 权力 / 资源增长的硬上限：
- 每次越级或破格推进必须支付的代价：

## 长线悬念
- 主线悬念：
- 中段大谜团：
- 终极揭秘：
- 哪些答案必须延后，不能提前泄露：

## 卷级运营硬约束
- 每卷至少要兑现的东西：
- 每卷结尾必须留下的前台问题：
- 不能连续超过多少章没有明确阶段回报：
- 不能连续超过多少章只铺设定不推进主线：

## 变更边界
- 可以灵活调整的内容：
- 需要写入变更日志才能改的内容：
- 明令禁止擅自改动的内容：
"""


def build_volume_blueprint_template() -> str:
    return """# 卷纲

用于管理 300 万字级连载的卷级推进。每卷都要有进入条件、兑现目标、卷末结算和遗留问题。

## 总览
| 卷次 | 目标章节区间 | 目标字数 | 地图/场域 | 主问题 | 卷末兑现 | 卷末遗留 |
|------|--------------|----------|-----------|--------|----------|----------|
| 第一卷 | 第1-60章 | 180000-300000 |  |  |  |  |
| 第二卷 | 第61-120章 | 180000-300000 |  |  |  |  |

## 卷模板

### 第一卷
- 进入条件：
- 卷核心任务：
- 主角本卷最需要拿到的资源 / 资格 / 认知：
- 本卷主反派 / 主阻碍：
- 本卷阶段高潮：
- 本卷必须兑现的爽点 / 情绪点：
- 本卷必须留下的下一卷入口：
- 与全书终局的关系：

### 第二卷
- 进入条件：
- 卷核心任务：
- 主角本卷最需要拿到的资源 / 资格 / 认知：
- 本卷主反派 / 主阻碍：
- 本卷阶段高潮：
- 本卷必须兑现的爽点 / 情绪点：
- 本卷必须留下的下一卷入口：
- 与全书终局的关系：
"""


def build_phase_plan_template() -> str:
    return """# 阶段规划

阶段是章与卷之间的治理层。默认每 10-20 章为一个阶段，每个阶段都要有硬目标、升级点和审计节点。

## 阶段总表
| 阶段 | 章节范围 | 所属卷 | 当前前台问题 | 阶段目标 | 阶段回报 | 结尾钩子 |
|------|----------|--------|--------------|----------|----------|----------|
| 阶段1 | 第1-12章 | 第一卷 |  |  |  |  |
| 阶段2 | 第13-24章 | 第一卷 |  |  |  |  |

## 阶段模板

### 阶段1
- 起点状态：
- 本阶段必须解决的问题：
- 本阶段不能提前解决的问题：
- 本阶段主角必须做出的关键选择：
- 本阶段主要关系变化：
- 本阶段新增或升级的风险：
- 本阶段最迟第几章要给回报：
- 阶段结算时要带走什么：

### 阶段2
- 起点状态：
- 本阶段必须解决的问题：
- 本阶段不能提前解决的问题：
- 本阶段主角必须做出的关键选择：
- 本阶段主要关系变化：
- 本阶段新增或升级的风险：
- 本阶段最迟第几章要给回报：
- 阶段结算时要带走什么：
"""


def build_change_log_template() -> str:
    return """# 变更日志

用于记录会影响长篇一致性的结构性调整。凡是会影响全书宪法、卷纲、阶段规划、主角长期弧线、世界底层规则的改动，都必须先登记再执行。

## 记录格式
| 日期 | 变更级别 | 变更项 | 原方案 | 新方案 | 影响范围 | 是否已同步 |
|------|----------|--------|--------|--------|----------|------------|
| YYYY-MM-DD | 全书/卷/阶段/人物/法则 |  |  |  |  | 否 |

## 变更审批问题
- 这个改动会不会破坏全书终局锚点：
- 这个改动会不会让前文伏笔失效：
- 这个改动会不会导致人物弧线断裂：
- 需要同步更新哪些文件：
- 如果不改，会出什么问题：
"""


LONGFORM_STATE_FIELDS = (
    ("目标总字数：", "3000000"),
    ("目标卷数：", "待定"),
    ("当前卷：", "未开始"),
    ("当前阶段：", "未开始"),
    ("当前阶段目标：", "未记录"),
    ("最近阶段审计：", "未记录"),
    ("最近阶段审计章节：", "0"),
    ("最近卷审计：", "未记录"),
    ("最近卷审计章节：", "0"),
    ("设定变更待同步：", "无"),
)


def ensure_state_field(text: str, label: str, value: str) -> str:
    pattern = rf"(?m)^- {re.escape(label)}.*$"
    replacement = f"- {label}{value}"
    if re.search(pattern, text):
        return text
    current_state = "## 当前状态\n"
    if current_state in text:
        return text.replace(current_state, current_state + replacement + "\n", 1)
    return text.rstrip() + "\n\n## 当前状态\n" + replacement + "\n"


def ensure_section(text: str, header: str, default_lines: list[str]) -> str:
    pattern = rf"(?ms)^## {re.escape(header)}\n(.*?)(?=^## |\Z)"
    if re.search(pattern, text):
        return text
    body = "\n".join(default_lines).rstrip() + "\n"
    return text.rstrip() + f"\n\n## {header}\n" + body


def ensure_longform_task_log(task_log_path: Path) -> None:
    if not task_log_path.exists():
        task_log_path.write_text(build_task_log(task_log_path.parent.name), encoding="utf-8")
        return

    text = task_log_path.read_text(encoding="utf-8")
    for label, value in LONGFORM_STATE_FIELDS:
        text = ensure_state_field(text, label, value)
    text = ensure_section(text, "阶段审计记录", ["- 暂无"])
    text = ensure_section(text, "卷审计记录", ["- 暂无"])
    task_log_path.write_text(text, encoding="utf-8")


def ensure_longform_governance_files(project_dir: Path, force: bool = False) -> None:
    longform_files = {
        project_dir / "docs" / "全书宪法.md": build_series_constitution_template(),
        project_dir / "docs" / "卷纲.md": build_volume_blueprint_template(),
        project_dir / "docs" / "阶段规划.md": build_phase_plan_template(),
        project_dir / "docs" / "变更日志.md": build_change_log_template(),
    }
    for path, content in longform_files.items():
        write_file(path, content, force=force)
    ensure_longform_task_log(project_dir / "task_log.md")


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_novel_project(
    project_name: str,
    target_dir: str | None = None,
    force: bool = False,
    mode: str = "single",
    complex_relationships: bool = False,
    romance_focus: bool = False,
) -> Path:
    base_dir = Path(target_dir).expanduser().resolve() if target_dir else Path.cwd()
    project_dir = base_dir / project_name

    for folder in ("docs", "characters", "manuscript", "plot", "runtime"):
        (project_dir / folder).mkdir(parents=True, exist_ok=True)

    project_outline = load_template("outline-template.md", "# 项目总纲\n")
    project_outline = project_outline.replace("[小说名称]", project_name)
    chapter_plan = load_template("chapter-plan-template.md", "# 章节规划\n")
    character = load_template("character-template.md", "# 人物档案\n")

    files = {
        project_dir / "docs" / "项目总纲.md": project_outline,
        project_dir / "docs" / "章节规划.md": chapter_plan,
        project_dir / "docs" / "作者意图.md": build_author_intent_template(),
        project_dir / "docs" / "当前焦点.md": build_current_focus_template(),
        project_dir / "docs" / "冲突设计.md": build_conflict_template(),
        project_dir / "docs" / "世界观.md": build_worldview_template(),
        project_dir / "docs" / "法则.md": build_rules_template(),
        project_dir / "characters" / "人物档案.md": character,
        project_dir / "plot" / "伏笔记录.md": build_foreshadow_template(),
        project_dir / "plot" / "时间线.md": build_timeline_template(),
        project_dir / "task_log.md": build_task_log(project_name),
    }

    if mode in {"dual", "ensemble"}:
        files[project_dir / "docs" / "群像主题拆分.md"] = build_ensemble_theme_template()
        files[project_dir / "plot" / "POV轮转表.md"] = build_pov_rotation_template()

    if complex_relationships or romance_focus:
        files[project_dir / "docs" / "关系图.md"] = build_relationship_map_template()

    for path, content in files.items():
        write_file(path, content, force=force)

    ensure_longform_governance_files(project_dir, force=force)

    print(f"项目创建成功：{project_dir}")
    return project_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="创建长篇小说项目结构")
    parser.add_argument("project_name", nargs="?", default="my-novel", help="项目目录名")
    parser.add_argument("--target-dir", help="项目创建到哪个目录下，默认当前目录")
    parser.add_argument(
        "--mode",
        choices=("single", "dual", "ensemble"),
        default="single",
        help="项目模式：单主角、双主角或群像",
    )
    parser.add_argument("--complex-relationships", action="store_true", help="创建关系图模板")
    parser.add_argument("--romance-focus", action="store_true", help="感情线重要时创建关系图模板")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的模板文件")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    create_novel_project(
        args.project_name,
        target_dir=args.target_dir,
        force=args.force,
        mode=args.mode,
        complex_relationships=args.complex_relationships,
        romance_focus=args.romance_focus,
    )
