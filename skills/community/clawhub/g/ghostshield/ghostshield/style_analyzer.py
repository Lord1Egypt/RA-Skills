"""
风格分析器
分析代码和文档的风格特征，生成风格指纹
支持：AST 分析、NLP、Git commit 风格、指纹向量生成
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import Counter, defaultdict
import ast
import hashlib
import json


class StyleAnalyzer:
    """
    风格分析器
    
    分析维度:
    - 代码风格：命名习惯、缩进、注释、函数长度
    - 文档风格：句式、词汇、段落结构
    - 决策风格：commit message 表达方式
    """
    
    def __init__(self):
        self.code_analyzer = CodeStyleAnalyzer()
        self.doc_analyzer = DocStyleAnalyzer()
        self.commit_analyzer = CommitStyleAnalyzer()
        self.fingerprint_generator = StyleFingerprint()
    
    def analyze(self, input_path: Path, include_commits: bool = True) -> Dict[str, Any]:
        """
        分析风格特征
        
        Args:
            input_path: 输入路径
            include_commits: 是否包含 Git commit 分析
        
        Returns:
            风格指纹字典，包含:
            - code_style: 代码风格特征
            - doc_style: 文档风格特征
            - commit_style: commit 风格特征
            - fingerprint: 风格指纹向量
            - uniqueness_score: 风格独特性评分
            - risk_score: 蒸馏风险评分
        """
        input_path = Path(input_path)
        
        code_style = {}
        doc_style = {}
        commit_style = {}
        
        if input_path.is_file():
            code_style = self.code_analyzer.analyze_file(input_path)
            doc_style = self.doc_analyzer.analyze_file(input_path)
        
        elif input_path.is_dir():
            code_style = self.code_analyzer.analyze_directory(input_path)
            doc_style = self.doc_analyzer.analyze_directory(input_path)
            
            if include_commits:
                commit_style = self.commit_analyzer.analyze(input_path)
        
        # 生成指纹
        fingerprint = self.fingerprint_generator.generate(
            code_style, doc_style, commit_style
        )
        
        # 计算独特性和风险
        uniqueness_score = self._calculate_uniqueness(code_style, doc_style, commit_style)
        risk_score = self._calculate_risk(code_style, doc_style, commit_style)
        
        return {
            "code_style": code_style,
            "doc_style": doc_style,
            "commit_style": commit_style,
            "fingerprint": fingerprint,
            "uniqueness_score": uniqueness_score,
            "risk_score": risk_score,
        }
    
    def compare_styles(
        self,
        style1: Dict[str, Any],
        style2: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        比较两个风格的相似度
        
        Args:
            style1: 风格1
            style2: 风格2
        
        Returns:
            相似度分析结果
        """
        fp1 = style1.get("fingerprint", {})
        fp2 = style2.get("fingerprint", {})
        
        overall_similarity = self.fingerprint_generator.compare(fp1, fp2)
        
        # 分维度比较
        dims1 = fp1.get("dimensions", {})
        dims2 = fp2.get("dimensions", {})
        
        dimension_similarities = {}
        for dim_name in ["naming_habits", "code_density", "doc_patterns", "commit_style"]:
            vec1 = dims1.get(dim_name, [])
            vec2 = dims2.get(dim_name, [])
            
            if vec1 and vec2:
                dot = sum(a * b for a, b in zip(vec1, vec2))
                norm1 = sum(a ** 2 for a in vec1) ** 0.5
                norm2 = sum(b ** 2 for b in vec2) ** 0.5
                
                if norm1 > 0 and norm2 > 0:
                    dimension_similarities[dim_name] = dot / (norm1 * norm2)
                else:
                    dimension_similarities[dim_name] = 0.0
            else:
                dimension_similarities[dim_name] = 0.0
        
        return {
            "overall_similarity": overall_similarity,
            "dimension_similarities": dimension_similarities,
        }
    
    def _calculate_uniqueness(
        self,
        code_style: Dict[str, Any],
        doc_style: Dict[str, Any],
        commit_style: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        计算风格独特性评分
        
        独特性越高，越容易被蒸馏
        """
        # 基于命名习惯、注释风格等的独特性
        score = 0.5
        
        # 代码命名习惯
        if code_style.get("naming_preference"):
            # 如果命名风格很统一，独特性高
            naming = code_style["naming_preference"]
            if naming.get("consistency", 0) > 0.8:
                score += 0.2
        
        # 注释密度
        if code_style.get("comment_density"):
            # 注释密度极端（很高或很低）都会增加独特性
            density = code_style["comment_density"]
            if density < 0.05 or density > 0.3:
                score += 0.15
        
        # 文档句式
        if doc_style.get("sentence_patterns"):
            # 常用句式越集中，独特性越高
            patterns = doc_style["sentence_patterns"]
            if patterns.get("top_pattern_frequency", 0) > 0.3:
                score += 0.15
        
        # commit 风格
        if commit_style:
            # 前缀使用一致性
            prefixes = commit_style.get("common_prefixes", [])
            if len(prefixes) > 0:
                top_prefix_count = prefixes[0][1] if prefixes else 0
                total = commit_style.get("total_commits", 1)
                if top_prefix_count / total > 0.5:
                    score += 0.1
        
        return min(score, 1.0)
    
    def _calculate_risk(
        self,
        code_style: Dict[str, Any],
        doc_style: Dict[str, Any],
        commit_style: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        计算蒸馏风险评分
        
        风险 = 独特性 × 可提取信息量
        """
        uniqueness = self._calculate_uniqueness(code_style, doc_style, commit_style)
        
        # 可提取信息量（代码量、文档量）
        info_volume = 0.5
        
        if code_style.get("file_count", 0) > 50:
            info_volume += 0.2
        
        if code_style.get("total_lines", 0) > 10000:
            info_volume += 0.2
        
        if commit_style and commit_style.get("total_commits", 0) > 100:
            info_volume += 0.1
        
        risk = uniqueness * 0.7 + min(info_volume, 1.0) * 0.3
        
        return min(risk, 1.0)


class CodeStyleAnalyzer:
    """代码风格分析器"""
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """分析单个代码文件"""
        result = {
            "file_count": 1,
            "total_lines": 0,
            "naming_preference": {},
            "comment_density": 0,
            "indent_style": "unknown",
            "avg_function_length": 0,
            "design_patterns": [],
        }
        
        # 只分析代码文件
        code_extensions = {'.py', '.js', '.ts', '.java', '.go', '.c', '.cpp'}
        if file_path.suffix.lower() not in code_extensions:
            return result
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            result["total_lines"] = len(lines)
            
            # 分析命名习惯
            result["naming_preference"] = self._analyze_naming(content)
            
            # 分析注释密度
            result["comment_density"] = self._analyze_comments(content, lines)
            
            # 分析缩进风格
            result["indent_style"] = self._analyze_indent(lines)
            
            # 分析函数长度
            result["avg_function_length"] = self._analyze_function_length(content)
        
        except:
            pass
        
        return result
    
    def analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """分析目录中的代码"""
        results = {
            "file_count": 0,
            "total_lines": 0,
            "naming_preference": {},
            "comment_density": 0,
            "indent_style": "unknown",
            "avg_function_length": 0,
        }
        
        all_naming = []
        all_comment_density = []
        all_function_length = []
        indent_counter = Counter()
        
        code_extensions = {'.py', '.js', '.ts', '.java', '.go', '.c', '.cpp'}
        
        for file_path in dir_path.rglob('*'):
            if file_path.suffix.lower() in code_extensions:
                file_result = self.analyze_file(file_path)
                
                results["file_count"] += 1
                results["total_lines"] += file_result["total_lines"]
                
                all_naming.append(file_result["naming_preference"])
                all_comment_density.append(file_result["comment_density"])
                all_function_length.append(file_result["avg_function_length"])
                indent_counter[file_result["indent_style"]] += 1
        
        # 聚合统计
        if all_comment_density:
            results["comment_density"] = sum(all_comment_density) / len(all_comment_density)
        
        if all_function_length:
            results["avg_function_length"] = sum(all_function_length) / len(all_function_length)
        
        if indent_counter:
            results["indent_style"] = indent_counter.most_common(1)[0][0]
        
        # 合并命名偏好
        if all_naming:
            results["naming_preference"] = self._merge_naming_preferences(all_naming)
        
        return results
    
    def _analyze_naming(self, content: str) -> Dict[str, Any]:
        """分析命名习惯"""
        # 提取标识符
        identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', content)
        
        if not identifiers:
            return {}
        
        # 分类命名风格
        camel_case = 0
        snake_case = 0
        pascal_case = 0
        upper_case = 0
        
        for ident in identifiers:
            if '_' in ident and ident.isupper():
                upper_case += 1
            elif '_' in ident:
                snake_case += 1
            elif ident[0].isupper():
                pascal_case += 1
            elif ident[0].islower() and any(c.isupper() for c in ident[1:]):
                camel_case += 1
        
        total = len(identifiers)
        
        return {
            "camel_case_ratio": camel_case / total,
            "snake_case_ratio": snake_case / total,
            "pascal_case_ratio": pascal_case / total,
            "upper_case_ratio": upper_case / total,
            "consistency": max(
                camel_case / total,
                snake_case / total,
                pascal_case / total,
                upper_case / total,
            ),
        }
    
    def _analyze_comments(self, content: str, lines: List[str]) -> float:
        """分析注释密度"""
        comment_lines = 0
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('#') or stripped.startswith('//'):
                comment_lines += 1
        
        return comment_lines / len(lines) if lines else 0
    
    def _analyze_indent(self, lines: List[str]) -> str:
        """分析缩进风格"""
        spaces = 0
        tabs = 0
        
        for line in lines:
            if line.startswith('    '):
                spaces += 1
            elif line.startswith('\t'):
                tabs += 1
        
        if spaces > tabs:
            return "spaces"
        elif tabs > spaces:
            return "tabs"
        else:
            return "mixed"
    
    def _analyze_function_length(self, content: str) -> float:
        """分析函数平均长度"""
        # 简单统计（基于 Python）
        try:
            tree = ast.parse(content)
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            
            if not functions:
                return 0
            
            lengths = []
            for func in functions:
                length = func.end_lineno - func.lineno + 1 if hasattr(func, 'end_lineno') else 0
                lengths.append(length)
            
            return sum(lengths) / len(lengths) if lengths else 0
        except:
            return 0
    
    def _merge_naming_preferences(self, preferences: List[Dict]) -> Dict[str, Any]:
        """合并命名偏好"""
        if not preferences:
            return {}
        
        merged = {
            "camel_case_ratio": 0,
            "snake_case_ratio": 0,
            "pascal_case_ratio": 0,
            "upper_case_ratio": 0,
            "consistency": 0,
        }
        
        for pref in preferences:
            if pref:
                merged["camel_case_ratio"] += pref.get("camel_case_ratio", 0)
                merged["snake_case_ratio"] += pref.get("snake_case_ratio", 0)
                merged["pascal_case_ratio"] += pref.get("pascal_case_ratio", 0)
                merged["upper_case_ratio"] += pref.get("upper_case_ratio", 0)
                merged["consistency"] += pref.get("consistency", 0)
        
        n = len([p for p in preferences if p])
        if n > 0:
            for key in merged:
                merged[key] /= n
        
        return merged


class DocStyleAnalyzer:
    """文档风格分析器"""
    
    def analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """分析单个文档文件"""
        result = {
            "file_count": 1,
            "total_lines": 0,
            "sentence_patterns": {},
            "top_words": [],
            "avg_sentence_length": 0,
        }
        
        doc_extensions = {'.md', '.txt', '.rst', '.doc', '.docx'}
        if file_path.suffix.lower() not in doc_extensions:
            return result
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            result["total_lines"] = len(lines)
            result["sentence_patterns"] = self._analyze_sentence_patterns(content)
            result["top_words"] = self._analyze_top_words(content)
            result["avg_sentence_length"] = self._analyze_sentence_length(content)
        
        except:
            pass
        
        return result
    
    def analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """分析目录中的文档"""
        results = {
            "file_count": 0,
            "total_lines": 0,
            "sentence_patterns": {},
            "top_words": [],
            "avg_sentence_length": 0,
        }
        
        all_patterns = []
        all_words = []
        all_lengths = []
        
        doc_extensions = {'.md', '.txt', '.rst', '.doc', '.docx'}
        
        for file_path in dir_path.rglob('*'):
            if file_path.suffix.lower() in doc_extensions:
                file_result = self.analyze_file(file_path)
                
                results["file_count"] += 1
                results["total_lines"] += file_result["total_lines"]
                
                all_patterns.append(file_result["sentence_patterns"])
                all_words.extend(file_result["top_words"])
                all_lengths.append(file_result["avg_sentence_length"])
        
        # 聚合
        if all_lengths:
            results["avg_sentence_length"] = sum(all_lengths) / len(all_lengths)
        
        if all_words:
            word_counter = Counter(all_words)
            results["top_words"] = word_counter.most_common(20)
        
        return results
    
    def _analyze_sentence_patterns(self, content: str) -> Dict[str, Any]:
        """分析句式模式"""
        # 简单的句式识别
        patterns = {
            "declarative": 0,  # 陈述句
            "interrogative": 0,  # 疑问句
            "imperative": 0,  # 祈使句
            "exclamatory": 0,  # 感叹句
        }
        
        sentences = re.split(r'[。！？.!?]', content)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # 简单判断
            if sentence.endswith('?') or sentence.endswith('？'):
                patterns["interrogative"] += 1
            elif sentence.endswith('!') or sentence.endswith('！'):
                patterns["exclamatory"] += 1
            elif sentence.startswith(('请', 'Please', 'Let\'s', '要')):
                patterns["imperative"] += 1
            else:
                patterns["declarative"] += 1
        
        total = sum(patterns.values())
        if total > 0:
            for key in patterns:
                patterns[key] = patterns[key] / total
        
        return {
            "distribution": patterns,
            "top_pattern_frequency": max(patterns.values()) if patterns else 0,
        }
    
    def _analyze_top_words(self, content: str) -> List[str]:
        """分析高频词"""
        # 简单分词（中文按字，英文按词）
        words = re.findall(r'\b[a-zA-Z]+\b', content)
        # 中文词（简单按2-3字组合）
        chinese = re.findall(r'[\u4e00-\u9fff]{2,3}', content)
        
        all_words = words + chinese
        
        # 过滤停用词
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', '的', '是', '在'}
        all_words = [w for w in all_words if w.lower() not in stopwords]
        
        counter = Counter(all_words)
        return [word for word, count in counter.most_common(50)]
    
    def _analyze_sentence_length(self, content: str) -> float:
        """分析平均句子长度"""
        sentences = re.split(r'[。！？.!?]', content)
        
        if not sentences:
            return 0
        
        lengths = [len(s.strip()) for s in sentences if s.strip()]
        
        return sum(lengths) / len(lengths) if lengths else 0


class CommitStyleAnalyzer:
    """Git commit 风格分析器"""
    
    def analyze(self, repo_path: Path) -> Dict[str, Any]:
        """
        分析 Git commit message 风格
        
        Args:
            repo_path: Git 仓库路径
        
        Returns:
            commit 风格分析结果
        """
        result = {
            "total_commits": 0,
            "avg_message_length": 0,
            "common_prefixes": [],
            "emoji_usage": 0,
            "style_type": "unknown",
            "top_keywords": [],
        }
        
        if not (repo_path / ".git").exists():
            return result
        
        try:
            # 获取 commit messages
            cmd_result = subprocess.run(
                ["git", "log", "--format=%s", "--all", "-n", "500"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30,
            )
            
            if cmd_result.returncode != 0:
                return result
            
            messages = cmd_result.stdout.strip().split('\n')
            messages = [m for m in messages if m]
            
            result["total_commits"] = len(messages)
            
            if not messages:
                return result
            
            # 平均长度
            lengths = [len(m) for m in messages]
            result["avg_message_length"] = sum(lengths) / len(lengths)
            
            # 常见前缀（如 feat:, fix:, docs:）
            prefix_pattern = r'^(\w+)(\([^)]+\))?:\s*'
            prefixes = []
            for msg in messages:
                match = re.match(prefix_pattern, msg)
                if match:
                    prefixes.append(match.group(1))
            
            if prefixes:
                prefix_counter = Counter(prefixes)
                result["common_prefixes"] = prefix_counter.most_common(10)
                result["style_type"] = "conventional"
            
            # emoji 使用率
            emoji_pattern = r'[\U0001F300-\U0001F9FF]'
            emoji_count = sum(1 for m in messages if re.search(emoji_pattern, m))
            result["emoji_usage"] = emoji_count / len(messages)
            
            # 关键词
            keywords = []
            for msg in messages:
                # 提取动词
                words = re.findall(r'\b[a-zA-Z]+\b', msg.lower())
                keywords.extend(words)
            
            # 过滤停用词
            stopwords = {'a', 'an', 'the', 'to', 'for', 'in', 'on', 'of', 'and', 'or', 'is', 'are'}
            keywords = [w for w in keywords if w not in stopwords and len(w) > 2]
            
            keyword_counter = Counter(keywords)
            result["top_keywords"] = keyword_counter.most_common(20)
        
        except Exception as e:
            pass
        
        return result


class StyleFingerprint:
    """风格指纹生成器"""
    
    def generate(
        self,
        code_style: Dict[str, Any],
        doc_style: Dict[str, Any],
        commit_style: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        生成风格指纹
        
        Args:
            code_style: 代码风格
            doc_style: 文档风格
            commit_style: commit 风格
        
        Returns:
            风格指纹，包含向量表示和哈希
        """
        # 特征向量
        features = []
        
        # 代码风格特征
        naming = code_style.get("naming_preference", {})
        features.extend([
            naming.get("camel_case_ratio", 0),
            naming.get("snake_case_ratio", 0),
            naming.get("pascal_case_ratio", 0),
            naming.get("consistency", 0),
        ])
        
        features.append(code_style.get("comment_density", 0))
        features.append(1.0 if code_style.get("indent_style") == "spaces" else 0.0)
        features.append(min(code_style.get("avg_function_length", 0) / 50, 1.0))
        
        # 文档风格特征
        patterns = doc_style.get("sentence_patterns", {})
        dist = patterns.get("distribution", {})
        features.extend([
            dist.get("declarative", 0),
            dist.get("interrogative", 0),
            dist.get("imperative", 0),
        ])
        
        features.append(min(doc_style.get("avg_sentence_length", 0) / 100, 1.0))
        
        # commit 风格特征
        if commit_style:
            features.append(min(commit_style.get("avg_message_length", 0) / 100, 1.0))
            features.append(commit_style.get("emoji_usage", 0))
            features.append(1.0 if commit_style.get("style_type") == "conventional" else 0.0)
        else:
            features.extend([0, 0, 0])
        
        # 生成指纹哈希
        feature_str = json.dumps(features, sort_keys=True)
        fingerprint_hash = hashlib.sha256(feature_str.encode()).hexdigest()[:16]
        
        return {
            "vector": features,
            "hash": fingerprint_hash,
            "dimensions": {
                "naming_habits": features[0:4],
                "code_density": features[4:7],
                "doc_patterns": features[7:11],
                "commit_style": features[11:14],
            },
        }
    
    def compare(self, fp1: Dict[str, Any], fp2: Dict[str, Any]) -> float:
        """
        比较两个指纹的相似度
        
        Args:
            fp1: 指纹1
            fp2: 指纹2
        
        Returns:
            相似度 (0-1)
        """
        vec1 = fp1.get("vector", [])
        vec2 = fp2.get("vector", [])
        
        if len(vec1) != len(vec2):
            return 0.0
        
        if not vec1:
            return 0.0
        
        # 余弦相似度
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a ** 2 for a in vec1) ** 0.5
        norm2 = sum(b ** 2 for b in vec2) ** 0.5
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
