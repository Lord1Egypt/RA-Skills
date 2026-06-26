## Nutrition check (nutrition-pro)
- Run: `nutrition log --check-today` to get today's meal count
- If breakfast window (08:00–09:30) and meals_today == 0: ask "What did you have for breakfast?"
- If lunch window (12:30–14:00) and meals_today < 2: ask "What did you have for lunch?"
- If dinner window (19:30–21:30) and meals_today < 3: ask "What are you having for dinner tonight?"
- Never ask the same meal question twice in one day — check memory/YYYY-MM-DD.md first
- If user mentions any food in passing (not a direct log): note it and ask "Should I log that?"
