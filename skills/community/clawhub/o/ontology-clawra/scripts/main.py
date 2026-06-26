#!/usr/bin/env python3
"""
ontology-clawra 主推理脚本
整合：检查本体 → 网络获取 → 典型场景 → 交互确认 → 置信度标注
"""

import os
import sys
import json
from datetime import datetime

# 添加脚本目录到路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from network_fetch import fetch_from_network, search_local, search_ontology
from typical_scenarios import TYPICAL_SCENARIOS, match_scenario, generate_confirmation_questions
from interactive_confirm import InteractiveConfirm, generate_scenario_options
from confidence_tracker import ConfidenceTracker, label_result, declare_source


class OntologyReasoner:
    """本体推理器 - 整合所有功能"""
    
    def __init__(self):
        self.tracker = ConfidenceTracker()
        self.current_confirm = None
        self.reasoning_chain = []
    
    def reason(self, query, category=None):
        """
        完整推理流程
        1. 检查本体 → 2. 网络获取 → 3. 典型场景 → 4. 交互确认 → 5. 置信度标注
        """
        print(f"\n{'='*60}")
        print(f"🔍 推理查询: {query}")
        print(f"{'='*60}")
        
        self.reasoning_chain = []
        
        # ===== 步骤1: 检查本体 =====
        print("\n📋 步骤1: 检查本地本体...")
        local_results = search_local(query.split())
        onto_results = search_ontology(query.split())
        
        if onto_results:
            print(f"  🟢 本体中有 {len(onto_results)} 条相关数据")
            self.reasoning_chain.append({
                "step": "check_ontology",
                "status": "FOUND",
                "confidence": "CONFIRMED",
                "data": onto_results
            })
            
            # 本体有数据，可以直接推理
            return self._generate_response(onto_results, query, "CONFIRMED")
        
        if local_results:
            print(f"  🟡 记忆中有 {len(local_results)} 条相关数据")
            self.reasoning_chain.append({
                "step": "check_ontology",
                "status": "FOUND_LOCAL",
                "confidence": "ASSUMED",
                "data": local_results
            })
        
        # ===== 步骤2: 尝试网络获取 =====
        print("\n🌐 步骤2: 尝试网络获取...")
        network_result = fetch_from_network(query)
        
        if network_result["status"] == "NOT_FOUND":
            print("  ⚪ 本地无相关数据，需要外部获取")
            self.reasoning_chain.append({
                "step": "network_fetch",
                "status": "NOT_FOUND",
                "confidence": "UNKNOWN",
                "suggestions": network_result.get("suggestions", [])
            })
        else:
            print(f"  🟢 网络获取成功")
        
        # ===== 步骤3: 匹配典型场景 =====
        if category and category in TYPICAL_SCENARIOS:
            print(f"\n🏠 步骤3: 匹配典型场景 ({category})...")
            scenarios = generate_scenario_options(category)
            
            if scenarios:
                print(f"  找到 {len(scenarios)} 个典型场景:")
                for s in scenarios:
                    print(f"    • {s['name']}: {s['description']}")
                
                self.reasoning_chain.append({
                    "step": "typical_scenarios",
                    "status": "MATCHED",
                    "confidence": "ASSUMED",
                    "scenarios": scenarios
                })
                
                return self._generate_scenario_response(scenarios, query)
        
        # ===== 步骤4: 需要交互确认 =====
        if category:
            return self._start_interactive_confirmation(category, query)
        
        # ===== 步骤5: 无法推进，返回建议 =====
        return self._generate_unknown_response(query)
    
    def _generate_response(self, data, query, confidence):
        """生成响应（本体有数据）"""
        print(f"\n🎯 结论: {confidence}")
        response = {
            "status": "SUCCESS",
            "confidence": confidence,
            "data": data,
            "reasoning": self.reasoning_chain
        }
        
        # 记录
        self.tracker.add_reasoning(query, confidence, "ontology", {"data_count": len(data)})
        
        return response
    
    def _generate_scenario_response(self, scenarios, query):
        """生成场景响应"""
        print(f"\n🎯 提供 {len(scenarios)} 个典型场景供选择")
        
        response = {
            "status": "NEED_SELECTION",
            "confidence": "ASSUMED",
            "message": "请选择一个最接近的场景，或回答以下问题：",
            "scenarios": scenarios,
            "questions": generate_confirmation_questions("gas_regulator", {}),
            "reasoning": self.reasoning_chain
        }
        
        # 记录
        self.tracker.add_reasoning(query, "ASSUMED", "typical_scenario", {"scenarios_count": len(scenarios)})
        
        return response
    
    def _start_interactive_confirmation(self, category, query):
        """启动交互确认"""
        self.current_confirm = InteractiveConfirm(category)
        
        intro = self.current_confirm.generate_intro_message()
        
        first_q = self.current_confirm.get_next_question()
        
        response = {
            "status": "NEED_CONFIRMATION",
            "confidence": "ASSUMED",
            "message": intro,
            "question": first_q,
            "reasoning": self.reasoning_chain
        }
        
        print(f"\n❓ {first_q['question']}")
        print(f"   选项: {first_q['options']}")
        print(f"   默认: {first_q['default']}")
        
        return response
    
    def submit_answer(self, answer):
        """提交交互回答"""
        if not self.current_confirm:
            return {"status": "ERROR", "message": "无进行中的交互"}
        
        self.current_confirm.submit_answer(answer)
        
        if self.current_confirm.is_complete():
            scenario = self.current_confirm.get_current_scenario()
            return {
                "status": "COMPLETE",
                "confidence": "ASSUMED",
                "scenario": scenario
            }
        
        next_q = self.current_confirm.get_next_question()
        return {
            "status": "CONTINUE",
            "question": next_q
        }
    
    def _generate_unknown_response(self, query):
        """生成无法推理的响应"""
        response = {
            "status": "UNKNOWN",
            "confidence": "UNKNOWN",
            "message": "无法进行推理，需要更多信息",
            "suggestions": [
                "请提供更多背景信息",
                "或指定场景类别（如 gas_regulator）",
            ]
        }
        
        # 记录
        self.tracker.add_reasoning(query, "UNKNOWN", "insufficient_info", {})
        
        return response
    
    def get_statistics(self):
        """获取推理统计"""
        return self.tracker.get_statistics()


def main():
    """测试主函数"""
    print("=" * 60)
    print("ontology-clawra 推理引擎测试")
    print("=" * 60)
    
    reasoner = OntologyReasoner()
    
    # 测试1: 调压箱选型（有典型场景）
    print("\n\n" + "="*60)
    print("测试1: 调压箱选型")
    print("="*60)
    
    result = reasoner.reason("100户居民小区调压箱选型", category="gas_regulator")
    
    print("\n📦 返回结果:")
    print(f"  状态: {result['status']}")
    print(f"  置信度: {result['confidence']}")
    
    if result.get('scenarios'):
        print(f"  场景数: {len(result['scenarios'])}")
    if result.get('question'):
        print(f"  问题: {result['question']['question']}")
    
    # 测试2: 统计
    print("\n\n" + "="*60)
    print("测试2: 置信度统计")
    print("="*60)
    
    stats = reasoner.get_statistics()
    print(f"  总推理数: {stats['total']}")
    for conf, info in stats['by_confidence'].items():
        print(f"  {conf}: {info['count']} ({info['percentage']}%)")


if __name__ == "__main__":
    main()
