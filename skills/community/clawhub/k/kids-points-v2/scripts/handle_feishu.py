"""kids-points-v2 skill handler.

V2 入口 (2026-06-20 老王拍板升级):
- 接收 OpenClaw 传入的飞书消息 context
- 群聊 + 单聊 全量响应 (chatType == group/topic_group/p2p/private 都接)
- subprocess 调 V2 cli.py, 返 reply 字符串给 OpenClaw
- 空消息 → return None

硬约束: V2 不动 V1 数据 (V1 已封存为 kids-points.disabled-20260620, 不会再跑)。
"""
import sys
import os
import subprocess
from pathlib import Path

# V2 runtime 路径解析（优先级）:
#   1. 环境变量 KIDS_POINTS_RUNTIME_DIR  （推荐：本地生产可指向原路径，发布版可指向 skill 内嵌 runtime）
#   2. 默认 fallback: skill 包内的 runtime/ 目录（ClawHub 安装后的标准位置）
#
# 这样：
#   - 本地 ~/.openclaw/openclaw.json 设 KIDS_POINTS_RUNTIME_DIR 指向原生产路径，零干扰
#   - 其他用户 ClawHub install 后不设 env，自动用 skill 内嵌 runtime，开箱即用
#   - 高级用户可以用 env 指向任意自定义路径
V2_RUNTIME_DIR = os.environ.get(
    "KIDS_POINTS_RUNTIME_DIR",
    str(Path(__file__).parent.parent / "runtime")
)


def handle_feishu_message(context):
    """
    V2 skill entry point (被 OpenClaw 平台自动 dispatch).
    
    Args:
        context: dict, OpenClaw skill context, 关键字段:
            - message (str): 飞书消息文本
            - messageId (str): 飞书消息 ID (dedup 用)
            - chatType (str): 'p2p' / 'private' / 'group' / 'topic_group'
            - senderId, senderOpenId, chatId, ... (其他 OpenClaw 字段)
    
    Returns:
        str: V2 reply 文本 (OpenClaw 会发回飞书)
        None: 不响应 (OpenClaw 看 None 跳过)
    """
    # ── Gate 1: 文本消息必须有内容 ─────────────────────────────────
    # 2026-06-20 老王拍板: V2 全量接管 (群聊 + 单聊), 不再按 chat_type 分流
    message = (context.get("message") or "").strip()
    if not message:
        return None  # 纯图片/语音/附件 → 当前 V2 不处理
    
    # ── 调 V2 cli.py 单条消息模式 ───────────────────────────────────
    # cli.py 走 process_message → 8 步 pipeline → 写 V2 SQLite → 返 result["reply"]
    # V2 的 dedup 走 trace_id, 单进程内 random hex 已足够
    try:
        result = subprocess.run(
            ["python3", "cli.py", message],
            cwd=V2_RUNTIME_DIR,
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ},  # 继承 ~/.hermes/.env (LLM API key) 等
        )
    except subprocess.TimeoutExpired:
        return "⚠️ V2 处理超时 (30s), 请重试"
    except FileNotFoundError:
        return f"⚠️ V2 路径找不到: {V2_RUNTIME_DIR}"
    except Exception as e:
        return f"⚠️ V2 调用失败: {type(e).__name__}: {e}"
    
    # ── 解析 V2 输出 ───────────────────────────────────────────────
    if result.returncode != 0:
        # V2 返非 0 (db error / invalid args / exception)
        err_msg = (result.stderr or result.stdout or "").strip() or "未知错误"
        return f"⚠️ V2 错误 (rc={result.returncode}): {err_msg[:300]}"
    
    reply = result.stdout.strip()
    return reply if reply else "✅ V2 已处理 (无返回内容)"


# ── 独立测试入口 (不走 OpenClaw) ────────────────────────────────────────
# 2026-06-23 BUG-V2-016: 加 --test gate, 防 LLM/手动误调触发测试模式污染生产库
# 必须显式 `python3 handle_feishu.py --test` 才跑, 默认 print 帮助信息
if __name__ == "__main__":
    if "--test" not in sys.argv:
        print("handle_feishu.py - V2 skill handler")
        print()
        print("用法:")
        print("  1. 生产: OpenClaw 平台自动 dispatch, 传 context dict")
        print("  2. 手动单条: cd <V2_RUNTIME_DIR> && python3 cli.py \"<消息>\"")
        print("  3. 开发测试: python3 handle_feishu.py --test  (会真实写库!)")
        sys.exit(0)

    print("=" * 60)
    print("V2 skill handler 独立测试  ⚠️ 会真实写库")
    print("=" * 60)
    
    # Test 1: p2p 加 1 分
    print("\n[Test 1] p2p 加 1 分:")
    r1 = handle_feishu_message({"message": "测试加 1 分", "chatType": "p2p", "messageId": "v2-skill-test-1"})
    print(f"  → {r1}")
    
    # Test 2: p2p 查余额
    print("\n[Test 2] p2p 查余额:")
    r2 = handle_feishu_message({"message": "现在多少分", "chatType": "p2p", "messageId": "v2-skill-test-2"})
    print(f"  → {r2}")
    
    # Test 3: group 群聊也应响应 (V2 全量生产)
    print("\n[Test 3] group 群聊 (V2 全量):")
    r3 = handle_feishu_message({"message": "数学加 1 分", "chatType": "group", "messageId": "v2-skill-test-3"})
    print(f"  → {r3}")

    # Test 4: 没传 chatType → 也响应 (V2 全量, 无 chat_type gate)
    print("\n[Test 4] 无 chatType → 也响应:")
    r4 = handle_feishu_message({"message": "测试", "messageId": "v2-skill-test-4"})
    print(f"  → {r4}")

    # Test 5: 空 message → return None
    print("\n[Test 5] 空 message → 应 return None:")
    r5 = handle_feishu_message({"message": "", "chatType": "p2p", "messageId": "v2-skill-test-5"})
    print(f"  → {r5} (期望 None)")
    
    # Test 6: 浮点边界 (V2-015 覆盖)
    print("\n[Test 6] 浮点边界 (扣 0.5 分):")
    r6 = handle_feishu_message({"message": "买甘蔗扣 0.5 分", "chatType": "p2p", "messageId": "v2-skill-test-6"})
    print(f"  → {r6}")
    
    # Test 7: 模糊短消息 (V2-006 模式)
    print("\n[Test 7] 模糊短消息 (今天 ABC Reading):")
    r7 = handle_feishu_message({"message": "今天 ABC Reading", "chatType": "p2p", "messageId": "v2-skill-test-7"})
    print(f"  → {r7}")
    
    print("\n" + "=" * 60)
    print("独立测试完成")
    print("=" * 60)
