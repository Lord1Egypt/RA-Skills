package cmd

import (
	"fmt"
	"os"

	"github.com/maxtechera/admirarr/internal/doctor"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var doctorFix bool

var doctorCmd = &cobra.Command{
	Use:   "doctor",
	Short: "Run full diagnostics on your stack",
	Long: `Run full diagnostics across your entire media stack.

Runs 9 diagnostic categories and reports pass/fail for each:
  1. Service Connectivity  — HTTP reachability + response time
  2. API Keys              — validates keys for all services
  3. Config Files          — checks existence of config files
  4. Docker Containers     — status of Docker containers
  5. Disk Space            — warns at >85%, errors at >95%
  6. Media Paths           — verifies media directories exist
  7. Root Folders          — validates Radarr/Sonarr root folders
  8. Indexers              — Prowlarr indexer health
  9. Service Warnings      — health endpoint warnings

Use --fix to launch the AI fix wizard.`,
	Example: "  admirarr doctor\n  admirarr doctor --fix",
	Run:     runDoctor,
}

func init() {
	doctorCmd.Flags().BoolVar(&doctorFix, "fix", false, "Launch the AI fix wizard to auto-repair detected issues")
	rootCmd.AddCommand(doctorCmd)
}

func runDoctor(cmd *cobra.Command, args []string) {
	if !ui.IsJSON() {
		ui.PrintBanner()
		fmt.Print("\n  Running diagnostics across your entire media stack...\n\n")
	}

	// Doctor checks print text to stdout unconditionally.
	// In JSON mode, suppress that output so only clean JSON is emitted.
	result := runDoctorChecks()

	type doctorOut struct {
		ChecksPassed int      `json:"checks_passed"`
		Issues       []string `json:"issues"`
	}
	dOut := doctorOut{ChecksPassed: result.ChecksPassed, Issues: []string{}}
	for _, issue := range result.Issues {
		dOut.Issues = append(dOut.Issues, issue.Description)
	}

	ui.PrintOrJSON(dOut, func() {
		// Summary
		totalChecks := result.ChecksPassed + len(result.Issues)
		fmt.Println(ui.Separator())
		if len(result.Issues) == 0 {
			fmt.Printf("\n  %s %d/%d checks passed\n", ui.Ok("✓ All clear!"), result.ChecksPassed, totalChecks)
		} else {
			fmt.Printf("\n  %s, %s\n", ui.Bold(fmt.Sprintf("%d/%d checks passed", result.ChecksPassed, totalChecks)),
				ui.Err(fmt.Sprintf("%d issue(s)", len(result.Issues))))
			fmt.Println()
			for i, issue := range result.Issues {
				fmt.Printf("  %s %s\n", ui.Err(fmt.Sprintf("%d.", i+1)), issue.Description)
			}
		}

		if len(result.Issues) > 0 {
			if doctorFix {
				doctor.Fix(result.Issues)
			} else {
				fmt.Println()
				fmt.Printf("  %s Run %s to auto-fix issues.\n", ui.GoldText("⚓"), ui.GoldText("admirarr doctor --fix"))
			}
		}
		fmt.Println()
	})
}

// runDoctorChecks runs doctor checks, suppressing stdout in JSON mode
// since the check functions print text unconditionally.
func runDoctorChecks() *doctor.Result {
	if !ui.IsJSON() {
		return doctor.RunChecks()
	}

	origStdout := os.Stdout
	devNull, _ := os.Open(os.DevNull)
	os.Stdout = devNull
	result := doctor.RunChecks()
	os.Stdout = origStdout
	devNull.Close()
	return result
}
