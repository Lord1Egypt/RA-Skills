#!/usr/bin/env python3
"""加载和规范化项目级默认配置。"""

import json
from dataclasses import dataclass, field, fields
from pathlib import Path
from typing import Dict, List, Optional, Any
import copy

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
DEFAULTS_PATH = PROJECT_ROOT / "references" / "project-defaults.json"

@dataclass
class FormatCheckConfig:
    """格式检查配置"""
    enabled: bool
    checkFontSize: bool
    checkFontName: bool
    checkLineSpacing: bool
    checkParagraphSpacing: bool
    checkIndentation: bool
    checkAlignment: bool


@dataclass
class TermValidationConfig:
    """术语验证配置"""
    enabled: bool
    useCnki: bool
    localTerminologyPath: str
    autoSearch: bool


@dataclass
class ExtractionConfig:
    """抽取配置"""
    includeFullChapter1: bool
    includeChapterIntroductions: bool
    includeChapterConclusions: bool
    includeFirstIntroParagraphOfLevel2: bool
    includeFirstIntroParagraphOfLevel3: bool
    dropFrontMatter: bool
    dropBackMatter: bool


@dataclass
class StageProfile:
    """阶段配置"""
    description: str
    refs: List[Dict[str, Any]]


@dataclass
class ReviewJobConfig:
    """审校任务配置"""
    projectId: str
    defaultTarget: Dict[str, str]
    stageProfiles: Dict[str, StageProfile]
    extraction: ExtractionConfig
    formatCheck: FormatCheckConfig
    termValidation: TermValidationConfig
    enabledChecks: Dict[str, bool]
    version: str
    note: str = ""
    
    # 用户覆盖的字段
    targetPath: Optional[str] = None
    outputDir: Optional[str] = None
    userRefs: List[Dict[str, Any]] = field(default_factory=list)

    def _stage_number(self, stage: str | int | None) -> int:
        value = str(stage or "stage1").strip().lower()
        if value.startswith("stage"):
            value = value[5:]
        try:
            return int(value)
        except Exception:
            return 1

    def _merged_refs_with_stage(self) -> List[Dict[str, Any]]:
        merged_by_id: Dict[str, Dict[str, Any]] = {}
        ordered_ids: List[str] = []
        for stage_name, stage_profile in self.stageProfiles.items():
            stage_number = self._stage_number(stage_name)
            for ref in stage_profile.refs:
                ref_id = ref.get("id")
                if not ref_id:
                    continue
                payload = copy.deepcopy(ref)
                payload.setdefault("stage", stage_number)
                if ref_id not in merged_by_id:
                    merged_by_id[ref_id] = payload
                    ordered_ids.append(ref_id)
                else:
                    merged_by_id[ref_id].update(payload)
                    merged_by_id[ref_id].setdefault("stage", stage_number)

        for user_ref in self.userRefs:
            ref_id = user_ref.get("id")
            if not ref_id:
                continue
            payload = copy.deepcopy(user_ref)
            payload.setdefault("stage", 1)
            if ref_id not in merged_by_id:
                merged_by_id[ref_id] = payload
                ordered_ids.append(ref_id)
            else:
                merged = copy.deepcopy(merged_by_id[ref_id])
                merged.update(payload)
                merged_by_id[ref_id] = merged

        return [merged_by_id[ref_id] for ref_id in ordered_ids]
    
    def get_active_refs(self, stage: str = "stage1") -> List[Dict[str, Any]]:
        """获取指定阶段启用的参照"""
        requested_stage = self._stage_number(stage)
        active_refs = []
        for ref in self._merged_refs_with_stage():
            ref_stage = self._stage_number(ref.get("stage"))
            enabled = ref.get("enabled")
            if enabled is None:
                enabled = True
            if ref_stage == requested_stage and bool(enabled):
                active_refs.append(copy.deepcopy(ref))
        return active_refs
    
    def _find_user_ref(self, ref_id: str) -> Optional[Dict[str, Any]]:
        """在用户提供的参照中查找匹配项"""
        for ref in self.userRefs:
            if ref.get("id") == ref_id:
                return ref
        return None
    
    def get_primary_refs(self) -> List[Dict[str, Any]]:
        """获取当前 stage 中标记为 primary 的参照。"""
        refs = self.get_active_refs("stage1")
        return [ref for ref in refs if ref.get("primary", False)]

    def get_style_profile_refs(self) -> List[Dict[str, Any]]:
        """获取 refs 风格画像专用参照集。

        规则：
        - 不复用 stage1/stage2 的启停逻辑；
        - 默认汇总所有 stageProfiles 中声明过的 refs；
        - 允许用户用 styleProfileEnabled 显式关闭单篇 ref；
        - 若用户覆盖了 path / label / enabled 等字段，以用户配置为准。
        """
        output: List[Dict[str, Any]] = []
        for merged in self._merged_refs_with_stage():
            if merged.get("styleProfileEnabled", True) is False:
                continue
            output.append(copy.deepcopy(merged))
        return output


def load_defaults() -> Dict[str, Any]:
    """加载项目默认配置"""
    if not DEFAULTS_PATH.exists():
        raise FileNotFoundError(f"项目默认配置文件不存在: {DEFAULTS_PATH}")
    
    with open(DEFAULTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _construct_dataclass(cls, data: Dict[str, Any]):
    """忽略配置里 dataclass 未声明的附加字段（如 description）。"""
    allowed = {f.name for f in fields(cls)}
    filtered = {k: v for k, v in (data or {}).items() if k in allowed}
    return cls(**filtered)


def create_job_config(user_config: Optional[Dict[str, Any]] = None) -> ReviewJobConfig:
    """
    创建审校任务配置，合并用户配置和默认配置
    
    Args:
        user_config: 用户提供的配置覆盖
        
    Returns:
        规范化后的任务配置
    """
    # 加载默认配置
    defaults = load_defaults()
    
    # 如果用户提供了配置，合并
    if user_config:
        config = _merge_configs(defaults, user_config)
    else:
        config = defaults
    
    # 创建配置对象
    return ReviewJobConfig(
        projectId=config.get("projectId", ""),
        defaultTarget=config.get("defaultTarget", {}),
        stageProfiles={
            stage_name: StageProfile(
                description=stage_data.get("description", ""),
                refs=stage_data.get("refs", [])
            )
            for stage_name, stage_data in config.get("stageProfiles", {}).items()
        },
        extraction=_construct_dataclass(ExtractionConfig, config.get("extraction", {})),
        formatCheck=_construct_dataclass(FormatCheckConfig, config.get("formatCheck", {})),
        termValidation=_construct_dataclass(TermValidationConfig, config.get("termValidation", {})),
        enabledChecks=config.get("enabledChecks", {}),
        version=config.get("version", "1.0"),
        note=config.get("note", ""),
        targetPath=user_config.get("target", {}).get("path") if user_config else None,
        outputDir=user_config.get("outputDir") if user_config else None,
        userRefs=user_config.get("refs", []) if user_config else []
    )


def _merge_configs(defaults: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    """深度合并配置"""
    result = copy.deepcopy(defaults)
    
    # 合并顶级字段
    for key, value in user.items():
        if key == "refs":
            # 特殊处理参照：用用户参照覆盖默认参照
            result["refs"] = _merge_refs(defaults.get("refs", []), value)
        elif key == "stageProfiles" and isinstance(value, dict):
            # 合并阶段配置
            for stage_name, stage_data in value.items():
                if stage_name in result["stageProfiles"]:
                    result["stageProfiles"][stage_name].update(stage_data)
                else:
                    result["stageProfiles"][stage_name] = stage_data
        elif isinstance(value, dict) and key in result and isinstance(result[key], dict):
            # 深度合并字典
            result[key].update(value)
        else:
            # 直接覆盖
            result[key] = value
    
    return result


def _merge_refs(default_refs: List[Dict[str, Any]], user_refs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """合并参照列表"""
    result = []
    ref_by_id = {ref["id"]: ref for ref in default_refs}
    
    # 用用户参照覆盖默认参照
    for user_ref in user_refs:
        ref_id = user_ref.get("id")
        if ref_id in ref_by_id:
            # 合并
            merged = copy.deepcopy(ref_by_id[ref_id])
            merged.update(user_ref)
            ref_by_id[ref_id] = merged
        else:
            # 新增
            ref_by_id[ref_id] = user_ref
    
    # 保持原始顺序（基于默认顺序）
    for default_ref in default_refs:
        if default_ref["id"] in ref_by_id:
            result.append(ref_by_id[default_ref["id"]])
    
    # 添加新增的参照
    for ref_id, ref in ref_by_id.items():
        if ref_id not in [r["id"] for r in result]:
            result.append(ref)
    
    return result


def main():
    """测试函数：验证默认配置加载"""
    try:
        config = create_job_config()
        print("默认配置加载成功:")
        print(f"项目ID: {config.projectId}")
        print(f"主要参照: {[ref['label'] for ref in config.get_primary_refs()]}")
        print(f"格式检查启用: {config.formatCheck.enabled}")
        print(f"术语验证启用: {config.termValidation.enabled}")
    except Exception as e:
        print(f"配置加载失败: {e}")


if __name__ == "__main__":
    main()
