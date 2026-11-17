# HelloFresh read recipes (curl + jq)

Prerequisite (SKILL.md § Core pattern): the token loaded into `~/.hellofresh-fpx`
and the `hf` function defined.

```sh
S=~/.hellofresh-fpx; T=~/.claude/skills/hellofresh-fpx/scripts/hf-token.mjs
(umask 077; fpx cookies apiV2Auth -p hellofresh --storage-subdomain www > "$S/cookie.json") && node "$T" load "$S"
hf() { curl -sS --fail-with-body -H @"$S/auth.header" -H 'accept: application/json' "https://www.hellofresh.com/gw$1"; }
Q='country=US&locale=en-US'
```

Records carry the account holder's name, email, addresses and payment token.
Every recipe below projects to the fields it needs; never dump a whole
subscription or delivery into a chat.

Money is in US **cents**, except the calculator's answer, which is in dollars. Weeks are ISO weeks (`2026-W49`). `deliveryOption`
handles read `US-<weekday 1=Mon..7=Sun>-<from HHMM>-<to HHMM>`.

## Subscription

```sh
hf "/api/customers/me/subscriptions?$Q" | jq '.items[] | {id, sku: .product.sku, unitPriceCents: .product.unitPrice,
  preset, deliveryOption: .deliveryOption.handle, deliveryWeekday, deliveryInterval, nextDeliveryWeek,
  nextCutoffDate, nextModifiableDeliveryWeek, customerPlanId, isActive, pausedAt,
  voucher: (.voucherInfo | if . then {code, is_active} else null end)}'
SUB=$(hf "/api/customers/me/subscriptions?$Q" | jq -r '.items[0].id')
PLAN=$(hf "/api/customers/me/subscriptions?$Q" | jq -r '.items[0].customerPlanId')
```

One subscription by id (same shape):

```sh
hf "/api/subscriptions/$SUB?$Q" | jq '{id, sku: .product.sku, deliveryOption: .deliveryOption.handle, deliveryInterval}'
```

## Upcoming deliveries (about 7 weeks)

```sh
hf "/api/customers/me/deliveries?$Q" | jq '.items | sort_by(.id)[] | {week: .id, deliveryDate, cutoffDate, status,
  sku: .product.handle, meals: .product.specs.meals, people: .product.specs.size,
  priceCents: .product.price, feeCents: .product.specialFee, shippingCents: .product.shippingPrice}'
```

`status`: `RUNNING` = coming, `PAUSED` = skipped, `DELIVERED`, `DONATED`.
One line per week:

```sh
hf "/api/customers/me/deliveries?$Q" | jq -r '.items | sort_by(.id)[] |
  "\(.id) — \(.deliveryDate[0:10]) — \(.status | ascii_downcase), \(.product.specs.meals)×\(.product.specs.size), cutoff \(.cutoffDate[5:10])"'
```

## One delivery week

```sh
W=2026-W49
hf "/api/subscriptions/$SUB/delivery_dates/$W?$Q" | jq '{week: .id, deliveryDate, cutoffDate, status, subStatus,
  sku: .product.handle, productName: .product.productName, allowedActions,
  deliveryOption: .deliveryOption.handle, otherDays: [.availableOneOffOptions[]? | {handle, deliveryDate}]}'
```

## Box sizes on offer

```sh
hf "/api/subscriptions/$SUB/product_options?$Q" | jq -r '.items[].products[] | "\(.handle)\t\(.specs.meals) meals × \(.specs.size) people"'
```

## Customer plan (the permanent box size)

```sh
hf "/api/plans?$Q" | jq '.[] | {id, planType, productHandle: .planItems[0].productHandle}'
```

## Menu weeks

```sh
hf "/menus-service/weeks?$Q" | jq -r '.weeks[]'
```

## A week's menu (with the current picks)

`servings` and `product-sku` are REQUIRED (400 without them) — take both from
that week's delivery, so a one-week size change is respected:

```sh
W=2026-W49
SKU=$(hf "/api/subscriptions/$SUB/delivery_dates/$W?$Q" | jq -r .product.handle)
PEOPLE=$(hf "/api/subscriptions/$SUB/delivery_dates/$W?$Q" | jq -r .product.specs.size)
hf "/my-deliveries/menu?subscription=$SUB&week=$W&locale=en-US&servings=$PEOPLE&product-sku=$SKU&customerPlanId=$PLAN&exclude-feedback=true" > "$S/menu-$W.json"
```

The menu lists base courses AND protein-swap variants (`modularity[].variations[].index`).
Base courses only, seafood first, with the premium per serving:

```sh
jq '([.modularity[]?.variations[]?.index]) as $variants | .meals[] | select(.index as $i | $variants | index($i) | not)
  | {index, name: .recipe.name, headline: .recipe.headline, category: .recipe.category,
     totalTime: .recipe.totalTime, kidFriendly: ([.recipe.tags[]? | .type] | index("family-friendly") != null),
     premiumPerServingCents: (.charge.unitAmount // 0), picked: (.selection.quantity // 0)}' "$S/menu-$W.json"
```

Seafood only (`category == "Seafood"`), or the swaps offered on a course:

```sh
jq '.meals[] | select(.recipe.category == "Seafood") | {index, name: .recipe.name, premium: .charge.label}' "$S/menu-$W.json"
jq '.modularity[] | select(.variations | length > 0) | {course: .defaultCourseIndex, swaps: [.variations[] | {index, title}]}' "$S/menu-$W.json"
```

The current picks (a `selection.quantity` means picked):

```sh
jq '.meals[] | select(.selection.quantity) | {index, name: .recipe.name, quantity: .selection.quantity}' "$S/menu-$W.json"
```

## Real box price (HelloFresh's own calculator, through the tab)

`POST /gw/calculate` is behind Cloudflare's WAF for anything that isn't the
browser (`403 "Attention Required"` from curl), so this one call goes through
the signed-in tab with `fpx post-json`. It needs the bearer header too. `fpx`
only takes headers as arguments, so the token is visible in `ps` for the
duration of that one call; it comes from the 600-mode file, never from your
typing, so it stays out of shell history. The hellofresh-mcp server avoids even
that. `recipeIndexes` must be **strings**. The answer is in **dollars**.

```sh
W=2026-W50
SUBJ=$(hf "/api/customers/me/subscriptions?$Q" | jq '.items[0]')
SUB=$(jq -r .id <<<"$SUBJ"); PLAN=$(jq -r .customerPlanId <<<"$SUBJ")
D=$(hf "/api/subscriptions/$SUB/delivery_dates/$W?$Q")
SKU=$(jq -r .product.handle <<<"$D"); PEOPLE=$(jq -r .product.specs.size <<<"$D")
hf "/my-deliveries/menu?subscription=$SUB&week=$W&locale=en-US&servings=$PEOPLE&product-sku=$SKU&customerPlanId=$PLAN&exclude-feedback=true" > "$S/menu-$W.json"
(umask 077; jq -n --argjson s "$SUBJ" --argjson d "$D" --slurpfile m "$S/menu-$W.json" '
  ($s.firstDeliveryWeek == $d.id) as $first |
  {customerID: ($s.customer.id | tonumber), subscriptionID: ($s.id | tonumber), couponCode: ($s.couponCode // ""),
   shippingAddress: {postcode: $s.shippingAddress.postcode}, planID: $s.customerPlanId, locale: "en-US", country: "US",
   products: [{handle: $d.product.handle, hfWeek: $d.id, deliveryOption: $d.deliveryOption.handle,
               recipeIndexes: [$m[0].meals[] | select(.selection.quantity) | (.index | tostring)]}],
   weekId: $d.id, isFirstOrder: $first, isRecurring: ($first | not), isFutureWeek: true, boxSize: $d.product.specs.size}' > "$S/calc-$W.json")
fpx post-json 'https://www.hellofresh.com/gw/calculate' @"$S/calc-$W.json" -p hellofresh -H "$(tr -d '\n' < "$S/auth.header")" \
  | jq --slurpfile m "$S/menu-$W.json" '{week: .products[0].hfWeek, grandTotal, subTotal, discountAmount, couponPercent: .products[0].couponPercent,
      shipping: .shippingAmount, shippingDiscount: .shippingDiscountAmount, tax: .taxAmount,
      premiumsNotIncluded: ([$m[0].meals[] | select(.selection.quantity) | (.charge.totalAmount // 0)] | add / 100)}'
```

The calculator does **not** include premium recipe upcharges (`charges` comes
back `null`): add `premiumsNotIncluded` yourself. The request body carries the
delivery postcode, and the response carries the customer ids and shipping
address, so the projection above keeps only the money. Keep it that way.
`$S/calc-$W.json` is written mode 600 for the same reason.

## Refresh (only when reloading the tab didn't help)

The refresh token **rotates** on every refresh and the response sets no
cookie, so the new set MUST be written back into the browser right away, or
the browser keeps a spent refresh token and is signed out. If the
hellofresh-mcp server is running too, prefer reloading the tab: two refreshers
fork the session.

```sh
code=$(curl -sS -o "$S/refreshed.json" -w '%{http_code}' -X POST \
  'https://www.hellofresh.com/gw/refresh?country=us&locale=en-US' \
  -H 'content-type: application/json' --data-binary @<(jq -c '{refresh_token}' "$S/auth.json"))
echo "refresh: HTTP $code" >&2
node "$T" store "$S" && fpx write-cookies apiV2Auth=@"$S/cookie.txt" -p hellofresh --storage-subdomain www
```

`store` writes `auth.json`, `auth.header` and `cookie.txt` (the value encoded
exactly as the site's js-cookie does); `fpx write-cookies` prints the cookie
name once it landed. `400 {"error":"invalid_grant"}` → the refresh token was
already spent: sign in again at hellofresh.com, then `load`.
