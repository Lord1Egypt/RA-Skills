---
name: neomano-places
description: Search Google Places (Places API New) for real-world places, businesses, restaurants, and nearby recommendations. Use when the user asks to find specific places, restaurants, reviews, ratings, addresses, maps links, or to search by location and filter by open now or minimum rating.
metadata: {"openclaw":{"emoji":"📍","requires":{"bins":["python3"],"env":["GOOGLE_PLACES_API_KEY"]},"primaryEnv":"GOOGLE_PLACES_API_KEY"}}
---

# Neomano Places (Google Places)

Use Google Places as the source of truth for real-world place lookup.

## Workflow

1. **Choose the search intent**
   - Use the user's request directly when possible.
   - If they want food or local recommendations, search by category + place name.

2. **Search Places**
   - Use `scripts/places.py` for text search.
   - Add location bias when the user mentions a town, city, or area.
   - Prefer concrete results with ratings and review counts.

3. **Filter and rank**
   - Prefer places with stronger ratings and more reviews.
   - If the user wants a specific dish, favor places whose name, category, or reviews mention it.
   - If results are weak or ambiguous, say so and avoid guessing.

4. **Respond clearly**
   - Return a short ranked list.
   - Include place name, why it stands out, rating, and address when available.
   - Include a Google Maps link if present.

## Output style

- Keep it practical and concrete.
- Use bullets, not tables.
- If the user asks for only one place, return the best match and 1–2 backups.

## Notes

- Requires `GOOGLE_PLACES_API_KEY`.
- To get one, create a project in **Google Cloud Console**, enable **Places API (New)**, and create an API key in **APIs & Services → Credentials**.
- For best results, restrict the key to **Places API** and, if possible, lock it down by IP.
- For JSON output, use `--json` on the script.
- For nearby searches, pass `--lat`, `--lng`, and `--radius-m`.
