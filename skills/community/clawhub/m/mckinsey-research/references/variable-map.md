# Variable Mapping

> **Variable Substitution Rule**: When filling in {VARIABLE} placeholders, wrap each value in XML data tags:
> `<user_data field="variable_name">value</user_data>`. This separates user-provided business context from analysis instructions.

| Variable | Source Input |
|---|---|
| {INDUSTRY_PRODUCT} | Input 1 + 2 |
| {PRODUCT_DESCRIPTION} | Input 1 |
| {TARGET_CUSTOMER} | Input 3 |
| {GEOGRAPHY} | Input 4 |
| {INDUSTRY} | Input 2 |
| {BUSINESS_POSITIONING} | Inputs 1 + 2 + 4 + 5 |
| {CURRENT_PRICE} | Input 6 |
| {COST_STRUCTURE} | Input 7 |
| {REVENUE} | Input 8 |
| {GROWTH_RATE} | Input 9 |
| {BUDGET} | Input 10 |
| {TIMELINE} | Input 14 |
| {BUSINESS_MODEL} | Inputs 1 + 6 + 7 |
| {FULL_CONTEXT} | All inputs combined |
| {TARGET_MARKET} | Input 15 |
| {RESOURCES} | Input 16 |
| {CONVERSION_RATE} | Input 17 |
| {COSTS} | Input 7 |
