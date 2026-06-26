#!/usr/bin/env python3
"""
NVIDIA Agent Fleet — 智能调度器
分析任务类型，匹配最佳 Agent，调度执行
"""
import os
import sys
import json
import re
import argparse
import time
from pathlib import Path

# 添加项目根目录到路径
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from agents.registry import AGENTS, get_agent

# ===== API Key 自动发现（多个来源） =====
def _discover_api_key():
    """从多个来源尝试获取 NVIDIA API Key"""
    # 1. 环境变量
    key = os.environ.get("NVIDIA_API_KEY")
    if key:
        return key
    
    # 2. ~/.zshrc（注意：zsh插件可能污染stdout，只提取nvapi-开头的行）
    zshrc = os.path.expanduser("~/.zshrc")
    if os.path.exists(zshrc):
        try:
            import subprocess
            result = subprocess.run(
                ["bash", "-c", f"source {zshrc} && echo $NVIDIA_API_KEY"],
                capture_output=True, text=True, timeout=5
            )
            # 从stdout中提取真正的nvapi key（过滤掉zsh插件输出的污染）
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith('nvapi-'):
                    return line
        except Exception:
            pass
    
    # 3. openclaw.json 中查找
    config_paths = [
        os.path.expanduser("~/.openclaw/openclaw.json"),
        os.path.expanduser("/opt/homebrew/etc/openclaw.yaml"),
    ]
    for cp in config_paths:
        if not os.path.exists(cp):
            continue
        try:
            with open(cp) as f:
                if cp.endswith('.json'):
                    cfg = json.load(f)
                else:
                    import re
                    content = f.read()
                    match = re.search(r'nvidia[^\n]*apiKey[\s:]+["\']([^"\']+)["\']', content, re.I)
                    if match:
                        return match.group(1)
                    continue
            # 深度搜索 json
            def _search(obj, depth=0):
                if depth > 5: return None
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        if 'nvidia' in str(k).lower() and isinstance(v, str) and 'nvapi' in v:
                            return v
                        r = _search(v, depth+1)
                        if r: return r
                    for v in obj.values():
                        if isinstance(v, str) and 'nvapi' in v:
                            return v
                elif isinstance(obj, list):
                    for v in obj:
                        if isinstance(v, str) and 'nvapi' in v:
                            return v
                        r = _search(v, depth+1)
                        if r: return r
                return None
            key = _search(cfg, 0)
            if key and 'nvapi' in key:
                return key
        except Exception:
            continue
    
    return None

API_KEY = _discover_api_key()

# 如果找到key但环境变量没设，顺手设置一下方便后续调用
if API_KEY and not os.environ.get("NVIDIA_API_KEY"):
    os.environ["NVIDIA_API_KEY"] = API_KEY

# 全局超时设置（每个模型最大等待秒数）
REQUEST_TIMEOUT = {
    "default": 30,           # 通用超时
    "qwen/qwen2.5-coder-32b-instruct": 20,  # 快模型
    "meta/llama-4-maverick-17b-128e-instruct": 15,
    "meta/llama-3.1-8b-instruct": 10,  # 极快模型（备用）
    "moonshotai/kimi-k2-instruct": 25,
    "deepseek-ai/deepseek-v3.2": 60,  # 慢模型
}

def _get_timeout(model: str) -> int:
    """获取模型专属超时"""
    for key, timeout in REQUEST_TIMEOUT.items():
        if key in model:
            return timeout
    return REQUEST_TIMEOUT["default"]

BASE_URL = "https://integrate.api.nvidia.com/v1"

# ===== 任务分类引擎 =====

TASK_PATTERNS = {
    "coding": {
        "patterns": [
            r"写(个|一|一段|一个|代码|程序|脚本)", r"实现|编程|代码|开发", r"bug|调试|debug|error",
            r"算法|函数|class|类", r"sql|查询|数据库", r"git|版本控制", r"测试|单元测试",
            r"重构|优化代码|代码审查", r"python|javascript|typescript|java|go|rust|c\+\+|ruby",
            r"api|接口|rest", r"前端|后端|全栈", r"docker|kubernetes|部署",
            r"正则|正則|regex", r"命令行|shell|bash|zsh"
        ],
        "priority": ["qwen-coder-32b", "qwen3-coder-480b", "codestral", "deepseek-coder"]
    },
    "reasoning": {
        "patterns": [
            r"推理|思考|分析|推導", r"为什么|原因|原理|机制|机制",
            r"逻辑|逻辑题|论证", r"证明|证伪|推导",
            r"规划|计划|策略|方案比较", r"决策|权衡|利弊",
            r"数学|数论|几何|微积分", r"物理|化学|科学"
        ],
        "priority": ["deepseek-v3-2", "kimi-k2-thinking", "stock-analyst", "mistral-large-3", "gemma-3-27b"]
    },
    "stock": {
        "patterns": [
            r"分析|股票|股价|行情|买入|卖出|持仓|自选|A股|大盘|板块",
            r"铜陵有色|云铝|神火|四川黄金|长城电工|四川长虹|华友钴业|茅台|宁德",
            r"基本面|技术面|消息面|资金面|六维"
        ],
        "priority": ["stock-analyst", "kimi-k2", "llama-4-maverick", "mistral-small"]
    },
    "writing": {
        "patterns": [
            r"写(篇|封|段|个)", r"文章|博客|作文|故事", r"邮件|邮件|email",
            r"创意|创作|文案|广告", r"翻译|译", r"润色|改写|优化文案",
            r"大纲|框架|结构", r"报告|汇报|总结"
        ],
        "priority": ["llama-4-maverick", "llama-3-3-70b", "yi-large", "mistral-small"]
    },
    "chinese": {
        "patterns": [
            r"中文|汉语|普通话", r"成语|古诗|文言文", r"中国|传统文化",
            r"拼音|汉字|笔画", r"诗词|对联"
        ],
        "priority": ["kimi-k2", "glm-5-1", "yi-large", "qwen-3-5-397b"]
    },
    "research": {
        "patterns": [
            r"研究|论文|学术|文献", r"综述|调查|调研", r"方法论|方法",
            r"数据|数据分析|统计", r"机器学习|深度学习|AI",
            r"知识问答|百科|什么是",
        ],
        "priority": ["mistral-large-3", "deepseek-v3-2", "qwen-3-5-397b", "gemma-3-27b"]
    },
    "quick": {
        "patterns": [
            r"快速|简单|简短|一句话", r"分类|类别", r"提取|抽取",
            r"摘要|总结", r"关键词|标签", r"格式化|转换"
        ],
        "priority": ["phi-4-mini", "gemma-3-4b", "mistral-small", "llama-3-3-70b"]
    },
    "creative": {
        "patterns": [
            r"创意|脑洞|想象力", r"设计|想法|点子", r"比喻|类比",
            r"故事|小说|情节", r"角色|人物|对话"
        ],
        "priority": ["llama-4-maverick", "qwen-3-5-397b", "mistral-large-3"]
    }
}

DEFAULT_PRIORITY = ["llama-3-3-70b", "mistral-small", "kimi-k2"]

def classify_task(task_text):
    """分析任务并返回匹配的类别和分数"""
    text = task_text.lower()
    scores = {}
    
    for category, config in TASK_PATTERNS.items():
        score = 0
        for pattern in config["patterns"]:
            if re.search(pattern, text):
                score += 1
        if score > 0:
            scores[category] = score
    
    # 排序
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    return ranked

def select_agents(task_text, top_n=3):
    """根据任务选择最佳 Agent 列表"""
    categories = classify_task(task_text)
    selected = []
    used_ids = set()
    
    # 从匹配的类别中按优先级选择
    for cat, score in categories:
        config = TASK_PATTERNS.get(cat)
        if not config:
            continue
        for aid in config["priority"]:
            if aid not in used_ids and aid in AGENTS:
                agent = AGENTS[aid]
                selected.append({
                    "agent_id": aid,
                    "name": agent["name"],
                    "emoji": agent["emoji"],
                    "specialty": agent["specialty"],
                    "model": agent["model"],
                    "match_reason": f"类别: {cat}, 匹配度: {score}"
                })
                used_ids.add(aid)
                if len(selected) >= top_n:
                    break
        if len(selected) >= top_n:
            break
    
    # 如果没匹配到，用默认
    if not selected:
        for aid in DEFAULT_PRIORITY:
            agent = AGENTS.get(aid)
            if agent:
                selected.append({
                    "agent_id": aid,
                    "name": agent["name"],
                    "emoji": agent["emoji"],
                    "specialty": agent["specialty"],
                    "model": agent["model"],
                    "match_reason": "默认选择"
                })
                if len(selected) >= top_n:
                    break
    
    return {
        "task": task_text[:100],
        "categories": [{"name": c, "score": s} for c, s in categories],
        "recommendations": selected
    }

def call_model(model, system_prompt, user_message, temperature=0.3, max_tokens=2048, timeout=None):
    """调用 NVIDIA API（线程安全，带超时控制）"""
    global API_KEY
    if not API_KEY:
        return {"error": "❌ NVIDIA_API_KEY 未设置"}
    
    import urllib.request
    import urllib.error
    
    # 自动获取模型专属超时
    if timeout is None:
        timeout = _get_timeout(model)
    
    data = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }).encode()
    
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read())
            choice = result.get("choices", [{}])[0]
            return {
                "content": choice.get("message", {}).get("content", ""),
                "usage": result.get("usage", {}),
                "model": result.get("model", model)
            }
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"error": f"连接失败: {e.reason}"}
    except Exception as e:
        return {"error": f"超时/错误: {str(e)}"}

def dispatch(task, agent_id=None, verbose=True):
    """调度任务到指定或自动选择的 Agent"""
    
    if verbose:
        print(f"\n{'='*50}")
        print(f"  🎯 NVIDIA Agent Fleet 调度引擎")
        print(f"{'='*50}")
    
    if agent_id:
        # 指定 Agent
        agent = get_agent(agent_id)
        if not agent:
            return {"error": f"未知 Agent: {agent_id}"}
        if verbose:
            print(f"  Agent: {agent['emoji']} {agent['name']}")
            print(f"  模型: {agent['model']}")
        recommendations = [{
            "agent_id": agent_id,
            "name": agent["name"],
            "emoji": agent["emoji"],
            "specialty": agent["specialty"],
            "model": agent["model"],
            "match_reason": "用户指定"
        }]
    else:
        # 自动调度
        analysis = select_agents(task)
        if verbose:
            cats = ", ".join([f"{c['name']}({c['score']})" for c in analysis["categories"]])
            print(f"\n  📊 任务分析: {cats or '通用'}")
            print(f"\n  🤖 推荐 Agent:")
            for r in analysis["recommendations"]:
                print(f"     {r['emoji']} {r['name']} ← {r['match_reason']}")
        
        best = analysis["recommendations"][0]
        agent = get_agent(best["agent_id"])
        if not agent:
            return {"error": f"Agent not found: {best['agent_id']}"}
        recommendations = analysis["recommendations"]
    
    if verbose:
        print(f"\n  🚀 执行 Agent: {agent['emoji']} {agent['name']}")
        print(f"  {'='*40}")
    
    start = time.time()
    result = call_model(agent["model"], agent["system_prompt"], task)
    elapsed = time.time() - start
    
    if "error" in result:
        if verbose:
            print(f"  ❌ 错误: {result['error']}")
        return {"error": result["error"]}
    
    if verbose:
        print(f"\n  {result['content']}")
        print(f"\n  {'='*40}")
        tokens = result.get("usage", {})
        print(f"  耗时: {elapsed:.1f}s | "
              f"输入: {tokens.get('prompt_tokens', '?')} | "
              f"输出: {tokens.get('completion_tokens', '?')}")
    
    return {
        "agent_id": agent_id or best["agent_id"],
        "model": result["model"],
        "content": result["content"],
        "usage": result.get("usage", {}),
        "time_seconds": round(elapsed, 1),
        "recommendations": recommendations
    }

def multi_dispatch(task, agent_ids=None, top_n=3, parallel=False):
    """多 Agent 协同 — 多个 Agent 处理同一任务（可选并行）"""
    if agent_ids:
        agents_to_run = [(aid, get_agent(aid)) for aid in agent_ids if get_agent(aid)]
    else:
        analysis = select_agents(task, top_n=top_n)
        agents_to_run = [(r["agent_id"], get_agent(r["agent_id"])) for r in analysis["recommendations"] if get_agent(r["agent_id"])]
    
    results = []
    print(f"\n{'='*50}")
    print(f"  🔄 多 Agent 协同模式")
    print(f"  任务: {task[:60]}...")
    print(f"  模式: {'⚡ 并行' if parallel else '➡️ 串行'}")
    print(f"{'='*50}")
    
    if parallel and len(agents_to_run) > 1:
        # ===== 并行执行（带逐模型超时） =====
        from concurrent.futures import ThreadPoolExecutor, as_completed
        import threading
        
        timeout_map = {aid: _get_timeout(agent["model"]) for aid, agent in agents_to_run}
        print(f"  🚀 同时启动 {len(agents_to_run)} 个 Agent (超时: {min(timeout_map.values())}-{max(timeout_map.values())}s)...")
        results_lock = threading.Lock()
        
        def run_agent(aid, agent):
            try:
                timeout = timeout_map.get(aid, 30)
                result = call_model(agent["model"], agent["system_prompt"], task, timeout=timeout)
                with results_lock:
                    if "error" in result:
                        print(f"  ❌ {agent['emoji']} {agent['name']}: {result['error']}")
                        return None
                    else:
                        entry = {
                            "agent_id": aid,
                            "model": result["model"],
                            "name": agent["name"],
                            "emoji": agent["emoji"],
                            "content": result.get("content", ""),
                            "usage": result.get("usage", {})
                        }
                        results.append(entry)
                        print(f"  ✅ {agent['emoji']} {agent['name']}: 完成 ({len(entry['content'])} 字符)")
                        return entry
                return None
            except Exception as e:
                with results_lock:
                    print(f"  ❌ {agent['emoji']} {agent['name']}: 异常 {e}")
                return None
        
        with ThreadPoolExecutor(max_workers=len(agents_to_run)) as executor:
            futures = {executor.submit(run_agent, aid, agent): (aid, agent) for aid, agent in agents_to_run}
            for future in as_completed(futures):
                pass  # 进度已在 run_agent 里打印
        
        # 统计完成情况
        successful = len(results)
        failed = len(agents_to_run) - successful
        elapsed_all = f"并行 ({successful}成功/{failed}超时)" if failed else "并行"
    else:
        # ===== 串行执行（原有逻辑） =====
        for aid, agent in agents_to_run:
            print(f"\n  ▶ {agent['emoji']} {agent['name']} 处理中...")
            result = call_model(agent["model"], agent["system_prompt"], task)
            if "error" in result:
                print(f"    ❌ {result['error']}")
            else:
                print(f"    ✅ 完成 ({len(result.get('content', ''))} 字符)")
                results.append({
                    "agent_id": aid,
                    "model": result["model"],
                    "name": agent["name"],
                    "emoji": agent["emoji"],
                    "content": result.get("content", ""),
                    "usage": result.get("usage", {})
                })
        elapsed_all = "串行"
    
    # 汇总
    print(f"\n{'='*50}")
    print(f"  📊 协同汇总 ({len(results)}/{len(agents_to_run)} 成功, {elapsed_all})")
    for r in results:
        tokens = r.get("usage", {})
        print(f"  {r['emoji']} {r['name']}: {len(r['content'])} 字符 | "
              f"{tokens.get('prompt_tokens', '?')}→{tokens.get('completion_tokens', '?')} tokens")
    
    return results


# ===== CLI =====

def main():
    parser = argparse.ArgumentParser(
        description="NVIDIA Agent Fleet — 智能调度器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  fleet "用Python写一个快速排序"
  fleet --list
  fleet --analyze "解释一下量子计算"
  fleet --agent qwen-coder-32b "实现二分查找"
  fleet --multi "如何看待人工智能的未来？"
  fleet --multi --agent deepseek-v3-2 --agent kimi-k2 "哲学问题"
        """
    )
    
    parser.add_argument("task", nargs="?", help="任务描述")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有 Agent")
    parser.add_argument("--agent", "-a", help="指定 Agent ID")
    parser.add_argument("--multi", "-m", action="store_true", help="多 Agent 协同模式")
    parser.add_argument("--parallel", "-p", action="store_true", help="并行执行（需配合 --multi）")
    parser.add_argument("--analyze", "-n", action="store_true", help="仅分析任务，不执行")
    parser.add_argument("--top", type=int, default=3, help="推荐 Agent 数量")
    parser.add_argument("--quiet", "-q", action="store_true", help="安静模式")
    
    args = parser.parse_args()
    
    if args.list:
        print(f"\n{'='*55}")
        print(f"  🤖 NVIDIA Agent Fleet — Agent 列表 ({len(AGENTS)} 个)")
        print(f"{'='*55}")
        
        cats = {}
        for aid, info in AGENTS.items():
            key = info["specialty"][:8]
            cats.setdefault(key, []).append((aid, info))
        
        for aid, info in sorted(AGENTS.items(), key=lambda x: -x[1]["strength"]):
            speed_icon = {"极快": "⚡⚡", "快": "⚡", "中等": "🌊", "慢": "🐢"}.get(info["speed"], "")
            print(f"  {info['emoji']} {info['name']:20s} {speed_icon}"
                  f" 强度:{info['strength']:.0%}  {info['specialty']}")
        print()
        return
    
    if not args.task:
        parser.print_help()
        return
    
    if args.analyze:
        analysis = select_agents(args.task, top_n=args.top)
        print(f"\n📊 任务分析")
        print(f"{'='*40}")
        print(f"  任务: {args.task[:60]}")
        print(f"  匹配类别: {', '.join([c['name'] for c in analysis['categories']]) or '通用'}")
        print(f"\n  推荐 Agent:")
        for r in analysis["recommendations"]:
            print(f"  {r['emoji']} {r['name']:20s} [{r['agent_id']}]")
            print(f"     模型: {r['model']}")
            print(f"     专长: {r['specialty']}")
            print(f"     原因: {r['match_reason']}")
            print()
        return
    
    verbose = not args.quiet
    
    if args.multi:
        agent_ids = [a.strip() for a in args.agent.split(",")] if args.agent else None
        results = multi_dispatch(args.task, agent_ids=agent_ids, top_n=args.top, parallel=args.parallel)
        return results
    else:
        result = dispatch(args.task, agent_id=args.agent, verbose=verbose)
        return result


if __name__ == "__main__":
    main()
