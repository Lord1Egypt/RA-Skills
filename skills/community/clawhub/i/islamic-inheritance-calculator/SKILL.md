---
name: islamic-inheritance-calculator
description: Islamic inheritance (Faraid, Mirath, Meeras, Wirasat, Waris) calculator and guide. Interviews the user about the deceased, estate, debts, will (wasiyyah) and surviving relatives, then computes each heir's share - fixed shares (1/2, 1/4, 1/8, 2/3, 1/3, 1/6), residuary ('asabah), blocking (hajb), 'awl and radd - citing the Quran ayah, sahih hadith, Companion (Sahaba) ruling or scholarly consensus (ijma) behind every rule, and clearly flagging where the Sunni schools (Hanafi, Maliki, Shafi'i, Hanbali) differ. Use when someone asks how to divide a Muslim's estate, who inherits under Sharia, what share a wife, husband, daughter, son, mother, father or sibling gets, or how much can be left in an Islamic will. Works fully offline, no APIs.
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "⚖️"
---

# Islamic Inheritance Calculator (Faraid)

You guide a user through dividing a deceased Muslim's estate according to Islamic inheritance law, and you show the evidence for every rule you apply.

## 1. Non-negotiable rules for you (read first)

1. **Accuracy over completeness.** This is a religious obligation. Use ONLY the rules and references in this file. If a case is not covered here, say so plainly and refer the user to a qualified scholar (mufti / qadi). Never improvise a ruling.
2. **Never fabricate a reference.** Cite only the references listed in Section 11. Hadith numbers follow sunnah.com numbering; tell the user numbering can differ between printed editions.
3. **Evidence hierarchy - always cite the highest source available, in this order:**
   1. `[QURAN]` - ayah reference, with a short paraphrase of its meaning (do not invent wording).
   2. `[SAHIH HADITH]` - only for Sahih al-Bukhari / Sahih Muslim.
   3. `[HADITH]` - other collections; state the collection, and if the grading is disputed say so and note the ruling also rests on consensus.
   4. `[SAHABA]` - ruling of the Companions (e.g. Umar, Zayd ibn Thabit, Ibn Mas'ud).
   5. `[IJMA]` - consensus of the scholars of the Ummah.
   6. `[MADHHAB]` - ONLY when sources 1-5 give no single answer. Then say explicitly: "There is no direct text from the Quran or Sunnah on this specific point, and scholars differ. Here are the positions:" and list each Sunni school's view neutrally. Do not prefer one school unless the user chose a madhab.
4. **No sectarian debate.** This skill follows the shared Sunni framework. If the user follows the Ja'fari (Shia) school, say its inheritance rules differ substantially and refer them to a scholar of that school. Do not argue or rank sects.
5. **Not a fatwa.** End every final answer with the disclaimer in Section 9.
6. **Exact arithmetic.** Work in fractions, not decimals. If you have a code/calculator tool, use it. Always verify the shares sum exactly to 1 (the whole) before presenting.
7. **Be gentle.** The user may be grieving. Brief condolence on the first turn, then be clear and efficient.

## 2. Interview flow

Ask in short rounds. Skip questions made irrelevant by earlier answers (e.g. if there is a son, do not ask about siblings, nephews or uncles - they are blocked, but mention that they are excluded).

**Round 1 - the deceased and the estate**

- Was the deceased male or female? Were they Muslim?
- Total estate value and currency (or "just show shares").
- Funeral/burial costs still unpaid? Any debts (loans, unpaid mahr to the wife, bills)?
- Did they leave a will (wasiyyah)? To whom and how much?
- Madhab preference (Hanafi / Maliki / Shafi'i / Hanbali / no preference). If none, you will show the majority view and flag differences.
- Country of residence (for the civil-law note only).

**Round 2 - surviving relatives** (alive at the moment of death; give counts)
Husband / wife(s); sons; daughters; son's sons; son's daughters; father; mother; father's father; father's mother; mother's mother; full brothers; full sisters; paternal half-brothers; paternal half-sisters; maternal half-brothers/sisters; sons of full brothers; sons of paternal half-brothers; full paternal uncles; paternal half-uncles (father's paternal half-brothers); sons of those uncles.

**Round 3 - impediment check**

- Is any listed relative not Muslim?
- Did any relative cause the death?
- Is any wife divorced? If yes: revocable (talaq raj'i) and still in 'iddah, or final?
- Is anyone pregnant with a possible heir? Is any heir missing / status unknown?
- Did any heirs die at the same time as the deceased (accident, disaster)?

## 3. Step A - settle the estate before dividing

Order (apply strictly):

1. **Funeral and burial costs** (reasonable). `[IJMA]`
2. **Debts** - including unpaid mahr. Debts come before the will. `[QURAN]` 4:11-12 mention "after any bequest or debt"; `[HADITH]` Ali: the Prophet ﷺ ruled debt before bequest (Tirmidhi 2094, 2122; Ibn Majah 2715 - chain contains al-Harith al-A'war, graded hasan by al-Albani due to supporting narrations); Imam al-Tirmidhi reports scholarly consensus on this. `[IJMA]`
   - Debts owed to Allah (unpaid zakat, missed Hajj): `[MADHHAB]` Shafi'i and Hanbali pay them from the estate like other debts; Hanafi pays them only if the deceased bequeathed it, and then from the one-third.
3. **Will (wasiyyah)** - maximum one-third of what remains, and not to someone who is already an heir.
   - One-third cap: `[SAHIH HADITH]` Sa'd ibn Abi Waqqas: "One third, and one third is a lot" (Bukhari 2742, Muslim 1628).
   - No bequest to an heir: `[HADITH]` "No bequest for an heir" (Abu Dawud 2870, Tirmidhi 2120 - Tirmidhi: hasan sahih; Ibn Majah 2713). `[IJMA]` on acting by it.
   - More than 1/3, or a bequest to an heir, is valid only if the other adult heirs freely consent after the death. `[MADHHAB]` majority view.
4. **The remainder is the net estate** divided by Faraid.

## 4. Step B - who is excluded by an impediment

| Impediment                                 | Ruling                                                                                                                                                                                                       | Evidence                                                                                                                                                                                                           |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Difference of religion                     | A Muslim does not inherit from a non-Muslim, nor a non-Muslim from a Muslim                                                                                                                                  | `[SAHIH HADITH]` Usamah ibn Zayd (Bukhari 6764, Muslim 1614)                                                                                                                                                       |
| Killing the deceased                       | The killer does not inherit                                                                                                                                                                                  | `[HADITH]` "The killer gets nothing" (Abu Dawud 4564, graded hasan by al-Albani; Ibn Majah 2645); `[IJMA]` for intentional killing. `[MADHHAB]` schools differ on accidental/indirect killing - refer to a scholar |
| Adopted child                              | Not an heir (can receive a bequest within 1/3)                                                                                                                                                               | `[QURAN]` 33:4-5 (adopted children are called by their real fathers)                                                                                                                                               |
| Step-child / in-law                        | Not an heir                                                                                                                                                                                                  | No kinship by blood or marriage-to-the-deceased; `[IJMA]`                                                                                                                                                          |
| Child born outside marriage                | Inherits from the mother and her side only, not from the biological father                                                                                                                                   | `[SAHIH HADITH]` "The child belongs to the marriage bed" (Bukhari 6749, Muslim 1457); `[IJMA]`                                                                                                                     |
| Wife in revocable divorce, still in 'iddah | Still inherits as a wife                                                                                                                                                                                     | `[IJMA]`                                                                                                                                                                                                           |
| Wife after final (irrevocable) divorce     | Does not inherit. Exception: divorce given in terminal illness to deprive her - `[SAHABA]` Uthman let Tumadir inherit from Abd al-Rahman ibn Awf; `[MADHHAB]` schools differ on details - refer to a scholar |                                                                                                                                                                                                                    |
| Died simultaneously, order unknown         | They do not inherit from each other; each estate goes to their own living heirs                                                                                                                              | `[SAHABA]` view of Zayd ibn Thabit and others; `[MADHHAB]` majority (Hanbali differs in some cases)                                                                                                                |
| Unborn child                               | Inherits if born alive. Estate should be held or the largest possible share reserved until birth                                                                                                             | `[HADITH]` Abu Dawud 2920 (the newborn inherits if it cries at birth), graded sahih by al-Albani - refer to scholar for the reserve calculation                                                                    |
| Missing person                             | Out of scope - refer to a scholar/court                                                                                                                                                                      |                                                                                                                                                                                                                    |

A relative who died BEFORE the deceased is not an heir. Their children inherit only in their own right (e.g. a son's son), never by "replacing" the parent.

## 5. Step C - the fixed-share heirs (Ashab al-Furud)

"Descendant" below = a child or a son's child (any depth through males), male or female. A daughter's children are not "descendants" here (they are distant kindred).

| Heir                                                    | Share                                 | Condition                                                                                     | Evidence                                                                                                                                                                                                                                                                           |
| ------------------------------------------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Husband                                                 | 1/2                                   | no descendant                                                                                 | `[QURAN]` 4:12                                                                                                                                                                                                                                                                     |
| Husband                                                 | 1/4                                   | with descendant                                                                               | `[QURAN]` 4:12                                                                                                                                                                                                                                                                     |
| Wife (1-4 wives share equally)                          | 1/4                                   | no descendant                                                                                 | `[QURAN]` 4:12                                                                                                                                                                                                                                                                     |
| Wife                                                    | 1/8                                   | with descendant                                                                               | `[QURAN]` 4:12                                                                                                                                                                                                                                                                     |
| Father                                                  | 1/6                                   | with a male descendant                                                                        | `[QURAN]` 4:11                                                                                                                                                                                                                                                                     |
| Father                                                  | 1/6 + residue                         | with only female descendants                                                                  | `[QURAN]` 4:11 + `[SAHIH HADITH]` "Give the shares to those entitled; what remains goes to the nearest male" (Bukhari 6732, Muslim 1615)                                                                                                                                           |
| Father                                                  | residue (all that remains)            | no descendant                                                                                 | same as above; `[IJMA]`                                                                                                                                                                                                                                                            |
| Mother                                                  | 1/6                                   | descendant exists, OR 2+ siblings of any type (even if those siblings are themselves blocked) | `[QURAN]` 4:11; two siblings suffice: `[SAHABA]` majority, `[IJMA]` of later scholars (Ibn Abbas held three)                                                                                                                                                                       |
| Mother                                                  | 1/3                                   | no descendant, fewer than 2 siblings                                                          | `[QURAN]` 4:11                                                                                                                                                                                                                                                                     |
| Mother                                                  | 1/3 of the remainder after the spouse | ONLY heirs are spouse + father + mother (Umariyyatan)                                         | `[SAHABA]` ruling of Umar, agreed by Uthman, Zayd, Ibn Mas'ud; `[MADHHAB]` adopted by all four schools. Ibn Abbas gave 1/3 of the whole                                                                                                                                            |
| Daughter (1)                                            | 1/2                                   | no son                                                                                        | `[QURAN]` 4:11                                                                                                                                                                                                                                                                     |
| Daughters (2+)                                          | 2/3 shared                            | no son                                                                                        | `[QURAN]` 4:11 (for "more than two"); two daughters take 2/3 by `[HADITH]` the daughters of Sa'd ibn al-Rabi' (Abu Dawud 2891, Tirmidhi 2092, Ibn Majah 2720 - graded hasan by Tirmidhi and al-Albani, some graders weaken it), by analogy with two sisters in 4:176, and `[IJMA]` |
| Daughter(s) with son(s)                                 | residuary, male = 2 females           |                                                                                               | `[QURAN]` 4:11                                                                                                                                                                                                                                                                     |
| Son's daughter(s)                                       | 1/2 (one) / 2/3 (2+)                  | no children of the deceased                                                                   | `[IJMA]` (son's children stand in place of children when there are none)                                                                                                                                                                                                           |
| Son's daughter(s)                                       | 1/6 shared                            | with exactly ONE daughter and no son ("completing 2/3")                                       | `[SAHIH HADITH]` Ibn Mas'ud reporting the Prophet's ﷺ ruling (Bukhari 6736)                                                                                                                                                                                                        |
| Full sister (1)                                         | 1/2                                   | no descendant male, no father (grandfather: see 7.3), no full brother, no daughter            | `[QURAN]` 4:176                                                                                                                                                                                                                                                                    |
| Full sisters (2+)                                       | 2/3 shared                            | same conditions                                                                               | `[QURAN]` 4:176                                                                                                                                                                                                                                                                    |
| Paternal half-sister(s)                                 | 1/2 / 2/3                             | as full sister, and no full sibling                                                           | `[QURAN]` 4:176; `[IJMA]` that 4:176 covers full and paternal siblings                                                                                                                                                                                                             |
| Paternal half-sister(s)                                 | 1/6 shared                            | with exactly ONE full sister (completing 2/3)                                                 | `[IJMA]`, by analogy with Bukhari 6736                                                                                                                                                                                                                                             |
| Maternal half-sibling (1)                               | 1/6                                   | no descendant, no father, no paternal grandfather                                             | `[QURAN]` 4:12 (kalalah)                                                                                                                                                                                                                                                           |
| Maternal half-siblings (2+)                             | 1/3 shared EQUALLY (male = female)    | same                                                                                          | `[QURAN]` 4:12 "they share in one third"                                                                                                                                                                                                                                           |
| Grandmother(s) - mother's mother and/or father's mother | 1/6 shared                            | no mother                                                                                     | `[HADITH]` Abu Bakr's ruling after al-Mughirah and Muhammad ibn Maslamah testified the Prophet ﷺ gave her 1/6 (Abu Dawud 2894, Tirmidhi 2100-2101, Ibn Majah 2724, Muwatta Malik - chain disputed); `[SAHABA]` Abu Bakr and Umar; `[IJMA]` on the 1/6                              |
| Paternal grandfather                                    | as father                             | no father (exceptions: 7.1, 7.3)                                                              | `[SAHABA]`; `[IJMA]`                                                                                                                                                                                                                                                               |

Kalalah = a deceased who left no child and no father (definition of Abu Bakr, accepted by the Companions) `[SAHABA]`.

## 6. Step D - blocking (Hajb) and residuaries ('Asabah)

### 6.1 Never fully blocked

Husband, wife, son, daughter, father, mother. `[IJMA]`

### 6.2 Who blocks whom

| Relative                    | Fully blocked by                                                                                                                | Evidence                                                                                                      |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Son's son / son's daughter  | son (a nearer male descendant)                                                                                                  | `[SAHIH HADITH]` "nearest male" (Bukhari 6732); `[IJMA]`                                                      |
| Son's daughter(s)           | also 2+ daughters, UNLESS a son's son of the same or lower level is present (he makes her residuary with him, male = 2 females) | `[IJMA]` (2/3 cap of 4:11, Bukhari 6736)                                                                      |
| Paternal grandfather        | father                                                                                                                          | `[IJMA]`                                                                                                      |
| Mother's mother             | mother                                                                                                                          | `[IJMA]`                                                                                                      |
| Father's mother             | mother; father - `[MADHHAB]` Hanafi, Maliki, Shafi'i: the father blocks her; Hanbali: he does not                               |                                                                                                               |
| Full brother / full sister  | son, son's son, father. Grandfather: see 7.3                                                                                    | `[QURAN]` 4:176 (no child); `[IJMA]` father blocks                                                            |
| Paternal half-brother       | all the above + full brother + a full sister who is residuary with daughters                                                    | `[HADITH]` Ali: full siblings inherit before paternal half-siblings (Tirmidhi 2094, Ibn Majah 2739); `[IJMA]` |
| Paternal half-sister        | as paternal half-brother, + 2 full sisters (unless a paternal half-brother is with her)                                         | `[IJMA]`                                                                                                      |
| Maternal half-siblings      | any descendant (male or female), father, paternal grandfather                                                                   | `[QURAN]` 4:12 (kalalah)                                                                                      |
| Full brother's son          | all who block the paternal half-brother + paternal half-brother + paternal grandfather                                          | `[IJMA]`                                                                                                      |
| Paternal half-brother's son | + full brother's son                                                                                                            | `[IJMA]`                                                                                                      |
| Full paternal uncle         | + any brother's son                                                                                                             | `[IJMA]`                                                                                                      |
| Paternal half-uncle         | + full uncle                                                                                                                    | `[IJMA]`                                                                                                      |
| Full uncle's son            | + paternal half-uncle                                                                                                           | `[IJMA]`                                                                                                      |
| Paternal half-uncle's son   | + full uncle's son                                                                                                              | `[IJMA]`                                                                                                      |

### 6.3 Residuaries - order of priority

After fixed shares, the remainder goes to the nearest male agnate. `[SAHIH HADITH]` Bukhari 6732, Muslim 1615.

1. Son -> son's son (nearer first)
2. Father -> paternal grandfather
3. Full brother -> paternal half-brother
4. Full brother's son -> paternal half-brother's son (then their sons)
5. Full uncle -> paternal half-uncle -> their sons

Within the same rank, full (both parents) beats paternal-only. Only the highest group present takes the residue.

Women who become residuaries:

- Daughters with sons; son's daughters with son's sons of the same (or lower) level; full sisters with full brothers; paternal sisters with paternal brothers - all male = 2 females. `[QURAN]` 4:11, 4:176
- **Sisters with daughters:** a full sister (or, if none, a paternal sister) takes the residue when there are daughters/son's daughters and no son, son's son or father. She then blocks the paternal half-brother and everyone below him. `[SAHIH HADITH]` Mu'adh ruled half to the daughter, half to the sister (Bukhari 6734, 6741); Ibn Mas'ud's ruling gave the remainder to the sister (Bukhari 6736).

## 7. Special cases

### 7.1 Umariyyatan (spouse + father + mother only)

- Husband + father + mother: husband 1/2, mother 1/6 (= 1/3 of the remaining half), father 1/3.
- Wife + father + mother: wife 1/4, mother 1/4 (= 1/3 of remainder), father 1/2.
- If the GRANDFATHER replaces the father, the mother takes 1/3 of the whole. `[MADHHAB]` majority.
  Evidence: `[SAHABA]` Umar's ruling, see Section 5.

### 7.2 Mushtarakah / Himariyyah

Heirs: husband + mother (or grandmother) + 2+ maternal half-siblings + full brother(s) (with or without full sisters).
Fixed shares exhaust the estate (1/2 + 1/6 + 1/3), leaving the full brothers nothing.

- `[MADHHAB]` Maliki & Shafi'i: full siblings SHARE the maternal siblings' 1/3 equally with them (ruling of Umar, `[SAHABA]`).
- `[MADHHAB]` Hanafi & Hanbali: full brothers get nothing (view of Ali, `[SAHABA]`).
  State: "No direct text covers this case; the Companions differed." Show both results.

### 7.3 Paternal grandfather with full/paternal siblings

"No direct text from the Quran or Sunnah settles this; the Companions differed." `[SAHABA]`

- **View 1 - Abu Bakr, Ibn Abbas; Hanafi school:** the grandfather is like the father and blocks all full and paternal siblings.
- **View 2 - Zayd ibn Thabit, Ali, Ibn Mas'ud (with differences); Maliki, Shafi'i, Hanbali, and Abu Yusuf & Muhammad al-Shaybani of the Hanafis:** siblings share with the grandfather. Using Zayd's method, the grandfather gets the BEST of:
  - No fixed-share heirs: (a) sharing as if he were a brother (a sister counts as half a brother), or (b) 1/3 of the estate.
  - With fixed-share heirs: (a) sharing the remainder as a brother, (b) 1/3 of the remainder, or (c) 1/6 of the whole.
  - **Akdariyyah** (husband + mother + grandfather + one full or paternal sister): husband 9/27, mother 6/27, grandfather 8/27, sister 4/27.
  - If BOTH full and paternal half-siblings are present with the grandfather (mu'addah), refer to a scholar.
    Show both views' results when the user has no madhab; follow the user's madhab if given.
    Maternal half-siblings are blocked by the grandfather in ALL views.

### 7.4 'Awl - shares exceed the whole

If the fixed shares add up to more than 1, raise the base so every heir is reduced proportionally (bases: 6 -> 7, 8, 9, 10; 12 -> 13, 15, 17; 24 -> 27).
`[SAHABA]` Ruling of Umar with the agreement of the Companions; `[IJMA]` of the four schools. Ibn Abbas disagreed after Umar's death.

### 7.5 Radd - surplus with no residuary

If the fixed shares total less than 1 and there is no residuary, return the surplus to the fixed-share heirs in proportion to their shares, EXCLUDING the spouse.
`[SAHABA]` view of Ali, Ibn Mas'ud and others; `[MADHHAB]` Hanafi and Hanbali, and the later (relied-upon) Shafi'i and Maliki scholars where there is no properly functioning public treasury. Evidence cited: `[QURAN]` 8:75 / 33:6 (blood relatives are nearer to one another).
If the spouse is the ONLY heir: say "scholars differ" - many later scholars give the spouse the remainder when no other relative exists; refer to a scholar.

### 7.6 Distant kindred (Dhawu al-Arham)

E.g. daughter's children, sister's children, maternal uncles/aunts, paternal aunts, mother's father.
They inherit only if there is no fixed-share heir (other than a spouse) and no residuary. `[MADHHAB]` Hanafi & Hanbali (and later Shafi'i & Maliki) accept this; the methods of division differ. Evidence cited: `[QURAN]` 8:75.
Do NOT compute - explain they may inherit and refer to a scholar.

### 7.7 Orphaned grandchildren (child of a predeceased son)

They are blocked by a living son. `[IJMA]` Explain this gently. Recommended remedy (not obligatory in classical fiqh): the grandparent makes a bequest for them within 1/3 during life (`[QURAN]` 2:180 general encouragement of bequest to relatives; 4:8 giving relatives present at the division). Note: some countries' civil laws (e.g. Pakistan's Muslim Family Laws Ordinance 1961 s.4, Egypt's obligatory bequest) legislate differently - that is state law, not a classical Sharia ruling.

## 8. Step E - calculate

1. Assign each eligible heir's fixed share (Sections 5-7).
2. Base (asl al-mas'alah) = LCM of the denominators: one of 2, 3, 4, 6, 8, 12, 24.
3. Convert shares to units of the base. Sum them.
   - Sum = base -> done.
   - Sum < base and a residuary exists -> residuary takes the difference.
   - Sum < base, no residuary -> radd (7.5).
   - Sum > base -> 'awl (7.4).
4. **Correction (tashih):** if a group's units do not divide evenly among its members (counting male = 2, female = 1 where applicable), multiply the base and all units by the smallest factor that makes every member's portion a whole number.
5. Final share per person = units / base. Amount = net estate × share. Round currency only at the very end; note any rounding remainder.
6. Verify: all fractions sum exactly to 1 (or the radd/'awl total), and all amounts sum to the net estate.

## 9. Output format

1. **Estate settlement:** gross estate -> minus funeral -> minus debts -> minus will (≤ 1/3) -> net estate.
2. **Distribution table:**

| Heir | Count | Share (fraction) | %   | Amount per person | Total | Basis |
| ---- | ----- | ---------------- | --- | ----------------- | ----- | ----- |

3. **Evidence for this case:** each rule applied, with its tag (`[QURAN]`, `[SAHIH HADITH]`, `[HADITH]`, `[SAHABA]`, `[IJMA]`, `[MADHHAB]`) and reference.
4. **Relatives who do not inherit here, and why** (blocked by whom, or impediment).
5. **Where scholars differ** (only if a 7.x case applied): "There is no direct text from the Quran or Sunnah on this point" + each school's result.
6. **Disclaimer (always):**
   > This is an educational calculation based on established rules of Islamic inheritance with their sources. It is not a fatwa or legal advice. Please confirm the final distribution with a qualified scholar (mufti), and check the inheritance laws of your country, which may differ.

## 10. Worked examples (use to self-check)

**A. Wife, mother, father, 2 sons, 1 daughter (net 120,000)**
Wife 1/8, mother 1/6, father 1/6 (male descendant). Base 24: 3 + 4 + 4 = 11; remainder 13 to children, 5 parts (2+2+1) -> correct to base 120.
Wife 15/120 = 15,000; mother 20/120 = 20,000; father 20/120 = 20,000; each son 26/120 = 26,000; daughter 13/120 = 13,000. Total 120,000. ✓

**B. Husband, mother, 2 full sisters ('awl)**
Husband 1/2, mother 1/6 (2 siblings), sisters 2/3. Base 6: 3 + 1 + 4 = 8 -> 'awl to 8.
Husband 3/8, mother 1/8, each sister 2/8. ✓

**C. Daughter, son's daughter, full sister** (Bukhari 6736)
Daughter 1/2, son's daughter 1/6, sister residue. Base 6: 3, 1, 2. ✓

**D. Wife, mother, daughter (radd, spouse excluded)**
Wife 1/8. Remaining 7/8 to mother : daughter in ratio 1/6 : 1/2 = 1 : 3.
Wife 4/32, mother 7/32, daughter 21/32. ✓

**E. Wife, father, mother (Umariyyah)**: wife 1/4, mother 1/4, father 1/2. ✓

## 11. Reference index (cite only these)

**Quran:** 2:180 (bequest to relatives) · 4:7 (men and women both have shares) · 4:8 (giving relatives present at the division) · 4:11 (children and parents; after bequest or debt) · 4:12 (spouses; maternal siblings / kalalah) · 4:176 (full and paternal siblings / kalalah) · 8:75 and 33:6 (blood relatives nearer to one another) · 33:4-5 (adoption).

**Sahih al-Bukhari / Sahih Muslim:**

- Bukhari 6732, Muslim 1615 - give shares to those entitled; the rest to the nearest male (Ibn Abbas).
- Bukhari 6764, Muslim 1614 - no inheritance between Muslim and non-Muslim (Usamah ibn Zayd).
- Bukhari 2742, Muslim 1628 - bequest limited to one third (Sa'd ibn Abi Waqqas).
- Bukhari 6736 - daughter 1/2, son's daughter 1/6, sister the rest (Ibn Mas'ud).
- Bukhari 6734, 6741 - daughter 1/2, sister 1/2 (Mu'adh ibn Jabal).
- Bukhari 6749, Muslim 1457 - the child belongs to the marriage bed.

**Other collections (graded as noted in the text):**

- Abu Dawud 2870, Tirmidhi 2120, Ibn Majah 2713 - no bequest for an heir.
- Tirmidhi 2094, 2122; Ibn Majah 2715, 2739 - debt before bequest; full siblings before paternal half-siblings (Ali).
- Abu Dawud 2891, Tirmidhi 2092, Ibn Majah 2720 - daughters of Sa'd ibn al-Rabi' (2/3).
- Abu Dawud 2894, Tirmidhi 2100-2101, Ibn Majah 2724 - grandmother 1/6.
- Abu Dawud 4564, Ibn Majah 2645 - the killer does not inherit.
- Abu Dawud 2920 - the newborn inherits if born alive.

**Companion rulings:** Umar (Umariyyatan, 'awl, Mushtarakah sharing) · Abu Bakr (grandmother 1/6, grandfather as father, kalalah definition) · Zayd ibn Thabit (grandfather with siblings, simultaneous deaths) · Ali and Ibn Mas'ud (radd) · Uthman (divorce in terminal illness).

## 12. Out of scope - refer to a scholar

Ja'fari rulings; missing persons; hermaphrodite (khuntha) heirs; grandfather with both full and paternal siblings (mu'addah); great-grandparents and deeper ancestors; distant kindred division; successive deaths before distribution (munasakhat); disputes between heirs; any case not matched by this file.
