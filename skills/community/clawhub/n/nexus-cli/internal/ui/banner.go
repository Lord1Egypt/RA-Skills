package ui

import "fmt"

// Version is set via ldflags at build time.
var Version = "dev"

// LogoLines are the octopus ASCII art lines.
var LogoLines = []string{
	GoldText("       ▄▄████▄▄"),
	GoldText("      ██") + Bold("▀▀▀▀") + GoldText("██"),
	GoldText("     █") + Dim("──────") + GoldText("█"),
	"      " + CyanText("◉") + " " + GoldText("████") + " " + CyanText("◉"),
	GoldText("     ╱│") + Dim("██████") + GoldText("│╲"),
	GoldText("    ╱ │") + Dim("██████") + GoldText("│ ╲"),
	GoldText("   ╱╱") + " " + GoldText("│") + Dim("████") + GoldText("│") + " " + GoldText("╲╲"),
	GoldText("  ╱╱") + "  " + GoldText("╰────╯") + "  " + GoldText("╲╲"),
}

// PrintBanner prints the compact startup banner.
func PrintBanner() {
	fmt.Printf("\n  %s %s %s    %s\n", GoldText("⚓"), Bold("ADMIRARR"), Dim("v"+Version), Dim("Command your fleet."))
	fmt.Println(Separator())
}

// PrintLogo prints the full octopus logo.
func PrintLogo() {
	for _, line := range LogoLines {
		fmt.Println("  " + line)
	}
	fmt.Printf("  %s %s\n", Bold("   ADMIRARR"), Dim("v"+Version))
	fmt.Printf("  %s\n\n", Dim("   Command your fleet."))
}
