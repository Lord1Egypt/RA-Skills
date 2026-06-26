#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def validate_mapping_block(name: str, block: dict, allow_empty_preferred: bool = False) -> list[str]:
    errs = []
    preferred = block.get("preferred_tool_name", "")
    keywords = block.get("fallback_discovery_keywords", [])
    required_args = block.get("required_args_schema", [])
    if not allow_empty_preferred and not isinstance(preferred, str):
        errs.append(f"{name}.preferred_tool_name 类型错误")
    if allow_empty_preferred and not isinstance(preferred, str):
        errs.append(f"{name}.preferred_tool_name 类型错误")
    if not isinstance(keywords, list) or not keywords:
        errs.append(f"{name}.fallback_discovery_keywords 必须是非空数组")
    if not isinstance(required_args, list) or not required_args:
        errs.append(f"{name}.required_args_schema 必须是非空数组")
    return errs


def main() -> int:
    skill_root = Path(__file__).resolve().parent.parent
    config_path = skill_root / "config.template.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    errs = []
    errs.extend(validate_mapping_block("image_generation", config.get("image_generation", {})))
    errs.extend(validate_mapping_block("video_generation", config.get("video_generation", {})))
    errs.extend(
        validate_mapping_block(
            "model3d_generation",
            config.get("model3d_generation", {}),
            allow_empty_preferred=True,
        )
    )
    errs.extend(validate_mapping_block("logo_design", config.get("logo_design", {})))
    errs.extend(validate_mapping_block("product_image_generation", config.get("product_image_generation", {})))
    errs.extend(validate_mapping_block("cutout_generation", config.get("cutout_generation", {})))
    product_image_generation = config.get("product_image_generation", {})
    if product_image_generation.get("preferred_tool_name") != "image_praline_edit_v2":
        errs.append("product_image_generation.preferred_tool_name 必须为 image_praline_edit_v2")
    if product_image_generation.get("fallback_tool_name") != "image_praline_edit_v2":
        errs.append("product_image_generation.fallback_tool_name 必须为 image_praline_edit_v2")

    stages = config.get("stages", {}).get("supported", [])
    expected = {
        "search",
        "generate-image",
        "generate-video",
        "generate-3d",
        "generate-logo",
        "generate-product-image",
        "cutout",
        "upload",
        "report",
    }
    if set(stages) != expected:
        errs.append("stages.supported 与预期阶段不一致")

    if errs:
        print("check_tools_mapping: FAIL")
        for e in errs:
            print(f"- {e}")
        return 1

    print("check_tools_mapping: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
