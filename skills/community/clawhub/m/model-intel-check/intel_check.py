"""模型"满血度"自测脚本（断网做题版，模型无关，不限于 K3）。

只依赖 openai（pip install openai）。从 data/ 读题，直接调用
环境变量 KIMI_BASE_URL / KIMI_API_KEY 指向的 OpenAI 兼容 chat-completions 接口。
被测模型全程不联网、不使用任何工具——请求体只有一条 user 消息。

用法:
    python intel_check.py                       # 默认: GPQA 50题 + AIME 15题(第1-5、21-30题)
    python intel_check.py --suite gpqa          # 只跑 GPQA
    python intel_check.py --suite aime --aime-indices 0-29   # AIME 全 30 题
    python intel_check.py --model deepseek-v4-flash          # 测别的模型
    python intel_check.py --no-thinking         # 被测模型不支持 thinking 参数时
结果写入 results/ 目录: 每题一条 JSONL + 人工复核用 answers_*.txt + 终端汇总。

计分协议（改动则分数不可与参考值比较）:
    temperature=1.0, top_p=0.95, max_tokens=98304, thinking keep=all effort=high,
    GPQA 选项按种子 42+题号 洗牌, prompt 模板见 GPQA_TEMPLATE / AIME_SUFFIX。
"""
import argparse
import json
import os
import random
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

THINKING_BODY = {"thinking": {"type": "enabled", "keep": "all", "effort": "high"}}
LETTERS = ["A", "B", "C", "D"]

GPQA_TEMPLATE = (
    "Answer the following multiple choice question. The last line of your "
    "response should be of the following format: 'ANSWER: $LETTER' (without "
    "quotes) where LETTER is one of A,B,C,D. Think step by step before "
    "answering.\n\n{question}\n\n{choices}"
)

AIME_SUFFIX = "\n\n Please reason step by step, and put your final answer within \\boxed{}."


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def make_client():
    from openai import OpenAI
    base_url = os.environ.get("KIMI_BASE_URL", "").rstrip("/")
    api_key = os.environ.get("KIMI_API_KEY", "")
    if not base_url or not api_key:
        sys.exit("请设置环境变量 KIMI_BASE_URL 和 KIMI_API_KEY（指向被测的中转接口）")
    # 说明: 自定义 HTTP User-Agent —— 某些中转的 WAF 按 "OpenAI/Python" UA 封请求,
    # 与 prompt/temperature/top_p/effort 等计分参数无关, 不影响分数可比性。
    return OpenAI(base_url=base_url, api_key=api_key, timeout=3600,
                  default_headers={"User-Agent": "curl/8.0.1"})


def ask(client, model, prompt, thinking=True):
    """带重试的单次请求，全程流式，返回 (completion, finish_reason, usage_dict)。"""
    extra = {"extra_body": THINKING_BODY} if thinking else {}
    last_err = None
    for attempt in range(4):
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=1.0,
                top_p=0.95,
                max_tokens=98304,
                stream=True,
                stream_options={"include_usage": True},
                **extra,
            )
            parts, finish, usage = [], None, {}
            for chunk in stream:
                if chunk.choices:
                    delta = chunk.choices[0].delta
                    if getattr(delta, "content", None):
                        parts.append(delta.content)
                    if chunk.choices[0].finish_reason:
                        finish = chunk.choices[0].finish_reason
                if getattr(chunk, "usage", None):
                    usage = chunk.usage.model_dump()
            return "".join(parts), finish, usage
        except Exception as e:  # 429/5xx/断流等, 重试
            last_err = e
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"请求重试 4 次仍失败: {last_err}")


def extract_boxed(text):
    """取最后一个 \\boxed{...} 内容, 支持嵌套花括号。"""
    if not text:
        return None
    hits, i = [], 0
    while True:
        i = text.find("\\boxed{", i)
        if i < 0:
            break
        depth, j = 1, i + len("\\boxed{")
        while j < len(text) and depth:
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
            j += 1
        if depth == 0:
            hits.append(text[i + len("\\boxed{"):j - 1])
        i = j
    return hits[-1] if hits else None


def norm_num(s):
    return re.sub(r"[,\s\$\\]", "", s or "")


def run_one(client, model, item, kind, correct_letter=None, thinking=True):
    if kind == "gpqa":
        choices_text = "\n".join(f"{LETTERS[i]}) {c}" for i, c in enumerate(item["shuffled"]))
        prompt = GPQA_TEMPLATE.format(question=item["question"], choices=choices_text)
    else:
        prompt = item["problem"] + AIME_SUFFIX
    completion, finish, usage = ask(client, model, prompt, thinking=thinking)
    if kind == "gpqa":
        m = re.findall(r"ANSWER\s*:\s*\(?([A-D])\)?", completion or "")
        extracted = m[-1] if m else None
        correct = extracted == correct_letter
        target = correct_letter
    else:
        extracted = extract_boxed(completion)
        correct = extracted is not None and norm_num(extracted) == norm_num(item["answer"])
        target = item["answer"]
    return {
        "kind": kind, "id": item["id"], "target": target,
        "extracted": extracted, "correct": correct, "finish_reason": finish,
        "output_tokens": usage.get("output_tokens") or usage.get("completion_tokens"),
        "reasoning_tokens": (usage.get("output_tokens_details")
                             or usage.get("completion_tokens_details") or {}).get("reasoning_tokens"),
        "completion": completion,
    }


def gpqa_items(records, n):
    items = []
    for pos, r in enumerate(records[:n]):
        idx = list(range(4))
        random.Random(42 + pos).shuffle(idx)  # 固定种子, 各环境可复现
        shuffled = [r["choices"][i] for i in idx]
        items.append({**r, "shuffled": shuffled,
                      "correct_letter": LETTERS[shuffled.index(r["choices"][r["correct_index"]])]})
    return items


def parse_indices(spec):
    out = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        elif part:
            out.append(int(part))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suite", choices=["gpqa", "aime", "all"], default="all")
    ap.add_argument("--model", default=os.environ.get("MODEL_NAME", "kimi-k3"))
    ap.add_argument("--gpqa-n", type=int, default=50)
    ap.add_argument("--aime-indices", default="0-4,20-29",
                    help="题目下标(从0计), 如 '0-4,20-29'; 默认与参考结果同口径")
    ap.add_argument("--aime-file", default="aime2025.jsonl",
                    help="data/ 下的 AIME 题库文件名, 如 aime2026.jsonl")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--no-thinking", action="store_true",
                    help="被测模型不支持 thinking 参数时使用")
    args = ap.parse_args()

    client = make_client()
    thinking = not args.no_thinking
    jobs = []  # (kind, item, correct_letter)
    if args.suite in ("gpqa", "all"):
        for it in gpqa_items(load_jsonl(DATA / "gpqa_diamond_50.jsonl"), args.gpqa_n):
            jobs.append(("gpqa", it, it["correct_letter"]))
    if args.suite in ("aime", "all"):
        aime = load_jsonl(DATA / args.aime_file)
        for i in parse_indices(args.aime_indices):
            jobs.append(("aime", aime[i], None))
    if not jobs:
        sys.exit("没有可跑的题: 请先运行 make_data.py 准备 data/ 题库")
    print(f"共 {len(jobs)} 题 | model={args.model} | concurrency={args.concurrency} | thinking={thinking}")

    outdir = ROOT / "results"
    outdir.mkdir(exist_ok=True)
    stamp = time.strftime("%Y%m%d_%H%M%S")
    results = []
    with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
        futs = {ex.submit(run_one, client, args.model, it, kind, cl, thinking): (kind, it["id"])
                for kind, it, cl in jobs}
        done = 0
        for fut in as_completed(futs):
            kind, iid = futs[fut]
            try:
                r = fut.result()
            except Exception as e:
                r = {"kind": kind, "id": iid, "target": None, "extracted": None,
                     "correct": False, "finish_reason": "error", "completion": f"ERROR: {e}"}
            results.append(r)
            done += 1
            print(f"[{done}/{len(jobs)}] {r['kind']}#{r['id']} "
                  f"{'OK ' if r['correct'] else 'MISS'} extracted={r.get('extracted')!r}")

    jsonl_path = outdir / f"results_{stamp}.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in sorted(results, key=lambda x: (x["kind"], str(x["id"]))):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    for kind in ("gpqa", "aime"):
        sub = [r for r in results if r["kind"] == kind]
        if not sub:
            continue
        acc = sum(r["correct"] for r in sub) / len(sub)
        miss = [r["id"] for r in sub if not r["correct"]]
        with open(outdir / f"answers_{kind}_{stamp}.txt", "w", encoding="utf-8") as f:
            for r in sub:
                f.write(f"===== {r['id']} target={r['target']} extracted={r['extracted']} "
                        f"{'OK' if r['correct'] else 'MISS'}\n{r['completion']}\n\n")
        print(f"\n=== {kind.upper()}: {sum(r['correct'] for r in sub)}/{len(sub)} = {acc:.2%} | 未对: {miss}")

    err = sum(1 for r in results if r["finish_reason"] != "stop")
    if err:
        print(f"\n警告: {err} 题 finish_reason 非 stop (传输/截断), 请用 rerun_failed.py 补跑后再判分")
    print(f"\n明细: {jsonl_path}")
    print(f"人工复核文件: results/answers_*_{stamp}.txt")
    print("注意: 若某题 completion 里实际答案正确但 extracted 为空/格式异常, 以人工复核为准。")


if __name__ == "__main__":
    main()
