package cmd

import (
	"fmt"
	"strings"

	"github.com/maxtechera/admirarr/internal/recyclarr"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var recyclarrCmd = &cobra.Command{
	Use:   "recyclarr",
	Short: "Recyclarr integration — sync TRaSH Guides quality profiles & custom formats",
	Long: `Manage Recyclarr, the community tool that syncs TRaSH Guides quality
profiles and custom formats to Radarr and Sonarr.

Without subcommands, shows Recyclarr detection status, version, and
configured instances.

Subcommands:
  sync       Run Recyclarr sync (applies TRaSH Guides to *Arr services)
  verify     Check quality profiles & custom formats via *Arr APIs
  instances  List configured Recyclarr instances`,
	Example: `  admirarr recyclarr
  admirarr recyclarr sync
  admirarr recyclarr sync radarr
  admirarr recyclarr verify`,
	Run: runRecyclarr,
}

var recyclarrSyncCmd = &cobra.Command{
	Use:   "sync [instance]",
	Short: "Run Recyclarr sync",
	Long: `Invokes Recyclarr to sync TRaSH Guides quality profiles and custom
formats to your *Arr services. Optionally specify an instance name
to sync only that instance.

Recyclarr must be installed (native binary or Docker container).
Use 'admirarr recyclarr' to check detection status.`,
	Example: `  admirarr recyclarr sync
  admirarr recyclarr sync radarr`,
	Run: runRecyclarrSync,
}

var recyclarrVerifyCmd = &cobra.Command{
	Use:   "verify",
	Short: "Verify quality profiles & custom formats are applied",
	Long: `Checks Radarr and Sonarr APIs directly to verify that quality profiles
and custom formats are configured. Does not require Recyclarr to be
installed — queries the service APIs.`,
	Example: "  admirarr recyclarr verify",
	Run:     runRecyclarrVerify,
}

var recyclarrInstancesCmd = &cobra.Command{
	Use:     "instances",
	Short:   "List configured Recyclarr instances",
	Example: "  admirarr recyclarr instances",
	Run:     runRecyclarrInstances,
}

func init() {
	recyclarrCmd.AddCommand(recyclarrSyncCmd)
	recyclarrCmd.AddCommand(recyclarrVerifyCmd)
	recyclarrCmd.AddCommand(recyclarrInstancesCmd)
	rootCmd.AddCommand(recyclarrCmd)
}

func runRecyclarr(cmd *cobra.Command, args []string) {
	rt := recyclarr.Detect()

	if ui.IsJSON() {
		type instanceJSON struct {
			Name string `json:"name"`
		}
		type out struct {
			Method    string         `json:"method"`
			Version   string         `json:"version,omitempty"`
			Path      string         `json:"path,omitempty"`
			Instances []instanceJSON `json:"instances"`
		}
		o := out{Method: rt.Method, Version: rt.Version, Path: rt.Path}
		if rt.Method != "none" {
			if instances, err := recyclarr.ListInstances(rt); err == nil {
				for _, inst := range instances {
					o.Instances = append(o.Instances, instanceJSON{Name: inst})
				}
			}
		}
		if o.Instances == nil {
			o.Instances = []instanceJSON{}
		}
		ui.PrintJSON(o)
		return
	}

	ui.PrintBanner()
	fmt.Println(ui.Bold("\n  Recyclarr"))
	fmt.Println(ui.Separator())

	switch rt.Method {
	case "native":
		fmt.Printf("  %s Installed (native): %s\n", ui.Ok("●"), rt.Path)
		if rt.Version != "" {
			fmt.Printf("  %s Version: %s\n", ui.Dim(" "), rt.Version)
		}
	case "docker":
		fmt.Printf("  %s Installed (Docker): %s\n", ui.Ok("●"), rt.Path)
		if rt.Version != "" {
			fmt.Printf("  %s Version: %s\n", ui.Dim(" "), rt.Version)
		}
	default:
		fmt.Printf("  %s Not installed\n", ui.Err("○"))
		fmt.Printf("\n  %s\n", ui.Dim("Recyclarr syncs TRaSH Guides quality profiles and custom"))
		fmt.Printf("  %s\n", ui.Dim("formats to Radarr/Sonarr. Install it to get optimal quality."))
		fmt.Printf("\n  %s Run %s to deploy all missing services\n", ui.Dim("→"), ui.GoldText("admirarr setup"))
		fmt.Printf("  %s Run %s to auto-fix detected issues\n\n", ui.Dim("→"), ui.GoldText("admirarr doctor --fix"))
		return
	}

	// List instances
	instances, err := recyclarr.ListInstances(rt)
	if err != nil {
		fmt.Printf("\n  %s Cannot list instances: %v\n", ui.Warn("⚠"), err)
	} else if len(instances) > 0 {
		fmt.Printf("\n  %s\n", ui.Bold("Instances"))
		for _, inst := range instances {
			fmt.Printf("  %s %s\n", ui.Dim("→"), inst)
		}
	} else {
		fmt.Printf("\n  %s\n", ui.Dim("No instances configured"))
		fmt.Printf("  %s\n", ui.Dim("Create a recyclarr.yml config to define instances"))
	}

	// Quick verify
	fmt.Printf("\n  %s\n", ui.Bold("Applied Config"))
	results := recyclarr.Verify("radarr", "sonarr")
	for _, v := range results {
		if len(v.Issues) > 0 {
			for _, issue := range v.Issues {
				fmt.Printf("  %s [%s] %s\n", ui.Err("✗"), v.Service, issue)
			}
			continue
		}
		profileInfo := fmt.Sprintf("%d profiles", v.QualityProfiles)
		formatInfo := fmt.Sprintf("%d custom formats", v.CustomFormats)
		if v.CustomFormats > 0 {
			fmt.Printf("  %s [%s] %s, %s\n", ui.Ok("✓"), v.Service, profileInfo, formatInfo)
		} else {
			fmt.Printf("  %s [%s] %s, %s\n", ui.Warn("!"), v.Service, profileInfo, formatInfo)
		}
	}

	fmt.Printf("\n  %s\n\n", ui.Dim("Run 'admirarr recyclarr sync' to apply TRaSH Guides"))
}

func runRecyclarrSync(cmd *cobra.Command, args []string) {
	rt := recyclarr.Detect()

	if rt.Method == "none" {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "Recyclarr not installed"})
		} else {
			ui.PrintBanner()
			fmt.Printf("\n  %s Recyclarr not installed\n", ui.Err("✗"))
			fmt.Printf("  %s Run %s to deploy it\n", ui.Dim("→"), ui.GoldText("admirarr setup"))
			fmt.Printf("  %s Run %s to auto-fix\n\n", ui.Dim("→"), ui.GoldText("admirarr doctor --fix"))
		}
		return
	}

	instance := ""
	if len(args) > 0 {
		instance = args[0]
	}

	if !ui.IsJSON() {
		ui.PrintBanner()
		target := "all instances"
		if instance != "" {
			target = instance
		}
		fmt.Printf("\n  %s Syncing %s via %s…\n\n", ui.GoldText("⟳"), target, rt.Method)
	}

	output, err := recyclarr.Sync(rt, instance)

	if ui.IsJSON() {
		ui.PrintJSON(map[string]interface{}{
			"success":  err == nil,
			"instance": instance,
			"output":   output,
		})
		return
	}

	// Show recyclarr output indented
	if output != "" {
		for _, line := range strings.Split(strings.TrimSpace(output), "\n") {
			fmt.Printf("  %s\n", ui.Dim(line))
		}
		fmt.Println()
	}

	if err != nil {
		fmt.Printf("  %s Sync failed: %v\n\n", ui.Err("✗"), err)
		return
	}

	fmt.Printf("  %s Sync complete\n", ui.Ok("✓"))

	// Verify after sync
	fmt.Printf("\n  %s\n", ui.Bold("Verification"))
	results := recyclarr.Verify("radarr", "sonarr")
	for _, v := range results {
		if len(v.Issues) > 0 {
			for _, issue := range v.Issues {
				fmt.Printf("  %s [%s] %s\n", ui.Err("✗"), v.Service, issue)
			}
			continue
		}
		fmt.Printf("  %s [%s] %d profiles, %d custom formats\n",
			ui.Ok("✓"), v.Service, v.QualityProfiles, v.CustomFormats)
	}
	fmt.Println()
}

func runRecyclarrVerify(cmd *cobra.Command, args []string) {
	results := recyclarr.Verify("radarr", "sonarr")

	if ui.IsJSON() {
		type verifyJSON struct {
			Service         string `json:"service"`
			QualityProfiles int    `json:"quality_profiles"`
			CustomFormats   int    `json:"custom_formats"`
			ProfilesOK     bool   `json:"profiles_applied"`
			FormatsOK      bool   `json:"formats_applied"`
			Issues          []string `json:"issues"`
		}
		var out []verifyJSON
		for _, v := range results {
			issues := v.Issues
			if issues == nil {
				issues = []string{}
			}
			out = append(out, verifyJSON{
				Service:         v.Service,
				QualityProfiles: v.QualityProfiles,
				CustomFormats:   v.CustomFormats,
				ProfilesOK:      v.ProfilesApplied,
				FormatsOK:       v.FormatsApplied,
				Issues:          issues,
			})
		}
		ui.PrintJSON(out)
		return
	}

	ui.PrintBanner()
	fmt.Println(ui.Bold("\n  Quality & Custom Formats"))
	fmt.Println(ui.Separator())

	for _, v := range results {
		if len(v.Issues) > 0 {
			for _, issue := range v.Issues {
				fmt.Printf("  %s [%s] %s\n", ui.Err("✗"), v.Service, issue)
			}
			continue
		}

		profileInfo := fmt.Sprintf("%d quality profiles", v.QualityProfiles)
		formatInfo := fmt.Sprintf("%d custom formats", v.CustomFormats)

		icon := ui.Ok("✓")
		hint := ""
		if v.CustomFormats == 0 {
			icon = ui.Warn("!")
			hint = " " + ui.Dim("(run 'admirarr recyclarr sync' to apply TRaSH Guides)")
		}
		fmt.Printf("  %s [%s] %s, %s%s\n", icon, v.Service, profileInfo, formatInfo, hint)
	}
	fmt.Println()
}

func runRecyclarrInstances(cmd *cobra.Command, args []string) {
	rt := recyclarr.Detect()

	if rt.Method == "none" {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "Recyclarr not installed"})
		} else {
			ui.PrintBanner()
			fmt.Printf("\n  %s Recyclarr not installed\n\n", ui.Err("✗"))
		}
		return
	}

	instances, err := recyclarr.ListInstances(rt)
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": err.Error()})
		} else {
			ui.PrintBanner()
			fmt.Printf("\n  %s Cannot list instances: %v\n\n", ui.Err("✗"), err)
		}
		return
	}

	if ui.IsJSON() {
		ui.PrintJSON(instances)
		return
	}

	ui.PrintBanner()
	fmt.Println(ui.Bold("\n  Recyclarr Instances"))
	fmt.Println(ui.Separator())
	if len(instances) == 0 {
		fmt.Printf("  %s\n", ui.Dim("No instances configured"))
	} else {
		for _, inst := range instances {
			fmt.Printf("  %s %s\n", ui.Dim("→"), inst)
		}
	}
	fmt.Println()
}
