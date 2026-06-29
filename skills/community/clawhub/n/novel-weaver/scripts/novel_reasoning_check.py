#!/usr/bin/env python3
"""
Reasoning Check - 推理审核引擎 (v3.0)
基于 deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B (transformers) 实现推理级别内容审核. CPU 可跑.

定位: finalize-chapter 第6步 (BERT 语义之后)
有模型 -> 执行5项推理审核
无模型 -> 自动跳过, 不影响现有流程

推理审核项目:
  1. 因果合理性 [HARD]
  2. 人物行为一致性 [HARD]
  3. 情绪弧自然度 [SOFT]
  4. 对话匹配度 [SOFT]
  5. 论证可靠性 [SOFT]

依赖:
  - transformers + torch (pip 安装, 有 prebuilt wheel, 无需编译)
  - deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B (transformers 格式, 首次加载自动下载 ~1GB)

安装:
  pip install transformers torch -i https://mirrors.aliyun.com/pypi/simple/
  HF_ENDPOINT=https://hf-mirror.com python -c "from transformers import AutoModel; AutoModel.from_pretrained('deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B', trust_remote_code=True)"
"""
import json, sys, re, os
from pathlib import Path

_LLM = None
_TOKENIZER = None
_DEVICE = "cpu"

MODEL_NAME = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
MODEL_CACHE = str(Path.home() / ".cache" / "huggingface" / "hub")

DIMENSIONS = [
    {"key": "causality", "name": "因果合理性", "hard": True,
     "desc": "事件是否有前文铺垫, 转折是否牵强"},
    {"key": "character_consistency", "name": "人物行为一致性", "hard": True,
     "desc": "角色行为是否符合其人格设定"},
    {"key": "emotion_arc", "name": "情绪弧自然度", "hard": False,
     "desc": "情绪转变是否有递进, 是否突兀"},
    {"key": "dialogue", "name": "对话匹配度", "hard": False,
     "desc": "对话是否符合角色身份/性格/处境"},
    {"key": "reasoning", "name": "论证可靠性", "hard": False,
     "desc": "角色的推理/判断是否有逻辑漏洞"},
]


def _download_model():
    """逐文件下载模型 (避免 snapshot_download 卡死), 支持 hf-mirror 降级"""
    import os as _os
    _os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
    _os.environ["HF_HUB_DISABLE_PROGRESS_BARS"] = "1"

    from huggingface_hub import hf_hub_download, list_repo_files
    import time

    try:
        files = list_repo_files(MODEL_NAME)
    except Exception:
        _os.environ["HF_ENDPOINT"] = "https://huggingface.co"
        try:
            files = list_repo_files(MODEL_NAME)
        except Exception as e:
            print(f"[推理审核] 无法获取文件列表: {e}")
            return False

    skip_patterns = [".gitattributes", "onnx/", "flax/", "tf/"]
    essentials = [f for f in files if not any(p in f for p in skip_patterns)]
    print(f"[推理审核] 需要下载 {len(essentials)} 个文件")

    success = True
    for fname in essentials:
        try:
            print(f"  -> {fname}...", end="", flush=True)
            t0 = time.time()
            hf_hub_download(MODEL_NAME, fname)
            elapsed = time.time() - t0
            print(f" 完成 ({elapsed:.1f}s)")
        except Exception as e:
            print(f" 失败: {e}")
            success = False
    return success


def _load_model():
    """懒加载 transformers 模型，只在本地已缓存时加载，永不联网尝试。"""
    global _LLM, _TOKENIZER, _DEVICE
    if _LLM is not None:
        return _LLM, _TOKENIZER
    try:
        import os as _os
        # 强制 CPU，避免与 LM Studio 抢夺 GPU 显存
        _os.environ.setdefault("CUDA_VISIBLE_DEVICES", "-1")
        import torch
        # transformers 导入时需要 HF_ENDPOINT 指向镜像以避免挂死
        _os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
        from transformers import AutoModelForCausalLM, AutoTokenizer

        # 强制 CPU（CUDA_VISIBLE_DEVICES=-1 后 torch.cuda.is_available() 返回 False）
        _DEVICE = "cpu"
        device_map = _DEVICE
        print(f"[推理审核] 设备: {_DEVICE.upper()}" + (f" ({torch.cuda.get_device_name(0)})" if _DEVICE == "cuda" else ""))

        # 查找本地模型缓存
        default_cache = str(Path.home() / ".cache" / "huggingface" / "hub")
        default_snap = _os.path.join(default_cache, f"models--{MODEL_NAME.replace('/', '--')}", "snapshots")
        try:
            sys.path.insert(0, str(Path(__file__).parent))
            from _path_utils import MODELS_DIR
            model_cache = str(MODELS_DIR / "ds-r1-distill-qwen-1.5b")
        except Exception:
            model_cache = default_cache

        # 先检查 MODELS_DIR，再检查默认 HF 缓存
        model_local_path = ""
        for cache_dir in [model_cache, default_cache]:
            snap_dir = _os.path.join(cache_dir, f"models--{MODEL_NAME.replace('/', '--')}", "snapshots")
            if _os.path.isdir(snap_dir):
                snap_items = [d for d in _os.listdir(snap_dir) if _os.path.isdir(_os.path.join(snap_dir, d))]
                if snap_items:
                    model_local_path = _os.path.join(snap_dir, snap_items[-1])
                    print(f"[推理审核] 本地缓存: {model_local_path}")
                    break

        if not model_local_path:
            # 没本地模型 → 跳过，绝不联网下载
            print("[推理审核] 跳过：本地无模型缓存，用户需主动安装")
            print(f"[推理审核] 安装命令: HF_ENDPOINT=https://hf-mirror.com python -c \"from transformers import AutoModel; AutoModel.from_pretrained('{MODEL_NAME}', trust_remote_code=True)\"")
            _LLM, _TOKENIZER = None, None
            return None, None

        print(f"[推理审核] 加载模型...")
        _TOKENIZER = AutoTokenizer.from_pretrained(model_local_path, trust_remote_code=True)
        _LLM = AutoModelForCausalLM.from_pretrained(
            model_local_path,
            trust_remote_code=True,
            torch_dtype="auto",
            device_map=device_map,
            low_cpu_mem_usage=True,
        )
        print(f"[推理审核] 加载完成")
    except ImportError:
        print("[推理审核] 模型不可用: 未安装 transformers/torch")
        print("[推理审核] 安装: pip install transformers torch -i https://mirrors.aliyun.com/pypi/simple/")
        _LLM = None
        _TOKENIZER = None
    except Exception as e:
        print(f"[推理审核] 模型加载失败: {e}")
        print("[推理审核] 模型将自动跳过, 不影响现有流程")
        _LLM = None
        _TOKENIZER = None
    return _LLM, _TOKENIZER


def _strip_think(text: str) -> str:
    """剥离 <think>...</think> 推理块"""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()


def _read_sub_file(chapter_dir, sub_key):
    """读取子结构文件正文 (跳过标题行和末行标记)"""
    p = Path(chapter_dir) / f"{sub_key}.txt"
    if not p.exists():
        return ""
    lines = p.read_text(encoding="utf-8-sig").strip().split("\n")
    lines = [l for l in lines if not re.match(r'L\d+ \xb7 S\d+<', l.strip())]
    if lines and re.match(r'L\d+S\d+', lines[-1].strip()):
        lines = lines[:-1]
    return "\n".join(lines)


def _build_prompt(data, chapter, chapter_dir) -> str:
    """构建推理审核 prompt"""
    ch_info = None
    for ch in data.get("chapters", []):
        if ch["id"] == chapter:
            ch_info = ch
            break
    if not ch_info:
        return ""

    subs = ch_info.get("sub_structures", {})
    sorted_keys = sorted(subs.keys())

    char_lines = []
    for c in data.get("characters", []):
        name = c.get("name", "")
        role = c.get("role", "")
        mbti = c.get("mbti", "")
        archetype = c.get("archetype", "")
        traits = c.get("traits", [])
        aliases = c.get("aliases", [])

        parts = [f"[{name}]"]
        if role:
            parts.append(f"[{role}]")
        if mbti or archetype:
            parts.append(f"[{mbti or ''}] [{archetype or ''}]")
        if traits:
            parts.append(f"[特质: {', '.join(traits[:4])}]")
        if aliases:
            parts.append(f"[别名: {', '.join(aliases)}]")
        char_lines.append(" ".join(parts))

    char_setting = "\n".join(char_lines) if char_lines else "(无角色设定)"

    sub_lines = []
    for sk in sorted_keys:
        sv = subs[sk]
        tone = sv.get("tone", "")
        emotions = sv.get("emotions", [])
        emo_str = ""
        if emotions:
            emo_parts = []
            for e in emotions:
                if isinstance(e, dict):
                    emo_parts.append(f"{e.get('type','')}({e.get('intensity',0):.1f})")
                else:
                    emo_parts.append(str(e))
            emo_str = " [" + ", ".join(emo_parts) + "]"
        sub_lines.append(f"  {sk} <{sv.get('title','')}>: {sv.get('summary','')} | tone={tone}{emo_str}")
    sub_plan = "\n".join(sub_lines) if sub_lines else "(无子结构规划)"

    content_parts = []
    for sk in sorted_keys:
        text = _read_sub_file(chapter_dir, sk)
        if not text.strip():
            continue
        lines = text.strip().split("\n")
        preview = "\n".join(lines[:15])
        if len(lines) > 23:
            preview += "\n    ...(中间省略)..."
            preview += "\n" + "\n".join(lines[-8:])
        content_parts.append(f"-- {sk} --\n{preview}")
    chapter_content = "\n\n".join(content_parts) if content_parts else "(无正文)"

    dim_lines = []
    for d in DIMENSIONS:
        level = "[硬性]" if d["hard"] else "[参考]"
        dim_lines.append(f"{level} {d['name']}: {d['desc']}")
    dims_str = "\n".join(dim_lines)

    prompt = f"""你是一个专业的小说审核编辑. 请审核以下章节内容, 严格按指定 JSON 格式输出审核结果.

[角色设定]
{char_setting}

[章节概述]
{ch_info.get('overview', '(无概述)')}

[子结构规划]
{sub_plan}

[正文预览]
{chapter_content}

[审核维度]
{dims_str}

[输出要求]
以 JSON 数组格式输出, 每项格式:
{{"dimension": "维度名", "result": "PASS"|"HARD"|"SOFT", "detail": "具体说明(20-50字)"}}

必须包含全部 5 个维度, 仅输出 JSON 数组, 不要有其他文字."""
    return prompt


def check_reasoning(state_path, chapter, chapter_dir):
    """
    推理审核主入口.
    返回 issues list, 格式同 finalize-chapter 标准.
    """
    issues = []

    sp = Path(state_path)
    if not sp.exists():
        return issues
    data = json.loads(sp.read_text(encoding="utf-8-sig"))

    model, tokenizer = _load_model()
    if model is None:
        print("\n  [推理审核] 跳过 (无 DeepSeek-R1-Distill-Qwen-1.5B 模型)")
        return issues

    print(f"\n{'='*50}")
    print(f"[推理审核] 开始推理审核 (DeepSeek-R1-Distill-Qwen-1.5B, CPU)...")
    print(f"{'='*50}")

    prompt = _build_prompt(data, chapter, chapter_dir)
    if not prompt:
        print("  [推理审核] 跳过: 无法构建 prompt")
        return issues

    try:
        from transformers import pipeline as _pipeline
        pipe = _pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if _DEVICE == "cuda" else -1)
        output = pipe(
            prompt,
            max_new_tokens=1024,
            temperature=0.6,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
        raw_output = output[0]["generated_text"]
        if raw_output.startswith(prompt):
            raw_output = raw_output[len(prompt):]
    except Exception as e:
        print(f"\n  [推理审核] 推理异常: {e}")
        print(f"  -> 跳过推理审核, 不影响现有流程")
        return issues

    cleaned = _strip_think(raw_output)

    results = None
    # 先提取 ```json ... ``` 代码块
    code_match = re.search(r'```(?:json)?\s*(.*?)\s*```', cleaned, re.DOTALL)
    text_to_parse = code_match.group(1) if code_match else cleaned

    # 找所有独立的 JSON 对象
    all_objs = []
    for m in re.finditer(r'\{[^{}]*\}', text_to_parse):
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                all_objs.append(obj)
        except (json.JSONDecodeError, TypeError):
            pass

    if all_objs and len(all_objs) >= 3:
        results = all_objs
    elif len(all_objs) == 1:
        obj = all_objs[0]
        for key in ("dimensions", "results", "items", "issues"):
            if isinstance(obj.get(key), list) and len(obj[key]) > 0:
                results = obj[key]
                break
        if results is None:
            results = all_objs
    if results is None:
        try:
            obj = json.loads(text_to_parse)
            if isinstance(obj, list):
                results = obj
            elif isinstance(obj, dict):
                for key in ("dimensions", "results", "items", "issues"):
                    if isinstance(obj.get(key), list):
                        results = obj[key]
                        break
        except json.JSONDecodeError:
            pass
    if not isinstance(results, list):
        results = [results] if results else []

    if not results:
        print("  [推理审核] 无法解析审核结果, 跳过")
        return issues

    for item in results:
        if not isinstance(item, dict):
            continue
        dim = item.get("dimension", "") or item.get("name", "") or item.get("dim", "") or ""
        result_raw = str(item.get("result", "PASS"))
        detail = item.get("detail", "") or item.get("description", "") or item.get("explanation", "") or ""
        # 模型有时把值填反了: dimension 字段有 SOFT/HARD, result 字段有说明文字
        if result_raw in ("HARD", "SOFT", "PASS"):
            result = result_raw
        elif dim in ("HARD", "SOFT", "PASS"):
            result = dim
            dim = ""
        else:
            result = "SOFT"
        result = result.upper()
        if result == "PASS":
            continue
        if result == "HARD":
            issues.append({
                "file": chapter,
                "problem": f"推理审核 - {dim}: {detail}",
                "position": f"{chapter} reasoning",
                "severity": "HARD",
                "suggestion": f"请检查{dim}问题, 根据审核建议修改后重新 finalize-chapter"
            })
        elif result == "SOFT":
            issues.append({
                "file": chapter,
                "problem": f"推理审核 - {dim}: {detail}",
                "position": f"{chapter} reasoning",
                "severity": "SOFT",
                "suggestion": "参考审核建议, 如需要可手动修改"
            })

    h_count = len([i for i in issues if i.get("severity") == "HARD"])
    s_count = len([i for i in issues if i.get("severity") == "SOFT"])
    print(f"\n{'─'*50}")
    print(f"[推理审核] 完成: {h_count} HARD + {s_count} SOFT")
    print(f"{'='*50}")

    return issues


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("用法: python novel_reasoning_check.py <state_path> <chapter> <chapter_dir>")
        print("  安装: pip install transformers torch -i https://mirrors.aliyun.com/pypi/simple/")
        print("  模型: 首次运行自动下载 DeepSeek-R1-Distill-Qwen-1.5B (~1GB)")
        print("  下载镜像: HF_ENDPOINT=https://hf-mirror.com python ...")
        sys.exit(1)
    issues = check_reasoning(sys.argv[1], sys.argv[2], sys.argv[3])
    if issues:
        print(f"\n发现 {len(issues)} 个推理审核问题:")
        for i in issues:
            print(f"  [{i.get('severity','?')}] {i.get('problem','?')}")
    else:
        print("\n推理审核全部通过.")
