---
name: Greyhound Predictor
description: Analyzes greyhound races, fetches data, and predicts winners/placings for upcoming races based on form, odds, and simple models.
version: 1.0
trigger_phrases:
  - predict greyhound race
  - greyhound prediction
  - analyze greyhound
tools:
  - web_search
  - browse_page
  - code_execution  # If your OpenClaw supports Python REPL for modeling
gated: false  # Allow open use; set to true if you want API keys required
---

## Instructions for Greyhound Predictor Skill

When activated (e.g., user says "predict Monmore R5 greyhounds" or "upcoming greyhound predictions"), follow these steps:

1. **Parse user input**: Extract race details like track (e.g., Monmore, Towcester), race number/date, or "upcoming" for today's races.

2. **Fetch data**: 
   - Use web_search or browse_page to get upcoming race cards from sites like gbgb.org.uk, sportinglife.com/greyhounds, or timeform.com/greyhounds.
   - Example: Browse "https://www.gbgb.org.uk/racing/todays-trials-meetings/" for today's races, or API like "https://api.gbgb.org.uk/api/results?page=1&date={today}&track={track}" for form.
   - Gather: Dog names, traps, recent form (e.g., 12131 = positions in last 5 races), best times, odds, trainer form.

3. **Analyze data**: 
   - Calculate basic metrics: Win rate (wins/races), average position, recent speed (time/distance), trap bias (e.g., inside traps win more in sprints).
   - Use rules: Favor dogs with form like 111 (recent wins), low traps in short races (270-480m), wide traps in stayers (650m+).
   - If code_execution available, run a simple Python model (see script below) on fetched data to score probabilities.

4. **Predict**:
   - Winner: Dog with highest score (e.g., best form + trap advantage).
   - Second: Strong chaser (good recent places, stalking trap).
   - Output: "Winner: [Dog Name] (Trap X) - Reasons: Recent wins, trap bias. Second: [Dog Name] (Trap Y) - Consistent placer."

5. **Handle errors**: If no data, say "Couldn't fetch race info—try specifying track/date."

### Sample Python Code for Prediction (if code_execution tool enabled)
If your OpenClaw supports code_execution, include this in instructions to run a basic model. Paste data into a DataFrame.

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Sample data (replace with fetched race data)
data = pd.DataFrame({
    'trap': [1, 2, 3, 4, 5, 6],
    'win_rate': [0.4, 0.3, 0.35, 0.2, 0.45, 0.25],  # Wins/races
    'avg_position': [2.1, 3.0, 2.5, 4.0, 1.8, 3.5],
    'recent_form_score': [0.8, 0.6, 0.7, 0.4, 0.9, 0.5]  # Custom score from form
})
data['winner'] = [1, 0, 0, 0, 0, 0]  # Dummy target for training (use historic data)

# Train simple model
X = data[['trap', 'win_rate', 'avg_position', 'recent_form_score']]
y = data['winner']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
model = LogisticRegression().fit(X_train, y_train)

# Predict for new race
new_data = pd.DataFrame(...)  # Fill with fetched data
preds = model.predict_proba(scaler.transform(new_data))[:, 1]
top_dog = new_data.iloc[preds.argmax()]['dog_name']
print(f"Predicted winner: {top_dog}")