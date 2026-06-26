#!/usr/bin/env python3
"""
批量商业计划书打分脚本
胡田-OPC导师-大赛标准化打分.Skill
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class ScoringConfig:
    """评分配置"""
    
    DEFAULT_WEIGHTS = {
        "team": 20,
        "market": 20,
        "innovation": 20,
        "business": 20,
        "legal_finance": 20
    }
    
    PRESET_PROFILES = {
        "standard": DEFAULT_WEIGHTS,
        "tech_innovation": {"team": 15, "market": 15, "innovation": 30, "business": 20, "legal_finance": 20},
        "internet_plus": {"team": 20, "market": 25, "innovation": 25, "business": 20, "legal_finance": 10},
        "angel": {"team": 25, "market": 20, "innovation": 20, "business": 25, "legal_finance": 10},
        "college": {"team": 20, "market": 20, "innovation": 25, "business": 20, "legal_finance": 15}
    }


class DocumentParser:
    """文档解析器基类"""
    
    SUPPORTED_FORMATS = ['.pptx', '.ppt', '.pdf', '.docx', '.doc']
    
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = ""
        self.structure = {}
        
    def parse(self) -> Dict[str, Any]:
        """解析文档"""
        raise NotImplementedError
        
    def extract_text(self) -> str:
        """提取文本"""
        return self.content
    
    def extract_sections(self) -> Dict[str, str]:
        """提取章节"""
        return self.structure


class Scorer:
    """评分器"""
    
    def __init__(self, config: Dict[str, int] = None):
        self.config = config or ScoringConfig.DEFAULT_WEIGHTS
        self.validate_config()
        
    def validate_config(self):
        """验证配置"""
        total = sum(self.config.values())
        if total != 100:
            raise ValueError(f"权重总和必须为100，当前为{total}")
            
    def score_document(self, content: str, structure: Dict) -> Dict[str, Any]:
        """评分文档"""
        scores = {
            "team": self._score_team(content, structure),
            "market": self._score_market(content, structure),
            "innovation": self._score_innovation(content, structure),
            "business": self._score_business(content, structure),
            "legal_finance": self._score_legal_finance(content, structure)
        }
        
        total = sum(scores.values())
        scores["total"] = total
        
        return scores
    
    def _score_team(self, content: str, structure: Dict) -> float:
        """团队维度评分"""
        score = 0
        
        # 创始人背景
        if any(kw in content for kw in ["博士", "硕士", "985", "211", "海归"]):
            score += 3
        if any(kw in content for kw in ["创始人", "CEO", "总裁"]):
            score += 3
        
        # 团队完整性
        team_keywords = ["技术", "产品", "市场", "运营"]
        found = sum(1 for kw in team_keywords if kw in content)
        score += min(found * 1.5, 6)
        
        # 股权结构
        if "股权" in content or "期权" in content:
            score += 2
            
        return min(score, 20)
    
    def _score_market(self, content: str, structure: Dict) -> float:
        """市场维度评分"""
        score = 0
        
        # 市场规模
        if "亿" in content or "万" in content:
            score += 5
        if any(kw in content for kw in ["TAM", "SAM", "SOM", "市场规模"]):
            score += 3
            
        # 痛点精准度
        if any(kw in content for kw in ["痛点", "需求", "问题"]):
            score += 4
            
        # 用户画像
        if any(kw in content for kw in ["用户", "客户", "目标"]):
            score += 4
            
        # 市场增速
        if any(kw in content for kw in ["增长", "增速", "趋势"]):
            score += 4
            
        return min(score, 20)
    
    def _score_innovation(self, content: str, structure: Dict) -> float:
        """创新维度评分"""
        score = 0
        
        # 技术创新
        if any(kw in content for kw in ["专利", "技术", "研发", "创新"]):
            score += 6
            
        # 模式创新
        if any(kw in content for kw in ["商业模式", "盈利", "差异化"]):
            score += 5
            
        # 竞品分析
        if any(kw in content for kw in ["竞品", "竞争对手", "对比"]):
            score += 5
            
        # 壁垒
        if any(kw in content for kw in ["壁垒", "护城河", "门槛"]):
            score += 4
            
        return min(score, 20)
    
    def _score_business(self, content: str, structure: Dict) -> float:
        """商业可行性评分"""
        score = 0
        
        # 产品成熟度
        if any(kw in content for kw in ["产品", "MVP", "上线", "用户"]):
            score += 6
            
        # 盈利模式
        if any(kw in content for kw in ["盈利", "收入", "付费"]):
            score += 5
            
        # 获客路径
        if any(kw in content for kw in ["获客", "推广", "渠道"]):
            score += 5
            
        # 现金流
        if any(kw in content for kw in ["融资", "资金", "预算"]):
            score += 4
            
        return min(score, 20)
    
    def _score_legal_finance(self, content: str, structure: Dict) -> float:
        """法务财务评分"""
        score = 0
        
        # 财务数据
        if any(kw in content for kw in ["财务", "收入", "成本", "利润"]):
            score += 6
            
        # 融资需求
        if any(kw in content for kw in ["融资", "投资", "估值"]):
            score += 5
            
        # 法律风险
        if any(kw in content for kw in ["股权", "合规", "资质"]):
            score += 5
            
        # 风险控制
        if any(kw in content for kw in ["风险", "控制", "规避"]):
            score += 4
            
        return min(score, 20)


class DeceptionDetector:
    """忽悠检测器"""
    
    RED_FLAGS = {
        "extreme_claims": ["第一", "唯一", "最好", "世界级", "顶级", "颠覆", "革命", "改变世界"],
        "unsupported": ["遥遥领先", "绝对领先", "全球领先", "亿级", "万亿"],
        "over_promise": ["6个月", "一年", "三年成为"],
        "tech_exaggeration": ["量子", "革命性", "颠覆性", "黑科技"]
    }
    
    def detect(self, content: str) -> Dict[str, Any]:
        """检测忽悠"""
        warnings = []
        score = 0
        
        for category, keywords in self.RED_FLAGS.items():
            for keyword in keywords:
                if keyword in content:
                    severity = self._get_severity(category)
                    warnings.append({
                        "type": category,
                        "keyword": keyword,
                        "severity": severity,
                        "suggestion": self._get_suggestion(category, keyword)
                    })
                    score += severity
        
        return {
            "deception_score": min(score, 30),
            "level": self._get_level(score),
            "warnings": warnings
        }
    
    def _get_severity(self, category: str) -> int:
        """获取严重程度"""
        severity_map = {
            "over_promise": 3,
            "tech_exaggeration": 3,
            "extreme_claims": 2,
            "unsupported": 2
        }
        return severity_map.get(category, 1)
    
    def _get_suggestion(self, category: str, keyword: str) -> str:
        """获取建议"""
        suggestions = {
            "extreme_claims": f"'{keyword}'表述过于绝对，建议提供具体数据支撑",
            "unsupported": f"'{keyword}'缺乏数据来源，建议引用权威报告",
            "over_promise": f"'{keyword}'时间线过于激进，建议重新评估",
            "tech_exaggeration": f"'{keyword}'描述模糊，建议说明具体技术路线"
        }
        return suggestions.get(category, "建议核实此表述")
    
    def _get_level(self, score: int) -> str:
        """获取风险等级"""
        if score <= 5:
            return "🟢 低风险"
        elif score <= 10:
            return "🟡 中风险"
        elif score <= 20:
            return "🟠 高风险"
        else:
            return "🔴 极高风险"


class BatchProcessor:
    """批量处理器"""
    
    def __init__(self, scorer: Scorer, detector: DeceptionDetector):
        self.scorer = scorer
        self.detector = detector
        self.results = []
        
    def process_folder(self, folder_path: str, extensions: List[str] = None) -> List[Dict]:
        """处理文件夹"""
        folder = Path(folder_path)
        extensions = extensions or DocumentParser.SUPPORTED_FORMATS
        
        files = []
        for ext in extensions:
            files.extend(folder.glob(f"*{ext}"))
            
        for file_path in files:
            try:
                result = self.process_file(str(file_path))
                self.results.append(result)
            except Exception as e:
                print(f"处理失败 {file_path}: {e}")
                
        return self.results
    
    def process_file(self, file_path: str) -> Dict[str, Any]:
        """处理单个文件"""
        # 实际使用时需要根据文件类型选择解析器
        # 这里简化处理，假设content已提取
        content = "示例内容"  # 实际应调用解析器
        
        # 评分
        scores = self.scorer.score_document(content, {})
        
        # 忽悠检测
        deception = self.detector.detect(content)
        
        return {
            "file_name": Path(file_path).name,
            "file_path": file_path,
            "scores": scores,
            "deception": deception,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_report(self, output_path: str):
        """生成报告"""
        report = {
            "summary": self._generate_summary(),
            "details": self.results,
            "ranking": self._generate_ranking()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        return report
    
    def _generate_summary(self) -> Dict:
        """生成汇总"""
        if not self.results:
            return {}
            
        total_scores = [r["scores"]["total"] for r in self.results]
        return {
            "total_projects": len(self.results),
            "average_score": sum(total_scores) / len(total_scores),
            "highest_score": max(total_scores),
            "lowest_score": min(total_scores),
            "deception_high_count": sum(1 for r in self.results if r["deception"]["deception_score"] > 10)
        }
    
    def _generate_ranking(self) -> List[Dict]:
        """生成排名"""
        ranked = sorted(self.results, key=lambda x: x["scores"]["total"], reverse=True)
        for i, r in enumerate(ranked, 1):
            r["rank"] = i
        return ranked


def main():
    parser = argparse.ArgumentParser(description="商业计划书批量打分工具")
    parser.add_argument("folder", help="文件夹路径")
    parser.add_argument("-o", "--output", default="output.json", help="输出文件")
    parser.add_argument("-p", "--profile", default="standard", 
                       choices=list(ScoringConfig.PRESET_PROFILES.keys()),
                       help="评分配置方案")
    
    args = parser.parse_args()
    
    # 初始化
    config = ScoringConfig.PRESET_PROFILES[args.profile]
    scorer = Scorer(config)
    detector = DeceptionDetector()
    processor = BatchProcessor(scorer, detector)
    
    # 处理
    print(f"正在处理文件夹: {args.folder}")
    results = processor.process_folder(args.folder)
    print(f"处理完成，共{len(results)}个文件")
    
    # 生成报告
    report = processor.generate_report(args.output)
    print(f"报告已生成: {args.output}")
    
    # 输出汇总
    summary = report["summary"]
    print(f"\n===== 汇总 =====")
    print(f"项目总数: {summary['total_projects']}")
    print(f"平均分: {summary['average_score']:.1f}")
    print(f"最高分: {summary['highest_score']}")
    print(f"最低分: {summary['lowest_score']}")


if __name__ == "__main__":
    main()
