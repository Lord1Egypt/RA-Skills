"""
PII 检测器
识别代码和文档中的敏感信息
支持：正则匹配、Git 作者分析、NER（可选）
"""

import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class PIIMatch:
    """PII 匹配结果"""
    file_path: str
    line_number: int
    pii_type: str
    original_text: str
    confidence: float
    position: tuple  # (start, end)
    context: str = ""  # 上下文（前后 50 字符）


class PIIDetector:
    """
    PII 检测器
    
    支持检测:
    - 邮箱
    - 电话号码
    - 身份证号
    - API Key / Token
    - IP 地址
    - 内部 URL
    - 密码
    - Git 作者信息
    - 自定义规则
    """
    
    # 默认规则
    DEFAULT_RULES = {
        "email": {
            "pattern": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            "description": "邮箱地址",
        },
        "phone_cn": {
            "pattern": r'\b1[3-9]\d{9}\b',
            "description": "中国大陆手机号",
        },
        "id_card_cn": {
            "pattern": r'\b\d{17}[\dXx]\b',
            "description": "中国身份证号",
        },
        "api_key": {
            "pattern": r'(api[_-]?key|apikey|token|secret|password)\s*[=:]\s*["\']?[^\s"\']{8,}',
            "description": "API Key / Token / 密码",
        },
        "ip_address": {
            "pattern": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            "description": "IP 地址",
        },
        "internal_url": {
            "pattern": r'https?://[a-zA-Z0-9.-]+\.(internal|local|company|corp|intranet)',
            "description": "内部 URL",
        },
        "aws_key": {
            "pattern": r'AKIA[0-9A-Z]{16}',
            "description": "AWS Access Key",
        },
        "github_token": {
            "pattern": r'ghp_[a-zA-Z0-9]{36}',
            "description": "GitHub Personal Access Token",
        },
    }
    
    def __init__(self, custom_rules: Optional[List[Dict[str, str]]] = None):
        """
        初始化 PII 检测器
        
        Args:
            custom_rules: 自定义规则列表，每个规则包含:
                - name: 规则名称
                - pattern: 正则表达式
                - description: 描述
        """
        self.rules = self.DEFAULT_RULES.copy()
        
        # 添加自定义规则
        if custom_rules:
            for rule in custom_rules:
                self.rules[rule["name"]] = {
                    "pattern": rule["pattern"],
                    "description": rule.get("description", ""),
                }
    
    def scan(self, input_path: Path) -> List[Dict[str, Any]]:
        """
        扫描路径中的所有文件
        
        Args:
            input_path: 输入路径（文件或目录）
        
        Returns:
            PII 匹配列表
        """
        input_path = Path(input_path)
        
        if input_path.is_file():
            return self._scan_file(input_path)
        elif input_path.is_dir():
            return self._scan_directory(input_path)
        else:
            return []
    
    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """扫描单个文件"""
        results = []
        
        # 跳过二进制文件和常见的不需要扫描的文件
        if self._should_skip(file_path):
            return results
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, start=1):
                for pii_type, rule in self.rules.items():
                    matches = re.finditer(rule["pattern"], line, re.IGNORECASE)
                    
                    for match in matches:
                        results.append({
                            "file_path": str(file_path),
                            "line_number": line_num,
                            "pii_type": pii_type,
                            "original_text": match.group(),
                            "confidence": 0.9,  # 基于规则的匹配置信度
                            "position": (match.start(), match.end()),
                            "description": rule["description"],
                        })
        
        except Exception as e:
            # 记录错误但不中断扫描
            pass
        
        return results
    
    def _scan_directory(self, dir_path: Path) -> List[Dict[str, Any]]:
        """扫描目录"""
        results = []
        
        # 跳过的目录
        skip_dirs = {
            '.git', '.svn', '__pycache__', 'node_modules', 
            'venv', '.venv', 'dist', 'build'
        }
        
        for item in dir_path.rglob('*'):
            # 跳过特定目录
            if any(skip_dir in item.parts for skip_dir in skip_dirs):
                continue
            
            if item.is_file():
                results.extend(self._scan_file(item))
        
        return results
    
    def _should_skip(self, file_path: Path) -> bool:
        """判断是否应该跳过该文件"""
        # 跳过二进制文件
        binary_extensions = {
            '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico',
            '.pdf', '.zip', '.tar', '.gz', '.rar',
            '.exe', '.dll', '.so', '.dylib',
            '.pyc', '.pyo', '.class',
        }
        
        if file_path.suffix.lower() in binary_extensions:
            return True
        
        # 跳过大文件（> 10MB）
        try:
            if file_path.stat().st_size > 10 * 1024 * 1024:
                return True
        except:
            pass
        
        return False
    
    def get_sanitized_text(
        self, 
        text: str, 
        pii_type: str,
        mode: str = "replace",
    ) -> str:
        """
        获取脱敏后的文本
        
        Args:
            text: 原始文本
            pii_type: PII 类型
            mode: 脱敏模式
                - "replace": 替换为占位符
                - "hash": 替换为哈希值
                - "redact": 完全删除
        
        Returns:
            脱敏后的文本
        """
        if pii_type not in self.rules:
            return text
        
        pattern = self.rules[pii_type]["pattern"]
        
        if mode == "replace":
            # 根据类型选择不同的占位符
            placeholders = {
                "email": "[email-removed]",
                "phone_cn": "[phone-removed]",
                "id_card_cn": "[id-removed]",
                "api_key": "[api-key-removed]",
                "ip_address": "[ip-removed]",
                "internal_url": "[internal-url]",
                "aws_key": "[aws-key-removed]",
                "github_token": "[github-token-removed]",
            }
            replacement = placeholders.get(pii_type, "[REMOVED]")
        
        elif mode == "hash":
            import hashlib
            def hash_repl(match):
                return hashlib.md5(match.group().encode()).hexdigest()[:8]
            replacement = hash_repl
        
        elif mode == "redact":
            replacement = ""
        
        else:
            replacement = "[REMOVED]"
        
        return re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    def extract_git_authors(self, repo_path: Path) -> Dict[str, List[str]]:
        """
        提取 Git 仓库中的作者信息
        
        Args:
            repo_path: Git 仓库路径
        
        Returns:
            作者信息字典: {
                "authors": ["Author Name <email@example.com>"],
                "emails": ["email@example.com"],
                "names": ["Author Name"]
            }
        """
        authors_info = {
            "authors": [],
            "emails": [],
            "names": [],
        }
        
        if not (repo_path / ".git").exists():
            return authors_info
        
        try:
            # 获取所有提交作者
            result = subprocess.run(
                ["git", "log", "--format=%an <%ae>", "--all"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            if result.returncode == 0:
                seen: Set[str] = set()
                for line in result.stdout.strip().split('\n'):
                    if line and line not in seen:
                        seen.add(line)
                        authors_info["authors"].append(line)
                        
                        # 提取邮箱和姓名
                        match = re.match(r'(.+?) <(.+?)>', line)
                        if match:
                            name, email = match.groups()
                            if name not in authors_info["names"]:
                                authors_info["names"].append(name)
                            if email not in authors_info["emails"]:
                                authors_info["emails"].append(email)
        
        except Exception as e:
            pass
        
        return authors_info
    
    def scan_git_config(self, repo_path: Path) -> List[Dict[str, Any]]:
        """
        扫描 Git 配置文件中的敏感信息
        
        Args:
            repo_path: Git 仓库路径
        
        Returns:
            PII 匹配列表
        """
        results = []
        git_config = repo_path / ".git" / "config"
        
        if not git_config.exists():
            return results
        
        try:
            with open(git_config, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            for line_num, line in enumerate(lines, start=1):
                # 检测邮箱
                email_match = re.search(r'email\s*=\s*(.+)', line, re.IGNORECASE)
                if email_match:
                    email = email_match.group(1).strip()
                    results.append({
                        "file_path": str(git_config),
                        "line_number": line_num,
                        "pii_type": "git_email",
                        "original_text": email,
                        "confidence": 1.0,
                        "position": (email_match.start(), email_match.end()),
                        "description": "Git 配置邮箱",
                    })
                
                # 检测姓名
                name_match = re.search(r'name\s*=\s*(.+)', line, re.IGNORECASE)
                if name_match:
                    name = name_match.group(1).strip()
                    results.append({
                        "file_path": str(git_config),
                        "line_number": line_num,
                        "pii_type": "git_name",
                        "original_text": name,
                        "confidence": 0.8,
                        "position": (name_match.start(), name_match.end()),
                        "description": "Git 配置姓名",
                    })
        
        except Exception as e:
            pass
        
        return results
    
    def scan_with_context(
        self, 
        input_path: Path,
        context_chars: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        扫描并返回上下文
        
        Args:
            input_path: 输入路径
            context_chars: 上下文字符数
        
        Returns:
            带上下文的 PII 匹配列表
        """
        results = self.scan(input_path)
        
        # 为每个匹配添加上下文
        file_cache: Dict[str, str] = {}
        
        for result in results:
            file_path = result["file_path"]
            
            # 缓存文件内容
            if file_path not in file_cache:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        file_cache[file_path] = f.read()
                except:
                    continue
            
            content = file_cache[file_path]
            start, end = result["position"]
            
            # 提取上下文
            context_start = max(0, start - context_chars)
            context_end = min(len(content), end + context_chars)
            result["context"] = content[context_start:context_end]
        
        return results
    
    def get_pii_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        生成 PII 检测摘要
        
        Args:
            results: PII 检测结果
        
        Returns:
            摘要报告
        """
        summary = {
            "total_count": len(results),
            "by_type": defaultdict(int),
            "by_file": defaultdict(int),
            "high_confidence_count": 0,
            "risk_score": 0.0,
        }
        
        for result in results:
            pii_type = result["pii_type"]
            file_path = result["file_path"]
            confidence = result["confidence"]
            
            summary["by_type"][pii_type] += 1
            summary["by_file"][file_path] += 1
            
            if confidence >= 0.9:
                summary["high_confidence_count"] += 1
        
        # 计算风险评分 (0-1)
        # 考虑数量、类型敏感度、置信度
        sensitive_types = {"api_key", "aws_key", "github_token", "id_card_cn"}
        sensitive_count = sum(summary["by_type"].get(t, 0) for t in sensitive_types)
        
        total = summary["total_count"]
        if total > 0:
            summary["risk_score"] = min(
                (total / 100) * 0.5 + (sensitive_count / total) * 0.5,
                1.0
            )
        
        # 转换 defaultdict 为普通 dict
        summary["by_type"] = dict(summary["by_type"])
        summary["by_file"] = dict(summary["by_file"])
        
        return summary
