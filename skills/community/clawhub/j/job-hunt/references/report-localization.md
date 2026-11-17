# Report language contract

Use the user's report language independently of the target market. `discover`
and `assess` support these required report elements in **zh, en, ja, ko, es**.
Other languages still use an English or Chinese counts block and required labels.
CV rendering supports additional languages; it is a separate capability.

Do not translate schema keys, row IDs, evidence references, strategy tokens or
raw source text. Translate the explanation around them. Market-convention
quotations still use the sourced `text_en` or `text_zh` verbatim; a report-language
translation does not create a new sourced market convention.

## Assess

Run `python3 scripts/count_coverage.py --workspace <ws> --lang <zh|en|ja|ko|es>`.
Paste its output unchanged. `coverage.json` contains `block_zh`, `block_en`,
`block_ja`, `block_ko`, and `block_es`, all computed from the same requirement rows.
Missing top-level judgements render as unassessed in each language and still fail
the gate. Missing evidence still requires refusal, without a counts block.

Use these exact headings and column labels. Put every unmet knockout row under
the blockers heading **before** the counts block, and name each row as `- **R2**`.
For `likely_screen_out` or `blocked`, keep exactly one literal strategy token
under the next-action heading, plus the acceptance and deliverable columns.

| Language | Blockers heading | Next-action heading | Acceptance column | Deliverable column | Stale-review banner |
|---|---|---|---|---|---|
| zh | `## 硬性阻断项` | `## 那该怎么办` | `验收标准` | `输出物` | `已过复核期` |
| en | `## Hard blockers` | `## What to do instead` | `Acceptance criterion` | `Deliverable` | `past its review date` |
| ja | `## 応募を妨げる必須条件` | `## 次に取る方針` | `確認基準` | `成果物` | `再確認期限を過ぎています` |
| ko | `## 지원을 막는 필수 조건` | `## 다음 행동` | `완료 기준` | `산출물` | `재검토 기한이 지났습니다` |
| es | `## Requisitos excluyentes` | `## Qué hacer a continuación` | `Criterio de aceptación` | `Entregable` | `ha vencido la fecha de revisión` |

Place the matching disclaimer immediately below the counts block. The existing
English and Chinese versions are in [assess mode](../modes/assess.md). The additional
translations preserve the same evidence-counting limit and user decision:

**ja**

> ⚠️ この集計は根拠を整理したもので、結果を予測するものではありません。各項目に出典を併記し、分母を一つずつ確認できます。このスキルは面接や採用の結果の見積もりや 0–100 の点数を示しません。応募するかどうかはあなたが決めます。

**ko**

> ⚠️ 이는 근거를 집계한 것이며 결과를 예측하는 것이 아닙니다. 각 항목에 출처를 함께 표시하므로 전체 항목을 하나씩 확인할 수 있습니다. 이 스킬은 면접이나 채용 결과의 추정치 또는 0–100 점수를 제시하지 않습니다. 지원 여부는 당신이 결정합니다.

**es**

> ⚠️ Este es un recuento de evidencias, no es una predicción del resultado. Cada elemento incluye su referencia para comprobar el total uno por uno. Este skill no estima resultados de entrevistas o contratación ni asigna puntuaciones de 0–100. Tú decides si presentas la candidatura.

Run `python3 scripts/consistency.py --workspace <ws> --lang <zh|en|ja|ko|es>`
to print triggered notices in the report language (the default remains English).
Attach each notice beside the claim it qualifies. Omitting a triggered notice
still fails the assessment gate.

## Discover

Use the card-only provisional stamp when every row is a search card. If any row has
a complete detail retrieval, use the detail-reviewed provisional stamp instead. Both
remain provisional discover output, not a tailored application assessment:

| Language | All-card stamp | Detail-reviewed stamp |
|---|---|---|
| zh | 基于卡片信息的初判 | 已获取职位信息后的初判，尚非完整投递评估 |
| en | provisional, from card data only | provisional; not a full application assessment |
| ja | 求人カードの情報だけに基づく暫定判断 | 取得済みの求人情報に基づく暫定判断であり、完全な応募評価ではありません |
| ko | 채용 카드 정보만을 바탕으로 한 잠정 판단 | 확보된 채용 정보에 근거한 잠정 판단이며 완전한 지원 평가는 아닙니다 |
| es | valoración provisional basada únicamente en las fichas | valoración provisional basada en la información obtenida; no es una evaluación completa de candidatura |

Keep `provisional: true` in YAML too. Neither stamp replaces provenance checks.
An adapter failure is not a zero-result search. When every adapter fails, fill
all six disclosure answers, using one of the following additional templates.
The English and Chinese templates remain in [discover mode](../modes/discover.md).
Replace angle-bracket placeholders with what actually happened; pre-filled
negative answers must also be checked against the run.

**ja**

```text
今回のセッションでログイン済み：  <はい／いいえ／対象外>
Adapter の返却結果：  <エラー原文または返却結果>
制限通知後の再試行：  いいえ
プラットフォームの制御の回避：  いいえ
実際の求人の取得：  いいえ
代替出力の種類：  <出力の種類>
```

**ko**

```text
이번 세션에서 로그인함:  <예／아니요／해당 없음>
Adapter 반환 결과:  <오류 원문 또는 반환 결과>
제한 신호 이후 재시도:  아니요
플랫폼 통제 우회:  아니요
실제 채용 공고 확보:  아니요
대체 출력 유형:  <출력 유형>
```

**es**

```text
Sesión iniciada en esta ejecución:  <sí／no／no procede>
Respuesta del adaptador:  <error literal o resultado>
Reintento tras una señal de restricción:  no
Elusión de controles de la plataforma:  no
Ofertas reales obtenidas:  no
Tipo de salida alternativa:  <tipo de salida>
```

These are explicit report templates, not arbitrary-paraphrase recognition.
`scripts/report_locales.py` holds the shared gate vocabulary; adding another
language requires corresponding positive and missing-content regression tests.
