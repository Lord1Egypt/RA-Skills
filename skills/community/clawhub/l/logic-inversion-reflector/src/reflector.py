"""
Logic Inversion Reflector (LIR-v2)
核心逻辑实现
"""

import json
import re
from typing import List, Dict, Any


class LogicInversionReflector:
    """逻辑反转反射器"""
    
    def __init__(self):
        self.common_axioms = self._load_common_axioms()
    
    def _load_common_axioms(self) -> Dict[str, str]:
        """加载常见公理库"""
        return {
            "效率": "效率总是好的",
            "增长": "增长是目标",
            "自动化": "自动化优于人工",
            "集中": "集中控制优于分散",
            "标准化": "标准化优于定制化",
            "速度": "快速迭代优于完美规划",
            "数据": "数据驱动优于直觉",
            "AI": "AI 应该辅助人类",
            "扁平": "扁平化优于科层制",
            "透明": "透明优于保密",
            "协作": "协作优于竞争",
            "长期": "长期主义优于短期利益",
            "用户": "用户体验第一",
            "创新": "创新优于守成",
            "规模": "规模化是成功标志",
            "核心": "核心业务优先于边缘业务"
        }
    
    def extract_anchors(self, text: str) -> List[str]:
        """
        第一阶段：特征提取
        从用户输入中提取 3-5 个核心假设锚点
        """
        anchors = []
        
        # 策略 1: 识别常见公理关键词
        for keyword, axiom in self.common_axioms.items():
            if keyword in text and axiom not in anchors:
                anchors.append(axiom)
                if len(anchors) >= 3:
                    break
        
        # 策略 2: 识别"应该"、"必须"等强假设
        patterns = [
            r'应该 (.*?) ',
            r'必须 (.*?) ',
            r'是 (.*?) 的',
            r'优先 (.*?) ',
            r'优于 (.*?) '
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches[:2]:
                anchor = f"{match.strip()}"
                if anchor and anchor not in anchors:
                    anchors.append(anchor)
                    if len(anchors) >= 5:
                        break
        
        # 策略 3: 如果提取不足，基于上下文推断
        if len(anchors) < 3:
            # 提取关键名词短语作为假设
            noun_phrases = re.findall(r'([A-Za-z\u4e00-\u9fa5]{2,8})(?:应该 | 必须 | 是 | 优先)', text)
            for np in noun_phrases[:3]:
                anchor = f"{np}是关键因素"
                if anchor not in anchors:
                    anchors.append(anchor)
        
        return anchors[:5]  # 最多返回 5 个
    
    def invert_axiom(self, axiom: str) -> Dict[str, str]:
        """
        第二阶段：公理反转
        对单个锚点执行 NOT 运算，并生成逻辑自洽的竞争方案
        """
        # 生成反转公理
        inversion_map = {
            "总是好的": "并非总是好的，有时是有害的",
            "是目标": "不是目标，只是手段",
            "优于": "并不优于，在特定情境下更差",
            "应该": "不应该，反而应该反向操作",
            "优先于": "不应优先，反而应该后置于",
            "是关键因素": "不是关键因素，可以被忽略"
        }
        
        counter_axiom = axiom
        for original, inverted in inversion_map.items():
            if original in axiom:
                counter_axiom = axiom.replace(original, inverted)
                break
        
        # 生成逻辑推导
        logic_deduction = self._generate_logic_deduction(counter_axiom)
        
        # 生成综合冲突
        synthetic_conflict = self._generate_synthetic_conflict(axiom, counter_axiom, logic_deduction)
        
        return {
            "Counter_Axiom": counter_axiom,
            "Logic_Deduction": logic_deduction,
            "Synthetic_Conflict": synthetic_conflict
        }
    
    def _generate_logic_deduction(self, counter_axiom: str) -> str:
        """生成逻辑推导链"""
        # 基于反转公理，构建 3 步推导链
        templates = [
            "{axiom}→在特定场景下成立→可能产生意外效果→需要重新评估原方案",
            "{axiom}→这意味着原假设不总是成立→存在反例→原方案的基础被动摇",
            "{axiom}→从这个角度看→原方案可能不是最优→甚至可能是次优选择",
            "{axiom}→历史上有类似案例→结果往往出乎意料→值得深入思考"
        ]
        
        import random
        template = random.choice(templates)
        return template.format(axiom=counter_axiom)
    
    def _generate_synthetic_conflict(self, original: str, counter: str, deduction: str) -> str:
        """生成综合冲突说明"""
        conflicts = [
            f"你的原方案基于'{original}'，但'{counter}'。{deduction}",
            f"如果'{counter}'成立，那么你的整个方案基础都需要重新审视。",
            f"这个反转揭示了你方案中的潜在盲点：{original}可能不是公理，而是假设。",
            f"考虑'{counter}'的视角，你的方案可能错过了更重要的机会或风险。"
        ]
        
        import random
        return random.choice(conflicts)
    
    def generate_meta_probes(self, original_text: str, anchors: List[str]) -> List[str]:
        """
        第三阶段：元坐标追问
        生成 2 个探测脉冲
        """
        probes = []
        
        # 维度 1: 动机审计
        motivation_probes = [
            "这个方案是为了解决实际问题，还是为了缓解你对'不可控'的恐惧？",
            "你选择这个方向，是因为它真的最优，还是因为它最符合你现有的认知框架？",
            "如果这个方案失败，你损失的是实际利益，还是只是'面子'？",
            "你是在解决问题，还是在证明自己是对的？"
        ]
        
        # 维度 2: 边界压力
        boundary_probes = [
            "如果关键资源（算力/资金/人力）突然减少 90%，这个方案如何从'药'变成'毒'？",
            "如果环境参数发生极值变化（如成本下降 100 倍或上升 100 倍），你的方案还成立吗？",
            "当系统规模扩大 10 倍时，你方案中的哪些'优势'会变成'劣势'？",
            "如果时间压缩到 1/10 或延长到 10 倍，你的方案哪些部分会崩溃？"
        ]
        
        import random
        probes.append(random.choice(motivation_probes))
        probes.append(random.choice(boundary_probes))
        
        return probes
    
    def reflect(self, user_input: str) -> Dict[str, Any]:
        """
        完整反射流程
        """
        # 阶段 1: 特征提取
        anchors = self.extract_anchors(user_input)
        
        # 阶段 2: 公理反转（选择最强的一个锚点）
        if anchors:
            strongest_axiom = anchors[0]  # 选择第一个作为主要反转对象
            inversion_model = self.invert_axiom(strongest_axiom)
        else:
            inversion_model = {
                "Counter_Axiom": "你的所有假设都可能是错的",
                "Logic_Deduction": "没有明确假设→无法反转→这本身就是一个问题",
                "Synthetic_Conflict": "你的方案缺乏明确的基础假设，这比假设错误更危险"
            }
        
        # 阶段 3: 元坐标追问
        meta_probes = self.generate_meta_probes(user_input, anchors)
        
        # 构建输出
        result = {
            "Original_Anchors": anchors,
            "Inversion_Model": inversion_model,
            "Meta_Probes": meta_probes,
            "System_Lock": "WAIT_FOR_HUMAN_JUDGEMENT"
        }
        
        return result
    
    def reflect_json(self, user_input: str) -> str:
        """
        以 JSON 格式输出反射结果
        """
        result = self.reflect(user_input)
        return json.dumps(result, ensure_ascii=False, indent=2)


# 快捷函数
def reflect(user_input: str) -> Dict[str, Any]:
    """快捷反射函数"""
    reflector = LogicInversionReflector()
    return reflector.reflect(user_input)


def reflect_json(user_input: str) -> str:
    """快捷 JSON 反射函数"""
    reflector = LogicInversionReflector()
    return reflector.reflect_json(user_input)


# CLI 入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("请输入你的方案/想法：")
    
    result = reflect(user_input)
    print(json.dumps(result, ensure_ascii=False, indent=2))
