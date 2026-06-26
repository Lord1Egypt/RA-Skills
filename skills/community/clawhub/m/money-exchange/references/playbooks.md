# Playbooks — currency-exchange

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: Exchange Rate

**Trigger:** "exchange rate {currency}"

```bash
flyai keyword-search --query "汇率 {currency}"
```

**Output emphasis:** Current exchange rates.

---

## Playbook B: Where to Exchange

**Trigger:** "where to exchange money"

```bash
flyai keyword-search --query "换汇 {dest}"
```

**Output emphasis:** Best exchange locations.

---

## Playbook C: Payment Methods

**Trigger:** "can I use Alipay in {dest}"

```bash
flyai keyword-search --query "支付方式 {dest}"
```

**Output emphasis:** Local payment method info.

---

