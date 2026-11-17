# Activity Intent Few-shots

Version: `activity-intent-few-shots-v1.0`

Use these examples to understand semantic boundaries before constructing a structured `recommend` call. They are reasoning examples, not an alias table. Never copy a label only because one word overlaps.

## Hard intent and negation

Input: `这周末想做点能真正跑起来的东西，不想只听概念`

- soft: `goal.hands_on`, `value.hands_on`
- must: `goal.hands_on`
- do not infer: `format.workshop`, `format.hackathon`
- reason: the user rejects concept-only content and requires an actionable outcome, but does not name an event format.

Input: `想听专业人士讲 AI 趋势，不需要动手`

- soft: `topic.ai_general`, `goal.learn`, `value.expert_insight`
- must: `topic.ai_general`
- exclude: `value.hands_on`
- reason: the negative phrase applies to hands-on event value; it does not imply a conference or lecture format.

## Goals and values

Input: `想找能带来客户资源的局`

- soft: `goal.acquire_customers`, `value.customer`, `value.resources`
- must: `goal.acquire_customers`
- do not infer: `goal.networking`
- reason: the core outcome is customer acquisition and resources. The casual word `局` is not enough to create a networking goal.

Input: `想看看别人怎么复盘 AI 产品`

- soft: `topic.ai_product`, `goal.learn`, `value.case_study`
- must: `topic.ai_product`
- do not infer: `goal.product_feedback`
- reason: learning from another case differs from requesting feedback on the user's own product.

Input: `我有个 AI 产品，想找人当面挑毛病`

- soft: `topic.ai_product`, `goal.product_feedback`, `value.peer_exchange`
- must: `topic.ai_product`
- reason: the user explicitly brings their own product for feedback.

## Deterministic soft implications

Input: `杭州免费的一人公司活动`

- soft: `topic.opc`, `audience.solo_founder`
- must: `topic.opc`
- location: `hangzhou`
- price: `免费`
- reason: `topic.opc` softly implies `audience.solo_founder`; the implied audience never becomes a hard condition automatically.

Input: `上海只看黑客松，不要大会`

- soft: `format.hackathon`, `value.hands_on`
- must: `format.hackathon`
- exclude: `format.conference`
- location: `shanghai`
- reason: the explicit format is hard; hands-on value is only a soft implication.

Input: `想和做 AI 自媒体的人 Coffeechat`

- soft: `topic.ai_content`, `goal.networking`, `audience.content_creator`, `format.coffee_chat`, `value.peer_exchange`
- must: `topic.ai_content`
- reason: an explicit Coffeechat softly implies peer exchange.

## Specific topics and conservative inference

Input: `北京 AI 展览或影像展映`

- soft: `topic.ai_video`, `format.exhibition`
- must: `topic.ai_video`
- location: `beijing`
- do not add: `topic.ai_general`
- reason: the specific AI media topic suppresses the generic AI topic.

Input: `北京免费 AI 交流`

- soft: `topic.ai_general`, `goal.networking`, `value.peer_exchange`
- must: `topic.ai_general`
- location: `beijing`
- price: `免费`
- reason: use generic AI only because no more specific AI subject is present.

Input: `我不社牛，想找十几个人认真聊 AI`

- soft: `topic.ai_general`, `goal.networking`, `value.peer_exchange`
- must: `topic.ai_general`
- do not infer: `format.closed_door`, `format.salon`, `format.coffee_chat`
- reason: small-group language does not prove a named event format.

Input: `想找搭子一起做点东西`

- soft: `goal.project_collaboration`
- must: `goal.project_collaboration`
- do not infer: `format.hackathon`, `audience.developer`

Input: `想学 Agent`

- soft: `topic.ai_agent`, `goal.learn`
- must: `topic.ai_agent`
- do not add: `topic.ai_general`, `format.course`
