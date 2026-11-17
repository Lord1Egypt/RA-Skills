# Store Atlas — Common Chain Layouts (starting points)

**Your map beats this atlas.** These are conventional layouts to seed a
`map-store` session or sanity-check yours. Chains rearrange; the walking
order from YOUR entrance is what matters.

## US conventional supermarkets

Typical zone walk (entrance usually at produce or front corner):

```
produce → bakery/floral → deli → meat/seafood → dairy →
breakfast/coffee → pantry center aisles → snacks/soda →
household/paper → health/HBA → pet → frozen (wall) → checkout
```

- Kroger/Albertsons/Safeway-class: produce entrance, frozen along a side
  wall, dairy at the far back.
- Walmart supercenter: groceries on one side; entrance maps matter more
  than usual (produce-entrance vs. general-merch entrance flip the walk).
- Trader Joe's: small store, single main loop — 6-8 zones is plenty.
- Aldi/Lidl: center-aisle specials in the middle; frozen wall at the end.
  Classic efficient loop already; your map will be short.

## US warehouse (Costco/Sam's)

You walk the whole warehouse regardless; a zone map still helps for
cold-chain timing (frozen last) and "which wall" recall. Zones: entrance
deals → electronics/clothing → dry pantry → canned/boxed → snacks →
office → household/paper → refrigerated wall → meat → frozen → checkout.

## EU supermarkets

```
produce → bakery (strong, often front) → dairy/chilled walls →
meat/fish counter → center dry goods → beverages (often separate alcove)
→ household → frozen → checkout
```

- Carrefour/Intermarché (FR), REWE/Edeka/Lidl (DE), Albert Heijn (NL),
  Tesco/Sainsbury (UK), Mercadona (ES), Conad/Coop (IT) — all roughly
  this shape with national quirks (bread and produce up front).
- Russian chains (Pyaterochka, Magnit, Lenta, VkusVill): produce/bakery
  front, dairy wall, meat counter, center grocery, household,
  frozen wall, checkout. VkusVill is small-format: 6-7 zones.

## Specialty formats

- **Ethnic markets**: produce + live herbs often 30% of floor; dry goods
  dominate; frozen is small. Map: produce → fresh herbs → tofu/vegan →
  noodles/rice (huge) → sauces → snacks → frozen → checkout.
- **Co-op/natural food**: bulk bins deserve their own zone; supplements
  corner; frozen small. produce → bulk → dairy-alt → packaged →
  supplements → frozen → checkout.
- **Hard discounters (Aldi Nord/Süd, Lidl, Penny)**: half the trip is the
  center "middle aisle" of non-food deals; decide if that's a zone for
  you (it is if you always slow down there — name it "middle-deals").

## Zone naming tips

- Use names you'd say out loud ("milk wall", "middle-deals", "cheese
  corner") — the matcher's aliases handle common ones, and learned items
  handle the rest.
- 8-12 zones. Below 6 you get mega-zones that force mini-backtracks;
  above 15 you're doing taxonomy homework.
- Put checkout last even though you don't buy there — the list feels
  complete and the frozen zone's melt-distance becomes visible.

## After a store remodel

Re-run `map-store` (it shows current zones and offers a redo). Learned
items persist but may need re-teaching if the store moved things —
`route` will surface them as unplaced if their zone vanished.
