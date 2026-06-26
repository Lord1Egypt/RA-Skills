#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CNC快速探明 Skill - 主入口
自动路由版本，集成到UniSkill V4

作者: 海狸 🦫
日期: 2026-04-02
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import sys
import os

# 导入参数收集器
sys.path.insert(0, "/home/admin/.openclaw/workspace/skills/cnc-quote-system")
from cnc_quote_collector import CNCQuoteCollector, ConvergenceLevel


class CNCQuickProbe:
    """CNC快速探明 Skill"""
    
    def __init__(self):
        self.collector = CNCQuoteCollector()
        self.skill_name = "cnc-quick-probe"
        self.version = "1.0.0"
    
    def should_trigger(self, context: Dict) -> Tuple[bool, str]:
        """
        判断是否应该触发此Skill
        
        Args:
            context: 包含 intent, convergence_rate, has_file 等信息
            
        Returns:
            (是否触发, 原因)
        """
        intent = context.get("intent", "")
        convergence = context.get("convergence_rate", 0)
        has_file = context.get("has_file", False)
        
        # 触发条件
        if intent != "cnc_quote":
            return False, "非报价意图"
        
        if convergence >= 0.8:
            return False, "参数完整，直接报价"
        
        if not has_file and convergence < 0.4:
            return True, "无文件且参数严重缺失"
        
        if convergence < 0.8:
            return True, f"参数不完整（收敛度{convergence*100:.0f}%）"
        
        return False, "条件不满足"
    
    def probe(self, user_input: str = "", context: Dict = None) -> Dict:
        """
        执行探明
        
        Args:
            user_input: 用户输入
            context: 上下文信息
            
        Returns:
            探明结果
        """
        context = context or {}
        
        # 合并用户输入
        combined_input = user_input
        if context.get("file_info"):
            combined_input += f" 文件:{context['file_info']}"
        
        # 收集参数
        result = self.collector.collect(combined_input)
        
        # 生成响应
        response = self._format_response(result)
        
        return {
            "skill": self.skill_name,
            "version": self.version,
            "status": "PROBING" if not result["can_quote"] else "READY",
            "convergence_rate": result["convergence_rate"],
            "can_quote": result["can_quote"],
            "questions": result["questions"],
            "current_params": result["current_params"],
            "response": response,
            "message": result["message"]
        }
    
    def update_from_response(self, user_response: str) -> Dict:
        """
        从用户回答更新参数
        
        Args:
            user_response: 用户回答
            
        Returns:
            更新后的状态
        """
        # 解析用户回答
        parsed = self._parse_user_response(user_response)
        
        # 更新参数
        for dim, value in parsed.items():
            self.collector.update(dim, value)
        
        # 检查收敛度
        result = self.collector.collect()
        
        return {
            "skill": self.skill_name,
            "convergence_rate": result["convergence_rate"],
            "can_quote": result["can_quote"],
            "message": result["message"],
            "summary": self.collector.get_summary()
        }
    
    def _parse_user_response(self, response: str) -> Dict:
        """解析用户回答"""
        import re
        parsed = {}
        
        # 材料识别
        materials = {
            "铝合金6061": ["6061", "铝合金6061", "铝6061"],
            "铝合金7075": ["7075", "铝合金7075"],
            "不锈钢304": ["304", "不锈钢304", "sus304"],
            "不锈钢316": ["316", "不锈钢316"],
            "黄铜": ["黄铜", "铜"],
            "钛合金": ["钛合金", "钛", "TC4"]
        }
        for mat, keywords in materials.items():
            if any(kw in response for kw in keywords):
                parsed["材料"] = mat
                break
        
        # 数量识别
        qty_match = re.search(r'(\d+)\s*件', response)
        if qty_match:
            parsed["数量"] = int(qty_match.group(1))
        
        # 精度识别
        tol_match = re.search(r'±0\.(\d+)', response)
        if tol_match:
            parsed["精度"] = f"±0.{tol_match.group(1)}mm"
        
        # 表面处理识别
        surfaces = ["阳极氧化", "喷砂", "抛光", "镀锌", "电镀", "发黑", "本色"]
        for surf in surfaces:
            if surf in response:
                parsed["表面处理"] = surf
                break
        
        # Ra识别
        ra_match = re.search(r'Ra\s*(\d+\.?\d*)', response, re.IGNORECASE)
        if ra_match:
            parsed["Ra"] = f"Ra {ra_match.group(1)}"
        
        return parsed
    
    def _format_response(self, result: Dict) -> str:
        """格式化响应"""
        lines = []
        
        # 标题
        conv_pct = result["convergence_rate"] * 100
        lines.append(f"📋 **参数收集**（收敛度：{conv_pct:.0f}%）")
        lines.append("")
        
        # 当前参数
        lines.append("📝 当前参数：")
        for key, value in result["current_params"].items():
            status = "✅" if value != "未填写" else "❓"
            lines.append(f"  {status} {key}: {value}")
        lines.append("")
        
        # 问题列表
        if result["questions"]:
            lines.append("❓ 请回答：")
            lines.append("")
            for i, q in enumerate(result["questions"], 1):
                required = "🔴" if q["required"] else "🟡"
                lines.append(f"{i}. {required}【{q['dimension']}】{q['question']}")
                for opt in q["options"][:4]:
                    lines.append(f"   □ {opt}")
                if len(q["options"]) > 4:
                    lines.append(f"   □ ...")
                lines.append("")
        
        # 回复提示
        lines.append("💡 快速回复示例：")
        lines.append("``")
        lines.append("材料6061，数量10件，精度±0.05，阳极氧化，Ra 1.6")
        lines.append("``")
        
        return "\n".join(lines)


# 便捷函数（供UniSkill V4调用）
def quick_probe(user_input: str, context: Dict = None) -> Dict:
    """快速探明入口"""
    skill = CNCQuickProbe()
    return skill.probe(user_input, context)


def check_trigger(context: Dict) -> Tuple[bool, str]:
    """检查是否应该触发"""
    skill = CNCQuickProbe()
    return skill.should_trigger(context)


# 测试
if __name__ == "__main__":
    skill = CNCQuickProbe()
    
    # 测试触发判断
    context = {
        "intent": "cnc_quote",
        "convergence_rate": 0.0,
        "has_file": True
    }
    
    should, reason = skill.should_trigger(context)
    print(f"触发: {should}, 原因: {reason}")
    
    # 测试探明
    result = skill.probe("用户上传STEP文件", context)
    print(result["response"])