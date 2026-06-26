#!/usr/bin/env python3
"""
IChing Divination Engine - 易经占卜引擎
确定性卦象生成 + AI智能解读
"""
import os
import json
import random
import hashlib
from datetime import datetime
from typing import Dict, Optional

# API配置
MINIMAX_KEY = os.environ.get('MINIMAX_KEY', 'sk-y9avgZsHEoTQ9be4jBVvmaEjWAvmJgfAs7ZCJ1lMRUrMNqvr')
MINIMAX_URL = "https://api.sfkey.cn/v1/chat/completions"


class Bagua:
    """八卦定义"""
    NAMES = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
    MEANINGS = {
        "乾": "天，刚健，自强不息",
        "坤": "地，柔顺，厚德载物",
        "震": "雷，震动，把握时机",
        "巽": "风，渗入，顺从谦逊",
        "坎": "水，陷险，危机意识",
        "离": "火，光明，智慧照临",
        "艮": "山，停止，稳健守成",
        "兑": "泽，喜悦，人际和谐"
    }


class HexagramDatabase:
    """六十四卦数据库"""
    
    # 六十四卦完整表 (简化版)
    HEXAGRAMS = {
        # 乾宫
        ("乾", "乾"): {"name": "乾为天", "guaci": "元亨利贞", "meaning": "大吉大利，诸事顺遂"},
        ("乾", "兑"): {"name": "天泽履", "guaci": "履虎尾，不咥人，亨", "meaning": "小心翼翼终获成功"},
        ("乾", "离"): {"name": "天火同人", "guaci": "同人于野，亨", "meaning": "贵人相助，广结善缘"},
        ("乾", "震"): {"name": "天雷无妄", "guaci": "无妄，元亨利贞", "meaning": "顺势而行必有收获"},
        ("乾", "巽"): {"name": "天风姤", "guaci": "姤，遇也，天下有风", "meaning": "意外相遇需要谨慎"},
        ("乾", "坎"): {"name": "天水讼", "guaci": "讼，有孚，窒惕", "meaning": "争执诉讼不吉"},
        ("乾", "艮"): {"name": "天山遁", "guaci": "遁，亨，小利贞", "meaning": "退避三舍以待时机"},
        ("乾", "坤"): {"name": "天地否", "guaci": "否之匪人，不利君子贞", "meaning": "闭塞不通需要改变"},
        
        # 坤宫
        ("坤", "乾"): {"name": "地天泰", "guaci": "泰，小往大来，吉亨", "meaning": "阴阳和畅万事通"},
        ("坤", "兑"): {"name": "地泽临", "guaci": "临，元亨利贞", "meaning": "居高临下指导有方"},
        ("坤", "离"): {"name": "地火明夷", "guaci": "明夷，利艰贞", "meaning": "韬光养晦等待时机"},
        ("坤", "震"): {"name": "地雷复", "guaci": "复，亨，出入无疾", "meaning": "恢复元气重新开始"},
        ("坤", "巽"): {"name": "地风升", "guaci": "升，亨，用见大人", "meaning": "稳步上升发展良好"},
        ("坤", "坎"): {"name": "地水师", "guaci": "师，贞，丈人吉", "meaning": "领导有方聚力成事"},
        ("坤", "艮"): {"name": "地山谦", "guaci": "谦，亨，君子有终", "meaning": "低调谦逊必有厚福"},
        ("坤", "坤"): {"name": "坤为地", "guaci": "元亨，利牝马之贞", "meaning": "柔顺中正承载万物"},
        
        # 常用卦 - 简化映射
        ("离", "离"): {"name": "离为火", "guaci": "明两作，离。大人以继明照于四方", "meaning": "光明照耀积极进取"},
        ("兑", "兑"): {"name": "兑为泽", "guaci": "兑亨利贞", "meaning": "和悦待人好事成双"},
        ("巽", "巽"): {"name": "巽为风", "guaci": "巽，小亨，利有攸往", "meaning": "顺势而为灵活变通"},
        ("坎", "坎"): {"name": "坎为水", "guaci": "习坎，有孚，维心亨", "meaning": "度过艰难险阻可得"},
        ("震", "震"): {"name": "震为雷", "guaci": "震亨，震来虩虩", "meaning": "行动果断把握机会"},
        ("艮", "艮"): {"name": "艮为山", "guaci": "艮其背，不获其身", "meaning": "适时停止避免过激"},
    }
    
    # 默认卦辞
    DEFAULT_GUACI = "卦辞待查，请咨询专业人士"
    
    @classmethod
    def get(cls, lower: str, upper: str) -> Dict:
        """获取卦象信息"""
        key = (lower, upper)
        if key in cls.HEXAGRAMS:
            return cls.HEXAGRAMS[key]
        # 如果没有精确匹配，生成一个
        return {
            "name": f"{lower}{upper}",
            "guaci": cls.DEFAULT_GUACI,
            "meaning": "此卦需要专业解读"
        }


class IChingDivination:
    """易经占卜引擎"""
    
    def __init__(self):
        self.bagua = Bagua()
        self.hexagrams = HexagramDatabase()
    
    def generate_hexagram(self, question: str, seed: Optional[int] = None) -> Dict:
        """
        生成六爻卦象
        
        Args:
            question: 用户问题
            seed: 可选的随机种子
            
        Returns:
            包含卦象信息的字典
        """
        # 使用问题生成确定性种子
        if seed is None:
            seed = int(hashlib.md5(question.encode()).hexdigest()[:8], 16)
        
        random.seed(seed)
        
        # 生成6爻
        lines = []
        for _ in range(6):
            # 50%概率阴阳
            lines.append(random.choice([0, 1]))
        
        # 组成卦象
        lower_idx = sum(lines[:3]) % 8
        upper_idx = sum(lines[3:6]) % 8
        
        lower = self.bagua.NAMES[lower_idx]
        upper = self.bagua.NAMES[upper_idx]
        
        # 获取卦辞
        hexagram_info = self.hexagrams.get(lower, upper)
        
        return {
            "question": question,
            "lower": lower,
            "upper": upper,
            "hexagram": lower + upper,
            "name": hexagram_info["name"],
            "guaci": hexagram_info["guaci"],
            "meaning": hexagram_info["meaning"],
            "lines": ["阳" if l == 1 else "阴" for l in lines],
            "line_details": lines,
            "timestamp": datetime.now().isoformat()
        }
    
    def interpret(self, hexagram_data: Dict) -> Dict:
        """
        AI解读卦象
        
        Args:
            hexagram_data: generate_hexagram返回的数据
            
        Returns:
            添加了AI解读的完整数据
        """
        prompt = self._build_interpretation_prompt(hexagram_data)
        interpretation = self._call_ai(prompt)
        
        return {
            **hexagram_data,
            "interpretation": interpretation,
            "interpreted_at": datetime.now().isoformat()
        }
    
    def _build_interpretation_prompt(self, data: Dict) -> str:
        """构建AI解读提示词"""
        return f"""你是易经大师，用简洁温暖的语言解读卦象。

【用户问题】
{data['question']}

【卦象】
卦名: {data['name']}（{data['hexagram']}）
下卦: {data['lower']} - {Bagua.MEANINGS.get(data['lower'], '')}
上卦: {data['upper']} - {Bagua.MEANINGS.get(data['upper'], '')}
六爻: {' '.join(data['lines'])}
卦辞: {data['guaci']}

请写一段150-200字的解读，包含：
1. 卦象基本含义（一句话概括）
2. 对用户问题的直接回答
3. 具体行动建议（2-3条）

风格要求：
- 像朋友聊天，有温度
- 不迷信，强调主观能动性
- 具体可行，不说空话
- 适度鼓励，不过度乐观

用中文回答。"""
    
    def _call_ai(self, prompt: str) -> str:
        """调用MiniMax AI"""
        import urllib.request
        
        data = {
            "model": "MiniMax-M2.7-highspeed",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800
        }
        
        req = urllib.request.Request(
            MINIMAX_URL,
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {MINIMAX_KEY}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"AI解读暂时不可用，请稍后再试。"


def divine(question: str, use_ai: bool = True) -> Dict:
    """
    简洁的占卜接口
    
    Args:
        question: 用户问题
        use_ai: 是否使用AI解读（如果API不可用可设为False）
        
    Returns:
        完整的占卜结果
    """
    engine = IChingDivination()
    
    # 生成卦象
    hexagram = engine.generate_hexagram(question)
    
    # AI解读
    if use_ai:
        result = engine.interpret(hexagram)
    else:
        result = {
            **hexagram,
            "interpretation": "（AI解读已禁用）"
        }
    
    return result


def format_result(result: Dict) -> str:
    """格式化占卜结果为可读文本"""
    output = []
    output.append(f"\n📿 得卦：{result['name']}卦")
    output.append(f"📜 卦辞：{result['guaci']}")
    output.append(f"💡 意象：{result['meaning']}")
    output.append(f"   六爻：{' '.join(result['lines'])}")
    
    if 'interpretation' in result:
        output.append(f"\n🔮 大师解读：")
        output.append(result['interpretation'])
    
    return '\n'.join(output)


# CLI测试
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        question = ' '.join(sys.argv[1:])
    else:
        question = input("请输入您的问题：")
    
    print("🔮 AI占卜大师")
    print("=" * 50)
    
    result = divine(question)
    print(format_result(result))
