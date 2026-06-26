# Examples

## 1) Team lunch (vendor compare + confirm)

User:

`Order lunch for 8 people in Koramangala under ₹2500. Compare Swiggy and Zomato first.`

Expected assistant behavior:

1. Ask preference constraints (veg/non-veg split, spice level, ETA priority).
2. Compare top options on both vendors.
3. Build cart and show full preview.
4. Ask explicit confirmation before placing order.

## 2) Budget dinner with strict cap

User:

`Get dinner for 2 under ₹700, fastest option near HSR.`

Expected assistant behavior:

1. Search across available vendors.
2. Rank by payable total + ETA.
3. Show best and backup vendor.
4. Confirm final address and place only after "yes".

## 3) Late-night fallback flow

User:

`Order biryani now, whichever app is open.`

Expected assistant behavior:

1. Check availability on preferred vendor.
2. If unavailable, fallback to alternate vendor automatically.
3. Re-show final cart and ask confirmation again.

## 4) Quick reorder from prior preference

User:

`Same as last Friday from Meghana, but add one extra starter.`

Expected assistant behavior:

1. Reconstruct likely cart from user message/context.
2. Validate current menu availability and price changes.
3. Show updated preview and ask confirmation.

## 5) Address ambiguity guardrail

User:

`Order to office.`

Expected assistant behavior:

1. Ask which saved "office" address if multiple exist.
2. Show exact address in final confirmation.
3. Do not place until address is unambiguous.

## 6) COD or non-cancellable warning

User:

`Place it quickly.`

Expected assistant behavior:

1. Surface risk note (if COD only/non-cancellable applies).
2. Ask explicit confirmation including risk note.
3. Place order only after affirmative response.

