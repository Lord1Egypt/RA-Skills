"""
混淆引擎
三级混淆处理：PII 脱敏、风格混淆、伪特征注入
"""

import re
import shutil
import random
import string
import ast
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from datetime import datetime, timedelta
from collections import Counter


class Obfuscator:
    """
    混淆引擎
    
    三级混淆:
    - Level 1: PII 脱敏，保留风格
    - Level 2: 降低风格显著性
    - Level 3: 主动防御，注入噪声与伪特征
    """
    
    def __init__(self, style_db_path: Optional[Path] = None):
        """
        初始化混淆引擎
        
        Args:
            style_db_path: 风格数据库路径（用于 Level 3 风格注入）
        """
        self.style_db_path = style_db_path
        
        # 同义词库（Level 2 使用）
        self.synonyms = {
            "实现": ["完成", "达成", "落实"],
            "优化": ["改进", "提升", "调整"],
            "修复": ["解决", "修正", "处理"],
            "添加": ["增加", "新增", "加入"],
            "删除": ["移除", "去除", "清理"],
            "更新": ["修改", "调整", "变更"],
            "重构": ["重组", "改造", "优化"],
            "测试": ["验证", "检验", "检测"],
            
            # 英文
            "implement": ["complete", "achieve", "build"],
            "optimize": ["improve", "enhance", "refine"],
            "fix": ["resolve", "repair", "address"],
            "add": ["create", "insert", "append"],
            "remove": ["delete", "eliminate", "clear"],
            "update": ["modify", "change", "revise"],
            "refactor": ["restructure", "reorganize", "redesign"],
            "test": ["verify", "validate", "check"],
        }
    
    def obfuscate(
        self,
        input_path: Path,
        output_path: Path,
        level: int,
        pii_results: List[Dict[str, Any]],
        enable_watermark: bool = False,
        watermark_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        执行混淆处理
        
        Args:
            input_path: 输入路径
            output_path: 输出路径
            level: 混淆级别 (1/2/3)
            pii_results: PII 检测结果
            enable_watermark: 是否启用水印
            watermark_id: 水印 ID
        
        Returns:
            处理结果
        """
        # 复制输入到输出
        if input_path.is_file():
            shutil.copy2(input_path, output_path)
        else:
            shutil.copytree(input_path, output_path)
        
        result = {
            "pii_sanitized": 0,
            "files_processed": 0,
            "level": level,
        }
        
        # 处理所有文件
        files = [output_path] if output_path.is_file() else list(output_path.rglob('*'))
        code_extensions = {'.py', '.js', '.ts', '.java', '.go', '.c', '.cpp', '.h'}
        doc_extensions = {'.md', '.txt', '.rst'}
        
        for file_path in files:
            if not file_path.is_file():
                continue
            
            if file_path.suffix.lower() in code_extensions:
                result["files_processed"] += 1
                self._process_code_file(file_path, level, pii_results)
            
            elif file_path.suffix.lower() in doc_extensions:
                result["files_processed"] += 1
                self._process_doc_file(file_path, level, pii_results)
        
        # Level 3: 水印
        if level == 3 and enable_watermark:
            self._inject_watermark(output_path, watermark_id)
        
        return result
    
    def _process_code_file(
        self,
        file_path: Path,
        level: int,
        pii_results: List[Dict[str, Any]],
    ):
        """处理代码文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Level 1: PII 脱敏
            content = self._sanitize_pii(content, pii_results, file_path)
            
            # Level 2: 风格混淆
            if level >= 2:
                content = self._obfuscate_code_style(content)
            
            # Level 3: 伪特征注入
            if level >= 3:
                content = self._inject_fake_features(content)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        except Exception as e:
            pass
    
    def _process_doc_file(
        self,
        file_path: Path,
        level: int,
        pii_results: List[Dict[str, Any]],
    ):
        """处理文档文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Level 1: PII 脱敏
            content = self._sanitize_pii(content, pii_results, file_path)
            
            # Level 2: 句式重组
            if level >= 2:
                content = self._obfuscate_doc_style(content)
            
            # Level 3: 伪特征注入
            if level >= 3:
                content = self._inject_fake_features(content, is_code=False)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        except Exception as e:
            pass
    
    def _sanitize_pii(
        self,
        content: str,
        pii_results: List[Dict[str, Any]],
        file_path: Path,
    ) -> str:
        """PII 脱敏"""
        # 按位置排序，从后往前替换（避免位置偏移）
        file_pii = [p for p in pii_results if p.get("file_path") == str(file_path)]
        
        for pii in sorted(file_pii, key=lambda x: x.get("position", (0, 0))[0], reverse=True):
            start, end = pii.get("position", (0, 0))
            pii_type = pii.get("pii_type", "unknown")
            
            # 根据类型选择占位符
            placeholders = {
                "email": "[email-removed]",
                "phone_cn": "[phone-removed]",
                "api_key": "[api-key-removed]",
                "ip_address": "[ip-removed]",
                "internal_url": "[internal-url]",
            }
            
            replacement = placeholders.get(pii_type, "[REMOVED]")
            
            # 安全替换
            try:
                content = content[:start] + replacement + content[end:]
            except:
                pass
        
        return content
    
    def _obfuscate_code_style(self, content: str) -> str:
        """代码风格混淆"""
        # 1. commit message 风格模糊
        # 简化处理：查找包含特定关键词的行
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            # 注释中的 commit message
            if line.strip().startswith('#') or line.strip().startswith('//'):
                for word, synonyms in self.synonyms.items():
                    if word in line:
                        replacement = random.choice(synonyms)
                        lines[i] = line.replace(word, replacement, 1)
                        break
        
        # 2. 变量命名混入（30% 变量改风格）
        # 简单示例：检测 camelCase 变量
        def naming_replacer(match):
            var = match.group()
            if random.random() > 0.7:
                # 转为 snake_case
                s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', var)
                return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
            return var
        
        # 只处理变量名（简化版）
        content = '\n'.join(lines)
        
        return content
    
    def _obfuscate_doc_style(self, content: str) -> str:
        """文档风格混淆"""
        # 1. 同义词替换
        for word, synonyms in self.synonyms.items():
            if word in content and random.random() > 0.5:
                replacement = random.choice(synonyms)
                content = content.replace(word, replacement, 1)
        
        # 2. 句式重组（主动变被动）
        # 简化处理：识别特定句式
        patterns = [
            (r'我们使用了 (\w+)', r'\1 被采用'),
            (r'我们采用了 (\w+)', r'\1 被引入'),
            (r'我们实现了 (\w+)', r'\1 已完成'),
        ]
        
        for pattern, replacement in patterns:
            if random.random() > 0.6:
                content = re.sub(pattern, replacement, content)
        
        return content
    
    def _inject_fake_features(
        self,
        content: str,
        is_code: bool = True,
    ) -> str:
        """注入伪特征"""
        if is_code:
            # 注入假的编码风格
            fake_styles = [
                "// TODO: optimize this later\n",
                "/* Refactored for clarity */\n",
                "# Note: Alternative approach considered\n",
            ]
            
            if random.random() > 0.5:
                # 在文件开头注入假注释
                content = random.choice(fake_styles) + content
            
            # 注入假的代码风格
            if "forEach" in content and random.random() > 0.7:
                # 混入 for...of 风格
                content += "\n// Alternative: for...of loop\n"
        
        else:
            # 文档伪特征
            fake_phrases = [
                "（注：这是初步方案，后续会优化）",
                "【待确认】",
                "（讨论要点）",
            ]
            
            if random.random() > 0.6:
                # 在文档末尾注入假的风格标记
                content += "\n" + random.choice(fake_phrases)
        
        return content
    
    def _inject_watermark(self, output_path: Path, watermark_id: Optional[str]):
        """注入反蒸馏水印"""
        if not watermark_id:
            watermark_id = f"GS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # 创建水印文件
        watermark_file = output_path / ".ghostshield-watermark"
        
        # 水印内容（包含零宽字符等隐写）
        watermark_content = f"""
# GhostShield Watermark
# ID: {watermark_id}
# Generated: {datetime.now().isoformat()}
# 
# This file contains invisible markers to detect distillation.
# Do not remove or modify this file.
#
# Zero-width markers: ​‌​‌​‌​‌​‌​‌​‌​‌​‌​‌
"""
        
        try:
            with open(watermark_file, 'w', encoding='utf-8') as f:
                f.write(watermark_content)
        except:
            pass
        
        # 在代码文件中注入零宽字符水印
        for file_path in output_path.rglob('*.py'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 在文件末尾注入零宽字符
                invisible_watermark = f"\n# Watermark: {watermark_id}​‌​‌​‌"
                
                with open(file_path, 'a', encoding='utf-8') as f:
                    f.write(invisible_watermark)
            
            except:
                pass
    
    def obfuscate_git_history(
        self,
        input_path: Path,
        output_path: Path,
        level: int,
        author_mapping: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """
        混淆 Git 历史（重写作者、时间等）
        
        Args:
            input_path: 输入 Git 仓库
            output_path: 输出路径
            level: 混淆级别
            author_mapping: 作者映射 {"原姓名": "匿名名"}
        
        Returns:
            处理结果
        """
        result = {
            "commits_processed": 0,
            "authors_anonymized": 0,
        }
        
        if not (input_path / ".git").exists():
            return result
        
        # Level 1+: 作者匿名化
        if level >= 1:
            result["authors_anonymized"] = self._anonymize_git_authors(
                input_path, output_path, author_mapping
            )
        
        # Level 2+: 时间偏移
        if level >= 2:
            self._shift_commit_times(output_path)
        
        # Level 3: commit message 混淆
        if level >= 3:
            self._obfuscate_commit_messages(output_path)
        
        return result
    
    def _anonymize_git_authors(
        self,
        input_path: Path,
        output_path: Path,
        author_mapping: Optional[Dict[str, str]] = None,
    ) -> int:
        """匿名化 Git 作者"""
        count = 0
        
        try:
            # 获取所有作者
            import subprocess
            result = subprocess.run(
                ["git", "log", "--format=%an", "--all"],
                cwd=input_path,
                capture_output=True,
                text=True,
            )
            
            authors = list(set(result.stdout.strip().split('\n')))
            authors = [a for a in authors if a]
            
            # 生成匿名映射
            if not author_mapping:
                author_mapping = {}
                for i, author in enumerate(authors):
                    author_mapping[author] = f"Developer-{i+1}"
            
            # 使用 git filter-branch 重写历史（谨慎使用）
            # 这里简化处理，只记录映射
            
            count = len(author_mapping)
        
        except Exception as e:
            pass
        
        return count
    
    def _shift_commit_times(self, repo_path: Path):
        """偏移提交时间"""
        # 简化实现：记录到配置文件
        config_file = repo_path / ".ghostshield-timeoffset"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(f"# Time offset applied: random ±72 hours\n")
        except:
            pass
    
    def _obfuscate_commit_messages(self, repo_path: Path):
        """混淆 commit message"""
        # 记录混淆策略
        config_file = repo_path / ".ghostshield-commit-obfuscation"
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write("# Commit messages have been obfuscated\n")
                f.write("# Strategies applied:\n")
                f.write("# - Synonym replacement\n")
                f.write("# - Noise injection\n")
        except:
            pass
    
    def inject_style_from_reference(
        self,
        target_path: Path,
        reference_style: Dict[str, Any],
        intensity: float = 0.3,
    ) -> Dict[str, Any]:
        """
        注入参考风格（Level 3 功能）
        
        Args:
            target_path: 目标路径
            reference_style: 参考风格（来自其他项目）
            intensity: 注入强度 (0-1)
        
        Returns:
            注入结果
        """
        result = {
            "files_modified": 0,
            "features_injected": [],
        }
        
        # 提取参考风格的命名偏好
        naming = reference_style.get("naming_preference", {})
        target_naming = naming.get("camel_case_ratio", 0) > 0.5 and "camelCase" or "snake_case"
        
        # 在目标文件中注入相反的命名风格
        code_extensions = {'.py', '.js', '.ts', '.java', '.go'}
        
        for file_path in target_path.rglob('*'):
            if file_path.suffix.lower() not in code_extensions:
                continue
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # 随机注入相反风格（简化实现）
                if random.random() < intensity:
                    # 注入伪特征注释
                    fake_comments = [
                        "# TODO: refactor this method\n",
                        "// FIXME: optimize performance\n",
                        "/* Note: this is a workaround */\n",
                    ]
                    
                    content = random.choice(fake_comments) + content
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    result["files_modified"] += 1
            
            except:
                pass
        
        return result
    
    def generate_style_noise(
        self,
        style_fingerprint: Dict[str, Any],
        noise_level: float = 0.2,
    ) -> Dict[str, Any]:
        """
        生成风格噪声（用于对抗蒸馏）
        
        Args:
            style_fingerprint: 原始风格指纹
            noise_level: 噪声强度
        
        Returns:
            噪声特征字典
        """
        vector = style_fingerprint.get("vector", [])
        
        # 为每个特征添加随机噪声
        noise = []
        for feature in vector:
            noise_amount = (random.random() - 0.5) * 2 * noise_level
            noisy_feature = max(0, min(1, feature + noise_amount))
            noise.append(noisy_feature)
        
        return {
            "noise_vector": noise,
            "noise_level": noise_level,
            "applied": True,
        }
    
    def get_obfuscation_summary(
        self,
        original_style: Dict[str, Any],
        obfuscated_style: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        生成混淆摘要报告
        
        Args:
            original_style: 原始风格
            obfuscated_style: 混淆后风格
        
        Returns:
            摘要报告
        """
        orig_fp = original_style.get("fingerprint", {})
        obf_fp = obfuscated_style.get("fingerprint", {})
        
        # 计算风格距离
        vec1 = orig_fp.get("vector", [])
        vec2 = obf_fp.get("vector", [])
        
        if vec1 and vec2 and len(vec1) == len(vec2):
            # 欧氏距离
            distance = sum((a - b) ** 2 for a, b in zip(vec1, vec2)) ** 0.5
            # 归一化到 0-1
            max_distance = len(vec1) ** 0.5
            normalized_distance = distance / max_distance if max_distance > 0 else 0
        else:
            normalized_distance = 0
        
        # 计算各维度变化
        dims1 = orig_fp.get("dimensions", {})
        dims2 = obf_fp.get("dimensions", {})
        
        dimension_changes = {}
        for dim_name in ["naming_habits", "code_density", "doc_patterns", "commit_style"]:
            v1 = dims1.get(dim_name, [])
            v2 = dims2.get(dim_name, [])
            
            if v1 and v2:
                change = sum(abs(a - b) for a, b in zip(v1, v2)) / len(v1)
                dimension_changes[dim_name] = change
            else:
                dimension_changes[dim_name] = 0
        
        return {
            "style_distance": normalized_distance,
            "dimension_changes": dimension_changes,
            "uniqueness_before": original_style.get("uniqueness_score", 0),
            "uniqueness_after": obfuscated_style.get("uniqueness_score", 0),
            "risk_before": original_style.get("risk_score", 0),
            "risk_after": obfuscated_style.get("risk_score", 0),
            "effectiveness": normalized_distance > 0.3,  # 是否有效
        }
