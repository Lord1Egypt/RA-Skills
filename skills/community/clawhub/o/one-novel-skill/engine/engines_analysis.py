#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析引擎 — 数据趋势/四率诊断/读者流失预警

驱动数据:
  06-platform-algorithms.md (番茄/起点推荐算法漏斗/完读率/追读率)
  04-reader-psychology.md (多巴胺周期/疲劳曲线)
  09-editor-perspective.md (14道审查关卡-第13关市场性评估)
import re
"""


class AnalysisEngine:
    """数据诊断与分析 — 基于平台算法"""

    # 来自06-platform-algorithms.md: 番茄推荐权重
    TOMATO_WEIGHTS = {
        "chapter1_completion": 0.25,
        "chapter3_completion": 0.15,
        "full_completion": 0.15,
        "follow_read": 0.20,
        "stay_time": 0.10,
        "share_rate": 0.05,
        "collect_rate": 0.05,
        "update_freq": 0.05,
    }

    # 来自06-platform-algorithms.md: 起点签约线
    QIDIAN_THRESHOLDS = {
        "xuanhuan_xianxia": {"follow_read": 0.05, "collect": 200},
        "dushi": {"follow_read": 0.08, "collect": 150},
        "qihuan_kehuan": {"follow_read": 0.03, "collect": 100},
    }

    # 来自04-reader-psychology: 阅读疲劳模型
    FATIGUE_ZONES = {
        "开头弃书": (1, 3, "前三章完读率"),
        "首次疲倦": (15, 20, "中段缓冲期"),
        "中期疲软": (50, 60, "中期疲劳"),
        "后期疲软": (100, 120, "后期疲劳"),
    }

    @staticmethod
    def analyze_retention(chapter_data: list) -> dict:
        """基于平台算法分析留存趋势"""
        if not chapter_data:
            return {"趋势": "无数据", "预警": False}

        rates = [c.get("engagement", 0.5) for c in chapter_data]

        if len(rates) >= 3:
            recent = sum(rates[-2:]) / 2
            early = sum(rates[:2]) / 2
            change = recent - early

            # 最近章节趋势
            if len(rates) >= 5:
                last_5 = sum(rates[-5:]) / 5
                prev_5 = sum(rates[-10:-5]) / 5 if len(rates) >= 10 else sum(rates[:-5]) / max(len(rates)-5, 1)
                short_trend = last_5 - prev_5
            else:
                short_trend = 0

            return {
                "trend": "上升" if change > 0.05 else "下降" if change < -0.05 else "稳定",
                "change": round(change, 3),
                "recent_avg": round(recent, 3),
                "short_trend": round(short_trend, 2),
                "alert": change < -0.1 or short_trend < -0.1,
                "level": "green" if change >= 0 else "yellow" if change >= -0.1 else "red",
            }
        return {"trend": "数据不足", "alert": False}

    @staticmethod
    def diagnose_four_rates(data: dict = None) -> list:
        """番茄四率诊断 (06-platform-algorithms.md)"""
        issues = []

        if not data:
            return ["无数据 - 建议采集: 首章完读率/三章完读率/追读率/收藏率"]

        # 首章完读率  (番茄冷启动关键指标)
        ch1_completion = data.get("chapter1_completion", 1.0)
        if ch1_completion < 0.6:
            issues.append(f"首章完读率{ch1_completion:.0%} < 60% - 优化开篇钩子(前300字必须有冲突/悬念)")
        elif ch1_completion >= 0.8:
            pass  # 优秀

        # 前三章完读率 (小流量池考核)
        ch3_completion = data.get("chapter3_completion", 1.0)
        if ch3_completion < 0.35:
            issues.append(f"前三章完读率{ch3_completion:.0%} < 35% - 严重警告: 第1章后流失严重")
        elif ch3_completion < 0.5:
            issues.append(f"前三章完读率{ch3_completion:.0%} < 50% - 第2-3章节奏需加速, 建议10章内出2次爽点")

        # 追读率 (番茄大流量池/起点核心指标)
        follow_read = data.get("follow_read", 1.0)
        if follow_read < 0.05:
            issues.append(f"追读率{follow_read:.0%} < 5% - 严重: 提升章末悬念强度")
        elif follow_read < 0.1:
            issues.append(f"追读率{follow_read:.0%} < 10% - 每章结尾需强钩子, 建议固定更新时间")

        # 收藏-阅读比 (起点上架关键)
        collect_ratio = data.get("collect_ratio", 1.0)
        if collect_ratio < 0.05:
            issues.append(f"收藏率{collect_ratio:.0%} < 5% - 加引导收藏话语")

        return issues or ["四率健康 - 继续观察"]

    @staticmethod
    def diagnose_platform_readiness(genre: str = "dushi", stats: dict = None) -> dict:
        """诊断是否达到签约/上架标准"""
        if not stats:
            return {"ready": False, "gates": ["无数据"], "score": 0}

        thresholds = AnalysisEngine.QIDIAN_THRESHOLDS.get(genre, {"follow_read": 0.05, "collect": 100})
        gates = []
        passed = 0
        total = 3

        # 追读率门
        fr = stats.get("follow_read", 0)
        if fr >= thresholds["follow_read"]:
            passed += 1
            gates.append(f"追读率{fr:.0%} >= {thresholds['follow_read']:.0%} ✅")
        else:
            gates.append(f"追读率{fr:.0%} < {thresholds['follow_read']:.0%} ❌")

        # 收藏门
        cl = stats.get("collect", 0)
        if cl >= thresholds["collect"]:
            passed += 1
            gates.append(f"收藏{cl} >= {thresholds['collect']} ✅")
        else:
            gates.append(f"收藏{cl} < {thresholds['collect']} ❌")

        # 字数门
        wc = stats.get("word_count", 0)
        min_words = 30000
        if wc >= min_words:
            passed += 1
            gates.append(f"字数{wc} >= {min_words} ✅")
        else:
            gates.append(f"字数{wc} < {min_words} ❌")

        score = int((passed / total) * 100)
        return {
            "ready": passed >= 2,
            "gates": gates,
            "score": score,
            "verdict": "可签约" if passed >= 2 else "还需积累" if passed >= 1 else "差距较大",
        }

    @staticmethod
    def predict_risky_zones(total_chapters: int, engagement_history: list = None) -> list:
        """基于疲劳曲线预测高风险弃书区间"""
        zones = []

        for name, (start, end, reason) in AnalysisEngine.FATIGUE_ZONES.items():
            if end <= total_chapters:
                risk = "medium"
                if engagement_history:
                    zone_data = [h for i, h in enumerate(engagement_history) if start <= i+1 <= end]
                    if zone_data:
                        avg_eng = sum(zone_data) / len(zone_data) if isinstance(zone_data, list) else 0
                        if avg_eng < 0.4:
                            risk = "high"
                        elif avg_eng < 0.6:
                            risk = "预警"

                zones.append({
                    "zone": name,
                    "chapters": f"#{start}-{end}",
                    "reason": reason,
                    "risk": risk,
                    "suggestion": {
                        "开头弃书": "优化前三章钩子和完读率",
                        "首次疲倦": "安排小高潮/引入新冲突",
                        "中期疲软": "开启新地图/引入中层次反派",
                        "后期疲软": "加速主线推进, 安排核心冲突",
                    }.get(name, "监控追读率变化"),
                })

        return zones

    @staticmethod
    def calculate_platform_score(chapter_data: list, platform: str = "番茄") -> dict:
        """基于平台算法权重计算综合评分"""
        if not chapter_data:
            return {"platform": platform, "score": 0, "pass": False}

        avg_engagement = sum(c.get("engagement", 0.5) for c in chapter_data) / len(chapter_data)
        avg_tension = sum(c.get("tension", 0.5) for c in chapter_data) / len(chapter_data)
        avg_interest = sum(c.get("interest", 0.5) for c in chapter_data) / len(chapter_data)

        # 模拟四率
        ch1 = chapter_data[0].get("engagement", 0.5) if chapter_data else 0.5
        ch3_avg = sum(c.get("engagement", 0.5) for c in chapter_data[:3]) / max(len(chapter_data[:3]), 1)

        components = {
            "chapter1_completion": ch1,
            "chapter3_completion": ch3_avg,
            "follow_read": avg_engagement,
            "stay_time": avg_tension,
            "interest": avg_interest,
        }

        if platform == "番茄":
            raw_weights = {
                "chapter1_completion": 0.25,
                "chapter3_completion": 0.15,
                "follow_read": 0.20,
                "stay_time": 0.10,
                "interest": 0.05,
            }
        elif platform == "起点":
            raw_weights = {
                "chapter1_completion": 0.10,  # 起点慢热，首章权重低
                "chapter3_completion": 0.15,
                "follow_read": 0.30,          # 追读最重要
                "stay_time": 0.15,            # 深度阅读
                "interest": 0.05,
            }
        elif platform == "飞卢":
            raw_weights = {
                "chapter1_completion": 0.30,  # 飞卢短平快
                "chapter3_completion": 0.20,
                "follow_read": 0.15,
                "stay_time": 0.05,
                "interest": 0.10,
            }
        elif platform == "七猫":
            raw_weights = {
                "chapter1_completion": 0.20,
                "chapter3_completion": 0.20,
                "follow_read": 0.20,
                "stay_time": 0.10,
                "interest": 0.10,
            }
        else:
            raw_weights = {
                "chapter1_completion": 0.20,
                "chapter3_completion": 0.15,
                "follow_read": 0.25,
                "stay_time": 0.10,
                "interest": 0.05,
            }
        total_wt = sum(raw_weights.values())
        score = sum(components[k] * v / total_wt for k, v in raw_weights.items())

        return {
            "platform": platform,
            "score": round(score * 100, 1),
            "components": components,
            "pass": score > 0.5,
            "verdict": "优秀" if score > 0.7 else "良好" if score > 0.5 else "需优化",
        }
    # === IP潜力五维评估 (源自09-web-novel-business-logic) ===
    @staticmethod
    def assess_ip_potential(concept, world_unique=3, char_memory=3, genre_fit=3,
                           expand_space=3, meme_density=3):
        """IP潜力五维度评分"""
        dims = {
            "世界观独占性": min(5, world_unique),
            "角色记忆度": min(5, char_memory),
            "题材适配度": min(5, genre_fit),
            "延展空间": min(5, expand_space),
            "梗密度": min(5, meme_density),
        }
        total = sum(dims.values())
        return {
            "total": total, "max": 25,
            "dimensions": dims,
            "verdict": "高IP潜力" if total >= 20 else "中IP潜力" if total >= 15 else "低IP潜力",
            "advice": "提升世界观独占性" if total < 15 and dims["世界观独占性"] < 3 else "",
        }
    # === 数据驱动写作 (源自05-data-driven-writing.md) ===
    @staticmethod
    def retention_curve(chapter_rates):
        """留存曲线分析: 第1->2章>80%, 第5章>60%, 第10章>50%"""
        if not chapter_rates or len(chapter_rates) < 2:
            return {"verdict": "数据不足"}
        issues = []
        for i, rate in enumerate(chapter_rates[:10]):
            expected = {0: 0.80, 1: 0.75, 2: 0.70, 3: 0.65, 4: 0.60}
            expected_val = expected.get(i, 0.50)
            if rate < expected_val:
                issues.append(f"第{i+1}章留存率{rate:.0%} < 预期{expected_val:.0%}")
        return {"issues": issues, "avg_retention": round(sum(chapter_rates[:10])/len(chapter_rates[:10]), 2),
                "verdict": "留存健康" if not issues else "需优化"}

    @staticmethod
    def three_second_hook(text):
        """三秒定生死检测 (源自01-douyin-algorithm.md)"""
        if not text or len(text) < 50:
            return {"has_hook": False}
        opening = text[:50]
        hook_words = ["?", "!", "？", "！", "突然", "发现", "原来", "难道", "为什么", "真相"]
        has_hook = any(w in opening for w in hook_words)
        return {"has_hook": has_hook,
                "verdict": "前3秒有钩子" if has_hook else "前3秒无钩子 - 建议抛出问题或反常识观点"}
    # === 书名质量分析 (源自02-21-days-web-novel.md) ===
    @staticmethod
    def check_title_quality(title):
        """书名分析: 核心关键词+悬念/反差元素"""
        if not title:
            return {"score": 0, "issues": ["书名不能为空"]}
        issues = []
        # 长度检查
        cn = len([c for c in title if "\u4e00" <= c <= "\u9fff"])
        if cn < 4:
            issues.append("书名过短(<4字) - 建议包含核心关键词")
        elif cn > 12:
            issues.append(f"书名过长({cn}字) - 建议压缩至4-12字")
        # 悬念/反差检测
        suspense_words = ["?", "!", "秘密", "真相", "之", "隐藏", "最后", "尽头"]
        has_suspense = any(w in title for w in suspense_words)
        if not has_suspense:
            issues.append("缺少悬念/反差元素 - 书名应让读者产生好奇")
        # 关键词检测
        genre_keywords = {"修仙": ["修", "仙", "道", "神", "魔"], "都市": ["都", "市", "城", "少", "王"]}
        return {"score": max(0, 10 - len(issues) * 2), "issues": issues,
                "has_suspense": has_suspense}
    # === 三章留存阈值检查 (源自07-golden-three-chapters.md) ===
    @staticmethod
    def check_three_chapter_retention(rates):
        """三章留存指标: 第1章>70%, 第2章>60%, 第3章>5%收藏"""
        if not rates or len(rates) < 3:
            return {"verdict": "数据不足"}
        issues = []
        if rates[0] < 0.70:
            issues.append(f"第一章留存率{rates[0]:.0%} < 70% - 优化开篇钩子")
        if len(rates) > 1 and rates[1] < 0.60:
            issues.append(f"第二章转人率{rates[1]:.0%} < 60% - 深化冲突")
        if len(rates) > 2 and rates[2] < 0.05:
            issues.append(f"第三章收藏率{rates[2]:.0%} < 5% - 加快爽点节奏")
        return {"issues": issues, "verdict": "三章健康" if not issues else "需优化"}
    # === 文学质量评估 (源自02-hugo-nebula.md) ===
    @staticmethod
    def literary_quality_check(text):
        """文学性评估: 语言质量/叙事弧完整性"""
        if not text:
            return {"score": 0}

        cn_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        if cn_chars < 200:
            return {"score": 5, "verdict": "文本过短"}
        # 语言多样性
        sent_count = len(re.findall(r"[。！？]", text))
        avg_sent = cn_chars / max(sent_count, 1)
        diversity = min(10, max(0, 10 - abs(avg_sent - 25) / 2.5))  # 离25越远分越低
        # 文学手法
        device_count = text.count("像") + text.count("如") + text.count("比")
        device_score = min(5, device_count / 5)
        score = int(min(10, 5 + diversity + device_score))
        return {
            "score": score,
            "avg_sent_len": round(avg_sent, 1),
            "device_score": round(device_score, 1),
            "verdict": "语言优秀(适合文学奖)" if score >= 8 else "语言合格" if score >= 5 else "语言粗糙",
        }
    # === 3000铁粉模型 (源自09-web-novel-business-logic.md) ===
    @staticmethod
    def fan_3000_model(follow_read_rate=0.1, collect_rate=0.05, total_readers=0):
        """3000铁粉可行性预测"""
        if total_readers == 0:
            return {"verdict": "需总读者数"}
        paying_fans = int(total_readers * follow_read_rate * collect_rate * 100)
        return {
            "total_readers": total_readers,
            "estimated_fans": paying_fans,
            "threshold_met": paying_fans >= 3000,
            "verdict": f"预计{paying_fans}铁粉" + " (>=3000: 可全职)" if paying_fans >= 3000
                       else f" (<3000: 需{3000 - paying_fans}更多读者)",
        }