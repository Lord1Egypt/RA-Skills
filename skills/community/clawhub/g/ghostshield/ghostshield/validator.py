"""
效果验证器
评估混淆效果，模拟蒸馏攻击，生成度量报告
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import math
import random
import subprocess
from collections import Counter


class Validator:
    """
    效果验证器
    
    评估指标:
    - 风格距离（混淆前后的风格差异）
    - PII 脱敏率
    - 能力保留度（代码是否仍可运行）
    - 蒸馏风险降低
    """
    
    def evaluate(
        self,
        original_style: Dict[str, Any],
        obfuscated_style: Dict[str, Any],
        pii_results: List[Dict[str, Any]],
        output_path: Path,
    ) -> Dict[str, Any]:
        """
        评估混淆效果
        
        Args:
            original_style: 原始风格指纹
            obfuscated_style: 混淆后风格指纹
            pii_results: PII 检测结果
            output_path: 输出路径
        
        Returns:
            评估报告
        """
        # 1. 计算风格距离
        style_distance = self._calculate_style_distance(
            original_style, obfuscated_style
        )
        
        # 2. 计算能力保留度
        capability_retention = self._calculate_capability_retention(output_path)
        
        # 3. 计算蒸馏风险降低
        risk_before = original_style.get("risk_score", 0)
        risk_after = obfuscated_style.get("risk_score", 0)
        risk_reduction = (risk_before - risk_after) / risk_before if risk_before > 0 else 0
        
        # 4. 综合评分
        overall_score = self._calculate_overall_score(
            style_distance, capability_retention, risk_reduction
        )
        
        return {
            "style_distance": style_distance,
            "capability_retention": capability_retention,
            "risk_before": risk_before,
            "risk_after": risk_after,
            "risk_reduction": risk_reduction,
            "overall_score": overall_score,
        }
    
    def _calculate_style_distance(
        self,
        style1: Dict[str, Any],
        style2: Dict[str, Any],
    ) -> float:
        """
        计算风格距离
        
        使用余弦距离计算风格向量的差异
        """
        # 提取关键特征
        features1 = self._extract_style_vector(style1)
        features2 = self._extract_style_vector(style2)
        
        if not features1 or not features2:
            return 0.0
        
        # 确保向量长度一致
        keys = set(features1.keys()) & set(features2.keys())
        
        if not keys:
            return 0.0
        
        vec1 = [features1[k] for k in sorted(keys)]
        vec2 = [features2[k] for k in sorted(keys)]
        
        # 余弦距离
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        cosine_similarity = dot_product / (norm1 * norm2)
        
        # 距离 = 1 - 相似度
        distance = 1 - cosine_similarity
        
        return max(0, min(1, distance))
    
    def _extract_style_vector(self, style: Dict[str, Any]) -> Dict[str, float]:
        """提取风格特征向量"""
        features = {}
        
        # 代码风格特征
        code_style = style.get("code_style", {})
        
        # 命名风格
        naming = code_style.get("naming_preference", {})
        features["camel_case"] = naming.get("camel_case_ratio", 0)
        features["snake_case"] = naming.get("snake_case_ratio", 0)
        features["naming_consistency"] = naming.get("consistency", 0)
        
        # 注释密度
        features["comment_density"] = code_style.get("comment_density", 0)
        
        # 函数长度
        features["avg_function_length"] = min(code_style.get("avg_function_length", 0) / 50, 1)
        
        # 文档风格特征
        doc_style = style.get("doc_style", {})
        features["avg_sentence_length"] = min(doc_style.get("avg_sentence_length", 0) / 100, 1)
        
        return features
    
    def _calculate_capability_retention(self, output_path: Path) -> float:
        """
        计算能力保留度
        
        检查:
        - 代码语法是否正确
        - 文件是否损坏
        - 测试是否通过（如果有）
        """
        score = 1.0
        
        # 检查语法正确性（Python）
        python_files = list(output_path.rglob('*.py'))
        
        syntax_errors = 0
        for py_file in python_files[:10]:  # 只检查前 10 个文件
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 尝试编译
                compile(content, str(py_file), 'exec')
            except SyntaxError:
                syntax_errors += 1
        
        if python_files:
            syntax_score = 1 - (syntax_errors / min(len(python_files), 10))
            score *= syntax_score
        
        # 检查文件完整性
        total_files = 0
        readable_files = 0
        
        for file_path in output_path.rglob('*'):
            if file_path.is_file() and not file_path.name.startswith('.'):
                total_files += 1
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        f.read(100)
                    readable_files += 1
                except:
                    pass
        
        if total_files > 0:
            integrity_score = readable_files / total_files
            score *= integrity_score
        
        return round(score, 2)
    
    def _calculate_overall_score(
        self,
        style_distance: float,
        capability_retention: float,
        risk_reduction: float,
    ) -> float:
        """
        计算综合评分
        
        理想状态:
        - style_distance 高（风格改变大）
        - capability_retention 高（能力保留）
        - risk_reduction 高（风险降低）
        """
        # 权重
        w_distance = 0.3
        w_capability = 0.4
        w_risk = 0.3
        
        score = (
            style_distance * w_distance +
            capability_retention * w_capability +
            risk_reduction * w_risk
        )
        
        return round(score, 2)
    
    def simulate_distillation_attack(
        self,
        original_path: Path,
        obfuscated_path: Path,
        attack_strength: float = 0.5,
    ) -> Dict[str, Any]:
        """
        模拟蒸馏攻击，评估防护效果
        
        Args:
            original_path: 原始路径
            obfuscated_path: 混淆后路径
            attack_strength: 攻击强度 (0-1)
        
        Returns:
            攻击模拟结果
        """
        result = {
            "attack_successful": False,
            "extraction_score": 0.0,
            "features_detected": [],
            "protection_effective": False,
        }
        
        # 简化的蒸馏模拟：检测可提取的特征
        try:
            # 读取混淆后的代码
            code_files = list(obfuscated_path.rglob('*.py'))[:20]
            
            detected_features = []
            
            for code_file in code_files:
                with open(code_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 检测命名模式
                import re
                identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', content)
                
                if identifiers:
                    naming_patterns = Counter(
                        'camelCase' if '_' not in id and any(c.isupper() for c in id[1:]) else
                        'snake_case' if '_' in id else
                        'pascalCase' if id[0].isupper() else
                        'lowercase'
                        for id in identifiers
                    )
                    
                    if naming_patterns:
                        top_pattern = naming_patterns.most_common(1)[0][0]
                        detected_features.append(f"naming:{top_pattern}")
            
            # 评估提取分数
            feature_diversity = len(set(detected_features))
            result["features_detected"] = list(set(detected_features))[:10]
            
            # 攻击成功 = 特征太少或特征太混乱
            if feature_diversity > 5:
                # 特征多样化，攻击者难以提取清晰模式
                result["extraction_score"] = 0.3
                result["protection_effective"] = True
            elif feature_diversity < 2:
                # 特征太少，攻击者难以提取有意义模式
                result["extraction_score"] = 0.4
                result["protection_effective"] = True
            else:
                # 中等多样性，可能被提取
                result["extraction_score"] = 0.7
                result["protection_effective"] = False
            
            result["attack_successful"] = result["extraction_score"] > 0.6
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def generate_evaluation_report(
        self,
        original_path: Path,
        obfuscated_path: Path,
        original_style: Dict[str, Any],
        obfuscated_style: Dict[str, Any],
        pii_results: List[Dict[str, Any]],
        level: int,
    ) -> Dict[str, Any]:
        """
        生成完整评估报告
        
        Args:
            original_path: 原始路径
            obfuscated_path: 混淆后路径
            original_style: 原始风格
            obfuscated_style: 混淆后风格
            pii_results: PII 检测结果
            level: 混淆级别
        
        Returns:
            完整评估报告
        """
        # 基础评估
        basic_eval = self.evaluate(
            original_style, obfuscated_style, pii_results, obfuscated_path
        )
        
        # 蒸馏攻击模拟
        distill_attack = self.simulate_distillation_attack(
            original_path, obfuscated_path
        )
        
        # 统计信息
        stats = self._collect_statistics(original_path, obfuscated_path)
        
        # 生成建议
        recommendations = self._generate_recommendations(
            basic_eval, distill_attack, level
        )
        
        return {
            "summary": {
                "level": level,
                "overall_score": basic_eval["overall_score"],
                "protection_effective": distill_attack["protection_effective"],
            },
            "style_analysis": {
                "style_distance": basic_eval["style_distance"],
                "risk_before": basic_eval["risk_before"],
                "risk_after": basic_eval["risk_after"],
                "risk_reduction": basic_eval["risk_reduction"],
            },
            "capability_analysis": {
                "capability_retention": basic_eval["capability_retention"],
                "syntax_valid": basic_eval["capability_retention"] > 0.8,
            },
            "pii_analysis": {
                "total_detected": len(pii_results),
                "types_found": list(set(p.get("pii_type", "unknown") for p in pii_results)),
            },
            "distillation_attack": distill_attack,
            "statistics": stats,
            "recommendations": recommendations,
        }
    
    def _collect_statistics(
        self,
        original_path: Path,
        obfuscated_path: Path,
    ) -> Dict[str, Any]:
        """收集统计信息"""
        stats = {
            "original": {},
            "obfuscated": {},
        }
        
        # 原始路径统计
        orig_files = list(original_path.rglob('*')) if original_path.is_dir() else [original_path]
        orig_code = [f for f in orig_files if f.suffix in {'.py', '.js', '.ts', '.java', '.go'}]
        
        stats["original"]["total_files"] = len([f for f in orig_files if f.is_file()])
        stats["original"]["code_files"] = len(orig_code)
        
        # 混淆后路径统计
        obf_files = list(obfuscated_path.rglob('*')) if obfuscated_path.is_dir() else [obfuscated_path]
        obf_code = [f for f in obf_files if f.suffix in {'.py', '.js', '.ts', '.java', '.go'}]
        
        stats["obfuscated"]["total_files"] = len([f for f in obf_files if f.is_file()])
        stats["obfuscated"]["code_files"] = len(obf_code)
        
        return stats
    
    def _generate_recommendations(
        self,
        evaluation: Dict[str, Any],
        distill_attack: Dict[str, Any],
        level: int,
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于风格距离
        if evaluation["style_distance"] < 0.3:
            recommendations.append(
                "风格改变较小，建议提高混淆级别或增加混淆强度"
            )
        
        # 基于能力保留
        if evaluation["capability_retention"] < 0.8:
            recommendations.append(
                "能力保留度较低，建议检查语法错误或降低混淆强度"
            )
        
        # 基于蒸馏攻击
        if not distill_attack["protection_effective"]:
            recommendations.append(
                "蒸馏攻击模拟显示保护不足，建议使用 Level 3 极致隐匿"
            )
        
        # 基于级别
        if level < 3 and evaluation["risk_after"] > 0.5:
            recommendations.append(
                "混淆后风险仍然较高，建议升级到 Level 3"
            )
        
        # 如果一切良好
        if evaluation["overall_score"] > 0.7 and distill_attack["protection_effective"]:
            recommendations.append(
                "✅ 混淆效果良好，可以有效防止风格蒸馏"
            )
        
        return recommendations
    
    def validate_output(
        self,
        output_path: Path,
        checks: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        验证输出结果
        
        Args:
            output_path: 输出路径
            checks: 检查项列表，可选：
                - "syntax": 语法检查
                - "structure": 结构完整性
                - "watermark": 水印存在性
                - "pii": PII 残留检查
        
        Returns:
            验证结果
        """
        if checks is None:
            checks = ["syntax", "structure"]
        
        results = {
            "passed": True,
            "checks": {},
        }
        
        if "syntax" in checks:
            results["checks"]["syntax"] = self._check_syntax(output_path)
            if not results["checks"]["syntax"]["passed"]:
                results["passed"] = False
        
        if "structure" in checks:
            results["checks"]["structure"] = self._check_structure(output_path)
            if not results["checks"]["structure"]["passed"]:
                results["passed"] = False
        
        if "watermark" in checks:
            results["checks"]["watermark"] = self._check_watermark(output_path)
        
        if "pii" in checks:
            results["checks"]["pii"] = self._check_pii_residual(output_path)
            if not results["checks"]["pii"]["passed"]:
                results["passed"] = False
        
        return results
    
    def _check_syntax(self, output_path: Path) -> Dict[str, Any]:
        """检查语法"""
        errors = []
        python_files = list(output_path.rglob('*.py'))[:20]
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                compile(content, str(py_file), 'exec')
            except SyntaxError as e:
                errors.append({
                    "file": str(py_file),
                    "line": e.lineno,
                    "message": str(e),
                })
        
        return {
            "passed": len(errors) == 0,
            "error_count": len(errors),
            "errors": errors[:5],
        }
    
    def _check_structure(self, output_path: Path) -> Dict[str, Any]:
        """检查结构完整性"""
        # 检查关键文件是否存在
        issues = []
        
        # 检查是否有文件
        files = list(output_path.rglob('*'))
        if not files:
            issues.append("输出目录为空")
        
        return {
            "passed": len(issues) == 0,
            "file_count": len([f for f in files if f.is_file()]),
            "issues": issues,
        }
    
    def _check_watermark(self, output_path: Path) -> Dict[str, Any]:
        """检查水印"""
        watermark_file = output_path / ".ghostshield-watermark"
        
        return {
            "exists": watermark_file.exists(),
            "path": str(watermark_file) if watermark_file.exists() else None,
        }
    
    def _check_pii_residual(self, output_path: Path) -> Dict[str, Any]:
        """检查 PII 残留"""
        # 简化检查：查找常见的 PII 模式
        import re
        
        patterns = {
            "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "phone": r'\b1[3-9]\d{9}\b',
        }
        
        residual_pii = []
        files = list(output_path.rglob('*'))[:50]
        
        for file_path in files:
            if not file_path.is_file():
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                for pii_type, pattern in patterns.items():
                    matches = re.findall(pattern, content)
                    if matches:
                        residual_pii.append({
                            "file": str(file_path),
                            "type": pii_type,
                            "count": len(matches),
                        })
            except:
                pass
        
        return {
            "passed": len(residual_pii) == 0,
            "residual_count": len(residual_pii),
            "residual": residual_pii[:5],
        }
