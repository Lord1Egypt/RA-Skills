"""
GhostShield 核心模块
协调 PII 检测、风格分析、混淆处理、效果评估
"""

from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
import json

from .pii_detector import PIIDetector
from .style_analyzer import StyleAnalyzer
from .obfuscator import Obfuscator
from .validator import Validator


@dataclass
class GhostShieldResult:
    """处理结果"""
    success: bool
    output_path: Optional[Path]
    report: Dict[str, Any]
    errors: List[str]


class GhostShield:
    """
    GhostShield 主类
    
    用法:
        gs = GhostShield()
        result = gs.process(
            input_path="./my-repo",
            output_path="./protected-repo",
            level=2,
            enable_watermark=False
        )
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化 GhostShield
        
        Args:
            config: 配置字典，可包含:
                - custom_pii_rules: 自定义 PII 检测规则
                - style_db_path: 风格数据库路径（用于 Level 3 风格注入）
                - watermark_secret: 水印密钥
        """
        self.config = config or {}
        
        # 初始化各模块
        self.pii_detector = PIIDetector(
            custom_rules=self.config.get("custom_pii_rules", [])
        )
        self.style_analyzer = StyleAnalyzer()
        self.obfuscator = Obfuscator(
            style_db_path=self.config.get("style_db_path")
        )
        self.validator = Validator()
    
    def analyze(self, input_path: str) -> Dict[str, Any]:
        """
        分析风格特征和 PII 风险
        
        Args:
            input_path: 输入路径（Git 仓库或文件目录）
        
        Returns:
            分析报告，包含:
            - style_fingerprint: 风格指纹向量
            - pii_risks: PII 风险列表
            - distillation_risk: 蒸馏风险评分 (0-1)
            - recommendations: 保护建议
        """
        input_path = Path(input_path)
        
        # 1. PII 检测
        pii_results = self.pii_detector.scan(input_path)
        
        # 2. 风格分析
        style_fingerprint = self.style_analyzer.analyze(input_path)
        
        # 3. 计算蒸馏风险
        distillation_risk = self._calculate_distillation_risk(
            style_fingerprint, pii_results
        )
        
        # 4. 生成建议
        recommendations = self._generate_recommendations(
            pii_results, style_fingerprint, distillation_risk
        )
        
        return {
            "style_fingerprint": style_fingerprint,
            "pii_risks": pii_results,
            "distillation_risk": distillation_risk,
            "recommendations": recommendations,
        }
    
    def process(
        self,
        input_path: str,
        output_path: str,
        level: int = 1,
        enable_watermark: bool = False,
        watermark_id: Optional[str] = None,
    ) -> GhostShieldResult:
        """
        执行混淆处理
        
        Args:
            input_path: 输入路径
            output_path: 输出路径
            level: 混淆级别 (1/2/3)
            enable_watermark: 是否启用水印（仅 Level 3）
            watermark_id: 水印标识符
        
        Returns:
            处理结果
        """
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        errors = []
        
        try:
            # 1. 分析原始风格
            original_style = self.style_analyzer.analyze(input_path)
            
            # 2. PII 检测
            pii_results = self.pii_detector.scan(input_path)
            
            # 3. 执行混淆
            obfuscation_result = self.obfuscator.obfuscate(
                input_path=input_path,
                output_path=output_path,
                level=level,
                pii_results=pii_results,
                enable_watermark=enable_watermark,
                watermark_id=watermark_id,
            )
            
            # 4. 评估混淆效果
            obfuscated_style = self.style_analyzer.analyze(output_path)
            evaluation = self.validator.evaluate(
                original_style=original_style,
                obfuscated_style=obfuscated_style,
                pii_results=pii_results,
                output_path=output_path,
            )
            
            # 5. 生成报告
            report = {
                "level": level,
                "pii_detected": len(pii_results),
                "pii_sanitized": obfuscation_result.get("pii_sanitized", 0),
                "style_distance": evaluation["style_distance"],
                "capability_retention": evaluation["capability_retention"],
                "distillation_risk_before": original_style.get("risk_score", 0),
                "distillation_risk_after": obfuscated_style.get("risk_score", 0),
                "watermark_enabled": enable_watermark,
            }
            
            return GhostShieldResult(
                success=True,
                output_path=output_path,
                report=report,
                errors=[],
            )
        
        except Exception as e:
            errors.append(str(e))
            return GhostShieldResult(
                success=False,
                output_path=None,
                report={},
                errors=errors,
            )
    
    def evaluate(
        self,
        original_path: str,
        obfuscated_path: str,
    ) -> Dict[str, Any]:
        """
        评估混淆效果
        
        Args:
            original_path: 原始路径
            obfuscated_path: 混淆后路径
        
        Returns:
            评估报告
        """
        original_style = self.style_analyzer.analyze(original_path)
        obfuscated_style = self.style_analyzer.analyze(obfuscated_path)
        
        return self.validator.evaluate(
            original_style=original_style,
            obfuscated_style=obfuscated_style,
            pii_results=[],
            output_path=obfuscated_path,
        )
    
    def _calculate_distillation_risk(
        self,
        style_fingerprint: Dict[str, Any],
        pii_results: List[Dict[str, Any]],
    ) -> float:
        """
        计算蒸馏风险评分
        
        综合考虑:
        - 风格特征的独特性
        - PII 暴露程度
        - 可提取信息量
        """
        # 风格独特性评分 (0-1)
        style_uniqueness = style_fingerprint.get("uniqueness_score", 0.5)
        
        # PII 暴露评分 (0-1)
        pii_exposure = min(len(pii_results) / 100, 1.0)
        
        # 综合风险
        risk = (style_uniqueness * 0.7) + (pii_exposure * 0.3)
        
        return round(risk, 2)
    
    def _generate_recommendations(
        self,
        pii_results: List[Dict[str, Any]],
        style_fingerprint: Dict[str, Any],
        distillation_risk: float,
    ) -> List[str]:
        """生成保护建议"""
        recommendations = []
        
        # PII 建议
        if len(pii_results) > 0:
            recommendations.append(
                f"检测到 {len(pii_results)} 处敏感信息，建议使用 Level 1+ 进行脱敏"
            )
        
        # 风格建议
        uniqueness = style_fingerprint.get("uniqueness_score", 0)
        if uniqueness > 0.7:
            recommendations.append(
                "你的代码风格非常独特，建议使用 Level 2+ 降低风格显著性"
            )
        
        # 综合建议
        if distillation_risk > 0.8:
            recommendations.append(
                "高风险：建议使用 Level 3 极致隐匿进行主动防御"
            )
        elif distillation_risk > 0.5:
            recommendations.append(
                "中风险：建议使用 Level 2 深度混淆"
            )
        else:
            recommendations.append(
                "低风险：Level 1 基础防护即可"
            )
        
        return recommendations
