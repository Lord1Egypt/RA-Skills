package nutrition

import "testing"

// food builds a header-keyed food-log row with the columns the aggregator reads.
func food(date, name, meal, quantity, units, calories, deleted, fat, protein, carbs, fiber string) map[string]string {
	return map[string]string{
		"Date":              date,
		"Name":              name,
		"Meal":              meal,
		"Quantity":          quantity,
		"Units":             units,
		"Calories":          calories,
		"Deleted":           deleted,
		"Fat (g)":           fat,
		"Protein (g)":       protein,
		"Carbohydrates (g)": carbs,
		"Fiber (g)":         fiber,
	}
}

func summ(date, foodCals, exerciseCals, budgetCals string) map[string]string {
	return map[string]string{
		"Date":          date,
		"Food cals":     foodCals,
		"Exercise cals": exerciseCals,
		"Budget cals":   budgetCals,
		"EER":           "2450",
	}
}

// fixture mirrors tests/test_offline.py: the confirmed columns and the exact
// rows, including a deleted 999-cal row that must be excluded.
func fixture() (foods, summary []map[string]string) {
	foods = []map[string]string{
		food("2026-06-16", "Greek Yogurt", "Breakfast", "1", "cup", "120", "false", "0", "22", "9", "0"),
		food("2026-06-16", "Banana", "Breakfast", "1", "each", "105", "false", "0", "1", "27", "3"),
		food("2026-06-16", "Chicken Breast", "Lunch", "6", "oz", "280", "false", "6", "52", "0", "0"),
		food("2026-06-16", "Old Deleted Food", "Lunch", "1", "each", "999", "true", "50", "0", "50", "0"),
		food("2026-06-15", "Protein Shake", "Snacks", "1", "scoop", "120", "false", "1", "24", "3", "1"),
	}
	summary = []map[string]string{
		summ("2026-06-16", "505", "120", "1663"),
		summ("2026-06-15", "120", "0", "1663"),
	}
	return foods, summary
}

func TestAggregationSumsMacrosAndSkipsDeleted(t *testing.T) {
	days := BuildByDay(fixture())
	n := days["2026-06-16"]
	if n.CaloriesFood != 505 { // 120+105+280 (deleted 999 excluded)
		t.Errorf("calories_food = %d, want 505", n.CaloriesFood)
	}
	if n.ProteinG != 75 { // 22+1+52
		t.Errorf("protein_g = %d, want 75", n.ProteinG)
	}
	if n.FiberG != 3 { // 0+3+0
		t.Errorf("fiber_g = %d, want 3", n.FiberG)
	}
	if n.CarbsG != 36 { // 9+27+0
		t.Errorf("carbs_g = %d, want 36", n.CarbsG)
	}
	if n.FatG != 6 { // 0+0+6
		t.Errorf("fat_g = %d, want 6", n.FatG)
	}
	if n.Source != "Lose It export" {
		t.Errorf("source = %q, want %q", n.Source, "Lose It export")
	}
}

func TestMealsGroupedAndOrdered(t *testing.T) {
	n := BuildByDay(fixture())["2026-06-16"]
	gotOrder := make([]string, len(n.Meals))
	for i, m := range n.Meals {
		gotOrder[i] = m.Meal
	}
	if len(gotOrder) != 2 || gotOrder[0] != "Breakfast" || gotOrder[1] != "Lunch" {
		t.Fatalf("meal order = %v, want [Breakfast Lunch]", gotOrder)
	}

	breakfast := n.Meals[0]
	if breakfast.Calories != 225 { // 120+105
		t.Errorf("breakfast calories = %d, want 225", breakfast.Calories)
	}
	if breakfast.ProteinG != 23 { // 22+1
		t.Errorf("breakfast protein_g = %d, want 23", breakfast.ProteinG)
	}
	if breakfast.FatG != 0 {
		t.Errorf("breakfast fat_g = %d, want 0", breakfast.FatG)
	}

	names := map[string]bool{}
	for _, it := range breakfast.Items {
		names[it.Name] = true
	}
	if !names["Greek Yogurt"] || !names["Banana"] {
		t.Errorf("breakfast items = %v, want Greek Yogurt + Banana", names)
	}
	// qty = Quantity + " " + Units, calories round-half-to-even of the row value.
	for _, it := range breakfast.Items {
		if it.Name == "Greek Yogurt" {
			if it.Qty != "1 cup" {
				t.Errorf("greek yogurt qty = %q, want %q", it.Qty, "1 cup")
			}
			if it.Calories != 120 {
				t.Errorf("greek yogurt calories = %d, want 120", it.Calories)
			}
		}
	}
}

func TestSummaryFieldsAttached(t *testing.T) {
	days := BuildByDay(fixture())

	n := days["2026-06-16"]
	if n.LoseItBudget == nil || *n.LoseItBudget != 1663 {
		t.Errorf("loseit_budget = %v, want 1663", n.LoseItBudget)
	}
	if n.LoseItUnder == nil || *n.LoseItUnder != 1663-505 {
		t.Errorf("loseit_under = %v, want %d", n.LoseItUnder, 1663-505)
	}
	if n.ExerciseAdjustment == nil || *n.ExerciseAdjustment != 120 {
		t.Errorf("exercise_adjustment = %v, want 120", n.ExerciseAdjustment)
	}

	// 2026-06-15 has Exercise cals 0 → exercise_adjustment must be omitted, but
	// budget/under are still present.
	d15 := days["2026-06-15"]
	if d15.ExerciseAdjustment != nil {
		t.Errorf("2026-06-15 exercise_adjustment = %v, want nil (0 exercise)", d15.ExerciseAdjustment)
	}
	if d15.LoseItUnder == nil || *d15.LoseItUnder != 1663-120 {
		t.Errorf("2026-06-15 loseit_under = %v, want %d", d15.LoseItUnder, 1663-120)
	}
	if order := d15.Meals[0].Meal; order != "Snacks" {
		t.Errorf("2026-06-15 first meal = %q, want Snacks", order)
	}
}

func TestEmptyMealNameDefaultsToOther(t *testing.T) {
	rows := []map[string]string{
		food("2026-06-16", "Mystery", "", "1", "serving", "50", "false", "0", "0", "0", "0"),
	}
	n := BuildByDay(rows, nil)["2026-06-16"]
	if n.Meals[0].Meal != "Other" {
		t.Errorf("blank meal name = %q, want Other", n.Meals[0].Meal)
	}
}

func TestUnparseableDateSkipped(t *testing.T) {
	rows := []map[string]string{
		food("not-a-date", "Ghost", "Lunch", "1", "x", "100", "false", "0", "0", "0", "0"),
	}
	if got := BuildByDay(rows, nil); len(got) != 0 {
		t.Errorf("unparseable date produced %d days, want 0", len(got))
	}
}

// TestBankersRoundingSumThenRound proves round-half-to-even and that totals round
// the summed float (not a sum of pre-rounded values).
func TestBankersRoundingSumThenRound(t *testing.T) {
	// 2.5 → 2 (even); 3.5 → 4 (even); 0.5+0.5 summed → 1.0 → 1 (round-then-sum
	// would give round(0.5)+round(0.5) = 0+0 = 0).
	cases := []struct {
		name    string
		protein []string
		want    int
	}{
		{"half-to-even-down", []string{"2.5"}, 2},
		{"half-to-even-up", []string{"3.5"}, 4},
		{"sum-then-round", []string{"0.5", "0.5"}, 1},
	}
	for _, c := range cases {
		t.Run(c.name, func(t *testing.T) {
			rows := make([]map[string]string, len(c.protein))
			for i, p := range c.protein {
				rows[i] = food("2026-06-16", "x", "Breakfast", "1", "u", "0", "false", "0", p, "0", "0")
			}
			n := BuildByDay(rows, nil)["2026-06-16"]
			if n.ProteinG != c.want {
				t.Errorf("protein_g = %d, want %d", n.ProteinG, c.want)
			}
		})
	}
}
