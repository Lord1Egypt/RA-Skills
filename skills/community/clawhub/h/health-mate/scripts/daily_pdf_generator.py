#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PDF rendering for the daily Health-Mate report."""

import os
import re
import urllib.request
import tempfile
from functools import partial
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdf_canvas
from i18n import (
    PORTION_UNIT_PATTERN,
    condition_name,
    exercise_name,
    format_weight,
    inline_localize,
    meal_name,
    resolve_locale,
    strip_approximate_phrase,
    strip_parenthetical_details,
    t,
)

try:
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm  
    import matplotlib.patheffects as path_effects  
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("WARNING: matplotlib is not installed, so chart rendering is disabled.")

C_PRIMARY_STR = "#2563EB"
C_SUCCESS_STR = "#10B981"
C_WARNING_STR = "#F59E0B"
C_DANGER_STR  = "#EF4444"
C_TEXT_MAIN_STR = "#1E293B"
C_TEXT_MUTED_STR= "#64748B"
C_BG_HEAD_STR = "#F8FAFC"
C_BORDER_STR  = "#E2E8F0"

C_PRIMARY_LIGHT_STR = "#60A5FA" 

C_PRIMARY = HexColor(C_PRIMARY_STR)
C_SUCCESS = HexColor(C_SUCCESS_STR)
C_WARNING = HexColor(C_WARNING_STR)
C_DANGER  = HexColor(C_DANGER_STR)
C_TEXT_MAIN = HexColor(C_TEXT_MAIN_STR)
C_TEXT_MUTED= HexColor(C_TEXT_MUTED_STR)
C_BG_HEAD = HexColor(C_BG_HEAD_STR)
C_BORDER  = HexColor(C_BORDER_STR)
C_CARB, C_PROTEIN, C_FAT = "#3B82F6", "#10B981", "#F59E0B"     
FONT_DOWNLOAD_ENV = "ALLOW_RUNTIME_FONT_DOWNLOAD"
LOCAL_CJK_FONT_FILENAME = "NotoSansSC-VF.ttf"
LOCAL_JP_FONT_FILENAME = "NotoSansJP-VF.ttf"
CJK_FONT_CANDIDATES = [
    "Noto Sans CJK SC",
    "Noto Sans SC",
    "Microsoft YaHei",
    "SimHei",
    "PingFang SC",
    "Source Han Sans SC",
    "Arial Unicode MS",
]
JP_FONT_CANDIDATES = [
    "Noto Sans JP",
    "Noto Sans CJK JP",
    "Yu Gothic",
    "Meiryo",
    "MS Gothic",
    "Hiragino Sans",
    "Arial Unicode MS",
]
FONT_DOWNLOAD_SOURCES = {
    "zh-CN": "https://raw.githubusercontent.com/tankeito/Health-Mate/main/assets/NotoSansSC-VF.ttf",
    "ja-JP": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosansjp/NotoSansJP%5Bwght%5D.ttf",
}

def clean_html_tags(text):
    """Strip HTML and symbols that commonly break PDF rendering."""
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', str(text))
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    for token in ['★', '☆', '✓', '•', '|', '☑']:
        text = text.replace(token, '')
    text = re.sub(r'\*\*【', '【', text)
    text = re.sub(r'】\*\*', '】', text)
    text = re.sub(r'\*\*', '', text)
    return re.sub(r'\s+', ' ', re.sub(r'[\ufffd]', '', re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text))).strip()

def stars_to_text(stars_str):
    if not stars_str:
        return ""
    star_count = str(stars_str).count('★')
    return f'<font color="{C_WARNING_STR}">{"★" * star_count}</font>' + f'<font color="{C_BORDER_STR}">{"☆" * (5 - star_count)}</font>'


def localize_text(locale, zh_text, en_text):
    return inline_localize(locale, zh_text, en_text)


def profile_condition_title(profile, locale):
    display = str((profile or {}).get("condition_display", "") or "").strip()
    if display:
        return display
    conditions = (profile or {}).get("conditions", [])
    if isinstance(conditions, list) and conditions:
        labels = [condition_name(locale, item) for item in conditions if item]
        labels = [item for item in labels if item]
        if labels:
            separator = "、" if resolve_locale(locale=locale) in {"zh-CN", "ja-JP"} else ", "
            return separator.join(labels)
    return condition_name(locale, (profile or {}).get('condition', 'balanced'))


def simplify_food_name_for_pdf(value):
    text = strip_parenthetical_details(strip_approximate_phrase(value))
    return re.sub(r'\s+', ' ', text).strip()


def compact_number(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def build_exercise_detail_lines(exercise_data, steps, locale):
    lines = []
    for entry in exercise_data or []:
        label = exercise_name(locale, entry.get('type', 'other'))
        if entry.get('time'):
            label = f"{label} ({entry.get('time')})"

        details = []
        if entry.get('distance_km', 0) > 0:
            details.append(t(locale, 'distance_unit_km', value=compact_number(entry.get('distance_km', 0))))
        if entry.get('duration_min', 0) > 0:
            details.append(t(locale, 'minutes_unit', value=compact_number(entry.get('duration_min', 0))))
        if entry.get('calories', 0) > 0:
            details.append(t(locale, 'calories_unit', value=compact_number(entry.get('calories', 0))))

        lines.append(f"{label}: {' / '.join(details)}" if details else label)

    if steps > 0:
        lines.append(f"{t(locale, 'today_steps')}: {t(locale, 'steps_unit', value=steps)}")
    return lines

def allow_runtime_font_download():
    return str(os.environ.get(FONT_DOWNLOAD_ENV, "")).strip().lower() in {"1", "true", "yes", "on"}


def _resolve_font_locale(locale=None):
    return "ja-JP" if resolve_locale(locale=locale) == "ja-JP" else "zh-CN"


def find_system_cjk_font(locale=None):
    if not MATPLOTLIB_AVAILABLE:
        return None
    try:
        candidates = JP_FONT_CANDIDATES if _resolve_font_locale(locale) == "ja-JP" else CJK_FONT_CANDIDATES
        for candidate in candidates:
            font_path = fm.findfont(candidate, fallback_to_default=False)
            if font_path and os.path.exists(font_path):
                return font_path
    except Exception:
        return None
    return None


def get_local_cjk_font_path(locale=None):
    filename = LOCAL_JP_FONT_FILENAME if _resolve_font_locale(locale) == "ja-JP" else LOCAL_CJK_FONT_FILENAME
    return os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", filename))


def has_local_cjk_font(locale=None):
    return os.path.exists(get_local_cjk_font_path(locale))


def register_chinese_font(locale=None):
    font_locale = _resolve_font_locale(locale)
    font_alias = "Japanese" if font_locale == "ja-JP" else "Chinese"
    try:
        pdfmetrics.getFont(font_alias)
        return font_alias
    except Exception:
        pass
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "..", "assets")
    local_ttf = get_local_cjk_font_path(font_locale)

    if os.path.exists(local_ttf):
        try:
            pdfmetrics.registerFont(TTFont(font_alias, local_ttf))
            return font_alias
        except Exception:
            pass

    builtin_cid = "HeiseiKakuGo-W5" if font_locale == "ja-JP" else "STSong-Light"
    try:
        pdfmetrics.registerFont(UnicodeCIDFont(builtin_cid))
        return builtin_cid
    except Exception:
        pass

    system_font = find_system_cjk_font(font_locale)
    if system_font:
        try:
            pdfmetrics.registerFont(TTFont(font_alias, system_font))
            return font_alias
        except Exception:
            pass

    if allow_runtime_font_download():
        try:
            if not os.path.exists(assets_dir):
                os.makedirs(assets_dir, exist_ok=True)
            with urllib.request.urlopen(FONT_DOWNLOAD_SOURCES[font_locale], timeout=15) as response:
                with open(local_ttf, 'wb') as f:
                    f.write(response.read())
            pdfmetrics.registerFont(TTFont(font_alias, local_ttf))
            return font_alias
        except Exception:
            pass
    return 'Helvetica'

def get_font_prop(locale=None):
    preferred_locales = [_resolve_font_locale(locale), "zh-CN", "ja-JP"]
    seen = set()
    ordered_locales = []
    for item in preferred_locales:
        if item not in seen:
            ordered_locales.append(item)
            seen.add(item)

    for font_locale in ordered_locales:
        local_ttf = get_local_cjk_font_path(font_locale)
        if os.path.exists(local_ttf):
            return fm.FontProperties(fname=local_ttf)
        system_font = find_system_cjk_font(font_locale)
        if system_font:
            return fm.FontProperties(fname=system_font)
    return None


def _style_matplotlib_text(text_obj, font_prop=None, *, color=None, fontsize=None, fontweight="bold"):
    resolved_color = color if color is not None else text_obj.get_color()
    if color is not None:
        text_obj.set_color(color)
    if fontsize is not None:
        text_obj.set_fontsize(fontsize)
    if font_prop:
        text_obj.set_fontproperties(font_prop)
    if fontweight:
        text_obj.set_fontweight(fontweight)
    outline_color = C_TEXT_MAIN_STR if str(resolved_color).lower() in {"#ffffff", "white"} else "white"
    text_obj.set_path_effects([path_effects.withStroke(linewidth=1.0, foreground=outline_color, alpha=0.65)])


def _apply_axis_tick_style(ax, font_prop=None, *, x_color=C_TEXT_MAIN_STR, y_color=C_TEXT_MAIN_STR, fontsize=8):
    for label in ax.get_xticklabels():
        _style_matplotlib_text(label, font_prop, color=x_color, fontsize=fontsize)
    for label in ax.get_yticklabels():
        _style_matplotlib_text(label, font_prop, color=y_color, fontsize=fontsize)


class NumberedCanvas(pdf_canvas.Canvas):
    """Canvas with a consistent footer and page numbering."""

    def __init__(self, *args, footer_brand="Generated by Health-Mate", footer_font_name="Helvetica", footer_margin=2 * cm, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []
        self._footer_brand = footer_brand
        self._footer_font_name = footer_font_name or "Helvetica"
        self._footer_margin = footer_margin

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(page_count)
            super().showPage()
        super().save()

    def _draw_footer(self, page_count):
        self.saveState()
        page_width, _ = self._pagesize
        line_y = 0.95 * cm
        text_y = 0.56 * cm
        self.setStrokeColor(HexColor(C_BORDER_STR))
        self.setLineWidth(0.45)
        self.line(self._footer_margin, line_y, page_width - self._footer_margin, line_y)

        try:
            self.setFont(self._footer_font_name, 8.2)
        except Exception:
            self.setFont("Helvetica", 8.2)
        self.setFillColor(HexColor(C_TEXT_MUTED_STR))
        self.drawCentredString(page_width / 2, text_y, self._footer_brand)
        self.drawRightString(page_width - self._footer_margin, text_y, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def build_numbered_canvasmaker(font_name, footer_brand="Generated by Health-Mate", footer_margin=2 * cm):
    return partial(
        NumberedCanvas,
        footer_brand=footer_brand,
        footer_font_name=font_name,
        footer_margin=footer_margin,
    )


class StatusBadge(Flowable):
    """Rounded status label for score tables."""

    def __init__(self, text, fill_color, font_name="Helvetica", max_width=3.2 * cm, height=0.7 * cm):
        super().__init__()
        self.text = clean_html_tags(text)
        self.fill_color = fill_color
        self.font_name = font_name or "Helvetica"
        self.font_size = 8.2
        self.height = height
        self.width = min(
            max(pdfmetrics.stringWidth(self.text or "OK", self.font_name, self.font_size) + 0.72 * cm, 1.7 * cm),
            max_width,
        )

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.fill_color)
        self.canv.roundRect(0, 0, self.width, self.height, self.height / 2, stroke=0, fill=1)
        self.canv.setFillColor(colors.white)
        try:
            self.canv.setFont(self.font_name, self.font_size)
        except Exception:
            self.canv.setFont("Helvetica-Bold", self.font_size)
        x = self.width / 2
        y = (self.height - self.font_size) / 2 + 1.8
        for dx, dy in ((0, 0), (0.16, 0), (-0.16, 0), (0, 0.12)):
            self.canv.drawCentredString(x + dx, y + dy, self.text)
        self.canv.restoreState()


class MicroProgressBar(Flowable):
    """Thin progress indicator for nutrition tables."""

    def __init__(self, ratio, fill_color, label, font_name="Helvetica", width=3.6 * cm, height=0.72 * cm):
        super().__init__()
        self.ratio = max(0.0, float(ratio or 0))
        self.fill_color = fill_color
        self.label = clean_html_tags(label)
        self.font_name = font_name or "Helvetica"
        self.font_size = 7.8
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        bar_y = 0.12 * cm
        bar_height = 0.16 * cm
        self.canv.saveState()
        try:
            self.canv.setFont(self.font_name, self.font_size)
        except Exception:
            self.canv.setFont("Helvetica-Bold", self.font_size)
        self.canv.setFillColor(HexColor(C_TEXT_MAIN_STR))
        self.canv.drawRightString(self.width, self.height - self.font_size + 1.2, self.label)

        self.canv.setFillColor(HexColor("#E5E7EB"))
        self.canv.roundRect(0, bar_y, self.width, bar_height, bar_height / 2, stroke=0, fill=1)
        self.canv.setFillColor(self.fill_color)
        filled_width = self.width * min(self.ratio, 1.0)
        if filled_width > 0:
            self.canv.roundRect(0, bar_y, filled_width, bar_height, bar_height / 2, stroke=0, fill=1)
        self.canv.restoreState()


def get_score_color(score):
    if score >= 80:
        return C_SUCCESS
    if score >= 60:
        return C_WARNING
    return C_DANGER


def split_sentences_for_report(text):
    if not text:
        return []
    raw_parts = re.split(r'(?<=[。！？!?;；])\s*', clean_html_tags(text))
    return [part.strip(" -\n\t") for part in raw_parts if part.strip(" -\n\t")]


def build_ai_comment_sections(comment_text, locale):
    lines = []
    for line in str(comment_text or "").splitlines():
        clean = clean_html_tags(line).strip()
        lowered = clean.lower()
        if (
            not clean
            or clean.startswith(("[plugins]", "[adp-", "[qqbot-", "[openclaw", "Hint:", "error:"))
            or "plugin registration complete" in lowered
            or "registering tool factory:" in lowered
            or "registered qqbot remind tool" in lowered
            or "no qqbot accounts configured, skipping" in lowered
        ):
            continue
        lines.append(clean)

    sections = []
    current = None
    heading_tokens = ("做得", "关注", "隐患", "建议", "提醒", "亮点", "风险", "Good", "Attention", "Risk", "Focus")
    for line in lines:
        normalized = line.strip("*：: ")
        if line.startswith(("【", "✅", "⚠", "1.", "2.")) or any(token in normalized for token in heading_tokens):
            current = {"title": normalized.rstrip("：:"), "items": []}
            sections.append(current)
            continue
        if current is None:
            current = {"title": "", "items": []}
            sections.append(current)
        bullet = normalized.lstrip("-•")
        if bullet:
            current["items"].append(bullet.strip())

    if sections and any(section.get("title") for section in sections):
        structured = []
        for section in sections:
            items = section.get("items", [])
            if not items and section.get("title"):
                structured.append({"title": section["title"], "items": []})
            elif items:
                structured.append({"title": section.get("title", ""), "items": items})
        if structured:
            return structured

    sentences = split_sentences_for_report("\n".join(lines))
    positives, risks = [], []
    positive_tokens = ("达标", "完成", "很好", "稳定", "合格", "友好", "good", "well", "stable", "met", "achieved")
    for sentence in sentences:
        target = positives if any(token.lower() in sentence.lower() for token in positive_tokens) else risks
        target.append(sentence)
    if not positives and sentences:
        positives = sentences[:1]
        risks = sentences[1:]
    title_good = "做得很好的地方" if locale == "zh-CN" else "What Went Well"
    title_risk = "需要关注的隐患" if locale == "zh-CN" else "Watchouts"
    sections = []
    if positives:
        sections.append({"title": title_good, "items": positives})
    if risks:
        sections.append({"title": title_risk, "items": risks})
    return sections


def classify_nutrition_progress(metric_key, actual, target):
    actual = float(actual or 0)
    target = float(target or 0)
    ratio = actual / target if target > 0 else 0
    if metric_key in {"protein", "fiber"}:
        if ratio >= 1:
            return ratio, C_SUCCESS, "good"
        if ratio >= 0.75:
            return ratio, C_WARNING, "warning"
        return ratio, C_DANGER, "bad"
    if metric_key in {"fat", "calories"}:
        if 0.85 <= ratio <= 1.05:
            return ratio, C_SUCCESS, "good"
        if 0.7 <= ratio < 0.85 or 1.05 < ratio <= 1.2:
            return ratio, C_WARNING, "warning"
        return ratio, C_DANGER, "bad"
    if 0.9 <= ratio <= 1.1:
        return ratio, C_SUCCESS, "good"
    if 0.75 <= ratio < 0.9 or 1.1 < ratio <= 1.2:
        return ratio, C_WARNING, "warning"
    return ratio, C_DANGER, "bad"

def create_nutrition_chart(nutrition, locale):
    if not MATPLOTLIB_AVAILABLE: return None
    try:
        locale = resolve_locale(locale=locale)
        my_font = get_font_prop(locale)
        carb_kcal, protein_kcal, fat_kcal = nutrition.get('carb', 0)*4, nutrition.get('protein', 0)*4, nutrition.get('fat', 0)*9
        if carb_kcal + protein_kcal + fat_kcal <= 0: return None
        
        fig, ax = plt.subplots(figsize=(5.2, 3.25), subplot_kw=dict(aspect="equal"))
        _, texts, autotexts = ax.pie(
            [carb_kcal, protein_kcal, fat_kcal],
            labels=[t(locale, 'carb'), t(locale, 'protein'), t(locale, 'fat')],
            colors=[C_CARB, C_PROTEIN, C_FAT],
            autopct='%1.1f%%',
            pctdistance=0.78,
            labeldistance=1.18,
            startangle=90,
            wedgeprops=dict(width=0.42, edgecolor='w'),
        )
        for label_text in texts:
            _style_matplotlib_text(label_text, my_font, color=C_TEXT_MAIN_STR, fontsize=9.2)
        for at in autotexts:
            at.set_color("#FFFFFF")
            at.set_fontsize(8.0)
            at.set_fontweight("bold")
            at.set_path_effects([path_effects.withStroke(linewidth=2.2, foreground="black")])
            if my_font: at.set_fontproperties(my_font)
            
        center_text = ax.text(
            0,
            0,
            t(locale, 'nutrition_chart_center', calories=int(nutrition.get('calories', 0))),
            ha='center',
            va='center',
            fontsize=10.6,
            fontweight='bold',
            color=C_TEXT_MAIN_STR,
        )
        _style_matplotlib_text(center_text, my_font, color=C_TEXT_MAIN_STR, fontsize=10.6, fontweight="bold")
        plt.tight_layout(pad=1.0)
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_img.name, transparent=True, dpi=200)
        plt.close(fig)
        return temp_img.name
    except Exception:
        return None


def create_meal_macro_stacked_chart(meals, locale):
    if not MATPLOTLIB_AVAILABLE or not meals:
        return None
    try:
        locale = resolve_locale(locale=locale)
        my_font = get_font_prop(locale)
        meal_order = {
            "breakfast": 0,
            "morning_snack": 1,
            "lunch": 2,
            "afternoon_snack": 3,
            "dinner": 4,
            "evening_snack": 5,
            "snack": 6,
        }
        filtered = [
            meal for meal in meals
            if sum(float(meal.get(key, 0) or 0) for key in ("total_protein", "total_fat", "total_carb")) > 0
        ]
        if not filtered:
            return None
        filtered = sorted(filtered, key=lambda meal: (meal_order.get(meal.get("type", ""), 99), meal.get("time", "")))
        labels = [meal_name(locale, meal.get("type", "")) for meal in filtered]
        protein_kcal = []
        fat_kcal = []
        carb_kcal = []
        totals = []
        for meal in filtered:
            raw_carb_kcal = float(meal.get("total_carb", 0) or 0) * 4
            raw_protein_kcal = float(meal.get("total_protein", 0) or 0) * 4
            raw_fat_kcal = float(meal.get("total_fat", 0) or 0) * 9
            macro_total_kcal = raw_carb_kcal + raw_protein_kcal + raw_fat_kcal
            reported_total_kcal = float(meal.get("total_calories", 0) or 0)
            display_total_kcal = reported_total_kcal if reported_total_kcal > 0 else macro_total_kcal
            scale_ratio = (display_total_kcal / macro_total_kcal) if macro_total_kcal > 0 else 1.0

            carb_kcal.append(raw_carb_kcal * scale_ratio)
            protein_kcal.append(raw_protein_kcal * scale_ratio)
            fat_kcal.append(raw_fat_kcal * scale_ratio)
            totals.append(display_total_kcal)

        fig, ax = plt.subplots(figsize=(7.6, 3.45))
        fig.patch.set_alpha(0)
        x = list(range(len(labels)))
        bars_carb = ax.bar(x, carb_kcal, color=C_CARB, width=0.58, label=t(locale, "carb"))
        bars_protein = ax.bar(x, protein_kcal, bottom=carb_kcal, color=C_PROTEIN, width=0.58, label=t(locale, "protein"))
        bars_fat = ax.bar(
            x,
            fat_kcal,
            bottom=[carb + protein for carb, protein in zip(carb_kcal, protein_kcal)],
            color=C_FAT,
            width=0.58,
            label=t(locale, "fat"),
        )

        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=8.6, color=C_TEXT_MAIN_STR)
        ylabel = ax.set_ylabel("kcal", color=C_TEXT_MAIN_STR)
        ax.tick_params(axis="y", colors=C_TEXT_MAIN_STR, labelsize=8.2)
        ax.grid(axis="y", linestyle="--", alpha=0.35, color=C_BORDER_STR)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(C_BORDER_STR)
        ax.spines["bottom"].set_color(C_BORDER_STR)
        _apply_axis_tick_style(ax, my_font, fontsize=8.4)
        _style_matplotlib_text(ylabel, my_font, color=C_TEXT_MAIN_STR, fontsize=8.5)

        max_total = max(totals) if totals else 0
        for idx, total in enumerate(totals):
            if total <= 0:
                continue
            total_label = ax.annotate(
                f"{int(round(total))}",
                xy=(idx, total),
                xytext=(0, 8),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.3,
                color=C_TEXT_MAIN_STR,
                fontweight="bold",
                clip_on=False,
            )
            _style_matplotlib_text(total_label, my_font, color=C_TEXT_MAIN_STR, fontsize=8.3)

        ax.set_ylim(0, max_total * 1.16 + 18)
        legend_kwargs = {
            "loc": "upper right",
            "bbox_to_anchor": (1.0, 1.16),
            "frameon": False,
            "ncol": 3,
            "columnspacing": 1.0,
            "handletextpad": 0.5,
            "borderaxespad": 0.0,
        }
        if my_font:
            legend_kwargs["prop"] = my_font
        legend = ax.legend(handles=[bars_carb, bars_protein, bars_fat], **legend_kwargs)
        for legend_text in legend.get_texts():
            _style_matplotlib_text(legend_text, my_font, color=C_TEXT_MAIN_STR, fontsize=8.2)

        plt.tight_layout(rect=(0, 0, 1, 0.94), pad=1.0)
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(temp_img.name, transparent=True, dpi=190)
        plt.close(fig)
        return temp_img.name
    except Exception as exc:
        print(f"WARNING: meal macro chart generation failed: {exc}")
        return None

def create_water_chart(water_records, target_ml, locale):
    if not MATPLOTLIB_AVAILABLE or not water_records: return None
    try:
        locale = resolve_locale(locale=locale)
        my_font = get_font_prop(locale)
        total_drank = sum([int(r.get('amount_ml', 0)) for r in water_records])
        target = target_ml if target_ml > 0 else 2000
        remaining = max(0, target - total_drank)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3), gridspec_kw={'width_ratios': [1, 1.5]})
        vibrant_colors = ["#4A90E2", "#50E3C2", "#F5A623", "#F8E71C", "#FF4081", "#00BCD4", "#9013FE"]
        if total_drank == 0: 
            ax1.pie([1], colors=[C_BORDER_STR], startangle=90, wedgeprops=dict(width=0.3, edgecolor='w'))
        else: 
            amounts_circle = [int(r.get('amount_ml', 0)) for r in water_records]
            sizes = amounts_circle + ([remaining] if remaining > 0 else [])
            c_list = [vibrant_colors[i % len(vibrant_colors)] for i in range(len(amounts_circle))]
            if remaining > 0: c_list.append(C_BORDER_STR)
            ax1.pie(sizes, colors=c_list, startangle=90, wedgeprops=dict(width=0.3, edgecolor='w', linewidth=1.5))
            
        t_center = ax1.text(0, 0, t(locale, 'water_chart_center', current=total_drank, target=target), ha='center', va='center', fontsize=11.2, fontweight='bold', color=C_TEXT_MAIN_STR)
        _style_matplotlib_text(t_center, my_font, color=C_TEXT_MAIN_STR, fontsize=11.2)
        hours = [0, 3, 6, 9, 12, 15, 18, 21, 24]
        ax2.set_xticks(hours)
        ax2.set_xticklabels(['0', '3', '6', '9', '12', '15', '18', '21', '0'])
        ax2.set_xlim(-1, 25) 
        
        bins = {} 
        for r in water_records:
            exact = r.get('exact_time', '')
            if exact:
                try:
                    h, m = map(int, exact.split(':'))
                    pos = h + m/60.0
                except: pos = -1
            else:
                mapping = {'wake_up': 7, 'morning': 10, 'noon': 12.5, 'afternoon': 16, 'evening': 20}
                pos = mapping.get(r.get('time_label', ''), -1)
            
            if pos >= 0:
                bin_key = round(pos / 1.5) * 1.5
                if bin_key not in bins: bins[bin_key] = []
                bins[bin_key].append(int(r.get('amount_ml', 0)))
                
        max_y = 0
        for bin_pos, amounts in bins.items():
            current_bottom = 0
            colors_stack = [C_PRIMARY_STR, C_PRIMARY_LIGHT_STR]
            for i, amt in enumerate(amounts):
                color = colors_stack[i % 2]
                bars = ax2.bar(bin_pos, amt, bottom=current_bottom, color=color, width=1.2, alpha=0.9, edgecolor='w', linewidth=0.5)
                
                if len(amounts) == 1:
                    t_bar = ax2.text(bin_pos, current_bottom + amt + 15, f"{amt}", ha='center', va='bottom', fontsize=8.2, color=C_TEXT_MAIN_STR, fontweight='bold')
                else:
                    t_bar = ax2.text(bin_pos + 0.8, current_bottom + amt/2, f"{amt}", ha='left', va='center', fontsize=8.2, color=C_TEXT_MAIN_STR, fontweight='bold')
                _style_matplotlib_text(t_bar, my_font, color=C_TEXT_MAIN_STR, fontsize=8.2)
                current_bottom += amt
            
            if len(amounts) > 1:
                t_total = ax2.text(bin_pos, current_bottom + 15, t(locale, 'water_chart_total', amount=current_bottom), ha='center', va='bottom', fontsize=8, color=C_TEXT_MAIN_STR, fontweight='bold')
                _style_matplotlib_text(t_total, my_font, color=C_TEXT_MAIN_STR, fontsize=8)
            
            max_y = max(max_y, current_bottom)
        
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.spines['left'].set_visible(True)
        ax2.spines['left'].set_color(C_BORDER_STR)
        ax2.spines['bottom'].set_color(C_BORDER_STR)
        
        if max_y == 0:
            y_limit, step = 500, 100
        else:
            y_limit = int(max_y * 1.2)
            step = max(100, int((max_y / 5) / 100) * 100)
            
        ax2.set_yticks(range(step, y_limit + step, step))
        ax2.set_ylim(0, max_y + (step if max_y < 800 else max_y * 0.3))
        
        ax2.tick_params(axis='y', labelleft=True, colors=C_TEXT_MAIN_STR, labelsize=8)
        ax2.tick_params(axis='x', colors=C_TEXT_MAIN_STR)
        ax2.yaxis.grid(True, linestyle='--', alpha=0.4, color=C_BORDER_STR)
        _apply_axis_tick_style(ax2, my_font, x_color=C_TEXT_MAIN_STR, y_color=C_TEXT_MAIN_STR, fontsize=8)

        plt.tight_layout()
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_img.name, transparent=True, dpi=150)
        plt.close(fig)
        return temp_img.name
    except Exception as e:
        print(f"WARNING: water chart generation failed: {e}")
        return None


def create_energy_balance_chart(nutrition, exercise_data, steps, step_target, resting_burn, locale):
    if not MATPLOTLIB_AVAILABLE:
        return None
    try:
        locale = resolve_locale(locale=locale)
        my_font = get_font_prop(locale)
        intake = float((nutrition or {}).get("calories", 0) or 0)
        exercise_burn = sum(float(entry.get("calories", 0) or 0) for entry in (exercise_data or []) if isinstance(entry, dict))
        step_burn = max(0.0, float(steps or 0) * 0.035)
        active_burn = exercise_burn + step_burn
        total_burn = float(resting_burn or 0) + active_burn
        if max(intake, total_burn, steps or 0) <= 0:
            return None

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.9), gridspec_kw={"width_ratios": [1.9, 1.0]})
        fig.patch.set_alpha(0)

        ax1.barh([1], [intake], color=C_PRIMARY_STR, height=0.34)
        ax1.barh([0], [resting_burn], color="#BFDBFE", height=0.34)
        ax1.barh([0], [active_burn], left=[resting_burn], color=C_SUCCESS_STR, height=0.34)

        ax1.set_yticks([0, 1])
        ax1.set_yticklabels([
            localize_text(locale, "预计消耗", "Estimated burn"),
            localize_text(locale, "实际摄入", "Intake"),
        ])
        ax1.tick_params(axis="x", colors=C_TEXT_MAIN_STR, labelsize=7.8)
        ax1.tick_params(axis="y", colors=C_TEXT_MAIN_STR, length=0, pad=8)
        ax1.grid(axis="x", linestyle="--", alpha=0.3, color=C_BORDER_STR)
        ax1.spines["top"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["left"].set_visible(False)
        ax1.spines["bottom"].set_color(C_BORDER_STR)
        _apply_axis_tick_style(ax1, my_font, fontsize=7.9)
        axis_upper = max(total_burn, intake) * 1.28 + 40
        ax1.set_xlim(0, axis_upper)

        intake_text = ax1.text(intake + max(total_burn, intake) * 0.04, 1, f"{int(round(intake))} kcal", va="center", ha="left", fontsize=7.9, color=C_TEXT_MAIN_STR, fontweight="bold", clip_on=False)
        burn_text = ax1.text(total_burn + max(total_burn, intake) * 0.04, 0, f"{int(round(total_burn))} kcal", va="center", ha="left", fontsize=7.9, color=C_TEXT_MAIN_STR, fontweight="bold", clip_on=False)
        detail_text = ax1.text(
            0,
            -0.48,
            localize_text(
                locale,
                f"静息 {int(round(resting_burn))} kcal + 活动 {int(round(active_burn))} kcal",
                f"Resting {int(round(resting_burn))} kcal + active {int(round(active_burn))} kcal",
            ),
            ha="left",
            va="center",
            fontsize=7.7,
            color=C_TEXT_MUTED_STR,
        )
        delta_value = total_burn - intake
        delta_text = ax1.text(
            0,
            1.56,
            localize_text(
                locale,
                f"能量差：{'-' if delta_value >= 0 else '+'}{abs(int(round(delta_value)))} kcal",
                f"Energy gap: {'-' if delta_value >= 0 else '+'}{abs(int(round(delta_value)))} kcal",
            ),
            ha="left",
            va="center",
            fontsize=8.0,
            color=C_SUCCESS_STR if delta_value >= 0 else C_WARNING_STR,
            fontweight="bold",
        )
        for text_obj, color in (
            (intake_text, C_TEXT_MAIN_STR),
            (burn_text, C_TEXT_MAIN_STR),
            (detail_text, C_TEXT_MUTED_STR),
            (delta_text, C_SUCCESS_STR if delta_value >= 0 else C_WARNING_STR),
        ):
            _style_matplotlib_text(text_obj, my_font, color=color, fontsize=text_obj.get_fontsize())

        legend_kwargs = {
            "handles": [
                plt.Rectangle((0, 0), 1, 1, color=C_PRIMARY_STR),
                plt.Rectangle((0, 0), 1, 1, color="#BFDBFE"),
                plt.Rectangle((0, 0), 1, 1, color=C_SUCCESS_STR),
            ],
            "labels": [
                localize_text(locale, "摄入热量", "Intake"),
                localize_text(locale, "静息消耗", "Resting burn"),
                localize_text(locale, "活动消耗", "Active burn"),
            ],
            "loc": "upper right",
            "bbox_to_anchor": (1.0, 1.18),
            "frameon": False,
            "ncol": 3,
            "fontsize": 7.2,
            "columnspacing": 1.0,
            "handletextpad": 0.5,
            "borderaxespad": 0.0,
        }
        if my_font:
            legend_kwargs["prop"] = my_font
        legend = ax1.legend(**legend_kwargs)
        for legend_text in legend.get_texts():
            _style_matplotlib_text(legend_text, my_font, color=C_TEXT_MAIN_STR, fontsize=7.2)

        safe_target = max(int(step_target or 0), 1)
        step_progress = max(0.0, min(float(steps or 0) / safe_target, 1.0))
        ax2.pie(
            [step_progress, max(1.0 - step_progress, 0.0)],
            startangle=90,
            counterclock=False,
            colors=[C_SUCCESS_STR if step_progress >= 1 else C_PRIMARY_STR, C_BORDER_STR],
            wedgeprops=dict(width=0.26, edgecolor="white", linewidth=2),
        )
        step_center = ax2.text(
            0,
            0.08,
            localize_text(locale, f"{int(steps or 0)}", f"{int(steps or 0)}"),
            ha="center",
            va="center",
            fontsize=14.2,
            color=C_TEXT_MAIN_STR,
            fontweight="bold",
        )
        step_sub = ax2.text(
            0,
            -0.22,
            localize_text(locale, f"/ {safe_target} 步", f"/ {safe_target} steps"),
            ha="center",
            va="center",
            fontsize=8.0,
            color=C_TEXT_MUTED_STR,
        )
        step_label = ax2.text(
            0,
            1.14,
            localize_text(locale, "步数进度", "Step progress"),
            ha="center",
            va="center",
            fontsize=8.6,
            color=C_TEXT_MAIN_STR,
            fontweight="bold",
        )
        for text_obj, color in (
            (step_center, C_TEXT_MAIN_STR),
            (step_sub, C_TEXT_MUTED_STR),
            (step_label, C_TEXT_MAIN_STR),
        ):
            _style_matplotlib_text(text_obj, my_font, color=color, fontsize=text_obj.get_fontsize())
        ax2.set(aspect="equal")
        ax2.axis("off")

        plt.tight_layout(rect=(0, 0, 1, 0.93), pad=1.05, w_pad=1.45)
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        plt.savefig(temp_img.name, transparent=True, dpi=210)
        plt.close(fig)
        return temp_img.name
    except Exception as exc:
        print(f"WARNING: energy balance chart generation failed: {exc}")
        return None

def create_exercise_chart(exercise_data, steps, step_target=8000, locale="zh-CN"):
    if not MATPLOTLIB_AVAILABLE: return None
    try:
        locale = resolve_locale(locale=locale)
        my_font = get_font_prop(locale)
        labels, calories, targets, is_step, inner_texts = [], [], [], [], []
        
        if exercise_data:
            for e in exercise_data:
                ex_type = exercise_name(locale, e.get('type', 'other'))
                dist = e.get('distance_km', 0)
                dur = e.get('duration_min', 0)
                
                labels.append(ex_type)
                
                in_str = []
                if dist > 0: in_str.append(t(locale, 'distance_unit_km', value=dist))
                if dur > 0: in_str.append(f"({t(locale, 'minutes_unit', value=dur)})")
                inner_texts.append(" ".join(in_str))
                
                calories.append(e.get('calories', 0))
                targets.append(None) 
                is_step.append(False)
                
        if steps > 0:
            labels.append(t(locale, 'today_steps'))
            calories.append(steps)
            targets.append(step_target) 
            is_step.append(True)
            inner_texts.append("")
            
        if not labels or sum(calories) == 0: return None
            
        fig_height = max(1.2, len(labels) * 0.6 + 0.5)
        fig, ax = plt.subplots(figsize=(7, fig_height))
        y_pos = range(len(labels))
        chart_color = "#20D091" 
        track_color = "#F1F5F9"
        step_color = "#3B82F6" 
        
        max_bg = max(step_target, steps) if steps > 0 else 100
        
        for i, (label, cal, tgt, is_s, in_txt) in enumerate(zip(labels, calories, targets, is_step, inner_texts)):
            if is_s:
                ax.plot([0, max_bg], [i, i], color=track_color, linewidth=12, solid_capstyle='round', zorder=1)
                ax.plot([0, cal], [i, i], color=step_color, linewidth=12, solid_capstyle='round', zorder=2)
                text_str = t(locale, 'step_progress', current=int(cal), target=int(tgt))
                t_val = ax.text(max_bg * 1.05, i, text_str, ha='left', va='center', fontsize=9, color=C_TEXT_MAIN_STR, fontweight='bold', zorder=3)
            else:
                ax.plot([0, max_bg], [i, i], color=chart_color, linewidth=12, solid_capstyle='round', zorder=1)
                if in_txt:
                    t_in = ax.text(max_bg * 0.02, i, in_txt, ha='left', va='center', fontsize=9, color=C_TEXT_MAIN_STR, fontweight='bold', zorder=3)
                    _style_matplotlib_text(t_in, my_font, color=C_TEXT_MAIN_STR, fontsize=9)
                text_str = t(locale, 'calories_unit', value=int(cal))
                t_val = ax.text(max_bg * 1.05, i, text_str, ha='left', va='center', fontsize=9, color=C_TEXT_MAIN_STR, fontweight='bold', zorder=3)

            _style_matplotlib_text(t_val, my_font, color=C_TEXT_MAIN_STR, fontsize=9)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.invert_yaxis()  
        ax.set_ylim(len(labels) - 0.5, -0.5)
        ax.set_xlim(0, max_bg * 1.35)
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.tick_params(axis='y', colors=C_TEXT_MAIN_STR, length=0, pad=10) 
        ax.tick_params(axis='x', bottom=False, labelbottom=False) 
        _apply_axis_tick_style(ax, my_font, x_color=C_TEXT_MAIN_STR, y_color=C_TEXT_MAIN_STR, fontsize=9)

        plt.tight_layout()
        temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        plt.savefig(temp_img.name, transparent=True, dpi=150)
        plt.close(fig)
        return temp_img.name
    except Exception as e:
        print(f"WARNING: exercise chart generation failed: {e}")
        return None

class GradientBanner(Flowable):
    """A decorative gradient banner for report headers."""
    def __init__(self, width, height=0.35*cm, color_left="#2563EB", color_right="#60A5FA"):
        super().__init__()
        self.width = width
        self.height = height
        self.color_left = HexColor(color_left)
        self.color_right = HexColor(color_right)

    def wrap(self, availWidth, availHeight):
        self.width = min(self.width, availWidth)
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        steps = 60
        step_w = self.width / steps
        r1, g1, b1 = self.color_left.red, self.color_left.green, self.color_left.blue
        r2, g2, b2 = self.color_right.red, self.color_right.green, self.color_right.blue
        for i in range(steps):
            t = i / steps
            r = r1 + (r2 - r1) * t
            g = g1 + (g2 - g1) * t
            b = b1 + (b2 - b1) * t
            self.canv.setFillColorRGB(r, g, b)
            self.canv.rect(i * step_w, 0, step_w + 0.5, self.height, stroke=0, fill=1)
        self.canv.restoreState()


class AccentHeading(Flowable):
    """Section heading with colored left accent bar."""
    def __init__(self, text, font_name="Helvetica", font_size=13, accent_color="#2563EB", text_color="#1E293B"):
        super().__init__()
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        self.accent_color = HexColor(accent_color)
        self.text_color = HexColor(text_color)
        self.bar_width = 4
        self.padding_left = 10
        self.height = font_size + 12

    def wrap(self, availWidth, availHeight):
        self.width = availWidth
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        # Draw accent bar
        self.canv.setFillColor(self.accent_color)
        self.canv.roundRect(0, 0, self.bar_width, self.height, 1.5, stroke=0, fill=1)
        # Draw text
        self.canv.setFillColor(self.text_color)
        try:
            self.canv.setFont(self.font_name, self.font_size)
        except:
            self.canv.setFont("Helvetica-Bold", self.font_size)
        self.canv.drawString(self.bar_width + self.padding_left, (self.height - self.font_size) / 2 + 2, self.text)
        self.canv.restoreState()


class SummaryCard(Flowable):
    """A KPI summary card with value and label."""
    def __init__(self, label, value, sub_text="", color="#2563EB", font_name="Helvetica", width=3.8*cm, height=2.2*cm):
        super().__init__()
        self.label = clean_html_tags(label)
        self.value = clean_html_tags(str(value))
        self.sub_text = clean_html_tags(sub_text)
        self.color = color if isinstance(color, Color) else HexColor(color)
        self.font_name = font_name
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        # Card background
        self.canv.setFillColor(HexColor("#F8FAFC"))
        self.canv.setStrokeColor(HexColor("#E2E8F0"))
        self.canv.setLineWidth(0.5)
        self.canv.roundRect(0, 0, self.width, self.height, 6, stroke=1, fill=1)
        # Top accent line
        self.canv.setFillColor(self.color)
        self.canv.roundRect(0, self.height - 3, self.width, 3, 1.5, stroke=0, fill=1)
        # Value text
        self.canv.setFillColor(self.color)
        try:
            self.canv.setFont(self.font_name, 16)
        except:
            self.canv.setFont("Helvetica-Bold", 16)
        self.canv.drawCentredString(self.width / 2, self.height / 2 + 2, self.value)
        # Label
        self.canv.setFillColor(HexColor("#1E293B"))
        try:
            self.canv.setFont(self.font_name, 8.5)
        except:
            self.canv.setFont("Helvetica", 8.5)
        self.canv.drawCentredString(self.width / 2, self.height / 2 - 14, self.label)
        # Sub text
        if self.sub_text:
            self.canv.setFillColor(HexColor("#475569"))
            try:
                self.canv.setFont(self.font_name, 7)
            except:
                self.canv.setFont("Helvetica", 7)
            self.canv.drawCentredString(self.width / 2, 6, self.sub_text)
        self.canv.restoreState()


def generate_pdf_report(data, profile, scores, nutrition, macros, risks, plan, output_path, locale="zh-CN", water_records=None, meals=None, exercise_data=None, ai_comment=None, medication_records=None, custom_sections=None, generation_meta=None):
    locale = resolve_locale(locale=locale)
    font_name = register_chinese_font(locale)
    footer_text = f"{profile_condition_title(profile, locale)} - Health-Mate"
    render_notice = str(((generation_meta or {}).get("render_notice")) or data.get("render_notice") or "").strip()

    def localize(zh_text, en_text):
        return inline_localize(locale, zh_text, en_text)

    def source_text(source):
        labels = {
            'llm': localize('\u6765\u6e90\uff1aLLM \u52a8\u6001\u751f\u6210', 'Source: LLM generated'),
            'fallback': localize('\u6765\u6e90\uff1a\u672c\u5730\u89c4\u5219', 'Source: local rules'),
            'fallback_tavily': localize('\u6765\u6e90\uff1aTavily \u68c0\u7d22 + \u672c\u5730\u89c4\u5219', 'Source: Tavily retrieval + local rules'),
            'local': localize('\u6765\u6e90\uff1a\u672c\u5730\u89c4\u5219', 'Source: local rules'),
        }
        return labels.get(source or 'local', labels['local'])

    module_map = scores.get('module_map', {}) if isinstance(scores, dict) else {}
    score_modules = scores.get('modules', []) if isinstance(scores, dict) else []

    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm, title=t(locale, 'daily_report_title'))
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=22, textColor=C_PRIMARY, spaceAfter=6, alignment=TA_CENTER, fontName=font_name, leading=28)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=13, textColor=C_PRIMARY, spaceBefore=18, spaceAfter=12, fontName=font_name)
    normal_style = ParagraphStyle('CustomNormal', parent=styles['Normal'], fontSize=10, textColor=C_TEXT_MAIN, fontName=font_name, leading=15)
    normal_bold_style = ParagraphStyle('CustomNormalBold', parent=normal_style, fontSize=10, leading=15)
    muted_style = ParagraphStyle('Muted', parent=normal_style, textColor=C_TEXT_MUTED, fontSize=8, leading=11)
    card_title_style = ParagraphStyle('CardTitle', parent=normal_style, fontSize=10.5, textColor=C_TEXT_MAIN, spaceAfter=4)
    sub_heading_style = ParagraphStyle('SubHeading', parent=normal_style, fontSize=10.6, textColor=C_TEXT_MAIN, spaceAfter=6)
    source_note_style = ParagraphStyle('SourceNote', parent=muted_style, alignment=TA_RIGHT, spaceBefore=4, spaceAfter=0)
    notice_style = ParagraphStyle(
        'RenderNotice',
        parent=normal_style,
        backColor=HexColor("#FFF7ED"),
        borderColor=C_WARNING,
        borderWidth=0.8,
        borderPadding=8,
        leading=14,
        spaceAfter=10,
    )
    cell_style_center = ParagraphStyle('CellCenter', parent=normal_style, alignment=TA_CENTER, leading=12)
    value_cell_style = ParagraphStyle('ValueCell', parent=normal_style, alignment=TA_CENTER, leading=11.5)
    muted_cell_style = ParagraphStyle('MutedCell', parent=muted_style, alignment=TA_CENTER, leading=11)
    food_name_style = ParagraphStyle('FoodNameCell', parent=normal_style, alignment=TA_LEFT, leading=12, fontSize=9.3)
    food_meta_style = ParagraphStyle('FoodMetaCell', parent=muted_style, alignment=TA_CENTER, leading=11, fontSize=8.6)

    base_table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#EFF6FF")),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor("#1E40AF")),
        ('TEXTCOLOR', (0, 1), (-1, -1), C_TEXT_MAIN),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), font_name),
        ('FONTSIZE', (0, 0), (-1, 0), 9.2),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 11),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, 0), (-1, 0), 1.0, HexColor('#BFDBFE')),
        ('LINEBELOW', (0, 1), (-1, -2), 0.4, HexColor('#F1F5F9')),
        ('LINEBELOW', (0, -1), (-1, -1), 0.6, HexColor('#E2E8F0')),
    ]

    def checklist_paragraph(content):
        return Paragraph(f"<font color='{C_PRIMARY_STR}' size='11'>□</font> {content}", normal_style)

    def format_plan_content(item):
        if isinstance(item, dict):
            time = clean_html_tags(item.get('time', item.get('period', item.get('time_range', ''))))
            content = item.get('menu', item.get('activity', item.get('amount', '')))
            note = item.get('note', item.get('details', ''))
            if not content:
                separator = ' / ' if locale == 'zh-CN' else ', '
                content = separator.join(str(i) for i in item.get('items', []))[:30]
            cal = item.get('calories', '')
            if cal:
                note = f"{cal}kcal {note}".strip()
            clean_item = f"<b>{time}</b> {clean_html_tags(content)}" if time else clean_html_tags(content)
            if note:
                clean_item += f" <font color='{C_TEXT_MUTED_STR}'>({clean_html_tags(note)})</font>"
            return clean_item

        raw = clean_html_tags(str(item))
        time_match = re.match(r'^(\d{1,2}:\d{2}(?:\s*[-~]\s*\d{1,2}:\d{2})?)\s*(.*)$', raw)
        if time_match:
            return f"<b>{time_match.group(1)}</b> {clean_html_tags(time_match.group(2))}"
        return raw

    story = []
    condition_title = profile_condition_title(profile, locale)
    story.append(Paragraph(f"<b>{condition_title} | {t(locale, 'daily_report_title')}</b>", title_style))
    story.append(Paragraph(f"<font color='#64748B'>{data['date']} | {profile.get('name', t(locale, 'default_name'))}</font>", ParagraphStyle('Date', parent=normal_style, alignment=TA_CENTER)))
    story.append(GradientBanner(16.1 * cm))
    if render_notice:
        story.append(Spacer(1, 0.2*cm))
        story.append(Paragraph(f"<b>{t(locale, 'render_notice_title')}</b><br/>{clean_html_tags(render_notice)}", notice_style))
    story.append(Spacer(1, 0.5*cm))

    # Summary KPI cards — dual-mode branching
    total_score = float(scores.get('total', 0) or 0)
    card_width = 3.72 * cm
    card_height = 2.2 * cm
    _primary_cond = str(profile.get('primary_condition') or profile.get('condition') or '').strip().lower()
    _is_lifestyle = _primary_cond in {'balanced', 'fat_loss'}

    _card_score = SummaryCard(t(locale, 'score_total_label'), f"{total_score:.0f}",
                   t(locale, 'excellent') if total_score >= 80 else t(locale, 'good') if total_score >= 60 else t(locale, 'needs_improvement'),
                   get_score_color(total_score), font_name, card_width, card_height)
    _card_weight = SummaryCard(t(locale, 'weight'), format_weight(locale, data.get('weight_morning')),
                   f"BMI {scores.get('bmi', 0) or (scores.get('module_map', {}).get('weight', {}).get('bmi', 0)):.1f}",
                   C_PRIMARY_STR, font_name, card_width, card_height)

    if _is_lifestyle:
        _card3 = SummaryCard(t(locale, 'calories'), f"{nutrition.get('calories', 0):.0f} kcal", "",
                           C_WARNING_STR, font_name, card_width, card_height)
        _card4 = SummaryCard(localize('饮水', 'Water'), f"{data.get('water_total', 0)} ml",
                           f"/ {data.get('water_target', 2000)} ml",
                           C_SUCCESS_STR, font_name, card_width, card_height)
    else:
        _card3 = SummaryCard(t(locale, 'calories'), f"{nutrition.get('calories', 0):.0f} kcal", "",
                           C_WARNING_STR, font_name, card_width, card_height)
        _symptom_mod = next((m for m in score_modules if m.get('id') == 'symptom'), {})
        _symptom_status = _symptom_mod.get('status', '-')
        _symptom_score = float(_symptom_mod.get('raw', 0) or 0)
        _card4 = SummaryCard(localize('症状管理', 'Symptoms'), _symptom_status,
                           f"{_symptom_score:.0f}/100",
                           get_score_color(_symptom_score), font_name, card_width, card_height)

    summary_cards = Table(
        [[_card_score, _card_weight, _card3, _card4]],
        colWidths=[card_width + 0.25*cm] * 4,
    )
    summary_cards.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(summary_cards)
    story.append(Spacer(1, 0.4*cm))

    story.append(Spacer(1, 0.35*cm))
    story.append(AccentHeading(f"1. {t(locale, 'overall_score_title', date=data.get('date', ''))}", font_name=font_name))
    story.append(Spacer(1, 0.25*cm))
    score_data = [[t(locale, 'dimension'), t(locale, 'score'), t(locale, 'stars'), t(locale, 'status')]]
    for module in score_modules:
        raw_score = float(module.get('raw', 0) or 0)
        score_data.append([
            Paragraph(f"<b>{clean_html_tags(module.get('title', module.get('id', '')))}</b>", food_name_style),
            Paragraph(f"<b>{raw_score:.0f}/100</b>", value_cell_style),
            Paragraph(stars_to_text(module.get('stars', '')), cell_style_center),
            StatusBadge(clean_html_tags(module.get('status', '')), get_score_color(raw_score), font_name=font_name),
        ])
    total_score = float(scores.get('total', 0) or 0)
    score_data.append([
        Paragraph(f"<b>{t(locale, 'score_total_label')}</b>", food_name_style),
        Paragraph(f"<b>{total_score:.0f}/100</b>", value_cell_style),
        Paragraph(stars_to_text(scores.get('total_stars', '')), cell_style_center),
        StatusBadge(
            t(locale, 'excellent') if total_score >= 80 else t(locale, 'good') if total_score >= 60 else t(locale, 'needs_improvement'),
            get_score_color(total_score),
            font_name=font_name,
        ),
    ])
    score_table = Table(score_data, colWidths=[5.2*cm, 2.7*cm, 3.1*cm, 3.5*cm])
    score_style = list(base_table_style)
    score_style.extend([
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('TOPPADDING', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
    ])
    score_table.setStyle(TableStyle(score_style))
    story.append(score_table)
    story.append(Spacer(1, 0.4*cm))

    if ai_comment:
        story.append(Spacer(1, 0.35*cm))
        story.append(AccentHeading(t(locale, 'expert_ai_insights'), font_name=font_name))
        story.append(Spacer(1, 0.25*cm))
        for section in build_ai_comment_sections(ai_comment, locale):
            title = clean_html_tags(section.get("title") or "").strip()
            items = [clean_html_tags(item).strip() for item in section.get("items", []) if clean_html_tags(item).strip()]
            section_nodes = []
            title_color = C_WARNING_STR
            if title:
                title_color = C_SUCCESS_STR if any(keyword in title.lower() for keyword in ("well", "good", "亮点", "做得")) else C_WARNING_STR
                section_nodes.append(Paragraph(f"<font color='{title_color}'><b>{title}</b></font>", card_title_style))
            for item in items:
                section_nodes.append(Paragraph(f"<font color='{C_PRIMARY_STR}'>•</font> {item}", normal_style))
                section_nodes.append(Spacer(1, 0.04 * cm))
            if not section_nodes and title:
                section_nodes.append(Paragraph(title, normal_style))
            story.append(
                Table(
                    [[[Spacer(3, 0)] + section_nodes]],
                    colWidths=[16.1 * cm],
                    style=TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), HexColor("#FAFBFC")),
                        ('LINEBELOW', (0, 0), (-1, -1), 0.0, colors.white),
                        ('LINEBEFORE', (0, 0), (0, -1), 3.0, HexColor(title_color)),
                        ('LEFTPADDING', (0, 0), (-1, -1), 14),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                        ('TOPPADDING', (0, 0), (-1, -1), 10),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]),
                )
            )
            story.append(Spacer(1, 0.12*cm))
        if generation_meta:
            story.append(Paragraph(source_text(generation_meta.get('ai_comment')), source_note_style))
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.35*cm))
    story.append(AccentHeading(f"2. {t(locale, 'daily_baseline_data')}", font_name=font_name))
    story.append(Spacer(1, 0.25*cm))
    weight_module = module_map.get('weight', {})
    bmi_val = weight_module.get('bmi', scores.get('bmi', 0)) or 0
    weight_val = data.get('weight_morning')
    bmr_val = (10 * (weight_val or 65) + 6.25 * profile.get('height_cm', 172) - 5 * profile.get('age', 34) + (5 if str(profile.get('gender', 'male')).lower() == 'male' else -161))
    tdee_val = bmr_val * profile.get('activity_level', 1.2)

    health_data = [
        [t(locale, 'metric'), t(locale, 'value'), t(locale, 'reference_range')],
        [Paragraph(f"<b>{t(locale, 'height')}</b>", food_name_style), Paragraph(f"<b>{profile['height_cm']}cm</b>", value_cell_style), Paragraph(t(locale, 'not_available'), muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'weight')}</b>", food_name_style), Paragraph(f"<b>{format_weight(locale, weight_val)}</b>", value_cell_style), Paragraph(t(locale, 'weight_target', weight=format_weight(locale, profile.get('target_weight_kg', 64))), muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'bmi')}</b>", food_name_style), Paragraph(f"<b>{bmi_val:.1f}</b>", value_cell_style), Paragraph(t(locale, 'bmi_reference'), muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'bmr')}</b>", food_name_style), Paragraph(f"<b>{bmr_val:.0f} kcal</b>", value_cell_style), Paragraph(t(locale, 'not_available'), muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'tdee')}</b>", food_name_style), Paragraph(f"<b>{tdee_val:.0f} kcal</b>", value_cell_style), Paragraph(t(locale, 'not_available'), muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'recommended_calories')}</b>", food_name_style), Paragraph(f"<b>{tdee_val:.0f} kcal/day</b>", value_cell_style), Paragraph(t(locale, 'recommended_calories_reference', condition=condition_title), muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'protein')}</b>", food_name_style), Paragraph(f"<b>{macros.get('protein_g', 0)}g/day</b>", value_cell_style), Paragraph(f"{macros.get('protein_p', 0)}%", muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'fat')}</b>", food_name_style), Paragraph(f"<b>{macros.get('fat_g', 0)}g/day</b>", value_cell_style), Paragraph(f"{macros.get('fat_p', 0)}%", muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'carb')}</b>", food_name_style), Paragraph(f"<b>{macros.get('carb_g', 0)}g/day</b>", value_cell_style), Paragraph(f"{macros.get('carb_p', 0)}%", muted_cell_style)],
        [Paragraph(f"<b>{t(locale, 'fiber')}</b>", food_name_style), Paragraph(f"<b>>={macros.get('fiber_min_g', 25)}g/day</b>", value_cell_style), Paragraph(t(locale, 'fiber_reference'), muted_cell_style)],
    ]
    health_table = Table(health_data, colWidths=[5*cm, 4*cm, 5*cm])
    health_style = list(base_table_style)
    health_style.extend([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ])
    if 18.5 <= bmi_val < 24:
        health_style.append(('TEXTCOLOR', (1, 3), (1, 3), C_SUCCESS))
    elif bmi_val > 0:
        health_style.append(('TEXTCOLOR', (1, 3), (1, 3), C_DANGER if bmi_val >= 28 or bmi_val < 18.5 else C_WARNING))
    health_table.setStyle(TableStyle(health_style))
    story.append(health_table)
    story.append(Spacer(1, 0.4*cm))

    temp_images = []

    story.append(Spacer(1, 0.35*cm))
    story.append(AccentHeading(f"3. {t(locale, 'daily_nutrition_breakdown')}", font_name=font_name))
    story.append(Spacer(1, 0.25*cm))
    chart_path_nutrition = create_nutrition_chart(nutrition, locale)
    if chart_path_nutrition:
        temp_images.append(chart_path_nutrition)
        img = Image(chart_path_nutrition, width=10*cm, height=6*cm)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 0.2*cm))

    nutrition_rows = [
        ("calories", t(locale, 'calories'), float(nutrition['calories']), float(tdee_val), f"{nutrition['calories']:.0f} kcal", f"{tdee_val:.0f} kcal"),
        ("protein", t(locale, 'protein'), float(nutrition['protein']), float(macros.get('protein_g', 0) or 0), f"{nutrition['protein']:.1f}g", f"{macros.get('protein_g', 0)}g"),
        ("fat", t(locale, 'fat'), float(nutrition['fat']), float(macros.get('fat_g', 0) or 0), f"{nutrition['fat']:.1f}g", f"{macros.get('fat_g', 0)}g"),
        ("carb", t(locale, 'carb'), float(nutrition['carb']), float(macros.get('carb_g', 0) or 0), f"{nutrition['carb']:.1f}g", f"{macros.get('carb_g', 0)}g"),
        ("fiber", t(locale, 'fiber'), float(nutrition['fiber']), float(macros.get('fiber_min_g', 25) or 25), f"{nutrition['fiber']:.1f}g", f">={macros.get('fiber_min_g', 25)}g"),
    ]
    nutrition_data = [[t(locale, 'nutrient'), t(locale, 'actual_intake'), t(locale, 'recommended_intake'), localize('达成度', 'Progress')]]
    for metric_key, label, actual, target, actual_text, target_text in nutrition_rows:
        ratio, color, _ = classify_nutrition_progress(metric_key, actual, target)
        nutrition_data.append([
            Paragraph(f"<b>{label}</b>", food_name_style),
            Paragraph(f"<b>{actual_text}</b>", value_cell_style),
            Paragraph(target_text, muted_cell_style),
            MicroProgressBar(ratio, color, f"{min(ratio, 9.99) * 100:.0f}%", font_name=font_name, width=3.4 * cm),
        ])
    nutri_table = Table(nutrition_data, colWidths=[4.4*cm, 3.5*cm, 4.2*cm, 3.7*cm])
    nutri_table.setStyle(TableStyle(base_table_style + [
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
    ]))
    story.append(nutri_table)
    story.append(Spacer(1, 0.4*cm))

    story.append(Spacer(1, 0.35*cm))
    story.append(AccentHeading(f"4. {t(locale, 'daily_water_details')}", font_name=font_name))
    story.append(Spacer(1, 0.25*cm))
    if water_records and len(water_records) > 0:
        chart_path_water = create_water_chart(water_records, data.get('water_target', 2000), locale)
        if chart_path_water:
            temp_images.append(chart_path_water)
            img_water = Image(chart_path_water, width=14*cm, height=5.25*cm)
            img_water.hAlign = 'CENTER'
            story.append(img_water)
            story.append(Spacer(1, 0.4*cm))
    else:
        story.append(Paragraph(f"<font color='#64748B'>{t(locale, 'no_water_today')}</font>", normal_style))
        story.append(Spacer(1, 0.4*cm))

    story.append(Spacer(1, 0.35*cm))
    story.append(AccentHeading(f"5. {t(locale, 'daily_meal_details')}", font_name=font_name))
    story.append(Spacer(1, 0.25*cm))
    if meals and len(meals) > 0:
        meal_chart_path = create_meal_macro_stacked_chart(meals, locale)
        if meal_chart_path:
            temp_images.append(meal_chart_path)
            meal_chart = Image(meal_chart_path, width=14.5 * cm, height=5.4 * cm)
            meal_chart.hAlign = 'CENTER'
            story.append(meal_chart)
            story.append(Spacer(1, 0.18 * cm))
        seen_meals = set()
        for meal in meals:
            meal_elements = []
            meal_type = meal.get('type', '')
            meal_time = meal.get('time', '')
            meal_key = f"{meal_type}_{meal_time}"
            if meal_key in seen_meals:
                continue
            seen_meals.add(meal_key)

            meal_time_str = f" <font color='#64748B' size='9'>({meal_time})</font>" if meal_time else ''
            meal_title_text = f"<b>{meal_name(locale, meal_type)}</b>{meal_time_str} <font color='#64748B' size='9'>| {t(locale, 'meal_total', calories=meal.get('total_calories', 0))}</font>"
            meal_title = Paragraph(meal_title_text, ParagraphStyle('MealTitle', parent=normal_style, spaceBefore=8, spaceAfter=4))
            meal_elements.append(meal_title)

            food_nutrition = meal.get('food_nutrition', [])
            _skip_kw = ('今日累计', '累计', '合计', '总计', 'total', 'subtotal',
                         '钾', '钠', '钙', '铁', '锌', '镁', '维生素', 'potassium', 'sodium', 'calcium')
            food_nutrition = [
                f for f in (food_nutrition or [])
                if not any(kw in str(f.get('name', '')).lower() for kw in _skip_kw)
                and float(f.get('calories', 0) or 0) > 0
            ]
            if food_nutrition and len(food_nutrition) > 0:
                meal_data = [[t(locale, 'food_name'), t(locale, 'portion'), t(locale, 'calories'), t(locale, 'protein'), t(locale, 'fat'), t(locale, 'carb')]]
                for food in food_nutrition:
                    name_raw = str(food.get('name', '')).strip()
                    portion_match = re.search(rf'(\d+(?:\.\d+)?)\s*{PORTION_UNIT_PATTERN}', name_raw, re.IGNORECASE)
                    if portion_match:
                        name_simple = re.sub(r'\s*' + re.escape(portion_match.group(0)), '', name_raw).strip()
                        portion_display = f"{float(portion_match.group(1)):.0f}{portion_match.group(2)}"
                    else:
                        name_simple = name_raw
                        portion_display = f"{food.get('portion_grams', 100):.0f}g"

                    name_simple = simplify_food_name_for_pdf(name_simple)
                    if len(name_simple) < 2:
                        name_simple = name_raw
                    meal_data.append([
                        Paragraph(f"<b>{clean_html_tags(name_simple)}</b>", food_name_style),
                        Paragraph(portion_display, muted_cell_style),
                        Paragraph(f"{food.get('calories', 0):.0f}kcal", food_meta_style),
                        Paragraph(f"{food.get('protein', 0):.1f}g", food_meta_style),
                        Paragraph(f"{food.get('fat', 0):.1f}g", food_meta_style),
                        Paragraph(f"{food.get('carb', 0):.1f}g", food_meta_style),
                    ])

                meal_table = Table(meal_data, colWidths=[4.5*cm, 2*cm, 2*cm, 2*cm, 2*cm, 2.5*cm])
                meal_table.setStyle(TableStyle(base_table_style + [
                    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ]))
                meal_elements.append(meal_table)
            else:
                meal_elements.append(Paragraph(f"<font color='#64748B'>{t(locale, 'no_food_detail')}</font>", normal_style))

            meal_elements.append(Spacer(1, 0.4*cm))
            story.append(KeepTogether(meal_elements))
    else:
        story.append(Paragraph(f"<font color='#64748B'>{t(locale, 'no_meals_today')}</font>", normal_style))
    story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.35*cm))
    story.append(AccentHeading(f"6. {t(locale, 'daily_exercise_details')}", font_name=font_name))
    story.append(Spacer(1, 0.25*cm))
    steps = data.get('steps', 0)
    step_target = profile.get('step_target', 8000)
    exercise_lines = build_exercise_detail_lines(exercise_data, steps, locale)
    if exercise_data or steps > 0:
        chart_path_exercise = create_energy_balance_chart(nutrition, exercise_data, steps, step_target, bmr_val, locale)
        if chart_path_exercise:
            temp_images.append(chart_path_exercise)
            img_ex = Image(chart_path_exercise, width=14.7*cm, height=5.5*cm)
            img_ex.hAlign = 'CENTER'
            story.append(img_ex)
            story.append(Spacer(1, 0.2*cm))

        for line in exercise_lines:
            safe_line = clean_html_tags(line)
            if ':' in safe_line:
                head, tail = safe_line.split(':', 1)
                story.append(Paragraph(f"<b>{head}:</b>{tail}", normal_style))
            else:
                story.append(Paragraph(f"<b>{safe_line}</b>", normal_style))
        if exercise_lines:
            story.append(Spacer(1, 0.2*cm))
        elif not chart_path_exercise:
            story.append(Paragraph(f"<font color='#64748B'>{t(locale, 'no_exercise_today')}</font>", normal_style))
    else:
        story.append(Paragraph(f"<font color='#64748B'>{t(locale, 'no_exercise_today')}</font>", normal_style))
    story.append(Spacer(1, 0.4*cm))

    section_idx = 7
    has_medication_module = any(module.get('id') == 'medication' for module in score_modules)
    if has_medication_module:
        medication_title = localize('\u7528\u836f\u60c5\u51b5', 'Medication')
        story.append(Spacer(1, 0.35*cm))
        story.append(AccentHeading(f"{section_idx}. {medication_title}", font_name=font_name))
        story.append(Spacer(1, 0.25*cm))
        section_idx += 1
        if medication_records:
            for item in medication_records:
                item_text = re.sub(r'^\s*[-*]\s*', '', str(item or '')).strip()
                story.append(Paragraph(f"- {clean_html_tags(item_text)}", normal_style))
        else:
            story.append(Paragraph(f"<font color='#64748B'>{t(locale, 'no_record')}</font>", normal_style))
        story.append(Spacer(1, 0.3*cm))

    if custom_sections:
        story.append(Spacer(1, 0.35*cm))
        story.append(AccentHeading(f"{section_idx}. {t(locale, 'extra_monitoring_records')}", font_name=font_name))
        story.append(Spacer(1, 0.25*cm))
        section_idx += 1
        for header, items in custom_sections.items():
            story.append(Paragraph(f"<b>{clean_html_tags(header)}</b>", ParagraphStyle('Sub', parent=normal_style, textColor=C_TEXT_MAIN, spaceAfter=4)))
            for item in items:
                item_text = re.sub(r'^\s*[-*]\s*', '', str(item or '')).strip()
                story.append(Paragraph(f"- {clean_html_tags(item_text)}", normal_style))
            story.append(Spacer(1, 0.3*cm))

    story.append(Spacer(1, 0.35*cm))
    story.append(AccentHeading(f"{section_idx}. {t(locale, 'risk_alerts')}", font_name=font_name))
    story.append(Spacer(1, 0.25*cm))
    section_idx += 1
    if risks:
        for risk in risks:
            story.append(Paragraph(f"<font color='{C_DANGER_STR}'><b>{clean_html_tags(risk.get('level', '')).strip()} {clean_html_tags(risk.get('item', ''))}</b></font>", normal_style))
            story.append(Paragraph(t(locale, 'risk_label', value=clean_html_tags(risk.get('risk', ''))), normal_style))
            story.append(Paragraph(t(locale, 'advice_label', value=clean_html_tags(risk.get('action', ''))), normal_style))
            story.append(Spacer(1, 0.2*cm))
    else:
        story.append(Paragraph(f"<font color='{C_SUCCESS_STR}'>{t(locale, 'no_risk')}</font>", normal_style))
    if generation_meta:
        story.append(Paragraph(source_text(generation_meta.get('risk_alerts')), source_note_style))
    story.append(Spacer(1, 0.4*cm))

    story.append(Spacer(1, 0.35*cm))
    story.append(AccentHeading(f"{section_idx}. {t(locale, 'action_plan')}", font_name=font_name))
    story.append(Spacer(1, 0.25*cm))
    for category, title in [('diet', t(locale, 'diet_plan')), ('water', t(locale, 'water_plan')), ('exercise', t(locale, 'exercise_plan'))]:
        if plan.get(category):
            story.append(Paragraph(f"<b>{title}</b>", ParagraphStyle('Sub', parent=sub_heading_style, textColor=C_TEXT_MAIN, spaceAfter=6)))
            for item in plan.get(category, []):
                story.append(checklist_paragraph(format_plan_content(item)))
            story.append(Spacer(1, 0.2*cm))

    if plan.get('notes'):
        story.append(Paragraph(f"<b>{t(locale, 'special_attention')}</b>", ParagraphStyle('Sub', parent=sub_heading_style, textColor=C_TEXT_MAIN, spaceAfter=6)))
        for item in plan.get('notes', []):
            story.append(checklist_paragraph(clean_html_tags(item)))
    if generation_meta:
        story.append(Paragraph(source_text(generation_meta.get('next_day_plan')), source_note_style))

    story.append(Spacer(1, 1.5*cm))
    footer_style = ParagraphStyle('Footer', parent=normal_style, fontSize=9, textColor=C_TEXT_MUTED, alignment=TA_CENTER)
    story.append(Paragraph(t(locale, 'generated_at', timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')), footer_style))
    story.append(Paragraph(f"{footer_text}", footer_style))

    doc.build(story, canvasmaker=build_numbered_canvasmaker(font_name))
    for temp_img in temp_images:
        try:
            os.remove(temp_img)
        except:
            pass
    print(f"PDF report generated: {output_path}")
if __name__ == "__main__":
    print("Use this module via daily_report_pro.py.")
    
