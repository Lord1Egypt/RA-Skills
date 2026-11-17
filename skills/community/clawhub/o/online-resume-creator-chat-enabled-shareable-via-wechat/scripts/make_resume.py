# -*- coding: utf-8 -*-
"""
把简历数据生成「可对话的单文件 HTML 网页」。
输出 index.html：内联 CSS+JS，零依赖、纯离线，内置前端关键词匹配的简历助手。

两种用法:
  1) 直接改下面 RESUME 字典后运行:
       python make_resume.py
  2) 从 JSON 读取（字段同 RESUME）:
       python make_resume.py --data resume.json

依赖: 无第三方库（纯标准库）。输出到 --out（默认 index.html）。

匹配逻辑: 遍历 RULES，命中关键词 -> 返回对应 SECTION；多命中取最长匹配；
未命中/空输入 -> 返回引导语。所有内容写死在前端，离线即可跑（非真 AI）。
"""
import argparse
import html
import json
import os

# ===================== 1. 简历数据（改这里） =====================
# 安全提示：以下为「占位示例」，发布/分享前请勿写入真实隐私（电话/邮箱/年薪）。
# 使用者请替换为自己的信息，或通过 --data resume.json 传入。
RESUME = {
    "name": "您的姓名",
    "title": "AI博士 · 数据科学家",
    "subtitle": "10年+ 大厂 AI 落地实战派（公司A / 公司B / 公司C）",
    "contact": "电话 1xx-xxxx-xxxx ｜ 邮箱 your@email.com",
    "sections": {
        "基本信息": "您的姓名，AI 博士，10 年以上大厂 AI 落地经验，曾任公司A、公司B、公司C等公司核心技术/管理岗，带过 X 人团队，发表 N 篇论文、M 部专著，期望年薪面议。",
        "工作经历": "公司A/公司B/公司C 等头部企业 AI 核心技术与管理经历，主导多个从 0 到 1 的 AI 落地项目，管理 X 人团队，打通算法到业务的全链路。",
        "核心技能": "大模型应用、机器学习、数据科学、AI 战略落地、团队管理、企业经营决策支持。",
        "重点项目": "多个 B 端 AI 预测与决策系统：从需求洞察、数据治理、模型研发到上线运营全流程主导，显著提升经营效率与预测准确率。",
        "教育背景": "博士学历，人工智能 / 数据科学方向，扎实的科研与工程复合背景。",
        "论文专著": "发表论文 N 篇，出版专著 M 部，覆盖 AI 算法、产业落地与战略应用。",
    },
    "rules": [
        ("工作经历", ["工作经历", "做过什么", "哪家公司", "公司A", "公司B", "公司C", "职业", "履历", "背景"]),
        ("核心技能", ["技能", "擅长", "能力", "技术", "大模型", "机器学习", "数据科学"]),
        ("重点项目", ["项目", "做过什么项目", "案例", "成果", "落地", "系统", "b端", "b 端", "销售预测"]),
        ("教育背景", ["学历", "教育", "学校", "博士", "毕业", "专业"]),
        ("论文专著", ["论文", "专著", "发表", "著作", "学术", "研究"]),
        ("基本信息", ["你是谁", "介绍", "你好", "简历", "个人", "资料", "联系方式", "电话", "邮箱", "年薪", "工资", "团队", "期望"]),
    ],
    "expire": None,  # 如 "2026-08-10T23:59:59+08:00" 则到时整页替换提示；None=永久
}
# ===================================================================


def build_html(data: dict) -> str:
    name = html.escape(data["name"])
    title = html.escape(data["title"])
    subtitle = html.escape(data["subtitle"])
    contact = html.escape(data["contact"])
    sections = data["sections"]
    rules = data["rules"]
    expire = data.get("expire")

    # SECTION 文本（前端常量）
    section_js = "const SECTION = " + json.dumps(sections, ensure_ascii=False, indent=2) + ";"
    rules_js = "const RULES = " + json.dumps(
        [{"k": k, "w": w} for k, w in rules], ensure_ascii=False, indent=2
    ) + ";"

    expire_guard = ""
    if expire:
        expire_guard = f"""
<script>
(function(){{
  var expire = new Date('{expire}').getTime();
  if (Date.now() > expire){{
    document.body.innerHTML = '<div style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:14px;font-family:system-ui,-apple-system,\\'PingFang SC\\',sans-serif;background:#0b1220;color:#e8eefb;text-align:center;padding:24px">'
      + '<div style="font-size:22px;font-weight:800">页面已过期</div>'
      + '<div style="font-size:14px;opacity:.75;line-height:1.7">本简历页面有效期至 <b>{expire[:10]}</b>，已停止访问。<br>如需查看，请联系{name}。</div>'
      + '</div>';
  }}
}})();
</script>"""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{name} · 个人简历（对话版）</title>
<meta name="description" content="{name}个人简历（对话版），{subtitle}，可对话式了解工作经历/项目/论文。" />
<meta property="og:title" content="{name} · 个人简历（对话版）" />
<meta property="og:description" content="{subtitle}" />
<meta property="og:type" content="website" />
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: system-ui, -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif;
         background: linear-gradient(160deg, #0b1220, #122036); color: #e8eefb; min-height: 100vh;
         display: flex; align-items: center; justify-content: center; padding: 20px; }}
  .wrap {{ width: 100%; max-width: 480px; }}
  .card {{ background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08);
          border-radius: 18px; padding: 28px 22px; backdrop-filter: blur(6px); }}
  .avatar {{ width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg,#38bdf8,#6366f1);
            display:flex; align-items:center; justify-content:center; font-size:26px; font-weight:800; margin-bottom:14px; }}
  h1 {{ font-size: 22px; }}
  .sub {{ color: #7dd3fc; font-size: 14px; margin-top: 4px; }}
  .tag {{ color: #94a3b8; font-size: 12px; margin-top: 10px; line-height:1.6; }}
  .chat {{ margin-top: 18px; background: rgba(0,0,0,.18); border-radius: 12px; padding: 12px;
          height: 300px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }}
  .msg {{ max-width: 85%; padding: 9px 12px; border-radius: 12px; font-size: 13px; line-height: 1.6; }}
  .bot {{ align-self: flex-start; background: rgba(56,189,248,.14); color: #dbeafe; }}
  .me {{ align-self: flex-end; background: #2563eb; color: #fff; }}
  .row {{ display: flex; gap: 8px; margin-top: 12px; }}
  input {{ flex: 1; padding: 10px 12px; border-radius: 10px; border: 1px solid rgba(255,255,255,.12);
          background: rgba(0,0,0,.25); color: #fff; font-size: 13px; outline: none; }}
  button {{ padding: 10px 16px; border: none; border-radius: 10px; background: #38bdf8; color: #06121f;
           font-weight: 700; cursor: pointer; font-size: 13px; }}
  .hint {{ color:#64748b; font-size:11px; margin-top:8px; text-align:center; }}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <div class="avatar">{name[:1]}</div>
    <h1>{name}</h1>
    <div class="sub">{title}</div>
    <div class="tag">{subtitle}<br>{contact}</div>
    <div class="chat" id="chat"></div>
    <div class="row">
      <input id="inp" placeholder="问我工作经历 / 项目 / 技能 / 论文…" />
      <button onclick="send()">发送</button>
    </div>
    <div class="hint">这是前端关键词匹配的简历助手（离线可跑，非大模型）</div>
  </div>
</div>
<script>
{section_js}
{rules_js}
const chat = document.getElementById('chat');
function addMsg(text, who){{
  const d = document.createElement('div');
  d.className = 'msg ' + who;
  d.textContent = text;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}}
function answer(q){{
  const qs = q.toLowerCase();
  let best = null, bestLen = 0;
  for (const r of RULES) {{
    for (const w of r.w) {{
      if (qs.includes(w.toLowerCase()) && w.length > bestLen) {{ best = r.k; bestLen = w.length; }}
    }}
  }}
  if (!best) return '我仅能介绍{name}简历相关内容～你可以问我：工作经历、核心技能、重点项目、教育背景、论文专著等。';
  return SECTION[best];
}}
function send(){{
  const inp = document.getElementById('inp');
  const q = inp.value.trim();
  if (!q) return;
  addMsg(q, 'me'); inp.value = '';
  setTimeout(() => addMsg(answer(q), 'bot'), 220);
}}
document.getElementById('inp').addEventListener('keydown', e => {{ if (e.key === 'Enter') send(); }});
addMsg('你好，我是 {name} 的 AI 简历助手。问我工作经历、核心技能、重点项目、教育背景或论文专著，我来详细介绍。', 'bot');
</script>
{expire_guard}
</body>
</html>"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", help="简历 JSON 文件路径（字段同脚本内 RESUME）")
    ap.add_argument("--out", default="index.html")
    a = ap.parse_args()

    data = RESUME
    if a.data:
        with open(a.data, "r", encoding="utf-8") as f:
            data = json.load(f)

    html_text = build_html(data)
    with open(a.out, "w", encoding="utf-8") as f:
        f.write(html_text)
    print("resume webpage saved:", os.path.abspath(a.out),
          f"({len(html_text)} bytes, 板块 {len(data['sections'])} 个)")


if __name__ == "__main__":
    main()
