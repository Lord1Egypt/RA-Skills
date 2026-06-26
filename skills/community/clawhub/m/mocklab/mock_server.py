# -*- coding: utf-8 -*-
"""
MockLab Mock Server - AI-driven Mock API Service
v1.1: 新增延迟模拟、错误注入、请求镜像、动态响应
"""
import os, sys, json, re, time, random, string, threading, asyncio, urllib.parse
from pathlib import Path
from datetime import datetime
from typing import Any, Optional

SKILL_DIR = Path(__file__).parent
SCHEMA_STORE = SKILL_DIR / "schema_store"
STATE_FILE = SKILL_DIR / "state_store.json"
SCHEMA_STORE.mkdir(exist_ok=True)

try:
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    import httpx
    FASTFAPI_AVAILABLE = True
except ImportError:
    FASTFAPI_AVAILABLE = False

_projects = {}
_sequences = {}
_refs = {}
_lock = threading.Lock()
_custom_interfaces = {}  # name -> {method, path, req_fields, resp_fields}
_CUSTOM_STORE = SKILL_DIR / "custom_store.json"

def _load_state():
    global _sequences, _refs
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
            _sequences = data.get("sequences", {})
            _refs = data.get("refs", {})
        except Exception:
            pass

def _save_state():
    STATE_FILE.write_text(json.dumps({"sequences": _sequences, "refs": _refs}, ensure_ascii=False, indent=2), encoding="utf-8")

_load_state()

def _load_custom_interfaces():
    global _custom_interfaces
    if _CUSTOM_STORE.exists():
        try:
            _custom_interfaces = json.loads(_CUSTOM_STORE.read_text(encoding="utf-8"))
            print("[MockLab] Loaded %d custom interfaces" % len(_custom_interfaces))
        except Exception:
            _custom_interfaces = {}

def _save_custom_interfaces():
    _CUSTOM_STORE.write_text(json.dumps(_custom_interfaces, ensure_ascii=False, indent=2), encoding="utf-8")

_load_custom_interfaces()

def _rnd(n): return "".join(random.choices(string.digits, k=max(1,int(n or "6"))))
def _rnd_alnum(n): return "".join(random.choices(string.ascii_uppercase + string.digits, k=max(1,int(n or "6"))))
def _ts_ms(): return int(time.time() * 1000)
def _ts_s(): return int(time.time())
def _token(n="32"): return "".join(random.choices("ABCDEF0123456789", k=max(1,int(n or "32"))))
def _phone():
    p = ["130","131","132","133","134","135","136","137","138","139","150","151","152","153","155","156","157","158","159","170","171","173","175","176","177","178","179","180","181","182","183","184","185","186","187","188","189","199"]
    return random.choice(p) + "".join(random.choices(string.digits, k=8))
def _idcard():
    provs = ["110000","310000","440100","330100","320500","420100","510100","130100","500000"]
    base = random.choice(provs) + "%04d%02d%02d%03d" % (random.randint(1970,2000), random.randint(1,12), random.randint(1,28), random.randint(100,999))
    factors = [7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
    codes = ["1","0","X","9","8","7","6","5","4","3","2"]
    total = sum(int(base[i])*factors[i] for i in range(17))
    return base + codes[total % 11]
def _name():
    s = ["王","李","张","刘","陈","杨","黄","赵","周","吴","徐","孙","马","朱","胡","郭","何","林","罗","高"]
    g = ["伟","芳","娜","秀","敏","静","丽","强","磊","军","洋","勇","艳","杰","涛","明","超","辉","婷","颖"]
    return random.choice(s) + random.choice(g)
def _plate():
    provs = ["京","沪","粤","鲁","苏","浙","闽","川","鄂","湘","皖","赣","冀","豫"]
    return random.choice(provs) + random.choice(string.ascii_uppercase) + "".join(random.choices(string.digits + string.ascii_uppercase, k=5))
def _amount(spec=""):
    if "-" in spec:
        lo, hi = map(float, spec.split("-")); return round(random.uniform(lo, hi), 2)
    return round(random.uniform(1000, 50000), 2)
def _rate(spec=""):
    if "-" in spec:
        lo, hi = map(float, spec.split("-")); return round(random.uniform(lo, hi), 2)
    return round(random.uniform(3.5, 24.0), 2)
def _enum(s, index: int = None):
    """支持 {index} 占位符的枚举函数"""
    vals = [v.strip() for v in s.split(",")]
    parsed = {}
    for v in vals:
        if "=" in v: k, _ = v.split("=", 1); parsed[k.strip()] = v
        else: parsed[v] = v
    choices = list(parsed.values())
    if not choices: return vals[0] if vals else ""
    # 如果包含 {index} 占位符，替换后返回
    if index is not None:
        # 找到包含 {index} 的值进行替换
        for v in choices:
            if "{index}" in v:
                return v.replace("{index}", str(index))
        # 没有找到 {index}，用 index 从列表中选择（循环取值保证不越界）
        return choices[index % len(choices)]
    # 没有 index 参数，随机选择一个
    return random.choice(choices)
def _seq(key):
    global _sequences
    with _lock:
        _sequences[key] = _sequences.get(key, 0) + 1
        return datetime.now().strftime("%Y%m%d") + "%06d" % _sequences[key]
def _date(): days = random.randint(-365,0); return datetime.fromtimestamp(time.time() + days*86400).strftime("%Y-%m-%d")
def _datetime(): days = random.randint(-30,0); ts = time.time() + days*86400 + random.randint(0,86399); return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
_PROVINCES = {"110000":"北京市","120000":"天津市","130000":"河北省","140000":"山西省","150000":"内蒙古","210000":"辽宁省","220000":"吉林省","230000":"黑龙江省","310000":"上海市","320000":"江苏省","330000":"浙江省","340000":"安徽省","350000":"福建省","360000":"江西省","370000":"山东省","410000":"河南省","420000":"湖北省","430000":"湖南省","440000":"广东省","450000":"广西省","460000":"海南省","500000":"重庆市","510000":"四川省","520000":"贵州省","530000":"云南省","540000":"西藏区","610000":"陕西省","620000":"甘肃省","630000":"青海省","640000":"宁夏区","650000":"新疆区"}
_CITIES = {"110100":("北京市","110000"),"310100":("上海市","310000"),"440100":("广州市","440000"),"440300":("深圳市","440000"),"330100":("杭州市","330000"),"320100":("南京市","320000"),"420100":("武汉市","420000"),"510100":("成都市","510000"),"500100":("重庆市","500000"),"610100":("西安市","610000")}
def _prov_code(): return random.choice(list(_PROVINCES.keys()))
def _prov_name(): return random.choice(list(_PROVINCES.values()))
def _city_code(pc=""):
    for code, (name, pcode) in _CITIES.items():
        if not pc or pcode == pc: return code
    return random.choice(list(_CITIES.keys()))
def _city_name(pc=""):
    for code, (name, pcode) in _CITIES.items():
        if not pc or pcode == pc: return name
    return list(_PROVINCES.values())[0]

# ─────────────────────────────────────────────
# v1.1 新增：工具函数
# ─────────────────────────────────────────────

def _get_nested_value(data: dict, path: str):
    """支持下钻路径：'data.order_id' / 'items.0.name' / 'user.phone'"""
    if not path or not data:
        return None
    parts = path.split(".")
    val = data
    for part in parts:
        if val is None:
            return None
        # 处理数组索引 like "items.0"
        if part.isdigit():
            idx = int(part)
            if isinstance(val, (list, tuple)) and idx < len(val):
                val = val[idx]
            else:
                return None
        elif isinstance(val, dict):
            val = val.get(part)
        else:
            return None
    return val

def _parse_delay(delay_spec) -> Optional[float]:
    """解析延迟配置，返回秒数（float）。None 表示不延迟。"""
    if not delay_spec:
        return None
    if isinstance(delay_spec, (int, float)):
        return float(delay_spec) / 1000.0  # ms → s
    s = str(delay_spec).strip()
    if s.isdigit():
        return float(s) / 1000.0
    if "-" in s:
        try:
            lo, hi = map(float, s.split("-", 1))
            return random.uniform(lo, hi) / 1000.0
        except Exception:
            return None
    try:
        return float(s) / 1000.0
    except Exception:
        return None

def _should_error(error_spec) -> tuple:
    """
    解析 error 配置，返回 (是否触发, 错误信息字典)。
    格式: "http_status[@prob[:err_code[:message]]]"
    示例:
      "500"                        → 100% HTTP 500
      "500@0.05"                   → 5% 概率 HTTP 500
      "500@1.0:ERR001:自定义消息"  → 100% HTTP 500，body.code=ERR001，body.error=自定义消息
      "timeout"                    → 模拟超时
      "network_error"              → 模拟网络错误
    """
    if not error_spec:
        return False, None

    prob = 1.0
    err_code = None
    err_msg = "Mock 模拟错误"
    http_status_part = str(error_spec).strip()

    # 1. 分离 @prob（如果有）
    if "@" in error_spec:
        idx_at = error_spec.rfind("@")
        http_status_part = error_spec[:idx_at]           # @ 前：基础状态
        prob_part = error_spec[idx_at + 1:]              # @ 后：概率[:err_code[:message]]

        # prob_part 第一个 : 前是概率
        if ":" in prob_part:
            prob_str, err_details = prob_part.split(":", 1)
            try:
                prob = float(prob_str)
            except Exception:
                prob = 1.0
            # err_details 格式: err_code[:message]
            if ":" in err_details:
                err_code, err_msg = err_details.split(":", 1)
            else:
                err_code = err_details
        else:
            try:
                prob = float(prob_part)
            except Exception:
                prob = 1.0

    # 2. 从 http_status_part 中提取 err_code 和 err_msg（跨格式复用）
    # 格式: http_status[:err_code[:message]]
    if ":" in http_status_part:
        parts = http_status_part.split(":")
        http_status_part = parts[0]
        if len(parts) > 1 and err_code is None:
            err_code = parts[1]
        if len(parts) > 2 and err_msg == "Mock 模拟错误":
            err_msg = parts[2]

    if random.random() > prob:
        return False, None

    err_map = {
        "timeout":       {"type": "timeout",  "http_code": 504, "err_code": err_code, "message": err_msg},
        "network_error": {"type": "network",  "http_code": 502, "err_code": err_code, "message": err_msg},
        "rate_limit":    {"type": "status",   "http_code": 429, "err_code": err_code, "message": err_msg},
    }
    if http_status_part in err_map:
        result = dict(err_map[http_status_part])
        if err_code: result["err_code"] = err_code
        if err_msg: result["message"] = err_msg
        return True, result

    try:
        http_code = int(http_status_part)
        return True, {"type": "status", "http_code": http_code, "err_code": err_code, "message": err_msg}
    except Exception:
        return False, None

def _resolve_dynamic_value(rule: str, fname: str, req_context: dict) -> Any:
    """
    解析动态响应规则：
      mirror          — 取请求 body 中同名字段
      body:xxx        — 取请求 body 中 xxx 路径
      path:xxx        — 取路径参数 xxx
      query:xxx       — 取查询参数 xxx
      header:xxx      — 取请求头 xxx
      state:xxx       — 取跨次调用状态 xxx
    """
    if rule == "mirror":
        # 取请求 body 中字段名为 fname 的值
        return _get_nested_value(req_context.get("body"), fname)

    if rule.startswith("body:"):
        sub = rule.split(":", 1)[1]
        return _get_nested_value(req_context.get("body"), sub)

    if rule.startswith("path:"):
        sub = rule.split(":", 1)[1]
        return req_context.get("path_params", {}).get(sub)

    if rule.startswith("query:"):
        sub = rule.split(":", 1)[1]
        return req_context.get("query_params", {}).get(sub)

    if rule.startswith("header:"):
        sub = rule.split(":", 1)[1].lower()
        headers = req_context.get("headers", {})
        return headers.get(sub) or headers.get(sub.title()) or headers.get(sub.upper())

    if rule.startswith("state:"):
        key = rule.split(":", 1)[1]
        with _lock:
            return _refs.get(key)

    return None

# ─────────────────────────────────────────────
# 核心生成函数（改造以支持 req_context）
# ─────────────────────────────────────────────

def gen_field_value(field, req_context: dict = None):
    """
    生成单个字段的 mock 值。
    req_context: {'body', 'path_params', 'query_params', 'headers', 'state'}
    """
    req_context = req_context or {}
    rule = field.get("rule", "")
    fname = field.get("name", "")
    if rule in ("skip", "ignore"): return None

    # ── when 条件字段：从 sub_rule 取实际值规则 ──
    if rule == "when":
        when_cond = field.get("when", {})
        sub_rule = when_cond.get("sub_rule", "string")
        # 用 sub_rule 递归生成值
        sub_field = dict(field)
        sub_field["rule"] = sub_rule
        # 暂时去掉 when 避免递归
        sub_field.pop("when", None)
        return gen_field_value(sub_field, req_context)

    # ── 动态响应规则（v1.1 新增）─────────────────
    if rule == "mirror":
        val = _resolve_dynamic_value("mirror", fname, req_context)
        if val is not None: return val
        # fallback: 生成假数据
        return "MIRROR_" + fname

    if rule.startswith("body:") or rule.startswith("path:") or rule.startswith("query:") or rule.startswith("header:") or rule.startswith("state:"):
        val = _resolve_dynamic_value(rule, fname, req_context)
        if val is not None: return val
        # 无 context 时返回占位值（示例展示用）
        return fname
    # ── 动态响应规则结束 ──────────────────────

    if rule.startswith("fixed:"):
        val = rule.split(":",1)[1]
        # 支持 {index} 占位符，用于数组元素编号
        if "{index}" in val:
            val = val.replace("{index}", str(field.get("_index", 0)))
        return val
    if rule.startswith("random:"): return _rnd(rule.split(":",1)[1])
    if rule.startswith("random:A:"): return _rnd_alnum(rule.split(":",2)[2])
    if rule == "timestamp:ms": return _ts_ms()
    if rule == "timestamp:s": return _ts_s()
    if rule.startswith("token"): return _token(rule.split(":",1)[1] if ":" in rule else "32")
    if rule == "phone": return _phone()
    if rule == "idcard": return _idcard()
    if rule == "name": return _name()
    if rule == "plate": return _plate()
    if rule.startswith("amount"): return _amount(rule.split(":",1)[1] if ":" in rule else "")
    if rule.startswith("rate"): return _rate(rule.split(":",1)[1] if ":" in rule else "")
    if rule.startswith("enum:"): return _enum(rule.split(":",1)[1], field.get("_index"))
    if rule.startswith("sequence:"): return _seq(rule.split(":",1)[1])
    if rule == "province:code": return _prov_code()
    if rule == "province:name": return _prov_name()
    if rule.startswith("city:"): return _city_code(rule.split(":",1)[1] if len(rule.split(":"))>1 else "")
    if rule in ("city:name","city"): return _city_name()
    if rule.startswith("date:"): return _date()
    if rule.startswith("nested:"): return _gen_object(rule.split(":",1)[1], req_context)
    if rule.startswith("object:"): return _gen_object(rule.split(":",1)[1], req_context)
    if rule.startswith("array:"):
        name = rule.split(":",1)[1]
        return [_gen_object(name, req_context, i) for i in range(random.randint(2,5))]
    if field.get("ref"):
        with _lock:
            if fname in _refs: return _refs[fname]
        return _seq(fname)
    # 字段名自动推断：只有当 rule 为空时，才根据字段名猜测合适的默认值
    if not rule:
        if "date" in fname.lower() or "time" in fname.lower(): return _datetime()
    return "MOCK_" + fname

def _gen_object(schema_name, req_context: dict = None, index: int = 0):
    for proj in _projects.values():
        inner = proj.get("inner_schemas", {})
        if schema_name in inner:
            schema = inner[schema_name]
            # 支持 {"fields": [...]} 和纯 [...] 两种格式
            fields = schema.get("fields", []) if isinstance(schema, dict) else schema
            obj = {}
            for f in fields:
                n = f.get("name","")
                if not n or re.match(r".*sign.*", n.lower()): continue
                # 给字段注入 index 信息，供 fixed:{index} 占位符使用
                f = dict(f)
                f["_index"] = index
                v = gen_field_value(f, req_context)
                if v is not None: obj[n] = v
            return obj
    return {}

def _check_condition(cond: dict, req_context: dict) -> bool:
    """检查 when 条件是否满足。"""
    if not cond:
        return True
    field = cond.get("field", "")
    op = cond.get("op", "eq")
    expect = cond.get("value")
    # 从 req_context 取值
    if field.startswith("body."):
        val = _get_nested_value(req_context.get("body"), field[5:])
    elif field.startswith("path."):
        val = req_context.get("path_params", {}).get(field[5:])
    elif field.startswith("query."):
        val = req_context.get("query_params", {}).get(field[5:])
    else:
        val = _get_nested_value(req_context.get("body"), field)
    if op == "eq": return val == expect
    if op == "ne": return val != expect
    if op == "gt": return val is not None and float(val) > float(expect)
    if op == "lt": return val is not None and float(val) < float(expect)
    if op == "contains": return val is not None and str(expect) in str(val)
    if op == "exists": return val is not None
    if op == "not_exists": return val is None
    return True

def gen_response_fields(fields, req_context: dict = None):
    """
    生成响应字段。
    req_context: {'body', 'path_params', 'query_params', 'headers'}
    """
    req_context = req_context or {}
    resp = {}
    for f in fields:
        n = f.get("name","")
        if not n or re.match(r".*sign.*", n.lower()): continue
        # 条件判断（v1.1 新增 when 条件）
        when = f.get("when")
        if when and not _check_condition(when, req_context):
            continue
        v = gen_field_value(f, req_context)
        if v is not None:
            resp[n] = v
            if f.get("is_ref"):
                with _lock: _refs[n] = v
    return resp

def _is_nested_rule(rule):
    return rule and (rule.startswith("nested:") or rule.startswith("object:") or rule.startswith("array:"))

def gen_req_example_fields(fields):
    result = []
    for f in fields:
        n = f.get("name","")
        if not n or re.match(r".*sign.*", n.lower()): continue
        rule = f.get("rule", "")
        val = gen_field_value(f)
        if _is_nested_rule(rule) and isinstance(val, (dict, list)):
            val = json.dumps(val, ensure_ascii=False, indent=2)
        result.append({
            "name": n,
            "desc": f.get("desc",""),
            "type": f.get("type","string"),
            "required": f.get("required",False),
            "rule": rule,
            "example": val,
            "is_ref": bool(f.get("is_ref", False)),
            "is_dynamic": rule.startswith(("mirror","body:","path:","query:","header:","state:")),
            "when": f.get("when"),
        })
    return result

def find_interface(project_name, api_path):
    if project_name not in _projects: return None
    for iface in _projects[project_name].get("interfaces", []):
        if iface.get("path") == api_path: return iface
    return None

def _extract_path_params(path_template: str, actual_path: str) -> dict:
    """
    从 URL 路径提取路径参数。
    path_template: '/order/{id}/detail' 或 '/order/{id}'
    actual_path:    '/order/12345/detail'
    返回 {'id': '12345'}
    """
    params = {}
    # 将模板部分 {xxx} 替换为正则
    pattern = re.sub(r'\{([^}]+)\}', r'(?P<\1>[^/]+)', path_template)
    # 兼容可选的尾斜杠
    pattern += r'/?$'
    match = re.match(pattern, actual_path)
    if match:
        params = match.groupdict()
    return params

# ─────────────────────────────────────────────
# FastAPI 应用
# ─────────────────────────────────────────────

app = FastAPI(title="MockLab", description="AI-driven Mock API Service v1.1")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

_static_dir = Path(__file__).parent / "static"
_static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

_ui_file = (Path(__file__).parent / "ui.html")
if _ui_file.exists():
    HTML_UI = _ui_file.read_text(encoding="utf-8")
else:
    HTML_UI = "<html><body><h1>ui.html not found</h1></body></html>"

@app.get("/", response_class=HTMLResponse)
async def index():
    ui_path = Path(__file__).parent / "ui.html"
    if ui_path.exists():
        return HTMLResponse(ui_path.read_text(encoding="utf-8"))
    return HTMLResponse("<html><body><h1>ui.html not found</h1></body></html>")

@app.get("/mock/projects")
async def list_projects():
    data = [{"name": name, "count": len(s.get("interfaces", []))} for name, s in _projects.items()]
    return {"code": 0, "data": data}

@app.get("/mock/project/{name}")
async def get_project(name: str):
    if name not in _projects:
        return JSONResponse({"code": 1, "error": "项目不存在"}, status_code=404)
    interfaces = [{"name": i.get("name"), "path": i.get("path"), "method": i.get("method", "POST")} for i in _projects[name].get("interfaces", [])]
    return {"code": 0, "data": interfaces}

@app.get("/mock/project-full/{name}")
async def get_project_full(name: str):
    """返回完整项目 Schema（含 inner_schemas），用于 CI 编辑器的嵌套字段编辑"""
    if name not in _projects:
        return JSONResponse({"code": 1, "error": "项目不存在"}, status_code=404)
    return {"code": 0, "data": _projects[name]}

@app.get("/mock/example/{name}/{path:path}")
async def get_example(name: str, path: str):
    import urllib.parse
    clean_path = "/" + urllib.parse.unquote(path.lstrip("/"))
    iface = find_interface(name, clean_path)
    if not iface:
        return JSONResponse({"code": 1, "error": "接口不存在"}, status_code=404)
    # raw fields 用于编辑弹窗，req_example/resp_example 用于 editor-body 的 mock 数据展示
    return {
        "code": 0,
        "data": {
            "name": iface.get("name"),
            "path": iface.get("path"),
            "method": iface.get("method", "POST"),
            "delay": iface.get("delay", ""),
            "error": iface.get("error", ""),
            "req_fields": iface.get("req_fields", []),
            "resp_fields": iface.get("resp_fields", []),
            "req_example": gen_req_example_fields(iface.get("req_fields", [])),
            "resp_example": gen_req_example_fields(iface.get("resp_fields", []))
        }
    }

@app.post("/mock/call/{name}/{path:path}")
async def call_mock(name: str, path: str, request: Request):
    """
    v1.1 核心改造：
    1. 延迟模拟（interface.delay）
    2. 错误注入（interface.error）
    3. 请求镜像 + 动态响应（通过 req_context 下钻）
    4. 支持自定义请求头（headers）
    5. 支持 Seed 固定随机数据（seed）
    """
    import urllib.parse
    raw_body = await request.body()
    # 从原始 body 解析 JSON（不要重复读 request.body()，流只能读一次）
    try:
        req_data = json.loads(raw_body.decode("utf-8")) if raw_body else {}
    except Exception:
        req_data = {}

    # ── 0. 提取全局参数（headers / seed）─────────
    # 从 X-Custom-Headers 请求头读取自定义请求头（JSON 编码）
    extra_headers = {}
    custom_headers_raw = request.headers.get("x-custom-headers")
    if custom_headers_raw:
        try:
            extra_headers = json.loads(custom_headers_raw)
        except Exception:
            pass
    seed = req_data.pop("seed", None) if isinstance(req_data, dict) else None
    if isinstance(req_data, dict) and "req" in req_data:
        req_data = req_data["req"]

    # 应用 Seed（如果指定）
    if seed is not None:
        try:
            random.seed(int(seed))
        except (ValueError, TypeError):
            pass

    # ── 1. 查找接口（先查自定义接口，再查项目接口）────
    clean_path = "/" + urllib.parse.unquote(path.lstrip("/"))

    # 优先查自定义接口（不依赖项目）
    iface = _custom_interfaces.get(clean_path)

    # 其次查项目接口
    if not iface and name in _projects:
        iface = find_interface(name, clean_path)

    if not iface:
        return JSONResponse({"code": 1, "error": "接口不存在"}, status_code=404)

    # ── 2. 构建请求上下文（用于动态响应）─────────
    query_params = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(str(request.url)).query))

    path_params = _extract_path_params(iface.get("path", clean_path), clean_path)

    headers = {k.lower(): v for k, v in request.headers.items()}

    # ── 2.1 解析 reqData / ciphertext 等加密字符串字段 ──
    req_data_merged = dict(req_data)
    for inner_field in ("reqData", "ciphertext", "data"):
        if inner_field in req_data_merged and isinstance(req_data_merged[inner_field], str):
            try:
                parsed = json.loads(req_data_merged[inner_field])
                if isinstance(parsed, dict):
                    req_data_merged.update(parsed)
            except Exception:
                pass

    req_context = {
        "body": req_data_merged,
        "path_params": path_params,
        "query_params": query_params,
        "headers": headers,
    }
    # 合并前端传递的自定义请求头
    if extra_headers:
        req_context["headers"].update(extra_headers)

    # ── 3. 延迟模拟 ───────────────────────────
    delay_spec = iface.get("delay")
    delay_seconds = _parse_delay(delay_spec)
    if delay_seconds:
        await asyncio.sleep(delay_seconds)

    # ── 4. 错误注入 ───────────────────────────
    error_spec = iface.get("error")
    should_err, err_info = _should_error(error_spec)
    if should_err:
        err_type = err_info["type"]
        http_code = err_info["http_code"]
        err_code_out = err_info.get("err_code")
        err_msg_out = err_info.get("message", "Mock 模拟错误")
        if err_type == "timeout":
            await asyncio.sleep(30)  # 超时模拟
            return JSONResponse({"code": err_code_out or 1, "error": err_msg_out}, status_code=http_code)
        if err_type == "network":
            return JSONResponse({"code": err_code_out or 1, "error": err_msg_out}, status_code=http_code)
        return JSONResponse(
            {"code": err_code_out or http_code, "error": err_msg_out},
            status_code=http_code
        )

    # ── 5. 生成响应（含动态值）─────────────────
    resp_data = gen_response_fields(iface.get("resp_fields", []), req_context)
    _save_state()

    from starlette.responses import Response
    return Response(json.dumps(resp_data, ensure_ascii=False, indent=2), media_type="application/json")

@app.post("/mock/proxy")
async def proxy_request(request: Request):
    """
    代理转发：把请求转发到真实目标地址，原样返回响应（不走 Mock 逻辑）。
    请求体: {
        "target_url": "http://localhost:8080/api/user",
        "method": "POST",
        "headers": {"Authorization": "Bearer xxx"},
        "body": {...}
    }
    """
    import httpx
    data = await request.json()
    target_url = data.get("target_url")
    method = data.get("method", "POST").upper()
    req_headers = data.get("headers", {})
    req_body = data.get("body")

    if not target_url:
        return JSONResponse({"code": 1, "error": "target_url 不能为空"}, status_code=400)

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if method == "GET":
                resp = await client.get(target_url, headers=req_headers)
            elif method == "POST":
                resp = await client.post(target_url, headers=req_headers, json=req_body)
            elif method == "PUT":
                resp = await client.put(target_url, headers=req_headers, json=req_body)
            elif method == "DELETE":
                resp = await client.delete(target_url, headers=req_headers)
            else:
                return JSONResponse({"code": 1, "error": "不支持的请求方法: " + method}, status_code=400)

        # 返回真实响应
        try:
            resp_data = resp.json()
            return Response(json.dumps(resp_data, ensure_ascii=False, indent=2), status_code=resp.status_code, media_type="application/json")
        except Exception:
            return Response(resp.text, status_code=resp.status_code, media_type="text/plain")

    except httpx.TimeoutException:
        return JSONResponse({"code": 1, "error": "请求超时: " + target_url}, status_code=504)
    except Exception as e:
        return JSONResponse({"code": 1, "error": "转发失败: " + str(e)}, status_code=502)

@app.post("/mock/load")
async def load_schema(request: Request):
    data = await request.json()
    name = data.get("name", "default")
    schema = data.get("schema", {})
    _projects[name] = schema
    schema_file = SCHEMA_STORE / (name + ".json")
    schema_file.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"code": 0, "message": "已加载 %s，%d 个接口" % (name, len(schema.get("interfaces", [])))}

@app.post("/mock/update-iface")
async def update_iface_settings(request: Request):
    """
    实时更新单个接口的 delay / error 配置，无需 reload 全量 schema。
    请求体: { "project": "项目名", "path": "/接口路径", "delay": "300-500", "error": "500@0.05" }
    """
    data = await request.json()
    project = data.get("project")
    iface_path = data.get("path", "").strip()
    delay = data.get("delay", None)
    error = data.get("error", None)

    if not project or not iface_path:
        return JSONResponse({"code": 1, "error": "缺少 project 或 path"}, status_code=400)

    clean_path = "/" + iface_path.lstrip("/")

    # 优先查自定义接口
    iface = _custom_interfaces.get(clean_path)
    is_custom = bool(iface)

    # 其次查项目接口
    if not iface:
        iface = find_interface(project, clean_path)

    if not iface:
        return JSONResponse({"code": 1, "error": "接口不存在"}, status_code=404)

    if delay is not None:
        iface["delay"] = str(delay).strip() if delay != "" else None
    if "error" in data:
        iface["error"] = str(error).strip() if error != "" else None

    if is_custom:
        # 自定义接口直接保存到 _custom_interfaces（已在原对象上修改）
        _save_custom_interfaces()
    else:
        # 项目接口回写 schema_store 中的文件（持久化）
        schema_file = SCHEMA_STORE / (project + ".json")
        if schema_file.exists():
            try:
                full_schema = json.loads(schema_file.read_text(encoding="utf-8"))
                for f_iface in full_schema.get("interfaces", []):
                    if f_iface.get("path") == clean_path:
                        f_iface["delay"] = iface.get("delay")
                        f_iface["error"] = iface.get("error")
                        break
                schema_file.write_text(json.dumps(full_schema, ensure_ascii=False, indent=2), encoding="utf-8")
            except Exception as e:
                print("[MockLab] Warn: 回写 schema 失败: %s" % e)

    updated = {"path": clean_path, "delay": iface.get("delay", ""), "error": iface.get("error", "")}
    return {"code": 0, "message": "已更新", "data": updated}

# ─────────────────────────────────────────────
# v2.0 新增：自定义 Mock 接口 CRUD
# ─────────────────────────────────────────────

@app.get("/mock/custom")
async def list_custom():
    """列出所有自定义接口"""
    return {"code": 0, "data": [{"path": p, "method": v.get("method", "POST"), "name": v.get("name", p)} for p, v in _custom_interfaces.items()]}

@app.post("/mock/custom")
async def create_custom(request: Request):
    """
    创建自定义接口。
    请求体: {
        "path": "/api/users",
        "method": "POST",
        "name": "用户列表",
        "req_fields": [{"name": "page", "rule": "number"}, ...],
        "resp_fields": [{"name": "id", "rule": "random:6"}, ...]
    }
    """
    data = await request.json()
    path = "/" + data.get("path", "").strip().lstrip("/")
    if not path or path == "/":
        return JSONResponse({"code": 1, "error": "path 不能为空"}, status_code=400)
    if path in _custom_interfaces:
        return JSONResponse({"code": 1, "error": "接口已存在: %s" % path}, status_code=409)

    _custom_interfaces[path] = {
        "method": data.get("method", "POST"),
        "name": data.get("name", path),
        "path": path,
        "req_fields": data.get("req_fields", []),
        "resp_fields": data.get("resp_fields", []),
    }
    _save_custom_interfaces()
    return {"code": 0, "message": "已创建", "data": {"path": path}}

@app.get("/mock/custom/{path:path}")
async def get_custom(path: str):
    """获取单个自定义接口详情（用于编辑）"""
    clean_path = "/" + urllib.parse.unquote(path.lstrip("/"))
    if clean_path not in _custom_interfaces:
        return JSONResponse({"code": 1, "error": "接口不存在"}, status_code=404)
    return {"code": 0, "data": _custom_interfaces[clean_path]}

@app.put("/mock/custom/{path:path}")
async def update_custom(path: str, request: Request):
    """更新自定义接口"""
    data = await request.json()
    clean_path = "/" + urllib.parse.unquote(path.lstrip("/"))
    new_path = "/" + data.get("path", "").strip().lstrip("/") or clean_path
    if clean_path not in _custom_interfaces:
        return JSONResponse({"code": 1, "error": "接口不存在"}, status_code=404)

    entry = _custom_interfaces[clean_path]
    if new_path != clean_path:
        # path 变了：删旧建新
        del _custom_interfaces[clean_path]
        entry = _custom_interfaces[new_path] = {
            "method": data.get("method", "POST"),
            "name": data.get("name", new_path),
            "path": new_path,
            "req_fields": data.get("req_fields", []),
            "resp_fields": data.get("resp_fields", []),
        }
    else:
        entry.update({
            "method": data.get("method", "POST"),
            "name": data.get("name", clean_path),
            "req_fields": data.get("req_fields", []),
            "resp_fields": data.get("resp_fields", []),
        })
    _save_custom_interfaces()
    return {"code": 0, "message": "已更新", "data": {"path": new_path}}

@app.delete("/mock/custom/{path:path}")
async def delete_custom(path: str):
    """删除自定义接口"""
    clean_path = "/" + urllib.parse.unquote(path.lstrip("/"))
    if clean_path not in _custom_interfaces:
        return JSONResponse({"code": 1, "error": "接口不存在"}, status_code=404)
    del _custom_interfaces[clean_path]
    _save_custom_interfaces()
    return {"code": 0, "message": "已删除"}

@app.put("/mock/project/{project}/interface")
async def update_project_interface(project: str, request: Request):
    """更新项目接口（编辑项目接口后保存）"""
    data = await request.json()
    clean_path = "/" + data.get("path", "").strip().lstrip("/")
    if not clean_path or clean_path == "/":
        return JSONResponse({"code": 1, "error": "path 不能为空"}, status_code=400)
    if project not in _projects:
        return JSONResponse({"code": 1, "error": "项目不存在"}, status_code=404)

    # 查找原接口
    iface = find_interface(project, clean_path)
    if not iface:
        return JSONResponse({"code": 1, "error": "接口不存在"}, status_code=404)

    # 更新字段
    if "req_fields" in data: iface["req_fields"] = data["req_fields"]
    if "resp_fields" in data: iface["resp_fields"] = data["resp_fields"]
    if "name" in data: iface["name"] = data["name"]
    if "method" in data: iface["method"] = data["method"]

    # 更新 inner_schemas（JSON 编辑器修改的嵌套结构）
    new_inner = data.get("inner_schemas", {})
    if new_inner:
        _projects[project]["inner_schemas"] = new_inner

    # 持久化到 schema 文件
    schema_file = SCHEMA_STORE / (project + ".json")
    if schema_file.exists():
        try:
            full_schema = json.loads(schema_file.read_text(encoding="utf-8"))
            for f_iface in full_schema.get("interfaces", []):
                if f_iface.get("path") == clean_path:
                    f_iface.update({
                        "name": iface.get("name"),
                        "method": iface.get("method"),
                        "req_fields": iface.get("req_fields", []),
                        "resp_fields": iface.get("resp_fields", []),
                    })
                    break
            # 同时持久化 inner_schemas
            if new_inner:
                full_schema["inner_schemas"] = new_inner
            schema_file.write_text(json.dumps(full_schema, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            return JSONResponse({"code": 1, "error": "保存失败: " + str(e)}, status_code=500)

    return {"code": 0, "message": "已更新", "data": {"path": clean_path}}

@app.delete("/mock/state")
async def clear_state():
    global _sequences, _refs
    with _lock:
        _sequences = {}
        _refs = {}
    _save_state()
    return {"code": 0, "message": "状态已清空"}

@app.get("/mock/state")
async def get_state():
    return {"code": 0, "data": {"sequences": _sequences, "refs": _refs}}

@app.get("/mock/health")
async def health():
    return {"status": "ok", "service": "mocklab", "version": "1.1", "projects": len(_projects), "interfaces": sum(len(s.get("interfaces", [])) for s in _projects.values())}

def _load_schemas():
    for f in SCHEMA_STORE.glob("*.json"):
        try:
            schema = json.loads(f.read_text(encoding="utf-8"))
            name = f.stem
            _projects[name] = schema
            print("[MockLab] Loaded: %s (%d interfaces)" % (name, len(schema.get("interfaces", []))))
        except Exception as e:
            print("[MockLab] Warn: failed to load %s: %s" % (f.name, e))

_load_schemas()

def start(port: int = 18080):
    print("\n========================================")
    print("  MockLab Mock Server v1.1")
    print("  新功能：延迟模拟 | 错误注入 | 请求镜像 | 动态响应")
    print("========================================")
    print("  URL: http://localhost:%d" % port)
    print("  Projects: %d" % len(_projects))
    print("========================================\n")
    uvicorn.run("mock_server:app", host="0.0.0.0", port=port, log_level="warning")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=18080)
    args = p.parse_args()
    start(port=args.port)
