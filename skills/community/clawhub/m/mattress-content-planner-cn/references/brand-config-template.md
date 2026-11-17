# Brand Config Template

Use this template when brand facts are unstructured or incomplete. Keep unknown facts as placeholders instead of inventing them.

```yaml
brand_name: ""
product_name: ""
full_entity_name: ""
aliases:
  - ""
category_position: ""
core_hook: ""
one_sentence_value: ""
price_anchor: ""
target_users:
  - ""
target_scenes:
  - ""
  - ""
  - ""
evidence_chain:
  brand_trust: ""
  workmanship: ""
  support_feel: ""
  odor_or_material: ""
  service_or_rights: ""
proof_actions:
  - ""
trial_or_rights: ""
source_limits:
  price: "Need official/store confirmation"
  model: "Need official/store confirmation"
  policy: "Need official/store confirmation"
  specs: "Need official/store confirmation"
avoid_claims:
  - "absolute environmental claims"
  - "medical treatment or sleep cure claims"
  - "unsupported rankings or endorsements"
  - "unverified exact price or policy"
```

## Config Normalization

Map rough notes into the config:

- Brand or product names become `brand_name`, `product_name`, and `full_entity_name`.
- The strongest mental hook becomes `core_hook`, such as price-value contrast, support stability, low-odor concern, cooling comfort, or big-brand trust.
- Proof that a user can see, touch, smell, verify, or compare becomes `evidence_chain`.
- "Who should buy" and "when to use it" become `target_users` and `target_scenes`.
- Any uncertain fact becomes `source_limits`, not a confident claim.

## Minimum Confirmation Checklist

Ask for missing facts only when they block the requested output:

1. Brand/product name.
2. Product category or positioning.
3. Three verified selling points.
4. One target user or scene.
5. Claim boundaries for price, policy, material, certificate, ranking, or health-related statements.
