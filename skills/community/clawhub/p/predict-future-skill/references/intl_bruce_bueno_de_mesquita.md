# International Relations — Bueno de Mesquita Game-Theoretic Forecasting

The most **explicitly predictive** methodology in political science. Bruce Bueno
de Mesquita (NYU / Hoover) models a decision as a **bargaining game among
stakeholders** and computes the most likely outcome. Key works: *The War Trap*
(1981), *Predicting Politics* (2002), *The Predictioneer's Game* (2009);
selectorate theory in *The Logic of Political Survival* (2003, with Smith,
Siverson, Morrow) and *The Dictator's Handbook* (2011).

CIA evaluations (Feder, 1995/2002) reported the model accurate in **~90% of
1,700+ real-time cases**, and notably *more specific* than human analysts — it
"hit the bull's-eye" about twice as often. **Caveat**: the same human experts
supplied the inputs and scored similarly on direction; the model's edge is in
**precision and consistency**, not magic. Garbage in, garbage out.

Use this reference when the decisive question is: **"Given who wants what and how
hard, what specific outcome will this negotiation / policy fight / power struggle
converge on?"** — i.e. concrete, near-to-medium-term decisions with identifiable
players.

## The model in one line

Treat the issue as a **point on a single metric scale** (a policy dial), list the
**stakeholders**, score each one, then simulate rounds of offers, threats, and
coalition-shifting until positions converge to an **equilibrium** — the forecast.

## The four inputs (score every stakeholder)

For each actor *i* on the issue, estimate:

1. **Position** — where they currently stand, as a number on the issue scale
   (e.g. "preferred year to adopt emission standards," or 0–100 on a policy dial).
2. **Clout / influence** (capability) — how much potential power they could bring
   to bear *on this issue* if fully mobilized.
3. **Salience** — how high a priority this issue is for them; how likely they are
   to spend their clout on it rather than stay on the sidelines.
4. **Resolve / flexibility** (added in the 2009 model) — how much they value
   *getting a deal* vs. *holding their position* even if it means losing.

Define the **issue continuum** precisely first — a clean, one-dimensional scale is
what makes the model work. Ambiguous issue definitions are the #1 failure mode.

## How the simulation runs (do this by hand)

The full software iterates expected-utility comparisons, but you can reproduce the
logic manually:

1. **Identify the median-voter / power-weighted center.** Sort stakeholders along
   the issue; weight each by `clout × salience`. The power-weighted center of
   gravity is the gravitational pull point.
2. **For each pair, compute who can credibly pressure whom.** An actor will
   challenge another if the expected utility of pressing (probability of winning
   × gain, minus cost and risk of conflict) beats the status quo.
3. **Let positions move.** Weak/low-salience actors concede toward stronger
   coalitions; flexible actors trade position for agreement; resolute actors
   anchor. Coalitions form around viable focal positions.
4. **Iterate** until positions stop moving materially — that equilibrium is the
   **predicted outcome**, with the surviving coalition structure showing *why*.

Output is specific: not "tensions will rise" but "the policy will settle near
point X, carried by coalition {A, B, C}, over roughly N rounds/months."

## Selectorate theory (companion lens for regime behavior)

For *why leaders choose the positions they do* — especially survival-driven
behavior — use selectorate theory:

- **Selectorate (S)** — everyone with a say in choosing the leader.
- **Winning coalition (W)** — the subset whose support the leader actually needs.
- **Small W (autocracy)** → leaders buy loyalty with **private goods** (patronage,
  corruption); risk-tolerant abroad, survive policy failure easily.
- **Large W (democracy)** → leaders must deliver **public goods** (growth,
  victory); punished for failed wars and bad economies.

This predicts foreign-policy risk appetite, war initiation, aid/repression
choices, and reform likelihood from regime structure — feed its conclusions back
in as each actor's *salience* and *resolve*.

## Limits

- Needs a **well-specified, one-dimensional issue** and a **bounded, identifiable
  set of stakeholders**. Diffuse, multi-issue, or mass-movement dynamics fit
  poorly.
- Highly sensitive to **input quality**; small errors in clout/salience swing
  results. State your scores explicitly so they can be challenged.
- Assumes instrumentally rational, self-interested actors — weak where ideology,
  honor, or genuine irrationality dominate.

## How to apply in this skill

1. **Define the issue as one numeric scale** and state it in the output.
2. **Build a stakeholder table**: actor | position | clout (0–100) | salience
   (0–100) | resolve. Use the Search/web tools to ground each score; label any
   guess as an assumption.
3. **Find the power-weighted center** (`clout × salience`) and identify the
   pivotal players and plausible coalitions.
4. **Reason through 2–4 rounds of bargaining** by hand using the rules above;
   show how positions and coalitions shift each round.
5. **State the equilibrium as the forecast**: predicted outcome on the scale,
   the winning coalition, a horizon, and the inputs whose change would flip it
   (your falsifiable triggers + sensitivity note).
6. If regime behavior drives any actor's resolve, **run selectorate theory** on
   that actor and fold the result back into the table.
7. Keep this forecast **standalone** — do not merge with the realism or Schelling
   sections; divergences are informative.
