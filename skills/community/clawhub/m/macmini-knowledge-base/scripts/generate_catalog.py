#!/usr/bin/env python3
"""
知识库标签提取脚本 - Python 全量匹配版（精简版，utils.py 已提取共享函数）
每次只处理 BATCH_SIZE 个文件，280秒超时断点，循环到全部完成
"""
import os
import json
import glob
import time
import pymupdf
import docx
import openpyxl
import pptx
import re as re_module
from utils import (
    load_cache, save_cache,
    load_progress, save_progress,
    is_gibberish,
    extract_pdf_text, extract_pdf_via_ocr,
    convert_old_office,
    extract_docx_text, extract_xlsx_text, extract_pptx_text
)

# ============== 配置 ==============
KNOWLEDGE_DIR = os.path.expanduser("~/.openclaw/workspace/knowledge")
CACHE_FILE    = os.path.join(KNOWLEDGE_DIR, ".analysis/.catalog_cache.json")
PROGRESS_FILE = os.path.join(KNOWLEDGE_DIR, ".analysis/.catalog_progress.json")
CATALOG_FILE  = os.path.join(KNOWLEDGE_DIR, "文章目录", "文章目录.md")
BATCH_SIZE    = 100
BATCH_TIMEOUT = 280

# ============== 关键词库 ==============
KEYWORDS = [
    # 中文（47个）
    '房产','房价','房地产','居民','资产负债表','消费','股市','经济','政策','利率',
    '通胀','人民币','A股','美联储','PBOC','GDP','五一','收入','储蓄','财富',
    '股票','资产','负债','资本','投资','债券','银行','企业','利润','房租',
    '租金','风险','溢价','评级','分析师','预期','复苏','周期','产能','PPI',
    'CPI','央行','流动性','美元','港币','汇率','并购','城中村','更新','改造',
    '勾地','土地','TOD','产业','租赁','港股','美股','欧洲','外贸',
    '出口','进口','制造业','PMI','社融','信贷','M2','财政','税收','就业',
    '失业','工资','零售','电商','汽车','家电','白酒','食品','医药',
    '光伏','新能源','芯片','半导体','AI','人工智能','数字经济','平台经济',
    '宏观','微观','折现率','风险溢价','大城市','北上深','日本','建筑',
    '施工','承包商','总包','分包','监理','验收','竣工','交付','成本',
    '预算','结算','审计','合同','招投标','安全','质量','进度','管理',
    # 英文（70+个）
    'property','real estate','housing','house price','home price','land','construction',
    'resident','household','consumption','consumer','stock market','equity','stock',
    'economy','economic','GDP','growth','inflation','CPI','PPI','rate','interest rate',
    'monetary','PBOC','Fed','Federal Reserve','USD','dollar','Yuan','RMB','CNY','HKD',
    'exchange rate','FX','bond','credit','bank','corporate','profit','leverage',
    'asset','liability','capital','investment','M2','money supply','liquidity',
    'fiscal','tax','revenue','budget','trade','export','import','manufacturing',
    'PMI','employment','unemployment','wage','salary','retail','e-commerce',
    'auto','automobile','EV','electric vehicle','new energy','semiconductor','chip',
    'digital economy','platform economy','FinTech','tech','urban renewal','urbanization',
    'city','metropolitan','tier-1 city','Shanghai','Shenzhen','Beijing','Guangzhou',
    'Hong Kong','Japan','REIT','TOD','industrial','park','infrastructure',
    'construction','contractor','subcontractor','supervisor','acceptance','completion',
    'cost','budget','settlement','audit','contract','bidding','safety','quality',
    'schedule','management','project','engineering','building','architect'
]

# ============== 全量文本提取（try...finally 健壮版）==============
def extract_full_text(filepath):
    """对文件执行全量文本提取，临时文件由 finally 机制保证清理"""
    ext = os.path.splitext(filepath)[1].lower()
    try:
        if ext == ".pdf":
            return extract_pdf_text(filepath)

        elif ext == ".doc":
            success, converted = convert_old_office(filepath, ext)
            if success:
                try:
                    text = extract_docx_text(converted)
                    return text
                finally:
                    try:
                        os.remove(converted)
                    except:
                        pass
            return ""

        elif ext == ".docx":
            return extract_docx_text(filepath)

        elif ext == ".xls":
            success, converted = convert_old_office(filepath, ext)
            if success:
                try:
                    text = extract_xlsx_text(converted)
                    return text
                finally:
                    try:
                        os.remove(converted)
                    except:
                        pass
            return ""

        elif ext == ".xlsx":
            return extract_xlsx_text(filepath)

        elif ext == ".ppt":
            success, converted = convert_old_office(filepath, ext)
            if success:
                try:
                    text = extract_pptx_text(converted)
                    return text
                finally:
                    try:
                        os.remove(converted)
                    except:
                        pass
            return ""

        elif ext == ".pptx":
            return extract_pptx_text(filepath)

        elif ext == ".md":
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()

        elif ext in (".txt", ".csv"):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()

        else:
            return ""

    except Exception as e:
        return ""


# ============== 关键词匹配打标签（try...finally 健壮版）==============
def extract_tags(filepath):
    ext = os.path.splitext(filepath)[1].lower()

    # PDF: pymupdf直接提取文字层，预检乱码再跳转OCR
    if ext == ".pdf":
        try:
            doc = pymupdf.open(filepath)
            text = ""
            for page_num in range(min(len(doc), 10)):
                t = doc[page_num].get_text()
                if t.strip():
                    text = text + t + "\n"
            doc.close()
            if text.strip():
                if is_gibberish(text):
                    return extract_pdf_via_ocr(filepath)
                found = list(set(kw for kw in KEYWORDS if kw in text))
                return "、".join(found[:3]) if found else "待提取"
        except:
            pass
        return extract_pdf_via_ocr(filepath)

    # .doc: 三级降级处理
    if ext == ".doc":
        # 第一级：直接用 pymupdf 尝试读取（绕过 LibreOffice，速度快）
        try:
            doc = pymupdf.open(filepath)
            text = ""
            for page_num in range(min(len(doc), 10)):
                t = doc[page_num].get_text()
                if t.strip():
                    text += t + "\n"
            doc.close()
            if text.strip() and not is_gibberish(text):
                found = list(set(kw for kw in KEYWORDS if kw in text))
                if found:
                    return "、".join(found[:3])
        except:
            pass
        
        # 第二级：LibreOffice 渐进式转换（对付复杂格式）
        success, converted = convert_old_office(filepath, ext)
        if success:
            try:
                text = extract_docx_text(converted)
                if text.strip():
                    found = list(set(kw for kw in KEYWORDS if kw in text))
                    return "、".join(found[:3]) if found else "待提取"
            finally:
                try:
                    os.remove(converted)
                except:
                    pass
        return "待提取"

    if ext == ".docx":
        text = extract_docx_text(filepath)
        if text.strip():
            found = list(set(kw for kw in KEYWORDS if kw in text))
            return "、".join(found[:3]) if found else "待提取"
        return "待提取"

    if ext == ".xls":
        success, converted = convert_old_office(filepath, ext)
        if success:
            try:
                text = extract_xlsx_text(converted)
                if text.strip():
                    found = list(set(kw for kw in KEYWORDS if kw in text))
                    return "、".join(found[:3]) if found else "待提取"
                return "待提取"
            finally:
                try:
                    os.remove(converted)
                except:
                    pass
        return "待提取"

    if ext == ".xlsx":
        text = extract_xlsx_text(filepath)
        if text.strip():
            found = list(set(kw for kw in KEYWORDS if kw in text))
            return "、".join(found[:3]) if found else "待提取"
        return "待提取"

    if ext == ".ppt":
        success, converted = convert_old_office(filepath, ext)
        if success:
            try:
                text = extract_pptx_text(converted)
                if text.strip():
                    found = list(set(kw for kw in KEYWORDS if kw in text))
                    return "、".join(found[:3]) if found else "待提取"
                return "待提取"
            finally:
                try:
                    os.remove(converted)
                except:
                    pass
        return "待提取"

    if ext == ".pptx":
        text = extract_pptx_text(filepath)
        if text.strip():
            found = list(set(kw for kw in KEYWORDS if kw in text))
            return "、".join(found[:3]) if found else "待提取"
        return "待提取"

    if ext == ".md":
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        if text.strip():
            found = list(set(kw for kw in KEYWORDS if kw in text))
            return "、".join(found[:3]) if found else "待提取"
        return "待提取"

    if ext in (".txt", ".csv"):
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        if text.strip():
            found = list(set(kw for kw in KEYWORDS if kw in text))
            return "、".join(found[:3]) if found else "待提取"
        return "待提取"

    return "待提取"


# ============== 文件扫描（独立保留）==============
def get_all_files():
    """扫描知识库所有支持的文件"""
    patterns = [
        "**/*.pdf", "**/*.doc", "**/*.docx",
        "**/*.xls", "**/*.xlsx", "**/*.ppt", "**/*.pptx",
        "**/*.md", "**/*.csv", "**/*.txt"
    ]
    files = []
    for pattern in patterns:
        for f in glob.glob(os.path.join(KNOWLEDGE_DIR, pattern), recursive=True):
            if ".analysis" not in f and ".interpret" not in f and ".storage" not in f:
                files.append(f)
    return files


# ============== 主流程（保持不变）==============
def main():
    cache = load_cache()
    progress = load_progress()
    all_files = get_all_files()
    total_start = time.time()

    for filepath in all_files:
        filename = os.path.basename(filepath)

        # 超时检测
        if time.time() - total_start > BATCH_TIMEOUT:
            save_progress(progress)
            print(f"  ⏰ 达到 {BATCH_TIMEOUT}s 超时限制，分批保存进度退出")
            break

        # 读取缓存
        tags = cache.get(filename, {}).get("tags", "")
        if tags and tags not in ("待提取", "无法提取"):
            continue
        # 无法提取的文件不再重试
        if tags == "无法提取":
            print(f"  跳过（无法提取）: {filename}")
            continue

        print(f"  提取标签: {filename}")
        tag = extract_tags(filepath)
        cache[filename] = {
            "tags": tag,
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }

    save_cache(cache)
    save_progress(progress)

    # 更新目录
    try:
        os.makedirs(os.path.dirname(CATALOG_FILE), exist_ok=True)
        with open(CATALOG_FILE, 'w', encoding='utf-8') as f:
            f.write("# 文章目录\n\n")
            for filename, info in sorted(cache.items()):
                tags = info.get("tags", "待提取")
                f.write(f"- {filename}  —  {tags}\n")
    except Exception as e:
        print(f"  ⚠️  目录写入失败: {e}")

    elapsed = time.time() - total_start
    print(f"✅ 标签提取完成，耗时 {elapsed:.1f}秒，文件数 {len(cache)}")


if __name__ == "__main__":
    main()
