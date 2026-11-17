#!/usr/bin/env python3
"""Gift card portfolio tracker: decay risk, dormancy clocks, resale verdicts.

Commands:
  add          --store NAME --balance N --received DATE [--last4 NNNN] [--note ...]
  list         (table of cards)
  status       (portfolio view with verdicts)
  sell-advice  --store NAME --offer-pct P   (cash-out verdict for a live offer)
  distress     --store NAME   (mark brand distressed -> AT RISK re-score)
  spend        --id N --amount N  (log activity; resets dormancy clock)
Registry: gift_cards.json next to script (or --registry PATH).
"""
import argparse
import json
from datetime import date, datetime
from pathlib import Path

# Resale market heuristics by brand family (fraction of face on exchanges).
# Deliberately coarse; sell-advice takes a live --offer-pct override.
RESALE_BANDS = [
    (["home depot", "lowes", "menards", "costco", "walmart", "target", "best buy",
      "apple", "amazon", "walgreens", "cvs"], (0.82, 0.92), "big-box/electronics: liquid"),
    (["nordstrom", "macy", "sephora", "ulta", "bath", "victoria", "express",
      "gap", "banana republic"], (0.60, 0.75), "fashion/niche: weak resale"),
    (["restaurant", "grill", "bar", "bistro", "cafe", "dining", "chili", "outback",
      "olive", "applebee", "denver", "carino", "texas", "bloomin"], (0.68, 0.80),
     "casual dining: resale OK, distress-prone sector"),
    (["airline", "hotel", "marriott", "hilton", "delta", "united", "uber", "lyft",
      "gas", "shell", "chevron"], (0.75, 0.88), "travel/fuel: strong resale"),
    (["visa", "mastercard", "amex", "american express"], (0.85, 0.95),
     "open-loop: near-cash (check front-end fees)"),
]

# Sector distress priors (chapter-11 frequency, casual dining leading).
DISTRESS_PRIORS = {
    "casual_dining": "high", "fashion": "medium", "big_box": "low",
    "travel": "low", "open_loop": "none",
}

DORMANCY_FEE_MONTHS = 12   # CARD Act: no inactivity fee before this
VALIDITY_YEARS = 5         # CARD Act floor from last activity
ESCHEAT_YEARS = 3          # shortest common state dormancy window


def load(p: Path) -> list:
    if p.exists():
        return json.loads(p.read_text())
    return []


def save(p: Path, cards: list) -> None:
    p.write_text(json.dumps(cards, indent=2, ensure_ascii=False) + "\n")


def classify(store: str):
    s = store.lower()
    for keys, band, label in RESALE_BANDS:
        if any(k in s for k in keys):
            return band, label
    return (0.55, 0.70), "niche/unknown: assume weak resale"


def sector_of(store: str) -> str:
    s = store.lower()
    if any(k in s for k in ("grill", "bar", "bistro", "cafe", "dining", "chili",
                            "outback", "olive", "applebee", "carino", "bloomin",
                            "restaurant")):
        return "casual_dining"
    if any(k in s for k in ("nordstrom", "macy", "sephora", "ulta", "bath",
                            "victoria", "express", "gap")):
        return "fashion"
    if any(k in s for k in ("visa", "mastercard", "amex")):
        return "open_loop"
    if any(k in s for k in ("airline", "hotel", "marriott", "hilton", "delta",
                            "united", "uber", "lyft", "gas", "shell", "chevron")):
        return "travel"
    return "big_box"


def months_idle(card: dict, today: date) -> float:
    last = card.get("last_activity") or card["received"]
    d = date.fromisoformat(last)
    return (today - d).days / 30.44


def decay_value(card: dict, today: date) -> float:
    """Face value after modeled dormancy fees (where allowed, post-12mo, $1/mo)."""
    idle = months_idle(card, today)
    fee = max(0.0, (idle - DORMANCY_FEE_MONTHS)) * 1.0
    return max(card["balance"] - fee, 0.0)


def verdict(card: dict, today: date) -> tuple:
    store = card["store"]
    idle = months_idle(card, today)
    distressed = card.get("distressed", False)
    band, label = classify(store)
    sec = sector_of(store)
    decayed = decay_value(card, today)

    if distressed:
        return ("AT RISK", f"{store} marked distressed: SPEND this week (essentials first) "
                           f"or sell before market reprices. Bankruptcy haircut 75-90%. "
                           f"Usable-ish value now: ~${decayed:.2f}.")
    if idle >= ESCHEAT_YEARS * 12:
        return ("REFRESH", f"Idle {idle:.0f} mo (escheat window): $1 purchase resets "
                           f"dormancy + escheat clocks; also check state unclaimed-property "
                           f"site for already-pulled balances.")
    if idle >= DORMANCY_FEE_MONTHS:
        return ("DORMANCY WATCH", f"Idle {idle:.0f} mo: inactivity fees legal after 12 mo "
                                  f"(~$1/mo where allowed). Modeled value ${decayed:.2f}. "
                                  f"Sector distress prior: {DISTRESS_PRIORS[sec]}.")
    # Not old: decide by usefulness proxy (note field) + resale floor
    floor = band[0]
    if card.get("will_use"):
        return ("BURN", f"You shop here — spend like cash. Resale floor would be "
                        f"{floor*100:.0f}% if that changes.")
    return ("HOLD/SELL?", f"Resale band {int(band[0]*100)}-{int(band[1]*100)}% ({label}). "
                          f"Won't-use card at floor ≈ ${card['balance']*floor:.2f} cash. "
                          f"Mark `--will-use` if you'll spend it within 3 months.")


def cmd_add(args, p: Path) -> None:
    cards = load(p)
    cards.append({
        "id": max((c["id"] for c in cards), default=0) + 1,
        "store": args.store, "balance": args.balance,
        "received": args.received, "last4": args.last4,
        "note": args.note, "will_use": args.will_use,
        "last_activity": None, "distressed": False,
    })
    save(p, cards)
    print(f"Added #{cards[-1]['id']}: {args.store} ${args.balance:.2f} "
          f"(received {args.received}).")


def cmd_list(args, p: Path) -> None:
    cards = load(p)
    if not cards:
        print("Registry empty. `add` cards first.")
        return
    today = date.today()
    print(f"{'ID':>3} {'Store':<22} {'Bal':>9} {'Idle mo':>8} {'Distressed':<10}")
    for c in cards:
        print(f"{c['id']:>3} {c['store'][:22]:<22} {c['balance']:>9.2f} "
              f"{months_idle(c, today):>8.1f} {'YES' if c.get('distressed') else 'no':<10}")
    print(f"Total: ${sum(c['balance'] for c in cards):.2f}")


def cmd_status(args, p: Path) -> None:
    cards = load(p)
    if not cards:
        print("Registry empty. `add` cards first.")
        return
    today = date.today()
    total = sum(c["balance"] for c in cards)
    print(f"Portfolio: {len(cards)} cards, ${total:.2f} total\n")
    for c in cards:
        v, advice = verdict(c, today)
        print(f"  [{c['id']}] {c['store'][:24]:<24} ${c['balance']:>7.2f}  -> {v}")
        print(f"        {advice}")
    at_risk = [c for c in cards if c.get("distressed")]
    if at_risk:
        print(f"\n!! {len(at_risk)} distressed-brand card(s): "
              f"${sum(c['balance'] for c in at_risk):.2f} at bankruptcy risk — act this week.")


def cmd_sell_advice(args, p: Path) -> None:
    cards = [c for c in load(p) if c["store"].lower() == args.store.lower()]
    if not cards:
        sys_exit(f"No card for '{args.store}' in registry.")
    card = cards[0]
    band, label = classify(card["store"])
    cash = card["balance"] * args.offer_pct / 100
    fair = card["balance"] * band[0]
    if args.offer_pct >= band[1] * 100:
        dec = "SELL — top of band"
    elif args.offer_pct >= band[0] * 100:
        dec = "SELL if you won't use the card within ~3 months"
    else:
        dec = "LOWBALL — compare another exchange (band floor is " \
              f"{int(band[0]*100)}%)"
    print(f"{card['store']} ${card['balance']:.2f} | offer {args.offer_pct}% "
          f"=> ${cash:.2f} cash (fair floor ≈ ${fair:.2f})")
    print(f"Band: {int(band[0]*100)}-{int(band[1]*100)}% ({label})")
    print(f"Verdict: {dec}")


def sys_exit(msg: str) -> None:
    raise SystemExit(msg)


def cmd_distress(args, p: Path) -> None:
    cards = load(p)
    hit = False
    for c in cards:
        if c["store"].lower() == args.store.lower():
            c["distressed"] = True
            hit = True
    if not hit:
        sys_exit(f"No card for '{args.store}' in registry.")
    save(p, cards)
    today = date.today()
    print(f"!! {args.store} marked distressed. Re-scored:")
    for c in cards:
        if c["store"].lower() == args.store.lower():
            v, advice = verdict(c, today)
            print(f"  [{c['id']}] ${c['balance']:.2f} -> {v}")
            print(f"      {advice}")


def cmd_spend(args, p: Path) -> None:
    cards = load(p)
    for c in cards:
        if c["id"] == args.id:
            if args.amount > c["balance"]:
                sys_exit(f"Amount exceeds balance (${c['balance']:.2f}).")
            c["balance"] = round(c["balance"] - args.amount, 2)
            c["last_activity"] = date.today().isoformat()
            save(p, cards)
            print(f"Spent ${args.amount:.2f} at {c['store']}; balance "
                  f"${c['balance']:.2f}; dormancy clock reset.")
            return
    sys_exit(f"No card id {args.id}.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--registry", default=str(Path(__file__).parent / "gift_cards.json"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("add")
    p.add_argument("--store", required=True)
    p.add_argument("--balance", type=float, required=True)
    p.add_argument("--received", required=True, help="YYYY-MM-DD")
    p.add_argument("--last4", default=None)
    p.add_argument("--note", default=None)
    p.add_argument("--will-use", action="store_true",
                   help="you genuinely shop here")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list"); p.set_defaults(func=cmd_list)
    p = sub.add_parser("status"); p.set_defaults(func=cmd_status)

    p = sub.add_parser("sell-advice")
    p.add_argument("--store", required=True)
    p.add_argument("--offer-pct", type=float, required=True)
    p.set_defaults(func=cmd_sell_advice)

    p = sub.add_parser("distress")
    p.add_argument("--store", required=True)
    p.set_defaults(func=cmd_distress)

    p = sub.add_parser("spend")
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--amount", type=float, required=True)
    p.set_defaults(func=cmd_spend)

    args = ap.parse_args()
    args.func(args, Path(args.registry))


if __name__ == "__main__":
    main()
