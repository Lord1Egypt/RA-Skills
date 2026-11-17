# Translation Tone

> A Chinese-only layer of AI residue: traces of English-first thinking translated too literally into Chinese. The engine exposes four zh-only detector types, and this file explains them in human terms while adding judgment rules that are not easy to capture with regex alone.

These shapes are uncommon in native Chinese prose and are a typical artifact when LLMs trained mostly on English corpora write Chinese. There is no English counterpart. This is a zh-only rule family; see [CATEGORIES.md](../detector/CATEGORIES.md) where `lang=zh`.

## 1. Passive stacks (`zh-passive-stack`)

Engine detection: dense repeated `被` constructions within one sentence (`3+` passive subclauses).

```text
❌ 系统被优化后，性能被显著提升，用户体验被大幅改善，整体被全面重构。
✅ 我们优化了数据库查询，页面加载从 3 秒降到 0.8 秒。
```

Judgment note: ordinary passive voice in academic or experimental prose, such as "实验由 MIT 团队完成", can be valid. The `3+` threshold already avoids single-passive false positives, but even dense passive usage can occasionally be justified in technical description. Judge by scene.

## 2. Long attributive chains (`zh-long-attributive`)

Engine detection: `4+` chained `的` modifiers.

```text
❌ 这是一个由多个相互关联的、复杂的、高度耦合的子系统构成的架构。
✅ 这个架构有几个耦合的子系统。
```

Judgment note: legal or highly formal writing can require longer modifier chains. The density threshold already filters most normal use. Near-threshold cases should be judged by readability, not by the count alone.

## 3. `基于 ...` openers (`zh-translation-opener`)

Engine detection: a sentence beginning with `基于 + noun phrase`.

```text
❌ 基于上述分析，我们可以得出结论……
✅ 上面分析了，结论是……
```

Judgment note: openers such as `基于实测数据` or `基于 RFC 7231` can be legitimate because they point to a concrete basis. The engine only matches the sentence-initial form; whether the phrase is empty depends on the object.

## 4. `通过 ... 来 ...` constructions (`zh-via-to`)

Engine detection: the `通过 X 来 Y` pattern.

```text
❌ 通过优化算法来提升性能，通过减少请求来降低延迟。
✅ 优化算法提升性能；少发请求降延迟。
```

Judgment note: in technical documentation, a phrase like `通过 API 来调用` can be precise because it emphasizes the mechanism. The real test is whether removing `通过…来` makes the sentence clearer.

## Translation-tone patterns that stay at the SKILL layer

- `对于…而言` filler: the engine can detect it, but whether it should be deleted depends on context.
- `在…方面` filler: same story.
- Whole-sentence translationese: long subjects, delayed verbs, stacked modifiers. These usually need rewriting, not surface replacement.

## Relation to protected spans

Translation-tone cleanup must **not** alter:

- commands, code, API names, or identifiers, even if they contain `的` or `被`
- raw error text, such as `"Error: 资源已被占用"` where `被` belongs to the original message
- quoted translation source text inside citation blocks

Fingerprint checks such as `ai-citation-markup` and protected-span checks run before translation-tone handling so the engine does not damage anchored text first and "improve" it second.
