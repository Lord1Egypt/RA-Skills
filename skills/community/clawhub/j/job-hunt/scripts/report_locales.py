"""Reader-facing report text shared by renderers and gates.

Machine keys, evidence references and verdict enums stay in vocab.py. These are
translations of the same report contract, not language-specific scoring rules.
Keep required wording here so an author can use a native-language template and
the gate can check it without asking for an English sentence in that document.
"""
from __future__ import annotations

import vocab

LANGUAGES = ("zh", "en", "ja", "ko", "es")

GATE_TEXT = {
    "zh": {
        "disclaimer": "不是对结果的预判", "verdict": "投递建议：",
        "blockers": "## 硬性阻断项", "strategy": "## 那该怎么办",
        "acceptance": "验收标准", "deliverable": "输出物",
        "stale": "已过复核期", "provisional": "基于卡片信息的初判",
        "detail_provisional": "已获取职位信息后的初判，尚非完整投递评估",
        "disclosure": ("本次会话已登录：", "Adapter 返回：", "收到限制信号后重试：",
                       "绕过任何平台控制：", "取得真实岗位：", "降级输出类型："),
        "empty": ("没有匹配", "没有结果", "未找到", "无匹配", "零结果"),
    },
    "en": {
        "disclaimer": "not a forecast of the outcome", "verdict": "apply verdict:",
        "blockers": "## Hard blockers", "strategy": "## What to do instead",
        "acceptance": "Acceptance criterion", "deliverable": "Deliverable",
        "stale": "past its review date", "provisional": "provisional, from card data only",
        "detail_provisional": "provisional; not a full application assessment",
        "disclosure": ("Logged in this session:", "Adapter returned:",
                       "Retried after a stop signal:", "Bypassed any platform control:",
                       "Obtained real postings:", "Degraded output type:"),
        "empty": ("no results", "no matching", "nothing found", "found nothing"),
    },
    "ja": {
        "disclaimer": "結果を予測するものではありません", "verdict": "応募の判断：",
        "blockers": "## 応募を妨げる必須条件", "strategy": "## 次に取る方針",
        "acceptance": "確認基準", "deliverable": "成果物",
        "stale": "再確認期限を過ぎています",
        "provisional": "求人カードの情報だけに基づく暫定判断",
        "detail_provisional": "取得済みの求人情報に基づく暫定判断であり、完全な応募評価ではありません",
        "disclosure": ("今回のセッションでログイン済み：", "Adapter の返却結果：",
                       "制限通知後の再試行：", "プラットフォームの制御の回避：",
                       "実際の求人の取得：", "代替出力の種類："),
        "empty": ("検索結果なし", "該当する求人はありません", "求人が見つかりませんでした"),
    },
    "ko": {
        "disclaimer": "결과를 예측하는 것이 아닙니다", "verdict": "지원 판단:",
        "blockers": "## 지원을 막는 필수 조건", "strategy": "## 다음 행동",
        "acceptance": "완료 기준", "deliverable": "산출물",
        "stale": "재검토 기한이 지났습니다",
        "provisional": "채용 카드 정보만을 바탕으로 한 잠정 판단",
        "detail_provisional": "확보된 채용 정보에 근거한 잠정 판단이며 완전한 지원 평가는 아닙니다",
        "disclosure": ("이번 세션에서 로그인함:", "Adapter 반환 결과:",
                       "제한 신호 이후 재시도:", "플랫폼 통제 우회:",
                       "실제 채용 공고 확보:", "대체 출력 유형:"),
        "empty": ("검색 결과 없음", "일치하는 공고가 없습니다", "공고를 찾지 못했습니다"),
    },
    "es": {
        "disclaimer": "no es una predicción del resultado", "verdict": "recomendación de candidatura:",
        "blockers": "## Requisitos excluyentes", "strategy": "## Qué hacer a continuación",
        "acceptance": "Criterio de aceptación", "deliverable": "Entregable",
        "stale": "ha vencido la fecha de revisión",
        "provisional": "valoración provisional basada únicamente en las fichas",
        "detail_provisional": "valoración provisional basada en la información obtenida; no es una evaluación completa de candidatura",
        "disclosure": ("Sesión iniciada en esta ejecución:", "Respuesta del adaptador:",
                       "Reintento tras una señal de restricción:", "Elusión de controles de la plataforma:",
                       "Ofertas reales obtenidas:", "Tipo de salida alternativa:"),
        "empty": ("sin resultados", "no se encontraron ofertas", "no hay ofertas coincidentes"),
    },
}


def anchors(key: str) -> tuple[str, ...]:
    return tuple(GATE_TEXT[lang][key] for lang in LANGUAGES)


# The original en/zh blocks remain byte-compatible with existing assessments.
# The additional blocks use these labels with the same counts and enum values.
CARD_TEXT = {
    "ja": {
        "must": "必須条件の強い根拠", "count": "全{total}項目中{count}項目", "partial": "部分的", "gap": "不足",
        "no_evidence": "根拠なし", "responsibilities": "裏付けのある主要業務",
        "level": "職位の対応", "effort": "不足を補うための作業量", "not_assessed": "未評価",
        "directions": dict(zip(vocab.LEVEL_DIRECTION, ("上位職", "同等", "下位職", "不明"))),
        "efforts": dict(zip(vocab.EFFORT, ("当日", "一晩", "数日", "解消できない"))),
        "verdicts": dict(zip(vocab.VERDICTS + (vocab.REFUSAL,),
                             ("強く応募を勧める", "応募する価値がある", "挑戦枠", "書類選考で落ちる可能性が高い",
                              "必須条件が未充足", "根拠不足のため判断しない"))),
    },
    "ko": {
        "must": "필수 요건의 강한 근거", "count": "{total}개 중 {count}개", "partial": "부분 충족", "gap": "부족",
        "no_evidence": "근거 없음", "responsibilities": "근거가 확인된 핵심 업무",
        "level": "직급 적합성", "effort": "부족한 부분을 보완하는 데 드는 노력", "not_assessed": "미평가",
        "directions": dict(zip(vocab.LEVEL_DIRECTION, ("상위 직급", "동일 직급", "하위 직급", "불명확"))),
        "efforts": dict(zip(vocab.EFFORT, ("당일", "하룻밤", "수일", "보완 불가"))),
        "verdicts": dict(zip(vocab.VERDICTS + (vocab.REFUSAL,),
                             ("적극 지원 권장", "지원할 가치 있음", "도전 지원", "서류 탈락 가능성이 높음",
                              "필수 조건 미충족", "근거 부족으로 판단 보류"))),
    },
    "es": {
        "must": "Requisitos obligatorios con evidencia sólida", "count": "{count} de {total}", "partial": "parcial",
        "gap": "carencia", "no_evidence": "sin evidencia", "responsibilities": "Funciones principales acreditadas",
        "level": "Correspondencia de nivel", "effort": "Esfuerzo para cubrir carencias", "not_assessed": "sin evaluar",
        "directions": dict(zip(vocab.LEVEL_DIRECTION, ("ascenso", "mismo nivel", "descenso", "incierto"))),
        "efforts": dict(zip(vocab.EFFORT, ("en el día", "una tarde", "varios días", "no subsanable"))),
        "verdicts": dict(zip(vocab.VERDICTS + (vocab.REFUSAL,),
                             ("Candidatura muy recomendable", "Merece la pena postularse", "Candidatura ambiciosa",
                              "Probable descarte inicial", "Requisito excluyente incumplido", "Sin conclusión por falta de evidencia"))),
    },
}

# Full notices are emitted by consistency.py; anchors are deliberately narrower
# so line wrapping and count changes do not alter the meaning the gate checks.
NOTICE_TEXT = {
    "NOTICE_WORK_AUTH_CONFLICT": {
        "ja": ("この二つは矛盾しているように見えます", "求人は既存の就労許可を求めていますが、あなたはスポンサーの支援が必要と申告しています。この二つは矛盾しているように見えます。雇用主に確認してください。このスキルは法的資格を判断しません。"),
        "ko": ("두 조건이 서로 충돌하는 것으로 보입니다", "공고는 기존 취업 허가를 요구하지만, 당신은 고용주의 후원이 필요하다고 밝혔습니다. 두 조건이 서로 충돌하는 것으로 보입니다. 고용주에게 확인하세요. 이 스킬은 법적 자격을 판단하지 않습니다."),
        "es": ("Estas dos condiciones parecen contradictorias", "La oferta exige autorización de trabajo vigente y has declarado que necesitas patrocinio. Estas dos condiciones parecen contradictorias; confírmalo con la empresa. Este skill no determina la elegibilidad legal de nadie."),
    },
    "NOTICE_WORK_AUTH_VERIFY": {
        "ja": ("必ずしも矛盾するとは限りません", "求人は既存の就労許可を求めていますが、あなたの経路は学生・卒業生向け、または一時的なものです。必ずしも矛盾するとは限りません。その経路が認められるか雇用主に確認してください。"),
        "ko": ("반드시 충돌하는 것은 아닙니다", "공고는 기존 취업 허가를 요구하며, 당신은 학생·졸업생 또는 임시 경로를 이용합니다. 반드시 충돌하는 것은 아닙니다. 해당 경로가 인정되는지 고용주에게 확인하세요."),
        "es": ("No es necesariamente una contradicción", "La oferta exige autorización de trabajo vigente y tu vía es de estudiante, graduado o temporal. No es necesariamente una contradicción; pregunta a la empresa si acepta esa vía."),
    },
    "NOTICE_VERDICT_EFFORT": {
        "ja": ("判断と必要な作業量が矛盾しています", "判断と必要な作業量が矛盾しています。選考条件を既に満たす経歴なら、数日の作業や解消できない不足が残るのは整合しません。上の判断より下の要件表を優先してください。"),
        "ko": ("판단과 예상 노력이 서로 맞지 않습니다", "판단과 예상 노력이 서로 맞지 않습니다. 선발 조건을 이미 충족하는 이력서라면 수일의 작업이나 보완 불가능한 부족이 남아 있어서는 안 됩니다. 위 판단보다 아래 요건표를 기준으로 보세요."),
        "es": ("La recomendación y el esfuerzo estimado no concuerdan", "La recomendación y el esfuerzo estimado no concuerdan: un CV que ya cubre los requisitos no debería necesitar días de trabajo ni cambios imposibles. Da prioridad a las filas de requisitos frente a la etiqueta anterior."),
    },
    "NOTICE_LOOSE_KNOCKOUTS": {
        "ja": ("必須の選考条件として指定されています", "{count} 件が必須の選考条件として指定されています。通常は多くても一つなので、この順序は実際の除外基準ではなく目安として読んでください。"),
        "ko": ("필수 선발 조건으로 표시되어 있습니다", "{count}개 요건이 필수 선발 조건으로 표시되어 있습니다. 대부분의 공고에는 많아야 하나이므로, 아래 순서를 실제 탈락 기준이 아닌 대략적인 순서로 보세요."),
        "es": ("se han marcado como filtros excluyentes", "{count} requisitos se han marcado como filtros excluyentes. La mayoría de las ofertas tienen como máximo uno; interpreta el orden como aproximado, no como los criterios que realmente descartan candidaturas."),
    },
    "NOTICE_GAP_ACTIONS": {
        "ja": ("一部の助言が行動リストに含まれていません", "応募前に補える不足は {gaps} 件ですが、行動は {actions} 件しかありません。一部の助言が行動リストに含まれていません。"),
        "ko": ("일부 조언이 행동 목록에 포함되지 않았습니다", "지원 전에 보완할 수 있는 부족은 {gaps}개인데 행동 목록에는 {actions}개만 있습니다. 일부 조언이 행동 목록에 포함되지 않았습니다."),
        "es": ("parte del consejo no aparece en esta lista", "Hay {gaps} carencias que pueden cubrirse antes de postularse, pero el plan enumera {actions} acciones; parte del consejo no aparece en esta lista."),
    },
}
