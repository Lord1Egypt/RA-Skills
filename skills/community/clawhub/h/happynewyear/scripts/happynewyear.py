#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新年祈福脚本 (纯净版 + 红包红底视频 + 随机6首背景音乐混音)

✅ 本版修正（按你最新反馈）：
- ✅ 去掉图片区域底部重复的标题条（.vision-label）
- ✅ 只保留上方那个 wish_8 半透明红色覆盖条（显示：XXXX · XXXX）
- ✅ wish_8 覆盖条贴底显示，不再与 vision-label 叠加
- ✅ 图片裁剪从顶部开始：避免人物头部被裁掉（object-position: center top）

其余逻辑（视频/混音/截图/样式结构/依赖等）不动。
"""

import os
import json
import argparse
import sys
import re
import ssl
import time
import base64
import subprocess
import urllib.request
import urllib.error
import random

# ==========================================
# 📦 自动依赖安装模块
# ==========================================
def auto_install_dependencies():
    """检测并自动安装缺失的第三方库"""
    required_libs = ["imageio-ffmpeg"]
    optional_libs = ["imgkit", "selenium", "webdriver-manager"]

    missing_libs = []
    optional_missing = []

    for lib in required_libs:
        try:
            import_name = lib.replace("-", "_")
            __import__(import_name)
        except ImportError:
            missing_libs.append(lib)

    for lib in optional_libs:
        try:
            import_name = lib.replace("-", "_")
            __import__(import_name)
        except ImportError:
            optional_missing.append(lib)

    if missing_libs:
        try:
            cmd = [
                sys.executable, "-m", "pip", "install",
                *missing_libs,
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
                "--quiet",
                "--root-user-action=ignore"
            ]
            subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(1)
        except subprocess.CalledProcessError:
            cmd = [
                sys.executable, "-m", "pip", "install",
                *missing_libs,
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple"
            ]
            subprocess.check_call(cmd)

    if optional_missing:
        try:
            if "imgkit" in optional_missing:
                cmd = [sys.executable, "-m", "pip", "install", "imgkit",
                       "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
                       "--quiet", "--root-user-action=ignore"]
                subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif "selenium" in optional_missing and "webdriver-manager" in optional_missing:
                cmd = [sys.executable, "-m", "pip", "install", "selenium", "webdriver-manager",
                       "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
                       "--quiet", "--root-user-action=ignore"]
                subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

auto_install_dependencies()

# --- 配置区 ---
SKILL_ID = "7599556663498096690"
LLM_MODEL = "ep-20260404091506-zrxm2"
IMAGE_MODEL = "ep-20260126165602-j9z59"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
ARK_API_KEY = "7d19f69b-b938-4e75-8046-3ae5ec1d8a27"

OPEN_SPEECH_TTS_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
OPEN_SPEECH_X_API_KEY = "6ab48559-f7ca-4283-a639-2268df02bebe"
OPEN_SPEECH_RESOURCE_ID = "volc.service_type.10029"
TTS_SPEAKER = "zh_female_gaolengyujie_emo_v2_mars_bigtts"

VIDEO_OUTPUT_FILENAME = "new_year_blessing_video.mp4"
HTML_OUTPUT_FILENAME = "new_year_blessing.html"

# ✅ 截图/视频捕获目标：外层红包红底框（确保红色露出来）
CAPTURE_TARGET_ID = "captureFrame"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MUSIC_POOL = [
    os.path.join(_script_dir, "../assets/chinese-new-year.mp3"),
    os.path.join(_script_dir, "../assets/new-year.mp3"),
]

BGM_VOLUME = 0.18

# =========================
# ✅ 吉凶概率脚本
# =========================
TYPE_WEIGHTS = [
    ("上上大吉", 0.30),
    ("上吉",     0.50),
    ("中吉",     0.15),
    ("小吉",     0.05),
]

def normalize_type(t: str) -> str:
    t = (t or "").strip()
    mapping = {
        "上上大吉": "上上大吉",
        "上吉": "上吉",
        "中吉": "中吉",
        "小吉": "小吉",
    }
    return mapping.get(t, "")

def pick_fortune_type(rng: random.Random) -> str:
    x = rng.random()
    acc = 0.0
    for t, w in TYPE_WEIGHTS:
        acc += float(w)
        if x <= acc:
            return t
    return TYPE_WEIGHTS[-1][0]

def type_style_hint(t: str) -> str:
    t = normalize_type(t)
    if t == "上上大吉":
        return "氛围：大吉祥瑞，光更明亮、金色光晕更饱满，人物状态昂扬自信，画面通透，喜庆但不俗艳。"
    if t == "上吉":
        return "氛围：吉顺渐起，暖光柔和，金红点缀适度，人物从容向前，画面稳定高级。"
    if t == "中吉":
        return "氛围：平稳向好但需自持，光影对比略强，金色收敛，画面更克制，留白更多，暗示谨慎与节奏。"
    if t == "小吉":
        return "氛围：小吉宜守不宜躁，暖光偏内敛，金色更少，画面更安静沉稳，隐含提醒与边界感。"
    return "氛围：吉运温和，整体克制温暖。"

# =========================
# ✅ user_wish -> wish_8 逻辑
# =========================
def escape_html(s: str) -> str:
    if s is None:
        return ""
    return (str(s)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;"))

def _only_cjk(text: str) -> str:
    return "".join(re.findall(r"[\u4e00-\u9fff]", text or ""))

def ensure_wish8(fortune: dict) -> dict:
    if not isinstance(fortune, dict):
        return fortune
    wish8_raw = fortune.get("wish_8") or fortune.get("wish8") or ""
    wish8 = _only_cjk(str(wish8_raw))

    if len(wish8) >= 8:
        fortune["wish_8"] = wish8[:8]
        return fortune

    src = _only_cjk(str(fortune.get("user_wish") or ""))
    if len(src) < 8:
        src = _only_cjk((fortune.get("title") or "") + (fortune.get("user_wish") or ""))

    if len(src) >= 8:
        fortune["wish_8"] = src[:8]
    else:
        pad = "顺遂安康事业精进财稳"
        fortune["wish_8"] = (src + pad)[:8]
    return fortune

def format_wish8_dot(wish8: str) -> str:
    s = _only_cjk(wish8 or "")
    if len(s) < 8:
        s = (s + "顺遂安康事业精进财稳")[:8]
    left = s[:4]
    right = s[4:8]
    return f"{escape_html(left)}&nbsp;<span class='dot'>·</span>&nbsp;{escape_html(right)}"

# --- 核心工具函数 ---
def _ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def make_request(url, data, api_key, method="POST", timeout=90):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    if method == "POST":
        req = urllib.request.Request(
            url,
            data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
            headers=headers,
            method="POST"
        )
    else:
        req = urllib.request.Request(url, headers=headers, method="GET")

    with urllib.request.urlopen(req, context=_ssl_context(), timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))

def http_post_bytes(url, data, headers, timeout=120):
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, context=_ssl_context(), timeout=timeout) as resp:
        return resp.read(), (resp.headers.get("Content-Type", "") or "").lower()

def find_image_url(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if (k == "url" or k == "image_url") and isinstance(v, str) and v.startswith("http"):
                return v
            found = find_image_url(v)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = find_image_url(item)
            if found:
                return found
    return None

def extract_json_from_text(text):
    if not text:
        return None
    cleaned = text.strip().replace("```json", "```").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except Exception:
        m = re.search(r"\{[\s\S]*\}", cleaned)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
    return None

def collect_streaming_audio(raw_text):
    buf = bytearray()
    decoder = json.JSONDecoder()
    s = raw_text.strip()
    i, n = 0, len(s)
    while i < n:
        while i < n and s[i].isspace():
            i += 1
        if i >= n:
            break
        if s[i] != "{":
            i += 1
            continue
        try:
            obj, end = decoder.raw_decode(s, i)
            if isinstance(obj, dict):
                d = obj.get("data")
                if isinstance(d, str) and len(d) > 64:
                    try:
                        buf.extend(base64.b64decode(d))
                    except Exception:
                        pass
            i = end
        except Exception:
            i += 1
    return bytes(buf)

# --- 业务逻辑 ---
def get_fortune_content(user_sentence, api_key, forced_type: str):
    forced_type = normalize_type(forced_type) or "上吉"
    system_prompt = f"""
你是一位精通周易、命理与国学断签的老师傅，擅长根据生辰信息与所求之事推演流年运势。

用户会提供：姓名、性别、生辰、出生地八字信息、以及2026年所求之事。
请结合这些具体信息，推演【2026马年】个人运势，并生成一条专属签文。

【重要约束：type 已由系统按概率抽取并锁定】
- 本次锁定的吉凶判断 type = “{forced_type}”
- 你必须让输出 JSON 中的 type 字段 **严格等于** “{forced_type}”
- 并且：签诗与解曰的语气、风险提示强度、趋吉避凶建议，需要与该 type 的“吉凶程度”相匹配

生成要求：
- 必须基于用户的个人信息与所求事项来写，不允许写成通用祝福语
- 内容要有命理推断感、断语感，而不是模板口号
- 语气像签文与断语，不像客服或AI说明
- 诗句贴合用户处境，可以引用古代有名的诗词
- explanation 要具体指出：事业 / 财运 / 所求之事 的走势与提醒
- wish_8 字段必须由两个四字成语组成，用于高度概括用户的「新年所求」。格式为“四字成语 + 四字成语”，概括其愿望方向。不得输出非成语或非四字结构内容。
- 不要出现“模板”“示例”等元说明
- 严格只返回 JSON（不得有任何前后缀文本）

### 输出结构（字段必须完整）：
{{
  "id": "签名编号（中文签式风格，如：第四十二签）",
  "user_name": "用户姓名",
  "user_wish": "用户所求之事（改写为更书面表达）",
  "wish_8": "用户所求的8字总结（严格8个汉字）",
  "type": "{forced_type}",
  "title": "本签标题（四字或六字断语风格）",
  "poem": "四句签诗，用<br>分行，意象明确，与用户情境相关",
  "explanation": "断语式解签，结合八字气势、2026马年流年、以及用户所求事项给出判断与提醒"
}}
"""
    try:
        url = f"{BASE_URL}/chat/completions"
        data = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"我的信息是：{user_sentence}"}
            ]
        }
        result = make_request(url, data, api_key)
        obj = extract_json_from_text(result["choices"][0]["message"]["content"])
        if isinstance(obj, dict):
            obj["type"] = forced_type
        return obj
    except Exception as e:
        print(f"【错误】{e}")
        return None


def build_fallback_fortune(user_sentence, forced_type="上吉"):
    """无 API Key 或远程模型失败时的本地兜底签文，确保 Skill 至少可以生成 HTML。"""
    name = "有缘人"
    m = re.search(r"我叫([^，,。\s]+)", user_sentence or "")
    if m:
        name = m.group(1)[:8]
    wish = user_sentence or "新年平安顺遂"
    return ensure_wish8({
        "id": "第二十六签",
        "user_name": name,
        "user_wish": wish,
        "wish_8": "平安顺遂福运常临",
        "type": normalize_type(forced_type) or "上吉",
        "title": "福马临门",
        "poem": "春风入户启新程<br>金马衔福照前庭<br>所愿若能循正道<br>一年稳进见光明",
        "explanation": "此签主稳中有进。2026马年宜先定方向，再求突破；事业上贵在持续推进，财运上不宜急躁冒进，所求之事若能保持节奏、少受外界扰动，年中之后更容易见到转机与回响。"
    })

def download_fallback_image(fortune_data):
    title = (fortune_data.get("title") or "吉").replace("&", "＆")
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400">
<defs>
  <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#B80000"/>
    <stop offset="100%" stop-color="#7E0000"/>
  </linearGradient>
</defs>
<rect width="800" height="400" fill="url(#g)"/>
<rect x="40" y="40" width="720" height="320" rx="26" fill="none" stroke="#D4AF37" stroke-width="10"/>
<text x="400" y="220" font-size="64" fill="#FFD700" text-anchor="middle" font-family="serif">{title}</text>
</svg>"""
    return f"data:image/svg+xml;base64,{base64.b64encode(svg.encode('utf-8')).decode('utf-8')}"

def generate_image_background(fortune_data, api_key, forced_type: str):
    try:
        forced_type = normalize_type(forced_type) or normalize_type(fortune_data.get("type")) or "上吉"
        poem_text = re.sub(r"<[^>]+>", "", fortune_data.get("poem", "")).strip()
        style_hint = type_style_hint(forced_type)

        image_prompt = (
            f"为用户生成一幅新春祈福主题插画，画面必须高度个性化，严禁套用固定模板元素。"
            f"【吉凶等级锁定】：{forced_type}。{style_hint}"
            f"请仅依据以下信息提炼意象与隐喻并落成画面："
            f"用户原始信息（含八字/出生信息/背景/所求）；"
            f"签运主题：{fortune_data.get('title','')}；"
            f"用户所求：{fortune_data.get('user_wish','')}；"
            f"签诗意境：{poem_text}；"
            f"解曰要点：{fortune_data.get('explanation','')}。"
            f"画面内容要求：把“所求 + 八字信息 + 签诗意境”转化为可见的场景、人物状态、动作、环境与光影。"
            f"风格：宫崎骏漫画风格质感 + 国风新年氛围，温暖治愈，电影感构图与光影。"
            f"配色：以正红与金色为主，层次柔和高级，不过度铺满。"
            f"质量：高清、细腻、超精细细节、8k质感。"
            f"限制：无文字、无题字、无水印、无logo、无印章。"
        )
        data = {
            "model": IMAGE_MODEL,
            "prompt": image_prompt,
            "response_format": "url",
            "size": "2K",
            "watermark": True
        }
        result = make_request(f"{BASE_URL}/images/generations", data, api_key)
        image_url = find_image_url(result)

        if not image_url:
            return download_fallback_image(fortune_data)

        req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=_ssl_context(), timeout=60) as response:
            return f"data:image/jpeg;base64,{base64.b64encode(response.read()).decode('utf-8')}"
    except Exception:
        return download_fallback_image(fortune_data)

def generate_tts_audio(fortune_data):
    print("时空回声已捕获，正在塑形神谕之声...")
    if not OPEN_SPEECH_X_API_KEY:
        print("⚠️ 未配置 OPEN_SPEECH_X_API_KEY，跳过语音合成")
        return None
    raw_poem = fortune_data.get("poem", "")
    text_with_newlines = re.sub(r"<br\s*/?>", "\n", raw_poem)
    clean_text = re.sub(r"<[^>]+>", "", text_with_newlines)
    lines = [line.strip() for line in clean_text.split("\n") if line.strip()]

    poem_text = ("，".join(lines) + "。") if lines else ""
    tts_text = f"{poem_text}解曰。{fortune_data.get('explanation','')}"

    headers = {
        "x-api-key": OPEN_SPEECH_X_API_KEY,
        "X-Api-Resource-Id": OPEN_SPEECH_RESOURCE_ID,
        "Content-Type": "application/json"
    }
    payload = {
        "req_params": {
            "text": tts_text,
            "speaker": TTS_SPEAKER,
            "additions": "{\"disable_markdown_filter\":true,\"enable_language_detector\":true,\"enable_latex_tn\":true,\"disable_default_bit_rate\":true,\"max_length_to_filter_parenthesis\":0,\"cache_config\":{\"text_type\":1,\"use_cache\":true}}",
            "audio_params": {"format": "mp3", "sample_rate": 24000}
        }
    }

    try:
        raw, ctype = http_post_bytes(OPEN_SPEECH_TTS_URL, payload, headers)
        if "audio" in ctype or "octet" in ctype:
            return raw
        return collect_streaming_audio(raw.decode("utf-8", "ignore"))
    except Exception:
        return None

def format_poem(poem_text):
    clean = poem_text.replace("<br>", "。").replace("，", "。").replace(",", "。").replace("\n", "。")
    return "".join([f'<div class="poem-line">{line}</div>' for line in clean.split("。") if line.strip()])

# -----------------------
# ✅ HTML 生成（此处修正：去掉 .vision-label，只保留 wish8）
# ✅ 图片裁剪从顶部开始：object-position: center top
# -----------------------
def save_final_html(data, image_data_uri, has_video=False, video_base64="", filename=None):
    if filename is None:
        filename = HTML_OUTPUT_FILENAME

    data = ensure_wish8(data if isinstance(data, dict) else {})
    wish8_html = format_wish8_dot(data.get("wish_8", ""))

    html_template = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>2026 新年祈福</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@400;700&display=swap');

* {{ box-sizing: border-box; }}

body {{
  margin: 0;
  padding: 0;
  background: #C00000;
  font-family: 'Noto Serif SC', serif;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}}

.container {{
  width: 100%;
  max-width: 560px;
  padding: 24px;
}}

.card {{
  background: linear-gradient(180deg,#C00000,#A80000);
  border-radius: 26px;
  padding: 14px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.55);
}}

.card-inner {{
  background: #FFF8E6;
  border-radius: 18px;
  padding: 40px 30px;
  text-align: center;
}}

.fortune-id {{
  color: #666;
  font-size: 1em;
  letter-spacing: 3px;
  margin-bottom: 10px;
  font-weight: 700;
}}

.fortune-level {{
  font-family: 'Ma Shan Zheng', cursive;
  font-size: 4.8em;
  color: #C00000;
  margin: 0;
}}

.user-signature {{
  font-size: 1.2em;
  margin-top: 8px;
  font-family: 'Ma Shan Zheng', cursive;
}}

.gold-line {{
  width: 200px;
  height: 2px;
  background: #E5B8B8;
  margin: 10px auto 24px;
}}

.vision-window {{
  width: 100%;
  height: 230px;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  margin-bottom: 26px;
}}

.vision-window img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center top; /* ✅ 从顶部开始裁剪，避免裁掉人物头部 */
}}

/* ✅ 只保留这条：wish_8 覆盖条（贴底） */
.wish8 {{
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;            /* ✅ 贴底 */
  background: rgba(192,0,0,0.62);
  color: #fff;
  text-align: center;
  font-weight: 800;
  letter-spacing: 1.5px;
  padding: 6px 10px;
  font-size: 13px;
  line-height: 1.15;
  backdrop-filter: blur(1.5px);
  -webkit-backdrop-filter: blur(1.5px);
}}

.wish8 .dot {{
  font-weight: 900;
  opacity: .95;
  font-size: 14px;
}}

/* ✅ 删除了 .vision-label 相关样式 */

.poem-box {{
  background: #FFEFDB;
  border-radius: 14px;
  padding: 26px 0;
  border: 2px dotted #E5B8B8;
  margin-bottom: 24px;
}}

.poem-line {{
  font-size: 1.5em;
  font-weight: 700;
  line-height: 1.8;
}}

.explanation {{
  font-size: 1.05em;
  color: #555;
  line-height: 1.7;
  text-align: justify;
}}

.explanation strong {{
  color: #C00000;
}}

.footer {{
  margin-top: 24px;
  font-size: 0.9em;
  color: #999;
}}

@media (max-width: 480px) {{
  .container {{ padding: 10px; }}
  .card {{ padding: 10px; border-radius: 16px; }}
  .card-inner {{ padding: 20px 16px; }}
  .fortune-id {{ margin-bottom: 8px; font-size: 0.9em; }}
  .fortune-level {{ font-size: 3.0em; margin: 6px 0; }}
  .user-signature {{ font-size: 1.1em; margin-top: 6px; }}
  .gold-line {{ width: 180px; margin: 8px auto 16px; }}
  .vision-window {{ height: 230px; margin-bottom: 16px; border-radius: 10px; }}
  .wish8 {{ font-size: 12px; padding: 5px 8px; }}
  .wish8 .dot {{ font-size: 13px; }}
  .poem-box {{ padding: 20px 0; margin-bottom: 16px; border-radius: 12px; }}
  .poem-line {{ font-size: 1.25em; line-height: 1.6; }}
  .explanation {{ font-size: 0.95em; line-height: 1.6; }}
  .footer {{ margin-top: 16px; font-size: 0.85em; }}
}}
</style>
</head>

<body>
<div class="container">
  <div class="card" id="{CAPTURE_TARGET_ID}">
    <div class="card-inner">
      <div class="fortune-id">{data.get('id','')}</div>
      <div class="fortune-level">{data.get('type','')}</div>

      <div class="user-signature">祈福人：{data.get('user_name','')}</div>
      <div class="gold-line"></div>

      <div class="vision-window">
        <img src="{image_data_uri}">
        <div class="wish8">{wish8_html}</div>
      </div>

      <div class="poem-box">
        {format_poem(data.get('poem',''))}
      </div>

      <div class="explanation">
        <strong>【解曰】</strong>{data.get('explanation','')}
      </div>

      <div class="footer">新年签运 · 2026 马年</div>
    </div>
  </div>
</div>
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_template)
    return filename

# -----------------------
# ✅ 背景音乐：随机 6 首之一
# -----------------------
def pick_random_music(music_pool):
    valid = [p for p in (music_pool or []) if p and os.path.exists(p)]
    if not valid:
        return None
    return random.choice(valid)

def mix_tts_with_bgm(tts_mp3_path, bgm_path, mixed_out_path):
    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return None

    if not bgm_path or not os.path.exists(bgm_path):
        return None

    cmd = [
        ffmpeg_exe, "-y",
        "-i", tts_mp3_path,
        "-stream_loop", "-1", "-i", bgm_path,
        "-filter_complex",
        f"[1:a]volume={BGM_VOLUME}[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=2",
        "-c:a", "libmp3lame",
        "-q:a", "2",
        mixed_out_path
    ]
    try:
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return mixed_out_path
    except Exception:
        return None

def capture_html_to_image(html_path, output_img):
    """
    ✅ 替换点（只改这里）：
    - 优先用 Playwright 对 #captureFrame 做元素截图
    - 动态读取 bounding_box 高度并调整 viewport，确保从上到下完整截取，不截断
    - Playwright 不可用再回退到原 imgkit / selenium 方案（其余逻辑不动）
    """
    # ① Playwright 元素截图（优先）
    try:
        from playwright.sync_api import sync_playwright
        import math as _math

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-software-rasterizer",
                    "--disable-background-timer-throttling",
                    "--disable-backgrounding-occluded-windows",
                    "--disable-renderer-backgrounding",
                ]
            )

            # 先给一个足够的高度，让页面内容完整布局出来
            context = browser.new_context(
                viewport={"width": 390, "height": 1400},
                device_scale_factor=2
            )
            page = context.new_page()

            page.goto(f"file://{os.path.abspath(html_path)}", wait_until="networkidle", timeout=30000)
            page.wait_for_timeout(180)

            locator = page.locator(f"#{CAPTURE_TARGET_ID}")
            locator.wait_for(state="visible", timeout=10000)

            # 确保从页面顶部开始布局/截取（避免某些环境滚动偏移）
            page.evaluate("window.scrollTo(0, 0)")
            page.wait_for_timeout(80)
            locator.scroll_into_view_if_needed()
            page.wait_for_timeout(120)

            box = locator.bounding_box()
            if box and box.get("height"):
                needed_h = int(_math.ceil(box["height"] + 80))  # 给点缓冲，避免阴影/圆角被裁
                needed_h = min(max(600, needed_h), 9000)
                page.set_viewport_size({"width": 390, "height": needed_h})
                page.wait_for_timeout(120)
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(80)
                locator.scroll_into_view_if_needed()
                page.wait_for_timeout(120)

            # 元素级截图：从元素顶部到元素底部完整截取
            locator.screenshot(path=output_img)

            context.close()
            browser.close()

        if os.path.exists(output_img) and os.path.getsize(output_img) > 1200:
            return True
    except Exception:
        pass

    # ② 原 imgkit 方案（保持不动）
    try:
        import imgkit
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        options = {
            'width': 390,
            'height': 844,
            'format': 'png',
            'encoding': 'UTF-8',
            'quiet': '',
            'disable-smart-width': '',
            'enable-local-file-access': ''
        }
        imgkit.from_string(html_content, output_img, options=options)
        if os.path.exists(output_img) and os.path.getsize(output_img) > 0:
            return True
    except Exception:
        pass

    # ③ 原 selenium 方案（保持不动）
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--force-device-scale-factor=2")
        chrome_options.add_argument("--window-size=390,844")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--no-first-run")

        driver = None
        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            driver.get(f"file://{os.path.abspath(html_path)}")
            time.sleep(1)
            driver.save_screenshot(output_img)
            if os.path.exists(output_img) and os.path.getsize(output_img) > 0:
                return True
        finally:
            if driver:
                driver.quit()
    except Exception:
        pass

    return False

def generate_video(html_path, audio_bytes, music_pool):
    print("正在为您描绘这幅锦绣签程（预计1分钟）...")

    try:
        import imageio_ffmpeg
    except ImportError:
        print("❌ 缺少 imageio-ffmpeg 依赖，无法合成视频")
        return

    temp_img = "temp_capture.png"
    temp_tts = "temp_tts.mp3"
    temp_mix = "temp_mix.mp3"

    with open(temp_tts, "wb") as f:
        f.write(audio_bytes)

    bgm = pick_random_music(music_pool)
    mixed_audio = mix_tts_with_bgm(temp_tts, bgm, temp_mix) if bgm else None
    final_audio_path = mixed_audio if mixed_audio and os.path.exists(mixed_audio) else temp_tts

    if not capture_html_to_image(html_path, temp_img):
        print("❌ HTML 截图失败，无法生成视频")
        for p in [temp_tts, temp_mix]:
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass
        return

    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_exe, "-y",
            "-loop", "1", "-i", temp_img,
            "-i", final_audio_path,
            "-c:v", "libx264",
            "-tune", "stillimage",
            "-c:a", "aac",
            "-b:a", "192k",
            "-pix_fmt", "yuv420p",
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
            "-shortest",
            VIDEO_OUTPUT_FILENAME
        ]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if not os.path.exists(VIDEO_OUTPUT_FILENAME):
            print("❌ 视频文件未生成")
            return

        if os.path.getsize(VIDEO_OUTPUT_FILENAME) < 1000:
            print("❌ 视频文件损坏")
            try:
                os.remove(VIDEO_OUTPUT_FILENAME)
            except Exception:
                pass
            return

    except Exception as e:
        print(f"❌ 视频合成失败: {e}")
        if os.path.exists(VIDEO_OUTPUT_FILENAME):
            try:
                os.remove(VIDEO_OUTPUT_FILENAME)
            except Exception:
                pass
    finally:
        for p in [temp_img, temp_tts, temp_mix]:
            try:
                if os.path.exists(p):
                    os.remove(p)
            except Exception:
                pass

def get_api_key():
    if "--api-key" in sys.argv:
        idx = sys.argv.index("--api-key")
        if idx + 1 < len(sys.argv):
            return sys.argv[idx + 1]
    return ARK_API_KEY

def parse_music_files_arg(s):
    if not s:
        return None
    parts = [p.strip() for p in s.split(",") if p.strip()]
    return parts or None

def main():
    global VIDEO_OUTPUT_FILENAME, HTML_OUTPUT_FILENAME
    parser = argparse.ArgumentParser(description="2026新年祈福")
    parser.add_argument("--user-info", type=str, help="用户信息")
    parser.add_argument("--api-key", type=str, help="API Key")
    parser.add_argument("--music-files", type=str, help="6首背景音乐路径（逗号分隔），不传则用默认池")
    parser.add_argument("--output-format", type=str, default="video", choices=["html", "video", "both"], help="输出格式: html/video/both，默认 video，即主输出 MP4")
    parser.add_argument("--output-file", type=str, default=VIDEO_OUTPUT_FILENAME, help="主输出 MP4 文件名或路径，默认 new_year_blessing_video.mp4")
    parser.add_argument("--html-output-file", type=str, default=HTML_OUTPUT_FILENAME, help="中间 HTML 文件名或路径，默认 new_year_blessing.html")
    parser.add_argument("--seed", type=str, default="", help="可选：抽签随机种子（为空则自动）")
    parser.add_argument("--output-dir", type=str, default=".", help="输出目录，默认当前目录")
    args = parser.parse_args()

    VIDEO_OUTPUT_FILENAME = args.output_file
    HTML_OUTPUT_FILENAME = args.html_output_file

    os.makedirs(args.output_dir, exist_ok=True)
    os.chdir(args.output_dir)

    user_input = args.user_info
    if not user_input:
        if sys.stdin.isatty():
            print("请输入祈愿信息 (例: 我叫李云龙，男，ESTP，求事业顺利):")
            user_input = input("👉 ").strip()
        else:
            user_input = "我叫李云龙，男，1995年10月1日出生，ESTP，2026年想要平安幸福"

    music_pool = parse_music_files_arg(args.music_files) or DEFAULT_MUSIC_POOL

    seed_text = (args.seed or "").strip()
    if not seed_text:
        seed_text = f"{int(time.time())}-{user_input[:24]}-{random.randint(0, 10_000_000)}"
    rng = random.Random(seed_text)
    forced_type = pick_fortune_type(rng)

    print("正在锚定时空坐标，解析命运波段...")
    api_key = args.api_key or get_api_key()
    if api_key:
        fortune = get_fortune_content(user_input, api_key, forced_type=forced_type)
    else:
        print("⚠️ 未配置 ARK_API_KEY，将使用本地兜底签文生成 HTML")
        fortune = build_fallback_fortune(user_input, forced_type=forced_type)

    if not fortune:
        print("⚠️ 远程模型未返回有效内容，将使用本地兜底签文")
        fortune = build_fallback_fortune(user_input, forced_type=forced_type)

    fortune["type"] = normalize_type(forced_type) or fortune.get("type") or "上吉"

    print("因果模型收敛完成，正在生成全息神谕...")
    img_uri = generate_image_background(fortune, api_key, forced_type=fortune["type"])
    audio_bytes = generate_tts_audio(fortune)

    html_path = save_final_html(fortune, img_uri, False, "")

    if args.output_format == "html":
        print(f"✅ HTML 已生成: {os.path.abspath(html_path)}")
        print(json.dumps({"status": "success", "output_type": "html", "output_path": os.path.abspath(html_path)}, ensure_ascii=False))
        return

    # OpenClaw Skill 的主输出是 MP4；HTML 只作为视频截图与预览的中间资产。
    if not audio_bytes:
        print("❌ 无法生成 MP4：语音合成失败或未配置 OPEN_SPEECH_X_API_KEY / BYTE_TTS_API_KEY")
        print(f"ℹ️ 已保留中间 HTML: {os.path.abspath(html_path)}")
        print(json.dumps({
            "status": "failed",
            "output_type": "mp4",
            "error": "missing_tts_audio",
            "html_preview_path": os.path.abspath(html_path)
        }, ensure_ascii=False))
        sys.exit(2)

    generate_video(html_path, audio_bytes, music_pool)
    if os.path.exists(VIDEO_OUTPUT_FILENAME):
        print(f"✅ MP4 已生成: {os.path.abspath(VIDEO_OUTPUT_FILENAME)}")
        print(json.dumps({
            "status": "success",
            "output_type": "mp4",
            "output_path": os.path.abspath(VIDEO_OUTPUT_FILENAME),
            "html_preview_path": os.path.abspath(html_path) if os.path.exists(html_path) else ""
        }, ensure_ascii=False))
    else:
        print("❌ MP4 生成失败：截图工具或 ffmpeg 环境不可用")
        print(json.dumps({
            "status": "failed",
            "output_type": "mp4",
            "error": "video_generation_failed",
            "html_preview_path": os.path.abspath(html_path)
        }, ensure_ascii=False))
        sys.exit(3)

    return

if __name__ == "__main__":
    main()
