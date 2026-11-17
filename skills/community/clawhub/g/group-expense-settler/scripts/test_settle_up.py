#!/usr/bin/env python3
"""Self-test for settle_up.py."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from settle_up import parse_ledger, split_cents, compute_nets, min_cash_flow, parse_amount

LEDGER = """\
Ana,450,Ana Ben Cho Dan
Ben,120,Ben Cho
Cho,80,Ana Ben Cho Dan
Dan,60,Ben Cho Dan
"""


def test_parse_amount():
    assert parse_amount("$100") == 10000
    assert parse_amount("33.33") == 3333
    assert parse_amount("0.01") == 1
    print("ok parse_amount")


def test_split_exact():
    sh = split_cents(10000, ["A", "B", "C"], {})
    assert sum(sh.values()) == 10000 and sh == {"A": 3334, "B": 3333, "C": 3333}
    sh2 = split_cents(10000, ["A", "B"], {"A": 3, "B": 1})
    assert sh2 == {"A": 7500, "B": 2500}
    print("ok split exact + weighted")


def test_nets():
    people, paid, share, nets, _ = compute_nets(parse_ledger(LEDGER), {})
    assert sum(nets.values()) == 0
    assert nets["Ana"] == 31750  # paid 450, share 132.50
    assert nets["Ben"] == -9250  # paid 120, share 212.50
    assert nets["Cho"] == -13250
    assert nets["Dan"] == -9250
    print("ok nets")


def test_settlement():
    _, _, _, nets, _ = compute_nets(parse_ledger(LEDGER), {})
    transfers = min_cash_flow(nets)
    # verify transfers reproduce nets
    final = dict(nets)
    for t in transfers:
        final[t["from"]] += t["amount_c"]
        final[t["to"]] -= t["amount_c"]
    assert all(v == 0 for v in final.values())
    assert len(transfers) <= 3  # n-1 with 4 people... here 3 debtors -> 3 transfers
    print(f"ok settlement ({len(transfers)} transfers)")


def test_no_pay_and_receive():
    # in a star pattern everyone pays one hub
    _, _, _, nets, _ = compute_nets(parse_ledger(LEDGER), {})
    transfers = min_cash_flow(nets)
    payers = {t["from"] for t in transfers}
    receivers = {t["to"] for t in transfers}
    assert not (payers & receivers), "someone both pays and receives"
    print("ok no pay-and-receive")


def test_weights():
    ledger = "Ana,2400,Ana Ben Cho\n"
    people, paid, share, nets, _ = compute_nets(parse_ledger(ledger), {"Ana": 2, "Ben": 1, "Cho": 1})
    assert share["Ana"] == 120000 and share["Ben"] == 60000 and share["Cho"] == 60000
    assert nets["Ana"] == 120000  # paid 2400, share 1200
    transfers = min_cash_flow(nets)
    assert len(transfers) == 2
    print("ok weights")


def test_edge_everyone_square():
    ledger = "Ana,100,Ana Ben\nBen,100,Ana Ben\n"
    _, _, _, nets, _ = compute_nets(parse_ledger(ledger), {})
    assert all(v == 0 for v in nets.values())
    assert min_cash_flow(nets) == []
    print("ok everyone square -> zero transfers")


if __name__ == "__main__":
    test_parse_amount()
    test_split_exact()
    test_nets()
    test_settlement()
    test_no_pay_and_receive()
    test_weights()
    test_edge_everyone_square()
    print("\nALL TESTS PASSED ✅")
