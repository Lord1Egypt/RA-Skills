package ui

import (
	"github.com/charmbracelet/lipgloss"
)

// Brand colors.
var (
	Navy = lipgloss.Color("#0A1628")
	Gold = lipgloss.Color("#D4A843")
	Cyan = lipgloss.Color("#00BCD4")

	ColorGreen  = lipgloss.Color("#00FF00")
	ColorRed    = lipgloss.Color("#FF0000")
	ColorYellow = lipgloss.Color("#FFFF00")
)

// Styles.
var (
	GoldStyle   = lipgloss.NewStyle().Foreground(Gold)
	CyanStyle   = lipgloss.NewStyle().Foreground(Cyan)
	GreenStyle  = lipgloss.NewStyle().Foreground(ColorGreen)
	RedStyle    = lipgloss.NewStyle().Foreground(ColorRed)
	YellowStyle = lipgloss.NewStyle().Foreground(ColorYellow)
	BoldStyle   = lipgloss.NewStyle().Bold(true)
	DimStyle    = lipgloss.NewStyle().Faint(true)
	NavyStyle   = lipgloss.NewStyle().Foreground(Navy)
)
