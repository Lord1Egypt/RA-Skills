#!/usr/bin/env python3
"""
🦞 今日内容工厂 — 批量生成小红书帖子配图+视频
直接调用 make_card.py 生成信息图，ffmpeg 转视频
"""
import subprocess, json, os, sys

MAKE_CARD = os.path.expanduser("~/.openclaw/workspace/skills/xhs-smart-post/scripts/make_card.py")
QUEUE = os.path.expanduser("~/.openclaw/workspace-ursa/content-queue")
UPLOAD = "/tmp/openclaw/uploads"
os.makedirs(QUEUE, exist_ok=True)
os.makedirs(UPLOAD, exist_ok=True)

# ===== 帖子定义 =====
POSTS = [
    {
        "id": "sun_1", "schedule": "12:00",
        "title": "我花5分钟配了31个AI技能",
        "content": "今天给大家看看，一个普通人怎么用 OpenClaw 变成 AI 高手 🦞\n\n不需要写代码\n不需要懂技术\n只要会说话\n\n31个技能涵盖：\n✅ 安全防护（自动扫描、权限管理）\n✅ 内容创作（小红书、公众号自动发）\n✅ 效率工具（翻译、搜索、日程管理）\n✅ 社交互动（AI帮我聊天交友）\n\n最绝的是——这些技能都是 AI 自己安装、自己配置的\n\n我全程只做了两件事：\n1. 告诉 AI 我想要什么\n2. 点确认\n\n这就是 2026 年的 AI 生活 🚀\n\n#OpenClaw #AI工具 #效率提升 #科技生活 #人工智能",
        "cards": [
            {"title": "5分钟配31个AI技能", "subtitle": "OpenClaw 龙虾养成指南", "items": []},
            {"title": "安全防护 6个", "subtitle": "自动扫描+权限管理+威胁预警", "items": ["##安全防护", "自动安全审核", "权限检查", "威胁预警", "防火墙管理", "SSH加固", "版本监控"]},
            {"title": "内容创作 6个", "subtitle": "小红书+公众号+视频", "items": ["##内容创作", "小红书自动发布", "公众号工作流", "图文信息图生成", "AI视频生成", "多语言翻译", "URL转Markdown"]},
            {"title": "效率工具 10个", "subtitle": "搜索+日程+记忆", "items": ["##效率工具", "网页搜索", "天气查询", "定时提醒", "记忆管理", "文件备份", "知识库", "YouTube字幕", "安全健康检查"]},
            {"title": "全自动化", "subtitle": "你说话，AI动手", "items": ["##核心能力", "语音交互", "浏览器自动化", "API调用", "文件管理", "代码执行", "定时任务调度"]},
        ]
    },
    {
        "id": "sun_2", "schedule": "20:00",
        "title": "AI帮我管理25台矿机的真实体验",
        "content": "说实话，最开始我也担心 AI 能不能管好矿机 🖥️\n\n实际用了之后发现：\n\n❌ 人工巡检：每天盯 2 小时，还是会漏\n✅ AI 监控：7×24 小时，掉线秒级发现\n\n我的 AI 做了什么：\n1️⃣ 自动检查每台机器状态\n2️⃣ 掉线自动重启\n3️⃣ 生成监控报告\n4️⃣ 异常自动通知我\n\n从 25 台到计划 200 台\nAI 不是替代运维，是让 1 个人干 10 个人的活 💪\n\n#AI运维 #矿机管理 #自动化 #效率革命",
        "cards": [
            {"title": "AI管理25台矿机", "subtitle": "真实体验分享", "items": []},
            {"title": "人工 vs AI", "subtitle": "效率差距一目了然", "items": ["##人工巡检", "每天盯屏2小时", "漏检率约5%", "1人最多管10台", "", "##AI监控", "7×24自动值守", "掉线秒级发现", "1人轻松管200台"]},
            {"title": "AI做了什么", "subtitle": "自动化四件套", "items": ["##1. 自动检查", "每5分钟扫描所有机器", "", "##2. 掉线重启", "发现异常立即重启进程", "", "##3. 监控报告", "生成实时状态看板", "", "##4. 异常通知", "掉线自动推送消息"]},
            {"title": "结论", "subtitle": "AI不是替代人，是超级外挂", "items": ["##效果", "1个人干10个人的活", "25台→200台无压力", "故障响应: 小时→秒级", "人力成本大幅降低", "", "##结论", "AI运维已经成熟了", "你还不用就晚了"]},
        ]
    },
    {
        "id": "sun_3", "schedule": "20:30",
        "title": "让AI帮你发小红书是什么体验",
        "content": "标题党警告：这篇帖子就是 AI 写的 🤖\n\n从选题→写文案→做图→发布\n全程 AI 自动化\n\n我是怎么做到的：\n\n1️⃣ 告诉 AI：\"帮我发一篇小红书\"\n2️⃣ AI 自动选题、写文案\n3️⃣ AI 生成信息图配图\n4️⃣ AI 自动上传发布\n\n我全程只做了一件事——说了那句话 😂\n\n你觉得 AI 写的内容能火吗？\n\n#AI创作 #小红书运营 #自动化内容 #科技生活",
        "cards": [
            {"title": "AI帮我发小红书", "subtitle": "全程自动化体验", "items": []},
            {"title": "Step 1: 选题", "subtitle": "AI分析热点+用户画像", "items": ["##选题策略", "分析平台热门话题", "匹配目标人群画像", "生成3个选题方案", "评估传播潜力打分"]},
            {"title": "Step 2: 内容", "subtitle": "AI写文案+做配图", "items": ["##文案生成", "标题(限20字)", "正文+标签优化", "自动排版美化", "", "##配图生成", "信息图自动设计", "5张配图批量出", "1080×1440竖屏"]},
            {"title": "Step 3: 发布", "subtitle": "AI自动上传+定时发布", "items": ["##自动化发布", "浏览器自动操作", "自动填写表单", "选择最佳时间", "定时自动发布", "", "##你只做一件事", "说\"帮我发小红书\"", "剩下全交给AI"]},
        ]
    },
]

def gen_images(post):
    """生成每张信息图"""
    out_dir = os.path.join(QUEUE, post["id"])
    os.makedirs(out_dir, exist_ok=True)
    
    preset_map = {"sun_1": "tutorial", "sun_2": "case", "sun_3": "secret"}
    preset = preset_map.get(post["id"], "default")
    
    pngs = []
    for i, card in enumerate(post["cards"]):
        fname = f"{post['id']}_{i+1}.png"
        fpath = os.path.join(out_dir, fname)
        items = [x for x in card.get("items", []) if x.strip()]
        subtitle = card.get("subtitle", "")
        if subtitle and items:
            items.insert(0, f"» {subtitle}")
        
        cmd = [sys.executable, MAKE_CARD, "--title", card["title"], "--output", fpath, "--preset", preset]
        if items:
            cmd += ["--items"] + items
        
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0:
            pngs.append(fpath)
            print(f"  ✅ {fname}")
        else:
            print(f"  ❌ {fname}: {r.stderr.strip()}")
    
    return pngs

def make_video(post):
    """图片拼成视频"""
    out_dir = os.path.join(QUEUE, post["id"])
    pngs = sorted([os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.endswith(".png")])
    if not pngs:
        return None
    
    concat = os.path.join(out_dir, "concat.txt")
    with open(concat, "w") as f:
        for p in pngs:
            f.write(f"file '{p}'\nduration 6\n")
        f.write(f"file '{pngs[-1]}'\n")
    
    vpath = os.path.join(UPLOAD, f"{post['id']}_slideshow.mp4")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat,
        "-vf", "scale=1080:1440:force_original_aspect_ratio=decrease,pad=1080:1440:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p",
        "-c:v", "libx264", "-r", "25", vpath
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode == 0:
        size = os.path.getsize(vpath)
        print(f"  🎬 视频: {vpath} ({size//1024}KB, {len(pngs)*6}s)")
        return vpath
    else:
        print(f"  ❌ 视频失败: {r.stderr[-100:]}")
        return None

# ===== 执行 =====
if __name__ == "__main__":
    print("🦞 龙虾内容工厂 启动\n")
    manifest = []
    
    for post in POSTS:
        print(f"\n{'='*40}")
        print(f"📝 {post['title']}")
        print(f"⏰ 定时: {post['schedule']}")
        print(f"{'='*40}")
        
        pngs = gen_images(post)
        video = make_video(post)
        
        manifest.append({
            "id": post["id"],
            "title": post["title"],
            "content": post["content"],
            "schedule": post["schedule"],
            "images": pngs,
            "video": video,
            "status": "ready"
        })
    
    mpath = os.path.join(QUEUE, "manifest.json")
    with open(mpath, "w") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*40}")
    print(f"🎉 完成！清单: {mpath}")
    for m in manifest:
        print(f"  {m['schedule']} → {m['title']} ({len(m['images'])}图 {'🎬' if m['video'] else ''})")
    print(f"{'='*40}")
