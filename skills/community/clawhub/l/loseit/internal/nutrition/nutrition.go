// Package nutrition aggregates Lose It! food-log rows into per-day nutrition
// objects, porting loseit/nutrition.py byte-for-byte where it matters.
//
// The emitted shape (frozen — see GOAL.md §5):
//
//	{ source, calories_food, protein_g, carbs_g, fat_g, fiber_g, meals,
//	  loseit_budget, loseit_under, exercise_adjustment }
//
// The three summary fields appear only when daily-calorie-summary.csv provides
// them, and after meals.
//
// Parity rules that the validated numbers depend on:
//   - Rounding is round-half-to-even (Python's round()). Raw floats are summed
//     across rows first, THEN each total is rounded — day totals and per-meal
//     totals each round the summed float, never a sum of pre-rounded values.
//   - A row is skipped when Deleted ∈ {true,1,yes} (case-insensitive).
//   - Dates are normalized via several layouts to ISO; unparseable rows skip.
//   - Meal order: Breakfast, Lunch, Dinner, Snacks first (that order), then any
//     other meals in first-encounter order; a blank meal name defaults to Other.
package nutrition

import (
	"math"
	"strconv"
	"strings"
	"time"
)

// mealOrder is the canonical leading order; meals outside it follow in
// first-encounter order.
var mealOrder = []string{"Breakfast", "Lunch", "Dinner", "Snacks"}

// dateLayouts are tried in order; the first that parses wins (ported from
// nutrition.py: %Y-%m-%d, %m/%d/%Y, %m/%d/%y, %Y/%m/%d).
var dateLayouts = []string{"2006-01-02", "01/02/2006", "01/02/06", "2006/01/02"}

// Item is one logged food within a meal. Key order frozen: name, qty, calories.
type Item struct {
	Name     string `json:"name"`
	Qty      string `json:"qty"`
	Calories int    `json:"calories"`
}

// Meal is one meal's aggregate plus its items. Key order frozen: meal, calories,
// protein_g, carbs_g, fat_g, items.
type Meal struct {
	Meal     string `json:"meal"`
	Calories int    `json:"calories"`
	ProteinG int    `json:"protein_g"`
	CarbsG   int    `json:"carbs_g"`
	FatG     int    `json:"fat_g"`
	Items    []Item `json:"items"`
}

// Nutrition is one day's aggregate. Key order frozen (GOAL.md §5). The three
// summary pointers are nil (omitted) unless the daily summary supplies them, so
// a legitimate zero (e.g. loseit_under == 0) is still emitted while an absent
// field disappears entirely.
type Nutrition struct {
	Source       string `json:"source"`
	CaloriesFood int    `json:"calories_food"`
	ProteinG     int    `json:"protein_g"`
	CarbsG       int    `json:"carbs_g"`
	FatG         int    `json:"fat_g"`
	FiberG       int    `json:"fiber_g"`
	Meals        []Meal `json:"meals"`

	LoseItBudget       *int `json:"loseit_budget,omitempty"`
	LoseItUnder        *int `json:"loseit_under,omitempty"`
	ExerciseAdjustment *int `json:"exercise_adjustment,omitempty"`
}

// internal per-meal accumulator carrying raw float sums.
type mealAcc struct {
	name     string
	calories float64
	protein  float64
	carbs    float64
	fat      float64
	items    []Item
}

// internal per-day accumulator carrying raw float sums and meal ordering.
type dayAcc struct {
	calories float64
	protein  float64
	carbs    float64
	fat      float64
	fiber    float64
	meals    map[string]*mealAcc
	order    []string // meal names in first-encounter order.
}

// BuildByDay returns {date_iso: Nutrition} aggregated from the export rows. Rows
// are header-keyed maps (csv.DictReader style).
func BuildByDay(foodRows, summaryRows []map[string]string) map[string]Nutrition {
	days := map[string]*dayAcc{}

	for _, r := range foodRows {
		if isDeleted(r) {
			continue
		}
		d := normDate(r["Date"])
		if d == "" {
			continue
		}

		cals := num(r["Calories"])
		pro := num(r["Protein (g)"])
		carb := num(r["Carbohydrates (g)"])
		fat := num(r["Fat (g)"])
		fib := num(r["Fiber (g)"])

		day := days[d]
		if day == nil {
			day = &dayAcc{meals: map[string]*mealAcc{}}
			days[d] = day
		}
		day.calories += cals
		day.protein += pro
		day.carbs += carb
		day.fat += fat
		day.fiber += fib

		mealName := strings.TrimSpace(r["Meal"])
		if mealName == "" {
			mealName = "Other"
		}
		meal := day.meals[mealName]
		if meal == nil {
			meal = &mealAcc{name: mealName}
			day.meals[mealName] = meal
			day.order = append(day.order, mealName)
		}
		meal.calories += cals
		meal.protein += pro
		meal.carbs += carb
		meal.fat += fat
		meal.items = append(meal.items, Item{
			Name:     strings.TrimSpace(r["Name"]),
			Qty:      qty(r),
			Calories: roundEven(cals),
		})
	}

	summary := map[string]map[string]string{}
	for _, r := range summaryRows {
		if d := normDate(r["Date"]); d != "" {
			summary[d] = r
		}
	}

	out := make(map[string]Nutrition, len(days))
	for d, day := range days {
		nut := Nutrition{
			Source:       "Lose It export",
			CaloriesFood: roundEven(day.calories),
			ProteinG:     roundEven(day.protein),
			CarbsG:       roundEven(day.carbs),
			FatG:         roundEven(day.fat),
			FiberG:       roundEven(day.fiber),
			Meals:        buildMeals(day),
		}
		attachSummary(&nut, summary[d])
		out[d] = nut
	}
	return out
}

// buildMeals orders the day's meals (canonical leading order, then
// first-encounter) and rounds each meal's summed floats.
func buildMeals(day *dayAcc) []Meal {
	ordered := make([]string, 0, len(day.order))
	for _, m := range mealOrder {
		if _, ok := day.meals[m]; ok {
			ordered = append(ordered, m)
		}
	}
	for _, m := range day.order {
		if !inCanonical(m) {
			ordered = append(ordered, m)
		}
	}

	meals := make([]Meal, 0, len(ordered))
	for _, name := range ordered {
		m := day.meals[name]
		meals = append(meals, Meal{
			Meal:     m.name,
			Calories: roundEven(m.calories),
			ProteinG: roundEven(m.protein),
			CarbsG:   roundEven(m.carbs),
			FatG:     roundEven(m.fat),
			Items:    m.items,
		})
	}
	return meals
}

// attachSummary adds the budget/under/exercise fields from the daily summary
// row, when present and non-zero (matching the Python `if budget:` / `if ex:`).
// loseit_under is emitted alongside loseit_budget even when it is zero.
func attachSummary(nut *Nutrition, s map[string]string) {
	if s == nil {
		return
	}
	if budget := roundEven(num(s["Budget cals"])); budget != 0 {
		under := budget - nut.CaloriesFood
		nut.LoseItBudget = &budget
		nut.LoseItUnder = &under
	}
	if ex := roundEven(num(s["Exercise cals"])); ex != 0 {
		nut.ExerciseAdjustment = &ex
	}
}

func inCanonical(name string) bool {
	for _, m := range mealOrder {
		if m == name {
			return true
		}
	}
	return false
}

// isDeleted ports _is_deleted: Deleted ∈ {true,1,yes}, case-insensitive.
func isDeleted(r map[string]string) bool {
	switch strings.ToLower(strings.TrimSpace(r["Deleted"])) {
	case "true", "1", "yes":
		return true
	default:
		return false
	}
}

// num ports _num: parse a float, defaulting to 0 on empty/invalid input.
func num(s string) float64 {
	f, err := strconv.ParseFloat(strings.TrimSpace(s), 64)
	if err != nil {
		return 0
	}
	return f
}

// normDate ports _norm_date: try each layout, return ISO (YYYY-MM-DD), or "".
func normDate(s string) string {
	s = strings.TrimSpace(s)
	if s == "" {
		return ""
	}
	for _, layout := range dateLayouts {
		if t, err := time.Parse(layout, s); err == nil {
			return t.Format("2006-01-02")
		}
	}
	return ""
}

// qty ports the Quantity+Units join: the two trimmed parts joined by a space,
// skipping empty parts.
func qty(r map[string]string) string {
	parts := make([]string, 0, 2)
	if q := strings.TrimSpace(r["Quantity"]); q != "" {
		parts = append(parts, q)
	}
	if u := strings.TrimSpace(r["Units"]); u != "" {
		parts = append(parts, u)
	}
	return strings.Join(parts, " ")
}

// roundEven rounds a summed float to the nearest integer using round-half-to-even
// (banker's rounding), matching Python's built-in round(). RoundToEven yields an
// integral float64, so the int conversion is exact.
func roundEven(f float64) int {
	return int(math.RoundToEven(f))
}
