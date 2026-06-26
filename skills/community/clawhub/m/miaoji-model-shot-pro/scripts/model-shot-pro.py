#!/usr/bin/env python3
"""
模特拍摄Pro版 - Level 2
Model Shot Pro

基于免费版模特提示词，增加：
- combo: 模特类型×场景×风格3维组合生成
- brand-match: 品牌调性匹配
- batch-export: 批量提示词导出

Author: Miaoji Studio Pro
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from itertools import product


@dataclass
class ModelShot:
    """模特拍摄方案"""
    model_type: str
    scene: str
    style: str
    prompt: str
    composition: str
    camera_angle: str
    lighting: str


@dataclass
class BrandMatch:
    """品牌匹配结果"""
    brand_personality: str
    recommended_model: str
    recommended_scene: str
    recommended_style: str
    match_score: float
    reasoning: List[str]


class ModelShotPro:
    """模特拍摄Pro版"""
    
    # 模特类型
    MODEL_TYPES = {
        "专业模特": {
            "features": ["专业姿态", "精准表情", "完美体态"],
            "best_for": ["高端产品", "时尚服饰", "品牌形象"]
        },
        "素人模特": {
            "features": ["真实自然", "亲和力强", "代入感好"],
            "best_for": ["日常服饰", "大众消费品", "口碑营销"]
        },
        "虚拟模特": {
            "features": ["可定制性高", "成本可控", "风格统一"],
            "best_for": ["标准化产品", "多场景需求", "快速迭代"]
        },
        "局部模特": {
            "features": ["聚焦细节", "突出产品", "想象空间"],
            "best_for": ["配饰", "美妆", "局部特写"]
        }
    }
    
    # 场景类型
    SCENES = {
        "室内棚拍": {
            "setting": "studio",
            "props": "minimal",
            "mood": "professional, clean"
        },
        "家居场景": {
            "setting": "home interior",
            "props": "cozy furniture",
            "mood": "comfortable, warm"
        },
        "户外自然": {
            "setting": "outdoor nature",
            "props": "natural elements",
            "mood": "fresh, natural"
        },
        "都市时尚": {
            "setting": "urban city",
            "props": "modern architecture",
            "mood": "stylish, trendy"
        },
        "专业场景": {
            "setting": "professional environment",
            "props": "office/lab setting",
            "mood": "competent, reliable"
        }
    }
    
    # 风格
    STYLES = {
        "简约高级": {
            "keywords": ["minimalist", "elegant", "high-end", "clean lines"],
            "colors": ["neutral tones", "monochrome"]
        },
        "活力年轻": {
            "keywords": ["vibrant", "energetic", "youthful", "colorful"],
            "colors": ["bright colors", "pastel"]
        },
        "自然清新": {
            "keywords": ["natural", "fresh", "organic", "earth tones"],
            "colors": ["green", "beige", "soft white"]
        },
        "轻奢精致": {
            "keywords": ["luxurious", "sophisticated", "premium", "refined"],
            "colors": ["gold", "black", "deep tones"]
        },
        "运动健康": {
            "keywords": ["athletic", "dynamic", "healthy", "active"],
            "colors": ["sporty colors", "neon"]
        }
    }
    
    def __init__(self):
        self.generated_shots: List[ModelShot] = []
    
    def generate_combo(self, product_type: str, 
                      model_type: str = None,
                      scene: str = None,
                      style: str = None) -> List[ModelShot]:
        """
        生成模特×场景×风格组合
        
        Args:
            product_type: 产品类型
            model_type: 模特类型（可选）
            scene: 场景（可选）
            style: 风格（可选）
        
        Returns:
            拍摄方案列表
        """
        # 如果未指定，使用所有组合
        models = [model_type] if model_type else list(self.MODEL_TYPES.keys())
        scenes = [scene] if scene else list(self.SCENES.keys())
        styles = [style] if style else list(self.STYLES.keys())
        
        shots = []
        
        for m, s, st in product(models, scenes, styles):
            shot = self._create_shot(product_type, m, s, st)
            shots.append(shot)
            self.generated_shots.append(shot)
        
        return shots
    
    def _create_shot(self, product: str, model_type: str, 
                    scene: str, style: str) -> ModelShot:
        """创建单个拍摄方案"""
        model_info = self.MODEL_TYPES.get(model_type, {})
        scene_info = self.SCENES.get(scene, {})
        style_info = self.STYLES.get(style, {})
        
        # 构建提示词
        prompt_parts = []
        prompt_parts.append(f"professional photography of {product}")
        prompt_parts.append(f"featuring {model_type.lower()}")
        prompt_parts.append(f"in {scene_info.get('setting', scene)}")
        prompt_parts.append(f"style: {', '.join(style_info.get('keywords', []))}")
        prompt_parts.append(f"mood: {scene_info.get('mood', 'neutral')}")
        prompt_parts.append("high resolution, sharp focus")
        
        prompt = ", ".join(prompt_parts)
        
        # 构图建议
        composition = self._get_composition(model_type, scene)
        
        # 机位建议
        camera_angle = self._get_camera_angle(model_type)
        
        # 光线建议
        lighting = self._get_lighting(style)
        
        return ModelShot(
            model_type=model_type,
            scene=scene,
            style=style,
            prompt=prompt,
            composition=composition,
            camera_angle=camera_angle,
            lighting=lighting
        )
    
    def _get_composition(self, model_type: str, scene: str) -> str:
        """获取构图建议"""
        if model_type == "局部模特":
            return "特写构图，产品占画面90%"
        
        compositions = {
            "室内棚拍": "居中或三分法，模特占画面60-70%",
            "家居场景": "生活化构图，模特占40-50%留白充足",
            "户外自然": "景大人小或人景融合",
            "都市时尚": "时尚杂志风，模特突出",
            "专业场景": "商务构图，背景简洁"
        }
        return compositions.get(scene, "标准人像构图")
    
    def _get_camera_angle(self, model_type: str) -> str:
        """获取机位建议"""
        angles = {
            "专业模特": "平视或微俯，与视线持平",
            "素人模特": "微俯视，45度角显得更自然",
            "虚拟模特": "根据风格灵活调整",
            "局部模特": "低角度仰拍或高角度俯拍"
        }
        return angles.get(model_type, "平视")
    
    def _get_lighting(self, style: str) -> str:
        """获取光线建议"""
        lights = {
            "简约高级": "柔和侧光，阴影过渡自然",
            "活力年轻": "明亮正面光，高调摄影",
            "自然清新": "自然光为主，窗边光最佳",
            "轻奢精致": "戏剧光，伦勃朗布光",
            "运动健康": "动态光，追焦拍摄"
        }
        return lights.get(style, "标准人像光")
    
    def match_brand(self, brand_personality: str) -> BrandMatch:
        """
        品牌调性匹配
        
        Args:
            brand_personality: 品牌个性描述
        
        Returns:
            匹配结果
        """
        # 分析品牌个性
        brand_lower = brand_personality.lower()
        
        # 匹配模特类型
        if any(kw in brand_lower for kw in ["高端", "奢侈", "专业", "premium"]):
            model = "专业模特"
        elif any(kw in brand_lower for kw in ["亲民", "自然", "真实", "接地气"]):
            model = "素人模特"
        elif any(kw in brand_lower for kw in ["时尚", "年轻", "活力", "潮流"]):
            model = "专业模特"  # 年轻专业模特
        else:
            model = "虚拟模特"
        
        # 匹配场景
        if any(kw in brand_lower for kw in ["家居", "舒适", "温馨", "生活"]):
            scene = "家居场景"
        elif any(kw in brand_lower for kw in ["自然", "有机", "环保", "健康"]):
            scene = "户外自然"
        elif any(kw in brand_lower for kw in ["专业", "商务", "可靠", "科技"]):
            scene = "专业场景"
        else:
            scene = "室内棚拍"
        
        # 匹配风格
        if any(kw in brand_lower for kw in ["简约", "极简", "干净", "清晰"]):
            style = "简约高级"
        elif any(kw in brand_lower for kw in ["活力", "年轻", "快乐", "活力"]):
            style = "活力年轻"
        elif any(kw in brand_lower for kw in ["自然", "有机", "健康"]):
            style = "自然清新"
        elif any(kw in brand_lower for kw in ["奢华", "精致", "优雅"]):
            style = "轻奢精致"
        else:
            style = "简约高级"
        
        # 计算匹配度
        match_score = 85  # 简化计算
        
        return BrandMatch(
            brand_personality=brand_personality,
            recommended_model=model,
            recommended_scene=scene,
            recommended_style=style,
            match_score=match_score,
            reasoning=[
                f"根据品牌调性'{brand_personality}'推荐",
                f"模特类型：{model}",
                f"场景：{scene}",
                f"风格：{style}"
            ]
        )
    
    def batch_export(self, shots: List[ModelShot] = None,
                    format: str = "json") -> str:
        """
        批量导出提示词
        
        Args:
            shots: 拍摄方案列表
            format: 导出格式 (json/csv/text)
        
        Returns:
            导出内容
        """
        if shots is None:
            shots = self.generated_shots
        
        if format == "json":
            return json.dumps([{
                "model_type": s.model_type,
                "scene": s.scene,
                "style": s.style,
                "prompt": s.prompt,
                "composition": s.composition,
                "camera_angle": s.camera_angle,
                "lighting": s.lighting
            } for s in shots], ensure_ascii=False, indent=2)
        
        elif format == "csv":
            lines = ["model_type,scene,style,prompt"]
            for s in shots:
                prompt_escaped = s.prompt.replace('"', '""')
                lines.append(f'"{s.model_type}","{s.scene}","{s.style}","{prompt_escaped}"')
            return "\n".join(lines)
        
        else:  # text
            lines = []
            for i, s in enumerate(shots, 1):
                lines.append(f"=== 方案{i} ===")
                lines.append(f"模特: {s.model_type}")
                lines.append(f"场景: {s.scene}")
                lines.append(f"风格: {s.style}")
                lines.append(f"提示词: {s.prompt}")
                lines.append(f"构图: {s.composition}")
                lines.append(f"机位: {s.camera_angle}")
                lines.append(f"光线: {s.lighting}")
                lines.append("")
            return "\n".join(lines)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python model-shot-pro.py <command> [args]")
        print("命令:")
        print("  combo         - 3维组合生成")
        print("  brand-match   - 品牌调性匹配")
        print("  batch-export  - 批量导出")
        return
    
    command = sys.argv[1]
    studio = ModelShotPro()
    
    if command == "combo":
        # 生成完整组合
        shots = studio.generate_combo("女士连衣裙")
        
        print("=" * 60)
        print("模特×场景×风格组合方案")
        print("=" * 60)
        print(f"\n共生成 {len(shots)} 个方案\n")
        
        for i, shot in enumerate(shots[:5], 1):
            print(f"【方案{i}】")
            print(f"  模特: {shot.model_type}")
            print(f"  场景: {shot.scene}")
            print(f"  风格: {shot.style}")
            print(f"  提示词: {shot.prompt[:80]}...")
            print(f"  构图: {shot.composition}")
            print()
        
        if len(shots) > 5:
            print(f"... 还有 {len(shots)-5} 个方案")
    
    elif command == "brand-match":
        brand = "高端轻奢女装品牌，目标用户为25-35岁都市白领"
        match = studio.match_brand(brand)
        
        print("=" * 60)
        print("品牌调性匹配")
        print("=" * 60)
        
        print(f"\n品牌定位: {match.brand_personality}")
        print(f"\n匹配结果:")
        print(f"  推荐模特: {match.recommended_model}")
        print(f"  推荐场景: {match.recommended_scene}")
        print(f"  推荐风格: {match.recommended_style}")
        print(f"  匹配度: {match.match_score}%")
        
        print("\n匹配理由:")
        for r in match.reasoning:
            print(f"  • {r}")
    
    elif command == "batch-export":
        # 先生成一些方案
        shots = studio.generate_combo("无线耳机", style="简约高级")
        
        # JSON导出
        json_output = studio.batch_export(shots, "json")
        print("JSON导出预览:")
        print(json_output[:500] + "...")
        
        # 文本导出
        print("\n" + "=" * 60)
        print("文本导出预览:")
        print("=" * 60)
        text_output = studio.batch_export(shots[:3], "text")
        print(text_output)
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
