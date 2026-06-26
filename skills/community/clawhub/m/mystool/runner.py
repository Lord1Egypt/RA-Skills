#!/usr/bin/env python3
"""
mystool cron runner — 供 OpenClaw cron 定时调用

用法:
  python runner.py tasks              # 执行所有用户的每日米游币任务
  python runner.py sign               # 执行所有用户的游戏签到
  python runner.py exchange <goods_id> [user_id]  # 兑换商品（可指定用户）
  python runner.py schedule           # 检查并执行到期的预约抢购

日志:
  执行记录保存到 log/ 文件夹，文件名格式：YYYY-MM-DD_HH-MM-SS.log
"""

import asyncio
import json
import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from plugin import (
    run_daily_tasks_all, 
    run_sign_all, 
    cmd_exchange,
    get_user_accounts,
    get_address_list,
    do_exchange,
    get_good_detail,
    _load_exchange_schedules,
    _save_exchange_schedules,
    GAME_BIZ,
)


def write_log(mode: str, content: str):
    """写入日志文件"""
    log_dir = Path(__file__).parent / "log"
    log_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = log_dir / f"{timestamp}_{mode}.log"
    
    header = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] mystool {mode}\n"
    separator = "=" * 50 + "\n"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(header)
        f.write(separator)
        f.write(content)
        f.write("\n")
    
    return log_file


async def run_exchange(goods_id: str, user_id: str = None, max_retries: int = 10) -> str:
    """
    执行商品兑换（带重试机制）
    
    :param goods_id: 商品ID
    :param user_id: 用户ID（可选，不指定则对所有用户执行）
    :param max_retries: 最大重试次数
    :return: 执行结果
    """
    results = []
    
    # 获取要执行的用户列表
    if user_id:
        user_ids = [user_id]
    else:
        from plugin import get_all_user_ids
        user_ids = get_all_user_ids()
    
    if not user_ids:
        return "⚠️ 没有绑定账号的用户"
    
    for uid in user_ids:
        accounts = get_user_accounts(uid)
        if not accounts:
            continue
        
        acc = accounts[0]
        cookies = acc["cookies"]
        nickname = acc.get("nickname", acc["uid"])
        games = acc.get("games", [])
        
        if not games:
            results.append(f"❌ [{nickname}] 未找到游戏账号信息")
            continue
        
        g = games[0]
        game_biz = g.get("game_biz", "hk4e_cn")
        game_uid = g.get("game_uid", "")
        region = g.get("region", "cn_gf01")
        
        # 获取地址
        ok_addr, addresses = await get_address_list(cookies)
        address_id = None
        if ok_addr and addresses:
            for addr in addresses:
                if addr.get("is_default"):
                    address_id = addr.get("id")
                    break
            if not address_id and addresses:
                address_id = addresses[0].get("id")
        
        # 获取商品信息
        ok_detail, detail = await get_good_detail(goods_id)
        goods_name = detail.get("name") or detail.get("goods_name", goods_id) if ok_detail else goods_id
        
        results.append(f"🛒 [{nickname}] 开始抢购: {goods_name}")
        
        # 重试机制
        for attempt in range(max_retries):
            ok, msg, next_time = await do_exchange(
                cookies=cookies,
                goods_id=goods_id,
                uid=game_uid,
                region=region,
                game_biz=game_biz,
                address_id=address_id,
            )
            
            if ok:
                results.append(f"✅ [{nickname}] {msg}")
                break
            elif "库存不足" in msg:
                # 库存不足，等待后重试
                if attempt < max_retries - 1:
                    results.append(f"⏳ [{nickname}] 第{attempt+1}次尝试: {msg}，等待重试...")
                    await asyncio.sleep(0.5)
                else:
                    results.append(f"❌ [{nickname}] 重试{max_retries}次后仍库存不足")
            else:
                # 其他错误，不重试
                results.append(f"❌ [{nickname}] {msg}")
                break
    
    return "\n".join(results)


async def run_scheduled_exchanges() -> str:
    """
    检查并执行到期的预约抢购
    删除已过期的预约
    """
    schedules = _load_exchange_schedules()
    now = time.time()
    
    results = []
    executed_count = 0
    expired_count = 0
    
    for user_id, user_schedules in list(schedules.items()):
        for schedule in list(user_schedules):
            next_time = schedule.get("next_time", 0)
            goods_id = schedule.get("goods_id", "")
            goods_name = schedule.get("goods_name", goods_id)
            
            # 已过期（超过开抢时间1小时）
            if next_time > 0 and now > next_time + 3600:
                user_schedules.remove(schedule)
                expired_count += 1
                results.append(f"🗑️ 已过期: {goods_name} (用户 {user_id})")
                continue
            
            # 到期执行
            if next_time > 0 and now >= next_time:
                result = await run_exchange(goods_id, user_id, max_retries=10)
                results.append(result)
                executed_count += 1
                
                # 执行后从预约列表移除
                user_schedules.remove(schedule)
    
    # 保存更新后的预约列表
    _save_exchange_schedules(schedules)
    
    if executed_count == 0 and expired_count == 0:
        return "✅ 没有需要执行的预约抢购"
    
    summary = f"📊 预约抢购执行完成：执行 {executed_count} 个，清理过期 {expired_count} 个"
    return "\n".join(results) + f"\n\n{summary}"


async def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "tasks"

    if mode == "tasks":
        result = await run_daily_tasks_all()
        print(result)
        log_file = write_log("tasks", result)
        print(f"\n[日志已保存] {log_file}")
    elif mode == "sign":
        result = await run_sign_all()
        print(result)
        log_file = write_log("sign", result)
        print(f"\n[日志已保存] {log_file}")
    elif mode == "exchange":
        if len(sys.argv) < 3:
            print("用法: python runner.py exchange <goods_id> [user_id]")
            sys.exit(1)
        goods_id = sys.argv[2]
        user_id = sys.argv[3] if len(sys.argv) > 3 else None
        result = await run_exchange(goods_id, user_id)
        print(result)
        log_file = write_log(f"exchange_{goods_id}", result)
        print(f"\n[日志已保存] {log_file}")
    elif mode == "schedule":
        result = await run_scheduled_exchanges()
        print(result)
        log_file = write_log("schedule", result)
        print(f"\n[日志已保存] {log_file}")
    else:
        print(f"未知模式: {mode}，支持 tasks / sign / exchange / schedule")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
