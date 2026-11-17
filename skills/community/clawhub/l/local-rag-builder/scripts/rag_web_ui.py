"""
local-rag-builder Web 可视化设置界面
v0.2.0
内嵌 HTML 面板，可直接修改 Python 核心配置
支持：输入源配置、GuardStack、文档切片三层流水线、策略级覆盖、AI 推荐
"""

import os
import sys
import json
import http.server
import socketserver
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import load_config, save_config, reset_config, DEFAULT_CONFIG
from prompt_manager import load_template, save_template, reset_template
from embedding_model_manager import list_downloaded_models, RECOMMENDED_MODELS
from knowledge_base_manager import list_knowledge_bases, get_kb_stats, get_kb_model, set_kb_model
from rag_standalone import verify_llm_connection
from text_splitter import STRATEGY_REGISTRY, GUARD_REGISTRY, get_all_strategies_info, SECONDARY_STRATEGIES
from utils import cfg_dir

PORT = 8765
HTML_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rag_settings.html")
TEMPLATES_DIR = os.path.join(os.path.dirname(cfg_dir), "config_templates")


# ==================== 配置模板管理 ====================

def list_templates():
    """列出所有已保存的配置模板"""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    templates = []
    for fname in sorted(os.listdir(TEMPLATES_DIR)):
        if fname.endswith(".json"):
            path = os.path.join(TEMPLATES_DIR, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                templates.append({
                    "name": fname[:-5],
                    "label": data.get("_label", fname[:-5]),
                    "size": os.path.getsize(path),
                    "mtime": os.path.getmtime(path),
                })
            except (json.JSONDecodeError, OSError):
                continue
    return templates


def save_template_config(name, label, config):
    """保存当前配置为模板"""
    os.makedirs(TEMPLATES_DIR, exist_ok=True)
    data = dict(config)
    data["_label"] = label
    data["_name"] = name
    path = os.path.join(TEMPLATES_DIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return path


def load_template_config(name):
    """加载模板配置"""
    path = os.path.join(TEMPLATES_DIR, f"{name}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 移除内部元字段
    data.pop("_label", None)
    data.pop("_name", None)
    return data


def delete_template_config(name):
    """删除模板"""
    path = os.path.join(TEMPLATES_DIR, f"{name}.json")
    if os.path.exists(path):
        os.remove(path)
        return True
    return False


def generate_html():
    """生成自包含 HTML 设置界面"""
    cfg = load_config()
    kbs = list_knowledge_bases()
    models = list_downloaded_models()
    template = load_template()
    guard_labels = {"mermaid": "🧜 Mermaid", "code": "💻 代码块", "math": "∑ LaTeX公式", "table": "📊 表格", "html": "🌐 HTML结构"}
    active_guards = cfg.get("splitting", {}).get("guards", ["code"])
    guard_card_html = ""
    for g in ["mermaid", "code", "math", "table", "html"]:
        active = g in active_guards
        border = "#667eea" if active else "#ddd"
        bg = "#f0f4ff" if active else "#fafafa"
        fg = "#667eea" if active else "#555"
        checked = "checked" if active else ""
        guard_card_html += f'<label style="display:flex;align-items:center;gap:6px;padding:8px 14px;border:2px solid {border};border-radius:10px;cursor:pointer;background:{bg};transition:all 0.2s;" onclick="toggleGuard(\'{g}\')">'
        guard_card_html += f'<input type="checkbox" {checked} style="accent-color:#667eea;">'
        guard_card_html += f'<span style="font-size:13px;font-weight:600;color:{fg};">{guard_labels[g]}</span></label>'
    guard_card_html += ""
    input_src = cfg.get("input_sources", {})
    split_cfg = cfg.get("splitting", {})
    overrides = split_cfg.get("strategy_overrides", {})

    # 策略配置表单（根据 config_schema 动态生成）
    def _render_field(name, schema, prefix="primary"):
        ftype = schema.get("type", "text")
        default = schema.get("default", "")
        label = schema.get("label", name)
        fid = f"{prefix}_{name}"
        if ftype == "int":
            mn = schema.get("min", "")
            mx = schema.get("max", "")
            return f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;"><span style="font-size:13px;font-weight:600;color:#555;white-space:nowrap;">{label}:</span><input id="{fid}" type="number" min="{mn}" max="{mx}" value="{default}" style="flex:1;max-width:120px;padding:6px 8px;border:1.5px solid #ddd;border-radius:6px;font-size:13px;" onchange="updateStrategyParam(\'{prefix}\',\'{name}\',this.value||null)"></div>'
        elif ftype == "select":
            opts = "".join(f'<option value="{o}"{" selected" if o==default else ""}>{o}</option>' for o in schema.get("options", []))
            return f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;"><span style="font-size:13px;font-weight:600;color:#555;white-space:nowrap;">{label}:</span><select id="{fid}" style="flex:1;max-width:160px;padding:6px 8px;border:1.5px solid #ddd;border-radius:6px;font-size:13px;" onchange="updateStrategyParam(\'{prefix}\',\'{name}\',this.value)">{opts}</select></div>'
        elif ftype == "multi-select":
            opts = "".join(
                f'<label style="display:inline-flex;align-items:center;gap:3px;margin:0 4px 0 0;font-size:13px;cursor:pointer;white-space:nowrap;">'
                f'<input type="checkbox" value="{o}" checked style="accent-color:#667eea;width:14px;height:14px;" '
                f'onchange="updateStrategyMulti(\'{prefix}\',\'{name}\',this)">{o}</label>'
                for o in schema.get("options", [])
            )
            return f'<div style="display:flex;align-items:center;gap:4px;flex-wrap:wrap;"><span style="font-size:13px;font-weight:600;color:#555;margin-right:4px;">{label}:</span>{opts}</div>'
        elif ftype == "bool":
            chk = 'checked' if default else ''
            return f'<label style="display:inline-flex;align-items:center;gap:4px;cursor:pointer;font-size:13px;margin-top:4px;"><input type="checkbox" id="{fid}" {chk} style="accent-color:#667eea;" onchange="updateStrategyParam(\'{prefix}\',\'{name}\',this.checked)">{label}</label>'
        elif ftype == "text":
            return f'<div class="form-group"><label>{label}</label><input id="{fid}" type="text" value="{default}" style="width:100%;padding:8px 10px;border:1.5px solid #ddd;border-radius:8px;font-size:13px;" onchange="updateStrategyParam(\'{prefix}\',\'{name}\',this.value)"></div>'
        return ""

    strategy_forms = {}
    for sname, splugin in STRATEGY_REGISTRY.items():
        fields = "".join(_render_field(k, v, f"strategy_{sname}") for k, v in splugin.config_schema.items())
        # headers 策略：标题级别和去除标题放在一行
        if sname == "headers":
            fields = (f'<div style="display:flex;gap:14px;align-items:flex-start;flex-wrap:wrap;">'
                      f'<div style="flex:1;min-width:200px;">{_render_field("headers_to_split_on", splugin.config_schema["headers_to_split_on"], "strategy_headers")}</div>'
                      f'<div style="padding-top:2px;">{_render_field("strip_headers", splugin.config_schema["strip_headers"], "strategy_headers")}</div>'
                      f'</div>')
        strategy_forms[sname] = f'<div id="form-strategy-{sname}" class="strategy-form" style="display:none;">{fields}</div>'
    strategy_forms_html = "".join(strategy_forms.values())

    # 后处理配置表单（复用主策略 schema + 默认 chunk_size 覆盖）
    secondary_forms_html = ""
    for sname in ["recursive", "fixed", "semantic"]:
        plugin = STRATEGY_REGISTRY.get(sname)
        if not plugin:
            continue
        if sname in ("fixed", "recursive"):
            fields = _render_field("chunk_size", {"type": "int", "label": "子切块大小", "default": 250, "min": 50, "max": 2000}, f"sec_{sname}")
            fields += _render_field("chunk_overlap", {"type": "int", "label": "子切重叠", "default": 25, "min": 0, "max": 500}, f"sec_{sname}")
        else:
            fields = _render_field("breakpoint_type", {"type": "select", "label": "断点算法", "options": ["percentile", "gradient", "stddev"], "default": "percentile"}, f"sec_{sname}")
        secondary_forms_html += f'<div id="form-secondary-{sname}" class="secondary-form" style="display:none;">{fields}</div>'

    # 原始 JSON 配置（极客模式）
    config_json_str = json.dumps(cfg, ensure_ascii=False, indent=2)
    STRATEGY_LABELS = {
        "fixed": "固定窗口", "recursive": "递归切分", "headers": "层级/标题切",
        "sentence": "按句切", "semantic": "语义切",
    }

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>RAG 系统设置面板</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; padding: 20px; color: #333; }}
.container {{ max-width: 1000px; margin: 0 auto; }}
.card {{ background: rgba(255,255,255,0.95); border-radius: 16px; padding: 28px; margin-bottom: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.15); backdrop-filter: blur(10px); }}
.card h2 {{ font-size: 18px; margin-bottom: 16px; color: #5a3e8a; border-bottom: 2px solid #e0d4f5; padding-bottom: 8px; }}
.form-group {{ margin-bottom: 14px; }}
.form-group label {{ display: block; font-size: 13px; font-weight: 600; color: #555; margin-bottom: 4px; }}
.form-group input, .form-group select, .form-group textarea {{ width: 100%; padding: 10px 12px; border: 1.5px solid #ddd; border-radius: 8px; font-size: 14px; transition: border 0.2s; }}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {{ border-color: #667eea; outline: none; box-shadow: 0 0 0 3px rgba(102,126,234,0.15); }}
.form-group textarea {{ min-height: 80px; font-family: 'Courier New', monospace; font-size: 13px; }}
.form-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }}
.form-row-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }}
.btn {{ padding: 10px 24px; border: none; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s; }}
.btn-secondary {{ background: #e8e8e8; color: #555; }}
.btn-secondary:hover {{ background: #ddd; }}
.btn-danger {{ background: #ff6b6b; color: white; }}
.btn-danger:hover {{ background: #ee5a5a; }}
.btn-success {{ background: #51cf66; color: white; }}
.btn-success:hover {{ background: #40c057; }}
.btn-ai {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
.btn-ai:hover {{ opacity: 0.9; transform: translateY(-1px); }}
.status {{ display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
.status-ok {{ background: #d3f9d8; color: #2b8a3e; }}
.status-warn {{ background: #fff3bf; color: #e67700; }}
.status-err {{ background: #ffe3e3; color: #c92a2a; }}
.grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
.stat-card {{ background: #f8f9fa; border-radius: 12px; padding: 16px; text-align: center; }}
.stat-card .num {{ font-size: 28px; font-weight: 700; color: #5a3e8a; }}
.stat-card .label {{ font-size: 12px; color: #888; margin-top: 4px; }}
.toast {{ position: fixed; bottom: 24px; right: 24px; padding: 14px 24px; border-radius: 10px; color: white; font-weight: 600; z-index: 999; animation: slideIn 0.3s ease; }}
@keyframes slideIn {{ from {{ transform: translateY(20px); opacity: 0; }} to {{ transform: translateY(0); opacity: 1; }} }}
.collapsible {{ background: #f0f4ff; border-radius: 10px; padding: 12px 16px; margin-top: 12px; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-size: 14px; font-weight: 600; color: #5a3e8a; user-select: none; }}
.collapsible:hover {{ background: #e0d4f5; }}
.collapsible-content {{ display: none; padding: 16px 0 0; }}
.override-row {{ display: grid; grid-template-columns: 1fr 80px 80px; gap: 10px; align-items: center; padding: 6px 0; border-bottom: 1px solid #eee; }}
.override-row:last-child {{ border: none; }}
.override-row span {{ font-size: 13px; font-weight: 600; color: #555; }}
.override-row input {{ width: 100%; padding: 6px 8px; border: 1.5px solid #ddd; border-radius: 6px; font-size: 13px; text-align: center; }}
.override-row input:focus {{ border-color: #667eea; outline: none; }}
.combo-warn {{ background: #fff3bf; border: 1px solid #fcc419; border-radius: 8px; padding: 8px 12px; font-size: 12px; color: #e67700; margin-top: 8px; display: none; }}
.toggle-switch {{ position: relative; display: inline-block; width: 40px; height: 22px; }}
.toggle-switch input {{ opacity: 0; width: 0; height: 0; }}
.toggle-slider {{ position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background: #ccc; transition: 0.3s; border-radius: 22px; }}
.toggle-slider:before {{ position: absolute; content: ""; height: 16px; width: 16px; left: 3px; bottom: 3px; background: white; transition: 0.3s; border-radius: 50%; }}
input:checked + .toggle-slider {{ background: #667eea; }}
input:checked + .toggle-slider:before {{ transform: translateX(18px); }}
</style>
</head>
<body>
<div class="container">
  <h1 style="color:white;margin-bottom:20px;font-weight:300;font-size:28px;">🛠️ RAG 系统设置面板</h1>

  <div class="card">
    <div class="grid-3">
      <div class="stat-card">
        <div class="num">{len(models)}</div>
        <div class="label">嵌入模型</div>
      </div>
      <div class="stat-card">
        <div class="num">{len(kbs)}</div>
        <div class="label">知识库</div>
      </div>
      <div class="stat-card">
        <div class="num">{sum(k.get('doc_count',0) for k in kbs.values())}</div>
        <div class="label">文档块</div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>📂 输入源</h2>
    <div class="form-row-3">
      <div class="form-group">
        <label>PDF 解析</label>
        <label class="toggle-switch" onclick="toggleInputSource('enable_pdf')">
          <input type="checkbox" {"checked" if input_src.get("enable_pdf", False) else ""}>
          <span class="toggle-slider"></span>
        </label>
        <div style="font-size:11px;color:#888;margin-top:4px;">需装 pypdf / pdfplumber</div>
      </div>
      <div class="form-group">
        <label>OCR 图片提取</label>
        <label class="toggle-switch" onclick="toggleInputSource('enable_ocr')">
          <input type="checkbox" {"checked" if input_src.get("enable_ocr", False) else ""}>
          <span class="toggle-slider"></span>
        </label>
        <div style="font-size:11px;color:#888;margin-top:4px;">需装 paddleocr</div>
      </div>
      <div class="form-group">
        <label>HTML→MD 转换</label>
        <label class="toggle-switch" onclick="toggleInputSource('enable_html2md')">
          <input type="checkbox" {"checked" if input_src.get("enable_html2md", False) else ""}>
          <span class="toggle-slider"></span>
        </label>
        <div style="font-size:11px;color:#888;margin-top:4px;">需装 html2text</div>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>📦 嵌入模型</h2>
    <div class="form-group">
      <label>当前模型</label>
      <select id="model-select" onchange="updateConfig('embedding','model_path',this.value)">
        {''.join(f'<option value="{m["path"]}" {"selected" if m["path"]==(cfg.get("embedding",{}).get("model_path","") or (models[0]["path"] if models else "")) else ""}>{m.get("model_id",m["path"].split(os.sep)[-1])}</option>' for m in models)}
        <option value="" {"selected" if not cfg.get("embedding",{}).get("model_path","") and not models else ""}>-- 无可用模型 --</option>
      </select>
      <div style="font-size:11px;color:#888;margin-top:4px;">未配置时自动使用列表中第一个可用模型。知识库未指定模型时回退到此默认值。</div>
    </div>
    <div class="form-row">
      <div class="form-group">
        <label>设备</label>
        <select id="device-select" onchange="updateConfig('embedding','device',this.value)">
          <option value="auto" {"selected" if cfg.get("embedding",{}).get("device","auto")=="auto" else ""}>自动检测</option>
          <option value="cuda" {"selected" if cfg.get("embedding",{}).get("device")=="cuda" else ""}>GPU (CUDA)</option>
          <option value="cpu" {"selected" if cfg.get("embedding",{}).get("device")=="cpu" else ""}>CPU</option>
        </select>
      </div>
      <div class="form-group">
        <label>推荐模型</label>
        <select onchange="if(this.value)window.open('https://huggingface.co/'+this.value)">
          <option value="">查看推荐模型</option>
          {''.join(f'<option value="{m["id"]}">{m["id"]} ({m["desc"]})</option>' for m in RECOMMENDED_MODELS)}
        </select>
      </div>
    </div>
  </div>

  <div class="card">
    <h2>🛡️ 守卫栈 <span style="font-weight:400;color:#888;font-size:12px;">— 预处理，保护特殊内容不被切碎（多选）</span></h2>
    <div style="display:flex;flex-wrap:wrap;gap:10px;">
      {guard_card_html}
    </div>
  </div>

  <div class="card">
    <h2>✂️ 文档切片</h2>
    <div class="form-row">
      <div class="form-group">
        <label>主策略</label>
        <select id="strategy-select" onchange="onStrategyChange(this.value)">
          <option value="recursive" {"selected" if split_cfg.get("strategy","recursive")=="recursive" else ""}>递归切分（推荐）</option>
          <option value="fixed" {"selected" if split_cfg.get("strategy")=="fixed" else ""}>固定窗口</option>
          <option value="headers" {"selected" if split_cfg.get("strategy")=="headers" else ""}>层级/标题切分</option>
          <option value="sentence" {"selected" if split_cfg.get("strategy")=="sentence" else ""}>按句切分</option>
          <option value="semantic" {"selected" if split_cfg.get("strategy")=="semantic" else ""}>语义切分</option>
        </select>
      </div>
      <div class="form-group">
        <label>后处理子切</label>
        <select id="secondary-select" onchange="onSecondaryChange(this.value)">
          <option value="">不处理</option>
          <option value="recursive" {"selected" if split_cfg.get("secondary_strategy")=="recursive" else ""}>递归子切</option>
          <option value="fixed" {"selected" if split_cfg.get("secondary_strategy")=="fixed" else ""}>固定窗口子切</option>
          <option value="semantic" {"selected" if split_cfg.get("secondary_strategy")=="semantic" else ""}>语义子切</option>
        </select>
      </div>
    </div>
    <div class="collapsible" onclick="toggleAdvanced()" id="adv-toggle">
      <span>⚙️ 切片参数（动态，依主策略+后处理组合）</span>
      <span id="adv-arrow">▶</span>
    </div>
    <div class="collapsible-content" id="adv-content">
      <div style="font-size:12px;color:#888;margin-bottom:8px;">当前策略配置</div>
      {strategy_forms_html}
      <div id="secondary-forms-container" style="margin-top:10px;padding-top:10px;border-top:1px dashed #ddd;display:none;">
        <div style="font-size:12px;color:#888;margin-bottom:8px;">后处理配置</div>
        {secondary_forms_html}
      </div>
      <div style="font-size:11px;color:#aaa;margin-top:8px;">
        💡 在对话中描述文档类型，系统将自动推荐切片配置。
      </div>
    </div>
  </div>

  <div class="card">
    <h2>🔍 检索参数</h2>
    <div class="form-row">
      <div class="form-group">
        <label>检索文档数 (K)</label>
        <input type="number" id="k-value" value="{cfg.get('retrieval',{}).get('k',3)}" min="1" max="20" onchange="updateConfig('retrieval','k',parseInt(this.value))">
      </div>
      <div class="form-group">
        <label>相似度阈值</label>
        <input type="number" id="threshold-value" value="{cfg.get('retrieval',{}).get('score_threshold') or ''}" min="0" max="1" step="0.05" placeholder="不启用" onchange="updateConfig('retrieval','score_threshold',this.value?parseFloat(this.value):null)">
      </div>
    </div>
  </div>

  <div class="card">
    <h2>🤖 LLM 模式</h2>
    <div class="form-group" style="margin-bottom:16px;">
      <label>运行模式 <span style="font-weight:400;color:#888;font-size:12px;">— 决定系统行为路径</span></label>
      <div style="display:flex;gap:12px;margin-top:8px;">
        <label style="flex:1;padding:14px 16px;border:2px solid {'#667eea' if cfg.get('mode','integrated')=='integrated' else '#ddd'};border-radius:12px;cursor:pointer;background:{'#f0f4ff' if cfg.get('mode','integrated')=='integrated' else '#fafafa'};transition:all 0.2s;" onclick="setMode('integrated')">
          <input type="radio" name="mode" value="integrated" {'checked' if cfg.get('mode','integrated')=='integrated' else ''} style="display:none;">
          <div style="font-size:16px;font-weight:600;color:{'#667eea' if cfg.get('mode','integrated')=='integrated' else '#555'};">🔌 集成模式</div>
          <div style="font-size:12px;color:#888;margin-top:4px;">无 LLM，纯检索。智能体根据检索到的 context 自行回答。</div>
          <div style="font-size:11px;color:#aaa;margin-top:2px;">无需配置 LLM，不产生额外推理成本</div>
        </label>
        <label style="flex:1;padding:14px 16px;border:2px solid {'#667eea' if cfg.get('mode','standalone')=='standalone' else '#ddd'};border-radius:12px;cursor:pointer;background:{'#f0f4ff' if cfg.get('mode','standalone')=='standalone' else '#fafafa'};transition:all 0.2s;" onclick="setMode('standalone')">
          <input type="radio" name="mode" value="standalone" {'checked' if cfg.get('mode','standalone')=='standalone' else ''} style="display:none;">
          <div style="font-size:16px;font-weight:600;color:{'#667eea' if cfg.get('mode','standalone')=='standalone' else '#555'};">🤖 独立模式</div>
          <div style="font-size:12px;color:#888;margin-top:4px;">检索 + LLM 全链路。系统自行完成检索→生成回答。</div>
          <div style="font-size:11px;color:#aaa;margin-top:2px;">需要配置下方 LLM 连接</div>
        </label>
      </div>
    </div>
    <div id="llm-settings" style="{'display:none' if cfg.get('mode','integrated')=='integrated' else 'block'};">
      <div class="form-group">
        <label>API 地址</label>
        <input type="text" id="llm-url" value="{cfg.get('llm',{}).get('base_url','http://localhost:1234/v1')}" onchange="updateConfig('llm','base_url',this.value)">
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Temperature</label>
          <input type="number" id="llm-temp" value="{cfg.get('llm',{}).get('temperature',0.1)}" min="0" max="2" step="0.05" onchange="updateConfig('llm','temperature',parseFloat(this.value))">
        </div>
        <div class="form-group">
          <label>Max Tokens</label>
          <input type="number" id="llm-tokens" value="{cfg.get('llm',{}).get('max_tokens',512)}" min="64" max="4096" step="64" onchange="updateConfig('llm','max_tokens',parseInt(this.value))">
        </div>
      </div>
      <button class="btn btn-secondary" onclick="verifyLLM()" style="margin-top:8px;">🔗 验证连接</button>
      <span id="llm-status"></span>
    </div>
  </div>

  <div class="card">
    <h2>📝 Prompt 模板</h2>
    <div class="form-group">
      <textarea id="prompt-template" rows="8" onchange="savePrompt(this.value)">{template}</textarea>
    </div>
    <button class="btn btn-secondary" onclick="resetPrompt()">↺ 重置为默认</button>
    <span id="prompt-status" style="margin-left:12px;font-size:13px;color:#888;"></span>
  </div>

  <div class="card">
    <h2>📚 知识库 & 分类规则</h2>
    <div id="kb-list" style="margin-bottom:8px;">
      {' '.join(f'''<div style="display:flex;justify-content:space-between;align-items:center;padding:8px;border-bottom:1px solid #eee;">
        <div style="flex:1;"><strong>{name}</strong> - {info.get("description","")} [{info.get("doc_count",0)} 文档]</div>
        <div style="min-width:200px;">
          <select class="kb-model-select" data-kb="{name}" style="width:100%;padding:6px 8px;border:1.5px solid #ddd;border-radius:6px;font-size:12px;" onchange="setKbModel('{name}',this.value)">
            <option value="">— 默认模型 ({models[0].get("model_id","") if models else "无"}) —</option>
            {''.join(f'<option value="{m.get("path","")}" {'selected' if info.get("embedding_model","")==m.get("path","") else ""}>{m.get("model_id","")}</option>' for m in models)}
          </select>
        </div>
      </div>''' for name, info in kbs.items())}
    </div>
    <div style="margin-top:12px;padding-top:12px;border-top:1px solid #eee;">
      <div style="font-size:13px;font-weight:600;color:#555;margin-bottom:6px;">📋 自动分类规则 <span style="font-weight:400;color:#888;font-size:11px;">（关键词 + 扩展名匹配）</span></div>
      <div id="rules-list" style="font-size:13px;color:#888;">加载中...</div>
      <div style="display:flex;gap:8px;margin-top:8px;flex-wrap:wrap;">
        <button class="btn btn-secondary" style="padding:6px 14px;font-size:12px;" onclick="refreshRules()">🔄 刷新规则</button>
        <button class="btn btn-primary" style="padding:6px 14px;font-size:12px;" onclick="showRuleEditor()">➕ 添加规则</button>
        <button class="btn btn-danger" style="padding:6px 14px;font-size:12px;" onclick="if(confirm('重置所有分类规则为默认？'))resetRules()">↺ 重置默认</button>
      </div>
    </div>
  </div>

  <!-- 规则编辑弹窗 -->
  <div id="rule-editor-overlay" style="display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.4);z-index:1000;align-items:center;justify-content:center;" onclick="if(event.target===this)hideRuleEditor()">
    <div style="background:white;border-radius:16px;padding:28px;max-width:480px;width:90%;box-shadow:0 8px 32px rgba(0,0,0,0.2);">
      <h3 id="rule-editor-title" style="font-size:18px;color:#5a3e8a;margin-bottom:16px;">添加分类规则</h3>
      <div class="form-group"><label>知识库名</label><input id="rule-name" type="text" style="width:100%;padding:8px 10px;border:1.5px solid #ddd;border-radius:8px;font-size:14px;"></div>
      <div class="form-group"><label>关键词（逗号分隔）</label><input id="rule-keywords" type="text" style="width:100%;padding:8px 10px;border:1.5px solid #ddd;border-radius:8px;font-size:14px;" placeholder="例: 代码,API,编程"></div>
      <div class="form-group"><label>扩展名（逗号分隔）</label><input id="rule-extensions" type="text" style="width:100%;padding:8px 10px;border:1.5px solid #ddd;border-radius:8px;font-size:14px;" placeholder="例: .py,.js,.ts"></div>
      <div class="form-group"><label>描述</label><input id="rule-desc" type="text" style="width:100%;padding:8px 10px;border:1.5px solid #ddd;border-radius:8px;font-size:14px;" placeholder="可选"></div>
      <div class="form-group"><label>知识库嵌入模型</label>
        <select id="rule-model" style="width:100%;padding:8px 10px;border:1.5px solid #ddd;border-radius:8px;font-size:14px;">
          <option value="">— 默认模型 ({models[0].get("model_id","") if models else "无"}) —</option>
          {''.join(f'<option value="{m.get("path","")}">{m.get("model_id","")}</option>' for m in models)}
        </select>
        <div style="font-size:11px;color:#888;margin-top:4px;">选空=回退到全局默认模型。已有文档的知识库切换模型后需重新导入。</div>
      </div>
      <div style="display:flex;gap:10px;margin-top:16px;justify-content:flex-end;">
        <button class="btn btn-secondary" onclick="hideRuleEditor()">取消</button>
        <button class="btn btn-primary" onclick="saveRule()">💾 保存</button>
      </div>
    </div>
  </div>

  <!-- 极客模式：JSON 配置编辑器 + 模板管理 -->
  <div class="card" style="margin-bottom: 12px;">
    <h2>⚡ 极客模式 <span style="font-weight:400;color:#888;font-size:12px;">— 编辑 & 保存复用模板</span></h2>
    <div class="form-group">
      <textarea id="geek-editor" rows="10" style="width:100%;padding:10px;border:1.5px solid #ddd;border-radius:8px;font-family:'Courier New',monospace;font-size:12px;">{config_json_str}</textarea>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:8px;">
      <button class="btn btn-danger" onclick="applyGeekConfig()" style="margin-right:4px;">💾 应用</button>
      <button class="btn btn-secondary" onclick="saveGeekTemplate()" style="margin-right:4px;">📋 另存为模板</button>
      <button class="btn btn-success" onclick="refreshGeekTemplates()" style="margin-right:4px;">🔄 刷新模板列表</button>
      <button class="btn btn-danger" onclick="if(confirm('确定重置所有配置为默认？'))resetAll()">↺ 重置默认</button>
    </div>
    <span id="geek-status" style="font-size:13px;color:#888;margin-left:8px;"></span>

    <div id="template-list" style="margin-top:10px;padding-top:10px;border-top:1px solid #eee;">
      <div style="font-size:13px;font-weight:600;color:#555;margin-bottom:6px;">已保存模板</div>
      <div id="template-items" style="font-size:13px;color:#888;">加载中...</div>
    </div>
  </div>

  <div class="card" style="display:flex;gap:12px;flex-wrap:wrap;">
    <button class="btn btn-danger" onclick="if(confirm('\u786e\u5b9a\u91cd\u7f6e\u6240\u6709\u914d\u7f6e\uff1f'))resetAll()">&#x1f5d1;&#xfe0f; \u91cd\u7f6e\u914d\u7f6e</button>
    <button class="btn btn-success" onclick="window.location.reload()">&#x1f504; \u5237\u65b0</button>
  </div>
</div>

<script>
function toast(msg, type) {{ type = type || 'success'; const t = document.createElement('div'); t.className = 'toast'; t.style.background = type==='success' ? '#51cf66' : type==='error' ? '#ff6b6b' : '#fcc419'; t.textContent = msg; document.body.appendChild(t); setTimeout(function(){{t.remove()}}, 2500); }}

function setMode(mode) {{
  fetch('/api/mode', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{mode}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ toast('已切换'); setTimeout(function(){{location.reload()}}, 300); }}
    else {{ toast(d.error, 'error'); }}
  }}).catch(function(e){{toast('请求失败', 'error')}});
}}

function updateConfig(section, key, value) {{
  fetch('/api/config', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{section: section, key: key, value: value}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) toast('已更新');
    else toast(d.error, 'error');
  }}).catch(function(e){{toast('请求失败', 'error')}});
}}

function setKbModel(kbName, modelId) {{
  fetch('/api/kb-model', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{kb_name: kbName, model_id: modelId}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) toast('知识库模型已更新: ' + d.message);
    else toast(d.error, 'error');
  }}).catch(function(e){{toast('请求失败', 'error')}});
}}

function updateOverride(strategy, key, value) {{
  fetch('/api/override', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{strategy: strategy, key: key, value: value}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) toast('已更新');
    else toast(d.error, 'error');
  }}).catch(function(e){{toast('请求失败', 'error')}});
}}

function toggleInputSource(key) {{
  fetch('/api/input-source', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{key: key}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ toast('已更新'); setTimeout(function(){{location.reload()}}, 200); }}
    else toast('操作失败', 'error');
  }}).catch(function(e){{toast('请求失败', 'error')}});
}}

function onStrategyChange(strategy) {{
  updateConfig('splitting','strategy',strategy);
  updateAdvView();
}}

function onSecondaryChange(val) {{
  fetch('/api/config', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{section: 'splitting', key: 'secondary_strategy', value: val || null}})
  }});
  updateAdvView();
}}

function toggleAdvanced() {{
  var content = document.getElementById('adv-content');
  var arrow = document.getElementById('adv-arrow');
  var on = content.style.display === 'block';
  content.style.display = on ? 'none' : 'block';
  arrow.textContent = on ? '\u25b6' : '\u25bc';
}}

function savePrompt(content) {{
  fetch('/api/prompt', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{content: content}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ document.getElementById('prompt-status').textContent = '\u2713 \u5df2\u4fdd\u5b58'; toast('\u6a21\u677f\u5df2\u4fdd\u5b58'); }}
    else toast('\u4fdd\u5b58\u5931\u8d25', 'error');
  }}).catch(function(e){{toast('\u8bf7\u6c42\u5931\u8d25', 'error')}});
}}

function resetPrompt() {{
  fetch('/api/prompt/reset', {{method:'POST'}})
  .then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ document.getElementById('prompt-template').value = d.template; toast('\u5df2\u91cd\u7f6e'); }}
  }});
}}

function verifyLLM() {{
  fetch('/api/verify-llm').then(function(r){{return r.json()}}).then(function(d){{
    var el = document.getElementById('llm-status');
    el.innerHTML = d.success ? '<span class="status status-ok">\u2713 \u8fde\u63a5\u6b63\u5e38</span>' : '<span class="status status-err">\u2717 '+d.message+'</span>';
  }});
}}

function toggleGuard(name) {{
  fetch('/api/guard/toggle', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{name: name}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ toast('\u5df2\u66f4\u65b0'); setTimeout(function(){{location.reload()}}, 200); }}
    else toast('\u64cd\u4f5c\u5931\u8d25', 'error');
  }}).catch(function(e){{toast('\u8bf7\u6c42\u5931\u8d25', 'error')}});
}}

function updateStrategyParam(strategy, key, value) {{
  // int 字段转数字
  if (value === '' || value === null) value = null;
  else if (!isNaN(value) && value !== true && value !== false) value = parseInt(value);
  fetch('/api/override', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{strategy: strategy, key: key, value: value}})
  }});
}}

function updateStrategyMulti(strategy, key, cb) {{
  // strategy 参数可能是 "strategy_headers"，去掉前缀
  var clean = strategy.replace(/^strategy_/, '');
  var checks = document.querySelectorAll('#form-strategy-' + clean + ' input[type=checkbox][value]');
  var values = [];
  checks.forEach(function(c) {{ if(c.checked) values.push(c.value); }});
  fetch('/api/override', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{strategy: clean, key: key, value: values}})
  }});
}}

function applyGeekConfig() {{
  var raw = document.getElementById('geek-editor').value;
  try {{ JSON.parse(raw); }} catch(e) {{ toast('JSON 格式错误: '+e.message, 'error'); return; }}
  fetch('/api/config/raw', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: raw
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ document.getElementById('geek-status').textContent = '\u2713 \u5df2\u5e94\u7528'; toast('\u914d\u7f6e\u5df2\u66f4\u65b0'); }}
    else {{ toast(d.error, 'error'); }}
  }}).catch(function(e){{toast('\u8bf7\u6c42\u5931\u8d25', 'error')}});
}}

function saveGeekTemplate() {{
  var name = prompt('\u8f93\u5165\u6a21\u677f\u540d\u79f0\uff08\u4f8b\u5982\uff1a\u201c\u6211\u7684\u6280\u672f\u6587\u6863\u914d\u7f6e\u201d\uff09:');
  if(!name) return;
  var label = prompt('\u8f93\u5165\u6a21\u677f\u63cf\u8ff0\uff08\u53ef\u7a7a\uff09:') || name;
  var raw = document.getElementById('geek-editor').value;
  fetch('/api/template/save', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{name: name, label: label, config: JSON.parse(raw)}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ toast('\u6a21\u677f\u5df2\u4fdd\u5b58\uff1a'+name); refreshGeekTemplates(); }}
    else toast(d.error, 'error');
  }}).catch(function(e){{toast('\u8bf7\u6c42\u5931\u8d25', 'error')}});
}}

function loadGeekTemplate(name) {{
  if(!confirm('\u786e\u5b9a\u52a0\u8f7d\u6a21\u677f "'+name+'" \u5e76\u8986\u76d6\u5f53\u524d\u914d\u7f6e\uff1f')) return;
  fetch('/api/template/load', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{name: name}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ toast('\u5df2\u52a0\u8f7d\u6a21\u677f\uff1a'+name); setTimeout(function(){{location.reload()}}, 300); }}
    else toast(d.error, 'error');
  }}).catch(function(e){{toast('\u8bf7\u6c42\u5931\u8d25', 'error')}});
}}

function deleteGeekTemplate(name) {{
  if(!confirm('\u786e\u5b9a\u5220\u9664\u6a21\u677f "'+name+'"\uff1f')) return;
  fetch('/api/template/delete', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{name: name}})
  }}).then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ toast('\u5df2\u5220\u9664'); refreshGeekTemplates(); }}
    else toast(d.error, 'error');
  }}).catch(function(e){{toast('\u8bf7\u6c42\u5931\u8d25', 'error')}});
}}

function refreshGeekTemplates() {{
  fetch('/api/template/list', {{method:'POST'}}).then(function(r){{return r.json()}}).then(function(d){{
    var el = document.getElementById('template-items');
    if(!d.templates || d.templates.length === 0) {{
      el.innerHTML = '\u6682\u65e0\u4fdd\u5b58\u7684\u6a21\u677f\u3002\u8c03\u597d\u53c2\u6570\u540e\u70b9\u201c\u53e6\u5b58\u4e3a\u6a21\u677f\u201d\u4fdd\u5b58\u3002';
      return;
    }}
    el.innerHTML = d.templates.map(function(t) {{
      return '<div style=\"display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid #eee;\">' +
        '<span><strong>' + t.label + '</strong> <span style=\"color:#aaa;font-size:11px;\">(' + t.name + ')</span></span>' +
        '<span>' +
        '<button class=\"btn btn-secondary\" style=\"padding:4px 12px;font-size:12px;margin-right:4px;\" onclick=\"loadGeekTemplate(\\'' + t.name + '\\')\">\u52a0\u8f7d</button>' +
        '<button class=\"btn btn-danger\" style=\"padding:4px 12px;font-size:12px;\" onclick=\"deleteGeekTemplate(\\'' + t.name + '\\')\">\u5220\u9664</button>' +
        '</span></div>';
    }}).join('');
  }});
}}

function refreshRules() {{
  Promise.all([
    fetch('/api/rules/list', {{method:'POST'}}).then(function(r){{return r.json()}}),
    fetch('/api/kb-models', {{method:'POST'}}).then(function(r){{return r.json()}})
  ]).then(function(results) {{
    var d = results[0], kbData = results[1];
    var el = document.getElementById('rules-list');
    var rules = d.rules || {{}};
    var kbModels = (kbData && kbData.kb_models) || {{}};
    var names = Object.keys(rules);
    if (names.length === 0) {{
      el.innerHTML = '\u6682\u65e0\u81ea\u5b9a\u4e49\u89c4\u5219\uff0c\u70b9\u201c\u91cd\u7f6e\u9ed8\u8ba4\u201d\u521b\u5efa\u9ed8\u8ba4\u89c4\u5219\u3002';
      return;
    }}
    el.innerHTML = names.map(function(name) {{
      var r = rules[name];
      var kws = (r.keywords || []).join(', ');
      var exts = (r.extensions || []).join(', ');
      var modelLabel = '\u9ed8\u8ba4\u6a21\u578b';
      if (kbModels[name]) {{
        var parts = kbModels[name].split('/');
        modelLabel = parts[parts.length-1] || kbModels[name];
      }}
      var modelHtml = '<br><span style=\"font-size:11px;color:#667eea;\">\u25b6 \u6a21\u578b: ' + modelLabel + '</span>';
      return '<div style=\"display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid #eee;\">' +
        '<div style=\"flex:1;\"><strong>' + name + '</strong> ' +
        (r.description ? '<span style=\"color:#888;font-size:11px;\">(' + r.description + ')</span>' : '') +
        '<br><span style=\"font-size:11px;color:#aaa;\">\u5173\u952e\u8bcd: ' + (kws || '\u2014') + ' | \u6269\u5c55\u540d: ' + (exts || '\u2014') + '</span>' +
        modelHtml + '</div>' +
        '<span>' +
        '<button class=\"btn btn-secondary\" style=\"padding:3px 10px;font-size:11px;margin-right:4px;\" onclick=\"editRule(\\'' + name + '\\')\">\u7f16\u8f91</button>' +
        '<button class=\"btn btn-danger\" style=\"padding:3px 10px;font-size:11px;\" onclick=\"deleteRule(\\'' + name + '\\')\">\u5220\u9664</button>' +
        '</span></div>';
    }}).join('');
  }});
}}

function showRuleEditor(editName) {{
  document.getElementById('rule-editor-overlay').style.display = 'flex';
  document.getElementById('rule-editor-title').textContent = editName ? '\u7f16\u8f91\u89c4\u5219' : '\u6dfb\u52a0\u89c4\u5219';
}}

function hideRuleEditor() {{
  document.getElementById('rule-editor-overlay').style.display = 'none';
  document.getElementById('rule-name').value = '';
  document.getElementById('rule-name').readOnly = false;
  document.getElementById('rule-keywords').value = '';
  document.getElementById('rule-extensions').value = '';
  document.getElementById('rule-desc').value = '';
  document.getElementById('rule-model').value = '';
}}

function editRule(name) {{
  Promise.all([
    fetch('/api/rules/list', {{method:'POST'}}).then(function(r){{return r.json()}}),
    fetch('/api/kb-models', {{method:'POST'}}).then(function(r){{return r.json()}})
  ]).then(function(results) {{
    var d = results[0], kbData = results[1];
    var r = (d.rules || {{}})[name];
    if (!r) {{ toast('\u89c4\u5219\u4e0d\u5b58\u5728', 'error'); return; }}
    document.getElementById('rule-name').value = name;
    document.getElementById('rule-name').readOnly = true;
    document.getElementById('rule-keywords').value = (r.keywords || []).join(', ');
    document.getElementById('rule-extensions').value = (r.extensions || []).join(', ');
    document.getElementById('rule-desc').value = r.description || '';
    document.getElementById('rule-editor-title').textContent = '\u7f16\u8f91\u89c4\u5219: ' + name;
    // 设置模型下拉
    var kbModels = (kbData && kbData.kb_models) || {{}};
    var sel = document.getElementById('rule-model');
    if (kbModels[name]) {{
      sel.value = kbModels[name];
    }} else {{
      sel.value = '';
    }}
    document.getElementById('rule-editor-overlay').style.display = 'flex';
  }});
}}

function saveRule() {{
  var name = document.getElementById('rule-name').value.trim();
  if (!name) {{ toast('\u8bf7\u8f93\u5165\u77e5\u8bc6\u5e93\u540d', 'error'); return; }}
  var kws = document.getElementById('rule-keywords').value.split(',').map(function(s){{return s.trim()}}).filter(function(s){{return s}});
  var exts = document.getElementById('rule-extensions').value.split(',').map(function(s){{return s.trim()}}).filter(function(s){{return s}});
  var desc = document.getElementById('rule-desc').value.trim();
  var modelId = document.getElementById('rule-model').value;
  // 先保存规则，再设置 KB 模型
  fetch('/api/rules/save', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{name: name, keywords: kws, extensions: exts, description: desc}})
  }}).then(function(r){{return r.json()}}).then(function(d) {{
    if (!d.success) {{ toast(d.error, 'error'); return; }}
    // 设置 KB 模型
    fetch('/api/kb-model', {{
      method: 'POST', headers: {{'Content-Type':'application/json'}},
      body: JSON.stringify({{kb_name: name, model_id: modelId}})
    }}).then(function(r){{return r.json()}}).then(function(d2) {{
      toast(d2.success ? '\u89c4\u5219\u5df2\u4fdd\u5b58\uff0c\u6a21\u578b\u5df2\u66f4\u65b0' : '\u89c4\u5219\u5df2\u4fdd\u5b58\uff0c\u6a21\u578b\u8bbe\u7f6e\u5931\u8d25');
      hideRuleEditor();
      refreshRules();
    }});
  }});
}}

function deleteRule(name) {{
  if (!confirm('\u786e\u5b9a\u5220\u9664\u89c4\u5219 "' + name + '"\uff1f')) return;
  fetch('/api/rules/delete', {{
    method: 'POST', headers: {{'Content-Type':'application/json'}},
    body: JSON.stringify({{name: name}})
  }}).then(function(r){{return r.json()}}).then(function(d) {{
    if (d.success) {{ toast('\u5df2\u5220\u9664'); refreshRules(); }}
    else toast(d.error, 'error');
  }});
}}

function resetRules() {{
  fetch('/api/rules/reset', {{method:'POST'}})
  .then(function(r){{return r.json()}}).then(function(d) {{
    if (d.success) {{ toast('\u89c4\u5219\u5df2\u91cd\u7f6e'); refreshRules(); }}
    else toast(d.error, 'error');
  }});
}}

function updateAdvView() {{
  var s = document.getElementById('strategy-select').value;
  var d2 = document.getElementById('secondary-select').value;
  // 隐藏所有策略和后处理表单
  document.querySelectorAll('.strategy-form').forEach(function(f) {{ f.style.display = 'none'; }});
  document.querySelectorAll('.secondary-form').forEach(function(f) {{ f.style.display = 'none'; }});
  // 显示当前策略表单
  var cur = document.getElementById('form-strategy-' + s);
  if (cur) cur.style.display = 'block';
  // 显示后处理表单
  var secContainer = document.getElementById('secondary-forms-container');
  if (d2) {{
    secContainer.style.display = 'block';
    var secForm = document.getElementById('form-secondary-' + d2);
    if (secForm) secForm.style.display = 'block';
  }} else {{
    secContainer.style.display = 'none';
  }}
}}

function resetAll() {{
  fetch('/api/reset', {{method:'POST'}})
  .then(function(r){{return r.json()}}).then(function(d){{
    if(d.success) {{ toast('已重置'); setTimeout(function(){{location.reload()}}, 500); }}
  }});
}}

window.onload = function() {{ updateAdvView(); refreshGeekTemplates(); refreshRules(); }};
</script>
</body>
</html>"""


class RAGHandler(http.server.BaseHTTPRequestHandler):
    """HTTP 请求处理器"""

    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(generate_html().encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            if path == "/api/config":
                data = self._read_body()
                section = data.get("section")
                key = data.get("key")
                value = data.get("value")
                cfg = load_config()
                if section not in cfg:
                    cfg[section] = {}
                cfg[section][key] = value
                save_config(cfg)
                self._send_json({"success": True})

            elif path == "/api/mode":
                data = self._read_body()
                mode = data.get("mode")
                if mode not in ("integrated", "standalone"):
                    self._send_json({"success": False, "error": "无效模式，可选: integrated, standalone"})
                    return
                cfg = load_config()
                cfg["mode"] = mode
                save_config(cfg)
                self._send_json({"success": True, "mode": mode})

            elif path == "/api/override":
                data = self._read_body()
                strategy = data.get("strategy")
                key = data.get("key")
                value = data.get("value")
                cfg = load_config()
                if "splitting" not in cfg:
                    cfg["splitting"] = {}
                if "strategy_overrides" not in cfg["splitting"]:
                    cfg["splitting"]["strategy_overrides"] = {}
                if strategy not in cfg["splitting"]["strategy_overrides"]:
                    cfg["splitting"]["strategy_overrides"][strategy] = {}
                cfg["splitting"]["strategy_overrides"][strategy][key] = value
                save_config(cfg)
                self._send_json({"success": True})

            elif path == "/api/input-source":
                data = self._read_body()
                key = data.get("key", "")
                if key not in ("enable_pdf", "enable_ocr", "enable_html2md"):
                    self._send_json({"success": False, "error": f"未知输入源: {key}"})
                    return
                cfg = load_config()
                if "input_sources" not in cfg:
                    cfg["input_sources"] = {}
                cfg["input_sources"][key] = not cfg["input_sources"].get(key, False)
                save_config(cfg)
                self._send_json({"success": True, "active": cfg["input_sources"][key]})

            elif path == "/api/prompt":
                data = self._read_body()
                content = data.get("content", "")
                save_template(content)
                self._send_json({"success": True})

            elif path == "/api/prompt/reset":
                tpl = reset_template()
                self._send_json({"success": True, "template": tpl})

            elif path == "/api/verify-llm":
                ok, msg = verify_llm_connection()
                self._send_json({"success": ok, "message": msg})

            elif path == "/api/guard/toggle":
                data = self._read_body()
                name = data.get("name", "")
                if name not in ("mermaid", "code", "math", "table", "html"):
                    self._send_json({"success": False, "error": f"未知守卫: {name}"})
                    return
                cfg = load_config()
                guards = cfg.get("splitting", {}).get("guards", ["code"])
                if name in guards:
                    guards = [g for g in guards if g != name]
                    active = False
                else:
                    guards = list(guards) + [name]
                    active = True
                if "splitting" not in cfg:
                    cfg["splitting"] = {}
                cfg["splitting"]["guards"] = guards
                save_config(cfg)
                self._send_json({"success": True, "active": active})

            elif path == "/api/mode-check":
                cfg = load_config()
                self._send_json({"mode": cfg.get("mode", "integrated")})

            elif path == "/api/config/raw":
                length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(length)
                try:
                    new_cfg = json.loads(body)
                except json.JSONDecodeError:
                    self._send_json({"success": False, "error": "JSON 格式错误"})
                    return
                if save_config(new_cfg):
                    self._send_json({"success": True})
                else:
                    self._send_json({"success": False, "error": "写入失败"})

            elif path == "/api/template/list":
                self._send_json({"success": True, "templates": list_templates()})

            elif path == "/api/template/save":
                data = self._read_body()
                name = data.get("name", "").strip()
                if not name:
                    self._send_json({"success": False, "error": "模板名不能为空"})
                    return
                label = data.get("label", name)
                config = data.get("config", {})
                save_template_config(name, label, config)
                self._send_json({"success": True})

            elif path == "/api/template/load":
                data = self._read_body()
                name = data.get("name", "")
                tpl = load_template_config(name)
                if tpl is None:
                    self._send_json({"success": False, "error": "模板不存在"})
                    return
                # 合并到当前配置
                cfg = load_config()
                for k, v in tpl.items():
                    if isinstance(v, dict) and k in cfg and isinstance(cfg[k], dict):
                        cfg[k].update(v)
                    else:
                        cfg[k] = v
                save_config(cfg)
                self._send_json({"success": True})

            elif path == "/api/template/delete":
                data = self._read_body()
                name = data.get("name", "")
                ok = delete_template_config(name)
                self._send_json({"success": ok})

            # 知识库分类规则 API
            elif path == "/api/rules/list":
                from knowledge_base_manager import _load_rules
                self._send_json({"success": True, "rules": _load_rules()})

            elif path == "/api/rules/delete":
                data = self._read_body()
                name = data.get("name", "")
                from knowledge_base_manager import remove_classify_rule
                ok, msg = remove_classify_rule(name)
                self._send_json({"success": ok, "message": msg})

            elif path == "/api/rules/save":
                data = self._read_body()
                name = data.get("name", "").strip()
                if not name:
                    self._send_json({"success": False, "error": "知识库名不能为空"})
                    return
                from knowledge_base_manager import set_classify_rule
                ok, msg = set_classify_rule(
                    name,
                    keywords=data.get("keywords", []),
                    extensions=data.get("extensions", []),
                    description=data.get("description", ""),
                )
                self._send_json({"success": ok, "message": msg})

            elif path == "/api/rules/reset":
                from knowledge_base_manager import reset_classify_rules
                ok, msg = reset_classify_rules()
                self._send_json({"success": ok, "message": msg})

            elif path == "/api/kb-model":
                data = self._read_body()
                kb_name = data.get("kb_name", "")
                model_id = data.get("model_id", "")
                if not kb_name:
                    self._send_json({"success": False, "error": "知识库名不能为空"})
                    return
                from knowledge_base_manager import set_kb_model
                ok, msg = set_kb_model(kb_name, model_id)
                self._send_json({"success": ok, "message": msg})

            elif path == "/api/kb-models":
                """返回所有知识库的模型配置 + 已下载模型列表"""
                from knowledge_base_manager import list_knowledge_bases, get_kb_model
                from embedding_model_manager import list_downloaded_models
                kbs = list_knowledge_bases()
                kb_models = {name: get_kb_model(name) for name in kbs}
                models = list_downloaded_models()
                self._send_json({"success": True, "kb_models": kb_models, "models": models})

            elif path == "/api/recommend":
                data = self._read_body()
                cfg = load_config()
                if "description" in data:
                    # LLM 模式：构造 prompt 调用外部 LLM
                    desc = data["description"]
                    try:
                        from langchain_community.llms import OpenAI
                        llm = OpenAI(
                            base_url=cfg.get("llm", {}).get("base_url", "http://localhost:1234/v1"),
                            api_key="not-needed",
                            temperature=0.1,
                            max_tokens=256,
                        )
                        prompt = f"""根据以下用户描述，推荐 RAG 切片配置。

用户描述：{desc}

可选策略：fixed(固定窗口), recursive(递归切分), headers(层级/标题切), sentence(按句切), semantic(语义切)
可选守卫：mermaid, code, math, table, html
可选后处理：recursive(递归子切), fixed(固定窗口子切), semantic(语义子切)

请返回 JSON 格式推荐，包含 strategy, guards(数组), secondary(或null), chunk_size(或null)：
"""
                        raw = llm.invoke(prompt).strip()
                        # 提取 JSON
                        import re as _re
                        json_match = _re.search(r'\{.*\}', raw, _re.DOTALL)
                        if json_match:
                            rec = json.loads(json_match.group(0))
                        else:
                            rec = {"strategy": "recursive", "guards": ["code"], "secondary": None, "chunk_size": 500}
                    except Exception:
                        rec = {"strategy": "recursive", "guards": ["code"], "secondary": None, "chunk_size": 500}

                    if "splitting" not in cfg:
                        cfg["splitting"] = {}
                    cfg["splitting"]["strategy"] = rec.get("strategy", "recursive")
                    cfg["splitting"]["guards"] = rec.get("guards", ["code"])
                    cfg["splitting"]["secondary_strategy"] = rec.get("secondary")
                    if rec.get("chunk_size"):
                        cfg["splitting"]["chunk_size"] = rec["chunk_size"]
                    save_config(cfg)
                    self._send_json({"success": True})

                elif "preset" in data:
                    # 预设模式
                    p = data["preset"]
                    if "splitting" not in cfg:
                        cfg["splitting"] = {}
                    cfg["splitting"]["strategy"] = p.get("strategy", "recursive")
                    cfg["splitting"]["guards"] = p.get("guards", ["code"])
                    cfg["splitting"]["secondary_strategy"] = p.get("secondary")
                    if p.get("cs"):
                        cfg["splitting"]["chunk_size"] = p["cs"]
                    save_config(cfg)
                    self._send_json({"success": True})
                else:
                    self._send_json({"success": False, "error": "缺少 description 或 preset 参数"})

            elif path == "/api/reset":
                reset_config()
                reset_template()
                self._send_json({"success": True})

            else:
                self._send_json({"error": "unknown endpoint"}, 404)

        except Exception as e:
            self._send_json({"success": False, "error": str(e)}, 500)

    def log_message(self, format, *args):
        pass


def start_server(port=PORT):
    """启动 HTTP 服务器"""
    handler = RAGHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"[OK] RAG 设置面板: http://localhost:{port}")
        print(f"  在浏览器中打开即可可视化配置")
        print(f"  按 Ctrl+C 停止服务器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RAG Web 设置界面")
    parser.add_argument("--port", type=int, default=PORT, help="端口号")
    parser.add_argument("--gen-html", action="store_true", help="仅生成 HTML 文件，不启动服务器")
    parser.add_argument("--output", type=str, help="HTML 输出路径")

    args = parser.parse_args()

    if args.gen_html:
        html = generate_html()
        output = args.output or HTML_FILE
        with open(output, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[OK] HTML 文件已生成: {output}")
    else:
        start_server(args.port)
