# Integrity workflow for a theory paper

The order matters. Each step gates the next.

## 1. State the claim before searching

Write the claim in the ledger first:

```bash
python run.py ledger -d 02-methodology-dev --add C1 conjecture "C(d,n) = A_leq d(n)"
```

Stating first, searching second, prevents retro-fitting the claim to whatever
the search happened to return.

## 2. Priority check — before writing "novel"

```bash
python run.py priority -d 02-methodology-dev --claim "C(d,n) = A_leq d(n)"
```

Read the candidates. Resolve with a URL to the page actually consulted:

```bash
python run.py priority -d 02-methodology-dev --resolve P1 --verdict covered \
    --evidence https://arxiv.org/abs/XXXX.XXXXX --note "identical identity in Thm 3"
```

Verdicts: `novel`, `covered`, `partial`, `unchecked`.
Only `novel` (or `partial` with the difference spelled out) supports a novelty
claim in the introduction. `unchecked` does not.

## 3. Prove, with dependencies tracked

```bash
python run.py ledger -d 02-methodology-dev --add L1 lemma "..." --status proven --proof proofs/L1.tex
python run.py ledger -d 02-methodology-dev --add T1 theorem "..." --depends L1
python run.py ledger -d 02-methodology-dev --set T1 proven   # refused while L1 is unproven
```

If a dependency cannot be proved, mark the dependent claim `conditional` and
name the assumption in the paper. Do not leave it `proven`.

## 4. Certify every numerical claim exactly

```bash
python run.py certify --script 07-audit-trail/check_C_dn.py --strict
```

Use `fractions.Fraction` or `sympy.Rational`. The linter flags float literals,
`float()`, bare `/`, and `math`/`numpy` imports. A certificate with float
contamination is not machine-precision evidence.

The script must print a line beginning with `CERTIFIED` or `REFUTED`.

## 5. Record dead ends

```bash
python run.py session -d session --attempt "LP duality" --outcome failure \
    --why "dual is unbounded; the envelope is not polyhedral"
```

A failed attempt without a recorded reason will be re-attempted next session.

## 6. Audit before submission

```bash
python run.py audit -p . --strict
python run.py check -p .
```

`audit` answers "can I defend this?"; `check` answers "is the material
present?". Both are necessary; neither is sufficient.

## What a self-audit must disclose

- claims still `open` (state them as open in the paper);
- claims `conditional` on an unproved assumption;
- priority records still `unchecked`;
- certificates with float contamination;
- revision rounds below 5.

Disclose these rather than omitting them. A reviewer who finds an undisclosed
gap stops trusting the rest of the paper.
