# Household — Money With Other People

**Before answering**, read `household` in `~/Clawic/data/money/config.yaml` and `## Situation` in `~/Clawic/data/money/memory.md`. Advising a couple as one person is the standard failure: two incomes, two risk postures, two credit files, and frequently two different sets of information.

## Joint, Separate, or Both

There is no correct structure, only structures that fail in different ways. The default that works for most couples is **all three accounts**:

| Account | Funded by | Pays for |
|---|---|---|
| Joint | Both, in an agreed proportion | Housing, utilities, food, childcare, shared insurance, shared sinking funds |
| Personal (one each) | The remainder of each income | Anything either person wants, with no accounting to the other |
| Shared savings | Both, from the joint account | Buffer, dated goals, shared long-term money |

The proportion is the real question, and there are three defensible answers:

- **Equal amounts** — simple, and it quietly transfers a larger share of the burden to the lower earner.
- **Proportional to income** — each contributes the same percentage of net income. The fairest on a spreadsheet and the most common recommendation.
- **Equal remaining discretionary** — both end the month with the same personal money. Best where incomes are very different, and hardest to compute.

Whichever is chosen, **each person keeps money that requires no explanation.** Structures with no personal money produce concealment, which is the actual mechanism behind most money conflict in couples.

Two constraints that are not preferences:

- **Both partners keep an account and a credit file in their own name.** A person with no independent financial identity cannot leave, cannot borrow, and is invisible to lenders after a bereavement. This is the single most consequential structural rule in the file.
- **Both know where everything is.** Not both manage it — one may — but both can find every account, debt, policy and document. The estate checklist below is what makes that true.

## Joint Debt and Joint Liability

- **Joint debt is joint and several: each party owes the lender the whole amount**, whatever they agreed between themselves. A separation agreement binds the couple; it does not bind the bank.
- The only way out of joint debt is refinancing into one name, which requires that person to qualify alone. Check this **before** the relationship needs it, not after.
- Being an additional cardholder is not the same as being a joint borrower — one carries liability, the other does not. Know which applies.
- **Financial association at the credit bureaus** links two files in several jurisdictions and persists after the accounts close until formally broken (`credit.md`).
- Guaranteeing a partner's or a relative's borrowing is taking on the debt with none of the control (`windfalls.md`).

## The Conversation, As A Procedure

Money conflict is rarely about the amount; it is about a difference in what money is for — security, freedom, status, or care — and those are learned in childhood and not argued away.

- **Schedule it.** A monthly review at a fixed time, thirty minutes, never during or after a disagreement about a specific purchase (`reviews.md`).
- **Agree a threshold** above which any purchase is discussed. Setting the number ends the recurring argument about whether this one counted.
- **Separate the numbers from the values.** Numbers are a shared fact-finding exercise; values are a negotiation. Doing both at once produces neither.
- **Both parties present when the plan is set.** A plan authored by one is defected from by the other, reliably.
- Disclose debts fully and early, including to a new partner. Undisclosed debt discovered later does more damage than the debt.
- Where one partner controls all the money and the other has no access or information, that is coercive control, not a preference — a Red Flags item, routed to the appropriate service in `country`.

## Children

- **Cost concentrates where the plan is weakest**: childcare in the early years, which frequently exceeds housing for a period, and education later. Both are foreseeable, so both are sinking funds, not surprises (`budget.md`).
- The **second-earner arithmetic** decides more than preference: childcare, transport, tax at the marginal rate and any withdrawn support can leave the marginal net near zero for a period. That is a temporary condition, and leaving the workforce has a long tail in earnings and pension — model both the current year and the decade (`income.md`, `taxes.md`).
- Education saving competes with retirement, and the ordering rule is unpopular but sound: **retirement first.** A child can borrow for education; nobody lends for retirement. Fund education from what remains, and say so plainly.
- Money education for the child is cheap and compounds: an allowance they control and can lose, a savings account they watch, and visible household trade-offs. What is being taught is that money is finite and allocated, which is the whole skill.
- On a child's birth: update beneficiaries, review life and income-protection cover for both parents including a non-earning one, name guardians, and write or update the will (`insurance.md`).

## Ageing Parents and Care

- Start the conversation while it is hypothetical. The questions: is there a will, where is it, who holds power of attorney, what income and cover exists, and what are the wishes about care.
- **A power of attorney must be set up while capacity is not in question.** After that it becomes a court process — slower, expensive, and public in many jurisdictions. This is the single highest-value item in the file per hour spent.
- Care costs are the largest late-life financial risk in most countries and the state's share varies enormously. Establish what `country` covers before anyone plans around an assumption.
- Adult children supporting parents: set a figure, from the family-help pot (`windfalls.md`), and keep it inside the household's own plan. A supporter who ends up unfunded creates a second problem rather than solving the first.
- Watch for financial abuse indicators (`scams.md`).

## Estate: The Checklist That Makes The Rest Work

Not an estate-planning service — the will, the trust and the tax structure belong to a qualified professional in `country` (Red Flags). What belongs here is the inventory, which is free, and which is what the family actually needs on the day.

- Will: exists, its location, when it was last reviewed, who the executor is
- **Beneficiary designations on every policy and pension — these override the will in many systems** and are the most common cause of money going to the wrong person. Check them after every life event (`insurance.md`)
- Power of attorney, financial and medical, and where the documents are
- Every account, debt, policy and pension, with the institution and reference — this is already `~/Clawic/data/finances/accounts.md`, which is why it stays current
- Digital assets: which accounts hold value, and how the family gains lawful access. **Never store credentials** — store the pointer to the password manager and who holds emergency access (`keychain:`, `1password:`)
- Funeral wishes and who to notify
- Who to call: solicitor, accountant, adviser, employer — people, so they live in `~/Clawic/data/contacts/contacts.md`, named here only

Review it annually and after every trigger: marriage, separation, birth, death, a house purchase, a move to another country, a business sale.

**Write it down.** The household structure, the contribution proportion, the discussion threshold and any dependants go to `## Situation` in `~/Clawic/data/money/memory.md`; `household` itself is a declaration and goes to `config.yaml`. Joint accounts and joint debts go to `~/Clawic/data/finances/accounts.md` marked as joint. The inventory above is an artifact at `~/Clawic/data/money/artifacts/estate-checklist.md`, reviewed annually in `## Due`, with its `## Boxes` line added the same turn. A solicitor, executor or guardian is a person: `~/Clawic/data/contacts/contacts.md`, referenced from here by name only. Format in `memory-template.md`.
