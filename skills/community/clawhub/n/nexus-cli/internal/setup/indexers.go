package setup

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// IndexerDef describes a recommended indexer with its Prowlarr configuration.
type IndexerDef struct {
	Name           string
	Category       string // "general", "movies", "tv", "anime"
	Implementation string
	ConfigContract string
	DefinitionFile string
	BaseURL        string
	NeedsFlare     bool
	ExtraFields    map[string]interface{}
}

// RecommendedIndexers is the canonical list of recommended indexers.
var RecommendedIndexers = []IndexerDef{
	// General
	{Name: "1337x", Category: "general", Implementation: "Cardigann", ConfigContract: "CardigannSettings",
		DefinitionFile: "1337x", NeedsFlare: true},
	{Name: "The Pirate Bay", Category: "general", Implementation: "Cardigann", ConfigContract: "CardigannSettings",
		DefinitionFile: "thepiratebay", BaseURL: "https://thepiratebay.org/",
		ExtraFields: map[string]interface{}{"apiurl": "apibay.org"}},
	{Name: "TorrentGalaxy", Category: "general", Implementation: "Cardigann", ConfigContract: "CardigannSettings",
		DefinitionFile: "torrentgalaxyclone", BaseURL: "https://torrentgalaxy.info/"},
	{Name: "Knaben", Category: "general", Implementation: "Knaben", ConfigContract: "NoAuthTorrentBaseSettings",
		BaseURL: "https://knaben.org/"},

	// Movies
	{Name: "YTS", Category: "movies", Implementation: "Cardigann", ConfigContract: "CardigannSettings",
		DefinitionFile: "yts"},

	// TV
	{Name: "EZTV", Category: "tv", Implementation: "Cardigann", ConfigContract: "CardigannSettings",
		DefinitionFile: "eztv"},

	// Anime
	{Name: "Nyaa.si", Category: "anime", Implementation: "Cardigann", ConfigContract: "CardigannSettings",
		DefinitionFile: "nyaasi", BaseURL: "https://nyaa.si/", NeedsFlare: true},
	{Name: "SubsPlease", Category: "anime", Implementation: "SubsPlease", ConfigContract: "SubsPleaseSettings"},
	{Name: "Anidex", Category: "anime", Implementation: "Anidex", ConfigContract: "AnidexSettings",
		BaseURL: "https://anidex.info/", NeedsFlare: true,
		ExtraFields: map[string]interface{}{"authorisedOnly": false}},
	{Name: "Tokyo Toshokan", Category: "anime", Implementation: "Cardigann", ConfigContract: "CardigannSettings",
		DefinitionFile: "tokyotosho", BaseURL: "https://www.tokyotosho.info/"},
}

// lookupRecommendedIndexer finds an IndexerDef by name (case-insensitive).
func lookupRecommendedIndexer(name string) (IndexerDef, bool) {
	for _, def := range RecommendedIndexers {
		if strings.EqualFold(def.Name, name) {
			return def, true
		}
	}
	return IndexerDef{}, false
}

// VerifyIndexers runs Phase 7: declarative indexer sync + Prowlarr wiring.
// Reads config.Indexers and converges Prowlarr to match.
func VerifyIndexers(state *SetupState) StepResult {
	r := StepResult{Name: "Prowlarr Wiring"}

	svc := state.Services["prowlarr"]
	if svc == nil || !svc.Reachable {
		fmt.Printf("  %s Prowlarr %s\n", ui.Dim("—"), ui.Dim("skipped (not reachable)"))
		r.skip()
		return r
	}

	client := arr.New("prowlarr")

	// Wire FlareSolverr proxy first
	flareTag := wireFlareProxy(state, &r, client)

	desired := config.GetIndexers()

	// Get current indexers from Prowlarr (single fetch, reused below)
	existing, fetchErr := client.Indexers()

	// If no indexers in config, auto-populate from recommended list
	// But skip if Prowlarr already has indexers configured (partial stack)
	if len(desired) == 0 && (state.Indexers == nil || len(state.Indexers) == 0) {
		if fetchErr == nil && len(existing) > 0 {
			fmt.Printf("  %s Prowlarr already has %d indexer(s), skipping auto-select\n", ui.Ok("✓"), len(existing))
		} else {
			state.Indexers = selectRecommendedIndexers(state)
		}
	}

	// Use state.Indexers if populated (from auto-select or interactive)
	if len(desired) == 0 && len(state.Indexers) > 0 {
		desired = state.Indexers
	}

	if len(desired) == 0 {
		fmt.Printf("  %s No indexers declared in config, skipping indexer sync\n", ui.Dim("—"))
		r.skip()
	} else if fetchErr != nil {
		r.errf("cannot query Prowlarr indexers: %v", fetchErr)
	} else {
		syncIndexers(state, &r, client, existing, desired, flareTag)
	}

	// Wire sync targets (Radarr, Sonarr)
	wireSyncTargets(state, &r, client)

	return r
}

// SyncIndexers is the standalone version called by `indexers sync`.
func SyncIndexers() StepResult {
	state := &SetupState{
		Services: make(map[string]*ServiceState),
		Keys:     make(map[string]string),
	}
	state.Services["prowlarr"] = &ServiceState{Reachable: api.CheckReachable("prowlarr")}
	state.Services["radarr"] = &ServiceState{Reachable: api.CheckReachable("radarr")}
	state.Services["sonarr"] = &ServiceState{Reachable: api.CheckReachable("sonarr")}
	return VerifyIndexers(state)
}

func syncIndexers(state *SetupState, r *StepResult, client *arr.Client, existing []arr.Indexer, desired map[string]config.IndexerConfig, flareTag int) {
	existingByName := make(map[string]arr.Indexer)
	for _, idx := range existing {
		existingByName[strings.ToLower(idx.Name)] = idx
	}

	// Converge: add missing, update flare tags
	for name, ic := range desired {
		if !ic.IsEnabled() {
			continue
		}

		lower := strings.ToLower(name)
		if idx, ok := existingByName[lower]; ok {
			// Already exists — check flare tag
			updated := ensureFlareTag(client, idx, ic.Flare, flareTag)
			if updated {
				fmt.Printf("  %s %s — updated flare tag\n", ui.GoldText("↻"), name)
				r.fix()
			} else {
				fmt.Printf("  %s %s\n", ui.Ok("✓"), name)
				r.pass()
			}
			delete(existingByName, lower)
		} else {
			// Need to add
			added := addIndexer(client, name, ic, flareTag)
			if added {
				fmt.Printf("  %s %s — added\n", ui.Ok("✓"), name)
				r.fix()
			} else {
				r.errf("failed to add indexer: %s", name)
			}
		}
	}

	// Remove indexers not in config
	for _, idx := range existingByName {
		if _, known := lookupRecommendedIndexer(idx.Name); known {
			if err := client.DeleteIndexer(idx.ID); err != nil {
				r.errf("failed to remove %s: %v", idx.Name, err)
			} else {
				fmt.Printf("  %s %s — removed (not in config)\n", ui.Dim("−"), idx.Name)
				r.fix()
			}
		}
	}
}

func wireFlareProxy(state *SetupState, r *StepResult, client *arr.Client) int {
	// Check if FlareSolverr is in the stack and reachable
	flareSvc := state.Services["flaresolverr"]
	if flareSvc == nil || !flareSvc.Reachable {
		return getFlareTag(client) // might still have a tag from previous setup
	}

	// Check existing proxies
	proxies, err := client.IndexerProxies()
	if err == nil {
		for _, p := range proxies {
			if len(p.Tags) > 0 {
				fmt.Printf("  %s FlareSolverr proxy exists (tag %d)\n", ui.Ok("✓"), p.Tags[0])
				r.pass()
				return p.Tags[0]
			}
		}
	}

	// Create tag
	var tagResp struct {
		ID int `json:"id"`
	}
	_, err = client.Post("api/v1/tag", map[string]interface{}{"label": "flaresolverr"}, nil)
	if err != nil {
		r.errf("failed to create FlareSolverr tag: %v", err)
		return 0
	}

	// Fetch tag to get ID
	var tags []struct {
		ID    int    `json:"id"`
		Label string `json:"label"`
	}
	if err := client.GetJSON("api/v1/tag", nil, &tags); err == nil {
		for _, t := range tags {
			if t.Label == "flaresolverr" {
				tagResp.ID = t.ID
				break
			}
		}
	}

	if tagResp.ID == 0 {
		r.errf("failed to get FlareSolverr tag ID")
		return 0
	}

	// Create proxy
	flareURL := state.InternalURL("flaresolverr")
	proxyPayload := map[string]interface{}{
		"name":           "FlareSolverr",
		"implementation": "FlareSolverr",
		"configContract": "FlareSolverrSettings",
		"fields": []map[string]interface{}{
			{"name": "host", "value": flareURL},
			{"name": "requestTimeout", "value": 60},
		},
		"tags": []int{tagResp.ID},
	}

	_, err = client.Post("api/v1/indexerProxy", proxyPayload, nil)
	if err != nil {
		r.errf("failed to create FlareSolverr proxy: %v", err)
		return 0
	}

	fmt.Printf("  %s FlareSolverr proxy created (tag %d)\n", ui.Ok("✓"), tagResp.ID)
	r.fix()
	return tagResp.ID
}

func wireSyncTargets(state *SetupState, r *StepResult, client *arr.Client) {
	apps, err := client.Applications()
	if err != nil {
		return
	}

	fmt.Printf("\n  %s\n", ui.Bold("Sync Targets"))

	for _, service := range []string{"radarr", "sonarr", "lidarr", "readarr", "whisparr"} {
		svc := state.Services[service]
		if svc == nil || !svc.Reachable || state.Keys[service] == "" {
			continue
		}

		// Check if already synced
		synced := false
		for _, app := range apps {
			if strings.EqualFold(app.Implementation, service) ||
				strings.EqualFold(app.Name, service) {
				synced = true
				fmt.Printf("  %s %s (%s, sync: %s)\n", ui.Ok("✓"), app.Name,
					ui.Dim(app.Implementation), ui.Dim(app.SyncLevel))
				r.pass()
				break
			}
		}

		if synced {
			continue
		}

		// Create sync target
		createSyncTarget(state, r, client, service)
	}
}

func createSyncTarget(state *SetupState, r *StepResult, client *arr.Client, service string) {
	impl := strings.ToUpper(service[:1]) + service[1:] // "radarr" → "Radarr"
	contract := impl + "Settings"

	payload := map[string]interface{}{
		"name":           impl,
		"syncLevel":      "fullSync",
		"implementation": impl,
		"configContract": contract,
		"fields": []map[string]interface{}{
			{"name": "prowlarrUrl", "value": state.InternalURL("prowlarr")},
			{"name": "baseUrl", "value": state.InternalURL(service)},
			{"name": "apiKey", "value": state.Keys[service]},
		},
		"tags": []int{},
	}

	_, err := client.Post("api/v1/applications", payload, nil)
	if err != nil {
		fmt.Printf("  %s %s sync target failed: %v\n", ui.Err("✗"), impl, err)
		r.errf("failed to create %s sync target: %v", service, err)
		return
	}

	fmt.Printf("  %s %s sync target created\n", ui.Ok("✓"), impl)
	r.fix()
}

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

func ensureFlareTag(client *arr.Client, idx arr.Indexer, wantFlare bool, flareTag int) bool {
	if flareTag == 0 || !wantFlare {
		return false
	}

	hasTag := false
	for _, t := range idx.Tags {
		if t == flareTag {
			hasTag = true
			break
		}
	}

	if hasTag == wantFlare {
		return false
	}

	// Need to update
	tags := idx.Tags
	if wantFlare && !hasTag {
		tags = append(tags, flareTag)
	}

	// GET full indexer first to have complete payload
	full, err := client.GetIndexerByID(idx.ID)
	if err != nil {
		return false
	}
	full["tags"] = tags

	err = client.UpdateIndexer(idx.ID, full)
	return err == nil
}

func addIndexer(client *arr.Client, name string, ic config.IndexerConfig, flareTag int) bool {
	def, ok := lookupRecommendedIndexer(name)
	if !ok {
		fmt.Printf("  %s %s — unknown indexer, skipping\n", ui.Warn("?"), name)
		return false
	}
	name = def.Name // use canonical name

	fields := []map[string]interface{}{}

	if def.DefinitionFile != "" {
		fields = append(fields, map[string]interface{}{
			"name": "definitionFile", "value": def.DefinitionFile,
		})
	}

	if ic.BaseURL != "" {
		fields = append(fields, map[string]interface{}{
			"name": "baseUrl", "value": ic.BaseURL,
		})
	}

	for k, v := range ic.ExtraFields {
		fields = append(fields, map[string]interface{}{
			"name": k, "value": v,
		})
	}

	tags := []int{}
	if ic.Flare && flareTag > 0 {
		tags = append(tags, flareTag)
	}

	// Add disabled first to bypass connectivity validation
	payload := map[string]interface{}{
		"enable":         false,
		"name":           name,
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
		fmt.Printf("  %s %s — POST failed: %v\n", ui.Err("✗"), name, err)
		return false
	}

	if created.ID == 0 {
		// Check for validation error
		body, _ := json.Marshal(created)
		var errs []struct {
			ErrorMessage string `json:"errorMessage"`
		}
		if json.Unmarshal(body, &errs) == nil && len(errs) > 0 {
			fmt.Printf("  %s %s — %s\n", ui.Err("✗"), name, errs[0].ErrorMessage)
		}
		return false
	}

	// Now enable via PUT
	payload["enable"] = true
	payload["id"] = created.ID
	err = client.UpdateIndexer(created.ID, payload)
	if err != nil {
		flareNote := ""
		if ic.Flare {
			flareNote = " (needs FlareSolverr)"
		}
		fmt.Printf("  %s %s — added disabled%s\n", ui.Warn("⚠"), name, flareNote)
		return true // still added, just disabled
	}

	return true
}

// selectRecommendedIndexers lets the user choose from recommended indexers
// (or auto-selects all in auto mode) and returns them as IndexerConfig entries.
func selectRecommendedIndexers(state *SetupState) map[string]config.IndexerConfig {
	if state.AutoMode {
		// Auto mode: add all recommended indexers
		result := make(map[string]config.IndexerConfig, len(RecommendedIndexers))
		for _, def := range RecommendedIndexers {
			result[def.Name] = defToIndexerConfig(def)
		}
		fmt.Printf("  %s Auto-selected %d recommended indexers\n", ui.Ok("✓"), len(result))
		return result
	}

	// Interactive: multi-select grouped by category
	categories := []string{"general", "movies", "tv", "anime"}
	categoryLabels := map[string]string{
		"general": "General (Movies + TV)",
		"movies":  "Movies",
		"tv":      "TV Series",
		"anime":   "Anime",
	}

	var allSelected []string
	for _, cat := range categories {
		var options []huh.Option[string]
		for _, def := range RecommendedIndexers {
			if def.Category != cat {
				continue
			}
			label := def.Name
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
			continue
		}
		allSelected = append(allSelected, selected...)
	}

	if len(allSelected) == 0 {
		return nil
	}

	result := make(map[string]config.IndexerConfig, len(allSelected))
	for _, name := range allSelected {
		for _, def := range RecommendedIndexers {
			if def.Name == name {
				result[name] = defToIndexerConfig(def)
				break
			}
		}
	}
	fmt.Printf("  %s Selected %d indexers\n", ui.Ok("✓"), len(result))
	return result
}

// defToIndexerConfig converts an IndexerDef to a config.IndexerConfig.
func defToIndexerConfig(def IndexerDef) config.IndexerConfig {
	return config.IndexerConfig{
		Flare:       def.NeedsFlare,
		BaseURL:     def.BaseURL,
		ExtraFields: def.ExtraFields,
	}
}
