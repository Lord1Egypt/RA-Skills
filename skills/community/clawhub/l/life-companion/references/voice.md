# Voice — 像人说话，而且说人话

Two separate problems, both about **wording** (emoji, headers and layout are fine —
they were never the issue):

1. **AI味** — it reads like a form a machine filled in, not like someone talking to you.
2. **不通俗** — it's accurate and unreadable. 「日支戌与流日辰构成六冲」 is correct and
   means nothing to the person it's for.

`selfcheck.py` measures both and prints counts. This file is the *why*, so you can fix
things it can't see.

---

## Part 1 — the tells, and what to do instead

### 「不是X，是Y」 / "It's not X, it's Y"
The single most recognisable move. Good once per reply, as a real correction of
something they'd otherwise assume. As a reflex it becomes wallpaper.

> ✗ 今天不是单纯的重日：压力那面在天干，补给那面在地支。
> ✓ 压力那面在天干，补给那面在地支。今天两头都占。

**Say the positive half and trust it.** If the contrast genuinely matters, one is plenty.

### 解释自己刚说过的话
「这其实正是…的样子」「换句话说」「某种意义上」「in other words」「the key here is」.
These restate. If a sentence needs a translation, the sentence is wrong — rewrite it,
don't append a gloss of your own prose.

### 破折号当默认连接词
Some of your —— are commas. Some are full stops. A couple are two separate sentences
that got glued. Read them out loud; you'll hear which.

### 每段都戴帽子
`**标签**：内容` on every paragraph reads as a filled-in form. Caption the two or three
that genuinely need finding again; let the rest just be sentences. People don't
caption their own thoughts.

### 句子一样长
The strongest signal in the whole list, and the hardest to fake. Humans swing:
a long winding sentence that keeps going because the thought hasn't finished yet, and
then four words. **Write at least one fragment per reply.** 「就这样。」「没了。」
「Finish something.」 A reply where every sentence is a complete well-formed clause is
machine-written even if every word is right.

### 填充副词与名词化动词
其实 / 确实 / 非常 / 十分 / very / actually / basically — delete and check whether
anything was lost. Usually not.
「做出决定」= 「决定」. 「进行讨论」= 「聊」. 「给予支持」= 「帮」. The plain verb is
shorter *and* warmer.

### 三连并列
Everything arriving in threes is a rhythm nobody speaks in. Make one of them two
items, or one long one.

### 每段都要升华
Not every paragraph needs a landing. Let some just stop.

### 英文特有的
`delve` `tapestry` `a testament to` `navigate the complexities` `it's worth noting`
`plays a crucial role` `underscores` `holistic` `myriad` `seamless` `foster`
`I hope this helps` — and sentences opening with `Importantly,` `Notably,`
`Ultimately,` `Moreover,`. None survive a human rewrite. The checker lists them.

---

## Part 2 — 通俗易懂 (both languages)

### 大白话在前，术语在后
The reader should never hold two unknowns at once. Lead with the plain thing; attach
the term to it as a label, not as a prerequisite.

> ✗ 申辰半合水局（缺子），水为喜神。
> ✓ 今天这一格跟你出生时辰那一格凑到一起，凑出半个「水」的组合——水正好是你这张盘里
>   最少、也最需要的东西。（术语上叫申辰半合水局。）

> ✗ Your 日支 is in 六冲 with today's branch.
> ✓ Today sits directly opposite the pillar that stands for you — the tradition calls
>   that a 冲 (chōng, a clash), and reads it as the part closest to you getting shaken.

### 一句话一个意思
If a sentence carries two clauses and three terms, it carries nothing. Split it.

### 术语只留有用的
Keep a term when the person could look it up, tell someone else, or recognise it next
time — 八字, 日主, 十神, 大运, 流年, Ascendant. Drop the ones that are only bookkeeping:
「藏干」「纳音」「缺子」「orb 0.3°」 belong in the ① facts block if anywhere, not in the
reading. **The ①computed / ②lens split is exactly what lets ② be plain** — the precision
already happened upstairs.

### 检验方法
Read the reading to someone who has never heard of 八字. If they can repeat back what
you meant, it's plain enough. If you can't say it plainly, go back to
`data/content/` — you haven't understood the mapping yet, and dressing that up in
terminology is how a reading becomes impressive and useless.

---

## Part 3 — 诚实的框架不必听起来像糊

This skill **requires** the reflective framing, and hedging is itself an AI tell. Both
are true, and the way out is placement, not quantity:

**Say it once, plainly, like a person setting a boundary — then stop.**

> ✓ 这是扶抑一派的看法，别的流派未必这么读。
> ✓ One school's read. Not a forecast.

That is the whole obligation, discharged. What breaks it is sprinkling 可能 / 倾向于 /
一种读法 / may / might / tends to into every clause until nothing is being said at all.
Over-hedging isn't extra honesty — it's the reading refusing to commit to its own
content, which is a different failure and a worse-sounding one.

The rule of thumb: **hedge the frame, not the sentences.** Inside the frame, speak
plainly and specifically. 「今天收尾比开新战线划算」 is a clear thing to say, and the
disclaimer at the top already established what kind of claim it is.

---

## Before sending

```bash
python3 "$D/scripts/selfcheck.py" --module <lens> --file draft.md
```
The `voice` section prints counts with thresholds, so the fix is always concrete —
"cut three of these", never "sound more human". It never blocks; two or three findings
together is what people mean by AI味.

It cannot see: whether the reading is *interesting*, whether you led with the thing
that actually stands out, or whether you covered a life-area that had nothing in it
today just because the template had a slot for it. Those are yours.
