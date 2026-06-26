#!/usr/bin/env python3
"""museum_assistant.py

入口脚本：
  Phase 1（画像提取）→ 展示确认 → Phase 2（路线生成）

用法：
  Step 1：python3 museum_assistant.py "帮我规划去上海博物馆的参观路线"
          → 输出画像 + confirmation_prompt，等用户确认

  Step 2：用户确认后
          python3 museum_assistant.py --phase2 --profile-json '<Phase1返回的profile的JSON>'
          → 输出完整路线
"""

import argparse
import json
import sys
from typing import Any, Dict

import extract_profile as ep
import plan_route as pr
import search_artifacts as sa


# ─────────────────────────────────────────────
# Phase 1：画像提取 + 确认
# ─────────────────────────────────────────────

def run_phase1(user_input: str) -> Dict[str, Any]:
    """
    Phase 1：仅提取用户画像并构建确认信息。

    返回值永远包含 confirmation_needed: True，
    AI 将此内容展示给用户，等用户回复后再进入 Phase 2。
    """
    llm_profile = ep.extract_profile(user_input)
    if not llm_profile:
        return {
            "phase": 1,
            "error": "画像提取失败，请检查 API 配置与网络连接",
            "confirmation_needed": False,
        }

    inferred_fields = _collect_inferred_fields(llm_profile)

    # 阶段一所有未提取的信息都标注为未指定
    llm_profile = ep.normalize_profile_for_scoring(llm_profile)

    confirmation_prompt = ep.build_confirmation_prompt(llm_profile, inferred_fields)

    return {
        "phase": 1,
        "profile": llm_profile,
        "inferred_fields": inferred_fields,
        "has_unfilled_mandatory": not llm_profile.get("museum_name"),
        "confirmation_needed": True,
        "confirmation_prompt": confirmation_prompt,
        "next_step": "phase2",
        "usage_hint": (
            "用户确认后，将 --profile-json '<JSON>' 传入 Phase 2，例如：\n"
            "  python3 museum_assistant.py --phase2 --profile-json '<此处粘贴profile>'"
        ),
    }


# ─────────────────────────────────────────────
# Phase 2：用户确认后，执行文物检索 + 路线生成
# ─────────────────────────────────────────────

def run_phase2(profile: Dict[str, Any], user_confirmation: str = "") -> Dict[str, Any]:
    """
    Phase 2：在用户明确确认 Phase 1 画像之后运行。
    接收确认后的 profile 和用户补充信息，执行二次提取和推断，然后进行文物检索与路线规划。
    """
    museum_name = profile.get("museum_name", "").strip()
    if not museum_name:
        return {
            "phase": 2,
            "error": "缺少博物馆名称，无法继续。请在 Phase 1 确认时提供博物馆名称。",
        }

    # 二次提取和推断：如果用户提供了补充信息，使用大模型进行二次提取
    if user_confirmation:
        # 调用 extract_profile 函数进行二次提取
        llm_result = ep.extract_profile(user_confirmation, current_profile=profile)
        if llm_result:
            # 更新profile
            profile.update(llm_result)

    # 对于缺失的维度，默认全选该维度的所有元素
    if not profile.get("domains"):
        profile["domains"] = ep.DOMAINS_LIST
    if not profile.get("artifact_types"):
        profile["artifact_types"] = ep.ARTIFACT_TYPES_LIST
    if not profile.get("dynasties"):
        profile["dynasties"] = ep.DYNASTIES_LIST

    # 确保所有值都来自原列表
    profile["domains"] = [d for d in profile.get("domains", []) if d in ep.DOMAINS_LIST]
    profile["artifact_types"] = [a for a in profile.get("artifact_types", []) if a in ep.ARTIFACT_TYPES_LIST]
    profile["dynasties"] = [d for d in profile.get("dynasties", []) if d in ep.DYNASTIES_LIST]

    # 如果过滤后为空，则全选
    if not profile.get("domains"):
        profile["domains"] = ep.DOMAINS_LIST
    if not profile.get("artifact_types"):
        profile["artifact_types"] = ep.ARTIFACT_TYPES_LIST
    if not profile.get("dynasties"):
        profile["dynasties"] = ep.DYNASTIES_LIST

    artifacts, source = sa.get_artifacts(museum_name)

    if not artifacts:
        return {
            "phase": 2,
            "error": f"无法检索到「{museum_name}」的文物信息，请检查网络或尝试其他博物馆。",
            "profile": profile,
        }

    result = _plan_route_inline(profile, artifacts)
    return {
        "phase": 2,
        "source": source,
        "markdown": result["markdown"],
        "selected_count": result["selected_count"],
        "selected": result["selected"],
        "profile": profile,
    }


# ─────────────────────────────────────────────
# 内部辅助函数
# ─────────────────────────────────────────────

def _collect_inferred_fields(profile: Dict[str, Any]) -> list:
    fields = []
    if not profile.get("duration"):
        fields.append("duration")
    if profile.get("first_visit") is None:
        fields.append("first_visit")
    if profile.get("with_children") is None:
        fields.append("with_children")
    if not profile.get("domains"):
        fields.append("domains")
    if not profile.get("artifact_types"):
        fields.append("artifact_types")
    if not profile.get("dynasties"):
        fields.append("dynasties")
    if not profile.get("museum_name"):
        fields.append("museum_name")
    return fields

def _plan_route_inline(profile: Dict[str, Any], artifacts: list) -> Dict[str, Any]:
    normalized_profile = pr.normalize_profile(profile)
    artifacts_selected = pr.select_and_sort(artifacts, normalized_profile)
    pr.summarize_reasons_with_llm(artifacts_selected, normalized_profile)
    table = pr.format_markdown_table(artifacts_selected)
    markdown_output = pr.build_output(profile, artifacts_selected, table)
    
    return {
        "markdown": markdown_output,
        "selected_count": len(artifacts_selected),
        "selected": artifacts_selected,
    }


# ─────────────────────────────────────────────
# main：两阶段路由
# ─────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="博物馆参观路线规划（两阶段：Phase1画像提取 → 确认 → Phase2路线生成）"
    )
    parser.add_argument("user_input", nargs="*", default=[],
                        help="用户原始需求描述（Phase 1 使用）")
    parser.add_argument("--phase2", dest="phase2", action="store_true",
                        help="运行 Phase 2（需配合 --profile-json）")
    parser.add_argument("--profile-json", dest="profile_json",
                        help="Phase 2 所需 profile JSON（Phase 1 返回的完整 JSON）")
    parser.add_argument("--profile-file", dest="profile_file",
                        help="Phase 2 所需 profile JSON 文件路径（替代 --profile-json）")
    parser.add_argument("--user-confirmation", dest="user_confirmation", default="",
                        help="用户的补充信息（Phase 2 使用）")


    args = parser.parse_args()

    # ── Phase 1 ───────────────────────────────
    if not args.phase2 and not getattr(args, "profile_json", None) and not getattr(args, "profile_file", None):
        user_input = " ".join(args.user_input).strip()
        if not user_input:
            print(json.dumps({"error": "请提供用户输入文本"}, ensure_ascii=False))
            sys.exit(1)

        result = run_phase1(user_input)
        if "error" in result and result.get("phase") != 1:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)

        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # ── Phase 2 ────────────────────────────────────────────
    if args.phase2 or getattr(args, "profile_json", None) or getattr(args, "profile_file", None):
        # 优先从文件读取profile
        if getattr(args, "profile_file", None):
            try:
                with open(args.profile_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
            except Exception as e:
                print(json.dumps({"error": f"从文件读取 profile 失败：{e}", "phase": 2}, ensure_ascii=False))
                sys.exit(1)
        elif getattr(args, "profile_json", None):
            try:
                # 处理可能的引号问题，去除首尾的单引号或双引号
                profile_json = args.profile_json
                if (profile_json.startswith('\'') and profile_json.endswith('\'')) or \
                   (profile_json.startswith('"') and profile_json.endswith('"')):
                    profile_json = profile_json[1:-1]
                # 处理转义字符问题
                profile_json = profile_json.replace('\\n', '\n').replace('\\t', '\t')
                profile = json.loads(profile_json)
            except json.JSONDecodeError as e:
                print(json.dumps({"error": f"profile JSON 解析失败：{e}", "phase": 2}, ensure_ascii=False))
                sys.exit(1)
        else:
            print(json.dumps({
                "error": "Phase 2 需要 --profile-json 或 --profile-file 参数，请先运行 Phase 1 获取 profile。",
                "phase": 2,
            }, ensure_ascii=False))
            sys.exit(1)
        
        # 获取用户补充信息
        user_confirmation = getattr(args, "user_confirmation", "")
        result = run_phase2(profile, user_confirmation)
        if "error" in result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
            sys.exit(1)
        print(result["markdown"])
        return


if __name__ == "__main__":
    main()
