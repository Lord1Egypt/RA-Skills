"""kids-points 记账流水线 — 消息接收 → 去重 → LLM 解析 → 校验 → 写入 → 回报。

核心原则：LLM 只负责语义理解，代码层负责所有确定性操作。
"""

import json
import time
from datetime import datetime, timezone
from typing import Optional

from .db import (
    init_db,
    get_current_balance,
    insert_transaction,
    insert_transactions_batch,
    is_message_processed,
    mark_message_processed,
    log_audit,
    cents_to_display,
    find_transaction_by_description,
    create_pending_adjustment,
    get_pending_adjustment,
    confirm_pending_adjustment,
    cancel_pending_adjustment,
    acquire_processing_lock,
    release_processing_lock,
    LockStatus,
)


# ─── LLM 调用 ────────────────────────────────────────────────────────────────

from .llm_config import LLM_API_KEY, LLM_API_URL, LLM_MODEL, AGENT_VERSION, call_llm as _call_llm, _extract_json

# 重新导出，保持 API 兼容
call_llm = _call_llm


# ─── Prompt 模板 ─────────────────────────────────────────────────────────────

CLASSIFY_PROMPT = """你是一个积分记账系统的意图分类器。分析用户消息，判断意图。

用户消息：{message}

请返回 JSON：
{{
    "intent": "record" | "adjust" | "query",
    "reasoning": "简短说明为什么是这个意图"
}}

规则：
- record：用户要加分或减分（如"口算加1分""买冰激凌扣4分"）
- adjust：用户要修正之前的记录（如"昨天的口算应该是加2分不是1分"）
- query：用户在查账（如"现在多少分""本周加了多少""口算一共加了多少"）

只返回 JSON，不要其他内容。

⚠️ 直接给 JSON,不要输出思考过程。"""


PARSE_RECORD_PROMPT = """你是积分记账系统的交易解析器。从用户消息提取所有积分变动为 JSON 数组。

返回 JSON 数组,每个元素:{{"type": "income"或"expense", "amount": 数字, "description": "保留关键修饰的简短描述"}}

规则:
1. income 加分,expense 减分;amount 均为正数(代码自动转负)
2. 一条消息可含多笔,全部提取
3. **口语换算**:"分/角/毛/块"=×1,"元"=×100;口语优先(如"5 块钱"=5 分)
4. description 只留"核心事项名词" 2-6 字: 去主语(孩子/宝贝)、形容词修饰(认真/连续/课外/三篇)、时间(7天/今天/第二天)。板子上只看"事项 + 分数",动作动词(买/写/判/补/读/找)保留。
5. 无法确定金额 → amount: null

示例:
输入:"口算加1分,买冰激凌扣4分,21天连续打卡加21分"
输出:[{{"type":"income","amount":1,"description":"口算"}},{{"type":"expense","amount":4,"description":"买冰激凌"}},{{"type":"income","amount":21,"description":"连续打卡"}}]

输入:"今天孩子做了认真大扫除，加20分"
输出:[{{"type":"income","amount":20,"description":"大扫除"}}]  # ← 去主语(孩子)、形容词(认真)、时间(今天)

输入:"课外语文阅读三篇，加6分"
输出:[{{"type":"income","amount":6,"description":"语文阅读"}}]  # ← 去修饰(课外)、数量(三篇)

输入:"今天连续第二天没有抄作业，扣10分"
输出:[{{"type":"expense","amount":10,"description":"抄作业"}}]  # ← 去时间(今天)、修饰(连续第二天)

用户消息:{message}

⚠️ 直接给 JSON,不要输出思考过程。"""


ENCOURAGE_PROMPT = """你是一个温暖的家长助手。孩子刚完成了积分变动，请给一句简短的鼓励或点评。

当前余额：{balance}分
最近变动：{changes}

要求：
- 一句话，不超过30字
- 正面、温暖、鼓励
- 可以提到具体的学习项目
- 不要说教

只返回一句话，不要引号。

⚠️ 直接给一句鼓励,不要输出思考过程。"""


# ─── 校验层 ─────────────────────────────────────────────────────────────────

class ValidationError(Exception):
    pass


def validate_record_items(raw, trace_id: Optional[str] = None) -> dict:
    """校验 LLM 解析结果。

    支持三种格式：
    - LLM 直接返回 list：[{"type": "...", ...}]
    - LLM 返回包装 dict：{"items": [...]}
    - LLM 返回裸数组元素（逗号分隔，无外层包装）：
      {"type": "income", ...}, {"type": "expense", ...}

    V2-005 (2026-06-12 修): 缺金额项不再抛错,标记 needs_amount 并从
    valid_items 中剔除(不写入 DB),由 caller 在 reply 末尾追加提示。

    V2-007 (2026-06-12 修): 接受 trace_id,自动注入到每条 valid/ref
    项的 ref_id 字段,后续 insert_transactions_batch 会写入
    transactions.ref_id 供审计。

    返回 dict:
    {
        "valid":     [ {type, amount, description, ref_id}, ... ],  # 可写入 DB
        "needs_amount": [ {type, description, raw_item}, ... ],     # 缺金额
    }
    """
    # 解包包装格式
    if isinstance(raw, dict):
        if "items" in raw:
            items = raw["items"]
        else:
            items = [raw]
    elif isinstance(raw, list):
        items = raw
    elif isinstance(raw, str):
        # 裸数组元素格式：{"type":...}, {"type":...}, ...
        try:
            items = json.loads(raw)
        except json.JSONDecodeError:
            try:
                items = json.loads(f"[{raw}]")
            except json.JSONDecodeError:
                raise ValidationError(f"无法解析 LLM 输出：{raw[:100]}")
    else:
        raise ValidationError(f"无法理解的解析结果类型：{type(raw).__name__}")

    if not items:
        raise ValidationError("未解析出任何记账条目")

    if not isinstance(items, list):
        raise ValidationError(f"items 应该是数组，实际：{type(items).__name__}")

    valid = []
    needs_amount = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValidationError(f"第{i+1}条不是有效对象：{type(item).__name__}")
        tx_type = item.get("type")
        if tx_type not in ("income", "expense"):
            raise ValidationError(f"第{i+1}条 type 无效: {tx_type}")

        description = (item.get("description") or "").strip()
        if not description:
            raise ValidationError(f"第{i+1}条缺少描述")

        amount = item.get("amount")

        # V2-005 缺金额：不抛错，收集到 needs_amount 列表
        if amount is None:
            needs_amount.append({
                "type": tx_type,
                "description": description,
                "raw_item": item,
            })
            continue
        # V2-decimal (2026-06-16): 删 V2-008 浮点拦截, 0.5/1.5 直接入账
        if not isinstance(amount, (int, float)):
            raise ValidationError(f"第{i+1}条金额类型错误: {type(amount)}")
        if amount <= 0:
            raise ValidationError(f"第{i+1}条金额必须为正数: {amount}")
        if amount > 9999.99:
            raise ValidationError(f"第{i+1}条金额过大: {amount}")

        # expense 的 amount 在 DB 层存负数, 保留两位小数
        amount_rounded = round(float(amount), 2)
        db_amount = amount_rounded if tx_type == "income" else -amount_rounded

        valid.append({
            "type": tx_type,
            "amount": db_amount,
            "description": description,
            "ref_id": trace_id,  # V2-007: 注入 trace_id 用于审计
        })

    return {"valid": valid, "needs_amount": needs_amount}


# ─── 主流程 ─────────────────────────────────────────────────────────────────

def process_message(
    conn,
    trace_id: str,
    message_text: str,
    *,
    message_id: str = None,
    worker_id: str = "agent",
    llm_call=call_llm,
) -> dict:
    """处理一条消息的完整流水线。

    参数：
        trace_id: 全局唯一追踪 ID（必须），用于入口锁和去重
        message_text: 消息文本内容
        message_id: 平台原生消息 ID（可选，飞书渠道有，其他渠道为 None）
        worker_id: 处理者标识（用于锁日志）
        llm_call: LLM 调用函数（可注入 mock）

    入口锁策略：
        1. 尝试加锁 PROCESSING
        2. 锁存在 → 检查状态：
           - COMPLETED → 直接返回 skipped
           - PROCESSING + TTL 未过期 → 返回 skipped（正在处理）
           - PROCESSING + TTL 过期 → 接管处理
        3. 处理完成 → 释放锁 COMPLETED
        4. 处理失败 → 释放锁 FAILED（包括部分成功需要回滚的情况）

    返回 {"status": "ok"|"skipped"|"error", "reply": "...", ...}
    """
    t_start = time.time()

    # Step 0: 入口锁（第一道防线：防并发）
    acquired = acquire_processing_lock(conn, trace_id, ttl_seconds=60, worker_id=worker_id)
    if not acquired:
        # 锁被占用（已处理完 / 正在处理 / TTL 未过期）
        existing = conn.execute(
            "SELECT status FROM processing_locks WHERE trace_id = ?", (trace_id,)
        ).fetchone()
        status = existing[0] if existing else "UNKNOWN"
        log_audit(conn, step="lock", input_summary=trace_id,
                  output_summary=f"skipped: {status}", success=True,
    trace_id=trace_id,)
        return {"status": "skipped", "reply": "", "skip_reason": f"lock_held_{status}"}

    # Step 0b: 消息入口气息
    log_audit(conn, step="intake", input_summary=message_text[:200],
              output_summary=f"trace_id={trace_id} msg_id={message_id}", success=True,
              trace_id=trace_id)

    # Step 0b1: V2-016 修正/补录/补打/更正 fast path(不调 LLM)
    # 根因 (2026-06-14 Run 4 唯一 error REPLAY-20260614-038):
    #   "昨天ABC Reading +2分（修正）" → LLM classify 看到 "修正"+"昨天" 走 adjust/查账,
    #   查不到 (日期 5/1 vs 6/13) → error "抱歉,没找到" → 用户体验差
    # 跟 V2-008/009 撤销/调账 同款:关键词命中 → 引导重发, 不调 LLM, 0.0s 响应
    # 关键: "修正"业务上是合法操作, 不该拒 (区别于 V2-004 撤销), 引导按 income/expense 重发即可
    _v2_016_keywords = ["修正", "补录", "补打", "更正"]
    _negation_prefixes_v16 = ["不", "别", "没", "未", "无", "不需要"]
    _has_v2_016 = False
    for kw in _v2_016_keywords:
        if kw in message_text:
            kw_pos = message_text.find(kw)
            prefix = message_text[max(0, kw_pos - 5):kw_pos]
            if any(neg in prefix for neg in _negation_prefixes_v16):
                continue
            _has_v2_016 = True
            _matched_kw_v16 = kw
            break
    if _has_v2_016:
        log_audit(conn, step="unsupported_intent", input_summary=message_text[:200],
                  output_summary=f"v2_016_matched={_matched_kw_v16}", success=True,
                  trace_id=trace_id)
        release_processing_lock(conn, trace_id, status=LockStatus.COMPLETED)
        return {
            "status": "ok",
            "reply": (
                f"🤔 看到消息里有「{_matched_kw_v16}」后缀, V2 暂不支持补录修改历史记录。\n\n"
                f"请按 income/expense 形式重发(跟正常记录一样):\n"
                f"  • 加分: <描述> 加 <X> 分(例:ABC Reading 加 2 分)\n"
                f"  • 减分: <描述> 减 <X> 分(例:海苔卷 减 4 分)\n"
                f"  • 多笔: <描述1> 加 <X1> 分, <描述2> 加 <X2> 分\n"
                f"          (例:数学口算 加 1 分, 写字 加 3 分)\n\n"
                f"收到后正常记账, 不区分新旧记录。"
            ),
        }

    # Step 0b2: V2-008/009 撤销/调账 fast path(不调 LLM)
    # 关键词命中 → 提示用户用 income/expense 形式(本质就是调账)
    # 否定词白名单:不/别/没/未/无/不需要 + 关键词 → 放行让 LLM 解析
    _unsupported_kw = ["撤销", "撤回", "取消", "作废", "调账"]
    _negation_prefixes = ["不", "别", "没", "未", "无", "不需要"]
    _has_unsupported = False
    for kw in _unsupported_kw:
        if kw in message_text:
            # 关键词前 5 字内有否定词 → 放行
            kw_pos = message_text.find(kw)
            prefix = message_text[max(0, kw_pos - 5):kw_pos]
            if any(neg in prefix for neg in _negation_prefixes):
                continue
            _has_unsupported = True
            _matched_kw = kw
            break
    if _has_unsupported:
        log_audit(conn, step="unsupported_intent", input_summary=message_text[:200],
                  output_summary=f"matched={_matched_kw}", success=True, trace_id=trace_id)
        release_processing_lock(conn, trace_id, status=LockStatus.COMPLETED)
        return {
            "status": "ok",
            "reply": "⚠️ V2 不支持「撤销/调账」语法。\n\n"
                     "如需调整分数,直接发 income/expense 形式(本质就是调账):\n"
                     "  • 加分: <描述> 加 <X> 分(例:笔误 加 5 分)\n"
                     "  • 减分: <描述> 减 <X> 分(例:上次奖励多了 减 3 分)\n\n"
                     "请明确金额后重发。",
        }

    try:
        # Step 0c: 检查是否有待确认的调账
        pending = get_pending_adjustment(conn)
        if pending:
            result = _handle_adjust_confirm(conn, trace_id, message_id, message_text, pending)
            release_processing_lock(conn, trace_id, status=LockStatus.COMPLETED)
            return result

        # Step 1: trace_id 去重（第二道防线：防 LLM 重试用不同 trace_id）
        if is_message_processed(conn, trace_id, message_id):
            log_audit(conn, step="dedup", input_summary=trace_id,
                      output_summary="duplicate", success=True,
    trace_id=trace_id,)
            release_processing_lock(conn, trace_id, status=LockStatus.COMPLETED)
            return {"status": "skipped", "reply": ""}

        # Step 2: 意图分类
        t0 = time.time()
        try:
            classify_resp = llm_call(CLASSIFY_PROMPT.format(message=message_text))
            intent_data = json.loads(_extract_json(classify_resp))
            intent = intent_data["intent"]
        except Exception as e:
            log_audit(conn, step="classify", input_summary=message_text[:200],
                      output_summary=str(e), duration_ms=int((time.time()-t0)*1000),
                      success=False, error_message=str(e), trace_id=trace_id)
            release_processing_lock(conn, trace_id, status=LockStatus.FAILED)
            return {"status": "error", "reply": "抱歉，我没理解你的意思，能再说一遍吗？"}
        log_audit(conn, step="classify", input_summary=message_text[:200],
                  output_summary=intent, duration_ms=int((time.time()-t0)*1000), success=True, trace_id=trace_id)

        # Step 3: 根据意图分发
        if intent == "record":
            result = _handle_record(conn, trace_id, message_text, llm_call)
        elif intent == "adjust":
            result = _handle_adjust(conn, trace_id, message_text, llm_call)
        elif intent == "query":
            result = _handle_query(conn, trace_id, message_text, llm_call)
        else:
            result = {"status": "error", "reply": f"未知意图: {intent}"}

        # 处理成功 → 释放锁 COMPLETED
        release_processing_lock(conn, trace_id, status=LockStatus.COMPLETED)
        return result

    except Exception as e:
        # 任何未捕获的异常 → 释放锁 FAILED
        release_processing_lock(conn, trace_id, status=LockStatus.FAILED)
        raise


def _handle_record(conn, trace_id: str, message_text: str, llm_call) -> dict:
    """处理记账意图。

    参数：trace_id 用于 mark_message_processed（幂等写）。
    失败时整条消息回滚（原子性）。
    """
    t0 = time.time()

    # Step 3a: LLM 语义解析
    try:
        parse_resp = llm_call(PARSE_RECORD_PROMPT.format(message=message_text))
        raw = _extract_json(parse_resp)
        try:
            items = json.loads(raw)
        except json.JSONDecodeError:
            # 裸数组格式：{"type":...}, {"type":...}  → 补上外层 []
            items = json.loads(f"[{raw}]")
    except Exception as e:
        log_audit(conn, step="parse", input_summary=message_text[:200],
                  output_summary=str(e), duration_ms=int((time.time()-t0)*1000),
                  success=False, error_message=str(e), trace_id=trace_id)
        return {"status": "error", "reply": "抱歉，我没能正确解析积分信息，请重新说一下。"}

    # V2-006 修复 (2026-06-13): LLM 返空 items 时(模糊短消息无法判定 type/amount),
    # 走 needs_amount 引导路径,引导用户补"加/扣几分",不再返 error
    if not items:
        needs_amount_placeholder = [{
            "type": "unknown",
            "description": message_text.strip()[:50],
            "raw_item": {"text": message_text},
        }]
        log_audit(conn, step="parse", input_summary=message_text[:200],
                  output_summary="empty_items: guided to needs_amount",
                  duration_ms=int((time.time()-t0)*1000), success=True, trace_id=trace_id)
        return {
            "status": "ok",
            "reply": (
                f"🤔 没理解「{message_text}」是要加还是扣、要加/扣多少。\n\n"
                f"请说清楚后重发,例如：\n"
                f"  • 加分: <描述> 加 <X> 分(例:汉字抄写 加 2 分)\n"
                f"  • 减分: <描述> 减 <X> 分(例:看动画 减 5 分)\n"
                f"  • 查账: 直接问「今天多少分」"
            ),
            "needs_amount": needs_amount_placeholder,
        }
    log_audit(conn, step="parse", input_summary=message_text[:200],
              output_summary=json.dumps(items, ensure_ascii=False),
              duration_ms=int((time.time()-t0)*1000), success=True, trace_id=trace_id)

    # Step 3b: 代码校验
    t0 = time.time()
    try:
        validation = validate_record_items(items, trace_id=trace_id)
        valid = validation["valid"]
        needs_amount = validation["needs_amount"]
    except ValidationError as e:
        log_audit(conn, step="validate", input_summary=json.dumps(items, ensure_ascii=False),
                  output_summary=str(e), duration_ms=int((time.time()-t0)*1000),
                  success=False, error_message=str(e), trace_id=trace_id)
        return {"status": "error", "reply": f"数据校验失败：{e}"}

    # V2-005: 全部都缺金额(没有 valid) → 视为错误,引导用户补金额
    if not valid:
        missing = "、".join(
            f"{item['description']}({item['type']})" for item in needs_amount
        )
        log_audit(conn, step="validate", input_summary=json.dumps(items, ensure_ascii=False),
                  output_summary=f"all_missing_amount: {missing}", success=False,
                  trace_id=trace_id)
        return {
            "status": "ok",
            "reply": (
                f"已收到，但以下项目没听清金额，没法记账：\n"
                f"📝 {missing}\n\n"
                f"请补充「{needs_amount[0]['description']} X 分/元/块」这样重新说一下。"
            ),
            "needs_amount": needs_amount,
        }

    log_audit(conn, step="validate", input_summary=json.dumps(items, ensure_ascii=False),
              output_summary=f"valid={len(valid)} missing={len(needs_amount)}",
              duration_ms=int((time.time()-t0)*1000), success=True, trace_id=trace_id)

    # Step 3c: SQL 原子写入（全部成功或全部回滚）
    t0 = time.time()
    try:
        results = insert_transactions_batch(conn, valid)
    except Exception as e:
        log_audit(conn, step="write", input_summary=json.dumps(valid, ensure_ascii=False),
                  output_summary=str(e), duration_ms=int((time.time()-t0)*1000),
                  success=False, error_message=str(e), trace_id=trace_id)
        return {"status": "error", "reply": "记账失败，请稍后重试。"}
    log_audit(conn, step="write", input_summary=f"{len(valid)} items",
              output_summary="ok", duration_ms=int((time.time()-t0)*1000), success=True,
              trace_id=trace_id)

    # Step 4: 标记已处理（幂等写，trace_id PRIMARY KEY）
    mark_message_processed(conn, trace_id=trace_id, model_name=LLM_MODEL, agent_version=AGENT_VERSION)
    log_audit(conn, step="mark_processed", input_summary=trace_id,
              output_summary="ok", success=True,
    trace_id=trace_id,)

    # Step 5: 生成回报
    balance = get_current_balance(conn)
    changes_desc = ", ".join(
        f"{'+' if r['amount']>0 else ''}{cents_to_display(r['amount'])} {r['description']}"
        for r in results
    )
    encourage = ""
    t_enc = time.time()
    try:
        encourage = llm_call(ENCOURAGE_PROMPT.format(
            balance=cents_to_display(balance),
            changes=changes_desc,
        )).strip()
        log_audit(conn, step="encourage", input_summary=changes_desc[:100],
                  output_summary=encourage, duration_ms=int((time.time()-t_enc)*1000), success=True, trace_id=trace_id)
    except Exception as e:
        encourage = "继续加油！"
        log_audit(conn, step="encourage", input_summary=changes_desc[:100],
                  output_summary=str(e), duration_ms=int((time.time()-t_enc)*1000),
                  success=False, error_message=str(e))

    reply = f"已记录！{changes_desc}\n当前余额：{cents_to_display(balance)}分"
    if encourage:
        reply += f"\n\n{encourage}"

    # V2-005: 部分项目缺金额 → 记账成功后追加提示,引导用户补金额
    if needs_amount:
        missing = "、".join(
            f"{item['description']}({item['type']})" for item in needs_amount
        )
        reply += (
            f"\n\n⚠️ 另收到但没听清金额,没记账的项目：\n"
            f"📝 {missing}\n"
            f"请补充金额：「{needs_amount[0]['description']} X 分/元/块」"
        )

    return {
        "status": "ok",
        "reply": reply,
        "balance": balance,
        "items": results,
        "needs_amount": needs_amount,  # 透传,供测试断言
    }


ADJUST_PARSE_PROMPT = """你是一个积分记账系统的调账解析器。用户要修正之前记错的记录，请提取关键信息。

用户消息：{message}
今天日期：{today}

请返回 JSON：
{{
    "date_hint": "日期描述，消息未提及时默认"今天"（如"昨天""前天""2024-01-15"）",
    "keyword": "用于匹配原记录的关键词（如'口算''语文'）",
    "new_amount": 新金额（数字，单位是"分"，规则同记账），
    "reasoning": "简短说明你的理解"
}}

规则：
- date_hint 是自然语言日期描述，代码会转换为实际日期
- keyword 是从消息中提取的描述关键词，用于模糊匹配
- new_amount 是修正后的金额，单位是分
- 如果无法确定某个字段，设为 null

示例：
消息："昨天的口算应该是加2分不是1分"
返回：{{"date_hint": "昨天", "keyword": "口算", "new_amount": 2, "reasoning": "把昨天口算的+1分改成+2分"}}

只返回 JSON，不要其他内容。

⚠️ 直接给 JSON,不要输出思考过程。"""


def _handle_adjust(conn, trace_id: str, message_text: str, llm_call) -> dict:
    """处理调账意图：LLM 解析 → 匹配原记录 → 创建 pending → 等待确认。

    参数：trace_id 用于 mark_message_processed（幂等写）。
    """
    t0 = time.time()
    today = datetime.now().strftime("%Y-%m-%d")

    # Step 1: LLM 解析调账请求
    try:
        adjust_resp = llm_call(ADJUST_PARSE_PROMPT.format(message=message_text, today=today))
        adjust_data = json.loads(_extract_json(adjust_resp))
    except Exception as e:
        log_audit(conn, step="adjust_parse", input_summary=message_text[:200],
                  output_summary=str(e), duration_ms=int((time.time()-t0)*1000),
                  success=False, error_message=str(e))
        return {"status": "error", "reply": "抱歉，我没理解你要调整什么，能再说清楚一点吗？比如「昨天的口算应该是加2分不是1分」。"}

    log_audit(conn, step="adjust_parse", input_summary=message_text[:200],
              output_summary=json.dumps(adjust_data, ensure_ascii=False),
              duration_ms=int((time.time()-t0)*1000), success=True, trace_id=trace_id)

    # Step 2: 转换日期（默认今天）
    raw_hint = adjust_data.get("date_hint") or ""
    date_hint = raw_hint if raw_hint not in (None, "") else "今天"
    target_date = _resolve_date_hint(date_hint)
    if not target_date:
        return {"status": "error", "reply": f"抱歉，我没法确定「{date_hint}」是哪天，能说具体日期吗？比如「5月12日」。"}

    # Step 3: 匹配原记录
    keyword = adjust_data.get("keyword", "")
    if not keyword:
        return {"status": "error", "reply": "抱歉，我没找到要调整的项目名称，能说一下是什么项目吗？比如「口算」「语文」。"}

    original = find_transaction_by_description(conn, target_date, keyword)
    if not original:
        log_audit(conn, step="adjust_match", input_summary=f"{target_date}/{keyword}",
                  output_summary="not_found", success=False,
    trace_id=trace_id,)
        return {"status": "error", "reply": f"抱歉，在 {target_date} 没有找到和「{keyword}」相关的记录。要不你先查一下？"}

    log_audit(conn, step="adjust_match", input_summary=f"{target_date}/{keyword}",
              output_summary=json.dumps({"id": original["id"], "amount": original["amount"], "description": original["description"]}, ensure_ascii=False),
              success=True, trace_id=trace_id)

    # Step 4: 校验新金额
    new_amount = adjust_data.get("new_amount")
    if new_amount is None:
        return {"status": "error", "reply": "抱歉，我没听清要改成多少分，能再说一下吗？"}
    if not isinstance(new_amount, (int, float)) or new_amount <= 0:
        return {"status": "error", "reply": f"金额格式不对：{new_amount}"}

    old_amount = abs(original["amount"])  # DB 里 expense 存负数，展示用绝对值

    # Step 5: 创建 pending adjustment
    pending = create_pending_adjustment(
        conn,
        message_id=trace_id,  # 用 trace_id 代替 message_id
        target_tx_id=original["id"],
        target_description=original["description"],
        old_amount=old_amount,
        new_amount=round(float(new_amount), 2),
    )

    reply = (
        f"找到 {target_date} 的记录：\n"
        f"📌 {original['description']} {'+' if original['amount']>0 else ''}{cents_to_display(old_amount)}分\n\n"
        f"要改成 {'+' if new_amount>0 else ''}{cents_to_display(round(float(new_amount), 2))}分吗？\n"
        f"回复「确认」执行，回复「取消」放弃。"
    )

    return {"status": "ok", "reply": reply, "pending_id": pending["id"]}


def _handle_adjust_confirm(conn, trace_id: str, message_id: str, message_text: str, pending: dict) -> dict:
    """处理调账确认/取消消息。

    参数：trace_id 用于 mark_message_processed（幂等写）。
    message_id 用于调账确认后的标记。
    """
    text = message_text.strip().lower()

    # 判断确认还是取消
    confirm_keywords = ["确认", "对", "是", "好", "行", "可以", "yes", "ok", "y", "对的", "是的"]
    cancel_keywords = ["取消", "不", "否", "算了", "no", "n", "不要", "别"]

    is_confirm = any(kw in text for kw in confirm_keywords)
    is_cancel = any(kw in text for kw in cancel_keywords)

    if is_cancel and not is_confirm:
        cancel_pending_adjustment(conn, pending["id"])
        mark_message_processed(conn, trace_id=trace_id, model_name=LLM_MODEL, agent_version=AGENT_VERSION)
        log_audit(conn, step="mark_processed", input_summary=trace_id,
                  output_summary="ok", success=True,
    trace_id=trace_id,)
        log_audit(conn, step="adjust_cancel", input_summary=pending["id"],
                  output_summary=f"cancelled: {pending['target_description']} {cents_to_display(pending['old_amount'])}→{cents_to_display(pending['new_amount'])}",
                  success=True, trace_id=trace_id)
        return {"status": "ok", "reply": "已取消调账。"}

    if not is_confirm:
        return {"status": "error", "reply": "请回复「确认」执行调账，或「取消」放弃。"}

    # 确认：追加 adjustment 记录
    diff = pending["new_amount"] - pending["old_amount"]
    tx_type = "adjustment"

    result = insert_transaction(
        conn,
        tx_type=tx_type,
        amount=diff,
        description=f"调账：{pending['target_description']} {cents_to_display(pending['old_amount'])}→{cents_to_display(pending['new_amount'])}分",
        ref_id=pending["target_tx_id"],
    )

    confirm_pending_adjustment(conn, pending["id"])
    mark_message_processed(conn, trace_id=trace_id, model_name=LLM_MODEL, agent_version=AGENT_VERSION)
    log_audit(conn, step="mark_processed", input_summary=trace_id,
              output_summary="ok", success=True,
    trace_id=trace_id,)
    log_audit(conn, step="adjust_confirm", input_summary=pending["id"],
              output_summary=f"confirmed: diff={cents_to_display(diff)}, new_tx={result['id']}",
              success=True, trace_id=trace_id)

    balance = get_current_balance(conn)
    reply = (
        f"已调整！{pending['target_description']} "
        f"{cents_to_display(pending['old_amount'])}→{cents_to_display(pending['new_amount'])}分\n"
        f"当前余额：{cents_to_display(balance)}分"
    )

    return {"status": "ok", "reply": reply, "adjustment": result}


def _resolve_date_hint(date_hint: str) -> Optional[str]:
    """将自然语言日期描述转换为 YYYY-MM-DD 格式。"""
    from datetime import timedelta

    today = datetime.now().date()

    if not date_hint:
        return None
    hint = date_hint.strip()
    if hint in ("今天", "今日"):
        return today.isoformat()
    elif hint in ("昨天", "昨日"):
        return (today - timedelta(days=1)).isoformat()
    elif hint in ("前天",):
        return (today - timedelta(days=2)).isoformat()
    elif hint in ("大前天",):
        return (today - timedelta(days=3)).isoformat()

    # 尝试解析 YYYY-MM-DD 或 MM-DD
    for fmt in ("%Y-%m-%d", "%m-%d", "%m月%d日", "%m月%d号"):
        try:
            d = datetime.strptime(hint, fmt)
            if d.year == 1900:
                d = d.replace(year=today.year)
            return d.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def _handle_query(conn, trace_id: str, message_text: str, llm_call) -> dict:
    """处理查账意图。

    分两种模式：
    1. 简单查询 — 确定性代码直接算（余额、今日、本周）
    2. 语义查询 — LLM 拼 SQL 执行
    """
    t0 = time.time()

    # Step 1: LLM 判断查询类型并生成 SQL
    query_prompt = QUERY_PROMPT.format(
        message=message_text,
        today=datetime.now().strftime("%Y-%m-%d"),
    )

    try:
        query_resp = llm_call(query_prompt)
        query_data = json.loads(query_resp.strip())
    except Exception as e:
        log_audit(conn, step="query_parse", input_summary=message_text[:200],
                  output_summary=str(e), duration_ms=int((time.time()-t0)*1000),
                  success=False, error_message=str(e))
        return {"status": "error", "reply": "抱歉，我没理解你的查询，能换个方式问吗？"}

    query_type = query_data.get("type", "unknown")
    log_audit(conn, step="query_parse", input_summary=message_text[:200],
              output_summary=json.dumps(query_data, ensure_ascii=False),
              duration_ms=int((time.time()-t0)*1000), success=True, trace_id=trace_id)

    # Step 2: 执行查询
    t0 = time.time()
    try:
        if query_type == "simple":
            result = _execute_simple_query(conn, query_data)
        elif query_type == "semantic":
            result = _execute_semantic_query(conn, query_data)
        else:
            return {"status": "error", "reply": "抱歉，我不支持这种查询方式。"}
    except Exception as e:
        log_audit(conn, step="query_execute",
                  input_summary=json.dumps(query_data, ensure_ascii=False),
                  output_summary=str(e), duration_ms=int((time.time()-t0)*1000),
                  success=False, error_message=str(e), trace_id=trace_id)
        return {"status": "error", "reply": f"查询执行失败：{e}"}

    log_audit(conn, step="query_execute",
              input_summary=json.dumps(query_data, ensure_ascii=False),
              output_summary="ok", duration_ms=int((time.time()-t0)*1000), success=True,
              trace_id=trace_id)

    # Step 3: 格式化回报
    reply = _format_query_reply(query_data, result)
    return {"status": "ok", "reply": reply, "data": result}


QUERY_PROMPT = """你是一个积分记账系统的查询解析器。分析用户消息，生成查询计划。

用户消息：{message}
今天日期：{today}

请返回 JSON：
{{
    "type": "simple" 或 "semantic",
    "intent": "balance" | "today" | "week" | "month" | "category" | "custom",
    "sql": "SQL 查询语句（仅 semantic 类型需要）",
    "params": {{}},
    "display_hint": "如何展示结果的提示"
}}

规则：
- simple：标准查询（查余额/今日/本周/本月），不需要 SQL，代码会处理
  - intent="balance" → 查当前余额
  - intent="today" → 查今日收支
  - intent="week" → 查本周收支
  - intent="month" → 查本月收支蛐
- semantic：自定义查询，需要生成 SQL
  - 表名：transactions
  - 列：id, created_at, type, amount, balance_after, description
  - amount 单位是分，展示时除以 100
  - 只生成 SELECT 语句
  - 示例："口算一共加了多少" →
    SELECT SUM(amount) as total FROM transactions WHERE type='income' AND description LIKE '%口算%'

只返回 JSON，不要其他内容。

⚠️ 直接给 JSON,不要输出思考过程。"""


def _execute_simple_query(conn, query_data: dict) -> dict:
    """执行简单查询（确定性代码）。"""
    intent = query_data.get("intent", "balance")
    today = datetime.now().strftime("%Y-%m-%d")

    if intent == "balance":
        balance = get_current_balance(conn)
        return {
            "type": "balance",
            "balance": balance,
            "display": f"当前余额：{cents_to_display(balance)}分",
        }

    elif intent == "today":
        rows = conn.execute(
            """SELECT type, SUM(amount) as total, COUNT(*) as count
               FROM transactions
               WHERE date(created_at) = ?
               GROUP BY type""",
            (today,),
        ).fetchall()
        income_total = 0
        expense_total = 0
        for row in rows:
            if row[0] == "income":
                income_total = row[1] or 0
            elif row[0] == "expense":
                expense_total = row[1] or 0

        return {
            "type": "today",
            "date": today,
            "income": income_total,
            "expense": expense_total,
            "net": income_total + expense_total,
            "display": (
                f"今日（{today}）\n"
                f"收入：+{cents_to_display(income_total)}分\n"
                f"支出：{cents_to_display(abs(expense_total))}分\n"
                f"净变动：{'+' if income_total+expense_total >= 0 else ''}{cents_to_display(income_total+expense_total)}分"
            ),
        }

    elif intent == "week":
        rows = conn.execute(
            """SELECT type, SUM(amount) as total
               FROM transactions
               WHERE date(created_at) >= date(?, '-6 days')
               GROUP BY type""",
            (today,),
        ).fetchall()
        income_total = 0
        expense_total = 0
        for row in rows:
            if row[0] == "income":
                income_total = row[1] or 0
            elif row[0] == "expense":
                expense_total = row[1] or 0

        return {
            "type": "week",
            "income": income_total,
            "expense": expense_total,
            "net": income_total + expense_total,
            "display": (
                f"本周（近7天）\n"
                f"收入：+{cents_to_display(income_total)}分\n"
                f"支出：{cents_to_display(abs(expense_total))}分\n"
                f"净变动：{'+' if income_total+expense_total >= 0 else ''}{cents_to_display(income_total+expense_total)}分"
            ),
        }

    elif intent == "month":
        month_start = today[:8] + "01"
        rows = conn.execute(
            """SELECT type, SUM(amount) as total
               FROM transactions
               WHERE date(created_at) >= ?
               GROUP BY type""",
            (month_start,),
        ).fetchall()
        income_total = 0
        expense_total = 0
        for row in rows:
            if row[0] == "income":
                income_total = row[1] or 0
            elif row[0] == "expense":
                expense_total = row[1] or 0

        return {
            "type": "month",
            "month": today[:7],
            "income": income_total,
            "expense": expense_total,
            "net": income_total + expense_total,
            "display": (
                f"本月（{today[:7]}）\n"
                f"收入：+{cents_to_display(income_total)}分\n"
                f"支出：{cents_to_display(abs(expense_total))}分\n"
                f"净变动：{'+' if income_total+expense_total >= 0 else ''}{cents_to_display(income_total+expense_total)}分"
            ),
        }

    return {"type": "unknown", "display": "未知查询类型"}


def _execute_semantic_query(conn, query_data: dict) -> dict:
    """执行语义查询（LLM 生成的 SQL）。"""
    from .db import execute_query

    sql = query_data.get("sql", "")
    if not sql:
        raise ValueError("semantic 查询缺少 SQL")

    # 安全检查：只允许 SELECT
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        raise ValueError(f"不允许的 SQL 操作：{sql[:50]}")

    rows = execute_query(conn, sql)

    # 尝试格式化金额列
    formatted_rows = []
    for row in rows:
        formatted = {}
        for k, v in row.items():
            if k in ("amount", "balance_after", "total", "sum") and isinstance(v, (int, float)):
                formatted[k] = cents_to_display(int(v))
            else:
                formatted[k] = v
        formatted_rows.append(formatted)

    return {
        "type": "semantic",
        "sql": sql,
        "rows": formatted_rows,
        "count": len(formatted_rows),
    }


def _format_query_reply(query_data: dict, result: dict) -> str:
    """格式化查询结果为可读文本。"""
    if result.get("type") in ("balance", "today", "week", "month"):
        return result.get("display", "")

    if result.get("type") == "semantic":
        rows = result.get("rows", [])
        if not rows:
            return "没有找到相关记录。"

        # 简单结果：单行单值
        if len(rows) == 1 and len(rows[0]) == 1:
            val = list(rows[0].values())[0]
            return f"{val}"

        # 多行结果：列表展示
        lines = [f"找到 {len(rows)} 条记录：", ""]
        for i, row in enumerate(rows[:20], 1):  # 最多显示 20 条
            parts = []
            for k, v in row.items():
                if k == "description":
                    parts.append(str(v))
                elif k in ("amount", "total", "sum"):
                    parts.append(f"{v}分")
                else:
                    parts.append(str(v))
            lines.append(f"{i}. {' | '.join(parts)}")

        if len(rows) > 20:
            lines.append(f"...还有 {len(rows)-20} 条")

        return "\n".join(lines)

    return str(result)
