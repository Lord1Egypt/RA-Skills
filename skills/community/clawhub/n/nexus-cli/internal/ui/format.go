package ui

import "fmt"

// Ok renders text in green.
func Ok(s string) string { return GreenStyle.Render(s) }

// Err renders text in red.
func Err(s string) string { return RedStyle.Render(s) }

// Warn renders text in yellow.
func Warn(s string) string { return YellowStyle.Render(s) }

// Bold renders text bold.
func Bold(s string) string { return BoldStyle.Render(s) }

// Dim renders text dimmed.
func Dim(s string) string { return DimStyle.Render(s) }

// CyanText renders text in cyan.
func CyanText(s string) string { return CyanStyle.Render(s) }

// GoldText renders text in gold.
func GoldText(s string) string { return GoldStyle.Render(s) }

// FmtSize formats bytes into human-readable size.
func FmtSize(bytes int64) string {
	if bytes == 0 {
		return "0 GB"
	}
	gb := float64(bytes) / 1073741824
	if gb >= 1024 {
		return fmt.Sprintf("%.2f TB", gb/1024)
	}
	return fmt.Sprintf("%.2f GB", gb)
}

// Separator returns a dim separator line.
func Separator() string {
	return "  " + Dim("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
}
