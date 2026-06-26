# Example: Cross-Tool Auto-Generated Tasks

> These examples show how Project Manager Pro automatically creates tasks from events in other NormieClaw tools.

---

## From Expense Tracker Pro

### Bill Due Date Approaching

When Expense Tracker detects an upcoming bill:

```
🔗 Auto-task from Expense Tracker:
   ✅ Added: "Pay electric bill — Xcel Energy"
   📅 Due: March 15 · 🟡 P2 · 🏷 expense-tracker, bills
   📝 Amount: $142.50 · Account: Xcel Energy · Auto-pay: OFF
```

### Subscription Renewal Warning

When a subscription renewal is detected 7 days before charge:

```
🔗 Auto-task from Expense Tracker:
   ✅ Added: "Review/cancel Adobe Creative Cloud renewal"
   📅 Due: March 18 (renews Mar 25) · 🟠 P3 · 🏷 expense-tracker, subscriptions
   📝 Amount: $54.99/mo · Last used: Feb 12 · Consider canceling?
```

### Budget Threshold Alert

When spending exceeds a category threshold:

```
🔗 Auto-task from Expense Tracker:
   ✅ Added: "Review dining out spending — over budget"
   📅 Due: March 12 · 🟡 P2 · 🏷 expense-tracker, budget
   📝 Dining out: $620 spent of $500 budget (124%) · 19 days left in month
```

---

## From Meal Planner Pro

### Weekly Grocery Run

When a meal plan is created for the week:

```
🔗 Auto-task from Meal Planner:
   ✅ Added: "Grocery shopping — week of March 10"
   📅 Due: Saturday, March 8 · 🟠 P3 · 🏷 meal-planner, groceries

   📝 Shopping list (14 items):
   Produce: chicken thighs (2 lbs), bell peppers (4), cilantro, limes (6),
   sweet potatoes (3), spinach (1 bag)
   Pantry: coconut milk (2 cans), garam masala, red curry paste
   Dairy: Greek yogurt (32 oz), shredded mozzarella
   Other: corn tortillas, eggs (1 dozen), hot sauce (obviously)
```

### Advance Meal Prep

When a recipe requires prep the day before:

```
🔗 Auto-task from Meal Planner:
   ✅ Added: "Prep overnight oats for tomorrow"
   📅 Due: Sunday, March 9 (evening) · 🟠 P3 · 🏷 meal-planner, prep
   📝 Recipe: Mango Coconut Overnight Oats · Prep time: 10 min
       Mix oats, coconut milk, chia seeds, diced mango. Refrigerate overnight.
```

---

## From Fitness Tracker Pro

### Scheduled Workout

When a workout is on the calendar:

```
🔗 Auto-task from Fitness Tracker:
   ✅ Added: "Upper body strength session"
   📅 Due: Wednesday, March 11 · 🟠 P3 · 🏷 fitness-tracker, workout
   📝 Program: Week 4, Day 3 · Target: chest, shoulders, triceps
       Estimated duration: 55 min · Location: home gym
```

### Supplement Reorder

When a supplement supply is running low:

```
🔗 Auto-task from Fitness Tracker:
   ✅ Added: "Reorder creatine monohydrate"
   📅 Due: March 14 · ⚪ P4 · 🏷 fitness-tracker, supplements
   📝 Current supply: ~5 days remaining · Last purchased: Amazon, $28.99
       Reorder link in notes.
```

---

## From Content Calendar Pro

### Content Creation Deadline

When a post is scheduled and needs to be created:

```
🔗 Auto-task from Content Calendar:
   ✅ Added: "Write blog post: '5 Ways to Use Hot Sauce Beyond Wings'"
   📅 Due: March 13 (publishes Mar 15) · 🟡 P2 · 🏷 content-calendar, blog
   📝 Target: 800-1200 words · SEO keyword: "hot sauce recipes"
       Publish platform: normieclaw.ai/blog · Needs: 2 product photos
```

### Content Series Project

When a multi-part content series is planned:

```
🔗 Auto-tasks from Content Calendar:
   📁 New project: March Social Media Series — "Spice Education" (4 posts)

   ├── 🔲 Write + design "Scoville Scale Explained" carousel (Mar 10) · P2
   ├── 🔲 Write + design "Habanero vs Ghost Pepper" comparison (Mar 14) · P2
   │   └── ⏳ Depends on: Scoville post published
   ├── 🔲 Write + design "Indian Spice Blends 101" post (Mar 18) · P2
   └── 🔲 Write + design "Behind the Recipe: Tikka Masala Sauce" (Mar 22) · P2

   4 tasks created · All due 2 days before publish date
```

---

## How Cross-Tool Tasks Behave

- **Tagged with source tool** — easy to filter ("show me all meal planner tasks")
- **Follow normal priority rules** — auto-escalate as deadlines approach
- **Editable like any task** — change due dates, priority, add notes
- **Deletable** — if you don't want auto-generated tasks, delete them or disable the integration
- **Don't duplicate** — if a similar task already exists, the agent skips creation and notes it in the check-in log
- **Respect quiet hours** — cross-tool task creation notifications follow your quiet hours settings
