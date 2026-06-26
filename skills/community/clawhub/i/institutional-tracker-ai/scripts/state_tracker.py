"""
状态追踪模块 - 连续性确认逻辑
信号需要连续2-3天才确认为有效信号，减少单日噪音
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

from config import SCORES_DIR, CONFIRM_DAYS


class StateTracker:
    """追踪每只股票的状态历史，实现连续确认"""

    def __init__(self):
        self.history_file = SCORES_DIR / "state_history.json"
        self.history = self._load()

    def _load(self) -> Dict:
        """加载历史状态"""
        if self.history_file.exists():
            try:
                return json.loads(self.history_file.read_text(encoding="utf-8"))
            except:
                pass
        return {}

    def _save(self):
        """保存状态历史"""
        self.history_file.write_text(
            json.dumps(self.history, ensure_ascii=False, indent=2), encoding="utf-8")

    def update(self, code: str, date: str, state: str, score: float) -> Dict:
        """
        更新股票状态并返回确认结果
        
        返回:
            {
                "confirmed_state": 确认后的状态,
                "raw_state": 今天的原始状态,
                "consecutive_days": 连续几天处于该状态,
                "is_new_signal": 是否是新触发的信号（状态刚转换且已确认）,
                "prev_state": 上一次确认的状态
            }
        """
        if code not in self.history:
            self.history[code] = {
                "confirmed_state": "NEUTRAL",
                "raw_history": [],  # 最近N天的原始状态
            }

        h = self.history[code]
        prev_confirmed = h["confirmed_state"]

        # 添加今天的记录
        h["raw_history"].insert(0, {"date": date, "state": state, "score": score})
        # 只保留最近10天
        h["raw_history"] = h["raw_history"][:10]

        # 计算连续天数
        consecutive = 0
        for record in h["raw_history"]:
            if record["state"] == state:
                consecutive += 1
            else:
                break

        # 连续确认逻辑
        is_new_signal = False
        if state in ["ACCUMULATION", "DISTRIBUTION"]:
            # 买入/卖出信号需要连续2天确认
            if consecutive >= CONFIRM_DAYS:
                if prev_confirmed != state:
                    is_new_signal = True  # 新信号!
                h["confirmed_state"] = state
            # 不够天数则保持之前状态
        elif state == "MARKUP":
            # 拉升期只需1天（已经在涨了）
            if prev_confirmed != state:
                is_new_signal = True
            h["confirmed_state"] = state
        else:
            # 观望/洗盘 1天就确认
            h["confirmed_state"] = state

        self._save()

        return {
            "confirmed_state": h["confirmed_state"],
            "raw_state": state,
            "consecutive_days": consecutive,
            "is_new_signal": is_new_signal,
            "prev_state": prev_confirmed,
        }

    def get_new_signals(self) -> List[Dict]:
        """获取所有新触发的信号（用于推送提醒）"""
        signals = []
        for code, h in self.history.items():
            if h["raw_history"]:
                latest = h["raw_history"][0]
                # 检查是否刚确认
                state = h["confirmed_state"]
                if state in ["ACCUMULATION", "DISTRIBUTION"]:
                    consec = sum(1 for r in h["raw_history"] if r["state"] == state)
                    if consec == CONFIRM_DAYS:  # 正好在确认天数时触发
                        signals.append({
                            "code": code,
                            "state": state,
                            "score": latest["score"],
                            "date": latest["date"],
                        })
        return signals

    def get_stock_history(self, code: str) -> Optional[Dict]:
        """获取某只股票的状态历史"""
        return self.history.get(code)
