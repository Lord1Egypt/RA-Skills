#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""原子Skill共享校验模块 — CRS强制卡点 + 三段校验锁
坤图_GIS:V5.0 | 所有原子Skill InputValidator强制导入

功能:
1. CRS强制卡点：任何含空间数据的输入必须检测坐标系
2. 三段校验锁：输入校验→执行中校验→输出合规校验
3. ArtifactSchema：工序间传递凭证标准化
"""

import json
import logging
from datetime import datetime
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# ═══════════════════════════════════════════════════════════════════════════
# §1 CRS强制卡点 (所有原子Skill的InputValidator必须调用)
# ═══════════════════════════════════════════════════════════════════════════

CRS_REQUIRED_FIELDS = ["name", "wkid", "type", "unit"]
CRS_UNKNOWN_PATTERNS = ["Unknown", "未定义", "Undefined", "", None]
CRS_MIN_ACCEPTABLE_WKID = 1  # WKID=0 表示未定义


def crs_checkpoint(data_path, logger=None, context: str = "") -> Tuple[bool, Dict, List[str]]:
    """CRS强制卡点：检测输入数据的坐标系是否有效。
    
    Args:
        data_path: 数据路径 (GDB要素类/SHP/TIF/GPKG等)
        logger: 日志记录器
        context: 调用上下文描述
    
    Returns:
        (pass_check, crs_info, issues)
    """
    issues = []
    crs_info = {"name": "未检测", "wkid": 0, "type": "未知", "unit": "未知", "wkt": ""}

    log = logger or logging.getLogger("crs_checkpoint")

    try:
        # 尝试 arcpy
        import arcpy
        desc = arcpy.Describe(data_path)
        sr = desc.spatialReference

        if sr is None:
            issues.append(f"[CRS-严重] {context}: 无坐标系定义 (spatialReference=None)")
            log.error(f"CRS卡点失败 [{context}]: 无坐标系")
            return False, crs_info, issues

        crs_info["name"] = sr.name or "未定义"
        crs_info["wkid"] = sr.factoryCode or 0
        crs_info["type"] = sr.type or "未知"
        crs_info["unit"] = (sr.linearUnitName if sr.type == "Projected" else sr.angularUnitName) or "未知"

        if crs_info["name"] in CRS_UNKNOWN_PATTERNS:
            issues.append(f"[CRS-严重] {context}: 坐标系名称为未知 ({crs_info['name']})")
            log.error(f"CRS卡点失败 [{context}]: 未知坐标系名称")
            return False, crs_info, issues

        if crs_info["wkid"] < CRS_MIN_ACCEPTABLE_WKID:
            issues.append(f"[CRS-严重] {context}: WKID={crs_info['wkid']} (无效)")
            log.error(f"CRS卡点失败 [{context}]: WKID无效")
            return False, crs_info, issues

        log.info(f"CRS卡点通过 [{context}]: {crs_info['name']} (EPSG:{crs_info['wkid']})")
        return True, crs_info, issues

    except ImportError:
        # 降级到 GDAL
        try:
            from osgeo import ogr, osr
            ds = ogr.Open(data_path)
            if ds:
                layer = ds.GetLayer()
                sr = layer.GetSpatialRef()
                if sr:
                    crs_info["name"] = sr.GetName() or "GDAL-未命名"
                    crs_info["wkid"] = int(sr.GetAuthorityCode(None) or 0)
                    crs_info["type"] = "Projected" if sr.IsProjected() else "Geographic"
                    crs_info["unit"] = sr.GetAttrValue("UNIT") or "未知"
                    crs_info["wkt"] = sr.ExportToWkt()[:200]

                    if crs_info["wkid"] < CRS_MIN_ACCEPTABLE_WKID:
                        issues.append(f"[CRS-严重] {context}: WKID无效 (GDAL检测)")
                        return False, crs_info, issues

                    log.info(f"CRS卡点通过(GDAL) [{context}]: {crs_info['name']}")
                    return True, crs_info, issues
                else:
                    issues.append(f"[CRS-严重] {context}: GDAL无法读取坐标系")
                    return False, crs_info, issues
        except ImportError:
            issues.append(f"[CRS-警告] {context}: arcpy和GDAL均不可用，跳过CRS检测")
            log.warning(f"CRS卡点跳过 [{context}]: 无可用的GIS引擎")
            return True, crs_info, issues  # 不阻断执行但记录警告
        except Exception as e:
            issues.append(f"[CRS-错误] {context}: GDAL异常 {e}")
            return False, crs_info, issues

    except Exception as e:
        issues.append(f"[CRS-错误] {context}: {e}")
        log.exception(f"CRS卡点异常 [{context}]")
        return False, crs_info, issues


# ═══════════════════════════════════════════════════════════════════════════
# §2 ArtifactSchema — 工序间传递凭证标准化
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class ArtifactSchema:
    """工序间传递凭证标准格式（所有原子Skill输出必须包含此结构）"""
    task_id: str = ""
    skill_id: str = ""           # 如 ATS-001
    skill_name: str = ""
    version: str = "V5.0"
    timestamp: str = ""          # ISO 8601
    status: str = "success"      # success | failed | partial | skipped
    duration_seconds: float = 0.0

    # 输入信息
    input_crs: Dict = field(default_factory=dict)
    input_path: str = ""
    input_info: Dict = field(default_factory=dict)

    # 输出信息
    output_crs: Dict = field(default_factory=dict)
    output_path: str = ""
    output_files: List[str] = field(default_factory=list)

    # 工序记录
    steps_completed: List[str] = field(default_factory=list)
    steps_skipped: List[str] = field(default_factory=list)
    steps_failed: List[Dict] = field(default_factory=list)

    # 校验结果
    validations: Dict = field(default_factory=lambda: {
        "input_check": True,
        "mid_check": True,
        "output_check": True,
    })

    # 元数据
    processing_engine: str = ""   # arcpy | geopandas | gdal | fme
    processing_time_iso: str = ""
    retry_count: int = 0
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    # 下一道工序
    next_step: str = ""
    artifact_ready: bool = True

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_json(self, path=None) -> str:
        data = self.to_dict()
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        if path:
            Path(path).write_text(json_str, encoding="utf-8")
        return json_str

    @classmethod
    def from_dict(cls, data: Dict) -> "ArtifactSchema":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


def create_artifact(skill_id: str, skill_name: str, input_path: str = "",
                    output_path: str = "", output_files: Optional[List[str]] = None,
                    status: str = "success", **kwargs) -> ArtifactSchema:
    """工厂方法：创建标准化工序凭证"""
    return ArtifactSchema(
        skill_id=skill_id,
        skill_name=skill_name,
        input_path=input_path,
        output_path=output_path,
        output_files=output_files or [],
        status=status,
        processing_time_iso=datetime.now().isoformat(timespec="seconds"),
        **kwargs,
    )


# ═══════════════════════════════════════════════════════════════════════════
# §3 7条输出禁令程序化检测器
# ═══════════════════════════════════════════════════════════════════════════

BANNED_PATTERNS = {
    "BAN-01": {
        "name": "禁止空谈理论",
        "pattern": r"^(理论上|从理论.*看|在理论.*层面|原则上)",
        "severity": "critical",
        "fix": "必须给出可落地执行的代码/步骤/参数",
    },
    "BAN-02": {
        "name": "禁止残缺示例",
        "pattern": r"(此处略|自行.*(实现|填写|补充|配置)|视情况.*定|根据实际.*调整)",
        "severity": "critical",
        "fix": "必须提供完整可运行的代码示例",
    },
    "BAN-03": {
        "name": "禁止甩锅话术",
        "pattern": r"(建议.*手动|请根据.*实际|建议.*验证|可能.*大概|不确定)",
        "severity": "critical",
        "fix": "必须给出确定性方案，不确定时说明原因并给出备选方案",
    },
    "BAN-04": {
        "name": "禁止绕过校验",
        "pattern": r"(跳过.*校验|省略.*检查|无需.*验证|假设.*正确)",
        "severity": "critical",
        "fix": "必须执行完整的三段校验（输入→执行中→输出）",
    },
    "BAN-05": {
        "name": "禁止无限迭代",
        "pattern": r"^(重新.*执行|再次.*尝试)$",
        "severity": "warning",
        "fix": "同一任务最多3轮迭代，第3轮失败触发熔断",
    },
    "BAN-06": {
        "name": "禁止交付残缺",
        "pattern": r"(TODO|待补充|待完善|待优化|待.*更新)$",
        "severity": "warning",
        "fix": "交付物必须完整可用，待补充项必须标注优先级和截止日期",
    },
    "BAN-07": {
        "name": "禁止跨权限操作",
        "pattern": r"(人工.*处理|需人工.*确认|需.*审批|需.*授权)",
        "severity": "info",
        "fix": "明确标注需人工介入的节点，不得超过自动处理边界",
    },
}


def scan_for_bans(text: str, source: str = "") -> List[Dict]:
    """扫描文本中的7条禁令违规
    
    Returns:
        [{ban_id, ban_name, severity, matched_text, source, fix}]
    """
    violations = []
    for ban_id, ban_info in BANNED_PATTERNS.items():
        import re
        matches = re.findall(ban_info["pattern"], text, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            violations.append({
                "ban_id": ban_id,
                "ban_name": ban_info["name"],
                "severity": ban_info["severity"],
                "matched_text": match if isinstance(match, str) else str(match),
                "source": source,
                "fix": ban_info["fix"],
            })
    return violations


# ═══════════════════════════════════════════════════════════════════════════
# §4 三段校验锁模板基类
# ═══════════════════════════════════════════════════════════════════════════

class TripleCheckpoint:
    """三段校验锁基类 — 所有原子Skill的main()函数必须包含这三段"""

    def __init__(self, skill_id: str, skill_name: str):
        self.skill_id = skill_id
        self.skill_name = skill_name
        self.artifact = create_artifact(skill_id, skill_name)
        self.logger = logging.getLogger(f"triple_check.{skill_id}")

    def input_check(self, data_paths: List[str]) -> Tuple[bool, List[str]]:
        """第一段：输入校验 — 包含CRS强制卡点"""
        issues = []
        for dp in data_paths:
            passed, crs_info, crs_issues = crs_checkpoint(
                dp, self.logger, f"{self.skill_id}/{dp}"
            )
            self.artifact.input_crs = crs_info
            issues.extend(crs_issues)
            if not passed:
                self.artifact.validations["input_check"] = False
        return len([i for i in issues if "严重" in i]) == 0, issues

    def mid_check(self) -> Tuple[bool, List[str]]:
        """第二段：执行中校验 — 子类必须重写"""
        return True, []

    def output_check(self, output_paths: List[str]) -> Tuple[bool, List[str]]:
        """第三段：输出合规校验 — 检查输出文件是否存在/有效"""
        issues = []
        for op in output_paths:
            if not Path(op).exists():
                issues.append(f"[输出-严重] 输出文件不存在: {op}")
                self.artifact.validations["output_check"] = False

            # CRS输出检查
            if any(op.lower().endswith(ext) for ext in ['.shp', '.gdb', '.gpkg', '.tif', '.tiff']):
                passed, crs_info, crs_issues = crs_checkpoint(
                    op, self.logger, f"{self.skill_id}/output:{op}"
                )
                self.artifact.output_crs = crs_info
                issues.extend(crs_issues)
                if not passed:
                    self.artifact.validations["output_check"] = False

        return len([i for i in issues if "严重" in i]) == 0, issues

    def finalize(self, output_dir: str) -> ArtifactSchema:
        """完成工序，输出标准化凭证"""
        self.artifact.timestamp = datetime.now().isoformat(timespec="seconds")

        # 保存artifact.json
        artifact_path = Path(output_dir) / "artifact.json"
        self.artifact.to_json(str(artifact_path))
        self.logger.info(f"工序凭证已保存: {artifact_path}")

        return self.artifact


# ═══════════════════════════════════════════════════════════════════════════
# §5 便捷函数
# ═══════════════════════════════════════════════════════════════════════════

def validate_input_with_crs(data_path: str, logger=None) -> Tuple[bool, List[str]]:
    """便捷函数：单文件CRS校验"""
    passed, crs_info, issues = crs_checkpoint(data_path, logger)
    return passed, issues


def validate_output_with_crs(data_path: str, logger=None) -> Tuple[bool, List[str]]:
    """便捷函数：输出文件CRS校验"""
    if not Path(data_path).exists():
        return False, [f"输出文件不存在: {data_path}"]
    return validate_input_with_crs(data_path, logger)
