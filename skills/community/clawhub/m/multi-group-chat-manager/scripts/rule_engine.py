"""
规则引擎（Rule Engine）
======================
好感度自动加减分引擎。读取 rules/*.json 规则文件，对群消息进行匹配，
自动处理 auto 规则，标记 ai 规则候选供 AI 判断。

核心设计：
- 水位线：记录已处理消息的最大 message_seq，防止重复处理
- 计数器：max_trigger_count 限制单用户单规则触发次数
- 双模式：auto 规则脚本自动执行，ai 规则标记后交给 AI
- 冲突处理：扣分优先，多条 auto 扣分取最高值

与 onebot_collector 配合：
  collector fetch → engine.evaluate_batch() → affection.py add
                                                   ↓
                                          AI 拿到 needs_ai_review
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from collections import defaultdict

# ── 路径 ──
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
RULES_DIR = SCRIPT_DIR / "rules"
COOLDOWN_FILE = RULES_DIR / "rule_cooldown.json"


# ════════════════════════════════════════════
# 辅助：JSON 读写
# ════════════════════════════════════════════

def _read_json(path, default=None):
    if not path.exists():
        return default if default is not None else {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default if default is not None else {}


def _write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# ════════════════════════════════════════════
# 核心类
# ════════════════════════════════════════════

class RuleEngine:
    """好感度规则引擎"""

    def __init__(self, skill_dir=None):
        self.skill_dir = Path(skill_dir) if skill_dir else SKILL_DIR
        self.scripts_dir = self.skill_dir / "scripts"
        self.rules_dir = self.scripts_dir / "rules"
        self.cooldown_file = self.rules_dir / "rule_cooldown.json"
        self._rules_cache = {}
        self._cooldown_cache = None

    # ── 规则加载 ──

    def load_rules(self, group_id: str) -> list:
        """加载指定群的规则列表"""
        if group_id in self._rules_cache:
            return self._rules_cache[group_id]

        path = self.rules_dir / f"rule_{group_id}.json"
        if not path.exists():
            return []

        data = _read_json(path)
        rules = data.get("rules", [])
        self._rules_cache[group_id] = rules
        return rules

    def list_groups(self) -> list:
        """列出有规则文件的群 ID 列表"""
        groups = []
        for f in self.rules_dir.glob("rule_*.json"):
            name = f.stem
            if name == "rule_sample" or name == "rule_cooldown":
                continue
            gid = name.replace("rule_", "")
            groups.append(gid)
        return sorted(groups)

    # ── 水位线管理 ──

    def _load_cooldown(self) -> dict:
        if self._cooldown_cache is not None:
            return self._cooldown_cache
        self._cooldown_cache = _read_json(self.cooldown_file, {})
        return self._cooldown_cache

    def _save_cooldown(self):
        _write_json(self.cooldown_file, self._cooldown_cache or {})

    def get_watermark(self, group_id: str) -> int:
        """获取已处理的最大 message_seq"""
        cd = self._load_cooldown()
        return cd.get(group_id, {}).get("watermark", 0)

    def set_watermark(self, group_id: str, seq: int):
        """更新水位线"""
        cd = self._load_cooldown()
        if group_id not in cd:
            cd[group_id] = {"watermark": 0, "counters": {}}
        old = cd[group_id].get("watermark", 0)
        if seq > old:
            cd[group_id]["watermark"] = seq
            self._save_cooldown()

    # ── 计数器管理 ──

    def get_counter(self, group_id: str, user_id: str, rule_key: str) -> int:
        """获取某人某规则的触发次数"""
        cd = self._load_cooldown()
        return cd.get(group_id, {}).get("counters", {}).get(user_id, {}).get(rule_key, 0)

    def increment_counter(self, group_id: str, user_id: str, rule_key: str):
        """增加触发计数"""
        cd = self._load_cooldown()
        g = cd.setdefault(group_id, {"watermark": 0, "counters": {}})
        u = g["counters"].setdefault(user_id, {})
        u[rule_key] = u.get(rule_key, 0) + 1
        self._save_cooldown()

    def reset_counters(self, group_id: str = None):
        """重置计数器（上下线时刷新）"""
        cd = self._load_cooldown()
        if group_id:
            if group_id in cd:
                cd[group_id]["counters"] = {}
        else:
            for g in cd:
                cd[g]["counters"] = {}
        self._save_cooldown()

    # ── 消息匹配 ──

    def _get_message_text(self, message: dict) -> str:
        """从消息中提取文本内容，安全处理 None 值"""
        if not isinstance(message, dict):
            return ""
        # 兼容 onebot_collector 输出（text 字段）
        text = message.get("text")
        if text and isinstance(text, str):
            return text
        # 兼容标准 OneBot 格式（message 数组）
        msg = message.get("message")
        if isinstance(msg, list):
            parts = []
            for seg in msg:
                if isinstance(seg, dict) and seg.get("type") == "text":
                    t = seg.get("data", {})
                    if isinstance(t, dict):
                        parts.append(t.get("text", ""))
            return " ".join(parts)
        if isinstance(msg, str):
            return msg
        return ""


    def _match_keyword_rule(self, text: str, rule: dict) -> bool:
        """关键词匹配，安全处理空文本"""
        if not text or not isinstance(text, str):
            return False
        cond = rule.get("conditions", {})
        if not isinstance(cond, dict):
            return False
        keywords = cond.get("keywords", [])
        if not keywords:
            return False
        match_type = cond.get("match_type", "any")

        try:
            if match_type == "all":
                return all(kw in text for kw in keywords)
            else:
                return any(kw in text for kw in keywords)
        except TypeError:
            return False

    def _detect_spam(self, messages: list, rule: dict) -> dict:
        """
        刷屏检测：按用户分组，检查时间窗口内的消息数。
        返回 {user_id: [matched_message_indices]}
        """
        cond = rule.get("conditions", {})
        max_count = cond.get("max_count", 5)
        window = cond.get("window_seconds", 10)
        same_content = cond.get("same_content", False)
        exclude_users = [str(u) for u in cond.get("exclude_users", [])]

        # 按用户分组（排除白名单用户）
        by_user = defaultdict(list)
        for i, msg in enumerate(messages):
            uid = str(msg.get("user_id", ""))
            if uid in exclude_users:
                continue
            by_user[uid].append((i, msg))

        def _get_time(msg):
            return msg.get("timestamp", msg.get("time", 0))

        results = defaultdict(list)
        for uid, items in by_user.items():
            # 排序（按时间）
            items.sort(key=lambda x: _get_time(x[1]))
            # 滑动窗口检测
            for i in range(len(items)):
                window_start = i
                window_end = i
                base_time = _get_time(items[i][1])

                for j in range(i + 1, len(items)):
                    if _get_time(items[j][1]) - base_time <= window:
                        window_end = j
                    else:
                        break

                count = window_end - window_start + 1
                if count >= max_count:
                    if same_content:
                        # 检查是否内容重复
                        texts = set()
                        for k in range(window_start, window_end + 1):
                            t = self._get_message_text(items[k][1]).strip()
                            if t:
                                texts.add(t)
                        if len(texts) > 2:
                            continue  # 内容不重复，不算刷屏
                    for k in range(window_start, window_end + 1):
                        results[uid].append(items[k][0])

        return dict(results)

    # ── 单条消息评估 ──

    def evaluate(self, message: dict, group_id: str) -> dict:
        """
        评估单条消息。
        返回：
        {
            "matched": None or {"rule_key": ..., "rule_name": ..., "score": ...},
            "suggested_rules": [{"key": ..., "name": ..., "score": ...}]
        }
        """
        rules = self.load_rules(group_id)
        if not rules:
            return {"matched": None, "suggested_rules": []}

        text = self._get_message_text(message)
        user_id = str(message.get("user_id", ""))
        seq = message.get("message_seq", 0)

        # 1️⃣ 检查水位线（跳过已处理的消息）
        watermark = self.get_watermark(group_id)
        is_new = seq > watermark

        # 2️⃣ 分离 auto 和 ai 规则
        auto_rules = [r for r in rules if r.get("mode") == "auto"]
        ai_rules = [r for r in rules if r.get("mode") == "ai"]

        auto_match = None
        suggested = []

        # 3️⃣ 处理 auto 规则
        if is_new:
            for rule in auto_rules:
                cond = rule.get("conditions", {})
                cond_type = cond.get("type", "keyword")

                matched = False
                if cond_type == "keyword":
                    matched = self._match_keyword_rule(text, rule)
                # frequency 类型需要批量处理，单条不处理

                if matched:
                    # 检查 max_trigger_count
                    mct = rule.get("max_trigger_count", 0)
                    current = self.get_counter(group_id, user_id, rule["key"])
                    if mct <= 0 or current < mct:
                        if auto_match is None:
                            auto_match = rule
                        else:
                            # 扣分优先，取分值最高的
                            if rule["score"] < auto_match["score"]:
                                auto_match = rule
                            elif rule["score"] > auto_match["score"] and rule["type"] == "positive":
                                auto_match = rule

            # 冲突处理：有 auto 扣分 → 跳过加分
            if auto_match and auto_match["type"] == "negative":
                # 有扣分，直接返回
                pass
            elif auto_match and auto_match["type"] == "positive":
                # 加分前确认没有扣分
                # 已经检查了，继续
                pass

        # 4️⃣ 收集 ai 规则候选（即使是已处理的消息也标记，供 AI 看上下文）
        for rule in ai_rules:
            suggested.append({
                "key": rule["key"],
                "name": rule["name"],
                "score": rule["score"],
                "type": rule["type"],
            })

        result = {
            "matched": None,
            "suggested_rules": suggested,
            "is_new": is_new,
        }

        if auto_match:
            result["matched"] = {
                "rule_key": auto_match["key"],
                "rule_name": auto_match.get("name", ""),
                "rule_type": auto_match["type"],
                "score": auto_match["score"],
            }

            # 如果是新消息，更新计数器和水位线
            if is_new:
                self.increment_counter(group_id, user_id, auto_match["key"])
                self.set_watermark(group_id, seq)

        return result

    # ── 批量评估 ──

    def evaluate_batch(self, messages: list, group_id: str) -> dict:
        """
        批量评估消息，返回按类型分类的结果。

        返回：
        {
            "auto_processed": [{"user_id", "rule_key", "rule_name", "score_change",
                                "reason", "message", "message_seq"}, ...],
            "needs_ai_review": [{"user_id", "message", "message_seq",
                                 "text", "matched_ai_rules"}, ...],
            "watermark": int,
            "summary": {"total_messages", "auto_count", "ai_count", "group_id"}
        }
        """
        rules = self.load_rules(group_id)
        if not rules:
            return {"auto_processed": [], "needs_ai_review": [], "watermark": 0,
                    "summary": {"total": 0, "auto": 0, "ai": 0, "group_id": group_id}}

        watermark = self.get_watermark(group_id)
        auto_processed = []
        needs_ai_review = []
        max_seq = watermark

        # 0️⃣ 先跑刷屏检测（频率规则需要在批量中处理）
        spam_rule = None
        spam_hits = {}
        for rule in rules:
            if rule.get("mode") == "auto" and rule.get("conditions", {}).get("type") == "frequency":
                spam_rule = rule
                spam_hits = self._detect_spam(messages, rule)
                break

        # 1️⃣ 逐条评估
        for msg in messages:
            seq = msg.get("message_seq", 0)
            if seq > max_seq:
                max_seq = seq

            is_new = seq > watermark
            text = self._get_message_text(msg)
            user_id = str(msg.get("user_id", ""))

            # 检查刷屏命中
            spammed = False
            msg_idx = messages.index(msg)
            if spam_rule and user_id in spam_hits and msg_idx in spam_hits[user_id]:
                spammed = True
                if is_new:
                    mct = spam_rule.get("max_trigger_count", 0)
                    current = self.get_counter(group_id, user_id, spam_rule["key"])
                    if mct <= 0 or current < mct:
                        auto_processed.append({
                            "user_id": user_id,
                            "rule_key": spam_rule["key"],
                            "rule_name": spam_rule.get("name", ""),
                            "score_change": spam_rule["score"],
                            "type": "negative",
                            "reason": f"刷屏检测：{spam_rule.get('window_seconds', 10)}秒内{spam_rule.get('max_count', 5)}条消息",
                            "message": text,
                            "message_seq": seq,
                        })
                        self.increment_counter(group_id, user_id, spam_rule["key"])

            # 非刷屏消息 → 跑其他 auto 规则 + 收集 ai 候选
            if not spammed:
                auto_rules = [r for r in rules
                              if r.get("mode") == "auto"
                              and r.get("conditions", {}).get("type") != "frequency"]
                ai_rules = [r for r in rules if r.get("mode") == "ai"]

                matched_auto = None

                # auto 规则匹配
                if is_new:
                    for rule in auto_rules:
                        cond_type = rule.get("conditions", {}).get("type", "keyword")
                        matched = False
                        if cond_type == "keyword":
                            matched = self._match_keyword_rule(text, rule)

                        if matched:
                            mct = rule.get("max_trigger_count", 0)
                            current = self.get_counter(group_id, user_id, rule["key"])
                            if mct <= 0 or current < mct:
                                if matched_auto is None:
                                    matched_auto = rule
                                else:
                                    # 扣分优先，取最高
                                    if rule["score"] < matched_auto["score"]:
                                        matched_auto = rule
                                    elif rule["type"] == "positive" and rule["score"] > matched_auto["score"]:
                                        matched_auto = rule

                    # 冲突处理：有 auto 扣分 → 加分跳过
                    if matched_auto:
                        auto_processed.append({
                            "user_id": user_id,
                            "rule_key": matched_auto["key"],
                            "rule_name": matched_auto.get("name", ""),
                            "score_change": matched_auto["score"],
                            "type": matched_auto["type"],
                            "reason": f"规则匹配：{matched_auto.get('name', '')}",
                            "message": text,
                            "message_seq": seq,
                        })
                        self.increment_counter(group_id, user_id, matched_auto["key"])

                # 收集 ai 候选（标记全部消息，方便 AI 看上下文）
                ai_rules_matched = [
                    {"key": r["key"], "name": r["name"], "score": r["score"], "type": r["type"]}
                    for r in ai_rules
                ]
                if ai_rules_matched:
                    needs_ai_review.append({
                        "user_id": user_id,
                        "message": text,
                        "message_seq": seq,
                        "timestamp": msg.get("timestamp", msg.get("time", 0)),
                        "matched_ai_rules": ai_rules_matched,
                    })

        # 更新水位线
        self.set_watermark(group_id, max_seq)

        return {
            "auto_processed": auto_processed,
            "needs_ai_review": needs_ai_review,
            "watermark": max_seq,
            "summary": {
                "total_messages": len(messages),
                "auto_count": len(auto_processed),
                "ai_count": len(needs_ai_review),
                "group_id": group_id,
            }
        }

    # ── 执行加减分 ──

    def apply_affection(self, user_id: str, rule_key: str, reason: str) -> dict:
        """
        调用 affection.py add 执行好感度加减。
        返回 subprocess 结果。
        """
        script = self.scripts_dir / "affection.py"
        cmd = [
            sys.executable,
            str(script),
            "add",
            str(user_id),
            rule_key,
            reason,
        ]
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=15,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "stdout": "", "stderr": "timeout", "returncode": -1}
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}

    def apply_batch(self, items: list) -> list:
        """
        批量执行加减分。
        items: [{"user_id": ..., "rule_key": ..., "reason": ...}, ...]
        返回每个的执行结果。
        """
        results = []
        for item in items:
            r = self.apply_affection(
                item["user_id"],
                item["rule_key"],
                item.get("reason", "规则引擎自动处理"),
            )
            results.append({**item, "result": r})
        return results


# ════════════════════════════════════════════
# CLI 入口
# ════════════════════════════════════════════

def main():
    import argparse

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    engine = RuleEngine()

    parser = argparse.ArgumentParser(description="好感度规则引擎 CLI")
    sub = parser.add_subparsers(dest="cmd")

    # list
    p_list = sub.add_parser("list", help="列出有规则文件的群")
    p_list.add_argument("--json", action="store_true", help="JSON 格式")

    # status
    p_status = sub.add_parser("status", help="查看群规则状态")
    p_status.add_argument("group_id", help="群号")

    # evaluate
    p_eval = sub.add_parser("eval", help="评估单条消息（JSON 字符串或文件）")
    p_eval.add_argument("group_id", help="群号")
    p_eval.add_argument("--message", help="消息 JSON 字符串")
    p_eval.add_argument("--file", help="消息 JSON 文件路径")

    # batch
    p_batch = sub.add_parser("batch", help="批量评估消息（JSON 文件）")
    p_batch.add_argument("group_id", help="群号")
    p_batch.add_argument("--file", help="消息列表 JSON 文件路径", required=True)
    p_batch.add_argument("--output", help="输出结果到文件")

    # reset
    p_reset = sub.add_parser("reset", help="重置计数器")
    p_reset.add_argument("--group", help="群号（不传则重置所有）")

    # apply
    p_apply = sub.add_parser("apply", help="单次执行好感度加减")
    p_apply.add_argument("user_id", help="用户 QQ 号")
    p_apply.add_argument("rule_key", help="规则 Key")
    p_apply.add_argument("reason", help="原因描述")

    args = parser.parse_args()

    if args.cmd == "list":
        groups = engine.list_groups()
        if args.json:
            print(json.dumps({"groups": groups}, ensure_ascii=False))
        else:
            print(f"共 {len(groups)} 个群有规则文件：")
            for g in groups:
                gname = "?"
                rules = engine.load_rules(g)
                if rules:
                    gname = rules[0].get("name", "?")
                print(f"  {g}  ({gname})")

    elif args.cmd == "status":
        rules = engine.load_rules(args.group_id)
        if not rules:
            print(json.dumps({"error": "未找到规则文件"}, ensure_ascii=False))
            return
        wm = engine.get_watermark(args.group_id)
        auto_count = sum(1 for r in rules if r.get("mode") == "auto")
        ai_count = sum(1 for r in rules if r.get("mode") == "ai")
        result = {
            "group_id": args.group_id,
            "rules_count": len(rules),
            "auto_rules": auto_count,
            "ai_rules": ai_count,
            "watermark": wm,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "eval":
        if args.message:
            msg = json.loads(args.message)
        elif args.file:
            msg = json.loads(Path(args.file).read_text(encoding="utf-8"))
        else:
            msg = json.loads(sys.stdin.read())
        result = engine.evaluate(msg, args.group_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "batch":
        msgs = json.loads(Path(args.file).read_text(encoding="utf-8"))
        result = engine.evaluate_batch(msgs, args.group_id)
        output = json.dumps(result, ensure_ascii=False, indent=2)
        if args.output:
            Path(args.output).write_text(output, encoding="utf-8")
            print(f"结果已写入 {args.output}")
        else:
            print(output)

    elif args.cmd == "reset":
        engine.reset_counters(args.group)
        if args.group:
            msg = f"群 {args.group} 计数器已重置"
        else:
            msg = "所有群计数器已重置"
        print(json.dumps({"ok": True, "message": msg}, ensure_ascii=False))

    elif args.cmd == "apply":
        r = engine.apply_affection(args.user_id, args.rule_key, args.reason)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
