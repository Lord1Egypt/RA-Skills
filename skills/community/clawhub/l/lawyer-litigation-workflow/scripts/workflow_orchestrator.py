#!/usr/bin/env python3
"""
律师诉讼自动化工作流 — 总控编排器 v1.0
SkillHub 适配版。

执行流程:
  Step0: 前置检查（许可 + 工作区 + 模板）
  Step1: 案件访谈（谈话笔录）
  Step2: 法律文书生成
  Step3: 类案检索
  Step4: 法条检索
  Step5: 诉讼策略
  Step6: 审查定稿
  Step7: 出庭文书
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

WORKSPACE_DIR = Path.home() / ".lawyer_workflow"
CONFIG_PATH = WORKSPACE_DIR / "workspace_config.json"


def get_cases_dir():
    """获取案件目录根路径"""
    if CONFIG_PATH.exists():
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return Path(config.get("cases_dir", WORKSPACE_DIR / "cases"))
    return WORKSPACE_DIR / "cases"


def get_template_dir():
    """获取模板目录路径"""
    template_config = WORKSPACE_DIR / "template_config.json"
    if template_config.exists():
        config = json.loads(template_config.read_text(encoding="utf-8"))
        return Path(config.get("template_dir", WORKSPACE_DIR / "templates"))
    return WORKSPACE_DIR / "templates"


def step0_precheck():
    """Step0: 前置检查"""
    import subprocess
    results = {"passed": True, "steps": {}}

    # 0-1 许可检查
    result = subprocess.run(
        [sys.executable, "scripts/license_manager.py", "--check"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stdout)
        return {"passed": False, "reason": "许可检查未通过"}
    results["steps"]["license"] = {"passed": True, "output": result.stdout.strip()}

    # 0-2 工作区初始化
    if not CONFIG_PATH.exists():
        result = subprocess.run(
            [sys.executable, "scripts/workspace_setup.py", "--init"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return {"passed": False, "reason": f"工作区初始化失败: {result.stderr}"}
    results["steps"]["workspace"] = {"passed": True}

    # 0-3 模板检测
    template_config = WORKSPACE_DIR / "template_config.json"
    if not template_config.exists():
        result = subprocess.run(
            [sys.executable, "scripts/template_setup.py", "--detect"],
            capture_output=True, text=True
        )
        print(result.stdout)
        # 模板检测不阻断流程，仅提示

    results["steps"]["templates"] = {"passed": True}
    return results


def step1_interview(case_name, case_data):
    """Step1: 案件访谈 — 生成谈话笔录"""
    cases_dir = get_cases_dir()
    template_dir = get_template_dir()
    output_dir = cases_dir / case_name / "output"
    data_dir = cases_dir / case_name / "data"

    output_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    # 保存案件数据
    case_data_path = data_dir / "案件数据.json"
    case_data_path.write_text(json.dumps(case_data, ensure_ascii=False, indent=2), encoding="utf-8")

    # 生成谈话笔录
    from specification_pipeline import run_spec_pipeline, generate_from_spec_only

    template_path = template_dir / "4-律师接待当事人谈话笔录.1份docx.docx"
    output_path = output_dir / "谈话笔录.docx"

    try:
        if template_path.exists():
            run_spec_pipeline(
                str(template_path), "谈话笔录", case_data, str(output_path),
                case_data_path=str(case_data_path)
            )
        else:
            generate_from_spec_only("谈话笔录", case_data, str(output_path))
    except Exception as e:
        print(f"[Step1] 谈话笔录生成警告: {e}")
        print("[Step1] 将使用规格文件降级生成")

    print(f"[Step1] 谈话笔录已生成: {output_path}")
    print(f"[Step1] 案件数据已保存: {case_data_path}")
    print(f"[Step1] ⏸ 请审阅谈话笔录和案件数据，确认后回复「继续」进入Step2。")

    return {"passed": True, "case_data_path": str(case_data_path), "output_dir": str(output_dir)}


def step2_documents(case_name, case_data, output_dir, case_data_path):
    """Step2: 法律文书生成"""
    template_dir = get_template_dir()
    output_path = Path(output_dir)

    docs_to_generate = [
        {"spec": "起诉状", "template": "起诉状3份（）.docx", "output": "民事起诉状.docx"},
        {"spec": "授权委托书", "template": "授权委托书3份.docx", "output": "授权委托书.docx"},
        {"spec": "律所出庭函", "template": "3.出庭函（民事诉讼类）(东润).docx", "output": "律师事务所函.docx"},
        {"spec": "委托代理协议", "template": "东润民商事诉讼协议.docx", "output": "委托代理协议.docx"},
    ]

    # 法人需要法定代表人身份证明
    parties = case_data.get("诉讼地位表", {})
    has_legal_entity = any(
        v.get("角色") == "被告" and ("公司" in k or "有限" in k or "企业" in k)
        for k, v in parties.items()
    )
    if has_legal_entity:
        docs_to_generate.append(
            {"spec": "法定代表人身份证明", "template": "3-法定代表人身份证明-3份.docx", "output": "法定代表人身份证明.docx"}
        )

    from specification_pipeline import run_spec_pipeline, generate_from_spec_only

    generated = []
    for doc_config in docs_to_generate:
        template_path = template_dir / doc_config["template"]
        output_doc = output_path / doc_config["output"]

        try:
            if template_path.exists():
                run_spec_pipeline(
                    str(template_path), doc_config["spec"], case_data, str(output_doc),
                    case_data_path=case_data_path
                )
            else:
                generate_from_spec_only(doc_config["spec"], case_data, str(output_doc))
            generated.append(doc_config["output"])
        except Exception as e:
            print(f"[Step2] {doc_config['output']} 生成失败: {e}")

    print(f"[Step2] 已生成 {len(generated)} 份文书: {', '.join(generated)}")
    print(f"[Step2] 输出目录: {output_dir}")
    return {"passed": True, "generated": generated}


def run_workflow(case_name, case_data, steps=None):
    """
    主入口：运行工作流

    Args:
        case_name: 案件名称
        case_data: 案件数据 dict（包含当事人信息、事实等）
        steps: 要运行的步骤列表，None=全部
    """
    if steps is None:
        steps = ["step0", "step1", "step2", "step3", "step4", "step5", "step6", "step7"]

    print(f"\n{'='*60}")
    print(f"律师诉讼自动化工作流 v1.0")
    print(f"案件: {case_name}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    state = {"case_name": case_name, "case_data": case_data, "results": {}}

    if "step0" in steps:
        print("[Step0] 前置检查...")
        state["results"]["step0"] = step0_precheck()
        if not state["results"]["step0"]["passed"]:
            return state

    if "step1" in steps:
        print("[Step1] 案件访谈...")
        result = step1_interview(case_name, case_data)
        state["results"]["step1"] = result
        state["case_data_path"] = result.get("case_data_path", "")
        state["output_dir"] = result.get("output_dir", "")

    if "step2" in steps:
        print("[Step2] 法律文书生成...")
        state["results"]["step2"] = step2_documents(
            case_name, case_data,
            state.get("output_dir", str(get_cases_dir() / case_name / "output")),
            state.get("case_data_path", "")
        )

    # Step3-7 由 AI 根据 SKILL.md 指令驱动执行
    print(f"\n[Step3-7] 后续步骤由 AI 驱动执行。")

    return state


if __name__ == "__main__":
    print("律师诉讼自动化工作流 v1.0")
    print("请通过 WorkBuddy Skill 调用，格式: 处理案件 {案件名}，案由是 {案由}")
    print()
    print("详细指令请参阅 SKILL.md。")
