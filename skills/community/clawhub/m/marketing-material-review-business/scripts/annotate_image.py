#!/usr/bin/env python3
"""
营销版面标注图生成脚本（业务版 v1.1.2，2026-08-01 改造）

OCR 策略：
  1) 自动检测时使用百度 OCR 含位置接口
  2) 外部传入的 risks 已带 bbox 时跳过 OCR，直接画框

Features:
1. 百度 OCR 文字定位
2. OpenCV 绘制多边形框（精准对齐）
3. 红/黄/绿三色编码风险等级
4. 自适应排版 v2.0：面板大小根据内容调整
5. 保持原始分辨率输出
6. 完整标注面板（原因 + 修改建议）
7. 双重风险检测路径：
   - 自动 OCR 关键词匹配（使用 HIGH_RISK_WORDS 词库）
   - 外部传入 risks（人工/其他审核结果已给 bbox）

依赖：cv2 (opencv-python) + numpy + Pillow（均为必要）
"""

import sys
import os
import json
import re
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# Risk word lists used by lightweight annotate_image auto-detection.
HIGH_RISK_WORDS = {
    '销量第一': '使用"第一"等绝对化用语,需提供权威数据证明,否则禁止',
    '市场第一': '绝对化用语,禁止使用',
    '全国第一': '绝对化用语,禁止使用',
    '全网第一': '极限词,禁止使用',
    '顶级': '绝对化用语,禁止使用',
    '至尊': '绝对化用语,禁止使用',
    '极致': '绝对化用语,禁止使用',
    '首创': '绝对化用语,需有依据',
    '独家': '需有依据',
    '第一': '绝对化用语,需谨慎',
    '最佳': '绝对化用语,禁止',
    '最优': '绝对化用语,禁止',
    '最好': '绝对化用语,禁止',
    '地板价': '极限促销词,涉嫌虚假宣传',
    '全网最低价': '极限促销词,禁止使用',
    '跌破地板价': '极限促销词,禁止使用',
    '史无前例': '绝对化用语,禁止',
    '前所未有': '绝对化用语,禁止',
    '万灵一': '极限词/封建迷信',
    '万里挑一': '极限词,禁止使用',
    '独一无二': '绝对化用语,禁止',
    '守护肠道': '有保健功能嫌疑,禁止使用',
    '肠道': '保健功能暗示,禁止出现',
    '肠态': '保健功能暗示',
    '润肠': '保健功能宣称,禁止',
    '通便': '保健功能宣称,禁止',
    '增强免疫力': '保健功能宣称,普通食品不得使用',
    '提高免疫力': '保健功能宣称,禁止',
    '增强抵抗力': '保健功能宣称,禁止',
    '养生': '保健功能暗示,禁止',
    '健康': '保健功能暗示,谨慎使用',
    '官方认证': '未注明具体情况,涉嫌虚假宣传',
    '央妈认证': '未获授权,违反广告法',
    '原肉切制': '与"原切"混淆风险,建议改为"原肉腌制"',
    '原切牛排': '需符合 QB/T 5442-2020 标准',
    '原切静腌': '已有打假案例,禁止',
    '宝宝放心吃': '0-36个月有歧义,建议改为"妈妈放心"',
    '根治': '医疗术语,禁止使用',
    '治愈': '医疗术语,禁止使用',
    '无效退款': '虚假宣传,禁止',
    '抽奖有好运': '封建迷信,禁止使用',
    '好运': '封建迷信,谨慎使用',
    '有口皆杯': '成语谐音,禁止使用',
    '骑乐无穷': '成语谐音,禁止使用',
    '咳不容缓': '成语谐音,禁止使用',
    '随心所浴': '成语谐音,禁止使用',
    '0添加': '"无添加"及其同义语,根据内部合规文件不得使用',
    '无添加': '禁止使用"无添加"及其同义语',
    '零添加': '"零添加"属于禁用宣称',
    '不添加': '"不添加"属于禁用宣称',
    '未添加': '"未添加"属于禁用宣称',
    '未使用': '"未使用"属于禁用宣称',
    '没加': '口语化禁用宣称',
    '没用': '口语化禁用宣称',
    '不含': '需含量为0并有检测报告+标准注释',
    '无蔗糖': '需标注"蔗糖含量未检出"及检测依据',
    '0蔗糖': '需标注"蔗糖含量未检出"及检测依据',
    '无乳糖': '需标注乳糖含量≤0.5g/100mL或g,符合GB 28050标准',
    '中国地图': '需确认地图来自标准地图服务系统并标注审图号',
    '地图': '商业广告用地图需审核并标注审图号',
}

MEDIUM_RISK_WORDS = {
    '销量领先': '接近绝对化用语,建议提供数据支持',
    '领先': '需有数据支持',
    '优良': '需有依据',
    '优质': '需有依据',
    '营养丰富': '需体现多样性,避免单一产品使用',
    '全面补充': '需有科学依据',
    '增强': '谨慎使用,避免保健功能暗示',
    '提升': '谨慎使用',
    '好喝': '可使用',
    '美味': '可使用',
    '新鲜': '可使用,需有依据',
    '纯净': '可使用',
    '天然': '需有依据,建议明确说明',
    '有机': '需有认证资质',
    '专利': '需标明专利号和类型',
    '独特': '需有依据',
    '专业': '可使用',
    '热销': '需有数据支持',
    '爆款': '需有数据支持',
    '网红': '需有依据',
    '送礼': '可使用',
    '送礼首选': '可使用',
    '礼品': '可使用',
    '官方': '需注明具体情况',
    '认证': '需有授权',
    '推荐': '需有依据',
    '优选': '需有依据',
    '臻选': '需有依据',
    '标准地图': '需确认来源并标注审图号',
    '审图号': '需验证审图号有效性',
}

COMPLIANT_ALTERNATIVES = {
    '销量第一': '销量领先(注明数据来源)',
    '顶级': '品质卓越 / 匠心品质',
    '地板价': '限时优惠 / 心动价',
    '全网最低价': '会员专享价 / 限时特惠',
    '守护肠道': '好喝美味 / 纯正好奶',
    '增强免疫力': '营养丰富 / 健康成长',
    '官方认证': '品质保证(注明具体认证机构)',
    '宝宝放心吃': '妈妈放心',
    '原肉切制': '原肉腌制 / 原肉加工',
}

FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/Library/Fonts/Arial Unicode.ttf",
]


def load_cjk_font(size):
    for font_path in FONT_CANDIDATES:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                continue
    return ImageFont.load_default()


LEVEL_STYLES = {
    'high': {'label': '高风险', 'bgr': (50, 50, 220), 'rgb': (220, 50, 50)},
    'medium': {'label': '中风险', 'bgr': (0, 165, 255), 'rgb': (255, 165, 0)},
    'low': {'label': '低风险', 'bgr': (80, 170, 60), 'rgb': (60, 170, 80)},
}


def normalize_level(level):
    level = str(level or 'medium').lower()
    return level if level in LEVEL_STYLES else 'medium'


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def bbox_points(bbox):
    if not bbox:
        return None
    if len(bbox) == 4 and all(isinstance(v, (int, float)) for v in bbox):
        x1, y1, x2, y2 = bbox
        return [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
    return bbox


def transform_bbox(bbox, scale, bbox_space='original'):
    points = bbox_points(bbox)
    if not points:
        return None
    if bbox_space == 'original':
        return [[p[0] * scale, p[1] * scale] for p in points]
    if bbox_space == 'display':
        return points
    raise ValueError("bbox_space must be 'original' or 'display'")


def transform_risk_bboxes(risk, scale, bbox_space='original'):
    raw_bboxes = risk.get('bboxes')
    if raw_bboxes:
        transformed = [transform_bbox(b, scale, bbox_space) for b in raw_bboxes]
        transformed = [b for b in transformed if b]
        risk['bboxes'] = transformed
        risk['bbox'] = transformed[0] if transformed else None
        return
    risk['bbox'] = transform_bbox(risk.get('bbox'), scale, bbox_space)


def risk_bboxes(risk):
    if risk.get('bboxes'):
        return [b for b in risk['bboxes'] if b]
    if risk.get('bbox'):
        return [risk['bbox']]
    return []
    return points

# ============================================================
# 上下文修饰规则（2026-04-17 新增）
# 根据关键词出现的上下文调整风险判断
# ============================================================
# 格式：(关键词, 包含关键词的上下文片段, 调整后的风险等级或排除)
# - "排除" 表示该上下文下不是风险
# - "low" 表示降级为低风险
# - "medium" 表示中风险（默认）
# - "high" 表示高风险（默认）

CONTEXT_MODIFIERS = [
    # "好喝" 系列
    ('好喝', '好喝剩', '排除'),      # "好喝剩的" = 如果喝剩的，不是产品宣称
    ('好喝', '请即冲', '排除'),       # 说明性文字
    
    # "推荐" 系列
    ('推荐', '冲调方法及推荐食用量', '排除'),  # 食用方法说明
    ('推荐', '方法及推荐', '排除'),    # 食用方法说明
    ('推荐', '推荐食用量', '排除'),     # 食用量说明
    
    # "第一" 系列
    ('第一', '配料表第一位', 'medium'),  # 配料排序说明，但需加注
    ('第一', '配料表第', 'medium'),
    
    # "好吃" 系列  
    ('好吃', '好吃剩', '排除'),       # "好吃剩的" = 如果吃剩的
]



def check_context_modifier(risk_word, text):
    """
    检查关键词在文本中的上下文，返回调整后的风险等级
    
    Args:
        risk_word: 风险关键词
        text: 包含关键词的完整文本
    
    Returns:
        '排除' - 该上下文下不是风险
        'low' - 降级为低风险
        'medium' - 保持中风险
        'high' - 升级为高风险
        None - 使用默认风险等级
    """
    for keyword, context, action in CONTEXT_MODIFIERS:
        if keyword == risk_word and context in text:
            return action
    return None


def annotate_image(image_path, risks=None, output_path=None, bbox_space='original'):
    """
    Annotate image

    Args:
        image_path: Image path
        risks: Risk list, if None will auto-detect using risk word lists
        output_path: Output path
        bbox_space: 'original' when risks bbox is based on the input image,
                    'display' when risks bbox is already based on resized output.

    Returns:
        Output image path
    """
    import sys
    from PIL import Image as PILImage

    print(f"[DEBUG] annotate_image called, risks={'len='+str(len(risks)) if risks else 'None'}", file=sys.stderr)

    # Read and resize large images to avoid memory issues while preserving detail.
    img_pil = PILImage.open(image_path)
    orig_w, orig_h = img_pil.size
    print(f"Original image: {orig_w}x{orig_h}")

    aspect_ratio = orig_h / max(orig_w, 1)
    is_long_image = aspect_ratio >= 4
    is_wide_image = aspect_ratio <= 0.75
    if is_long_image:
        max_display_h = 13500
        max_display_w = 900
    elif is_wide_image:
        max_display_h = 1200
        max_display_w = 1800
    else:
        max_display_h = 1800
        max_display_w = 1400
    scale = 1.0
    if orig_w > max_display_w or orig_h > max_display_h:
        scale = min(max_display_w / orig_w, max_display_h / orig_h)
        new_w = int(orig_w * scale)
        new_h = int(orig_h * scale)
        img_pil = img_pil.resize((new_w, new_h), PILImage.LANCZOS)
        print(f"Resized to: {new_w}x{new_h} (scale={scale:.2f})")
        # Save to temp for OCR
        import tempfile
        temp_fd, temp_path = tempfile.mkstemp(suffix='.png')
        os.close(temp_fd)
        img_pil.save(temp_path)
    else:
        temp_path = None

    img = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    display_h, display_w = img.shape[:2]
    if risks:
        for risk in risks:
            transform_risk_bboxes(risk, scale, bbox_space)

    # OCR 只在自动检测，或外部 risks 缺少 bbox 时调用。
    # 如果外部审核结果已经给出 bbox，直接画框，避免多花一次百度 OCR 调用。
    needs_ocr = risks is None or any(not risk_bboxes(risk) for risk in risks)
    ocr_result = None
    ocr_image_path = temp_path if temp_path else image_path

    if needs_ocr:
        print("Recognizing text...")
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)
            from ocr_localize import find_text_by_content
            regions, source = find_text_by_content(ocr_image_path, '')
            # 转内部格式：[[bbox, text, conf], ...]
            ocr_result = []
            for r in regions:
                bbox = [[r['x1'], r['y1']], [r['x2'], r['y1']],
                        [r['x2'], r['y2']], [r['x1'], r['y2']]]
                ocr_result.append([bbox, r.get('text', ''), r.get('confidence', 0.5)])
            print(f"  [✓] ocr_localize({source}) 识别到 {len(ocr_result)} 个区域", file=sys.stderr)
        except Exception as e:
            print(f"  [⚠] OCR 失败 ({e})，将仅用传入的 risks 直接画框", file=sys.stderr)
            ocr_result = []
    else:
        print("Skip OCR: external risks already include bbox")
        ocr_result = []

    if not ocr_result and not risks:
        print("Warning: No OCR text and no risks provided, nothing to annotate")
        if temp_path:
            os.unlink(temp_path)
        return None

    print(f"Recognized {len(ocr_result) if ocr_result else 0} text regions")

    # For risks without bbox, try to match them to OCR results
    matched_count = 0
    if risks is not None:
        existing_bbox_count = 0
        for risk in risks:
            if risk_bboxes(risk):
                existing_bbox_count += 1
            else:
                risk_word = risk.get('word', '')
                # Try to find this word in OCR results
                for ocr_item in ocr_result:
                    ocr_text = ocr_item[1]
                    if risk_word in ocr_text:
                        risk['bbox'] = ocr_item[0]
                        risk['matched_text'] = ocr_text
                        print(f"  Matched external risk '{risk_word}' to OCR text '{ocr_text}'")
                        matched_count += 1
                        break
        total_bbox_count = existing_bbox_count + matched_count
        print(f"  BBox状态: {total_bbox_count}/{len(risks)} 个风险有bbox，其中OCR补齐 {matched_count} 个")

    # Auto-detect risks if not provided
    if risks is None:
        risks = []
        risk_id = 1
        all_risk_words = {**HIGH_RISK_WORDS, **MEDIUM_RISK_WORDS}

        for item in ocr_result:
            bbox, text, conf = item
            text_clean = text.strip()

            # Check each risk word
            for risk_word, reason in all_risk_words.items():
                # 检查是否在词库中标记为可使用（低风险/可忽略）
                if '可使用' in str(reason) or '合规' in str(reason):
                    continue
                    
                if risk_word in text_clean:
                    # 检查上下文修饰规则
                    context_action = check_context_modifier(risk_word, text_clean)
                    
                    if context_action == '排除':
                        print(f"  ⏭️ 排除: '{risk_word}' in '{text_clean}' (上下文判断)")
                        continue
                    
                    # 确定风险等级
                    if risk_word in HIGH_RISK_WORDS:
                        base_level = 'high'
                    else:
                        base_level = 'medium'
                    
                    # 根据上下文调整
                    if context_action == 'low':
                        level = 'low'
                    elif context_action == 'medium':
                        level = 'medium'
                    elif context_action == 'high':
                        level = 'high'
                    else:
                        level = base_level
                    
                    risks.append({
                        'id': risk_id,
                        'word': risk_word,
                        'level': level,
                        'reason': reason,
                        'suggestion': COMPLIANT_ALTERNATIVES.get(risk_word, '建议删除或修改'),
                        'bbox': bbox,
                        'matched_text': text_clean
                    })
                    risk_id += 1
                    level_icon = '🔴' if level == 'high' else ('🟡' if level == 'medium' else '🟢')
                    print(f"  {level_icon} {level.upper()}: '{risk_word}' in '{text_clean}'")

        print(f"\n规则匹配完成: {len(risks)} 个候选风险")

    if not risks:
        print("No risks detected!")
        if temp_path:
            os.unlink(temp_path)
        return None

    # ============================================================
    # 长图批注版排版：左侧原图，右侧风险卡片按原图 y 轴位置排列。
    # ============================================================
    if is_long_image:
        panel_w = int(clamp(display_w * 0.60, 420, 560))
    elif is_wide_image:
        panel_w = int(clamp(display_w * 0.42, 420, 680))
    else:
        panel_w = int(clamp(display_w * 0.50, 420, 620))
    panel_padding = int(clamp(panel_w * 0.032, 12, 20))
    card_padding = int(clamp(panel_w * 0.024, 9, 14))
    card_gap = int(clamp(panel_w * 0.020, 8, 12))
    title_size = int(clamp(panel_w * (0.040 if is_long_image else 0.043), 18, 24))
    body_size = int(clamp(panel_w * (0.027 if is_long_image else 0.029), 12, 16))
    small_size = int(clamp(body_size - 1, 11, 14))
    line_ratio = 1.22
    title_font = load_cjk_font(title_size)
    header_font = load_cjk_font(body_size)
    body_font = load_cjk_font(body_size)
    small_font = load_cjk_font(small_size)
    header_line_h = int(body_size * line_ratio)
    body_line_h = int(body_size * line_ratio)
    small_line_h = int(small_size * line_ratio)

    def text_w(font, text):
        try:
            box = font.getbbox(text)
            return box[2] - box[0]
        except Exception:
            return len(text) * body_size * 0.6

    def text_size(font, text):
        try:
            box = font.getbbox(text)
            return box[2] - box[0], box[3] - box[1]
        except Exception:
            return int(len(text) * small_size * 0.6), small_size

    def wrap_text(text, font, max_width, max_lines=None):
        text = str(text or '').replace('\n', ' ').strip()
        if not text:
            return []
        lines, current = [], ''
        for ch in text:
            test = current + ch
            if text_w(font, test) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = ch
                if max_lines and len(lines) >= max_lines:
                    break
        if current and (not max_lines or len(lines) < max_lines):
            lines.append(current)
        if max_lines and len(lines) == max_lines and len(''.join(lines)) < len(text):
            lines[-1] = lines[-1].rstrip('。；，,. ') + '...'
        return lines

    def draw_centered_text(draw, center, text, font, fill):
        try:
            box = draw.textbbox((0, 0), text, font=font)
            text_w = box[2] - box[0]
            text_h = box[3] - box[1]
            x = center[0] - text_w / 2 - box[0]
            y = center[1] - text_h / 2 - box[1]
        except Exception:
            text_w = len(text) * small_size * 0.6
            text_h = small_size
            x = center[0] - text_w / 2
            y = center[1] - text_h / 2
        draw.text((x, y), text, fill=fill, font=font)

    def risk_anchor_y(risk):
        boxes = risk_bboxes(risk)
        if not boxes:
            return None
        ys = []
        for bbox in boxes:
            points = bbox_points(bbox)
            ys.extend([p[1] for p in points])
        return int((min(ys) + max(ys)) / 2)

    badge_gutter = 30 if is_long_image else 36
    card_text_w = panel_w - panel_padding * 2 - card_padding * 2 - badge_gutter
    item_data_list = []
    for idx, risk in enumerate(risks, 1):
        risk.setdefault('id', idx)
        level = normalize_level(risk.get('level'))
        style = LEVEL_STYLES[level]
        title = risk.get('title') or risk.get('word') or risk.get('matched_text') or '风险点'
        basis = risk.get('basis') or risk.get('依据') or risk.get('law') or ''
        reason = risk.get('reason') or risk.get('判定') or ''
        suggestion = risk.get('suggestion') or risk.get('改法') or '建议修改或删除'
        header = f"[{risk['id']}] {title} | {style['label']}"
        header_lines = wrap_text(header, header_font, card_text_w, 2)
        basis_lines = wrap_text(f"依据: {basis}", small_font, card_text_w, 2) if basis else []
        reason_lines = wrap_text(f"理由: {reason}", body_font, card_text_w, 3 if is_long_image else 4)
        suggest_lines = wrap_text(f"建议: {suggestion}", body_font, card_text_w, 2 if is_long_image else 3)
        card_h = (
            card_padding * 2
            + len(header_lines) * header_line_h
            + (3 if basis_lines else 0) + len(basis_lines) * small_line_h
            + (4 if reason_lines else 0) + len(reason_lines) * body_line_h
            + (4 if suggest_lines else 0) + len(suggest_lines) * body_line_h
        )
        item_data_list.append({
            'risk': risk,
            'level': level,
            'style': style,
            'header_lines': header_lines,
            'basis_lines': basis_lines,
            'reason_lines': reason_lines,
            'suggest_lines': suggest_lines,
            'card_h': max(card_h, 44 if is_long_image else 64),
            'anchor_y': risk_anchor_y(risk),
        })

    header_h = max((54 if is_long_image else 68), panel_padding * 2 + title_size + small_size + 8)
    footer_h = max(28, small_size + 16)
    total_cards_h = sum(item['card_h'] for item in item_data_list) + card_gap * max(len(item_data_list) - 1, 0)
    min_panel_h_for_cards = header_h + panel_padding + total_cards_h + footer_h + panel_padding
    panel_h = max(display_h, min_panel_h_for_cards)
    top_limit = header_h + panel_padding
    bottom_limit = panel_h - footer_h - panel_padding
    if (not is_long_image) or all(item['anchor_y'] is None for item in item_data_list):
        current_y = top_limit
        for item in item_data_list:
            item['card_y'] = current_y
            current_y += item['card_h'] + card_gap
    else:
        fallback_step = max((bottom_limit - top_limit) // max(len(item_data_list), 1), 1)
        for i, item in enumerate(item_data_list):
            item['desired_y'] = (item['anchor_y'] if item['anchor_y'] is not None else top_limit + i * fallback_step) - item['card_h'] // 2
        item_data_list.sort(key=lambda item: item['desired_y'])
        current_y = top_limit
        for item in item_data_list:
            item['card_y'] = max(item['desired_y'], current_y)
            current_y = item['card_y'] + item['card_h'] + card_gap
        overflow = current_y - card_gap - bottom_limit
        if overflow > 0:
            for item in reversed(item_data_list):
                item['card_y'] -= overflow
                overflow = max(top_limit - item['card_y'], 0)
                item['card_y'] = max(item['card_y'], top_limit)

    print("批注版排版参数:")
    print(f"  长图模式: {'是' if is_long_image else '否'}")
    print(f"  图片: {display_w}x{display_h}px, 右栏: {panel_w}x{panel_h}px")
    print(f"  风险卡片: {len(item_data_list)} 项")

    # ============================================================
    # 绘制部分
    # ============================================================
    
    # --- 图片上的红框和编号（基于OCR文字区域大小自适应）---
    img_h, img_w = img.shape[:2]
    
    # LINE_WIDTH 应该和图片尺寸成正比（至少2px）
    LINE_WIDTH = max(int(min(img_w, img_h) * (0.002 if is_long_image else 0.0015)), 2)
    
    for risk in risks:
        for bbox in risk_bboxes(risk):
            level = normalize_level(risk.get('level'))
            color = LEVEL_STYLES[level]['bgr']
            pts = np.array(bbox, dtype=np.int32)
            cv2.polylines(img, [pts], isClosed=True, color=color, thickness=LINE_WIDTH)
            
            # 圆圈放在左上角(pts[0])，避免挡住文字内容
            # 圆圈大小基于单个文字区域的尺寸自适应
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            bbox_w = max(xs) - min(xs)
            bbox_h = max(ys) - min(ys)
            circle_radius = max(min(int(min(bbox_w, bbox_h) * 0.32), 18), 8)
            
            min_x = min(xs)
            min_y = min(ys)
            center_x = int(np.clip(min_x + circle_radius, circle_radius + 1, img_w - circle_radius - 1))
            center_y = int(np.clip(min_y + circle_radius, circle_radius + 1, img_h - circle_radius - 1))
            cv2.circle(img, (center_x, center_y), circle_radius, color, -1)
            
            # 编号按文字实际尺寸居中，兼容 1 位/2 位编号和不同圆半径。
            number = str(risk['id'])
            font_scale = circle_radius / (13.0 if len(number) == 1 else 17.0)
            font_thickness = max(1, int(circle_radius / 7))
            (text_w, text_h), baseline = cv2.getTextSize(
                number, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness
            )
            text_x = int(center_x - text_w / 2)
            text_y = int(center_y + text_h / 2 - baseline)
            cv2.putText(img, number,
                        (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, font_scale,
                        (255, 255, 255), font_thickness, cv2.LINE_AA)
    
    # --- 右侧面板 ---
    panel = np.ones((panel_h, panel_w, 3), dtype=np.uint8) * 255
    panel_pil = Image.fromarray(panel)
    draw = ImageDraw.Draw(panel_pil)
    draw.rectangle([0, 0, panel_w - 1, panel_h - 1], outline=(220, 220, 220), width=1)
    draw.rectangle([0, 0, panel_w, header_h], fill=(248, 250, 252))
    high_count = sum(1 for r in risks if normalize_level(r.get('level')) == 'high')
    med_count = sum(1 for r in risks if normalize_level(r.get('level')) == 'medium')
    low_count = sum(1 for r in risks if normalize_level(r.get('level')) == 'low')
    draw.text((panel_padding, panel_padding), "版面审核风险标注", fill=(20, 20, 20), font=title_font)
    summary = f"共 {len(risks)} 项  高 {high_count} / 中 {med_count} / 低 {low_count}"
    draw.text((panel_padding, panel_padding + title_size + 8), summary, fill=(90, 90, 90), font=small_font)

    for item_info in item_data_list:
        risk = item_info['risk']
        header_lines = item_info['header_lines']
        basis_lines = item_info['basis_lines']
        reason_lines = item_info['reason_lines']
        suggest_lines = item_info['suggest_lines']
        card_h = item_info['card_h']
        rect_color = item_info['style']['rgb']
        
        # 绘制卡片背景
        card_left = panel_padding
        card_top = int(item_info['card_y'])
        card_right = panel_w - panel_padding
        card_bottom = card_top + card_h
        
        draw.rectangle([card_left, card_top, card_right, card_bottom],
                       fill=(248, 248, 248), outline=rect_color, width=LINE_WIDTH)
        draw.rectangle([card_left, card_top, card_left + 5, card_bottom], fill=rect_color)
        
        # 绘制内容
        content_x = card_left + card_padding + badge_gutter
        y = card_top + card_padding
        badge_text = str(risk['id'])
        badge_text_w, badge_text_h = text_size(small_font, badge_text)
        dot_r = max(8 if is_long_image else 10, int(max(badge_text_w, badge_text_h) / 2) + 4)
        dot_center = (card_left + dot_r, card_top + dot_r)
        draw.ellipse(
            [
                dot_center[0] - dot_r,
                dot_center[1] - dot_r,
                dot_center[0] + dot_r,
                dot_center[1] + dot_r,
            ],
            fill=rect_color,
        )
        draw_centered_text(draw, dot_center, badge_text, small_font, (255, 255, 255))
        
        # Header（风险词 + 等级）
        for line in header_lines:
            draw.text((content_x, y), line, fill=(0, 0, 0), font=header_font)
            y += header_line_h

        if basis_lines:
            y += 3
            for line in basis_lines:
                draw.text((content_x, y), line, fill=(85, 85, 85), font=small_font)
                y += small_line_h
        
        # 理由
        y += 4
        for line in reason_lines:
            draw.text((content_x, y), line, fill=(60, 60, 60), font=body_font)
            y += body_line_h
        
        # 建议
        y += 4
        for line in suggest_lines:
            draw.text((content_x, y), line, fill=(0, 100, 0), font=body_font)
            y += body_line_h
    
    # 底部注释
    draw.rectangle([0, panel_h - footer_h, panel_w, panel_h], fill=(248, 250, 252))
    draw.text((panel_padding, panel_h - footer_h + 7), 
              "本标注仅供参考，最终以法务意见为准", fill=(100, 100, 100), font=small_font)

    # 合并图片和面板
    panel_arr = cv2.cvtColor(np.array(panel_pil), cv2.COLOR_RGB2BGR)
    if display_h > panel_arr.shape[0]:
        panel_arr = np.vstack([panel_arr, 
                                np.ones((display_h - panel_arr.shape[0], panel_w, 3), dtype=np.uint8) * 255])
    elif panel_arr.shape[0] > display_h:
        img = np.vstack([img, 
                         np.ones((panel_arr.shape[0] - display_h, display_w, 3), dtype=np.uint8) * 255])

    img_combined = np.hstack([img, panel_arr])

    # 保存
    if output_path is None:
        name, ext = os.path.splitext(image_path)
        output_path = f"{name}_annotated.png"

    cv2.imwrite(output_path, img_combined, [cv2.IMWRITE_PNG_COMPRESSION, 9])
    print(f"\nSaved: {output_path}")

    # Cleanup temp file
    if temp_path and os.path.exists(temp_path):
        os.unlink(temp_path)

    return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='营销版面标注图生成（业务版 v1.1.2）'
    )
    parser.add_argument('image_path', help='输入图片路径')
    parser.add_argument('output_path', nargs='?', default=None, help='输出图片路径（默认原路径 + _annotated 后缀）')
    parser.add_argument('--risks', default=None,
                        help='外部传入 risks JSON 文件路径（人工/其他审核结果输出）'
                             '格式：[{"word":"...","bbox":[x1,y1,x2,y2],"level":"high|medium|low","reason":"...","suggestion":"..."}]')
    parser.add_argument('--bbox-space', choices=['original', 'display'], default='original',
                        help='risks bbox 坐标系。original=输入原图坐标（默认）；display=缩放后输出图坐标')
    args = parser.parse_args()

    risks = None
    if args.risks:
        import json
        with open(args.risks, 'r', encoding='utf-8') as f:
            risks = json.load(f)
        # 外部传入的 risks 可能没有 id 字段，补上（画标注图需用）
        for i, r in enumerate(risks, 1):
            r.setdefault('id', i)
            # bbox/bboxes 标准化：支持矩形或多边形顶点。
            if r.get('bboxes'):
                r['bboxes'] = [bbox_points(b) for b in r['bboxes']]
                r['bboxes'] = [b for b in r['bboxes'] if b]
            elif r.get('bbox'):
                r['bbox'] = bbox_points(r['bbox'])
        print(f"载入外部 risks: {len(risks)} 项")

    annotate_image(args.image_path, risks, args.output_path, bbox_space=args.bbox_space)


if __name__ == "__main__":
    main()

# ============================================================
