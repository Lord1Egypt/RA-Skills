#!/usr/bin/env python3
"""Imperial Orchestrator · 执行引擎

接收路由决策，真正调用模型，处理 fallback/retry，记录 token 和成本。
这是路由器和模型 API 之间的桥梁——路由器只规划，executor 真正执行。

执行流程:
  1. 接收路由 JSON (selected_model, fallback_chain, system_prompt, ...)
  2. 组装请求 (system_prompt + user task)
  3. 调用 selected_model
  4. 失败 → 自动走 fallback_chain
  5. 全部失败 → survival_model
  6. 记录 token/成本/延迟，更新 state，写审计日志
  7. 如果有 review_roles → 自动送审

用法:
  # 从 stdin 读路由 JSON
  python3 scripts/router.py --task "写一个 LRU Cache" | python3 scripts/executor.py

  # 从文件读
  python3 scripts/executor.py --routing-json route_result.json

  # 直接指定（跳过路由器）
  python3 scripts/executor.py --model deepseek/deepseek-chat --task "Hello"
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lib import (
    AuditLog,
    RateLimiter,
    Registry,
    calculate_cost,
    estimate_tokens,
    load_json,
    now_ts,
    read_openclaw_config,
    record_failure,
    record_success,
    refresh_group_summaries,
    save_json,
)
from model_validator import resolve_api_base, resolve_api_key, is_local_provider, _build_endpoint


# ── 全局速率限制器 ────────────────────────────────────────────────────

_rate_limiter = RateLimiter(window_seconds=60, max_requests=50)


# ── API 调用 ──────────────────────────────────────────────────────────

def _http_call(url: str, payload: bytes, headers: Dict[str, str], timeout: int) -> Dict[str, Any]:
    """通用 HTTP 调用，返回解析后的结果。"""
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    start = time.monotonic()

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            latency_ms = (time.monotonic() - start) * 1000
            body = json.loads(resp.read())
            return {"success": True, "body": body, "latency_ms": round(latency_ms, 1)}
    except urllib.error.HTTPError as e:
        latency_ms = (time.monotonic() - start) * 1000
        code = e.code
        try:
            raw = e.read()
            parsed = json.loads(raw)
            detail = parsed.get("error", {})
            if isinstance(detail, dict):
                detail = detail.get("message", str(e))
        except Exception:
            detail = str(e)
        error_type = "auth" if code in (401, 403) else ("rate_limit" if code == 429 else "server_error")
        return {"success": False, "error_type": error_type, "error": f"HTTP {code}: {detail}", "latency_ms": round(latency_ms, 1)}
    except (TimeoutError, urllib.error.URLError) as e:
        latency_ms = (time.monotonic() - start) * 1000
        return {"success": False, "error_type": "timeout", "error": str(e), "latency_ms": round(latency_ms, 1)}
    except Exception as e:
        latency_ms = (time.monotonic() - start) * 1000
        return {"success": False, "error_type": "server_error", "error": str(e), "latency_ms": round(latency_ms, 1)}


def _extract_response(body: Dict[str, Any], api_type: str) -> Dict[str, Any]:
    """从不同 API 格式的响应体中提取统一的 content/tokens。"""
    if api_type == "anthropic-messages":
        # Anthropic: {"content": [{"text": "..."}], "usage": {"input_tokens": N, "output_tokens": N}}
        parts = body.get("content", [])
        content = "".join(p.get("text", "") for p in parts if p.get("type") == "text")
        usage = body.get("usage", {})
        return {
            "content": content,
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "finish_reason": body.get("stop_reason", "unknown"),
        }
    elif api_type == "ollama":
        # Ollama: {"message": {"content": "..."}, "eval_count": N, "prompt_eval_count": N}
        content = body.get("message", {}).get("content", "")
        return {
            "content": content,
            "input_tokens": body.get("prompt_eval_count", 0),
            "output_tokens": body.get("eval_count", 0),
            "finish_reason": "stop" if body.get("done") else "unknown",
        }
    else:
        # OpenAI 兼容
        choices = body.get("choices", [])
        content = choices[0].get("message", {}).get("content", "") if choices else ""
        usage = body.get("usage", {})
        return {
            "content": content,
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
            "finish_reason": choices[0].get("finish_reason", "unknown") if choices else "empty",
        }


def call_model_api(
    base_url: str,
    model_id: str,
    api_key: Optional[str],
    api_type: str,
    messages: List[Dict[str, str]],
    max_tokens: int = 4096,
    temperature: float = 0.3,
    timeout: int = 120,
) -> Dict[str, Any]:
    """根据 API 类型调用模型。支持 openai-completions, anthropic-messages, ollama。"""
    url = _build_endpoint(base_url, api_type)

    if api_type == "anthropic-messages":
        # Anthropic 格式: system 单独提取
        system_text = ""
        user_messages = []
        for m in messages:
            if m["role"] == "system":
                system_text = m["content"]
            else:
                user_messages.append(m)
        body: Dict[str, Any] = {
            "model": model_id,
            "messages": user_messages or [{"role": "user", "content": "Hi"}],
            "max_tokens": max_tokens,
        }
        if system_text:
            body["system"] = system_text
        payload = json.dumps(body).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        if api_key:
            headers["x-api-key"] = api_key

    elif api_type == "ollama":
        payload = json.dumps({
            "model": model_id,
            "messages": messages,
            "stream": False,
            "options": {"num_predict": max_tokens, "temperature": temperature},
        }).encode("utf-8")
        headers = {"Content-Type": "application/json"}

    else:
        # OpenAI 兼容
        payload = json.dumps({
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

    result = _http_call(url, payload, headers, timeout)
    if not result["success"]:
        return result

    extracted = _extract_response(result["body"], api_type)
    return {
        "success": True,
        "latency_ms": result["latency_ms"],
        **extracted,
    }


# ── 执行单个模型 ──────────────────────────────────────────────────────

def execute_on_model(
    model_ref: str,
    messages: List[Dict[str, str]],
    providers_cfg: Dict[str, Any],
    max_tokens: int = 4096,
    timeout: int = 120,
) -> Dict[str, Any]:
    """在指定模型上执行任务。自动识别 API 类型并正确调用。"""
    provider_key = model_ref.split("/", 1)[0] if "/" in model_ref else "unknown"
    model_id = model_ref.split("/", 1)[1] if "/" in model_ref else model_ref
    provider_data = providers_cfg.get(provider_key, {})

    base_url = resolve_api_base(provider_key, provider_data)
    if not base_url:
        return {"success": False, "error_type": "config", "error": f"No API base for '{provider_key}'", "latency_ms": 0}

    api_key = resolve_api_key(provider_key, provider_data)
    if not api_key and not is_local_provider(provider_key):
        return {"success": False, "error_type": "auth", "error": f"No API key for '{provider_key}'", "latency_ms": 0}

    # Find model-level api type from provider config
    api_type = "openai-completions"
    models_list = provider_data.get("models", [])
    if isinstance(models_list, list):
        for m in models_list:
            if m.get("id") == model_id:
                api_type = (m.get("api") or provider_data.get("api") or "openai-completions").lower()
                break
    else:
        api_type = (provider_data.get("api") or "openai-completions").lower()

    # 速率限制检查
    wait = _rate_limiter.wait_time(provider_key)
    if wait > 0:
        time.sleep(min(wait, 5))
    _rate_limiter.record_request(provider_key)

    return call_model_api(base_url, model_id, api_key, api_type, messages, max_tokens, timeout=timeout)


# ── Fallback 链执行 ───────────────────────────────────────────────────

def execute_with_fallback(
    model_chain: List[str],
    messages: List[Dict[str, str]],
    providers_cfg: Dict[str, Any],
    state: Dict[str, Any],
    audit: AuditLog,
    max_tokens: int = 4096,
    timeout: int = 120,
) -> Dict[str, Any]:
    """按顺序尝试模型链，直到成功或全部失败。"""
    errors = []

    for i, model_ref in enumerate(model_chain):
        attempt = i + 1
        audit.log("execute_attempt", model=model_ref, attempt=attempt, total_chain=len(model_chain))

        result = execute_on_model(model_ref, messages, providers_cfg, max_tokens, timeout)

        if result["success"]:
            # 成功 → 更新 state
            record_success(state, model_ref)
            input_tokens = result.get("input_tokens", 0)
            output_tokens = result.get("output_tokens", 0)

            # 如果 API 没返回 token 数，用估算
            if input_tokens == 0:
                input_tokens = sum(estimate_tokens(m.get("content", "")) for m in messages)
            if output_tokens == 0:
                output_tokens = estimate_tokens(result.get("content", ""))

            cost = calculate_cost(model_ref, input_tokens, output_tokens)
            result["input_tokens"] = input_tokens
            result["output_tokens"] = output_tokens
            result["cost_usd"] = round(cost, 6)
            result["model_used"] = model_ref
            result["attempt"] = attempt
            result["fallback_used"] = attempt > 1

            audit.log(
                "execute_success",
                model=model_ref,
                attempt=attempt,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=round(cost, 6),
                latency_ms=result["latency_ms"],
            )
            return result
        else:
            # 失败 → 记录并继续
            error_type = result.get("error_type", "server_error")
            record_failure(state, model_ref, error_type)
            errors.append({"model": model_ref, "error": result.get("error", ""), "error_type": error_type})

            audit.log(
                "execute_failure",
                model=model_ref,
                attempt=attempt,
                error_type=error_type,
                error=result.get("error", ""),
            )

    # 全部失败
    return {
        "success": False,
        "error_type": "all_failed",
        "error": f"All {len(model_chain)} models failed",
        "errors": errors,
        "latency_ms": 0,
    }


# ── 审核流水线 ────────────────────────────────────────────────────────

def run_review(
    content: str,
    task: str,
    review_roles: List[str],
    review_prompts: Dict[str, str],
    state: Dict[str, Any],
    providers_cfg: Dict[str, Any],
    reg: Registry,
    audit: AuditLog,
) -> Dict[str, Any]:
    """将产出送交 censor-review 审核。返回审核结果。"""
    if not review_roles or not review_prompts:
        return {"verdict": "skip", "reason": "no review configured"}

    from router import candidate_models_for_role, choose_with_cross_provider

    results = {}
    for role in review_roles:
        prompt = review_prompts.get(role, "")
        if not prompt:
            continue

        # 找审核模型
        candidates = candidate_models_for_role(reg, state, role)
        review_model, _ = choose_with_cross_provider(candidates)
        if not review_model:
            results[role] = {"verdict": "skip", "reason": "no model available for review"}
            continue

        review_messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"请审核以下输出。\n\n## 原始任务\n{task}\n\n## 待审核内容\n{content}"},
        ]

        audit.log("review_start", role=role, model=review_model)
        result = execute_on_model(review_model, review_messages, providers_cfg, max_tokens=1024, timeout=60)

        if result["success"]:
            record_success(state, review_model)
            review_content = result.get("content", "")

            # 解析 verdict
            verdict = "pass"
            lower = review_content.lower()
            if "reject" in lower or "打回" in lower or "❌" in lower:
                verdict = "reject"
            elif "revise" in lower or "修改" in lower or "⚠️" in lower:
                verdict = "revise"

            input_tokens = result.get("input_tokens", 0) or estimate_tokens(str(review_messages))
            output_tokens = result.get("output_tokens", 0) or estimate_tokens(review_content)
            cost = calculate_cost(review_model, input_tokens, output_tokens)

            results[role] = {
                "verdict": verdict,
                "model": review_model,
                "content": review_content,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": round(cost, 6),
            }
            audit.log(
                "review_complete",
                role=role,
                model=review_model,
                verdict=verdict,
                cost_usd=round(cost, 6),
            )
        else:
            record_failure(state, review_model, result.get("error_type", "server_error"))
            results[role] = {"verdict": "skip", "reason": result.get("error", "review failed")}

    # 汇总审核结论
    verdicts = [r.get("verdict", "skip") for r in results.values()]
    if "reject" in verdicts:
        final_verdict = "reject"
    elif "revise" in verdicts:
        final_verdict = "revise"
    else:
        final_verdict = "pass"

    return {
        "verdict": final_verdict,
        "reviews": results,
    }


# ── 主入口 ────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="执行路由决策，调用模型，处理 fallback。")
    p.add_argument("--routing-json", type=Path, default=None, help="路由结果 JSON 文件")
    p.add_argument("--model", type=str, default=None, help="直接指定模型（跳过路由）")
    p.add_argument("--task", type=str, default=None, help="任务文本（直接指定时需要）")
    p.add_argument("--system-prompt", type=str, default=None, help="自定义 system prompt")
    p.add_argument("--openclaw-config", type=Path, default=None)
    p.add_argument("--state-file", type=Path, default=Path(".imperial_state.json"))
    p.add_argument("--audit-file", type=Path, default=Path(".imperial_audit.json"))
    p.add_argument("--max-tokens", type=int, default=4096)
    p.add_argument("--timeout", type=int, default=120)
    p.add_argument("--no-review", action="store_true", help="跳过审核")
    p.add_argument("--json", action="store_true", help="JSON 格式输出")
    p.add_argument("--stats", action="store_true", help="显示统计信息")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    reg = Registry(root)
    audit = AuditLog(args.audit_file)

    # 显示统计
    if args.stats:
        stats = audit.stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return 0

    # 加载 config 和 state
    cfg = read_openclaw_config(args.openclaw_config)
    providers_cfg = cfg.get("models", {}).get("providers", {}) if cfg else {}

    state = load_json(args.state_file) if args.state_file.exists() else {"models": {}}
    refresh_group_summaries(state)

    # 获取路由决策
    routing: Dict[str, Any] = {}
    if args.routing_json:
        routing = load_json(args.routing_json)
    elif args.model:
        routing = {
            "selected_model": args.model,
            "fallback_chain": [],
            "survival_model": None,
            "lead_system_prompt": args.system_prompt,
            "review_roles": [],
            "review_system_prompts": None,
        }
        if not args.task:
            print("❌ --model 模式需要 --task", file=sys.stderr)
            return 1
    else:
        # 从 stdin 读路由 JSON
        try:
            raw = sys.stdin.read()
            routing = json.loads(raw)
        except (json.JSONDecodeError, IOError) as e:
            print(f"❌ 无法读取路由 JSON: {e}", file=sys.stderr)
            return 1

    task = args.task or routing.get("reasoning", {}).get("task", "")
    if not task:
        print("❌ 缺少任务文本", file=sys.stderr)
        return 1

    # 构建模型链: selected → fallback_chain → survival
    model_chain: List[str] = []
    selected = routing.get("selected_model")
    if selected:
        model_chain.append(selected)
    model_chain.extend(routing.get("fallback_chain", []))
    survival = routing.get("survival_model")
    if survival and survival not in model_chain:
        model_chain.append(survival)

    if not model_chain:
        print("❌ 没有可用模型", file=sys.stderr)
        return 1

    # 构建 messages
    messages: List[Dict[str, str]] = []
    system_prompt = routing.get("lead_system_prompt") or args.system_prompt
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": task})

    audit.log(
        "pipeline_start",
        task=task[:200],
        lead_role=routing.get("lead_role"),
        model_chain=model_chain,
        mode=routing.get("mode"),
    )

    # 执行
    result = execute_with_fallback(
        model_chain, messages, providers_cfg, state, audit,
        max_tokens=args.max_tokens, timeout=args.timeout,
    )

    # 审核
    review_result = None
    if result["success"] and not args.no_review:
        review_roles = routing.get("review_roles", [])
        review_prompts = routing.get("review_system_prompts") or {}
        if review_roles and review_prompts:
            review_result = run_review(
                result["content"], task, review_roles, review_prompts,
                state, providers_cfg, reg, audit,
            )

    # 汇总输出
    output = {
        "success": result["success"],
        "content": result.get("content"),
        "model_used": result.get("model_used"),
        "attempt": result.get("attempt", 0),
        "fallback_used": result.get("fallback_used", False),
        "input_tokens": result.get("input_tokens", 0),
        "output_tokens": result.get("output_tokens", 0),
        "cost_usd": result.get("cost_usd", 0),
        "latency_ms": result.get("latency_ms", 0),
        "review": review_result,
    }

    if not result["success"]:
        output["error"] = result.get("error")
        output["errors"] = result.get("errors", [])

    # 统计总成本（包含审核）
    total_cost = output.get("cost_usd", 0)
    total_input = output.get("input_tokens", 0)
    total_output = output.get("output_tokens", 0)
    if review_result:
        for rv in review_result.get("reviews", {}).values():
            total_cost += rv.get("cost_usd", 0)
            total_input += rv.get("input_tokens", 0)
            total_output += rv.get("output_tokens", 0)

    output["total_cost_usd"] = round(total_cost, 6)
    output["total_input_tokens"] = total_input
    output["total_output_tokens"] = total_output

    audit.log(
        "pipeline_complete",
        success=result["success"],
        model=result.get("model_used"),
        total_cost_usd=round(total_cost, 6),
        total_input_tokens=total_input,
        total_output_tokens=total_output,
        review_verdict=review_result.get("verdict") if review_result else None,
    )

    # 持久化
    save_json(args.state_file, state)
    audit.flush()

    # 输出
    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if result["success"]:
            content = result.get("content", "")
            model = result.get("model_used", "?")
            tokens = f"{output['input_tokens']}→{output['output_tokens']}"
            cost = f"${output['cost_usd']:.4f}"
            lat = f"{result.get('latency_ms', 0):.0f}ms"

            if result.get("fallback_used"):
                print(f"⚠️  降级到: {model}", file=sys.stderr)
            print(content)
            print(f"\n{'─' * 50}", file=sys.stderr)
            print(f"📊 {model} | tokens: {tokens} | cost: {cost} | latency: {lat}", file=sys.stderr)
            if review_result:
                v = review_result.get("verdict", "?")
                icon = {"pass": "✅", "revise": "⚠️", "reject": "❌"}.get(v, "❓")
                print(f"🔍 审核: {icon} {v} | 总成本: ${total_cost:.4f}", file=sys.stderr)
        else:
            print(f"❌ 执行失败: {result.get('error', 'unknown')}", file=sys.stderr)

    return 0 if result["success"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
