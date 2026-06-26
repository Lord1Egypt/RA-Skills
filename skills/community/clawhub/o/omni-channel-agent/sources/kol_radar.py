"""
KOL Radar — 核心趋势雷达账户监控

基于 Lark 文档《Identifying Global Social Media Trends for AI Agent Development》
监控 11 个分层 KOL 账户，抓取最新内容并评估趋势适配度。

数据源: TikTok Apify Scraper (clockworks/tiktok-scraper)
"""

import sys, os, json
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from apify_client import run_actor

ACTOR_ID = "clockworks~tiktok-scraper"

# ═══════════════════════════════════════════════════
# 三级 KOL 雷达体系
# ═══════════════════════════════════════════════════

KOL_TIERS = {
    "tier1": {
        "name": "🔴 TIER 1: 非常高优先级（潮流引领者）",
        "description": "每天监控。他们创造趋势，当他们发布新视觉风格/转换/舞蹈时，很可能全球传播。旗舰AI模板的主要候选。",
        "accounts": [
            {
                "handle": "cyber0318",
                "niche": "摄影趋势/高端角色扮演/视觉指导",
                "ai_value": "电影AI照片滤镜、动漫角色扮演视频模板、照明风格/拍摄角度复制",
                "url": "https://www.tiktok.com/@cyber0318"
            },
            {
                "handle": "hoaa.hanassii",
                "niche": "原创舞蹈编排/病毒动作",
                "ai_value": "AI视频agent骨骼运动数据(姿势跟踪)、AI化身舞蹈、抢先竞争对手提取舞蹈趋势",
                "url": "https://www.tiktok.com/@hoaa.hanassii"
            },
            {
                "handle": "thybui.__",
                "niche": "史诗级化妆改造/角色扮演/趋势适应",
                "ai_value": "面部交换AI、即时化妆/角色扮演变换模板、戏剧化前后揭示",
                "url": "https://www.tiktok.com/@thybui.__"
            },
        ]
    },
    "tier2": {
        "name": "🟡 TIER 2: 高优先级（快速采用者）",
        "description": "不一定发明潮流，但最先加入。多个T2创造者使用相同音频/风格 = 趋势确认信号。",
        "accounts": [
            {
                "handle": "angelinazhq",
                "niche": "病毒式舞蹈翻唱/歌曲趋势",
                "ai_value": "音频配对验证——她用的声音可安全用于AI生成视频",
                "url": "https://www.tiktok.com/@angelinazhq"
            },
            {
                "handle": "lena_foxxx",
                "niche": "角色扮演/流行舞蹈",
                "ai_value": "AI角色扮演生成+AI视频动作结合的参考、当前最受欢迎角色",
                "url": "https://www.tiktok.com/@lena_foxxx"
            },
            {
                "handle": "caroline_xdc",
                "niche": "核心角色扮演/舞蹈",
                "ai_value": "趋势人物服装配件数据、静态AI艺术生成器素材",
                "url": "https://www.tiktok.com/@caroline_xdc"
            },
            {
                "handle": "upminaa.cos",
                "niche": "核心角色扮演/舞蹈",
                "ai_value": "AI图像模型提示想法(如'趋势原神角色')、动漫游戏社区晴雨表",
                "url": "https://www.tiktok.com/@upminaa.cos"
            },
        ]
    },
    "tier3": {
        "name": "🔵 TIER 3: 专业与运动雷达",
        "description": "专注特定技术数据：清洁身体动作(AI运动跟踪)、独特视频编辑风格、竞争对手AI分析。",
        "accounts": [
            {
                "handle": "cellow111",
                "niche": "视频转换/运动编辑趋势",
                "ai_value": "UI/UX和模板开发——摄像头抖动/闪光/视觉过渡编程参考",
                "url": "https://www.tiktok.com/@cellow111"
            },
            {
                "handle": "emmawhatstwo",
                "niche": "虚拟/AI影响者",
                "ai_value": "直接竞争对手分析——公众对AI生成化身表演流行舞蹈的反应",
                "url": "https://www.tiktok.com/@emmawhatstwo"
            },
            {
                "handle": "voulezjj",
                "niche": "纯舞蹈/快速采用者",
                "ai_value": "运动捕捉金矿——光线明亮、身体框架清晰，AI姿态估计/骨架跟踪完美素材",
                "url": "https://www.tiktok.com/@voulezjj"
            },
            {
                "handle": "sawamura_kirari",
                "niche": "纯舞蹈/快速采用者",
                "ai_value": "提取干净高质量舞蹈动作，AI视频化身二级来源",
                "url": "https://www.tiktok.com/@sawamura_kirari"
            },
        ]
    },
}


def get_all_kol_handles() -> list:
    """Return flat list of all KOL handles."""
    handles = []
    for tier in KOL_TIERS.values():
        for acc in tier["accounts"]:
            handles.append(acc["handle"])
    return handles


def fetch_kol_profile(handle: str, max_results: int = 10) -> list:
    """Fetch recent posts from a specific TikTok KOL profile."""
    input_data = {
        "profiles": [handle],
        "resultsPerPage": max_results,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
    }
    return run_actor(ACTOR_ID, input_data)


def fetch_all_kol_profiles(max_per_kol: int = 5) -> dict:
    """
    Fetch recent posts from ALL KOL accounts.
    Returns dict keyed by tier → handle → posts.
    
    Note: To reduce Apify cost, batches profiles in single actor runs.
    """
    all_handles = get_all_kol_handles()
    
    print(f"\n🎯 [KOL雷达] 批量抓取 {len(all_handles)} 个账号...")
    
    # Batch all profiles into one actor run
    input_data = {
        "profiles": all_handles,
        "resultsPerPage": max_per_kol,
        "shouldDownloadVideos": False,
        "shouldDownloadCovers": False,
        "shouldDownloadSlideshowImages": False,
    }
    
    try:
        raw_items = run_actor(ACTOR_ID, input_data)
    except Exception as e:
        print(f"   ❌ KOL雷达批量抓取失败: {e}")
        return {}
    
    # Group results by author
    by_author = {}
    for item in raw_items:
        author = item.get("authorMeta", {}).get("name", "").lower()
        if not author:
            author = item.get("authorMeta", {}).get("nickName", "unknown").lower()
        if author not in by_author:
            by_author[author] = []
        by_author[author].append(item)
    
    # Map back to tier structure
    result = {}
    for tier_key, tier_data in KOL_TIERS.items():
        result[tier_key] = {
            "name": tier_data["name"],
            "accounts": {}
        }
        for acc in tier_data["accounts"]:
            handle = acc["handle"].lower()
            posts = by_author.get(handle, [])
            result[tier_key]["accounts"][acc["handle"]] = {
                "info": acc,
                "posts": _extract_kol_posts(posts),
                "post_count": len(posts),
            }
            if posts:
                print(f"   ✅ @{acc['handle']}: {len(posts)} posts")
            else:
                print(f"   ⚠️ @{acc['handle']}: 0 posts (可能被限流)")
    
    return result


def _extract_kol_posts(items: list) -> list:
    """Extract structured data from KOL posts."""
    posts = []
    for item in items:
        posts.append({
            "id": item.get("id", ""),
            "desc": (item.get("text", "") or "")[:200],
            "plays": item.get("playCount", 0),
            "likes": item.get("diggCount", 0),
            "comments": item.get("commentCount", 0),
            "shares": item.get("shareCount", 0),
            "music": item.get("musicMeta", {}).get("musicName", ""),
            "music_author": item.get("musicMeta", {}).get("musicAuthor", ""),
            "hashtags": [h.get("name", "") for h in item.get("hashtags", [])],
            "url": item.get("webVideoUrl", ""),
            "createTime": item.get("createTimeISO", ""),
            "duration": item.get("videoMeta", {}).get("duration", 0),
        })
    posts.sort(key=lambda x: x.get("plays", 0), reverse=True)
    return posts


# ═══════════════════════════════════════════════════
# 趋势评估框架 (Phase 4)
# ═══════════════════════════════════════════════════

def evaluate_trend_for_ai(post: dict) -> dict:
    """
    基于文档 Phase 4 的3个核心验证问题评估趋势。
    
    返回评估结果，包含:
    - visual_distinct: 视觉上是否有区别？
    - ai_accessible: AI能否轻松复制？
    - vanity_trigger: 是否引发虚荣心？
    - overall_score: 综合评分 (0-100)
    
    注意：这是基于数据指标的初步评估，最终判断仍需人类直觉。
    """
    plays = post.get("plays", 0)
    likes = post.get("likes", 0)
    comments = post.get("comments", 0)
    shares = post.get("shares", 0)
    hashtags = post.get("hashtags", [])
    desc = (post.get("desc", "") or "").lower()
    
    score = 0
    signals = []
    
    # 1. 传播力信号 (max 30分)
    if plays > 1_000_000:
        score += 30; signals.append("🔥 百万播放")
    elif plays > 100_000:
        score += 20; signals.append("📈 10万+播放")
    elif plays > 10_000:
        score += 10; signals.append("📊 1万+播放")
    
    # 2. 互动率信号 (max 25分)
    engagement = (likes + comments + shares) / max(plays, 1)
    if engagement > 0.1:
        score += 25; signals.append("💎 超高互动率")
    elif engagement > 0.05:
        score += 15; signals.append("✨ 高互动率")
    elif engagement > 0.02:
        score += 8; signals.append("👍 中等互动")
    
    # 3. AI相关性关键词 (max 20分)
    ai_keywords = ["ai", "filter", "cosplay", "dance", "transformation", "makeup",
                   "角色扮演", "换装", "变装", "特效", "滤镜", "挑战"]
    visual_keywords = ["photo", "art", "style", "aesthetic", "visual", "cinematic",
                       "anime", "cyberpunk", "fantasy", "futuristic"]
    
    kw_hits = sum(1 for kw in ai_keywords if kw in desc or kw in " ".join(hashtags).lower())
    vis_hits = sum(1 for kw in visual_keywords if kw in desc or kw in " ".join(hashtags).lower())
    
    if kw_hits >= 2:
        score += 15; signals.append(f"🎯 AI关键词匹配({kw_hits})")
    elif kw_hits >= 1:
        score += 8; signals.append("🎯 AI关键词")
    
    if vis_hits >= 2:
        score += 5; signals.append(f"🎨 视觉关键词({vis_hits})")
    
    # 4. 音频驱动信号 (max 15分) — 文档强调音频是趋势支柱
    music = post.get("music", "")
    if music:
        score += 10; signals.append(f"🎵 音频: {music[:30]}")
    
    # 5. 分享率信号 (max 10分) — 分享=用户想让别人看到=虚荣心触发
    share_rate = shares / max(plays, 1)
    if share_rate > 0.01:
        score += 10; signals.append("📤 高分享率(虚荣触发)")
    elif share_rate > 0.005:
        score += 5; signals.append("📤 中等分享率")
    
    # 优先级
    if score >= 70:
        priority = "🔴 HIGH"
    elif score >= 40:
        priority = "🟡 MEDIUM"
    else:
        priority = "🔵 LOW"
    
    return {
        "score": min(score, 100),
        "priority": priority,
        "signals": signals,
        "note": "⚠️ 数据评估仅供参考，最终判断需人类直觉验证视觉效果和氛围"
    }


# ═══════════════════════════════════════════════════
# 音频趋势聚合
# ═══════════════════════════════════════════════════

def aggregate_audio_trends(kol_data: dict) -> list:
    """
    从 KOL 数据中聚合音频趋势。
    文档强调：音乐和音频决定短视频趋势，病毒式声音是舞蹈/角色扮演过渡的支柱。
    
    当多个 KOL 使用相同音频 → 强趋势信号
    """
    audio_usage = {}  # music_name → {count, kols, total_plays, posts}
    
    for tier_key, tier in kol_data.items():
        for handle, data in tier.get("accounts", {}).items():
            for post in data.get("posts", []):
                music = post.get("music", "").strip()
                if not music or music.lower() in ("original sound", "原声"):
                    continue
                
                if music not in audio_usage:
                    audio_usage[music] = {
                        "music": music,
                        "music_author": post.get("music_author", ""),
                        "count": 0,
                        "kols": set(),
                        "total_plays": 0,
                        "sample_urls": [],
                    }
                
                audio_usage[music]["count"] += 1
                audio_usage[music]["kols"].add(handle)
                audio_usage[music]["total_plays"] += post.get("plays", 0)
                if len(audio_usage[music]["sample_urls"]) < 3:
                    audio_usage[music]["sample_urls"].append(post.get("url", ""))
    
    # Convert sets to lists and sort
    trends = []
    for music, data in audio_usage.items():
        data["kols"] = list(data["kols"])
        data["kol_count"] = len(data["kols"])
        # Multiple KOLs using same audio = strong signal (doc Phase 2)
        data["trend_strength"] = "🔥 强趋势" if data["kol_count"] >= 3 else (
            "📈 中等趋势" if data["kol_count"] >= 2 else "📊 单源"
        )
        trends.append(data)
    
    trends.sort(key=lambda x: (x["kol_count"], x["total_plays"]), reverse=True)
    return trends


# ═══════════════════════════════════════════════════
# 格式化输出
# ═══════════════════════════════════════════════════

def format_kol_radar_report(kol_data: dict) -> str:
    """Format KOL radar data into Slack report."""
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    sections = []
    sections.append(f"🎯 *KOL 趋势雷达 — {ts}*\n")
    
    for tier_key in ["tier1", "tier2", "tier3"]:
        tier = kol_data.get(tier_key, {})
        if not tier:
            continue
        
        sections.append(f"*{tier['name']}*")
        
        lines = ["```"]
        lines.append(f"{'账号':<18s}  {'最新播放':>10s}  {'总赞':>8s}  {'视频数':>4s}  {'热门标签'}")
        lines.append("─" * 70)
        
        for handle, data in tier.get("accounts", {}).items():
            posts = data.get("posts", [])
            if not posts:
                lines.append(f"@{handle:<17s}  {'N/A':>10s}  {'N/A':>8s}  {'0':>4s}  -")
                continue
            
            top = posts[0]
            total_likes = sum(p.get("likes", 0) for p in posts)
            top_tags = ", ".join(list(set(
                tag for p in posts for tag in p.get("hashtags", [])
            ))[:3])
            
            from run_pipeline import fmt_num
            lines.append(
                f"@{handle:<17s}  {fmt_num(top.get('plays', 0)):>10s}  "
                f"{fmt_num(total_likes):>8s}  {len(posts):>4d}  {top_tags[:25]}"
            )
        
        lines.append("```")
        sections.append("\n".join(lines))
    
    # Audio trends
    audio_trends = aggregate_audio_trends(kol_data)
    if audio_trends:
        sections.append("\n🎵 *音频趋势信号（多KOL使用 = 强趋势）*")
        lines = ["```"]
        lines.append(f"{'趋势强度':<10s}  {'KOL数':>5s}  {'总播放':>10s}  {'音频名称'}")
        lines.append("─" * 65)
        for at in audio_trends[:10]:
            from run_pipeline import fmt_num
            lines.append(
                f"{at['trend_strength']:<10s}  {at['kol_count']:>5d}  "
                f"{fmt_num(at['total_plays']):>10s}  {at['music'][:30]}"
            )
            if at["kol_count"] >= 2:
                lines.append(f"{'':>18s}  使用者: {', '.join('@'+k for k in at['kols'][:5])}")
        lines.append("```")
        sections.append("\n".join(lines))
    
    sections.append("\n💡 *评估提醒:* 数据仅做初筛，最终判断需人类直觉验证「视觉区分度 + AI可复制性 + 虚荣心触发」三要素")
    
    return "\n\n".join(sections)


if __name__ == "__main__":
    print("=== KOL Radar Test ===")
    print(f"监控账号: {get_all_kol_handles()}")
    print(f"\n共 {len(get_all_kol_handles())} 个账号，分 3 级")
    
    for tier_key, tier in KOL_TIERS.items():
        print(f"\n{tier['name']}")
        for acc in tier["accounts"]:
            print(f"  @{acc['handle']:20s} | {acc['niche']}")
