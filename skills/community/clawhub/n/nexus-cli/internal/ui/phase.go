package ui

import "fmt"

// PhaseHeader prints a formatted phase header with anchor, name, and description.
func PhaseHeader(num int, name, description string) {
	fmt.Println()
	fmt.Printf("  %s Phase %d — %s\n", GoldText("⚓"), num, Bold(name))
	fmt.Printf("  %s\n", Dim(description))
	fmt.Println(Separator())
}

// PhaseTransition prints a dim transition line between phases.
func PhaseTransition(nextNum int, nextName string) {
	fmt.Printf("\n  %s\n", Dim(fmt.Sprintf("─── Next: Phase %d — %s ───", nextNum, nextName)))
}

// PhaseSummary prints a formatted per-phase result summary.
func PhaseSummary(name string, passed, fixed, skipped, errors int) {
	parts := []string{}
	if passed > 0 {
		parts = append(parts, Ok(fmt.Sprintf("%d passed", passed)))
	}
	if fixed > 0 {
		parts = append(parts, GoldText(fmt.Sprintf("%d fixed", fixed)))
	}
	if skipped > 0 {
		parts = append(parts, Dim(fmt.Sprintf("%d skipped", skipped)))
	}
	if errors > 0 {
		parts = append(parts, Err(fmt.Sprintf("%d error(s)", errors)))
	}
	summary := ""
	for i, p := range parts {
		if i > 0 {
			summary += ", "
		}
		summary += p
	}
	fmt.Printf("\n  %s %s: %s\n", Dim("→"), Bold(name), summary)
}
