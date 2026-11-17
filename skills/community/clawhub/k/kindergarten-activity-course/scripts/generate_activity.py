# -*- coding: utf-8 -*-
"""幼儿园五大领域活动方案生成器。

用法:
  python generate_activity.py --age 大班 --domain science,art --count 4 --out plan.html
"""
import argparse, random, sys

# ---------------- 活动库 ----------------
# 字段: (domain, age, title, emoji, goal, materials, steps, tips, minutes)
ACTIVITIES = [
    # 健康
    ("health", "小班", "小动物跳跳跳", "🐸", "双脚跳与模仿能力",
     ["客厅空地", "抱枕若干"],
     ["家长示范双脚向前跳，像小兔子", "在地垫间隔放抱枕当荷叶", "孩子连续跳过 4-5 个荷叶", "换成青蛙跳、袋鼠跳各一轮"],
     ["地面防滑，家长在旁保护", "跳 5 分钟休息一下"], 20),
    ("health", "中班", "拍球闯关", "🏀", "手眼协调与连续拍球",
     ["小皮球", "粉笔或胶带"],
     ["地上画 5 个圆圈当关卡", "每关连续拍球 5 下", "拍满 25 下到达终点", "和爸爸比赛看谁先到"],
     ["球的大小以孩子单手能握住为准", "失败不扣关，多鼓励"], 25),
    ("health", "大班", "亲子跳绳挑战", "🪢", "连续跳绳与坚持性",
     ["儿童跳绳"],
     ["先空手摇臂跳 10 次找节奏", "带绳跳 1 次即算过，慢慢连跳", "挑战连续 5 个、10 个", "家长跳 30 秒，孩子数数"],
     ["选轻质珠节绳更容易上手", "穿运动鞋，脚踝不适就停"], 25),
    ("health", "幼小衔接", "书包整理大赛", "🎒", "自理能力与时间观念",
     ["书包", "课本文具", "计时器"],
     ["列出书包清单贴在墙上", "计时 3 分钟按清单整理", "家长检查并指出遗漏", "第二轮挑战 2 分钟完成"],
     ["以学校实际清单为准", "重点夸『又快又齐』"], 15),
    # 语言
    ("language", "小班", "动物叫-name叫", "🐮", "发音模仿与词汇",
     ["动物卡片或玩偶"],
     ["家长拿卡片问『谁来了』学叫声", "孩子说出动物名字", "轮流扮演动物互相猜", "最后把 5 种动物叫一遍"],
     ["口型夸张一些帮助模仿"], 15),
    ("language", "中班", "看图讲故事接龙", "📖", "连贯讲述与想象",
     ["绘本或图片 2-3 张"],
     ["家长开头讲一句", "孩子接着讲一句", "轮流接龙编完整故事", "给故事起个名字"],
     ["不纠正语法，只复述扩展", "孩子卡住时给两个选项"], 20),
    ("language", "大班", "小小新闻播报员", "🎤", "完整表达与自信",
     ["玩具话筒", "当天照片或画"],
     ["孩子用话筒播报今天做了什么", "按『时间+地点+事情』说三句", "家长当观众提问一个问题", "鼓掌结束换家长播报"],
     ["先示范一遍降低难度", "录音回放给孩子听很有成就感"], 20),
    ("language", "幼小衔接", "字母/汉字寻宝", "🔍", "前识字与观察",
     ["便签纸", "笔"],
     ["把认识的字写在便签上贴家里", "孩子按清单找齐 8 张", "每找到一张读出并组一个词", "最后用 3 个词说一句话"],
     ["从名字、招牌等生活字入手"], 25),
    # 社会
    ("social", "小班", "我是小小帮手", "🧹", "家庭参与感与自理",
     ["小抹布", "玩具收纳箱"],
     ["孩子把玩具送『回家』", "用小抹布擦桌子", "家长拍照表扬", "贴一枚小星星"],
     ["降低标准，过程比结果重要"], 15),
    ("social", "中班", "轮流桌游夜", "🎲", "规则意识与等待",
     ["飞行棋或拼图"],
     ["讲清规则和轮流顺序", "全家一起玩一局", "输了击掌说『下次再来』", "复盘谁遵守了规则"],
     ["故意输一次示范 gracefully", "中途想放弃先陪走完"], 30),
    ("social", "大班", "超市小管家", "🛒", "任务执行与算数运用",
     ["购物清单 3 项", "现金零钱"],
     ["孩子持清单负责找商品", "自己向店员询问位置", "比较两件商品价格选一个", "付款时递钱并说谢谢"],
     ["人多时段不宜，先从便利店开始"], 40),
    ("social", "幼小衔接", "明日计划会", "🗓️", "任务意识与表达",
     ["小白板或纸", "磁贴/贴纸"],
     ["晚饭后全家说明天安排", "孩子说出自己的 3 件事", "按顺序排 1-2-3 贴上墙", "第二天睡前逐项打勾"],
     ["让孩子体验『说到做到』"], 15),
    # 科学
    ("science", "小班", "沉浮猜猜猜", "🛁", "观察与猜想",
     ["一盆水", "积木/树叶/硬币/塑料瓶盖"],
     ["先猜哪个会沉哪个会浮", "逐个放入水中验证", "分『沉』『浮』两堆摆放", "再找一件家里的东西猜一猜"],
     ["全程看护防止玩水入迷", "结束后一起收拾"], 20),
    ("science", "中班", "影子从哪里来", "🔦", "光影现象与因果",
     ["手电筒", "玩具", "晚上或暗处"],
     ["用手电照玩具看影子", "移动光源观察影子变化", "用手做小狗/小鸟影子戏", "试一试影子能不能消失"],
     ["解释『光被挡住就有影子』即可"], 20),
    ("science", "大班", "彩虹牛奶画", "🥛", "表面张力与色彩混合",
     ["牛奶", "盘子", "色素或水彩", "棉签", "洗洁精"],
     ["盘中倒薄薄一层牛奶", "滴几滴不同颜色色素", "棉签蘸洗洁精轻点中央", "看颜色炸开成彩虹并描述"],
     ["不可食用，提醒孩子", "点完一次换棉签"], 25),
    ("science", "幼小衔接", "种子成长日记", "🌱", "长期观察与记录",
     ["绿豆", "透明杯", "湿纸巾"],
     ["绿豆贴杯壁用湿纸巾固定", "每天观察并画下变化", "量一量芽长了几个手指宽", "第 7 天总结『种子需要什么』"],
     ["每天固定时间观察更易坚持"], 10),
    # 艺术
    ("art", "小班", "手指点画小果园", "🖌️", "色彩感知与手部控制",
     ["水彩", "画纸", "湿巾"],
     ["家长画树干", "孩子用手指点出果子", "每棵树一种颜色", "数一数结了几个果"],
     ["选可水洗颜料", "完成先描述再展示"], 15),
    ("art", "中班", "纸盘小动物", "🦁", "剪贴与造型表现",
     ["纸盘", "彩纸", "安全剪刀", "胶棒"],
     ["纸盘做动物的脸", "剪耳朵胡子贴上", "画眼睛鼻子", "给动物起名字并介绍"],
     ["剪刀沿直线剪，家长协助弧线", "剪下的纸屑一起收"], 30),
    ("art", "大班", "家庭音乐会", "🎼", "节奏感受与表现",
     ["锅碗瓢盆", "筷子", "手机放歌"],
     ["锅碗当鼓探索声音", "跟一首熟悉的歌打节奏", "每人用『乐器』独奏一段", "合奏结束鞠躬谢幕"],
     ["约定停止口令防止过吵", "轻拿轻放碗碟"], 25),
    ("art", "幼小衔接", "我的第一本小书", "📚", "创作与叙事表达",
     ["A4 纸 4 张", "订书机", "彩笔"],
     ["对折装订成 8 页小书", "想一个故事有开头和结尾", "每页一图配一句话", "封面署名并读给全家听"],
     ["一句话写不出可由孩子说家长代笔"], 40),
]

DOMAINS = {"health": "健康", "language": "语言", "social": "社会", "science": "科学", "art": "艺术"}
DOMAIN_COLOR = {"health": "#2f9e6e", "language": "#3b82c4", "social": "#e8a13c", "science": "#7c5cbf", "art": "#e17055"}
DOMAIN_EMOJI = {"health": "🏃", "language": "🗣️", "social": "🤝", "science": "🔬", "art": "🎨"}
AGES = ["小班", "中班", "大班", "幼小衔接"]

CSS = """
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:"Microsoft YaHei","PingFang SC","Segoe UI",sans-serif;background:#eef2f6;color:#1f2d3d;line-height:1.7;padding:24px 16px;}
.wrap{max-width:900px;margin:0 auto;}
.no-print{margin-bottom:16px;}
.no-print button{padding:8px 20px;border:none;border-radius:8px;background:#e17055;color:#fff;font-size:14px;cursor:pointer;}
.hero{background:linear-gradient(135deg,#2b4a6f,#3b82c4);border-radius:14px;color:#fff;padding:24px 28px;margin-bottom:20px;}
.hero h1{font-size:22px;margin-bottom:6px;}
.hero p{font-size:13px;opacity:.92;}
.card{background:#fff;border-radius:14px;margin-bottom:16px;padding:20px 22px;box-shadow:0 1px 4px rgba(20,40,60,.07);border-left:5px solid var(--c);break-inside:avoid;}
.card .top{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.card .top .ic{font-size:26px;}
.card .top h2{font-size:16px;}
.card .top .tag{margin-left:auto;font-size:11px;background:var(--softbg);color:var(--c);border-radius:14px;padding:2px 10px;white-space:nowrap;}
.card .goal{font-size:13px;color:#6b7a8c;margin-bottom:10px;}
.card .grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.card .grid h3{font-size:13px;margin-bottom:4px;color:var(--c);}
.card ul{list-style:none;font-size:13px;}
.card ul li{padding:2px 0;}
.card ul li:before{content:"• ";color:var(--c);}
.tips{grid-column:1/-1;background:#fdf6ee;border-radius:10px;padding:10px 12px;font-size:12.5px;color:#8a6d3b;}
.tips b{color:#b0741f;}
.meta{font-size:11px;color:#9aa7b4;margin-top:8px;}
@media(max-width:640px){.card .grid{grid-template-columns:1fr;}}
@media print{body{background:#fff;padding:0;}.no-print{display:none;}}
"""

def render(age, acts, out_path):
    parts = [
        '<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">',
        '<title>幼儿园五大领域活动方案</title>',
        f'<style>{CSS}</style></head><body><div class="wrap">',
        '<div class="no-print"><button onclick="window.print()">🖨 打印 / 另存为 PDF</button></div>',
        f'<div class="hero"><h1>{DOMAIN_EMOJI["science"]} 幼儿园五大领域活动方案</h1>',
        f'<p>适合年龄：{age} ｜ 本页活动数：{len(acts)} ｜ 建议每天完成 1-2 个，动静搭配</p></div>',
    ]
    for i, (domain, a, title, emoji, goal, materials, steps, tips, minutes) in enumerate(acts, 1):
        c = DOMAIN_COLOR[domain]
        mat = "".join(f"<li>{m}</li>" for m in materials)
        stp = "".join(f"<li>{s}</li>" for s in steps)
        parts.append(
            f'<div class="card" style="--c:{c};--softbg:{c}1a">'
            f'<div class="top"><span class="ic">{emoji}</span>'
            f'<h2>活动 {i} · {title}</h2>'
            f'<span class="tag">{DOMAIN_EMOJI[domain]} {DOMAINS[domain]} · 约 {minutes} 分钟</span></div>'
            f'<div class="goal">🎯 目标：{goal}</div>'
            f'<div class="grid"><div><h3>🧺 材料</h3><ul>{mat}</ul></div>'
            f'<div><h3>👣 步骤</h3><ul>{stp}</ul></div>'
            f'<div class="tips">⚠️ <b>家长提示</b>：{tips}</div></div></div>'
        )
    parts.append("</div></body></html>")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("".join(parts))

def main():
    ap = argparse.ArgumentParser(description="幼儿园五大领域活动方案生成器")
    ap.add_argument("--age", default="大班", choices=AGES, help="年龄段")
    ap.add_argument("--domain", default="all", help="逗号分隔: health,language,social,science,art 或 all")
    ap.add_argument("--count", type=int, default=5, help="活动数量")
    ap.add_argument("--seed", type=int, default=None, help="随机种子（复现）")
    ap.add_argument("--out", required=True, help="输出 HTML 路径")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    domains = list(DOMAINS) if args.domain == "all" else [d.strip() for d in args.domain.split(",") if d.strip() in DOMAINS]
    pool = [a for a in ACTIVITIES if a[1] == args.age and a[0] in domains]
    if not pool:
        print(f"活动库中暂无 {args.age} × {domains} 的活动，已回退到全部年龄段该领域活动")
        pool = [a for a in ACTIVITIES if a[0] in domains]
    rng.shuffle(pool)
    picked = pool[: args.count]
    # 同领域数量均衡：尽量不重复领域排前
    picked.sort(key=lambda a: domains.index(a[0]) if a[0] in domains else 99)
    render(args.age, picked, args.out)
    print(f"已生成: {args.out}")
    print(f"年龄 {args.age} | 领域: {','.join(DOMAINS[a[0]] for a in picked)} | 活动数 {len(picked)}")

if __name__ == "__main__":
    main()
