# Product List And Create Params

The product list is the source of truth for task creation. The runtime must fetch it before model binding.

## Fields That Matter

- `attribute_id`: selected from the matched `credit_rules` entry; create calls fail if this is stale or zero
- `model_version`: the product-list leaf `id`; this is the version key the backend expects in create
- `form_config`: default parameter values for the selected product leaf
- `credit_rules.attributes`: rule-specific parameter combinations that can change `attribute_id` and credit cost

## Binding Rules

`extract_model_params()` in `shared/catalog.py`:

- resolves default `form_config` values first
- selects the best matching credit rule based on those defaults
- keeps `rule_attributes`, `form_params`, and `all_credit_rules` so later create logic can merge safely

`create_task()` in `shared/client.py` then builds the request in this order:

1. required rule attributes
2. `form_config` defaults
3. canonical values from the matched credit rule
4. user `extra_params` that do not override canonical rule values

## Payload Construction Constraints

- always send the raw product-list `model_id` when available if that is what the backend expects for request binding
- always send `model_version` from the bound leaf, not the friendly model name
- always include `cast.points` and `cast.attribute_id`
- `text_to_video` should not keep stray image-only payload fields
- Pixverse variants may need an inferred `model` parameter when `form_config` omits it; current code derives it from the product name

If you skip the product-list bind step, the most common failure mode is an attribute/rule mismatch on create.
