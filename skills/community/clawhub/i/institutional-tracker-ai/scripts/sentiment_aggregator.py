"""
外部分析素材情绪聚合模块 v2.0
整合多源高质量分析内容，生成市场情绪分数用于宏观环境判断
新增: 散户过热检测 (东方财富人气指数 = 小红书/抖音的量化替代)

数据源:
1. YouTube 财经博主（通过RSS无需API Key）
2. 东方财富股吧情绪（AKShare接口）
3. 东方财富/新浪财经资讯（关键词情绪分析）
4. 东方财富热股趋势（市场关注度）
5. 东方财富人气指数（散户关注度 = 小红书/抖音过热的量化代理）

输出:
- sentiment_score (-100 ~ +100)，集成到 market_regime 作为补充维度
- stock_overheat_map: 个股级别过热信号，集成到 signal_engine 作为惩罚因子
"""
import re
import os
import time
import json
import urllib.request
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta


# ============================================================
# 配置：高质量频道和关键词库
# ============================================================

# YouTube 财经频道（通过RSS免费获取，无需API Key）
# channel_id 需要准确，否则404
YOUTUBE_CHANNELS = {
    # 英文主流财经频道
    "CNBC": "UCvJJ_dzjViJCoLf5uKUTwoA",
    "Wall Street Journal": "UCK7tptUDHh-RYDsdxO1-5QQ",
    # 可以在这里添加更多验证过的频道
    # "Bloomberg": "UCIALMKvObZNtJ6AmdCLP7Lg",  # 有时404
}

# 中文财经关键词情绪字典
# 看涨关键词（权重从高到低）
BULLISH_KEYWORDS = {
    # 强看涨
    "暴涨": 3, "大涨": 3, "涨停": 3, "牛市": 3, "强势": 2.5,
    "突破": 2, "创新高": 2.5, "利好": 2, "爆发": 2.5, "起飞": 2,
    # 中等看涨
    "上涨": 1.5, "回暖": 1.5, "反弹": 1.5, "看多": 2, "做多": 2,
    "加仓": 1.5, "买入": 1.5, "抄底": 1.5, "底部": 1.5, "启动": 1.5,
    "金叉": 1.5, "放量": 1, "资金流入": 2, "北向买入": 2,
    # 轻度看涨
    "稳定": 0.5, "企稳": 1, "止跌": 1, "修复": 1, "机会": 1,
    "配置": 0.5, "价值": 0.5, "低估": 1, "景气": 1, "复苏": 1.5,
}

# 看跌关键词
BEARISH_KEYWORDS = {
    # 强看跌
    "暴跌": -3, "大跌": -3, "崩盘": -3, "熊市": -3, "跌停": -3,
    "黑天鹅": -2.5, "恐慌": -2.5, "踩踏": -2.5, "爆仓": -2.5,
    # 中等看跌
    "下跌": -1.5, "回调": -1, "看空": -2, "做空": -2, "减仓": -1.5,
    "卖出": -1.5, "出货": -2, "逃顶": -2, "高位": -1, "见顶": -2,
    "死叉": -1.5, "缩量": -1, "资金流出": -2, "北向卖出": -2,
    # 轻度看跌
    "风险": -1, "谨慎": -1, "观望": -0.5, "压力": -1, "利空": -2,
    "套牢": -1.5, "割肉": -1.5, "亏损": -1, "衰退": -2, "滞胀": -2,
}

# 英文关键词（用于YouTube英文频道）
EN_BULLISH = {
    "rally": 2, "surge": 3, "bull": 2.5, "breakout": 2, "record high": 3,
    "boom": 2.5, "recovery": 1.5, "growth": 1, "gain": 1.5, "soar": 3,
    "buy": 1.5, "opportunity": 1, "upside": 1.5, "optimism": 1.5,
}

EN_BEARISH = {
    "crash": -3, "plunge": -3, "bear": -2.5, "collapse": -3, "recession": -2.5,
    "sell-off": -2.5, "selloff": -2.5, "fear": -2, "risk": -1, "decline": -1.5,
    "drop": -1.5, "fall": -1, "warning": -1.5, "crisis": -2.5, "bubble": -2,
    "tariff": -1.5, "trade war": -2, "inflation": -1, "rate hike": -1.5,
}


# ============================================================
# 数据采集函数
# ============================================================

def fetch_youtube_sentiment(max_channels: int = 5) -> Dict:
    """
    通过YouTube RSS获取财经频道最新视频标题，分析情绪倾向
    
    返回:
        {
            "score": float (-100~100),
            "reason": str,
            "videos_analyzed": int,
            "details": list
        }
    """
    all_titles = []
    details = []
    
    for channel_name, channel_id in list(YOUTUBE_CHANNELS.items())[:max_channels]:
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode()
                root = ET.fromstring(content)
                ns = {"atom": "http://www.w3.org/2005/Atom"}
                entries = root.findall("atom:entry", ns)
                
                # 只取最近7天的视频
                cutoff = (datetime.now() - timedelta(days=7)).isoformat()
                recent = []
                for e in entries:
                    pub = e.find("atom:published", ns)
                    title_el = e.find("atom:title", ns)
                    if pub is not None and title_el is not None:
                        if pub.text >= cutoff[:10]:
                            title = title_el.text or ""
                            recent.append(title)
                            all_titles.append(title)
                
                if recent:
                    details.append(f"{channel_name}: {len(recent)}个视频")
        except Exception:
            pass
        time.sleep(0.3)
    
    if not all_titles:
        return {"score": 0, "reason": "YouTube数据获取失败", "videos_analyzed": 0, "details": []}
    
    # 用英文关键词分析
    total_sentiment = 0
    hit_count = 0
    
    for title in all_titles:
        title_lower = title.lower()
        for kw, weight in EN_BULLISH.items():
            if kw in title_lower:
                total_sentiment += weight
                hit_count += 1
        for kw, weight in EN_BEARISH.items():
            if kw in title_lower:
                total_sentiment += weight  # 已是负值
                hit_count += 1
    
    # 归一化到 -100 ~ 100
    if hit_count > 0:
        avg = total_sentiment / max(1, len(all_titles))
        score = max(-100, min(100, avg * 30))  # 放大系数
    else:
        score = 0
    
    direction = "偏多" if score > 10 else "偏空" if score < -10 else "中性"
    reason = f"YouTube {len(all_titles)}个视频分析→{direction}({score:+.0f})"
    
    return {
        "score": round(score, 1),
        "reason": reason,
        "videos_analyzed": len(all_titles),
        "details": details,
    }


def fetch_eastmoney_sentiment() -> Dict:
    """
    通过AKShare获取东方财富股吧市场情绪
    
    使用 stock_comment_em() 获取全市场个股情绪数据，
    计算看涨比例作为市场整体情绪指标
    
    返回:
        {
            "score": float (-100~100),
            "reason": str,
            "bullish_pct": float,
            "total_stocks": int
        }
    """
    try:
        import akshare as ak
        
        # 东方财富股吧人气/情绪
        df = ak.stock_comment_em()
        if df is None or df.empty:
            return {"score": 0, "reason": "东方财富情绪数据为空", "bullish_pct": 50, "total_stocks": 0}
        
        total = len(df)
        
        # 使用"涨跌幅"列判断市场情绪
        # 以及"换手率"等列判断活跃度
        if "涨跌幅" in df.columns:
            df_valid = df[df["涨跌幅"].notna()]
            if len(df_valid) > 0:
                up_count = (df_valid["涨跌幅"] > 0).sum()
                down_count = (df_valid["涨跌幅"] < 0).sum()
                total_valid = len(df_valid)
                
                up_pct = up_count / total_valid * 100 if total_valid > 0 else 50
                
                # 同时看平均涨跌幅
                avg_change = df_valid["涨跌幅"].mean()
                
                # 综合评分
                # up_pct: 70%+ 看涨, 30%- 看跌
                ratio_score = (up_pct - 50) * 2  # 50%时=0, 70%时=40, 30%时=-40
                change_score = avg_change * 20    # 平均涨1%=20分
                
                score = max(-100, min(100, ratio_score * 0.6 + change_score * 0.4))
                
                reason = f"全市场上涨{up_pct:.0f}%(涨{up_count}/跌{down_count})，均涨{avg_change:+.2f}%"
                return {
                    "score": round(score, 1),
                    "reason": reason,
                    "bullish_pct": round(up_pct, 1),
                    "total_stocks": total_valid,
                }
        
        return {"score": 0, "reason": "东方财富数据格式异常", "bullish_pct": 50, "total_stocks": total}
        
    except Exception as e:
        return {"score": 0, "reason": f"东方财富接口异常: {str(e)[:50]}", "bullish_pct": 50, "total_stocks": 0}


def fetch_news_sentiment() -> Dict:
    """
    通过AKShare获取财经新闻标题，用关键词进行情绪分析
    
    整合:
    - 东方财富全球资讯 (stock_info_global_em)
    - 新浪财经全球新闻 (stock_info_global_sina)
    
    返回:
        {
            "score": float (-100~100),
            "reason": str,
            "articles_analyzed": int,
            "key_headlines": list
        }
    """
    titles = []
    key_headlines = []
    
    try:
        import akshare as ak
        
        # 东方财富全球资讯
        try:
            df = ak.stock_info_global_em()
            if df is not None and not df.empty:
                # 找标题列
                title_col = None
                for col in ["标题", "title", df.columns[0]]:
                    if col in df.columns:
                        title_col = col
                        break
                if title_col is None and len(df.columns) > 0:
                    title_col = df.columns[0]
                
                if title_col:
                    for _, row in df.head(50).iterrows():
                        t = str(row.get(title_col, ""))
                        if t and len(t) > 5:
                            titles.append(t)
        except Exception:
            pass
        
        # 新浪财经全球
        try:
            df = ak.stock_info_global_sina()
            if df is not None and not df.empty:
                title_col = None
                for col in ["title", "标题", df.columns[0]]:
                    if col in df.columns:
                        title_col = col
                        break
                if title_col is None and len(df.columns) > 0:
                    title_col = df.columns[0]
                    
                if title_col:
                    for _, row in df.head(20).iterrows():
                        t = str(row.get(title_col, ""))
                        if t and len(t) > 5:
                            titles.append(t)
        except Exception:
            pass
            
    except ImportError:
        return {"score": 0, "reason": "akshare未安装", "articles_analyzed": 0, "key_headlines": []}
    
    if not titles:
        return {"score": 0, "reason": "未获取到新闻标题", "articles_analyzed": 0, "key_headlines": []}
    
    # 关键词情绪分析
    total_sentiment = 0
    strong_signals = []
    
    for title in titles:
        title_score = 0
        for kw, weight in BULLISH_KEYWORDS.items():
            if kw in title:
                title_score += weight
        for kw, weight in BEARISH_KEYWORDS.items():
            if kw in title:
                title_score += weight  # 已是负值
        
        # 英文标题也分析
        title_lower = title.lower()
        for kw, weight in EN_BULLISH.items():
            if kw in title_lower:
                title_score += weight
        for kw, weight in EN_BEARISH.items():
            if kw in title_lower:
                title_score += weight
        
        total_sentiment += title_score
        
        # 记录强信号标题
        if abs(title_score) >= 3:
            strong_signals.append((title[:40], title_score))
    
    # 归一化
    avg = total_sentiment / len(titles)
    score = max(-100, min(100, avg * 25))
    
    # 取最显著的3条标题
    strong_signals.sort(key=lambda x: abs(x[1]), reverse=True)
    key_headlines = [f"{'📈' if s > 0 else '📉'} {t}" for t, s in strong_signals[:3]]
    
    direction = "偏多" if score > 10 else "偏空" if score < -10 else "中性"
    reason = f"财经新闻{len(titles)}条分析→{direction}({score:+.0f})"
    
    return {
        "score": round(score, 1),
        "reason": reason,
        "articles_analyzed": len(titles),
        "key_headlines": key_headlines,
    }


def fetch_hot_stock_momentum() -> Dict:
    """
    通过东方财富热股排名，分析市场热度和方向
    
    逻辑:
    - 热门股整体上涨 → 市场热情高
    - 热门股整体下跌 → 市场恐慌
    - 热股换手率 → 活跃度
    
    返回:
        {
            "score": float (-100~100),
            "reason": str,
            "top_hot": list,
            "avg_change": float
        }
    """
    try:
        import akshare as ak
        
        df = ak.stock_hot_rank_em()
        if df is None or df.empty:
            return {"score": 0, "reason": "热股数据为空", "top_hot": [], "avg_change": 0}
        
        # 取前50只热股分析
        hot50 = df.head(50)
        
        # 获取涨跌幅
        if "涨跌幅" in hot50.columns:
            valid = hot50[hot50["涨跌幅"].notna()]
            if len(valid) > 0:
                avg_change = valid["涨跌幅"].mean()
                up_pct = (valid["涨跌幅"] > 0).sum() / len(valid) * 100
                
                # 热股中涨停占比
                limit_up = (valid["涨跌幅"] >= 9.5).sum()
                limit_down = (valid["涨跌幅"] <= -9.5).sum()
                
                # 评分
                change_score = avg_change * 15
                ratio_score = (up_pct - 50) * 1.5
                limit_bonus = limit_up * 5 - limit_down * 8
                
                score = max(-100, min(100, change_score * 0.5 + ratio_score * 0.3 + limit_bonus * 0.2))
                
                top_hot = []
                for _, row in hot50.head(5).iterrows():
                    name = row.get("股票名称", row.get("名称", ""))
                    chg = row.get("涨跌幅", 0)
                    if name:
                        top_hot.append(f"{name}({chg:+.1f}%)" if chg else str(name))
                
                reason = f"热股50均涨{avg_change:+.2f}%(涨{up_pct:.0f}%),涨停{limit_up}/跌停{limit_down}"
                return {
                    "score": round(score, 1),
                    "reason": reason,
                    "top_hot": top_hot,
                    "avg_change": round(avg_change, 2),
                }
        
        return {"score": 0, "reason": "热股数据无涨跌幅列", "top_hot": [], "avg_change": 0}
        
    except Exception as e:
        return {"score": 0, "reason": f"热股接口异常: {str(e)[:50]}", "top_hot": [], "avg_change": 0}


# ============================================================
# 散户过热检测 (v2新增)
# 逻辑: 东方财富人气指数 = 散户关注度的最佳量化代理
# 类似小红书/抖音股票话题热度，但数据更结构化
# ============================================================

def detect_stock_overheat(ts_code: str) -> Dict:
    """
    检测单只股票是否被散户过度关注（过热信号）
    
    使用东方财富人气指数历史数据，检测:
    1. 人气排名突然飙升 → 散户涌入
    2. 人气维持高位 → 可能过热
    3. 关联热搜词中出现"买入""暴涨"等 → FOMO情绪
    
    参数:
        ts_code: 股票代码 (如 "300750.SZ")
        
    返回:
        {
            "is_overheated": bool,
            "overheat_score": float (0~100, 越高越过热),
            "reason": str,
            "popularity_rank": int,
            "fomo_keywords": list
        }
    """
    # 转换代码格式: 300750.SZ -> SZ300750
    if "." in ts_code:
        parts = ts_code.split(".")
        em_code = parts[1] + parts[0]  # SZ300750
    else:
        em_code = ts_code
    
    overheat_score = 0
    reasons = []
    fomo_keywords = []
    popularity_rank = -1
    
    try:
        import akshare as ak
        
        # 1. 检查是否在热股TOP100
        try:
            hot_df = ak.stock_hot_rank_em()
            if hot_df is not None and not hot_df.empty:
                code_col = "股票代码" if "股票代码" in hot_df.columns else hot_df.columns[1]
                match = hot_df[hot_df[code_col].astype(str) == em_code]
                if not match.empty:
                    rank_col = "排名" if "排名" in hot_df.columns else hot_df.columns[0]
                    popularity_rank = int(match.iloc[0][rank_col])
                    
                    if popularity_rank <= 10:
                        overheat_score += 40
                        reasons.append(f"散户关注TOP{popularity_rank}!")
                    elif popularity_rank <= 30:
                        overheat_score += 25
                        reasons.append(f"散户关注TOP{popularity_rank}")
                    elif popularity_rank <= 50:
                        overheat_score += 15
                        reasons.append(f"散户关注TOP{popularity_rank}")
                    elif popularity_rank <= 100:
                        overheat_score += 5
                        reasons.append(f"散户关注TOP{popularity_rank}")
        except Exception:
            pass
        
        # 2. 检查人气趋势（突然飙升 = 散户涌入）
        try:
            detail_df = ak.stock_hot_rank_detail_em(symbol=em_code)
            if detail_df is not None and len(detail_df) >= 30:
                # 取最近7天vs30天均值对比
                rank_col = "排名" if "排名" in detail_df.columns else detail_df.columns[1]
                recent_7d = detail_df.head(7)[rank_col].mean()
                avg_30d = detail_df.head(30)[rank_col].mean()
                
                # 排名越小越热门，排名下降=关注度飙升
                if avg_30d > 0:
                    rank_change_pct = (avg_30d - recent_7d) / avg_30d * 100
                    
                    if rank_change_pct > 50:  # 排名提升50%以上
                        overheat_score += 30
                        reasons.append(f"7日人气飙升{rank_change_pct:.0f}%(排名{avg_30d:.0f}→{recent_7d:.0f})")
                    elif rank_change_pct > 25:
                        overheat_score += 15
                        reasons.append(f"7日人气升{rank_change_pct:.0f}%")
                    elif rank_change_pct < -30:
                        # 人气下降 = 热度退潮
                        overheat_score -= 10
                        reasons.append(f"人气下降{abs(rank_change_pct):.0f}%")
        except Exception:
            pass
        
        # 3. 检查关联热搜词（FOMO情绪识别）
        try:
            kw_df = ak.stock_hot_keyword_em(symbol=em_code)
            if kw_df is not None and not kw_df.empty:
                kw_col = None
                for col in kw_df.columns:
                    if "关键" in str(col) or "概念" in str(col) or "板块" in str(col):
                        kw_col = col
                        break
                if kw_col is None and len(kw_df.columns) >= 3:
                    kw_col = kw_df.columns[2]
                
                if kw_col:
                    hot_kws = kw_df[kw_col].tolist()[:10]
                    fomo_words = ["暴涨", "涨停", "牛股", "翻倍", "起飞", "买入", "龙头"]
                    for kw in hot_kws:
                        kw_str = str(kw)
                        for fw in fomo_words:
                            if fw in kw_str:
                                fomo_keywords.append(kw_str)
                                overheat_score += 5
                    
                    if fomo_keywords:
                        reasons.append(f"FOMO热词:{','.join(fomo_keywords[:3])}")
        except Exception:
            pass
        
    except ImportError:
        pass
    
    overheat_score = min(100, max(0, overheat_score))
    is_overheated = overheat_score >= 40
    
    if not reasons:
        reasons = ["散户关注度正常"]
    
    return {
        "is_overheated": is_overheated,
        "overheat_score": overheat_score,
        "reason": "；".join(reasons),
        "popularity_rank": popularity_rank,
        "fomo_keywords": fomo_keywords,
    }


def fetch_xiaohongshu_sentiment(keywords: List[str] = None) -> Dict:
    """
    小红书散户情绪检测（通过cookie直接搜索）
    
    注意: 需要小红书cookies且需要X-S签名，当前为降级实现:
    - 如果MCP可用，通过MCP搜索
    - 否则返回空结果，由东方财富人气指数替代
    
    返回:
        {
            "score": float (-100~100),
            "reason": str,
            "hot_posts": int,
            "available": bool
        }
    """
    if keywords is None:
        keywords = ["A股", "股票", "基金定投"]
    
    # 尝试通过MCP搜索
    import subprocess
    mcp_script = os.path.expanduser("~/.workbuddy/skills/xiaohongshu/scripts/search.sh")
    
    if os.path.exists(mcp_script):
        try:
            result = subprocess.run(
                [mcp_script, "A股 买入"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and result.stdout.strip():
                output = result.stdout
                # 尝试解析JSON
                import json as _json
                idx = output.find("{")
                if idx >= 0:
                    data = _json.loads(output[idx:])
                    items = data.get("result", [])
                    if items:
                        # 分析帖子标题情绪
                        total = len(items)
                        bullish = sum(1 for it in items
                                     if any(w in str(it.get("title", "")) for w in ["涨", "买", "牛", "翻倍"]))
                        bearish = sum(1 for it in items
                                     if any(w in str(it.get("title", "")) for w in ["跌", "割", "亏", "套"]))
                        
                        if total > 0:
                            bias = (bullish - bearish) / total * 100
                            score = max(-100, min(100, bias * 2))
                            return {
                                "score": round(score, 1),
                                "reason": f"小红书{total}条,看涨{bullish}/看跌{bearish}",
                                "hot_posts": total,
                                "available": True,
                            }
        except Exception:
            pass
    
    # 降级: 小红书不可用，标记等待MCP修复
    return {
        "score": 0,
        "reason": "小红书MCP未就绪(macOS无Xvfb),由东方财富人气指数替代",
        "hot_posts": 0,
        "available": False,
    }


# ============================================================
# 主聚合函数
# ============================================================

def aggregate_external_sentiment(include_youtube: bool = True,
                                  include_eastmoney: bool = True,
                                  include_news: bool = True,
                                  include_hot_stocks: bool = True,
                                  include_xiaohongshu: bool = True) -> Dict:
    """
    聚合所有外部情绪数据源，输出综合情绪分数
    
    权重分配:
    - 东方财富股吧情绪: 30% (最直接的市场情绪)
    - 热股动量: 25% (市场热度)
    - 财经新闻: 20% (媒体/分析师观点)
    - YouTube博主: 15% (国际视角补充)
    - 小红书散户情绪: 10% (社交媒体反向指标)
    
    返回:
        {
            "sentiment_score": float (-100~100),
            "sentiment_label": str,
            "sources": dict (各源详情),
            "key_signals": list (关键信号摘要),
            "confidence": float (置信度, 基于有效数据源数量)
        }
    """
    sources = {}
    weights = {}
    
    # 1. 东方财富市场情绪
    if include_eastmoney:
        em = fetch_eastmoney_sentiment()
        sources["eastmoney"] = em
        weights["eastmoney"] = 0.30
    
    # 2. 热股动量
    if include_hot_stocks:
        hot = fetch_hot_stock_momentum()
        sources["hot_stocks"] = hot
        weights["hot_stocks"] = 0.25
    
    # 3. 财经新闻
    if include_news:
        news = fetch_news_sentiment()
        sources["news"] = news
        weights["news"] = 0.20
    
    # 4. YouTube博主
    if include_youtube:
        yt = fetch_youtube_sentiment()
        sources["youtube"] = yt
        weights["youtube"] = 0.15
    
    # 5. 小红书（v2新增）
    if include_xiaohongshu:
        xhs = fetch_xiaohongshu_sentiment()
        sources["xiaohongshu"] = xhs
        weights["xiaohongshu"] = 0.10
    
    # 加权汇总
    total_score = 0
    total_weight = 0
    active_sources = 0
    
    for key, data in sources.items():
        s = data.get("score", 0)
        w = weights.get(key, 0)
        if s != 0 or data.get("articles_analyzed", 0) > 0 or data.get("total_stocks", 0) > 0:
            total_score += s * w
            total_weight += w
            active_sources += 1
    
    # 归一化（考虑缺失数据源）
    if total_weight > 0:
        final_score = total_score / total_weight
    else:
        final_score = 0
    
    final_score = max(-100, min(100, round(final_score, 1)))
    
    # 置信度 = 有效数据源占比
    confidence = active_sources / max(1, len(sources)) * 100
    
    # 情绪标签
    if final_score >= 40:
        label = "🔥 极度乐观"
    elif final_score >= 20:
        label = "📈 偏多乐观"
    elif final_score >= 5:
        label = "☀️ 温和偏多"
    elif final_score >= -5:
        label = "⚖️ 中性"
    elif final_score >= -20:
        label = "🌧️ 温和偏空"
    elif final_score >= -40:
        label = "📉 偏空悲观"
    else:
        label = "💀 极度恐慌"
    
    # 关键信号
    key_signals = []
    for key, data in sources.items():
        if abs(data.get("score", 0)) >= 20:
            key_signals.append(data.get("reason", ""))
        # 新闻关键标题
        for hl in data.get("key_headlines", []):
            key_signals.append(hl)
    
    return {
        "sentiment_score": final_score,
        "sentiment_label": label,
        "sources": sources,
        "key_signals": key_signals[:5],
        "confidence": round(confidence, 1),
    }


# ============================================================
# 独立运行测试
# ============================================================

if __name__ == "__main__":
    print("🌐 外部分析素材情绪聚合系统 v2.0 (含散户过热检测)")
    print("=" * 55)
    
    result = aggregate_external_sentiment()
    
    print(f"\n📊 综合情绪: {result['sentiment_label']} ({result['sentiment_score']:+.1f})")
    print(f"   置信度: {result['confidence']:.0f}%")
    print(f"\n{'='*55}")
    
    for source, data in result["sources"].items():
        name = {"eastmoney": "东方财富", "hot_stocks": "热股动量",
                "news": "财经新闻", "youtube": "YouTube",
                "xiaohongshu": "小红书"}.get(source, source)
        print(f"  [{name}] {data.get('score', 0):+.1f} → {data.get('reason', '无')}")
    
    if result["key_signals"]:
        print(f"\n  🔑 关键信号:")
        for sig in result["key_signals"]:
            print(f"    • {sig}")
    
    print(f"\n{'='*55}")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 演示个股过热检测
    print(f"\n{'='*55}")
    print("🔥 个股散户过热检测 (类似小红书/抖音热度)")
    print("=" * 55)
    demo_stocks = ["300750.SZ", "002594.SZ", "688981.SH", "600519.SH"]
    for code in demo_stocks:
        oh = detect_stock_overheat(code)
        icon = "🔥" if oh["is_overheated"] else "✅"
        print(f"  {icon} {code}: 过热{oh['overheat_score']:.0f}分 | {oh['reason']}")
        if oh["fomo_keywords"]:
            print(f"     FOMO热词: {', '.join(oh['fomo_keywords'][:3])}")
