# Example: Weekly Meal Plan Generation

This shows a realistic conversation flow from request to plan generation to refinement.

---

## Household Context (from `data/household.json`)
- **Mom** (38) — allergic to tree nuts & shellfish, dislikes mushrooms & olives, adventurousness 4, prefers fish > chicken > tofu
- **Dad** (40) — no allergies, dislikes liver, adventurousness 3, prefers chicken > beef > fish
- **Tommy** (7) — no allergies, dislikes visible onions, texture issue with "slimy" foods, adventurousness 2, prefers chicken > beef
- **Lily** (4) — no allergies, dislikes spicy food, texture issue with "mushy" foods, adventurousness 1, prefers chicken > pasta

---

## The Conversation

**User:** Plan my week! Dad is traveling Tuesday through Thursday. Wednesday is a busy day for me.

**Agent:**

> Got it! Planning for the week with a few notes:
> - Dad's out Tue–Thu (meals for 3 those days, portions adjusted)
> - Wednesday is a busy day — I'll keep it to 20 minutes or less
> - I checked your freezer — you've got ground beef (2 lbs, from Feb 15) that we should use
> - Tommy ❤️'d the Chicken Taco Bowls 3 weeks ago — perfect time to bring those back
> - Skipping salmon this week since Lily 👎'd it last time
>
> Here's your week:
>
> ---
>
> **📅 MONDAY** — All 4 eating
>
> 🌅 **Breakfast:** Overnight Oats w/ berries & honey *(prep night before, 5 min)*
> 🥪 **Lunch:** Turkey & Cheese Wraps + apple slices *(10 min, kids packed)*
> 🍽️ **Dinner:** One-Pan Lemon Chicken w/ roasted broccoli & rice *(15 min prep, 25 min cook)*
> 💡 *Make extra chicken — we'll use it for Wednesday lunch*
> 🍎 **Snack:** Apple slices + cheese sticks *(kids)*
>
> **📅 TUESDAY** — Mom, Tommy, Lily (Dad traveling)
>
> 🌅 **Breakfast:** Scrambled Eggs + Toast *(10 min)*
> 🥪 **Lunch:** PB&J + carrot sticks *(kids packed); Mom: leftover chicken wrap*
> 🍽️ **Dinner:** Chicken Taco Bowls w/ rice, beans, cheese, salsa *(20 min)*
> ⭐ *Tommy's favorite — ❤️ last month!*
> 🍎 **Snack:** Yogurt cups *(kids)*
>
> **📅 WEDNESDAY** — Mom, Tommy, Lily ⚡ BUSY DAY
>
> 🌅 **Breakfast:** Cereal + banana *(2 min)*
> 🥪 **Lunch:** Leftover chicken from Monday + crackers *(0 min prep)*
> 🍽️ **Dinner:** ⚡ Sheet Pan Quesadillas *(15 min total — use leftover taco ingredients)*
> 🍎 **Snack:** Goldfish crackers + grapes *(kids)*
>
> **📅 THURSDAY** — Mom, Tommy, Lily (Dad still out)
>
> 🌅 **Breakfast:** Yogurt Parfait w/ granola & berries *(5 min)*
> 🥪 **Lunch:** Ham & cheese rollups + pretzels *(kids packed); Mom: big salad*
> 🍽️ **Dinner:** Beef Tacos w/ ground beef from freezer 🧊 *(20 min)*
> 💡 *Using up your frozen ground beef (from Feb 15 — 3 weeks old)*
> 🍎 **Snack:** String cheese + crackers *(kids)*
>
> **📅 FRIDAY** — All 4 eating (Dad's back!)
>
> 🌅 **Breakfast:** Pancakes *(15 min)*
> 🥪 **Lunch:** Grilled cheese + tomato soup *(15 min)*
> 🍽️ **Dinner:** Homemade Pizza Night 🍕 *(30 min — everyone makes their own)*
> 🍎 **Snack:** Popcorn *(family movie night?)*
>
> **📅 SATURDAY** — All 4 eating
>
> 🌅 **Breakfast:** Eggs & Toast *(10 min)*
> 🥪 **Lunch:** Out / leftovers
> 🍽️ **Dinner:** Teriyaki Chicken Stir-Fry w/ rice & snap peas *(25 min)*
> 🍎 **Snack:** Fruit salad
>
> **📅 SUNDAY** — All 4 eating
>
> 🌅 **Breakfast:** French Toast *(15 min)*
> 🥪 **Lunch:** Chicken Salad sandwiches *(leftover teriyaki chicken)*
> 🍽️ **Dinner:** Slow Cooker Pot Roast w/ carrots & potatoes *(15 min prep, 6-8hr cook — start morning)*
> 🍎 **Snack:** Veggies + hummus
>
> ---
>
> **Quick stats:**
> - 5 unique protein sources across dinners (chicken, beef, pizza, chicken, beef)
> - 5 different cuisines (American, Mexican, Mexican, Italian, Japanese, American)
> - Zero allergen conflicts ✅
> - Freezer ground beef used up ✅
> - Wednesday stays under 20 min ✅
>
> Want me to tweak anything, or should I generate the grocery list?

---

## Refinement Example

**User:** Swap Tuesday dinner — Tommy's been anti-taco lately.

**Agent:**

> No problem! Here are 3 options that work for Mom, Tommy, and Lily (no tree nuts, no slimy textures, kid-friendly):
>
> 1. **Chicken Pesto Pasta** — 20 min, Tommy 👍'd it last month
> 2. **Mini Meatball Subs** — 25 min, comfort food, uses ground beef (but we need the freezer beef for Thu)
> 3. **Cheesy Chicken & Rice Casserole** — 15 min prep + 25 min bake, one dish cleanup
>
> Which one sounds good? Or tell me what you're in the mood for.

**User:** Chicken pesto pasta!

**Agent:**

> Done! Tuesday dinner is now **Chicken Pesto Pasta** (20 min).
>
> **Grocery list updates:**
> - ❌ Removed: taco seasoning, salsa (was only for Tue)
> - ✅ Added: penne pasta (1 lb), basil pesto (1 jar), parmesan cheese (wedge)
> - Chicken thighs quantity stays the same (already needed for Monday)
>
> Everything else in your plan is untouched. 👍
