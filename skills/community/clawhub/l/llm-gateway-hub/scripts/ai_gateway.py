# -*- coding: utf-8 -*-
"""AI 团队统一模型网关（LLM Gateway）V1.0.3
统一入口调用各家大模型（OpenAI 兼容协议），自动记录消耗台账，内置预算硬拦截。
用法：
  python ai_gateway.py text --provider doubao --prompt "你好"
  python ai_gateway.py image --provider doubao --prompt "封面图提示词" [--size 1920x1080]
  python ai_gateway.py models --provider doubao
  python ai_gateway.py budget                # 查看预算状态
  python ai_gateway.py doctor                # 体检：配置/Key/预算/台账健康报告
配置：gateway_config.json（本机私有，含各家 Key）——复制模板到脚本同目录即用；
      或用环境变量 LLM_GATEWAY_HOME 指定配置目录（零改路径自动探测）
预算：gateway_budget.json（月度预算，80% 预警 / 100% 硬拦截）
台账：自动追加到 API消耗台账.md
"""
import argparse
import datetime
import json
import os
import socket
import sys
import time
import urllib.request
import urllib.error

# 三个路径支持两种方式：1) 显式赋值（脚本顶部或测试中直接改）；2) 留空 None -> 自动探测（零改路径即用）
CONFIG_PATH = None
LEDGER_PATH = None
BUDGET_PATH = None
DEFAULT_BUDGET = 50.0
WARN_PCT = 0.8
HARD_PCT = 1.0


def _detect_base_dir():
    """自动探测配置目录：环境变量 LLM_GATEWAY_HOME > 脚本所在目录 > 当前目录。"""
    env = os.environ.get("LLM_GATEWAY_HOME", "").strip()
    if env:
        return os.path.abspath(env)
    here = os.path.dirname(os.path.abspath(__file__))
    if here:
        return here
    return os.getcwd()


def _init_paths():
    """初始化三个路径：显式赋值优先；未赋值则自动探测（零改路径即用）。"""
    global CONFIG_PATH, LEDGER_PATH, BUDGET_PATH
    if CONFIG_PATH is None:
        base = _detect_base_dir()
        CONFIG_PATH = os.path.join(base, "gateway_config.json")
        BUDGET_PATH = os.path.join(base, "gateway_budget.json")
        LEDGER_PATH = os.path.join(base, "API消耗台账.md")


def load_config():
    _init_paths()
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"配置文件不存在：{CONFIG_PATH}\n"
            f"请复制 gateway_config.template.json 到脚本同目录（或设置环境变量 LLM_GATEWAY_HOME 指定目录），并填写各家 Key。"
        )
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"配置文件格式错误（不是合法 JSON）：{CONFIG_PATH}\n  {e}")
    if not isinstance(cfg, dict) or "providers" not in cfg:
        raise ValueError(f"配置文件缺少 'providers' 字段：{CONFIG_PATH}")
    for name, p in cfg.get("providers", {}).items():
        if not isinstance(p, dict):
            raise ValueError(f"provider {name} 配置格式错误（应为对象）")
        if p.get("enabled") and not p.get("base_url"):
            raise ValueError(f"provider {name} 已启用但缺少 base_url（见 gateway_config.json）")
    return cfg


def load_budget():
    _init_paths()
    now = datetime.datetime.now()
    month = now.strftime("%Y-%m")
    if os.path.exists(BUDGET_PATH):
        try:
            with open(BUDGET_PATH, "r", encoding="utf-8") as f:
                b = json.load(f)
            if not isinstance(b, dict):
                raise ValueError
        except (json.JSONDecodeError, ValueError):
            # 预算文件损坏：降级到内存默认，不崩溃（首次记账时落盘覆盖）
            b = {"month": month, "spent": 0.0, "budget": DEFAULT_BUDGET}
    else:
        b = {"month": month, "spent": 0.0, "budget": DEFAULT_BUDGET}
    if b.get("month") != month:
        b = {"month": month, "spent": 0.0, "budget": b.get("budget", DEFAULT_BUDGET)}
    return b


def save_budget(b):
    _init_paths()
    with open(BUDGET_PATH, "w", encoding="utf-8") as f:
        json.dump(b, f, ensure_ascii=False, indent=2)


def check_budget(est_cost):
    """调用前预算检查：>=100% 硬拦截；>=80% 预警（图像/视频等高消耗拒绝）"""
    b = load_budget()
    ratio = (b["spent"] + est_cost) / b["budget"]
    if ratio >= HARD_PCT:
        raise RuntimeError(
            f"预算硬拦截：本月已用 {b['spent']:.2f}/{b['budget']:.0f} 元，本次调用后将达 {ratio*100:.0f}%"
            f"，已停止。请管理员调整预算（改 gateway_budget.json）或下月再试。"
        )
    if ratio >= WARN_PCT:
        print(f"⚠️ 预算预警：已用 {b['spent']:.2f}/{b['budget']:.0f} 元（{b['spent']/b['budget']*100:.0f}%），本次将达 {ratio*100:.0f}%")
    return b


def record_cost(cost):
    b = load_budget()
    b["spent"] = round(b["spent"] + cost, 4)
    save_budget(b)
    return b


def http_json(url, payload, api_key, timeout=180, retries=2, get=False):
    """统一 HTTP 调用（POST/GET）。

    - HTTP 4xx/5xx：立即抛出带状态码的 RuntimeError（不重试）
    - 网络不可达/超时(URLError)：自动重试 retries 次（指数退避），仍失败则抛出清晰 RuntimeError
    - 所有异常都被捕获并转为可读消息，绝不裸 traceback
    """
    last_err = None
    for attempt in range(retries + 1):
        try:
            if get:
                req = urllib.request.Request(url, method="GET")
            else:
                req = urllib.request.Request(url, method="POST")
                req.add_header("Content-Type", "application/json")
            req.add_header("Authorization", "Bearer " + api_key)
            data = None if get else json.dumps(payload).encode("utf-8")
            with urllib.request.urlopen(req, data, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"HTTP {e.code}: {body[:500]}")
        except urllib.error.URLError as e:
            reason = getattr(e, "reason", e)
            is_timeout = isinstance(reason, socket.timeout) or "timed out" in str(reason).lower()
            msg = f"请求超时（>{timeout}s）：{url}" if is_timeout else f"网络不可达（{url}）：{reason}"
            last_err = RuntimeError(msg)
            if attempt < retries:
                time.sleep(0.4 * (attempt + 1))  # 退避后重试
                continue
            raise last_err
    if last_err:
        raise last_err


def call_text(provider, prompt, model=None, max_tokens=1000):
    cfg = load_config()["providers"][provider]
    model = model or cfg["default_text_model"]
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
    }
    resp = http_json(cfg["base_url"] + "/chat/completions", payload, cfg["api_key"])
    content = resp["choices"][0]["message"]["content"]
    usage = resp.get("usage", {})
    return content, usage, model, "text"


def call_image(provider, prompt, size=None):
    cfg = load_config()["providers"][provider]
    size = size or cfg.get("image_size", "1920x1080")
    model = cfg["default_image_model"]
    if not model:
        raise RuntimeError(f"provider {provider} 未配置图像模型")
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "response_format": "url",
        "watermark": False,
    }
    resp = http_json(cfg["base_url"] + "/images/generations", payload, cfg["api_key"])
    url = resp["data"][0]["url"]
    usage = resp.get("usage", {})
    return url, usage, model, "image"


def list_models(provider):
    cfg = load_config()["providers"][provider]
    data = http_json(cfg["base_url"] + "/models", None, cfg["api_key"], timeout=60, get=True)
    ids = [m["id"] for m in data.get("data", [])]
    return ids


def doctor():
    """体检：配置/各provider/预算/台账，输出健康报告（不发起任何API调用）"""
    _init_paths()
    lines = []
    ok = True
    cfg_all = load_config()
    lines.append(f"配置：{CONFIG_PATH} 存在={os.path.exists(CONFIG_PATH)} 平台数={len(cfg_all.get('providers', {}))}")
    for name, p in cfg_all.get("providers", {}).items():
        en = p.get("enabled")
        key = p.get("api_key", "")
        key_ok = bool(key) and not key.startswith("XXXX") and " " not in key and key != "ollama" or name == "ollama"
        if not en:
            lines.append(f"  [{name}] 未启用（可接入）")
            continue
        if not key_ok:
            lines.append(f"  [{name}] ⚠️ Key 未配置或格式可疑")
            ok = False
        else:
            lines.append(f"  [{name}] ✅ 已启用，Key 就绪，文本模型={p.get('default_text_model','-')}，图像模型={p.get('default_image_model','-') or '-'}")
    b = load_budget()
    ratio = b["spent"] / b["budget"] * 100
    flag = "✅" if ratio < 80 else ("⚠️ 接近上限" if ratio < 100 else "🚫 已封顶")
    lines.append(f"预算：{b['month']} 已用 {b['spent']:.2f}/{b['budget']:.0f} 元（{ratio:.1f}%）{flag}")
    lines.append(f"台账：{LEDGER_PATH} 存在={os.path.exists(LEDGER_PATH)}")
    lines.append("体检完成：" + ("✅ 全部正常" if ok and ratio < 100 else "⚠️ 有需关注项，见上"))
    return "\n".join(lines)


def estimate_cost(provider, kind, usage, cfg):
    """按官网价估算费用（元）"""
    if kind == "text":
        pin = usage.get("prompt_tokens", 0)
        pout = usage.get("completion_tokens", 0)
        return pin / 1e6 * cfg["price_text_in"] + pout / 1e6 * cfg["price_text_out"], pin, pout
    if kind == "image":
        n = usage.get("generated_images", 1)
        return n * cfg.get("price_image_per", 0.2), 0, n
    return 0, 0, 0


def log_ledger(provider, model, kind, usage, cost, prompt_preview):
    _init_paths()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    if kind == "text":
        detail = f"{usage.get('prompt_tokens',0)}/{usage.get('completion_tokens',0)}"
    else:
        detail = f"{usage.get('generated_images',1)} 张"
    row = f"| {now} | 网关调用 | {model} | {kind} | {detail} | {cost:.3f} | 待累计 |\n"
    # 读取最后累计值并更新（简化：追加行，累计下次统计）
    with open(LEDGER_PATH, "a", encoding="utf-8") as f:
        f.write(row)
    return row


def main():
    ap = argparse.ArgumentParser(description="AI 团队统一模型网关")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_text = sub.add_parser("text", help="文本调用")
    p_text.add_argument("--provider", required=True)
    p_text.add_argument("--prompt", required=True)
    p_text.add_argument("--model", default=None)
    p_text.add_argument("--max-tokens", type=int, default=1000)
    p_img = sub.add_parser("image", help="图像生成")
    p_img.add_argument("--provider", required=True)
    p_img.add_argument("--prompt", required=True)
    p_img.add_argument("--size", default=None)
    p_models = sub.add_parser("models", help="列出可用模型")
    p_models.add_argument("--provider", required=True)
    sub.add_parser("budget", help="查看预算状态")
    sub.add_parser("doctor", help="体检：配置/Key/预算/台账健康报告")
    args = ap.parse_args()

    if args.cmd == "doctor":
        print(doctor())
        return

    if args.cmd == "budget":
        b = load_budget()
        ratio = b["spent"] / b["budget"] * 100
        flag = "✅" if ratio < WARN_PCT * 100 else ("⚠️ 预警" if ratio < HARD_PCT * 100 else "🚫 已封顶")
        print(f"预算状态：{b['month']} 已用 {b['spent']:.2f}/{b['budget']:.0f} 元（{ratio:.1f}%）{flag}")
        print(f"规则：≥{WARN_PCT*100:.0f}% 预警；≥{HARD_PCT*100:.0f}% 硬拦截")
        return

    cfg_all = load_config()
    if args.provider not in cfg_all["providers"]:
        sys.exit(f"未知 provider: {args.provider}，可用: {list(cfg_all['providers'])}")
    pcfg = cfg_all["providers"][args.provider]
    if not pcfg.get("enabled") or not pcfg.get("api_key"):
        sys.exit(f"provider {args.provider} 未启用或未配置 Key（见 gateway_config.json）")

    if args.cmd == "text":
        check_budget(0.01)  # 文本预估费用低，先做硬拦截检查
        content, usage, model, kind = call_text(args.provider, args.prompt, args.model, args.max_tokens)
        cost, _, _ = estimate_cost(args.provider, kind, usage, pcfg)
        record_cost(cost)
        print("=== 响应 ===")
        print(content)
        print(f"\n=== 消耗 === model={model} prompt={usage.get('prompt_tokens')} completion={usage.get('completion_tokens')} 费用≈{cost:.4f}元")
        log_ledger(args.provider, model, kind, usage, cost, args.prompt[:30])
    elif args.cmd == "image":
        check_budget(0.2)  # 图像单张 0.2 元，调用前预估检查
        url, usage, model, kind = call_image(args.provider, args.prompt, args.size)
        cost, _, _ = estimate_cost(args.provider, kind, usage, pcfg)
        record_cost(cost)
        print("=== 图片 URL ===")
        print(url)
        print(f"\n=== 消耗 === model={model} 张数={usage.get('generated_images',1)} 费用≈{cost:.4f}元")
        log_ledger(args.provider, model, kind, usage, cost, args.prompt[:30])
    elif args.cmd == "models":
        for m in list_models(args.provider):
            print(m)


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError) as e:
        # 配置类错误：转成单行清晰提示，不裸 traceback
        sys.exit(f"配置错误：{e}")
