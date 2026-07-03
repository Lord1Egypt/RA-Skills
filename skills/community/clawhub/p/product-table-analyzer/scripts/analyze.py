#!/usr/bin/env python3
"""
商品表市场洞察分析引擎
Market Insight Analysis Engine for Product Tables

输入：CSV 或 Excel 商品列表表格
输出：结构化 JSON 分析结果（类目分布、标题词频、价格带、卖家格局、卖点提炼、竞争度评估、综合建议）
"""

import sys
import json
import csv
import re
import math
import os
from pathlib import Path
from collections import Counter, defaultdict
from itertools import combinations

# ── 依赖检测 ──────────────────────────────────────────────
_OPENPYXL = None
_JIEBA = None


def _ensure_openpyxl():
    global _OPENPYXL
    if _OPENPYXL is None:
        try:
            import openpyxl
            _OPENPYXL = openpyxl
        except ImportError:
            print(
                "[WARN] openpyxl not installed. Excel (.xlsx) files will not be supported. "
                "Install with: pip install openpyxl",
                file=sys.stderr,
            )
    return _OPENPYXL


def _ensure_jieba():
    global _JIEBA
    if _JIEBA is None:
        try:
            import jieba
            _JIEBA = jieba
        except ImportError:
            pass  # graceful fallback
    return _JIEBA


# ── 列名智能匹配 ──────────────────────────────────────────
COLUMN_ALIASES = {
    "name": ["商品名", "标题", "名称", "产品名称", "商品名称", "品名",
             "product_name", "title", "name", "item_name", "product"],
    "price": ["价格", "售价", "单价", "定价", "成交价", "原价",
              "price", "unit_price", "selling_price", "final_price"],
    "sales": ["销量", "月销量", "累计销量", "成交数", "已售", "付款人数",
              "sales", "volume", "monthly_sales", "total_sales", "sold", "orders"],
    "shop": ["店铺", "店铺名", "卖家", "商家", "品牌", "店铺名称",
             "shop", "store", "seller", "brand", "merchant", "shop_name"],
    "category": ["类目", "分类", "品类", "商品类目", "一级类目",
                 "category", "type", "product_category"],
    "rating": ["评分", "好评率", "评价分", "rating", "score", "review_score"],
    "platform": ["平台", "来源", "platform", "source", "channel"],
    "link": ["链接", "商品链接", "URL", "link", "url", "product_url"],
}


def detect_columns(headers):
    """智能匹配列名 → 标准化字段名"""
    mapping = {}
    headers_lower = [h.strip().lower() if h else "" for h in headers]
    for std_field, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            alias_lower = alias.lower()
            for idx, h in enumerate(headers_lower):
                if idx in mapping.values():
                    continue
                # 精确匹配 or 包含匹配
                if h == alias_lower or alias_lower in h:
                    mapping[std_field] = idx
                    break
            if std_field in mapping:
                break
    return mapping


# ── 数据清洗 ──────────────────────────────────────────────
def clean_price(val):
    """清洗价格：去掉 ¥ 符号、逗号、空格，转 float"""
    if val is None:
        return None
    s = str(val).strip()
    s = re.sub(r"[¥￥,$€£\s]", "", s)
    # 处理范围价格，取低值
    s = re.split(r"[-–—~]", s)[0]
    try:
        p = float(s)
        if p < 0 or p > 100000000:
            return None
        return round(p, 2)
    except (ValueError, TypeError):
        return None


def clean_sales(val):
    """清洗销量：去掉 '万' '+', '人付款' 等，转 int"""
    if val is None:
        return None
    s = str(val).strip()
    s = s.replace(",", "").replace("，", "")
    multiplier = 1
    if "万" in s:
        multiplier = 10000
        s = s.replace("万", "")
    s = re.sub(r"[+＋人付款已售笔单件个\s]", "", s)
    try:
        n = float(s) * multiplier
        if n < 0:
            return None
        return int(n)
    except (ValueError, TypeError):
        return None


def clean_text(val):
    """清洗文本"""
    if val is None:
        return ""
    return str(val).strip()


# ── 文件读取 ──────────────────────────────────────────────
def read_csv(filepath):
    """读取 CSV 文件"""
    encodings = ["utf-8-sig", "utf-8", "gbk", "gb2312", "gb18030"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc, newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)
            if rows:
                return rows, {"encoding": enc}
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(f"无法解码 CSV 文件: {filepath}")


def read_xlsx(filepath):
    """读取 Excel 文件"""
    openpyxl = _ensure_openpyxl()
    if openpyxl is None:
        raise ImportError("需要安装 openpyxl: pip install openpyxl")
    wb = openpyxl.load_workbook(filepath, read_only=True, data_only=True)
    ws = wb.active
    rows = []
    for row in ws.iter_rows(values_only=True):
        rows.append([cell if cell is not None else "" for cell in row])
    wb.close()
    return rows


def normalize_rows(raw_rows):
    """将原始行数据标准化为 dict 列表"""
    if not raw_rows:
        return [], {}

    headers = [str(h).strip() if h else "" for h in raw_rows[0]]
    col_map = detect_columns(headers)

    records = []
    for row in raw_rows[1:]:
        record = {}
        for field, idx in col_map.items():
            if idx < len(row):
                record[field] = row[idx]
            else:
                record[field] = None
        # 跳过完全空行
        if not any(v for v in record.values() if v):
            continue
        # 清洗
        if "price" in record:
            record["price"] = clean_price(record["price"])
        if "sales" in record:
            record["sales"] = clean_sales(record["sales"])
        if "name" in record:
            record["name"] = clean_text(record["name"])
        if "shop" in record:
            record["shop"] = clean_text(record["shop"])
        if "category" in record:
            record["category"] = clean_text(record["category"])
        records.append(record)

    return records, col_map


# ── 分析函数 ──────────────────────────────────────────────

def analyze_categories(records):
    """类目分布分析"""
    categories = [r.get("category", "") for r in records if r.get("category")]
    if not categories:
        return {"available": False, "message": "表格中未检测到类目列"}

    counter = Counter(categories)
    total = len(categories)
    items = [
        {
            "category": cat,
            "count": cnt,
            "pct": round(cnt / total * 100, 1),
            "ranking": i + 1,
        }
        for i, (cat, cnt) in enumerate(counter.most_common())
    ]

    # 集中度
    top3_pct = sum(item["pct"] for item in items[:3])
    concentration = "高" if top3_pct > 70 else ("中" if top3_pct > 40 else "低")

    # 按类目统计价格和销量
    cat_details = {}
    for r in records:
        cat = r.get("category", "")
        if not cat:
            continue
        if cat not in cat_details:
            cat_details[cat] = {"prices": [], "sales": [], "count": 0}
        if r.get("price") is not None:
            cat_details[cat]["prices"].append(r["price"])
        if r.get("sales") is not None:
            cat_details[cat]["sales"].append(r["sales"])
        cat_details[cat]["count"] += 1

    for cat, detail in cat_details.items():
        prices = detail["prices"]
        sales = detail["sales"]
        detail["avg_price"] = round(sum(prices) / len(prices), 2) if prices else None
        detail["median_price"] = (
            round(sorted(prices)[len(prices) // 2], 2) if prices else None
        )
        detail["total_sales"] = sum(sales) if sales else None
        detail["avg_sales"] = round(sum(sales) / len(sales), 1) if sales else None
        del detail["prices"]
        del detail["sales"]

    return {
        "available": True,
        "total_categories": len(counter),
        "top3_concentration_pct": round(top3_pct, 1),
        "concentration_level": concentration,
        "distribution": items,
        "category_details": cat_details,
    }


def analyze_title_keywords(records, top_n=50):
    """标题词频与卖点分析"""
    titles = [r.get("name", "") for r in records if r.get("name")]
    if not titles:
        return {"available": False, "message": "表格中未检测到商品名称列"}

    # 中文分词
    jieba = _ensure_jieba()
    all_words = []
    if jieba:
        # 加载自定义词典（常见电商词）
        ecommerce_words = [
            "充电宝", "移动电源", "数据线", "无线耳机", "蓝牙音箱",
            "加厚", "加绒", "纯棉", "透气", "防滑", "防水", "耐磨",
            "大容量", "快充", "便携", "多功能", "智能", "高清",
            "2024", "2025", "2026", "新款", "爆款", "旗舰", "升级",
            "USB-C", "Type-C", "RGB", "LED", "IPS", "LCD",
        ]
        for w in ecommerce_words:
            jieba.add_word(w)

        for title in titles:
            words = jieba.cut(title)
            all_words.extend([w.strip() for w in words if len(w.strip()) >= 2])
    else:
        # fallback: 按常见分隔符切词
        for title in titles:
            parts = re.split(r"[\s\-/|（）()【】\[\]【】·、，。！？,!?]+", title)
            all_words.extend([p.strip() for p in parts if len(p.strip()) >= 2])

    # 停用词
    stopwords = {
        "商品", "产品", "一个", "这个", "那个", "可以", "使用", "用于",
        "能够", "过来", "起来", "什么", "怎么", "哪些", "进行", "通过",
        "以及", "还有", "其他", "其它", "各种", "不同", "一种", "一些",
        "就是", "不是", "还是", "或者", "因为", "所以", "但是",
        "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
        "都", "一", "这", "他", "之", "与", "及", "可", "为", "也",
        "等", "你", "要", "中", "上", "下", "大", "小", "来", "去",
        "很", "会", "能", "没", "对", "从", "到", "让", "给", "被",
        "吧", "吗", "呢", "啊", "哦", "嗯", "哈",
    }

    filtered = [w for w in all_words if w not in stopwords]
    word_freq = Counter(filtered)

    # 高频词
    top_words = [
        {"word": word, "count": cnt, "pct": round(cnt / len(titles) * 100, 1)}
        for word, cnt in word_freq.most_common(top_n)
    ]

    # 卖点词识别（功能/材质/场景类词汇）
    selling_point_keywords = {
        "材质": ["纯棉", "涤纶", "尼龙", "真皮", "硅胶", "不锈钢", "铝合金", "塑料",
                "玻璃", "陶瓷", "木质", "竹制", "碳纤维", "钛合金", "纳米"],
        "功能": ["防水", "防滑", "耐磨", "透气", "加厚", "加绒", "保温", "速干",
                "抗菌", "防霉", "防晒", "隔音", "减震", "防摔", "可折叠", "可拆卸"],
        "场景": ["户外", "家用", "办公", "旅行", "车载", "厨房", "浴室", "卧室",
                "客厅", "露营", "运动", "健身", "学生", "儿童", "老人"],
        "属性": ["大容量", "迷你", "便携", "轻便", "静音", "智能", "自动", "手动",
                "电动", "充电", "无线", "蓝牙", "USB", "快充", "闪充"],
    }

    discovered_selling_points = defaultdict(list)
    for word, _ in word_freq.most_common(top_n * 2):
        for sp_type, sp_words in selling_point_keywords.items():
            if word in sp_words:
                discovered_selling_points[sp_type].append(word)

    selling_points = {
        sp_type: {
            "words": words,
            "count": len(words),
            "summary": "、".join(words[:5]),
        }
        for sp_type, words in discovered_selling_points.items()
    }

    return {
        "available": True,
        "total_titles": len(titles),
        "total_unique_words": len(word_freq),
        "top_words": top_words,
        "selling_points": selling_points,
    }


def analyze_price_bands(records):
    """价格带分析"""
    prices = [r.get("price") for r in records if r.get("price") is not None]
    if not prices:
        return {"available": False, "message": "表格中未检测到有效价格数据"}

    prices_sorted = sorted(prices)
    n = len(prices_sorted)

    stats = {
        "count": n,
        "min": prices_sorted[0],
        "max": prices_sorted[-1],
        "mean": round(sum(prices_sorted) / n, 2),
        "median": round(prices_sorted[n // 2], 2),
        "p25": round(prices_sorted[n // 4], 2),
        "p75": round(prices_sorted[3 * n // 4], 2),
    }

    # 自动分段（按分布密度智能分段）
    if stats["max"] == stats["min"]:
        bands = [{
            "range": f"{stats['min']}元",
            "min": stats["min"],
            "max": stats["max"],
            "count": n,
            "pct": 100.0,
        }]
    else:
        # 使用等频分段（每个段大致等量商品）
        num_bands = min(10, n)
        band_size = n // num_bands
        bands = []
        for i in range(num_bands):
            start_idx = i * band_size
            end_idx = (i + 1) * band_size if i < num_bands - 1 else n
            segment = prices_sorted[start_idx:end_idx]
            band_min = segment[0]
            band_max = segment[-1]
            cnt = len(segment)
            band_range = (
                f"{band_min:.0f}-{band_max:.0f}元"
                if band_min != band_max
                else f"{band_min:.0f}元"
            )
            bands.append({
                "range": band_range,
                "min": band_min,
                "max": band_max,
                "count": cnt,
                "pct": round(cnt / n * 100, 1),
            })

    # 价格-销量关联分析
    price_sales = []
    for r in records:
        if r.get("price") is not None and r.get("sales") is not None:
            price_sales.append((r["price"], r["sales"]))

    price_sales_correlation = None
    if len(price_sales) > 10:
        # 简单相关性：按价格带分组看销量
        price_buckets = defaultdict(list)
        for p, s in price_sales:
            bucket = int(p / 10) * 10  # 每10元一档
            price_buckets[bucket].append(s)
        bucket_avgs = {
            b: round(sum(sl) / len(sl), 1)
            for b, sl in sorted(price_buckets.items())
        }
        # 找销量最高的价格带
        if bucket_avgs:
            best_bucket = max(bucket_avgs, key=bucket_avgs.get)
            price_sales_correlation = {
                "best_price_range": f"{best_bucket}-{best_bucket + 9}元",
                "best_avg_sales": bucket_avgs[best_bucket],
                "bucket_details": [
                    {"range": f"{b}-{b+9}元", "avg_sales": s, "product_count": len(price_buckets[b])}
                    for b, s in sorted(bucket_avgs.items())
                ],
            }

    return {
        "available": True,
        "stats": stats,
        "bands": bands,
        "price_sales_correlation": price_sales_correlation,
    }


def analyze_sellers(records):
    """卖家/品牌格局分析"""
    shops = [r.get("shop", "") for r in records if r.get("shop")]
    if not shops:
        return {"available": False, "message": "表格中未检测到店铺/品牌列"}

    counter = Counter(shops)
    total = len(shops)
    total_shops = len(counter)

    # 集中度指标
    top_shops = counter.most_common(min(10, total_shops))
    cr4 = sum(cnt for _, cnt in top_shops[:4]) / total * 100 if len(top_shops) >= 4 else None
    cr10 = sum(cnt for _, cnt in top_shops[:10]) / total * 100

    # 按店铺统计
    shop_details = []
    for shop, cnt in top_shops:
        shop_records = [r for r in records if r.get("shop") == shop]
        prices = [r["price"] for r in shop_records if r.get("price") is not None]
        sales_list = [r["sales"] for r in shop_records if r.get("sales") is not None]
        shop_details.append({
            "shop": shop,
            "product_count": cnt,
            "pct": round(cnt / total * 100, 1),
            "avg_price": round(sum(prices) / len(prices), 2) if prices else None,
            "median_price": round(sorted(prices)[len(prices) // 2], 2) if prices and len(prices) > 1 else (prices[0] if prices else None),
            "total_sales": sum(sales_list) if sales_list else None,
            "avg_sales": round(sum(sales_list) / len(sales_list), 1) if sales_list else None,
            "price_range": f"{min(prices):.0f}-{max(prices):.0f}元" if prices and len(prices) > 1 else (f"{prices[0]:.0f}元" if prices else "N/A"),
        })

    # 竞争格局分类
    if cr4 and cr4 > 60:
        landscape = "高度集中（寡头格局）"
    elif cr4 and cr4 > 30:
        landscape = "中度集中"
    else:
        landscape = "分散竞争"

    return {
        "available": True,
        "total_shops": total_shops,
        "total_products": total,
        "cr4_pct": round(cr4, 1) if cr4 else None,
        "cr10_pct": round(cr10, 1),
        "landscape": landscape,
        "top_shops": shop_details,
    }


def analyze_competition(records):
    """综合竞争度评估"""
    n = len(records)
    scores = {}

    # 1. 卖家集中度
    shops = [r.get("shop", "") for r in records if r.get("shop")]
    if shops:
        shop_counter = Counter(shops)
        hhi = sum((cnt / n) ** 2 for cnt in shop_counter.values()) * 10000
        if hhi > 2500:
            scores["seller_concentration"] = {"level": "高", "hhi": round(hhi, 0), "desc": "市场被少数大卖把控，新进入难度大"}
        elif hhi > 1500:
            scores["seller_concentration"] = {"level": "中", "hhi": round(hhi, 0), "desc": "存在头部卖家但仍有空间"}
        else:
            scores["seller_concentration"] = {"level": "低", "hhi": round(hhi, 0), "desc": "市场分散，新进入机会大"}

    # 2. 价格竞争激烈度
    prices = [r["price"] for r in records if r.get("price") is not None]
    if len(prices) > 1:
        mean_p = sum(prices) / len(prices)
        cv = (math.sqrt(sum((p - mean_p) ** 2 for p in prices) / len(prices)) / mean_p) * 100
        if cv < 20:
            scores["price_variance"] = {"level": "低", "cv_pct": round(cv, 1), "desc": "价格趋同，利润空间透明"}
        elif cv < 50:
            scores["price_variance"] = {"level": "中", "cv_pct": round(cv, 1), "desc": "价格有一定分化空间"}
        else:
            scores["price_variance"] = {"level": "高", "cv_pct": round(cv, 1), "desc": "价格差异大，存在溢价机会"}

    # 3. 综合评估
    levels = {
        "seller_concentration": scores.get("seller_concentration", {}).get("level"),
        "price_variance": scores.get("price_variance", {}).get("level"),
    }

    high_count = sum(1 for v in levels.values() if v == "高")
    low_count = sum(1 for v in levels.values() if v == "低")

    if high_count >= 2:
        overall = "红海市场 — 竞争激烈，卖家集中且价格透明"
    elif low_count >= 2:
        overall = "蓝海机会 — 市场分散，价格有空间，适合切入"
    else:
        overall = "中性市场 — 有竞争但存在差异化空间"

    return {
        "overall": overall,
        "dimensions": scores,
    }


def generate_recommendations(results):
    """综合所有分析维度，生成选品建议"""
    recs = []

    # 竞争度建议
    comp = results.get("competition", {})
    if "红海" in comp.get("overall", ""):
        recs.append({
            "priority": "P1",
            "type": "竞争策略",
            "title": "红海突围：差异化是关键",
            "detail": "市场竞争激烈，建议从功能差异化、细分场景切入，或寻找未被满足的价格带。",
        })
    elif "蓝海" in comp.get("overall", ""):
        recs.append({
            "priority": "P1",
            "type": "入场时机",
            "title": "蓝海窗口：尽快入场",
            "detail": "市场分散、竞争度低，建议快速布局，抢占品类心智。",
        })

    # 价格带建议
    price_data = results.get("price_bands", {})
    if price_data.get("available"):
        corr = price_data.get("price_sales_correlation")
        if corr:
            recs.append({
                "priority": "P1",
                "type": "定价策略",
                "title": f"最佳价格带：{corr['best_price_range']}",
                "detail": f"该价格带平均销量最高（{corr['best_avg_sales']}件），建议定价在此区间。",
            })
        stats = price_data.get("stats", {})
        if stats:
            recs.append({
                "priority": "P2",
                "type": "价格布局",
                "title": f"价格覆盖建议",
                "detail": f"当前市场均价{stats.get('mean', 'N/A')}元，中位数{stats.get('median', 'N/A')}元。"
                         f"建议主攻{stats.get('p25', 'N/A')}-{stats.get('p75', 'N/A')}元价格带，覆盖主流消费力。",
            })

    # 卖点建议
    kw_data = results.get("keywords", {})
    if kw_data.get("available"):
        sp = kw_data.get("selling_points", {})
        if sp:
            sp_summary = []
            for sp_type, info in sp.items():
                sp_summary.append(f"{sp_type}: {info['summary']}")
            recs.append({
                "priority": "P2",
                "type": "卖点策略",
                "title": "热门卖点方向",
                "detail": " | ".join(sp_summary) + "。建议标题覆盖这些高频卖点词。",
            })

    # 类目建议
    cat_data = results.get("categories", {})
    if cat_data.get("available"):
        cats = cat_data.get("distribution", [])
        if len(cats) > 3:
            small_cats = [c for c in cats if c["pct"] < 15]
            if small_cats:
                recs.append({
                    "priority": "P2",
                    "type": "类目机会",
                    "title": "细分品类机会",
                    "detail": f"以下品类占比较低但可能存在蓝海机会: {', '.join(c['category'] for c in small_cats[:3])}。建议评估这些品类的竞争度和利润空间。",
                })

    return recs


# ── 主流程 ─────────────────────────────────────────────────

def analyze(filepath):
    """主分析入口"""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {filepath}")

    ext = path.suffix.lower()
    if ext in (".csv", ".txt"):
        raw_rows, meta = read_csv(str(path))
    elif ext in (".xlsx", ".xls"):
        raw_rows = read_xlsx(str(path))
        meta = {"format": ext}
    else:
        raise ValueError(f"不支持的文件格式: {ext}，请使用 CSV 或 Excel 文件")

    records, col_map = normalize_rows(raw_rows)

    if len(records) < 3:
        return {
            "error": True,
            "message": f"有效数据行数不足（仅 {len(records)} 行），至少需要 3 行数据进行分析。",
            "records": records,
        }

    # 执行各维度分析
    results = {
        "meta": {
            "file": str(path.name),
            "rows": len(raw_rows) - 1,
            "valid_records": len(records),
            "detected_columns": {
                std: raw_rows[0][idx] if idx < len(raw_rows[0]) else "?"
                for std, idx in col_map.items()
            },
            "encoding": meta.get("encoding", "N/A"),
        },
        "categories": analyze_categories(records),
        "keywords": analyze_title_keywords(records),
        "price_bands": analyze_price_bands(records),
        "sellers": analyze_sellers(records),
        "competition": analyze_competition(records),
    }
    results["recommendations"] = generate_recommendations(results)

    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python analyze.py <商品表文件.csv|xlsx>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        results = analyze(filepath)
    except Exception as e:
        results = {"error": True, "message": str(e)}

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
