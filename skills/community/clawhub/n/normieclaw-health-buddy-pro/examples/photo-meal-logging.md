# Example: Photo-Based Meal Logging

This example shows the full flow of snapping a food photo and getting it logged.

---

## The Conversation

**User:** *[sends a photo of a Chipotle burrito bowl with rice, chicken, black beans, salsa, cheese, and guacamole]*

**Health Buddy Pro:**
> 🌯 Nice choice! Here's what I see in that burrito bowl:
>
> - Cilantro-lime rice: ~210 cal | 4g protein | 40g carbs | 4g fat
> - Grilled chicken: ~180 cal | 32g protein | 0g carbs | 4g fat
> - Black beans: ~130 cal | 8g protein | 22g carbs | 1g fat
> - Pico de gallo: ~25 cal | 1g protein | 5g carbs | 0g fat
> - Shredded cheese: ~110 cal | 7g protein | 1g carbs | 9g fat
> - Guacamole: ~230 cal | 3g protein | 8g carbs | 22g fat
>
> **Meal total: ~885 cal | 55g protein | 76g carbs | 40g fat**
>
> You've had 1,250 / 2,200 cal today. Plenty of room for dinner! Want me to log this?

**User:** Yeah log it! But I think the rice was a smaller portion, maybe half.

**Health Buddy Pro:**
> Got it! Adjusting the rice down to a half portion:
>
> **Updated meal total: ~780 cal | 53g protein | 56g carbs | 38g fat**
>
> ✅ Logged as lunch! You've had 1,145 / 2,200 cal today with 55g protein banked already. Solid. 💪

---

## What's Happening Behind the Scenes

1. The `image` tool analyzes the photo to identify individual food items and estimate portions
2. Each item is matched against known nutritional data (Chipotle's published nutrition info for restaurant items)
3. Results are presented for user confirmation — never auto-logged
4. User correction ("half portion of rice") triggers a recalculation
5. Confirmed meal is appended to `data/nutrition-log.json`
6. Daily running totals are updated
