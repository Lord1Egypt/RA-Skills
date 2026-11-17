"""
双轨并行架构 - 操作链提取器

从文本中提取操作步骤序列，生成 ExtractedOperationChain 对象。
"""

from typing import List
from ..operation_chain import ExtractedOperationChain
from .base_extractor import BaseExtractor
import re
from datetime import datetime


class OperationExtractor(BaseExtractor):
    """
    操作链提取器
    
    通过顺序词匹配和步骤识别，从文本中提取：
    - 操作步骤列表
    - 预期结果
    - 所需资源
    - 预估耗时
    """
    
    extractor_name = "operation"
    
    # 顺序词（中文）
    SEQUENCE_KEYWORDS_CN = [
        "首先", "第一", "第一步", "先", "初始",
        "然后", "接着", "其次", "第二", "第二步",
        "再", "随后", "接下来", "第三", "第三步",
        "最后", "最终", "末了", "第四",
    ]
    
    # 顺序词（英文）
    SEQUENCE_KEYWORDS_EN = [
        "first", "firstly", "first of all", "to begin",
        "then", "next", "second", "secondly",
        "third", "thirdly", "after that", "subsequently",
        "finally", "eventually", "last", "lastly",
    ]
    
    # 操作动词（中文）
    ACTION_VERBS_CN = [
        "执行", "运行", "启动", "打开", "关闭",
        "创建", "删除", "更新", "修改", "设置",
        "配置", "安装", "部署", "发布", "提交",
        "检查", "验证", "测试", "确认", "审批",
        "分析", "处理", "生成", "导出", "导入",
        "点击", "选择", "输入", "输出", "复制",
    ]
    
    # 操作动词（英文）
    ACTION_VERBS_EN = [
        "run", "execute", "start", "stop", "open",
        "create", "delete", "update", "modify", "configure",
        "install", "deploy", "publish", "submit", "commit",
        "check", "verify", "test", "validate", "approve",
        "analyze", "process", "generate", "export", "import",
        "click", "select", "input", "output", "copy",
    ]
    
    # 结果关键词
    OUTCOME_KEYWORDS = [
        "结果", "输出", "产出", "成果", "效果",
        "result", "output", "outcome", "deliverable",
    ]
    
    # 资源关键词
    RESOURCE_KEYWORDS = [
        "需要", "工具", "依赖", "资源", "要求",
        "need", "require", "tool", "dependency", "resource",
        "prerequisite", "precondition", "environment",
    ]
    
    # 时间关键词
    DURATION_KEYWORDS = [
        "耗时", "用时", "花费", "需要.*时间",
        "duration", "takes", "spend", "estimate",
        "分钟", "小时", "天", "周", "月",
    ]
    
    @staticmethod
    def _get_all_sequence_keywords() -> List[str]:
        """获取所有顺序词"""
        return (
            OperationExtractor.SEQUENCE_KEYWORDS_CN +
            OperationExtractor.SEQUENCE_KEYWORDS_EN
        )
    
    def extract(self, text: str, **kwargs) -> List[ExtractedOperationChain]:
        """
        从文本中提取操作链
        
        Args:
            text: 输入文本
            **kwargs: 支持参数
                - source_id: 来源标识
        
        Returns:
            操作链列表
        """
        if not text or not text.strip():
            return []
        
        # 提取步骤
        steps = self._extract_steps(text)
        
        # 如果没有通过顺序词提取到步骤，尝试列表项提取
        if not steps:
            list_items = self.extract_list_items(text)
            if list_items:
                steps = list_items
        
        # 如果还没有，尝试基于操作动词分段
        if not steps:
            steps = self._extract_by_action_verbs(text)
        
        # 提取结果和资源
        outcome = self._extract_outcome(text)
        resources = self._extract_resources(text)
        duration = self._extract_duration(text)
        
        # 计算置信度
        seq_matches = len(self.find_keywords(text, self._get_all_sequence_keywords()))
        action_matches = len(
            self.find_keywords(text, self.ACTION_VERBS_CN + self.ACTION_VERBS_EN)
        )
        total_clues = max(len(steps), 1)
        confidence = self.calculate_confidence(
            seq_matches + action_matches,
            total_clues + 1,
            0.1,
        )
        
        if confidence < self.min_confidence and not steps:
            return []
        
        chain = ExtractedOperationChain(
            chain_id=f"op_{datetime.now().strftime('%Y%m%d%H%M%S')}_{id(text) % 10000}",
            content=text[:self.max_chain_length],
            steps=steps[:10],
            expected_outcome=outcome,
            resources_needed=resources[:5],
            estimated_duration=duration,
            extraction_confidence=confidence,
        )
        
        return [chain]
    
    def _extract_steps(self, text: str) -> List[str]:
        """基于顺序词提取步骤"""
        steps = []
        all_seq = self.SEQUENCE_KEYWORDS_CN + self.SEQUENCE_KEYWORDS_EN
        
        # 按顺序词匹配
        for kw in all_seq:
            pattern = re.escape(kw) + r'[：:，,、\s]*([^。！？\.!?\n]*)'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                step = match.group(1).strip()
                if step and len(step) > 1 and step not in steps:
                    steps.append(step)
        
        # 按顺序词出现的顺序排序
        if steps:
            return steps
        
        # 尝试编号列表模式
        numbered = re.findall(
            r'(?:^|\n)\s*(\d+)[\.\)、]\s*([^\n]+)',
            text,
            re.MULTILINE
        )
        if numbered:
            steps = [item[1].strip() for item in numbered if item[1].strip()]
        
        return steps
    
    def _extract_by_action_verbs(self, text: str) -> List[str]:
        """基于操作动词提取步骤"""
        steps = []
        sentences = self.split_sentences(text)
        all_verbs = self.ACTION_VERBS_CN + self.ACTION_VERBS_EN
        
        for sent in sentences:
            if any(kw in sent.lower() for kw in all_verbs):
                if len(sent) > 3 and sent not in steps:
                    steps.append(sent)
        
        return steps[:8]
    
    def _extract_outcome(self, text: str) -> str:
        """提取预期结果"""
        for kw in self.OUTCOME_KEYWORDS:
            pattern = r'[^。！？\.!?]*' + re.escape(kw) + r'[^。！？\.!?]*'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group().strip()
                if content and len(content) > 3:
                    return content
        
        # 取最后一句作为结果
        sentences = self.split_sentences(text)
        if sentences:
            last = sentences[-1]
            if len(last) > 5:
                return last
        return ""
    
    def _extract_resources(self, text: str) -> List[str]:
        """提取所需资源"""
        resources = []
        
        for kw in self.RESOURCE_KEYWORDS:
            pattern = r'[^。！？\.!?]*' + re.escape(kw) + r'[^。！？\.!?]*'
            for match in re.finditer(pattern, text, re.IGNORECASE):
                content = match.group().strip()
                if content and len(content) > 3 and content not in resources:
                    resources.append(content)
        
        return resources[:5]
    
    def _extract_duration(self, text: str) -> str:
        """提取预估耗时"""
        # 匹配时间表达式 + 时间单位
        patterns = [
            r'耗时[：:]\s*[\d.]+[\s]*[分时天周月]',
            r'需要[\d.]+[\s]*[分时天周月]',
            r'约[\d.]+[\s]*[分时天周月]',
            r'[\d.]+[\s]*(?:分钟|小时|天|周|月)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group()
        
        return ""