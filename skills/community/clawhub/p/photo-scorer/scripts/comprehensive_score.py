#!/usr/bin/env python3
"""
Comprehensive Aesthetic Scorer - Unified Scoring Script
Combines Improved Predictor and NIMA scores with DYNAMIC WEIGHT based on NIMA's standard deviation.
Base weights: IAP 45%, NIMA 55% (adjustable: IAP 45%-70%, NIMA 30%-55%)
All processing is performed locally - no external API calls
"""

import json
import argparse
import sys
from pathlib import Path

# Import two scoring modules
try:
    from score_improved_predictor import predict_aesthetic
except ImportError:
    print("Warning: score_improved_predictor module not found")
    predict_aesthetic = None

try:
    from score_nima import predict_with_nima
except ImportError:
    print("Warning: score_nima module not found")
    predict_with_nima = None


def calculate_weighted_score(scores):
    """
    Calculate weighted average with DYNAMIC WEIGHT based on NIMA's standard deviation.
    
    Dynamic Weight Logic:
    - NIMA std (standard deviation) indicates consensus level
    - High std = controversial = more weight to IAP (content-based)
    - Low std = consensus = use balanced weights
    
    Formula:
    - Base weights: IAP 45%, NIMA 55%
    - Dynamic adjustment: IAP weight increases with NIMA std
    - Penalty: When IAP and NIMA differ greatly, apply small penalty
    
    Final Formula:
    weighted_score = weight_iap * IAP + weight_nima * NIMA - penalty
    where:
      weight_iap = 0.45 + (normalized_std * 0.25), capped at [0.45, 0.70]
      weight_nima = 1 - weight_iap
      penalty = 0.05 * |IAP - NIMA| (only when diff >= 2.0)
    """
    valid_scores = {k: v for k, v in scores.items() if v is not None}
    
    if not valid_scores:
        return None, "All scoring failed"
    
    # Extract scores
    iap_score = valid_scores.get('improved')
    nima_score = valid_scores.get('nima')
    nima_std = valid_scores.get('nima_std', 1.5)  # default if not available
    
    # Handle single source case
    if iap_score is None:
        return {
            'weighted_score': nima_score,
            'source_count': 1,
            'weight_iap': 0,
            'weight_nima': 1.0,
            'penalty': 0,
            'method': 'nima_only'
        }, None
    
    if nima_score is None:
        return {
            'weighted_score': iap_score,
            'source_count': 1,
            'weight_iap': 1.0,
            'weight_nima': 0,
            'penalty': 0,
            'method': 'iap_only'
        }, None
    
    # Dynamic weight calculation
    # Normalize NIMA std (empirical range: 0-2.5)
    normalized_std = min(nima_std / 2.5, 1.0)
    
    # IAP weight increases with controversy (std)
    # Range: 0.45 (consensus) to 0.70 (highly controversial)
    weight_iap = 0.45 + normalized_std * 0.25
    weight_nima = 1.0 - weight_iap
    
    # Calculate score difference and penalty
    score_diff = abs(iap_score - nima_score)
    penalty = 0
    if score_diff >= 2.0:
        penalty = 0.05 * score_diff
    
    # Final weighted score
    weighted_score = weight_iap * iap_score + weight_nima * nima_score - penalty
    
    # Ensure score stays in valid range [0, 10]
    weighted_score = max(0, min(10, weighted_score))
    
    return {
        'weighted_score': weighted_score,
        'source_count': len(valid_scores),
        'weight_iap': weight_iap,
        'weight_nima': weight_nima,
        'penalty': penalty,
        'score_diff': score_diff,
        'nima_std': nima_std,
        'normalized_std': normalized_std,
        'method': 'dynamic_weight'
    }, None


def get_score_level(score):
    """Get '从夯到拉' score level"""
    if score >= 9.0:
        return "夯", "exceptional"
    elif score >= 8.0:
        return "顶级", "excellent"
    elif score >= 7.0:
        return "人上人", "very_good"
    elif score >= 6.0:
        return "NPC", "average"
    else:
        return "拉完了", "poor"


def analyze_image(image_path, api_key=None):
    """
    Perform comprehensive aesthetic analysis and return unified report
    All processing is done locally - no external API calls or data transmission

    Args:
        image_path: Path to image file (local file only)
        api_key: Deprecated parameter (kept for backward compatibility, not used)

    Returns:
        dict with unified analysis results
    """
    results = {}
    sources_failed = []
    nima_std = 1.5  # default
    
    print("正在执行综合美学分析...", end=" ")
    
    # 1. Improved Aesthetic Predictor (dynamic weight)
    try:
        if predict_aesthetic:
            result = predict_aesthetic(image_path)
            if result:
                results['improved'] = result['score']
    except Exception as e:
        print(f"Warning: Improved Aesthetic Predictor failed: {e}")
        sources_failed.append("Improved Aesthetic Predictor")
    
    # 2. NIMA Model (dynamic weight)
    try:
        if predict_with_nima:
            result = predict_with_nima(image_path)
            if result:
                results['nima'] = result['mean_score']
                nima_std = result.get('std_score', 1.5)
                results['nima_std'] = nima_std
    except Exception as e:
        print(f"Warning: NIMA failed: {e}")
        sources_failed.append("NIMA")
    
    print("完成\n")
    
    # Calculate weighted comprehensive score with dynamic weights
    weighted_result, error = calculate_weighted_score(results)
    
    if error:
        print(f"错误: {error}")
        return None
    
    # Get score level
    level_cn, level_en = get_score_level(weighted_result['weighted_score'])
    
    # Generate unified report
    unified_report = {
        'weighted_score': weighted_result['weighted_score'],
        'level_cn': level_cn,
        'level_en': level_en,
        'source_count': weighted_result['source_count'],
        'sources_failed': sources_failed,
        'method': weighted_result.get('method', 'unknown'),
        'weight_iap': weighted_result.get('weight_iap'),
        'weight_nima': weighted_result.get('weight_nima'),
        'penalty': weighted_result.get('penalty', 0),
        'score_diff': weighted_result.get('score_diff'),
        'nima_std': weighted_result.get('nima_std'),
    }
    
    return unified_report


def generate_report(analysis):
    """Generate unified analysis report"""
    score = analysis['weighted_score']
    level_cn = analysis['level_cn']
    
    report = f"""
## 综合美学分析报告

### 综合评分: {score:.2f}/10 ({level_cn})

### 评分解读
基于两个专业评分模型的综合分析，这张照片的最终评分为 {score:.2f} 分。
"""
    
    # Add interpretation based on score
    if score >= 9.0:
        report += """这是一张达到专业水平的优秀作品。构图、色彩、光线、技术质量各方面都表现出色，几乎无瑕。
适合专业展示、商业用途和摄影比赛。可以作为您的代表作。
"""
    elif score >= 7.5:
        report += """这是一张高质量的作品。美学基础扎实，各方面表现优秀，仅有微小改进空间。
展示了成熟的摄影技巧和良好的审美感知。适合广泛用途和展示。
"""
    elif score >= 6.0:
        report += """这是一张质量良好的照片。具有坚实的美学基础，构图和技术都达到良好水平。
存在一些可以改进的方面，但整体效果令人满意。适合社交媒体分享和个人收藏。
"""
    elif score >= 4.5:
        report += """这张照片达到了一般水平。基本构图和技术执行尚可，但存在明显的改进空间。
需要在构图、光线、色彩或技术质量方面下更多功夫。适合学习和练习。
"""
    elif score >= 3.0:
        report += """这张照片质量低于平均水平。在构图、色彩、光线或技术执行方面存在较明显的问题。
需要大幅改进拍摄技巧和后期处理能力。建议多学习、多练习、多参考优秀作品。
"""
    else:
        report += """这张照片存在严重的美学和技术问题。多个方面需要全面改进。
建议从基础摄影技巧开始学习，逐步提升构图、光线、色彩和曝光控制能力。
"""
    
    report += """

#### 构图评价
综合两个评分模型的分析，这张照片的构图"""
    
    # Dynamic composition analysis based on score
    if score >= 7.5:
        report += """出色。视觉主体突出，元素布局合理，引导线运用得当，层次分明。
构图具有很强的吸引力和专业水准。
"""
    elif score >= 6.0:
        report += """良好。整体构图合理，主体位置适当，视觉平衡感较好。
在某些细节上可以进一步优化，但基础扎实。
"""
    elif score >= 4.5:
        report += """一般。基本构图尚可，但缺乏吸引力和创意。
建议多尝试不同的构图方式，注意黄金分割和视觉引导原则。
"""
    else:
        report += """较弱。构图存在明显问题，如主体不突出、元素杂乱、平衡感缺失等。
建议系统学习摄影构图原理，参考优秀作品的构图方式。
"""
    
    report += """

#### 色彩评价
综合两个评分模型的分析，这张照片的色彩"""
    
    if score >= 7.5:
        report += """非常和谐。色彩搭配恰当，饱和度和色温控制出色，营造了良好的视觉氛围。
色彩的运用增强了照片的美学表现力。
"""
    elif score >= 6.0:
        report += """良好。整体色调协调，色彩搭配基本合理。
在某些情况下可以通过后期处理进一步提升色彩的层次感和冲击力。
"""
    elif score >= 4.5:
        report += """一般。色彩表现平淡或存在一些不协调的地方。
建议学习色彩理论，注意色温、饱和度和对比度的平衡。
"""
    else:
        report += """较弱。色彩运用存在明显问题，如色偏、饱和度过高或过低、色彩杂乱等。
需要深入学习色彩理论和后期调色技巧。
"""
    
    report += """

#### 光线评价
综合两个评分模型的分析，这张照片的光线"""
    
    if score >= 7.5:
        report += """运用出色。光线的方向、质量和强度都控制得当，塑造了良好的立体感和氛围。
曝光准确，高光和阴影细节都得到保留。
"""
    elif score >= 6.0:
        report += """运用良好。整体曝光合理，光线塑造了基本的立体感。
在某些场景下可以通过补光或调整拍摄角度来进一步改善。
"""
    elif score >= 4.5:
        report += """运用一般。曝光控制存在一些问题，如过曝、欠曝或光比过大。
建议学习曝光三要素，掌握不同光线条件下的拍摄技巧。
"""
    else:
        report += """运用较弱。曝光控制存在明显问题，光线运用不当影响整体效果。
需要系统学习曝光原理和光线控制技巧。
"""
    
    report += """

#### 技术质量评价
综合两个评分模型的分析，这张照片的技术质量"""
    
    if score >= 7.5:
        report += """优秀。清晰度高，细节丰富，噪点控制良好，动态范围得当。
技术执行达到专业水平，为美学表现提供了坚实的技术基础。
"""
    elif score >= 6.0:
        report += """良好。整体技术质量令人满意，清晰度和细节都不错。
在某些方面（如噪点、锐化等）还有提升空间。
"""
    elif score >= 4.5:
        report += """一般。基本技术质量尚可，但在清晰度、噪点或细节方面存在不足。
建议使用更稳定的拍摄装备和更优化的拍摄参数。
"""
    else:
        report += """较差。技术质量存在明显问题，如模糊、噪点严重、细节丢失等。
需要改进拍摄设备和技术，确保基础技术质量达标。
"""
    
    report += """
### 改进建议

#### 拍摄技巧
"""
    
    # Dynamic suggestions based on score
    if score >= 7.5:
        report += """1. 尝试不同季节、不同时间段、不同角度拍摄，发掘更多创意可能
2. 关注细节打磨，在优秀基础上追求完美
3. 尝试将技术达到极限，探索更复杂的拍摄技巧
"""
    elif score >= 6.0:
        report += """1. 多尝试不同的构图方式，如黄金分割、对角线、框架式等
2. 注意光线条件的选择，黄金时段（日出日落）往往效果更佳
3. 掌握曝光三要素（光圈、快门、ISO）的平衡
4. 使用三脚架保证稳定性，特别是在低光条件下
"""
    elif score >= 4.5:
        report += """1. 系统学习摄影构图原理，多参考优秀作品的构图方式
2. 学习色彩理论，理解色温、饱和度、对比度对视觉效果的影响
3. 掌握曝光控制，了解直方图和曝光补偿的使用
4. 练习基础技术，如对焦、稳定性、ISO选择等
"""
    else:
        report += """1. 从基础开始系统学习摄影，包括相机操作和基本原理
2. 多看多学多拍，参考大量优秀摄影作品
3. 掌握最基本的构图、曝光、对焦技巧
4. 建议参加摄影课程或跟随有经验的摄影师学习
"""
    
    report += """#### 后期处理
"""
    
    if score >= 7.5:
        report += """1. 轻微调整即可，保持自然真实
2. 可以尝试不同的调色风格，发掘个人特色
3. 注意细节修饰，但避免过度处理
"""
    elif score >= 6.0:
        report += """1. 适当调整对比度和饱和度，增强视觉冲击力
2. 处理暗部和高光，保留更多细节
3. 适当锐化，但避免过度导致不自然
4. 学习基础调色技巧，提升整体质感
"""
    elif score >= 4.5:
        report += """1. 学习基础后期处理流程，如Lightroom或Photoshop
2. 掌握曝光、对比度、色温、饱和度等基本调整
3. 学习局部调整工具，针对性地改善问题区域
4. 参考优秀作品的后期风格，但不要过度模仿
"""
    else:
        report += """1. 从基础后期处理开始学习，不要急于求成
2. 掌握最基本的曝光、对比度、色温调整
3. 多看多学多练，参考大量优秀后期作品
4. 建议：前期拍好比后期修好更重要
"""
    
    report += """#### 构图优化
"""
    
    if score >= 7.5:
        report += """1. 尝试更多创意构图方式，突破常规
2. 考虑加入前景、中景、远景，增强层次感
3. 注意留白和视觉平衡的细微调整
"""
    elif score >= 6.0:
        report += """1. 多尝试黄金分割、三分法等经典构图
2. 注意视觉引导线的运用，引导观众视线
3. 考虑框架式构图，突出主体
4. 寻找有趣的视角和角度
"""
    elif score >= 4.5:
        report += """1. 学习并应用基本构图原则：黄金分割、三分法、对称等
2. 注意画面的简洁性，避免杂乱的元素
3. 确保主体突出，避免背景干扰
4. 多从不同角度和高度观察拍摄对象
"""
    else:
        report += """1. 首先保证画面简洁，去除干扰元素
2. 确保主体清晰可见，位置适当
3. 学习构图的基本原则，如平衡、对比、节奏等
4. 多参考和学习优秀摄影作品的构图方式
"""
    
    report += f"""
### 总体评价
这张照片的最终综合评分为 {score:.2f} 分，属于{level_cn}水平。
"""
    
    # Add specific overall evaluation
    if score >= 8.5:
        report += """这是一张非常出色的作品，两个专业评分模型都给予了高度评价。
构图、色彩、光线、技术质量各方面都达到了优秀水平，具有专业水准。
可以作为您的代表作，适合专业展示、商业用途和摄影比赛。
继续发挥这种高水平，在创意和细节上追求完美，您会创作出更多优秀作品！
"""
    elif score >= 7.0:
        report += """这是一张质量很高的作品，展示了扎实的摄影技巧和良好的审美。
两个专业评分模型总体认可这张照片的质量，虽然存在一些改进空间，但整体效果令人满意。
建议在保持现有水平的基础上，在细节和创意上进一步提升，您会达到更高的专业水准。
"""
    elif score >= 5.5:
        report += """这是一张质量良好的照片，具有坚实的美学基础。
构图和技术都达到良好水平，但在某些方面还有提升空间。
建议多学习多练习，针对具体问题进行改进，您会逐步提升到更高的水平。
"""
    elif score >= 4.0:
        report += """这张照片达到一般水平，基本要求满足但存在明显改进空间。
在构图、色彩、光线或技术质量的一个或多个方面需要下功夫。
建议系统学习摄影基础知识，多参考优秀作品，多拍多练，不断提升。
"""
    else:
        report += """这张照片存在较多需要改进的方面，建议从基础开始系统学习。
摄影是一门需要不断学习和练习的艺术，保持耐心和热情，逐步提升您的技能。
多看多学多拍，参考优秀作品，您一定会不断进步！
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Unified comprehensive aesthetic analysis')
    parser.add_argument('image_path', type=str, help='Path to image file')
    parser.add_argument('--api-key', type=str, default=None, help='(Deprecated) API key parameter - kept for backward compatibility, not used')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Validate image exists
    if not Path(args.image_path).exists():
        print(f"错误: 图片文件未找到: {args.image_path}")
        sys.exit(1)
    
    # Perform comprehensive analysis
    analysis = analyze_image(args.image_path, args.api_key)
    
    if analysis is None:
        sys.exit(1)
    
    # Generate and display unified report
    if args.json:
        print(json.dumps(analysis, indent=2))
    else:
        report = generate_report(analysis)
        print(report)
    
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
