#!/usr/bin/env python3
"""Pet Emotion Recognition — AI-powered pet emotion analyzer using DashScope multimodal API.

Usage:
    python pet_emotion.py --image path/to/pet.jpg [--output report.html] [--api dashscope]
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

# --- Constants ---
EMOTIONS = ["快乐", "悲伤", "愤怒", "恐惧", "放松", "警觉"]
EMOTION_EMOJI = {
    "快乐": "😊", "悲伤": "😢", "愤怒": "😠",
    "恐惧": "😨", "放松": "😌", "警觉": "🧐"
}
EMOTION_COLORS = {
    "快乐": "#4CAF50", "悲伤": "#2196F3", "愤怒": "#F44336",
    "恐惧": "#FF9800", "放松": "#8BC34A", "警觉": "#9C27B0"
}

MIME_MAP = {
    ".jpg": "jpeg", ".jpeg": "jpeg", ".png": "png",
    ".webp": "webp", ".bmp": "bmp", ".gif": "gif"
}

DASHSCOPE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def find_api_key():
    """Find DashScope API key from env or config file."""
    # Priority 1: DASHSCOPE_API_KEY env
    key = os.environ.get("DASHSCOPE_API_KEY", "")
    if key:
        return key

    # Priority 2: OPENAI_API_KEY (compatible mode)
    key = os.environ.get("OPENAI_API_KEY", "")
    if key:
        return key

    # Priority 3: Config file
    config_paths = [
        os.path.expanduser("~/.workbuddy/config/dashscope.json"),
        os.path.expanduser("~/.dashscope/config.json"),
    ]
    for cfg in config_paths:
        if os.path.exists(cfg):
            try:
                with open(cfg, encoding="utf-8") as f:
                    data = json.load(f)
                    if "api_key" in data:
                        return data["api_key"]
                    if "DASHSCOPE_API_KEY" in data:
                        return data["DASHSCOPE_API_KEY"]
            except Exception:
                pass
    return ""


def encode_image(image_path):
    """Encode image to base64 data URL."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"图片不存在: {image_path}")
    
    ext = path.suffix.lower()
    mime = MIME_MAP.get(ext, "jpeg")
    
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    
    return f"data:image/{mime};base64,{data}", mime


def build_prompt():
    """Build the analysis prompt for pet emotion recognition."""
    return """你是一位专业的宠物行为学家和情感分析师。请仔细分析这张照片中的宠物（猫或狗）的情绪状态。

分析要点：
1. 首先判断图片中是否有猫或狗
2. 观察宠物的面部表情（眼睛、耳朵、嘴巴）
3. 观察身体姿态（尾巴、背部、四肢）
4. 综合判断情绪状态

情绪分类（6选1）：
- 快乐：放松愉悦，可能摇尾巴、眯眼、张嘴（像在笑）
- 悲伤：耷拉耳朵、蜷缩、无精打采、回避镜头
- 愤怒：龇牙、竖毛、耳朵后压、身体僵硬
- 恐惧：夹尾、躲藏、瞳孔放大、身体低伏
- 放松：眯眼打盹、肚皮朝上、完全舒展
- 警觉：竖耳凝视、身体紧绷、尾巴直立

请严格返回以下JSON格式，不要包含任何其他内容：
{"species": "dog"|"cat"|"unknown", "emotion": "快乐"|"悲伤"|"愤怒"|"恐惧"|"放松"|"警觉", "confidence": 0.0-1.0, "reason": "一句话简短判断依据（20字以内）", "suggestion": "给主人的互动建议（30字以内）", "expression_desc": "表情特征描述（15字以内）", "body_desc": "身体姿态描述（15字以内）"}"""


def call_dashscope(api_key, image_data_url, model="qwen-vl-max"):
    """Call DashScope multimodal API for emotion analysis."""
    import urllib.request
    import urllib.error
    
    payload = json.dumps({
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": image_data_url}},
                {"type": "text", "text": build_prompt()}
            ]
        }],
        "temperature": 0.1,
        "max_tokens": 500
    }).encode()
    
    req = urllib.request.Request(
        DASHSCOPE_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        raise RuntimeError(f"API请求失败 (HTTP {e.code}): {error_body}")


def parse_response(api_result):
    """Parse DashScope API response into structured result."""
    try:
        content = api_result["choices"][0]["message"]["content"]
        # Try to extract JSON from response
        content = content.strip()
        if content.startswith("```"):
            # Remove markdown code blocks
            lines = content.split("\n")
            content = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        
        result = json.loads(content)
        
        # Validate fields
        species = result.get("species", "unknown")
        emotion = result.get("emotion", "未知")
        confidence = float(result.get("confidence", 0.5))
        reason = result.get("reason", "无法判断")
        suggestion = result.get("suggestion", "")
        expression_desc = result.get("expression_desc", "")
        body_desc = result.get("body_desc", "")
        
        # Ensure emotion is valid
        if emotion not in EMOTIONS:
            emotion = "未知"
        
        return {
            "species": species,
            "emotion": emotion,
            "confidence": min(max(confidence, 0.0), 1.0),
            "reason": reason,
            "suggestion": suggestion,
            "expression_desc": expression_desc,
            "body_desc": body_desc,
            "emoji": EMOTION_EMOJI.get(emotion, "❓"),
            "color": EMOTION_COLORS.get(emotion, "#999"),
            "raw": result
        }
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        # Fallback: try to extract emotion from raw text
        raw_text = api_result.get("choices", [{}])[0].get("message", {}).get("content", str(api_result))
        return {
            "species": "unknown",
            "emotion": "未知",
            "confidence": 0.0,
            "reason": f"解析失败: {str(e)[:50]}",
            "suggestion": "",
            "expression_desc": "",
            "body_desc": "",
            "emoji": "❓",
            "color": "#999",
            "raw": {"error": str(e), "raw_text": raw_text[:200]}
        }


def generate_html_report(result, image_path, output_path):
    """Generate interactive HTML report using the template."""
    # Read template
    template_path = Path(__file__).parent.parent / "assets" / "report_template.html"
    if template_path.exists():
        with open(template_path, encoding="utf-8") as f:
            html = f.read()
    else:
        html = get_default_template()
    
    # Encode image for embedding
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    ext = Path(image_path).suffix.lower()
    mime = MIME_MAP.get(ext, "jpeg")
    img_src = f"data:image/{mime};base64,{img_b64}"
    
    # Prepare template variables
    emotion_distribution = []
    for e in EMOTIONS:
        val = result["confidence"] if e == result["emotion"] else round((1 - result["confidence"]) / (len(EMOTIONS) - 1), 2) if result["emotion"] != "未知" else round(1/len(EMOTIONS), 2)
        emotion_distribution.append({
            "name": e,
            "value": val,
            "color": EMOTION_COLORS.get(e, "#999"),
            "emoji": EMOTION_EMOJI.get(e, "❓")
        })
    
    # Replace placeholders
    html = html.replace("{{IMAGE_SRC}}", img_src)
    html = html.replace("{{SPECIES}}", result.get("species", "unknown"))
    html = html.replace("{{SPECIES_LABEL}}", {"dog": "🐕 狗狗", "cat": "🐈 猫咪"}.get(result.get("species"), "❓ 未知"))
    html = html.replace("{{EMOTION}}", result.get("emotion", "未知"))
    html = html.replace("{{EMOTION_EMOJI}}", result.get("emoji", "❓"))
    html = html.replace("{{CONFIDENCE}}", str(int(result.get("confidence", 0) * 100)))
    html = html.replace("{{CONFIDENCE_DECIMAL}}", str(result.get("confidence", 0)))
    html = html.replace("{{REASON}}", result.get("reason", ""))
    html = html.replace("{{SUGGESTION}}", result.get("suggestion", ""))
    html = html.replace("{{EXPRESSION_DESC}}", result.get("expression_desc", ""))
    html = html.replace("{{BODY_DESC}}", result.get("body_desc", ""))
    html = html.replace("{{COLOR}}", result.get("color", "#999"))
    html = html.replace("{{TIMESTAMP}}", time.strftime("%Y-%m-%d %H:%M:%S"))
    html = html.replace("{{EMOTION_DISTRIBUTION}}", json.dumps(emotion_distribution, ensure_ascii=False))
    html = html.replace("{{RESULT_JSON}}", json.dumps({
        "reason": result.get("reason", ""),
        "expression_desc": result.get("expression_desc", ""),
        "body_desc": result.get("body_desc", ""),
        "suggestion": result.get("suggestion", ""),
        "emotion": result.get("emotion", ""),
        "color": result.get("color", "#999")
    }, ensure_ascii=False))
    
    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return output_path


def get_default_template():
    """Return a minimal default HTML template as a fallback."""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>宠物情绪识别报告</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;background:linear-gradient(135deg,#f5f7fa 0%,#c3cfe2 100%);min-height:100vh;display:flex;justify-content:center;align-items:center;padding:20px}
.card{background:#fff;border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.12);max-width:600px;width:100%;overflow:hidden}
.header{background:linear-gradient(135deg,{{COLOR}} 0%,{{COLOR}}dd 100%);color:#fff;padding:30px;text-align:center}
.header .emoji{font-size:64px;display:block;margin-bottom:10px}
.header h1{font-size:22px;margin-bottom:8px}
.header .confidence{font-size:14px;opacity:.85}
.header .confidence-bar{background:rgba(255,255,255,.25);border-radius:10px;height:8px;margin-top:10px;overflow:hidden}
.header .confidence-fill{background:#fff;height:100%;border-radius:10px;transition:width 1.2s ease}
.image-section{padding:20px 30px;text-align:center;background:#fafafa}
.image-section img{max-width:100%;max-height:300px;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,.1)}
.info-section{padding:20px 30px}
.info-card{display:flex;align-items:flex-start;gap:12px;padding:14px 16px;background:#f8f9fa;border-radius:12px;margin-bottom:10px;border-left:4px solid {{COLOR}}}
.info-card .icon{font-size:22px;flex-shrink:0}
.info-card .label{font-size:12px;color:#999}
.info-card .value{font-size:14px;color:#333;line-height:1.6}
.chart-section{padding:0 30px 25px}
.chart-section h3{font-size:16px;margin-bottom:12px;color:#333}
.chart-container{position:relative;height:250px}
.footer{text-align:center;padding:15px;color:#bbb;font-size:12px}
</style>
</head>
<body>
<div class="card">
<div class="header">
<span class="emoji">{{EMOTION_EMOJI}}</span>
<h1>{{SPECIES_LABEL}} · {{EMOTION}}</h1>
<div class="confidence">置信度 {{CONFIDENCE}}%</div>
<div class="confidence-bar"><div class="confidence-fill" style="width:{{CONFIDENCE}}%"></div></div>
</div>
<div class="image-section"><img src="{{IMAGE_SRC}}" alt="宠物照片"></div>
<div class="info-section" id="infoSection"></div>
<div class="chart-section">
<h3>📊 情绪分布雷达图</h3>
<div class="chart-container"><canvas id="emotionChart"></canvas></div>
</div>
<div class="footer">🐱🐶 AI宠物情绪识别 · {{TIMESTAMP}}</div>
</div>
<script>
var infoCards = [];
var r = {{RESULT_JSON}};
if(r.reason) infoCards.push({i:'🔍',l:'判断依据',v:r.reason});
if(r.expression_desc) infoCards.push({i:'😺',l:'面部表情',v:r.expression_desc});
if(r.body_desc) infoCards.push({i:'🐾',l:'身体姿态',v:r.body_desc});
if(r.suggestion) infoCards.push({i:'💡',l:'互动建议',v:r.suggestion});
document.getElementById('infoSection').innerHTML = infoCards.map(function(c){
  return '<div class="info-card"><span class="icon">'+c.i+'</span><div><div class="label">'+c.l+'</div><div class="value">'+c.v+'</div></div></div>';
}).join('');
var data = {{EMOTION_DISTRIBUTION}};
new Chart(document.getElementById('emotionChart'),{
type:'radar',
data:{labels:data.map(function(d){return d.emoji+' '+d.name}),datasets:[{label:'情绪概率',data:data.map(function(d){return d.value}),backgroundColor:'{{COLOR}}20',borderColor:'{{COLOR}}',borderWidth:2.5,pointBackgroundColor:data.map(function(d){return d.color}),pointBorderColor:'#fff',pointBorderWidth:2,pointRadius:5}]},
options:{responsive:true,maintainAspectRatio:false,scales:{r:{min:0,max:1,ticks:{stepSize:.2,display:false}}},plugins:{legend:{display:false}}}
});
</script>
</body>
</html>"""


def generate_summary(result):
    """Generate a text summary for the conversation."""
    species_label = {"dog": "🐕 狗狗", "cat": "🐈 猫咪"}.get(result.get("species"), "宠物")
    
    lines = [
        f"## {result['emoji']} 情绪识别结果",
        "",
        f"| 项目 | 详情 |",
        f"|------|------|",
        f"| 物种 | {species_label} |",
        f"| 情绪 | {result['emoji']} **{result['emotion']}** |",
        f"| 置信度 | **{int(result['confidence'] * 100)}%** |",
    ]
    if result.get("reason"):
        lines.append(f"| 判断依据 | {result['reason']} |")
    if result.get("suggestion"):
        lines.append(f"| 互动建议 | {result['suggestion']} |")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="AI宠物情绪识别")
    parser.add_argument("--image", required=True, help="宠物照片路径")
    parser.add_argument("--output", default=None, help="HTML报告输出路径")
    parser.add_argument("--api", default="dashscope", choices=["dashscope", "openai"], help="API类型")
    args = parser.parse_args()
    
    # Set default output path
    if args.output is None:
        img_stem = Path(args.image).stem
        args.output = f"pet_emotion_{img_stem}.html"
    
    # Find API key
    api_key = find_api_key()
    if not api_key:
        print("ERROR: 未找到 API Key。请设置环境变量 DASHSCOPE_API_KEY 或 OPENAI_API_KEY")
        print("你可以在 https://dashscope.console.aliyun.com/ 获取 DashScope API Key")
        sys.exit(1)
    
    print(f"🐱🐶 宠物情绪识别中...")
    print(f"   图片: {args.image}")
    
    # Encode image
    try:
        image_data_url, _ = encode_image(args.image)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    # Call API
    try:
        api_result = call_dashscope(api_key, image_data_url)
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    # Parse response
    result = parse_response(api_result)
    
    if result["species"] == "unknown" and result["emotion"] == "未知":
        print("⚠️ 未能识别到宠物或情绪，请确认上传的是猫/狗的清晰照片")
        print(f"   API原始返回: {result['raw']}")
        sys.exit(1)
    
    # Generate report
    output_path = generate_html_report(result, args.image, args.output)
    
    # Print summary
    print()
    print(generate_summary(result))
    print()
    print(f"📄 报告已生成: {output_path}")
    print(f"REPORT_PATH: {os.path.abspath(output_path)}")


if __name__ == "__main__":
    main()
