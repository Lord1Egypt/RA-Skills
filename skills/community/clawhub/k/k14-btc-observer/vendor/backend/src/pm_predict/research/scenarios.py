"""Build and run labeled synthetic end-to-end cases; no market-data fetching."""
from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
from pm_predict.strategy.indicators import Bar
from pm_predict.research.replay import replay

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = ROOT / "data/demo_output"
TH = json.loads((ROOT / "config/thresholds_2026-10.json").read_text("utf-8"))
START = 1792800000
MS = START * 1000


class Scenario:
    def __init__(self):
        self.events, self.seq = [], 0

    def add(self, method, **args):
        self.events.append({"event_id": f"E{len(self.events)+1:04d}", "method": method, "args": args})

    def start(self):
        self.add("open_window", market="BTC", start=START,
                 bars=[asdict(Bar(START - (14-i)*900, 110, 100, 100)) for i in range(14)],
                 thresholds=TH, ptb=100, rule_verified=True, ptb_source="CHAINLINK_TWAP60_AT_START")
        self.refresh(0)
        self.add("step", market="BTC", now=MS)
        self.add("ack", order="P0001", now=MS+1)

    def refresh(self, offset, opposite=".70"):
        self.seq += 1
        for side, bid, ask in (("Up", ".46", ".49"), ("Down", ".20", opposite)):
            self.add("book", market="BTC", side=side, seq=self.seq, source_ms=MS+offset,
                     receive_ms=MS+offset, bid=bid, asks=[[ask, "10"]])
        self.add("price", market="BTC", spot=100, sigma=.001, source_ms=MS+offset, receive_ms=MS+offset)
        self.add("health", market="BTC", now=MS+offset, connected=True, reconciled=True)

    def entry_fill(self, qty="5"):
        self.add("fill", fill_id="entry", order="P0001", qty=qty, price=".47", now=MS+2, synthetic=True)
        self.add("confirm", fill_id="entry", now=MS+3)

    def hedge(self):
        self.refresh(10, ".45")
        self.add("step", market="BTC", now=MS+10)
        self.add("fill", fill_id="hedge", order="P0002", qty="5", price=".45", fee_usd=".08663", now=MS+11, synthetic=True)
        self.add("confirm", fill_id="hedge", now=MS+12)
        self.add("step", market="BTC", now=MS+13)


def scenarios():
    s = Scenario(); s.start(); s.entry_fill(); s.hedge()
    s.add("chain_result", market="BTC", now=MS+14, success=True, operation="MERGE")
    # Duplicate delivery of the exact chain receipt must not credit cash twice.
    s.events.append(deepcopy(s.events[-1]))
    yield "paired_merge", "双边配齐后合并（含重复回执）", s.events, "60.31337"

    s = Scenario(); s.start(); s.entry_fill("2")
    s.refresh(120000); s.add("step", market="BTC", now=MS+120000)
    s.add("cancel_ack", order="P0001", now=MS+120010)
    s.add("fill", fill_id="late", order="P0001", qty="1", price=".47", now=MS+120020, synthetic=True)
    s.add("confirm", fill_id="late", now=MS+120030)
    s.add("reconcile", order="P0001", now=MS+120040, final_filled="3")
    s.add("settle", market="BTC", winner="Down", now=MS+900000)
    s.add("chain_result", market="BTC", now=MS+900001, success=True, operation="REDEEM")
    yield "partial_late_fill_loss", "只成交两份，撤单后又来一份，最终单边亏损", s.events, "58.59"

    s = Scenario(); s.start(); s.entry_fill(); s.hedge()
    s.add("chain_result", market="BTC", now=MS+14, success=False, operation="MERGE")
    s.add("settle", market="BTC", winner="Down", now=MS+900000)
    s.add("chain_result", market="BTC", now=MS+900001, success=True, operation="REDEEM")
    yield "merge_failed_redeem", "合并失败，保留双边至结算兑付", s.events, "60.31337"

    s = Scenario(); s.start()
    s.refresh(120000); s.add("step", market="BTC", now=MS+120000)
    s.add("cancel_ack", order="P0001", now=MS+120001)
    s.add("reconcile", order="P0001", now=MS+120002, final_filled="0")
    s.add("settle", market="BTC", winner="Up", now=MS+900000)
    s.add("chain_result", market="BTC", now=MS+900001, success=True, operation="REDEEM")
    yield "unfilled", "挂单未成交，到时撤单并释放资金", s.events, "60"

    s = Scenario(); s.start(); s.add("step", market="BTC", now=MS+2001)
    yield "feed_gap", "行情中断，发出撤单意图并保留资金占用", s.events, "60"


def main():
    out = OUT / "synthetic_replays"
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for name, title, events, expected in scenarios():
        e, result = replay(events)
        assert result["cash"] == expected
        e2, r2 = replay(events)
        assert e.journal == e2.journal
        assert e.intents == e2.intents
        assert {k:v for k,v in result.items() if k != "local_replay_handler_ns"} == {
            k:v for k,v in r2.items() if k != "local_replay_handler_ns"}
        (out / f"{name}.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False)+"\n" for x in events), "utf-8")
        (out / f"{name}_journal.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False)+"\n" for x in e.journal), "utf-8")
        results.append({"id": name, "title": title, "replay_identical": True, **result})
    (OUT / "demo_results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2), "utf-8")
    print(json.dumps([{"case": r["title"], "cash": r["cash"], "synthetic_pnl": r["realized_synthetic_pnl"],
                       "deterministic_replay": r["replay_identical"]} for r in results], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
