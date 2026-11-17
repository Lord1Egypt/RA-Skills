# Kanji and Kana — Which Script, and Why

Japanese chooses between four scripts for the same word, and the choice carries register, readability and word boundaries at once. Governed by `kanji_density` and `okurigana_rule`.

**Contents:** [What Each Script Does](#what-each-script-does) · [The 30% Target](#the-30-target) · [The ひらく List](#the-ひらく-list) · [送り仮名](#送り仮名) · [常用漢字 and Beyond](#常用漢字-and-beyond) · [Katakana Beyond Loanwords](#katakana-beyond-loanwords) · [Long Vowels in Katakana](#long-vowels-in-katakana) · [ルビ](#ルビ) · [Romanization](#romanization) · [変換ミス](#変換ミス) · [What Gets Written Down](#what-gets-written-down)

## What Each Script Does

| Script | Carries | Effect of overuse |
|---|---|---|
| 漢字 | Content words, 漢語 vocabulary, semantic density | Stiff, bureaucratic, hard to scan |
| ひらがな | Grammar, particles, 和語, softness | Childish, and word boundaries disappear |
| カタカナ | Loanwords, onomatopoeia, emphasis, technical terms, some names | Reads as advertising or as a foreigner speaking |
| ローマ字 | Brands, acronyms, product names, URLs | Reads as untranslated |

The script alternation is what does the work of spaces: 私は今日会社に行きます parses instantly because the kanji mark where the content words are. An all-hiragana sentence (わたしはきょうかいしゃにいきます) is legible and slow, which is exactly why over-opening a text hurts readability as much as over-closing it.

## The 30% Target

Editorial rule of thumb, not a standard: **漢字3割・かな7割** is the traditional publishing target. Compute it as `kanji characters ÷ total characters` over a sample paragraph when a text feels heavy.

| Register | Working range |
|---|---|
| Chat, casual social copy | 20-25% |
| note, blog, general web | 25-30% |
| Business email, news | 30-35% |
| Academic, legal, 公文書 | 35-40%+ |

Two directions of failure and their fixes:
- **Too heavy** (a 漢語 chain: 当該業務遂行上必要不可欠) — replace the 漢語 with 和語 (`register.md`) before opening anything. Opening a kanji-heavy sentence into kana makes it worse.
- **Too light** — usually a text that opened content words rather than function words. Open こと, とき, ため; keep 会議, 資料, 確認.

`kanji_density` moves the target: `light` aims at the bottom of the band and applies the ひらく list aggressively, `heavy` aims at the top and keeps 出来る, 下さい and 頂く closed where the house style permits.

## The ひらく List

"ひらく" means writing a word in kana that could be written in kanji. This is not taste — the same words are opened by essentially every Japanese style guide (共同通信's 記者ハンドブック is the canonical published one), and doing it is the difference between a text that reads professionally and one that reads like a legal notice.

**Always open (formal nouns and auxiliaries used grammatically):**

| Closed | Open | Note |
|---|---|---|
| 事 | こと | 事 stays only in 事件, 事情, 出来事 |
| 物 | もの | 物 stays for physical objects: 荷物, 建物 |
| 時 | とき | 時 stays for clock time: 3時, 時間 |
| 所 | ところ | 所 stays in 場所, 住所 |
| 為 | ため | Always open |
| 事が出来る | ことができる | Or just the 可能形 (`ai-tells.md`) |
| 出来る | できる | Always open as a verb |
| 下さい | ください | Open as an auxiliary (見てください); 下さい only for "give me" |
| 頂く | いただく | Open as an auxiliary (見ていただく); 頂く for physically receiving |
| 致します | いたします | Open as an auxiliary (お願いいたします); 致す only as a full verb |
| 有る / 無い | ある / ない | Always open |
| 良い | よい / いい | Open in most prose |
| 沢山 | たくさん | Always open |
| 是非 | ぜひ | Always open |
| 又 / 尚 / 但し | また / なお / ただし | Connectives are opened |
| 更に / 既に | さらに / すでに | Always open |
| 全て | すべて | Both are common; pick one |
| 予め / 敢えて / 概ね | あらかじめ / あえて / おおむね | Always open |
| 出来上がる | できあがる | Always open |
| 分かる | わかる / 分かる | Contested; 分かる is common, 解る/判る are marked |

**Keep closed (content words):** 確認, 資料, 会議, 提案, 検討, 対応, 連絡, 変更, 導入, 納品 — and every noun with real semantic weight. Opening these is what produces the childish reading.

The pattern behind the list: **a word used for its grammatical function is opened; a word used for its meaning is closed.** 見て頂く (auxiliary → open) vs お土産を頂く (verb → closed) is the same word making the same distinction.

## 送り仮名

Where the kana ends and the kanji begins. Governed by `okurigana_rule`, and the choice must be applied to every occurrence.

| Word | 本則 (常用漢字表の送り仮名) | 許容 / 慣用 |
|---|---|---|
| おこなう | 行う | 行なう |
| もうしこみ | 申し込み | 申込み / 申込 |
| うけつけ | 受け付け | 受付け / 受付 |
| とりひき | 取り引き | 取引き / 取引 |
| ひきわたし | 引き渡し | 引渡し / 引渡 |
| くみあわせ | 組み合わせ | 組合せ / 組合 |
| よみとる | 読み取る | 読取る |

The pattern: **verbs keep their okurigana (行う, 申し込む); compound nouns lose it progressively, and the fully-closed form is the one used in official terms, forms and signage** (受付, 取引, 申込). So 申し込みはこちら on a web page and 申込書 as the name of the document are both correct in the same text — the noun is a term, the verb phrase is not.

The one thing that is always wrong is inconsistency inside one document: 受付 in the heading and 受け付け in the body.

## 常用漢字 and Beyond

- **常用漢字表** (2010 revision) lists 2,136 characters, and it is what newspapers, textbooks and 公文書 restrict themselves to. A character outside it is either opened into kana, replaced, or given ルビ.
- **The 交ぜ書き problem**: when only one character of a compound is outside the list, publications historically wrote the other in kana — 破たん, ら致, 隠ぺい — which is widely disliked as unreadable. Modern practice prefers the full kanji with ルビ, or a different word entirely.
- **人名用漢字** are permitted in given names and not in general text; a name may legally contain characters no newspaper would print.
- **旧字体 and 異体字** in surnames (髙, 﨑, 濵, 邊/邉) are the writer's actual name and are not interchangeable with the simplified form. Copy the character from their own signature; a substitution is noticed by the person it belongs to, every time (`punctuation.md`, `numbers-and-names.md`).

## Katakana Beyond Loanwords

Katakana does five jobs and only the first is taught:

1. **Loanwords**: コーヒー, デプロイ, プロジェクト.
2. **Onomatopoeia**, especially sharp or mechanical sounds: ガチャ, ピカピカ (`onomatopoeia.md`).
3. **Emphasis**, the equivalent of italics: これはヤバい, 完全にアウト. Writing a native word in katakana makes it stand out and adds a slightly detached or ironic tone.
4. **Technical and scientific terms**, including animal and plant names: ネコ, イネ, ヒト — standard in scientific writing, and jarring in prose.
5. **Register signalling**: ダメ, オレ, ワタシ in fiction to mark a voice as blunt, foreign, robotic or non-native (`fiction.md`).

The trap for a model: **katakana is not a transliteration device.** An English word not established as a loanword, written in katakana, reads as untranslated rather than as Japanese — and the fix is to find the Japanese word, not to spell the English one more carefully.

## Long Vowels in Katakana

The single most common 表記ゆれ in Japanese technical writing:

| Both exist | Convention |
|---|---|
| サーバ / サーバー | JIS-derived engineering style drops the final ー on 3+ mora words; general and journalistic style keeps it |
| ユーザ / ユーザー | Same |
| コンピュータ / コンピューター | Same |
| インタフェース / インターフェース | Same |
| プリンタ / プリンター | Same |

内閣告示の外来語の表記 and 記者ハンドブック keep the long vowel; older JIS documentation and much Japanese engineering writing drops it. **Neither is wrong; both in one document is.** Settle it once in `conventions.hyoki` and apply it everywhere, including inside compound terms.

## ルビ

Furigana, governed by `furigana`.

- **総ルビ** (every kanji) is for children's books and for text aimed at learners.
- **パラルビ** (selected kanji) is the normal case: names, 難読 kanji, and anything the reader has no reason to know.
- **Names always take ルビ on first appearance** in a document that will be read aloud, in a programme, or in anything where a stranger has to pronounce them (`speaking.md`).
- **In HTML** ルビ is `<ruby>`; in plain text it is written in （）after the word: 東海林（しょうじ）.
- **A wrong ルビ is worse than none**, because it is an assertion. Never generate one for a name from the characters (below).

## Romanization

| System | Use | 例 |
|---|---|---|
| ヘボン式 (Hepburn) | Passports, signage, almost all English-language use | Shinjuku, Fuji, Chichibu |
| 訓令式 (Kunrei) | School instruction, some linguistics | Sinzyuku, Huzi, Titibu |
| 日本式 | Historical, rare | — |

Use Hepburn unless there is a specific reason not to. Within Hepburn, the decisions that come up:

- **Long vowels**: passport style writes them out with no marker (Ono for 大野 and 小野 alike, Sato for 佐藤); academic style uses macrons (Ōno, Satō); web style often doubles (Ohno, Satoh). A person's own spelling of their own name overrides every rule — record it in `### Name Readings` with its source (`numbers-and-names.md`).
- **ん before b/m/p**: Hepburn traditionally writes m (Shimbashi), modern passport style writes n (Shinbashi). Both are current.
- **Particles**: は is *wa*, へ is *e*, を is *o* when romanizing text.
- **Name order**: 文化庁 and the government moved to surname-first with the surname in capitals for official use (YAMADA Taro) from 2020; most private-sector English writing still uses given-name-first. Pick per document and state it if it could be ambiguous.

## 変換ミス

IME conversion errors are the native writer's characteristic typo, which means they read as careless rather than as foreign — and a spell-checker will not catch a single one, because every candidate is a real word.

| Confusion set | Distinction |
|---|---|
| 以外 / 意外 | other than / unexpected |
| 保証 / 保障 / 補償 | guarantee / safeguard / compensate |
| 制作 / 製作 | creative work / manufacturing |
| 対象 / 対照 / 対称 | target / contrast / symmetry |
| 追求 / 追及 / 追究 | pursue (a goal) / pursue (responsibility) / investigate |
| 早い / 速い | early / fast |
| 図る / 計る / 測る / 諮る | plan / count / measure / consult a body |
| 収める / 納める / 治める / 修める | store / deliver / govern / master |
| 変える / 換える / 替える / 代える | change / exchange / replace / substitute |
| 移動 / 異動 | physical move / personnel transfer |

The full confusion set and the sweep procedure are in `proofreading.md`. The one to check first in business writing is 保証/保障/補償, because it appears in contracts and the wrong one changes the obligation.

## What Gets Written Down

Destinations, all in `memory-template.md`:

- **Every 表記 decision** — the long-vowel rule, the ひらく exceptions the house keeps closed, the 送り仮名 form for a term that recurs → `conventions.hyoki` in `config.yaml`. It is a declaration, and it applies to every occurrence from then on.
- **A term's settled rendering** — which script, which katakana spelling, whether it stays in Latin → `### Terms` or `### Keep In Latin` in the glossary.
- **A character that a system cannot render** — 髙 in a surname, a 機種依存文字 in a client's company name → `## Environment`, with what was substituted and who noticed.
- **A house style sheet** the user or the client supplies → `artifacts/hyoki-house-rules.md` as given, with its source and date, and its `## Boxes` line.
