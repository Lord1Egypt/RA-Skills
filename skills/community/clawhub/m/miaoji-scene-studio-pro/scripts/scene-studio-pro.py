#!/usr/bin/env python3
"""
场景工作室Pro版 - Level 2
Scene Studio Pro

基于免费版场景提示词，增加：
- brand-score: 品牌一致性评分
- cross-platform: 跨平台适配(Amazon/Shopify/独立站)
- ab-plan: A/B测试方案

Author: Miaoji Studio Pro
Version: 1.0.0
"""

import sys
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class ScenePrompt:
    """场景提示词"""
    scene_type: str
    prompt: str
    composition: str
    style: str
    keywords: List[str]


@dataclass
class BrandScore:
    """品牌评分"""
    overall_score: float
    consistency: float
    visual_identity: float
    messaging: float
    gaps: List[str]
    recommendations: List[str]


@dataclass
class PlatformAdaptation:
    """平台适配"""
    platform: str
    dimensions: Dict[str, int]  # 宽x高
    aspect_ratio: str
    key_requirements: List[str]
    adapted_prompt: str


class SceneStudioPro:
    """场景工作室Pro版"""
    
    # 平台规格
    PLATFORM_SPECS = {
        "Amazon": {
            "main_image": {"width": 3000, "height": 3000, "ratio": "1:1"},
            "lifestyle": {"width": 2560, "height": 1440, "ratio": "16:9"},
            "infographic": {"width": 2000, "height": 1500, "ratio": "4:3"}
        },
        "Shopify": {
            "hero": {"width": 1920, "height": 1080, "ratio": "16:9"},
            "product": {"width": 2048, "height": 2048, "ratio": "1:1"},
            "banner": {"width": 1200, "height": 600, "ratio": "2:1"}
        },
        "独立站": {
            "hero": {"width": 2560, "height": 1440, "ratio": "16:9"},
            "product_detail": {"width": 1600, "height": 2000, "ratio": "4:5"},
            "banner": {"width": 1920, "height": 800, "ratio": "12:5"}
        }
    }
    
    # 风格定义
    STYLES = {
        "现代简约": ["clean", "minimal", "white space", "simple"],
        "自然生活": ["lifestyle", "cozy", "warm light", "natural"],
        "科技感": ["sleek", "modern", "high-tech", "futuristic"],
        "轻奢优雅": ["elegant", "luxury", "premium", "sophisticated"]
    }
    
    def __init__(self):
        self.generated_prompts: List[ScenePrompt] = []
    
    def generate_scene_prompt(self, product_type: str, scene_type: str,
                             style: str = "现代简约") -> ScenePrompt:
        """
        生成场景提示词
        
        Args:
            product_type: 产品类型
            scene_type: 场景类型
            style: 风格
        
        Returns:
            场景提示词
        """
        # 基础提示词模板
        base_templates = {
            "产品展示": "{style} {product} on {background}, studio lighting, professional photography",
            "使用场景": "{model} using {product} in {setting}, natural lighting, lifestyle photography",
            "细节特写": "close-up of {product} {feature}, macro lens, sharp focus, {style}",
            "对比展示": "{product} vs competitors, same setting, professional comparison",
            "品牌故事": "{product} in {brand_environment}, brand narrative, emotional connection"
        }
        
        style_keywords = self.STYLES.get(style, self.STYLES["现代简约"])
        
        prompt = base_templates.get(scene_type, base_templates["产品展示"]).format(
            style=" ".join(style_keywords),
            product=product_type,
            background="clean white background",
            model="Asian female model",
            setting="modern living room",
            feature="premium details",
            brand_environment="luxury boutique"
        )
        
        composition = self._get_composition(scene_type)
        
        scene = ScenePrompt(
            scene_type=scene_type,
            prompt=prompt,
            composition=composition,
            style=style,
            keywords=[product_type, style, scene_type]
        )
        
        self.generated_prompts.append(scene)
        return scene
    
    def _get_composition(self, scene_type: str) -> str:
        """获取构图建议"""
        compositions = {
            "产品展示": "居中构图，产品占画面60%，上方留白20%",
            "使用场景": "三分法，模特占右侧1/3，产品为视觉焦点",
            "细节特写": "中心特写，细节占画面80%",
            "对比展示": "左右分栏，同等占比",
            "品牌故事": "故事性构图，引导视线流向"
        }
        return compositions.get(scene_type, "居中构图")
    
    def evaluate_brand_consistency(self, brand_guidelines: Dict,
                                   assets: List[Dict]) -> BrandScore:
        """
        评估品牌一致性
        
        Args:
            brand_guidelines: 品牌规范
            assets: 素材列表
        
        Returns:
            品牌评分
        """
        # 模拟评分
        consistency = 75
        visual_identity = 80
        messaging = 70
        
        # 根据品牌规范调整
        if brand_guidelines.get("strict_colors"):
            visual_identity += 10
        
        if brand_guidelines.get("unified_style"):
            consistency += 10
        
        # 计算综合分
        overall = (consistency + visual_identity + messaging) / 3
        
        gaps = []
        recommendations = []
        
        if consistency < 80:
            gaps.append("场景风格不够统一")
            recommendations.append("建立标准化的场景风格指南")
        
        if visual_identity < 80:
            gaps.append("视觉识别度有待提升")
            recommendations.append("统一色彩和元素使用")
        
        if messaging < 80:
            gaps.append("品牌调性表达不一致")
            recommendations.append("制定统一的品牌话术规范")
        
        return BrandScore(
            overall_score=round(overall, 1),
            consistency=round(consistency, 1),
            visual_identity=round(visual_identity, 1),
            messaging=round(messaging, 1),
            gaps=gaps,
            recommendations=recommendations
        )
    
    def adapt_cross_platform(self, base_prompt: ScenePrompt,
                            target_platforms: List[str]) -> List[PlatformAdaptation]:
        """
        跨平台适配
        
        Args:
            base_prompt: 基础提示词
            target_platforms: 目标平台列表
        
        Returns:
            平台适配列表
        """
        adaptations = []
        
        for platform in target_platforms:
            specs = self.PLATFORM_SPECS.get(platform, {})
            
            # 根据平台调整提示词
            adapted_prompt = base_prompt.prompt
            
            if platform == "Amazon":
                adapted_prompt = f"high resolution, {adapted_prompt}, clean background preferred"
            elif platform == "Shopify":
                adapted_prompt = f"web optimized, {adapted_prompt}, lifestyle focus"
            elif platform == "独立站":
                adapted_prompt = f"premium quality, {adapted_prompt}, emotional appeal"
            
            adaptations.append(PlatformAdaptation(
                platform=platform,
                dimensions=specs.get("lifestyle", {"width": 1920, "height": 1080}),
                aspect_ratio=specs.get("lifestyle", {}).get("ratio", "16:9"),
                key_requirements=self._get_platform_requirements(platform),
                adapted_prompt=adapted_prompt
            ))
        
        return adaptations
    
    def _get_platform_requirements(self, platform: str) -> List[str]:
        """获取平台要求"""
        requirements = {
            "Amazon": [
                "白底主图(3000x3000)",
                "避免水印和文字",
                "图片清晰度300dpi",
                "支持缩放"
            ],
            "Shopify": [
                "Web优化格式",
                "加载速度快",
                "支持Retina",
                "响应式裁剪"
            ],
            "独立站": [
                "高质量视觉",
                "品牌调性一致",
                "适合多种设备",
                "支持Lazy Load"
            ]
        }
        return requirements.get(platform, [])
    
    def generate_ab_plan(self, product_type: str,
                         test_variables: List[str] = None) -> Dict:
        """
        生成A/B测试方案
        
        Args:
            product_type: 产品类型
            test_variables: 测试变量
        
        Returns:
            A/B测试方案
        """
        if test_variables is None:
            test_variables = ["场景类型", "模特风格", "色调"]
        
        tests = []
        
        # 场景类型测试
        if "场景类型" in test_variables:
            tests.append({
                "test_id": "SCENE-001",
                "variable": "场景类型",
                "variants": [
                    {"name": "A", "description": "室内白底棚拍", "hypothesis": "简洁专业感更强"},
                    {"name": "B", "description": "生活场景展示", "hypothesis": "代入感更强促进转化"},
                    {"name": "C", "description": "室外自然光", "hypothesis": "自然真实提升信任"}
                ],
                "metrics": ["CTR", "CVR", "停留时间"],
                "duration": "2周",
                "min_sample_size": 1000
            })
        
        # 模特风格测试
        if "模特风格" in test_variables:
            tests.append({
                "test_id": "MODEL-001",
                "variable": "模特风格",
                "variants": [
                    {"name": "A", "description": "专业模特", "hypothesis": "高端感强"},
                    {"name": "B", "description": "素人模特", "hypothesis": "真实感强"}
                ],
                "metrics": ["CVR", "评论提及率"],
                "duration": "2周",
                "min_sample_size": 800
            })
        
        # 色调测试
        if "色调" in test_variables:
            tests.append({
                "test_id": "COLOR-001",
                "variable": "主色调",
                "variants": [
                    {"name": "A", "description": "暖色调", "hypothesis": "温馨感促进购买"},
                    {"name": "B", "description": "冷色调", "hypothesis": "专业感强"},
                    {"name": "C", "description": "中性色", "hypothesis": "百搭接受度高"}
                ],
                "metrics": ["CTR", "加购率"],
                "duration": "3周",
                "min_sample_size": 1500
            })
        
        return {
            "product_type": product_type,
            "total_tests": len(tests),
            "tests": tests,
            "recommendations": [
                "建议分批次进行测试，避免同时测试过多变量",
                "每个测试需达到最小样本量再下结论",
                "测试期间保持其他变量不变",
                "记录测试结果形成知识库"
            ]
        }


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python scene-studio-pro.py <command> [args]")
        print("命令:")
        print("  brand-score      - 品牌一致性评分")
        print("  cross-platform    - 跨平台适配")
        print("  ab-plan           - A/B测试方案")
        return
    
    command = sys.argv[1]
    studio = SceneStudioPro()
    
    if command == "brand-score":
        guidelines = {
            "strict_colors": True,
            "unified_style": False,
            "brand_voice": "premium"
        }
        
        assets = [
            {"type": "main_image", "score": 85},
            {"type": "lifestyle", "score": 70},
            {"type": "infographic", "score": 75}
        ]
        
        score = studio.evaluate_brand_consistency(guidelines, assets)
        
        print("=" * 60)
        print("品牌一致性评分")
        print("=" * 60)
        
        print(f"\n综合评分: {score.overall_score}分")
        print(f"  一致性: {score.consistency}分")
        print(f"  视觉识别: {score.visual_identity}分")
        print(f"  品牌调性: {score.messaging}分")
        
        if score.gaps:
            print("\n发现差距:")
            for gap in score.gaps:
                print(f"  • {gap}")
        
        if score.recommendations:
            print("\n建议:")
            for rec in score.recommendations:
                print(f"  → {rec}")
    
    elif command == "cross-platform":
        base = studio.generate_scene_prompt("wireless earbuds", "使用场景", "自然生活")
        
        adaptations = studio.adapt_cross_platform(base, ["Amazon", "Shopify", "独立站"])
        
        print("=" * 60)
        print("跨平台适配方案")
        print("=" * 60)
        
        for ad in adaptations:
            print(f"\n📱 {ad.platform}")
            print(f"   尺寸: {ad.dimensions['width']}x{ad.dimensions['height']} ({ad.aspect_ratio})")
            print(f"   提示词: {ad.adapted_prompt[:60]}...")
            print(f"   要求:")
            for req in ad.key_requirements[:2]:
                print(f"     • {req}")
    
    elif command == "ab-plan":
        plan = studio.generate_ab_plan("wireless earbuds")
        
        print("=" * 60)
        print("A/B测试方案")
        print("=" * 60)
        
        print(f"\n产品类型: {plan['product_type']}")
        print(f"测试总数: {plan['total_tests']}\n")
        
        for test in plan["tests"]:
            print(f"📊 {test['test_id']}: {test['variable']}")
            print(f"   时长: {test['duration']} | 最小样本: {test['min_sample_size']}")
            print(f"   指标: {', '.join(test['metrics'])}")
            print(f"   变体:")
            for v in test["variants"]:
                print(f"     [{v['name']}] {v['description']}")
                print(f"         假设: {v['hypothesis']}")
    
    else:
        print(f"未知命令: {command}")


if __name__ == "__main__":
    main()
