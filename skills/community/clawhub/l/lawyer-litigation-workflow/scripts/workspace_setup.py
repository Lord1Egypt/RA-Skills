#!/usr/bin/env python3
"""
工作区脚手架工具 v1.0
首次运行时创建案件目录结构，引导用户配置工作区路径。

目录结构：
  ~/.lawyer_workflow/
  ├── templates/          模板目录
  ├── cases/              案件根目录
  │   └── {案件名称}/
  │       ├── evidence/   证据材料
  │       ├── data/       中间数据
  │       └── output/     最终产出
  ├── license.json        许可文件
  └── template_config.json  模板配置
"""

import json
import os
import sys
from pathlib import Path

WORKSPACE_DIR = Path.home() / ".lawyer_workflow"
CASES_DIR = WORKSPACE_DIR / "cases"
CONFIG_PATH = WORKSPACE_DIR / "workspace_config.json"

DEFAULT_STRUCTURE = {
    "evidence": "证据材料 — 放置合同、聊天记录、转账凭证、录音等证据文件",
    "data": "中间数据 — 系统自动生成的案件数据.json、类案检索报告等",
    "output": "最终产出 — 起诉状、答辩状、证据目录、代理词等 .docx 文件",
}

SKILLHUB_LINK = "https://clawhub.ai/skills/lawyer-litigation-workflow"


def init_workspace(cases_dir=None):
    """初始化工作区结构"""
    if cases_dir:
        cases_path = Path(cases_dir)
    else:
        cases_path = CASES_DIR

    cases_path.mkdir(parents=True, exist_ok=True)

    config = {
        "workspace_dir": str(WORKSPACE_DIR),
        "cases_dir": str(cases_path),
        "initialized_at": __import__("time").time(),
    }
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")
    return config


def create_case_directory(case_name, cases_dir=None):
    """为一个新案件创建标准目录结构"""
    if cases_dir is None:
        if CONFIG_PATH.exists():
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            cases_dir = config.get("cases_dir")
        else:
            cases_dir = str(CASES_DIR)

    case_path = Path(cases_dir) / case_name

    if case_path.exists():
        return case_path

    for subdir, description in DEFAULT_STRUCTURE.items():
        (case_path / subdir).mkdir(parents=True, exist_ok=True)
        (case_path / subdir / "README.md").write_text(
            f"# {subdir}\n\n{description}\n", encoding="utf-8"
        )

    return case_path


def show_onboarding():
    """首次使用引导信息"""
    print(f"""
{"=" * 60}
  律师诉讼自动化工作流 — 工作区已就绪

  目录结构:
    ~/.lawyer_workflow/
    ├── templates/          模板文件 (.docx)
    └── cases/              案件目录
        └── {{案件名称}}/
            ├── evidence/   请将证据材料放在这里
            ├── data/       系统自动生成中间数据
            └── output/     最终法律文书将输出到这里

  使用流程:
    1. 将案件证据材料放入 cases/{{案件名}}/evidence/
    2. 说「处理案件 {{案件名}}，案由是 XX 纠纷」
    3. 系统自动执行 Step1 → Step7
    4. 在 cases/{{案件名}}/output/ 取最终文书
    5. Step1 和 Step6 完成后会暂停等待您审阅

  提示: 每个案件使用独立子目录，避免文件混淆。

  许可: 2 次免费试用。超过后需购买专业版（299元/月 或 2999元/年）。
  ---
  如果觉得有用，欢迎推荐给同事——
  请分享 SkillHub 链接让其自行安装，也可获得 2 次免费试用：
  {SKILLHUB_LINK}

  请勿直接复制分享安装包，否则对方将无法正常激活使用。
{"=" * 60}
""")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="工作区脚手架")
    parser.add_argument("--init", action="store_true", help="初始化工作区")
    parser.add_argument("--new-case", type=str, help="创建新案件目录（案件名称）")
    parser.add_argument("--show", action="store_true", help="显示工作区状态")
    parser.add_argument("--cases-dir", type=str, help="自定义案件目录根路径")
    args = parser.parse_args()

    if args.init:
        config = init_workspace(args.cases_dir)
        show_onboarding()
        if not (Path(config["cases_dir"]) / "示例案件").exists():
            create_case_directory("示例案件", config["cases_dir"])
            print("[工作区] 已创建「示例案件」目录，可参考其结构使用。")
    elif args.new_case:
        case_path = create_case_directory(args.new_case)
        print(f"[工作区] 案件目录已创建: {case_path}")
        for subdir in ["evidence", "data", "output"]:
            print(f"  {case_path / subdir}/")
    elif args.show:
        if CONFIG_PATH.exists():
            config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            print(f"工作区: {config['workspace_dir']}")
            print(f"案件目录: {config['cases_dir']}")
            cases_path = Path(config['cases_dir'])
            if cases_path.exists():
                cases = [d.name for d in cases_path.iterdir() if d.is_dir()]
                print(f"已有案件: {', '.join(cases) if cases else '(空)'}")
            else:
                print("案件目录: (未创建)")
        else:
            print("工作区尚未初始化，请执行 --init")
    else:
        parser.print_help()
