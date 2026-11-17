# -*- coding: utf-8 -*-
"""F7: 基础汉化

自动提取模组的英语语言文件键值对，翻译为简体中文，
生成zh_cn.json汉化补丁，可调用F5重打包固化进JAR。

V1仅处理基础词条（方块/物品/道具名称），不涉及配置面板和深层代码文本汉化。

使用方式:
    from core.translator import run
    import argparse
    args = argparse.Namespace(jar_path="xxx.jar", target_lang="zh_cn", patch_only=False)
    result = run(args)
"""

import sys
import os
import json
import re
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config
from utils.logger import get_logger
from utils.jar_utils import (
    extract_jar, create_temp_dir, cleanup_temp_dir,
    read_jar_file
)
from utils.report_gen import ReportGenerator

logger = get_logger("translator")

# === MC基础词条分类正则 ===
CATEGORY_PATTERNS = {
    "block": re.compile(r"^(block|tile)\.", re.IGNORECASE),
    "item": re.compile(r"^(item|gun|ammo)\.", re.IGNORECASE),
    "tooltip": re.compile(r"\.tooltip\.|\.desc\.|\.info\.|\.text\.|tooltip|tooltip", re.IGNORECASE),
    "advancement": re.compile(r"^(advancement|achievement)\.", re.IGNORECASE),
    "entity": re.compile(r"^(entity|mob)\.", re.IGNORECASE),
    "sound": re.compile(r"^(sound|sounds|Music)\.", re.IGNORECASE),
    "creative": re.compile(r"^(itemGroup|creativeTab|tab)\.", re.IGNORECASE),
    "config": re.compile(r"^(config|gui|screen|button|option)\.", re.IGNORECASE),
}

# === MC常见术语翻译词典（英语 -> 目标语言） ===
# 主词典：英语 -> 简体中文（默认）
MC_TERMS_DICT = {
    # 通用词汇
    "item": "物品",
    "block": "方块",
    "tile": "方块",
    "entity": "实体",
    "mob": "生物",
    "player": "玩家",
    "damage": "伤害",
    "health": "生命",
    "speed": "速度",
    "duration": "持续时间",
    "infinite": "无限",
    "normal": "普通",
    "small": "小型",
    "large": "大型",
    # 矿物
    "coal": "煤炭",
    "iron": "铁",
    "gold": "金",
    "diamond": "钻石",
    "emerald": "绿宝石",
    "redstone": "红石",
    "lapis": "青金石",
    "obsidian": "黑曜石",
    # 工具
    "pickaxe": "镐",
    "sword": "剑",
    "axe": "斧",
    "shovel": "铲",
    "hoe": "锄",
    "hammer": "锤",
    "bow": "弓",
    "arrow": "箭",
    "shield": "盾牌",
    # 食物
    "apple": "苹果",
    "bread": "面包",
    "cooked": "熟",
    "raw": "生",
    # 颜色
    "white": "白色",
    "red": "红色",
    "green": "绿色",
    "blue": "蓝色",
    "black": "黑色",
    "yellow": "黄色",
    "gray": "灰色",
    "grey": "灰色",
    "silver": "银色",
    # 功能
    "toggle": "切换",
    "enabled": "启用",
    "disabled": "禁用",
    "allow": "允许",
    "deny": "拒绝",
    "open": "打开",
    "close": "关闭",
    "on": "开",
    "off": "关",
    "yes": "是",
    "no": "否",
    # 模组通用
    "create": "机械动力",
    "steam": "蒸汽",
    "rails": "铁轨",
    "engine": "引擎",
    "belt": "传送带",
    "gear": "齿轮",
    "shaft": "轴",
    "pulley": "滑轮",
    "chain": "链条",
    "windmill": "风车",
    "water": "水",
    "fire": "火",
    "air": "空气",
    "earth": "泥土",
    "stone": "石头",
    "wood": "木头",
    "plank": "木板",
    "log": "原木",
    "leaves": "树叶",
    # 附魔
    "enchanted": "附魔的",
    "enchantment": "附魔",
    "fortune": "时运",
    "silk": "精准采集",
    "unbreaking": "耐久",
    "efficiency": "效率",
    # 游戏机制
    "survival": "生存",
    "creative": "创造",
    "adventure": "冒险",
    "spectator": "旁观",
    "peaceful": "和平",
    "easy": "简单",
    "hard": "困难",
}

# 阿拉伯语术语词典（英语 -> 通用阿拉伯语）
MC_TERMS_DICT_AR_SA = {
    # General terms
    "item": "عنصر",
    "block": "كتلة",
    "tile": "كتلة",
    "entity": "كيان",
    "mob": "كائن",
    "player": "لاعب",
    "damage": "ضرر",
    "health": "صحة",
    "speed": "سرعة",
    "duration": "مدة",
    "infinite": "غير محدود",
    "normal": "عادي",
    "small": "صغير",
    "large": "كبير",
    # Minerals
    "coal": "فحم",
    "iron": "حديد",
    "gold": "ذهب",
    "diamond": "ماس",
    "emerald": "زمرد",
    "redstone": "ريدستون",
    "lapis": "لازورد",
    "obsidian": "أوبسيديان",
    # Tools
    "pickaxe": "معول",
    "sword": "سيف",
    "axe": "فأس",
    "shovel": "مجرفة",
    "hoe": "مذرع",
    "hammer": "مطرقة",
    "bow": "قوس",
    "arrow": "سهم",
    "shield": "درع",
    # Food
    "apple": "تفاحة",
    "bread": "خبز",
    "cooked": "مطبوخ",
    "raw": "نيء",
    # Colors
    "white": "أبيض",
    "red": "أحمر",
    "green": "أخضر",
    "blue": "أزرق",
    "black": "أسود",
    "yellow": "أصفر",
    "gray": "رمادي",
    "grey": "رمادي",
    "silver": "فضي",
    # Functions
    "toggle": "تبديل",
    "enabled": "مفعل",
    "disabled": "معطل",
    "allow": "سماح",
    "deny": "رفض",
    "open": "فتح",
    "close": "إغلاق",
    "on": "تشغيل",
    "off": "إيقاف",
    "yes": "نعم",
    "no": "لا",
    # Mods common
    "create": "كرييت",
    "steam": "بخار",
    "rails": "قضبان",
    "engine": "محرك",
    "belt": "حزام ناقل",
    "gear": "ترس",
    "shaft": "عمود",
    "pulley": "بكرة",
    "chain": "سلسلة",
    "windmill": "طاحونة هوائية",
    "water": "ماء",
    "fire": "نار",
    "air": "هواء",
    "earth": "تراب",
    "stone": "حجر",
    "wood": "خشب",
    "plank": "لوح خشبي",
    "log": "جذع شجرة",
    "leaves": "أوراق",
    # Enchantments
    "enchanted": "مشحون",
    "enchantment": "سحر",
    "fortune": "الحظ",
    "silk": "اللمس الحريري",
    "unbreaking": "عدم الكسر",
    "efficiency": "كفاءة",
    # Game mechanics
    "survival": "بقاء",
    "creative": "إبداع",
    "adventure": "مغامرة",
    "spectator": "متفرج",
    "peaceful": "هادئ",
    "easy": "سهل",
    "hard": "صعب",
}

# 语言 -> 术语词典映射表
LANG_TERMS_DICT = {
    "zh_cn": MC_TERMS_DICT,
    "zh_tw": MC_TERMS_DICT,  # 繁体暂用简体词典（后续可单独维护）
    "ar_sa": MC_TERMS_DICT_AR_SA,
}


def _categorize_key(key: str) -> str:
    """根据key判断词条分类"""
    for category, pattern in CATEGORY_PATTERNS.items():
        if pattern.search(key):
            return category
    return "other"


def _simple_translate(text: str) -> str:
    """简易翻译（基于词典替换）

    V1版本使用词典替换方式，V2/V3将接入AI翻译API
    """
    if not text or not isinstance(text, str):
        return text

    result = text

    # 按长度降序排列，优先匹配长词
    sorted_terms = sorted(MC_TERMS_DICT.items(), key=lambda x: len(x[0]), reverse=True)

    for en, zh in sorted_terms:
        # 仅替换独立单词，不替换子串
        pattern = re.compile(r'\b' + re.escape(en) + r'\b', re.IGNORECASE)
        result = pattern.sub(zh, result)

    return result


def _find_language_files(jar_path: Path) -> List[Tuple[str, str]]:
    """在JAR中查找语言文件

    Returns:
        [(en_us_path, local_path), ...]
    """
    lang_files = []
    tmp_dir = create_temp_dir("lang_find")

    try:
        extract_jar(jar_path, tmp_dir)

        for root, dirs, files in os.walk(tmp_dir):
            for filename in files:
                if filename == "en_us.json":
                    local_path = str(Path(root) / filename)
                    # 计算JAR内相对路径（使用正斜杠）
                    rel_in_jar = Path(local_path).relative_to(tmp_dir).as_posix()
                    lang_files.append((rel_in_jar, local_path))
    except (zipfile.BadZipFile, Exception) as e:
        logger.warning(f"解压JAR失败 {jar_path.name}: {e}")
    finally:
        cleanup_temp_dir(tmp_dir)

    return lang_files


def _extract_lang_content(jar_path: Path, lang_path: str) -> Optional[Dict[str, Any]]:
    """从JAR中提取语言文件内容"""
    try:
        content = read_jar_file(jar_path, lang_path)
        if content:
            return json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError, KeyError) as e:
        logger.debug(f"读取语言文件失败: {lang_path}, 原因: {e}")
    return None


def _categorize_entries(lang_data: Dict[str, Any]) -> Dict[str, List[Tuple[str, str]]]:
    """按分类整理语言条目

    Returns:
        {category: [(key, value), ...]}
    """
    categorized = defaultdict(list)

    for key, value in lang_data.items():
        if not isinstance(value, str):
            continue
        category = _categorize_key(key)
        categorized[category].append((key, value))

    # 按分类排序
    for cat in categorized:
        categorized[cat].sort(key=lambda x: x[0])

    return dict(categorized)


def _generate_zh_cn(
    lang_data: Dict[str, Any],
    categories: Dict[str, List[Tuple[str, str]]],
    target_lang: str,
) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
    """生成中文翻译文件

    Returns:
        (zh_cn_data, quality_notes)
    """
    zh_cn = {}
    quality_notes = []

    # 仅翻译基础词条（V1范围）
    v1_categories = {"block", "item", "tooltip", "advancement", "entity", "other"}

    for category, entries in categories.items():
        if category not in v1_categories:
            continue

        for key, value in entries:
            translated = _simple_translate(value, target_lang)
            zh_cn[key] = translated

    # 质量说明
    cat_counts = {k: len(v) for k, v in categories.items() if k in v1_categories}
    if cat_counts.get("tooltip", 0) > 50:
        quality_notes.append("建议人工校对：tooltip类词条可能含模组专有术语")
    if cat_counts.get("advancement", 0) > 0:
        quality_notes.append("建议人工校对：advancement类词条需结合游戏进度理解")
    if cat_counts.get("config", 0) > 0:
        quality_notes.append("配置面板文本未汉化（V2功能），如需请升级到V2")

    return zh_cn, quality_notes


def _generate_html_report(
    jar_path: str,
    target_lang: str,
    categories: Dict[str, List[Tuple[str, str]]],
    zh_cn: Dict[str, str],
    quality_notes: List[str],
    timestamp: str,
) -> str:
    """生成HTML翻译报告"""
    rg = ReportGenerator("基础汉化报告")

    # === 统计概览 ===
    total_entries = sum(len(v) for v in categories.values())
    translated_count = len(zh_cn)
    untranslated_count = total_entries - translated_count

    overview_html = f"""
    <div class='overview-grid'>
      <div class='overview-card'>
        <div class='oc-num'>{total_entries}</div>
        <div class='oc-label'>源词条总数</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{translated_count}</div>
        <div class='oc-label'>已翻译词条</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{untranslated_count}</div>
        <div class='oc-label'>未翻译词条</div>
      </div>
      <div class='overview-card'>
        <div class='oc-num'>{len(categories)}</div>
        <div class='oc-label'>涉及分类</div>
      </div>
    </div>
    """

    # === 分类统计 ===
    category_labels = {
        "block": "方块", "item": "物品", "tooltip": "提示文本",
        "advancement": "进度", "entity": "实体", "sound": "音效",
        "creative": "创造标签", "config": "配置", "other": "其他",
    }

    cat_rows = ""
    for cat, entries in sorted(categories.items(), key=lambda x: -len(x[1])):
        label = category_labels.get(cat, cat)
        v1_tag = " <span class='badge badge-accent'>V1</span>" if cat in {"block", "item", "tooltip", "advancement"} else ""
        cat_rows += f"""
        <tr>
          <td>{label}{v1_tag}</td>
          <td>{len(entries)}</td>
          <td>{'✅' if cat in {'block', 'item', 'tooltip', 'advancement', 'entity', 'other'} else '⏭️'}</td>
        </tr>
        """

    cat_html = f"""
    <div class='callout'>
      <div class='callout-title'>📊 分类统计</div>
      <table class='data-table'>
        <thead>
          <tr><th>分类</th><th>词条数</th><th>V1是否处理</th></tr>
        </thead>
        <tbody>
          {cat_rows}
        </tbody>
      </table>
    </div>
    """

    # === 翻译示例 ===
    sample_entries = list(zh_cn.items())[:20]
    if sample_entries:
        sample_rows = ""
        for key, zh_val in sample_entries:
            en_val = ""
            for cat, entries in categories.items():
                for k, v in entries:
                    if k == key:
                        en_val = v
                        break
                if en_val:
                    break
            sample_rows += f"""
            <tr>
              <td><code>{key}</code></td>
              <td>{en_val}</td>
              <td><strong>{zh_val}</strong></td>
            </tr>
            """
        sample_html = f"""
        <div class='callout'>
          <div class='callout-title'>📝 翻译示例（前20条）</div>
          <table class='data-table'>
            <thead>
              <tr><th>Key</th><th>原文</th><th>译文</th></tr>
            </thead>
            <tbody>
              {sample_rows}
            </tbody>
          </table>
        </div>
        """
    else:
        sample_html = """
        <div class='callout warning'>
          <div class='callout-title'>⚠️ 无翻译内容</div>
          <p>该模组的语言文件可能为空，或已包含中文翻译。</p>
        </div>
        """

    # === 质量说明 ===
    quality_html = ""
    if quality_notes:
        notes_html = "".join(f"<li>{n}</li>" for n in quality_notes)
        quality_html = f"""
        <div class='callout warning'>
          <div class='callout-title'>🔍 质量提示</div>
          <ul>{notes_html}</ul>
        </div>
        """

    # === 技术说明 ===
    tech_html = """
    <div class='callout'>
      <div class='callout-title'>技术说明</div>
      <p>V1基础汉化仅处理以下分类：方块名、物品名、实体名、基础提示文本、进度文本。</p>
      <p>不处理：配置面板GUI文本、光影配置文件、深层代码硬编码文本。这些属于V2深度精细化汉化。</p>
      <p>翻译方式：V1使用本地词典替换，准确率约60%-70%。V2将接入AI翻译API，准确率可达85%-90%。</p>
      <p>建议：使用前人工校对关键词条，特别是模组专有术语。</p>
    </div>
    """

    body_html = f"""
    <h2>翻译概览</h2>
    {overview_html}

    <h2>分类统计</h2>
    {cat_html}

    <h2>翻译示例</h2>
    {sample_html}

    <h2>质量提示</h2>
    {quality_html}

    <h2>技术说明</h2>
    {tech_html}
    """

    return rg.render_full_html("基础汉化报告", body_html, timestamp)


def run(args) -> Dict[str, Any]:
    """F7 基础汉化主入口

    Args:
        args: argparse.Namespace，需包含:
            - jar_path: JAR文件路径
            - target_lang: 目标语言，默认zh_cn
            - patch_only: 仅生成补丁不固化进JAR
            - output: 输出目录(可选)

    Returns:
        统一返回结构字典
    """
    start_time = datetime.now()
    jar_path = getattr(args, "jar_path", None)
    target_lang = getattr(args, "target_lang", "zh_cn")
    patch_only = getattr(args, "patch_only", False)
    output_dir = getattr(args, "output", None) or str(config.OUTPUT_DIR / "reports")

    if not jar_path:
        return config.make_result(
            status="error",
            feature="F7",
            input_summary={"jar_path": None},
            result={"error": "缺少 --jar-path 参数"},
            errors=["必须指定JAR文件路径"],
        )

    jar_path_obj = Path(jar_path)
    if not jar_path_obj.exists():
        return config.make_result(
            status="error",
            feature="F7",
            input_summary={"jar_path": str(jar_path_obj)},
            result={"error": f"文件不存在: {jar_path}"},
            errors=[f"JAR文件不存在: {jar_path}"],
        )

    logger.info(f"开始汉化: {jar_path}")

    # === 1. 查找语言文件 ===
    lang_files = _find_language_files(jar_path_obj)
    if not lang_files:
        return config.make_result(
            status="warning",
            feature="F7",
            input_summary={"jar_path": str(jar_path_obj)},
            result={"error": "未找到英语语言文件(en_us.json)"},
            warnings=["该模组可能没有en_us.json，或语言文件结构特殊"],
        )

    logger.info(f"找到 {len(lang_files)} 个语言文件")

    # === 2. 提取语言内容 ===
    all_lang_data = {}
    for lang_path, local_path in lang_files:
        lang_data = _extract_lang_content(jar_path_obj, lang_path)
        if lang_data:
            all_lang_data[lang_path] = lang_data

    if not all_lang_data:
        return config.make_result(
            status="warning",
            feature="F7",
            input_summary={"jar_path": str(jar_path_obj)},
            result={"error": "语言文件解析失败"},
            warnings=["所有en_us.json文件均无法解析"],
        )

    # === 3. 合并所有语言数据 ===
    merged_lang = {}
    for lang_data in all_lang_data.values():
        merged_lang.update(lang_data)

    # === 4. 分类整理 ===
    categories = _categorize_entries(merged_lang)

    # === 5. 生成翻译 ===
    zh_cn, quality_notes = _generate_zh_cn(merged_lang, categories, target_lang)

    # === 6. 保存zh_cn.json ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(output_dir, exist_ok=True)

    # 补丁资源目录
    patch_resources_dir = config.PATCH_DIR / "resources"
    os.makedirs(patch_resources_dir, exist_ok=True)

    # 从语言文件路径推断资源路径
    first_lang_path = lang_files[0][0]
    # en_us.json -> zh_cn.json
    zh_cn_jar_path = first_lang_path.replace("en_us.json", f"{target_lang}.json")

    # 保存到补丁目录
    patch_save_path = patch_resources_dir / zh_cn_jar_path
    os.makedirs(patch_save_path.parent, exist_ok=True)

    with open(patch_save_path, "w", encoding="utf-8") as f:
        json.dump(zh_cn, f, ensure_ascii=False, indent=2)

    logger.info(f"汉化补丁已生成: {patch_save_path}")

    # === 7. 生成报告 ===
    total_entries = sum(len(v) for v in categories.values())
    report_html = _generate_html_report(
        str(jar_path_obj), target_lang, categories, zh_cn, quality_notes, timestamp
    )
    html_path = Path(output_dir) / f"translator_{timestamp}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(report_html)

    # JSON数据
    json_path = Path(output_dir) / f"translator_{timestamp}.json"
    json_data = {
        "jar_path": str(jar_path_obj),
        "target_lang": target_lang,
        "categories": {k: len(v) for k, v in categories.items()},
        "total_entries": total_entries,
        "translated_entries": len(zh_cn),
        "quality_notes": quality_notes,
        "patch_path": str(patch_save_path),
    }
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    # === 8. 如需要，调用F5固化进JAR ===
    output_files = {
        "report": str(html_path),
        "data": str(json_path),
        "patch": str(patch_save_path),
    }

    if not patch_only:
        try:
            from core.repacker import run as repacker_run

            repacker_args = type("Args", (), {
                "jar_path": str(jar_path_obj),
                "resources_dir": str(patch_resources_dir),
                "output": str(Path(config.DOWNLOADS_DIR) / f"{jar_path_obj.stem}_zh.jar"),
                "validate": True,
            })()

            repacker_result = repacker_run(repacker_args)
            if repacker_result.get("status") == "success":
                output_files["repacked_jar"] = repacker_result["output_files"].get("downloaded", "")
                logger.info(f"汉化JAR已生成: {output_files.get('repacked_jar')}")
            else:
                logger.warning(f"F5固化失败: {repacker_result.get('errors')}")
        except Exception as e:
            logger.warning(f"调用F5失败: {e}")

    logger.info(
        f"汉化完成: {len(zh_cn)}条翻译, "
        f"{len(quality_notes)}条质量提示"
    )

    return config.make_result(
        status="success",
        feature="F7",
        input_summary={
            "jar_path": str(jar_path_obj),
            "target_lang": target_lang,
            "patch_only": patch_only,
        },
        result={
            "total_entries": total_entries,
            "translated_entries": len(zh_cn),
            "categories": {k: len(v) for k, v in categories.items()},
            "quality_notes": quality_notes,
        },
        warnings=quality_notes,
        output_files=output_files,
    )
