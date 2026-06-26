package cmd

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/setup"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/spf13/cobra"
)

var indexersCmd = &cobra.Command{
	Use:   "indexers",
	Short: "Prowlarr indexer status and management",
	Long: `Show Prowlarr indexer status and health.

Lists all configured indexers with enable/disable status and failure info.

Subcommands:
  setup     Interactive wizard to configure recommended indexers
  add       Add a specific indexer by name
  remove    Remove an indexer by name
  test      Test all indexer connectivity

API endpoints used:
  Prowlarr   GET /api/v1/indexer
  Prowlarr   GET /api/v1/indexerstatus`,
	Example: `  admirarr indexers
  admirarr indexers setup
  admirarr indexers add nyaa
  admirarr indexers remove LimeTorrents
  admirarr indexers test`,
	Run: runIndexers,
}

var indexersSetupCmd = &cobra.Command{
	Use:   "setup",
	Short: "Interactive wizard to configure recommended indexers",
	Long: `Guides you through setting up the recommended indexer configuration
for movies, TV series, and anime.

Recommended indexers:
  General:  1337x, The Pirate Bay, TorrentGalaxy, Knaben
  Movies:   YTS
  TV:       EZTV
  Anime:    Nyaa.si, SubsPlease, Anidex, Tokyo Toshokan

Indexers that require FlareSolverr (for Cloudflare bypass) will be
tagged automatically if FlareSolverr is configured in Prowlarr.`,
	Example: "  admirarr indexers setup",
	Run:     runIndexersSetup,
}

var indexersAddCmd = &cobra.Command{
	Use:   "add [indexer]",
	Short: "Add an indexer from the recommended list",
	Long: `Add a specific indexer by name or keyword.

Available indexers:
  1337x, eztv, yts, subsplease, nyaa, piratebay/tpb,
  torrentgalaxy/tg, knaben, tokyotosho, anidex

If the indexer needs FlareSolverr, it will be tagged automatically.`,
	Example: "  admirarr indexers add nyaa\n  admirarr indexers add tpb",
	Args:    cobra.ExactArgs(1),
	Run:     runIndexersAdd,
}

var indexersRemoveCmd = &cobra.Command{
	Use:     "remove [indexer]",
	Short:   "Remove an indexer by name",
	Example: "  admirarr indexers remove LimeTorrents",
	Args:    cobra.ExactArgs(1),
	Run:     runIndexersRemove,
}

var indexersTestCmd = &cobra.Command{
	Use:   "test",
	Short: "Test all indexer connectivity",
	Run:   runIndexersTest,
}

var indexersSyncCmd = &cobra.Command{
	Use:   "sync",
	Short: "Sync Prowlarr indexers to match config.yaml",
	Long: `Declaratively converge Prowlarr indexers to the state defined in config.yaml.

Actions taken:
  - Add indexers declared in config but missing from Prowlarr
  - Remove known indexers present in Prowlarr but not in config
  - Update FlareSolverr tags to match config
  - Custom/unknown indexers are left untouched

Example config:
  indexers:
    1337x:
      flare: true
    YTS: {}`,
	Example: "  admirarr indexers sync",
	Run:     runIndexersSync,
}

func init() {
	indexersCmd.AddCommand(indexersSetupCmd)
	indexersCmd.AddCommand(indexersAddCmd)
	indexersCmd.AddCommand(indexersRemoveCmd)
	indexersCmd.AddCommand(indexersTestCmd)
	indexersCmd.AddCommand(indexersSyncCmd)
	rootCmd.AddCommand(indexersCmd)
}

// ── Sync from config ──

func runIndexersSync(cmd *cobra.Command, args []string) {
	ui.PrintBanner()
	fmt.Println(ui.Bold("\n  Syncing indexers to config...\n"))

	r := setup.SyncIndexers()
	if len(r.Errors) > 0 {
		for _, e := range r.Errors {
			fmt.Printf("  %s %s\n", ui.Err("✗"), e)
		}
	}
	fmt.Printf("\n  %s %d passed, %s fixed\n\n",
		ui.Ok("✓"), r.Passed, ui.GoldText(fmt.Sprintf("%d", r.Fixed)))
}

// Use setup.RecommendedIndexers as the canonical list.
// Local alias for convenience.
var recommendedIndexers = setup.RecommendedIndexers

// ── List indexers ──

func runIndexers(cmd *cobra.Command, args []string) {
	client := arr.New("prowlarr")

	indexers, err := client.Indexers()
	if err != nil {
		if ui.IsJSON() {
			ui.PrintJSON(map[string]string{"error": "Cannot reach Prowlarr"})
		} else {
			ui.PrintBanner()
			fmt.Println(ui.Bold("\n  Prowlarr — Indexers\n"))
			fmt.Printf("  %s\n", ui.Err("Cannot reach Prowlarr"))
		}
		return
	}

	statuses, _ := client.IndexerStatuses()

	failedIDs := make(map[int]bool)
	for _, s := range statuses {
		if s.MostRecentFailure != "" {
			failedIDs[s.IndexerID] = true
		}
	}

	type indexerOut struct {
		Name    string `json:"name"`
		Enabled bool   `json:"enabled"`
		Status  string `json:"status"`
	}
	var out []indexerOut
	for _, idx := range indexers {
		st := "ok"
		if !idx.Enable {
			st = "disabled"
		} else if failedIDs[idx.ID] {
			st = "failing"
		}
		out = append(out, indexerOut{Name: idx.Name, Enabled: idx.Enable, Status: st})
	}

	ui.PrintOrJSON(out, func() {
		ui.PrintBanner()
		fmt.Println(ui.Bold("\n  Prowlarr — Indexers\n"))
		for _, idx := range indexers {
			icon := ui.Ok("●")
			status := ui.Ok("OK")
			if !idx.Enable {
				icon = ui.Dim("○")
				status = ui.Dim("DISABLED")
			} else if failedIDs[idx.ID] {
				icon = ui.Err("●")
				status = ui.Err("FAILING")
			}
			flare := ""
			for _, t := range idx.Tags {
				if t == 1 {
					flare = ui.Dim(" [flare]")
				}
			}
			cats := ""
			if len(idx.Capabilities.Categories) > 0 {
				var names []string
				for _, c := range idx.Capabilities.Categories {
					if len(names) < 3 {
						names = append(names, c.Name)
					}
				}
				cats = ui.Dim(" " + strings.Join(names, ", "))
			}
			fmt.Printf("  %s %-20s %-8s%s%s\n", icon, idx.Name, status, flare, cats)
		}
		fmt.Printf("\n  %s\n", ui.Dim(fmt.Sprintf("%d indexers total", len(indexers))))
		fmt.Printf("  %s\n\n", ui.Dim("Use 'admirarr indexers setup' to configure recommended indexers"))
	})
}

// ── Setup wizard ──

func runIndexersSetup(cmd *cobra.Command, args []string) {
	ui.PrintBanner()
	fmt.Println(ui.Bold("\n  Indexer Setup Wizard\n"))

	client := arr.New("prowlarr")

	// Check Prowlarr connectivity
	existing, err := client.Indexers()
	if err != nil {
		fmt.Printf("  %s\n\n", ui.Err("Cannot reach Prowlarr"))
		return
	}

	existingNames := make(map[string]bool)
	for _, idx := range existing {
		existingNames[strings.ToLower(idx.Name)] = true
	}

	// Check FlareSolverr
	flareTag := getFlareTag(client)
	if flareTag > 0 {
		fmt.Printf("  %s FlareSolverr detected (tag %d)\n\n", ui.Ok("●"), flareTag)
	} else {
		fmt.Printf("  %s FlareSolverr not configured\n", ui.Warn("⚠"))
		fmt.Printf("  %s\n\n", ui.Dim("Some indexers (Nyaa, 1337x, Anidex) need FlareSolverr for Cloudflare bypass"))
	}

	// Build options grouped by category
	categories := []string{"general", "movies", "tv", "anime"}
	categoryLabels := map[string]string{
		"general": "General (Movies + TV)",
		"movies":  "Movies",
		"tv":      "TV Series",
		"anime":   "Anime",
	}

	var toAdd []setup.IndexerDef
	for _, cat := range categories {
		fmt.Printf("  %s\n", ui.Bold(categoryLabels[cat]))

		var options []huh.Option[string]

		for _, def := range recommendedIndexers {
			if def.Category != cat {
				continue
			}
			label := def.Name
			if existingNames[strings.ToLower(def.Name)] {
				label += " (installed)"
			}
			if def.NeedsFlare {
				label += " [needs FlareSolverr]"
			}
			options = append(options, huh.NewOption(label, def.Name))
		}

		var selected []string
		err := huh.NewMultiSelect[string]().
			Title(categoryLabels[cat]).
			Options(options...).
			Value(&selected).
			Run()
		if err != nil {
			fmt.Printf("  %s\n\n", ui.Err("Cancelled"))
			return
		}

		for _, name := range selected {
			if existingNames[strings.ToLower(name)] {
				continue
			}
			for _, def := range recommendedIndexers {
				if def.Name == name {
					toAdd = append(toAdd, def)
				}
			}
		}
	}

	if len(toAdd) == 0 {
		fmt.Printf("\n  %s\n\n", ui.Dim("No new indexers to add"))
		return
	}

	// Confirm
	fmt.Printf("\n  Adding %d indexers:\n", len(toAdd))
	for _, def := range toAdd {
		flare := ""
		if def.NeedsFlare {
			flare = ui.Dim(" [flare]")
		}
		fmt.Printf("    %s %s%s\n", ui.GoldText("→"), def.Name, flare)
	}

	var confirm bool
	err = huh.NewConfirm().
		Title("Proceed?").
		Value(&confirm).
		Run()
	if err != nil || !confirm {
		fmt.Printf("  %s\n\n", ui.Dim("Cancelled"))
		return
	}

	fmt.Println()
	for _, def := range toAdd {
		addProwlarrIndexer(client, def, flareTag)
	}
	fmt.Println()
}

// ── Add single indexer ──

func runIndexersAdd(cmd *cobra.Command, args []string) {
	ui.PrintBanner()

	query := strings.ToLower(args[0])

	// Alias lookup
	aliases := map[string]string{
		"tpb":        "the pirate bay",
		"piratebay":  "the pirate bay",
		"tg":         "torrentgalaxy",
		"nyaa":       "nyaa.si",
		"tosho":      "tokyo toshokan",
		"tokyotosho": "tokyo toshokan",
	}
	if alias, ok := aliases[query]; ok {
		query = alias
	}

	var def *setup.IndexerDef
	for i, d := range recommendedIndexers {
		if strings.ToLower(d.Name) == query || strings.ToLower(d.DefinitionFile) == query {
			def = &recommendedIndexers[i]
			break
		}
	}

	if def == nil {
		fmt.Printf("\n  %s Unknown indexer: %s\n", ui.Err("✗"), args[0])
		fmt.Printf("  %s\n\n", ui.Dim("Available: 1337x, eztv, yts, subsplease, nyaa, tpb, torrentgalaxy, knaben, tokyotosho, anidex"))
		return
	}

	client := arr.New("prowlarr")

	// Check if already exists
	existing, err := client.Indexers()
	if err != nil {
		fmt.Printf("\n  %s\n\n", ui.Err("Cannot reach Prowlarr"))
		return
	}
	for _, idx := range existing {
		if strings.EqualFold(idx.Name, def.Name) {
			fmt.Printf("\n  %s %s is already configured (id=%d)\n\n", ui.Warn("⚠"), def.Name, idx.ID)
			return
		}
	}

	flareTag := getFlareTag(client)
	fmt.Println()
	addProwlarrIndexer(client, *def, flareTag)
	fmt.Println()
}

// ── Remove indexer ──

func runIndexersRemove(cmd *cobra.Command, args []string) {
	ui.PrintBanner()

	client := arr.New("prowlarr")

	indexers, err := client.Indexers()
	if err != nil {
		fmt.Printf("\n  %s\n\n", ui.Err("Cannot reach Prowlarr"))
		return
	}

	query := strings.ToLower(args[0])
	var target *arr.Indexer
	for i, idx := range indexers {
		if strings.EqualFold(idx.Name, query) || strings.EqualFold(idx.Name, args[0]) {
			target = &indexers[i]
			break
		}
	}

	if target == nil {
		fmt.Printf("\n  %s No indexer found matching: %s\n\n", ui.Err("✗"), args[0])
		return
	}

	if err := client.DeleteIndexer(target.ID); err != nil {
		fmt.Printf("\n  %s Failed to remove %s: %v\n\n", ui.Err("✗"), target.Name, err)
		return
	}

	fmt.Printf("\n  %s Removed %s\n\n", ui.Ok("✓"), target.Name)
}

// ── Test indexers ──

func runIndexersTest(cmd *cobra.Command, args []string) {
	ui.PrintBanner()
	fmt.Println(ui.Bold("\n  Testing Indexers\n"))

	client := arr.New("prowlarr")

	results, err := client.TestAllIndexers()
	if err != nil {
		fmt.Printf("  %s\n\n", ui.Err("Cannot reach Prowlarr"))
		return
	}

	// Get indexer names
	indexers, _ := client.Indexers()
	nameMap := make(map[int]string)
	for _, idx := range indexers {
		nameMap[idx.ID] = idx.Name
	}

	for _, r := range results {
		name := nameMap[r.ID]
		if name == "" {
			name = fmt.Sprintf("id=%d", r.ID)
		}
		if r.IsValid {
			fmt.Printf("  %s %-20s %s\n", ui.Ok("●"), name, ui.Ok("OK"))
		} else {
			msg := ""
			if len(r.ValidationFailures) > 0 {
				msg = r.ValidationFailures[0].ErrorMessage
				if len(msg) > 50 {
					msg = msg[:50] + "…"
				}
			}
			fmt.Printf("  %s %-20s %s %s\n", ui.Err("●"), name, ui.Err("FAIL"), ui.Dim(msg))
		}
	}
	fmt.Println()
}

// ── Helpers ──

func getFlareTag(client *arr.Client) int {
	proxies, err := client.IndexerProxies()
	if err == nil {
		for _, p := range proxies {
			if len(p.Tags) > 0 {
				return p.Tags[0]
			}
		}
	}
	return 0
}

func addProwlarrIndexer(client *arr.Client, def setup.IndexerDef, flareTag int) {
	fields := []map[string]interface{}{}

	// Definition file for Cardigann
	if def.DefinitionFile != "" {
		fields = append(fields, map[string]interface{}{
			"name": "definitionFile", "value": def.DefinitionFile,
		})
	}

	// Base URL if specified
	if def.BaseURL != "" {
		fields = append(fields, map[string]interface{}{
			"name": "baseUrl", "value": def.BaseURL,
		})
	}

	// Extra fields
	for k, v := range def.ExtraFields {
		fields = append(fields, map[string]interface{}{
			"name": k, "value": v,
		})
	}

	tags := []int{}
	if def.NeedsFlare && flareTag > 0 {
		tags = append(tags, flareTag)
	}

	// If it needs flare and no flare is configured, warn but still try
	if def.NeedsFlare && flareTag == 0 {
		fmt.Printf("  %s %s needs FlareSolverr — adding disabled\n", ui.Warn("⚠"), def.Name)
	}

	// Add disabled first to bypass validation, then enable
	payload := map[string]interface{}{
		"enable":         false,
		"name":           def.Name,
		"implementation": def.Implementation,
		"configContract": def.ConfigContract,
		"appProfileId":   1,
		"protocol":       "torrent",
		"priority":       25,
		"tags":           tags,
		"fields":         fields,
	}

	created, err := client.AddIndexer(payload)
	if err != nil {
		fmt.Printf("  %s Failed to add %s: %v\n", ui.Err("✗"), def.Name, err)
		return
	}

	if created.ID == 0 {
		// Check if it's a validation error array — re-marshal and check
		body, _ := json.Marshal(created)
		var errs []struct {
			ErrorMessage string `json:"errorMessage"`
		}
		if json.Unmarshal(body, &errs) == nil && len(errs) > 0 {
			msg := errs[0].ErrorMessage
			if len(msg) > 80 {
				msg = msg[:80] + "…"
			}
			fmt.Printf("  %s %s: %s\n", ui.Err("✗"), def.Name, msg)
			return
		}
		fmt.Printf("  %s %s: unexpected response\n", ui.Err("✗"), def.Name)
		return
	}

	// Now enable it
	payload["enable"] = true
	payload["id"] = created.ID
	err = client.UpdateIndexer(created.ID, payload)
	if err != nil {
		// Enable failed (connectivity issue) — leave disabled
		flareNote := ""
		if def.NeedsFlare {
			flareNote = " (needs FlareSolverr)"
		}
		fmt.Printf("  %s %s added but disabled — cannot reach site%s\n", ui.Warn("⚠"), def.Name, flareNote)
		return
	}

	flareNote := ""
	if def.NeedsFlare {
		flareNote = ui.Dim(" [flare]")
	}
	fmt.Printf("  %s %s%s\n", ui.Ok("✓"), def.Name, flareNote)
}
