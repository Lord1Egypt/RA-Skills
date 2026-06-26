#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 报告生成器（现代 SaaS 高颜值版 v4 - 逻辑完全对齐原版）
- 引入 HexColor 现代网页级配色（蓝/绿/橙/红）
- 引入富文本 Paragraph 实现彩色星级（⭐⭐⭐⭐⭐ 效果）
- 扁平化表格设计，移除沉重的纯黑边框
- 100% 保留原有业务逻辑（饮水、进食明细、风险预警等全部恢复）
"""

import os
import re
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ==================== 现代 UI 配色板 ====================
C_PRIMARY = HexColor("#2563EB")   # 科技蓝 (主标题/重要标识)
C_SUCCESS = HexColor("#10B981")   # 达标绿 (正常/优秀)
C_WARNING = HexColor("#F59E0B")   # 警告橙 (关注/待改进)
C_DANGER  = HexColor("#EF4444")   # 危险红 (超标/有症状)
C_TEXT_MAIN = HexColor("#1E293B") # 主文本色 (深灰，比纯黑更柔和)
C_TEXT_MUTED= HexColor("#64748B") # 辅助文本色 (浅灰)
C_BG_HEAD = HexColor("#F8FAFC")   # 表头背景色(极浅灰)
C_BORDER  = HexColor("#E2E8F0")   # 表格边框色


def clean_html_tags(text):
    """移除 HTML 标签及会导致 PDF 崩溃的复杂彩色 Emoji 和特殊字符"""
    if not text:
        return ""
    text = str(text)
    # 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 移除会导致 PDF 崩溃的复杂彩色 Emoji
    emojis_to_remove = ['⭐', '✅', '⚠️', '❌', '🎉', '💡', '🚶', '🍎', '🥗', '💧', '🏃', '📊', '📈', '📄', '📥', '🥣', '🍜', '🍽️', '🍲', '⏰', '🚴', '🧘', '🔴', '🥦', '🍚', '🍳', '🥤', '🕐', '🌙', '💪', '🎯', '📌', '👍', '💯']
    for emoji in emojis_to_remove:
        text = text.replace(emoji, '')
    # 修复 2：移除其他特殊字符（乱码、不可打印字符等）
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)  # 控制字符
    text = re.sub(r'[\ufffd]', '', text)  # 替换字符
    text = re.sub(r'\s+', ' ', text)  # 多个空格合并为一个
    return text.strip()

def stars_to_text(stars_str):
    """利用富文本实现美观的彩色星级 (如: ★★★☆☆)"""
    if not stars_str:
        return ""
    star_count = stars_str.count('⭐')
    # 亮星用金色，暗星用浅灰色
    active = f'<font color="#F59E0B">{"★" * star_count}</font>'
    inactive = f'<font color="#E2E8F0">{"★" * (5 - star_count)}</font>'
    return active + inactive

def register_chinese_font():
    """注册中文字体"""
    try:
        pdfmetrics.getFont('Chinese')
        return 'Chinese'
    except:
        pass
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_ttf = os.path.join(script_dir, "..", "assets", "NotoSansSC-VF.ttf")
    local_ttf = os.path.normpath(local_ttf)
    
    if os.path.exists(local_ttf):
        try:
            pdfmetrics.registerFont(TTFont('Chinese', local_ttf))
            return 'Chinese'
        except Exception as e:
            print(f"⚠️ 字体加载失败：{e}")
    
    return 'Helvetica'

def generate_pdf_report(data, profile, scores, nutrition, macros, risks, plan, output_path, water_records=None, meals=None, exercise_data=None, ai_comment=None):
    """生成高颜值 PDF 报告（修复 2：JSON 解析 + 修复 3：AI 点评）"""
    font_name = register_chinese_font()
    
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                           rightMargin=2*cm, leftMargin=2*cm,
                           topMargin=2*cm, bottomMargin=2*cm)
    
    styles = getSampleStyleSheet()
    
    # === 重新定义高颜值文字样式 ===
    title_style = ParagraphStyle(
        'CustomTitle', parent=styles['Heading1'],
        fontSize=20, textColor=C_PRIMARY, spaceAfter=10,
        alignment=TA_CENTER, fontName=font_name,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading', parent=styles['Heading2'],
        fontSize=13, textColor=C_PRIMARY, spaceBefore=15, spaceAfter=10,
        fontName=font_name,
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal', parent=styles['Normal'],
        fontSize=10, textColor=C_TEXT_MAIN, fontName=font_name, leading=15,
    )
    
    cell_style_center = ParagraphStyle(
        'CellCenter', parent=normal_style, alignment=TA_CENTER, leading=12
    )
    
    # === 通用的现代化表格样式（清爽无黑框） ===
    base_table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), C_BG_HEAD),
        ('TEXTCOLOR', (0, 0), (-1, 0), C_TEXT_MAIN),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, C_BORDER),
    ]

    story = []
    
    # ==================== 页面头部 ====================
    story.append(Paragraph("<b>胆结石健康日报</b>", title_style))
    story.append(Paragraph(f"<font color='#64748B'>{data['date']} | 监测人：{profile.get('name', '默认用户')}</font>", ParagraphStyle('Date', parent=normal_style, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.5*cm))
    
    # ==================== 一、综合评分 ====================
    story.append(Paragraph("一、今日综合评分", heading_style))
    
    score_data = [
        ["维度", "得分", "星级", "状态"],
        ["饮食合规性", f"{scores['diet']['raw']:.0f}/100", Paragraph(stars_to_text(scores["diet"]["stars"]), cell_style_center), "达标" if scores["diet"]["raw"]>=80 else "待改进"],
        ["饮水完成度", f"{scores['water']['raw']:.0f}/100", Paragraph(stars_to_text(scores["water"]["stars"]), cell_style_center), "达标" if scores["water"]["raw"]>=100 else "未达标"],
        ["体重管理", f"{scores['weight']['raw']:.0f}/100", Paragraph(stars_to_text(scores["weight"]["stars"]), cell_style_center), "正常" if scores["weight"].get("bmi") and 18.5<=scores["weight"]["bmi"]<24 else "关注"],
        ["症状管理", f"{scores['symptom']['raw']:.0f}/100", Paragraph(stars_to_text(scores["symptom"]["stars"]), cell_style_center), "无症状" if not scores["symptom"]["has_symptoms"] else "有症状"],
        ["运动管理", f"{scores['exercise']['raw']:.0f}/100", Paragraph(stars_to_text(scores["exercise"]["stars"]), cell_style_center), "达标" if scores["exercise"]["raw"]>=60 else "待加强"],
        ["健康依从性", f"{scores['adherence']['raw']:.0f}/100", Paragraph(stars_to_text(scores["adherence"]["stars"]), cell_style_center), "优秀" if scores["adherence"]["raw"]>=80 else "一般"],
        ["总分", f"{scores['total']:.0f}/100", Paragraph(stars_to_text(scores["total_stars"]), cell_style_center), "优秀" if scores["total"]>=80 else "良好" if scores["total"]>=60 else "待改进"],
    ]
    
    score_table = Table(score_data, colWidths=[4*cm, 3*cm, 3.5*cm, 3.5*cm])
    score_style = list(base_table_style)
    # 状态列彩色渲染
    for i in range(1, len(score_data)):
        status = score_data[i][3]
        if status in ["达标", "优秀", "正常", "无症状"]:
            score_style.append(('TEXTCOLOR', (3, i), (3, i), C_SUCCESS))
        elif status in ["待改进", "未达标", "关注", "有症状", "待加强", "一般"]:
            score_style.append(('TEXTCOLOR', (3, i), (3, i), C_WARNING if status in ["关注", "待加强", "一般", "待改进"] else C_DANGER))
    
    score_table.setStyle(TableStyle(score_style))
    story.append(score_table)
    story.append(Spacer(1, 0.4*cm))
    
    # ==================== 修复 3：AI 专属健康点评 ====================
    if ai_comment:
        story.append(Paragraph("专家 AI 点评", heading_style))
        # 清理评论中的日志前缀和特殊字符
        clean_comment = ai_comment
        for prefix in ['[plugins]', '[adp-', 'Hint:', 'error:']:
            clean_comment = '\n'.join([l for l in clean_comment.split('\n') if not l.strip().startswith(prefix)])
        clean_comment = clean_comment.strip()
        
        # 将点评分成段落（按句号分割）
        paragraphs = re.split(r'(?<=[.!。!])\s+', clean_comment)
        for para in paragraphs[:5]:  # 最多显示 5 段
            if para.strip():
                story.append(Paragraph(f"<font color='#1E293B'>{clean_html_tags(para)}</font>", normal_style))
        story.append(Spacer(1, 0.3*cm))
    
    # ==================== 二、基础健康数据 ====================
    story.append(Paragraph("二、基础健康数据", heading_style))
    
    from health_report_pro import calculate_bmr, calculate_tdee
    bmi_val = scores["weight"].get("bmi", 0) or 0
    weight_val = data.get("weight_morning")
    bmr_val = calculate_bmr(weight_val if weight_val else 65, profile["height_cm"], profile["age"], profile["gender"])
    tdee_val = calculate_tdee(bmr_val, profile["activity_level"])
    
    health_data = [
        ["指标", "数值", "参考范围"],
        ["身高", f"{profile['height_cm']}cm", "-"],
        ["体重", f"{weight_val*2:.1f}斤" if weight_val else "未记录", f"目标：{profile.get('target_weight_kg', 64)*2:.1f} 斤"],
        ["BMI", f"{bmi_val:.1f}", "18.5-24（正常）"],
        ["基础代谢", f"{bmr_val:.0f} kcal", "-"],
        ["每日消耗", f"{tdee_val:.0f} kcal", "-"],
        ["推荐热量", f"{tdee_val:.0f} kcal/天", "胆结石安全范围"],
        ["蛋白质", f"{macros.get('protein_g', 0)}g/天", f"{macros.get('protein_p', 0)}%总热量"],
        ["脂肪", f"{macros.get('fat_g', 0)}g/天", f"{macros.get('fat_p', 0)}%（低脂）"],
        ["碳水", f"{macros.get('carb_g', 0)}g/天", f"{macros.get('carb_p', 0)}%总热量"],
        ["膳食纤维", f">={macros.get('fiber_min_g', 25)}g/天", "促进胆汁排泄"],
    ]
    
    health_table = Table(health_data, colWidths=[5*cm, 4*cm, 5*cm])
    health_style = list(base_table_style)
    # BMI 颜色高亮
    if 18.5 <= bmi_val < 24:
        health_style.append(('TEXTCOLOR', (1, 3), (1, 3), C_SUCCESS))
    elif bmi_val > 0:
        health_style.append(('TEXTCOLOR', (1, 3), (1, 3), C_DANGER if bmi_val >= 28 or bmi_val < 18.5 else C_WARNING))

    health_table.setStyle(TableStyle(health_style))
    story.append(health_table)
    story.append(Spacer(1, 0.4*cm))
    
    # ==================== 三、当日营养摄入 ====================
    story.append(Paragraph("三、当日营养摄入核算", heading_style))
    
    nutrition_data = [
        ["营养素", "实际摄入", "推荐量"],
        ["总热量", f"{nutrition['calories']:.0f} kcal", f"{tdee_val:.0f} kcal"],
        ["蛋白质", f"{nutrition['protein']:.1f}g", f"{macros.get('protein_g', 0)}g"],
        ["脂肪", f"{nutrition['fat']:.1f}g", f"{macros.get('fat_g', 0)}g"],
        ["碳水", f"{nutrition['carb']:.1f}g", f"{macros.get('carb_g', 0)}g"],
        ["膳食纤维", f"{nutrition['fiber']:.1f}g", f">={macros.get('fiber_min_g', 25)}g"],
    ]
    
    nutri_table = Table(nutrition_data, colWidths=[5*cm, 4*cm, 5*cm])
    nutri_style = list(base_table_style)
    nutri_table.setStyle(TableStyle(nutri_style))
    story.append(nutri_table)
    story.append(Spacer(1, 0.4*cm))
    
    # ==================== 四、饮水详情 (完全恢复) ====================
    story.append(Paragraph("四、饮水详情", heading_style))
    if water_records and len(water_records) > 0:
        water_data = [["时间", "饮水量", "累计进度"]]
        for record in water_records:
            time_str = record.get("time", "")
            amount = record.get("amount_ml", 0)
            cumulative = record.get("cumulative_ml", 0)
            progress = f"{cumulative}/2000ml ({cumulative//20}%)"
            water_data.append([time_str, f"{amount}ml", progress])
        
        water_table = Table(water_data, colWidths=[4*cm, 3*cm, 7*cm])
        water_table.setStyle(TableStyle(base_table_style))
        story.append(water_table)
    else:
        story.append(Paragraph("<font color='#64748B'>今日无饮水记录</font>", normal_style))
    story.append(Spacer(1, 0.4*cm))
    
    # ==================== 五、进食详情 (完全恢复) ====================
    story.append(Paragraph("五、进食详情", heading_style))
    if meals and len(meals) > 0:
        seen_meals = set()
        for meal in meals:
            meal_type = meal.get("type", "")
            meal_time = meal.get("time", "")
            meal_key = f"{meal_type}_{meal_time}"
            
            if meal_key in seen_meals:
                continue
            seen_meals.add(meal_key)
            
            food_nutrition = meal.get("food_nutrition", [])
            total_calories = meal.get("total_calories", 0)
            
            story.append(Paragraph(f"<b>{meal_type}（{meal_time}）</b>- 总计 {total_calories:.0f} kcal", ParagraphStyle('MealTitle', parent=normal_style, fontSize=10, textColor=C_PRIMARY, spaceBefore=4, spaceAfter=4)))
            
            if food_nutrition and len(food_nutrition) > 0:
                meal_data = [["食物", "份量", "热量", "蛋白质", "脂肪", "碳水"]]
                for food in food_nutrition:
                    name = food.get("name", "")
                    
                    # 修复 1：智能提取食物名中的单位（如"250ml"、"200g"、"1 个"）
                    if '→' in name:
                        name_raw = name.split('→')[0].strip()
                    else:
                        name_raw = name.strip()
                    
                    # 提取份量单位（支持 ml/g/个/碗/份等）
                    portion_match = re.search(r'(\d+(?:\.\d+)?)\s*(ml|g|个 | 碗 | 份 | 杯 | 片)', name_raw)
                    if portion_match:
                        portion_value = float(portion_match.group(1))
                        portion_unit = portion_match.group(2)
                        # 从食物名中移除份量
                        name_simple = re.sub(r'\s*' + re.escape(portion_match.group(0)), '', name_raw).strip()
                        # 转换为单位 g（ml 近似为 g）
                        if portion_unit == 'ml':
                            portion_grams = portion_value
                        elif portion_unit == '个':
                            portion_grams = portion_value * 50  # 估算
                        elif portion_unit == '碗':
                            portion_grams = portion_value * 150
                        elif portion_unit == '份':
                            portion_grams = portion_value * 100
                        elif portion_unit == '杯':
                            portion_grams = portion_value * 200
                        elif portion_unit == '片':
                            portion_grams = portion_value * 30
                        else:  # g
                            portion_grams = portion_value
                        portion_display = f"{portion_value:.0f}{portion_unit}"
                    else:
                        # 没有单位，使用默认份量
                        name_simple = name_raw
                        portion_grams = food.get("portion_grams", 100)
                        portion_display = f"{portion_grams:.0f}g"
                    
                    # 修复 1：清理食物名中的各种标注（约、约 75g 等）
                    name_simple = re.sub(r'\s*（约\d+g）$', '', name_simple)
                    name_simple = re.sub(r'\s*（约）$', '', name_simple)  # 移除单独的"（约）"
                    name_simple = re.sub(r'\s*约$', '', name_simple)  # 移除末尾的"约"
                    name_simple = name_simple.strip()
                    
                    # 如果名字太短，使用原始名
                    if len(name_simple) < 2:
                        name_simple = name_raw
                    
                    # 获取营养数据（已根据份量缩放）
                    calories = food.get("calories", 0)
                    protein = food.get("protein", 0)
                    fat = food.get("fat", 0)
                    carb = food.get("carb", 0)
                    
                    meal_data.append([
                        clean_html_tags(name_simple),
                        portion_display,
                        f"{calories:.0f}kcal",
                        f"{protein:.1f}g",
                        f"{fat:.1f}g",
                        f"{carb:.1f}g"
                    ])
                
                meal_table = Table(meal_data, colWidths=[4*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2*cm])
                # 子表样式：表头颜色更浅
                sub_table_style = list(base_table_style)
                sub_table_style[0] = ('BACKGROUND', (0, 0), (-1, 0), HexColor("#F1F5F9"))
                sub_table_style[9] = ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#CBD5E1"))
                meal_table.setStyle(TableStyle(sub_table_style))
                story.append(meal_table)
            else:
                story.append(Paragraph("<font color='#64748B'>无详细食物记录</font>", normal_style))
            story.append(Spacer(1, 0.2*cm))
    else:
        story.append(Paragraph("<font color='#64748B'>今日无进食记录</font>", normal_style))
    story.append(Spacer(1, 0.4*cm))
    
    # ==================== 六、运动详情 ====================
    story.append(Paragraph("六、运动详情", heading_style))
    if exercise_data:
        cycling_list = exercise_data.get("cycling", []) if isinstance(exercise_data, dict) else [e for e in exercise_data if e.get("type") == "骑行"]
        walking = exercise_data.get("walking", {}) if isinstance(exercise_data, dict) else {}
        steps = walking.get("steps", 0)
        
        total_cycling_km = sum(c.get("distance_km", 0) for c in cycling_list)
        total_cycling_min = sum(c.get("duration_min", 0) for c in cycling_list)
        
        exercise_table_data = [["项目", "详情"]]
        if cycling_list:
            cycling_details = [f"{c.get('distance_km', 0)}km/{c.get('duration_min', 0)}分钟" for c in cycling_list]
            exercise_table_data.append(["骑行", "；".join(cycling_details) + f"\n（合计 {total_cycling_km}km / {total_cycling_min:.0f}分钟）"])
        if steps > 0:
            exercise_table_data.append(["步数", f"{steps}步"])
            
        exercise_raw = scores.get("exercise", {}).get("raw", 0)
        exercise_status = "达标" if exercise_raw >= 60 else "待加强"
        exercise_table_data.append(["运动评分", f"{exercise_raw:.0f}/100"])
        exercise_table_data.append(["状态", Paragraph(f"<font color='#10B981'><b>达标</b></font>" if exercise_status == "达标" else f"<font color='#F59E0B'><b>待加强</b></font>", cell_style_center)])
        
        exercise_table = Table(exercise_table_data, colWidths=[5*cm, 9*cm])
        exercise_table.setStyle(TableStyle(base_table_style))
        story.append(exercise_table)
    else:
        story.append(Paragraph("<font color='#64748B'>今日无运动记录</font>", normal_style))
    story.append(Spacer(1, 0.4*cm))
    
    # ==================== 七、风险预警 (完全恢复) ====================
    story.append(Paragraph("七、风险预警", heading_style))
    if risks:
        for risk in risks:
            level = clean_html_tags(risk.get('level', '')).strip()
            item_text = clean_html_tags(risk.get('item', ''))
            story.append(Paragraph(f"<font color='#EF4444'><b>{level} {item_text}</b></font>", normal_style))
            story.append(Paragraph(f"<font color='#64748B'>风险：</font>{clean_html_tags(risk.get('risk', ''))}", normal_style))
            story.append(Paragraph(f"<font color='#64748B'>建议：</font>{clean_html_tags(risk.get('action', ''))}", normal_style))
            story.append(Spacer(1, 0.2*cm))
    else:
        story.append(Paragraph("<font color='#10B981'>今日无明显风险，继续保持健康生活方式！</font>", normal_style))
    story.append(Spacer(1, 0.4*cm))
    
    # ==================== 八、次日方案（修复 2：JSON 对象解析）====================
    story.append(Paragraph("八、次日可执行方案", heading_style))
    
    # 修复 2 和 3：处理 AI 返回的 JSON 对象数组格式（增强通用性，兼容不同大模型）
    # 修复 2：文字修改 - "居家简易版"改成"饮食计划"
    if plan.get("diet"):
        story.append(Paragraph("<b>饮食计划</b>", ParagraphStyle('Sub', parent=normal_style, textColor=C_TEXT_MAIN, spaceAfter=6)))
        for item in plan.get("diet", []):
            if isinstance(item, dict):
                # 修复 3：兼容不同大模型的字段名
                meal = item.get('meal', item.get('meal_name', ''))
                time = item.get('time', item.get('time_range', item.get('period', '')))
                # 兼容多种字段名：menu/items/dishes/menu_detail/food/content
                menu = item.get('menu', '')
                if not menu:
                    # AI 返回的是 items 数组（千问 3.5plus 格式）
                    items = item.get('items', [])
                    if items:
                        menu = '、'.join(str(i) for i in items[:3])  # 只显示前 3 项
                        if len(items) > 3:
                            menu += ' 等'
                # 如果还是空，尝试其他字段名
                if not menu:
                    menu = item.get('dishes', item.get('menu_detail', item.get('food', item.get('content', ''))))
                calories = item.get('calories', item.get('kcal', ''))
                fat = item.get('fat', item.get('fat_g', ''))
                fiber = item.get('fiber', item.get('fiber_g', ''))
                # 构建完整显示：时间 + 菜单 + 营养信息
                if menu:
                    nutrition_info = f"({calories}kcal"
                    if fat: nutrition_info += f", 脂肪{fat}g"
                    if fiber: nutrition_info += f", 纤维{fiber}g"
                    nutrition_info += ")"
                    clean_item = f"{time} {clean_html_tags(menu)} {nutrition_info}"
                elif meal and time:
                    clean_item = f"{meal} ({time})"
                else:
                    # 退化为显示所有可用字段
                    clean_item = f"{meal} {time}"
            else:
                # 修复 3：如果是字符串（其他大模型直接返回文本），直接使用
                clean_item = clean_html_tags(str(item))
            story.append(Paragraph(f"<font color='#2563EB'>■</font> {clean_item}", normal_style))
        story.append(Spacer(1, 0.2*cm))
        
    if plan.get("water"):
        story.append(Paragraph("<b>饮水计划</b>", ParagraphStyle('Sub', parent=normal_style, textColor=C_TEXT_MAIN, spaceAfter=6)))
        for item in plan.get("water", []):
            if isinstance(item, dict):
                # 修复 3：兼容不同大模型的字段名
                time = item.get('time', item.get('period', ''))
                amount = item.get('amount', item.get('amount_ml', item.get('volume', '')))
                # 确保 amount 带单位
                if amount and not any(unit in str(amount) for unit in ['ml', 'L']):
                    amount = f"{amount}ml"
                note = item.get('note', item.get('tip', item.get('remark', item.get('description', ''))))
                clean_item = f"⏰ {time} {clean_html_tags(str(amount))} ({clean_html_tags(note)})"
            else:
                # 修复 3：如果是字符串（其他大模型直接返回文本），直接使用
                clean_item = clean_html_tags(str(item))
            story.append(Paragraph(f"<font color='#2563EB'>■</font> {clean_item}", normal_style))
        story.append(Spacer(1, 0.2*cm))

    if plan.get("exercise"):
        story.append(Paragraph("<b>运动建议</b>", ParagraphStyle('Sub', parent=normal_style, textColor=C_TEXT_MAIN, spaceAfter=6)))
        for item in plan.get("exercise", []):
            if isinstance(item, dict):
                # 修复 3：兼容不同大模型的字段名
                time = item.get('time', item.get('time_range', item.get('period', '')))
                activity = item.get('activity', item.get('type', item.get('name', '')))
                duration = item.get('duration', item.get('duration_min', item.get('time_length', '')))
                details = item.get('details', item.get('description', item.get('desc', item.get('content', ''))))
                # 确保所有字段都有值
                if activity and duration and details:
                    clean_item = f"{time} {clean_html_tags(activity)} ({clean_html_tags(duration)}): {clean_html_tags(details)}"
                elif activity and duration:
                    clean_item = f"{time} {clean_html_tags(activity)} ({clean_html_tags(duration)})"
                elif activity:
                    clean_item = f"{time} {clean_html_tags(activity)}"
                else:
                    clean_item = f"{time}"
            else:
                # 修复 3：如果是字符串（其他大模型直接返回文本），直接使用
                clean_item = clean_html_tags(str(item))
            story.append(Paragraph(f"<font color='#2563EB'>■</font> {clean_item}", normal_style))
            
    if plan.get("notes"):
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph("<b>特别关注</b>", ParagraphStyle('Sub', parent=normal_style, textColor=C_TEXT_MAIN, spaceAfter=6)))
        for item in plan.get("notes", []):
            clean_item = clean_html_tags(item)
            story.append(Paragraph(f"<font color='#F59E0B'>■</font> {clean_item}", normal_style))
    
    # ==================== 页脚 ====================
    story.append(Spacer(1, 1.5*cm))
    footer_style = ParagraphStyle('Footer', parent=normal_style, fontSize=9, textColor=C_TEXT_MUTED, alignment=TA_CENTER)
    story.append(Paragraph(f"报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", footer_style))
    story.append(Paragraph("胆结石专属健康管理 - 西西小帮手", footer_style))
    
    # 构建 PDF
    doc.build(story)
    print(f"✅ 高颜值 PDF 报告已生成：{output_path}")

if __name__ == "__main__":
    print("PDF 生成器模块，请通过 health_report_pro.py 调用")
    