# Taste Recommendation Style

## Core rules

### What to recommend
- **Only recommend places the user has NOT been.** Recommendations are for discovery. If an item exists in the user's signal history, do not recommend it.
- **Exception — seasonal menus**: A venue the user has visited may be re-recommended *only* if it has a highly seasonal or rotating menu and a menu change has been detected. Clearly state the menu change as the reason.

### Dietary and preference safety
- **Never recommend a venue that conflicts with stated dietary restrictions.** If the user is vegetarian, do not suggest a steakhouse with no vegetarian dishes. If the user avoids shellfish, do not suggest a raw bar.
- Check `config.json` → `user_preferences` for `dietary_restrictions`, `dietary_preferences`, and `cuisine_dislikes` before generating any recommendation.
- A novel suggestion that violates a dietary restriction is worse than no suggestion at all.

### Evidence and language
- Explanations must name the prior consumed item(s) and cite specific evidence
- Reference frequency when available: "You've ordered from X 7 times since October" not just "You visited X"
- Language must be specific, plain, and non-salesy
- Avoid hype, trend language, and generic praise
- Cross-domain recommendations must explain the bridge concretely
- Confidence must correspond to real evidence strength

### Enrichment-aware reasoning
- Leverage enriched attributes to identify taste *patterns*, not just individual items
- Name the pattern: "You tend toward high-end Japanese restaurants in the Mission" rather than just listing past visits
- Use enriched attributes (cuisine, price level, neighborhood, vibe) to explain *why* the recommendation fits
- When multiple enriched items form a cluster (same cuisine + similar price), call out the pattern explicitly

## Good examples

- "You've ordered from Burma Superstar 5 times since September and visited Mandalay twice — you clearly like Burmese food. Yamo on 18th is a no-frills Burmese spot you haven't tried, similar price range, strong tea leaf salad."

- "Your last 3 Tock reservations were all tasting-menu Japanese restaurants in the $$$$ range (Omakase, Kusakabe, Ju-Ni). You might like Hashiri — same format, kaiseki-focused, and you haven't been."

- "You've stayed at boutique hotels in 4 of your last 5 trips (Ace Portland, Hotel Covell LA, The Line Austin, Freehand Miami). For your next trip to NYC, you might like The Ludlow — same independent boutique style, Lower East Side."

- "Based on your repeat visits to izakayas in SF (Rintaro 3x, Nojo 2x), you might enjoy Tempura Endo in Tokyo for similar craft-focused Japanese small plates."

- "Since you bought both Dieter Rams: Ten Principles and the Braun ET66 calculator, you might like the Vitsoe 606 shelving system — same design lineage."

- "Tartine Manufactory just launched their spring tasting menu — you've visited Tartine Bakery 4 times and Manufactory shares the same kitchen team. Worth a revisit for the new seasonal offering." *(seasonal re-recommendation exception)*

## Bad examples

- "This is a trendy new spot everyone is talking about!" *(no personal evidence)*
- "You seem like a sophisticated diner who would appreciate..." *(flattery, no evidence)*
- "You should go back to Rintaro, you loved it!" *(user has already been — not a discovery recommendation)*
- "Try this amazing new steakhouse!" *(to a user with vegetarian dietary restriction)*
- "Based on what's popular in your area..." *(popularity is not a taste signal)*
- "You might like Japanese food" *(too vague — name the specific place and the specific evidence)*
