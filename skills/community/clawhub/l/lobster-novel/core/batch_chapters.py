#!/usr/bin/env python3
"""
串行批量生成章节计划：每卷分N批，每批20章，串行执行。
"""
import json, os, sys, time, re, urllib.request, urllib.error, logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("batch_chapters")

API_URL = "https://token.sensenova.cn/v1/chat/completions"
MODEL = "sensenova-6.7-flash-lite"
KEY = os.environ.get("SENSENOVA_API_KEY", "")
BATCH_SIZE = 10  # 每批10章，给模型思考留空间


def call_llm(messages, temp=0.5, max_tokens=4096, retries=3, timeout=120):
    """Call SenseNova with retry. Timeout per call: 120s."""
    payload = json.dumps({
        "model": MODEL,
        "messages": messages,
        "temperature": temp,
        "max_tokens": max_tokens,
    }).encode("utf-8")

    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                API_URL, data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {KEY}",
                })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            msg = data.get("choices", [{}])[0].get("message", {})
            # Support both 'content' and 'reasoning' fields
            content = msg.get("content", "")
            if content:
                return content
            # content为空说明思考过程没走完，用reasoning可能有中间内容但很危险
            reasoning = msg.get("reasoning", "")
            logger.warning(f"content为空(finish={data.get('choices',[{}])[0].get('finish_reason','?')}), reasoning长度={len(reasoning)}")
            # 如果reasoning里有JSON，尝试提取
            if reasoning and ('{' in reasoning or '[' in reasoning):
                return reasoning
            raise ValueError(f"No content in response, finish={data.get('choices',[{}])[0].get('finish_reason','?')}")
        except Exception as e:
            logger.warning(f"LLM call failed (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(5 * (attempt + 1))
    raise RuntimeError("LLM call failed after all retries")


def extract_json(text):
    """Extract JSON from LLM response, handling truncation gracefully."""
    raw = text
    # Remove markdown fences
    text = re.sub(r'```(?:json)?\s*\n?', '', text)
    text = re.sub(r'\n?```\s*', '', text)
    # Find { ... }
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"No JSON boundaries in response")
    text = text[start:end+1]
    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Fix common issues
    text = re.sub(r',\s*}', '}', text)
    text = re.sub(r',\s*\]', ']', text)
    text = re.sub(r"'", '"', text)
    text = text.replace('None', 'null').replace('True', 'true').replace('False', 'false')
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # If we got a partial parse, try to salvage what we can
        logger.warning(f"JSON parse failed: {e}, attempting to salvage")
        raise


def generate_batch(vol_info, batch_num, total_batches, prev_summary=""):
    """Generate ONE batch of BATCH_SIZE chapters via LLM (single call)."""
    start_ch = (batch_num - 1) * BATCH_SIZE + 1
    end_ch = min(batch_num * BATCH_SIZE, vol_info["chapters"])
    batch_size = end_ch - start_ch + 1

    sys_prompt = (
        "你是DND 5e奇幻小说章节大纲策划师。"
        f"这是卷1「{vol_info['title']}」的第{batch_num}/{total_batches}批章节计划，"
        f"需要生成第{start_ch}~{end_ch}章的详细大纲。"
        "每一章要有: 标题(4-6字)、内容概要(80-120字)、场景地点、戏剧张力类型。"
        "章节之间要有悬念连接。"
        "注意：使用自建泰伦大陆世界观的地点(灰港镇/破浪者酒馆/黑色礁石滩/汉克的木屋/码头街等)，"
        "不要使用被遗忘的国度的地名(绝冬城/深水城/博德之门)。"
    )

    user_prompt = f"""卷{vol_info['number']}: {vol_info['title']}
概要: {vol_info['summary']}
等级范围: {vol_info['level_range'][0]}→{vol_info['level_range'][1]}级
职业成长: {'; '.join(vol_info['class_growth'])}
关键事件: {'; '.join(vol_info['key_encounters'])}
高潮类型: {vol_info['climax_type']}

这是该卷的第{batch_num}批(共{total_batches}批)，需要生成第{start_ch}~{end_ch}章。
{"上一批最后章节摘要: " + prev_summary if prev_summary else "这是第一批，理查德·泰森在灰港镇破浪者酒馆卖唱，过着平庸吟游诗人学徒的生活。"}

输出JSON格式:
{{
  "chapters": [
    {{
      "number": 章节号,
      "title": "标题(4-6字)",
      "summary": "内容概要(80-120字)",
      "location": "场景地点",
      "dramatic_type": "buildup/climax/resolution/twist/reveal",
      "word_target": 字数(铺垫3500/普通4000/高潮5000)
    }}
  ]
}}
"""

    msg = [{"role": "system", "content": sys_prompt},
           {"role": "user", "content": user_prompt}]

    logger.info(f"  → 生成第{start_ch}~{end_ch}章...")
    resp = call_llm(msg, temp=0.5, max_tokens=8192, timeout=180)
    data = extract_json(resp)
    chapters = data.get("chapters", [])
    logger.info(f"  ← 收到{len(chapters)}章")
    return chapters


def gen_volume_chapters(vol_info, plans_dir):
    """Generate all chapters for one volume, in BATCH_SIZE batches."""
    total = vol_info["chapters"]
    total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
    all_chapters = []
    prev_summary = ""

    for batch in range(1, total_batches + 1):
        try:
            batch_chs = generate_batch(vol_info, batch, total_batches, prev_summary)
            if batch_chs:
                all_chapters.extend(batch_chs)
                # 记录最后章节摘要供下一批参考
                last = batch_chs[-1]
                prev_summary = last.get("summary", "")[:80]
                logger.info(f"  批次{batch}/{total_batches}完成，累计{len(all_chapters)}章")
                # 每批存一次中间结果
                _save_checkpoint(plans_dir, vol_info["number"], all_chapters)
            else:
                logger.warning(f"  批次{batch}返回空，使用自动填充")
                all_chapters.extend(_fallback_batch(vol_info, batch, total))
        except Exception as e:
            logger.error(f"  批次{batch}失败: {e}，使用自动填充")
            all_chapters.extend(_fallback_batch(vol_info, batch, total))

        # 串行节流：批次间等3秒
        if batch < total_batches:
            time.sleep(3)

    return all_chapters


def _fallback_batch(vol_info, batch_num, total_chapters):
    """Fallback for one batch when LLM fails."""
    start = (batch_num - 1) * BATCH_SIZE + 1
    end = min(batch_num * BATCH_SIZE, total_chapters)
    chapters = []
    for i in range(start, end + 1):
        frac = i / total_chapters
        if frac > 0.85:
            wt, dt = 5500, "climax"
        elif i == 1:
            wt, dt = 5000, "buildup"
        elif i % 7 == 0:
            wt, dt = 4500, "twist"
        elif i % 5 == 0:
            wt, dt = 5000, "climax"
        elif i % 3 == 0:
            wt, dt = 3500, "reveal"
        else:
            wt, dt = 4000, "buildup"
        chapters.append({
            "number": i,
            "title": f"第{i}章",
            "summary": f"{vol_info['title']} 第{i}章",
            "location": vol_info["main_locations"][0] if vol_info["main_locations"] else "灰港镇",
            "dramatic_type": dt,
            "word_target": wt,
        })
    return chapters


def _save_checkpoint(plans_dir, vol_num, chapters):
    """Save intermediate results for a volume."""
    vol_info_path = plans_dir / "phase1_volumes.json"
    vols = json.loads(vol_info_path.read_text(encoding="utf-8"))
    vi = next(v for v in vols.get("volumes", []) if v["number"] == vol_num)
    vol_data = {"volume": vi, "chapters": chapters,
                "generated_at": datetime.now().isoformat()}
    (plans_dir / f"volume_{vol_num:02d}_plan.json").write_text(
        json.dumps(vol_data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"  💾 已保存 {len(chapters)}章 -> volume_{vol_num:02d}_plan.json")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="串行生成章节计划")
    parser.add_argument("--dir", default=".", help="小说项目目录")
    parser.add_argument("--volume", type=int, default=1, help="卷号")
    parser.add_argument("--all", action="store_true", help="生成所有卷")
    args = parser.parse_args()

    plans_dir = Path(args.dir) / "plans"
    vols_path = plans_dir / "phase1_volumes.json"
    if not vols_path.exists():
        logger.error(f"找不到 {vols_path}，先跑 arc_planner Phase 1")
        return

    vols = json.loads(vols_path.read_text(encoding="utf-8"))
    all_vols = vols.get("volumes", [])

    if args.all:
        target_vols = all_vols
    else:
        target_vols = [v for v in all_vols if v["number"] == args.volume]
        if not target_vols:
            logger.error(f"找不到卷{args.volume}")
            return

    for vol in target_vols:
        vn = vol["number"]
        existing = plans_dir / f"volume_{vn:02d}_plan.json"
        if existing.exists():
            logger.info(f"卷{vn} 已有计划，跳过（删掉文件可重新生成）")
            continue

        logger.info(f"\n{'='*50}")
        logger.info(f"开始生成卷{vn}: {vol['title']} ({vol['chapters']}章)")
        logger.info(f"每批{BATCH_SIZE}章，共{(vol['chapters']+BATCH_SIZE-1)//BATCH_SIZE}批")

        chapters = gen_volume_chapters(vol, plans_dir)
        logger.info(f"卷{vn} 完成: {len(chapters)}章")
        logger.info(f"{'='*50}\n")

    # 生成汇总 outline
    logger.info("全部完成！")


if __name__ == "__main__":
    main()
