package setup

import (
	"fmt"
	"strings"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/recyclarr"
	"github.com/maxtechera/admirarr/internal/ui"
)

// SyncQualityProfiles runs Phase 10: deploy Recyclarr if needed, generate config,
// sync TRaSH Guides, then ensure all items use the configured quality profile.
func SyncQualityProfiles(state *SetupState) StepResult {
	r := StepResult{Name: "Quality Profile Sync"}

	// Step 1: Ensure Recyclarr is available (deploy if missing + selected)
	rt := ensureRecyclarr(state)

	// Step 2: Generate and write recyclarr config with actual service URLs + keys
	if rt.Method != "none" {
		cfgContent := generateRecyclarrConfig(state)
		if cfgContent != "" {
			if err := writeRecyclarrConfig(state, cfgContent); err != nil {
				r.errf("failed to write recyclarr config: %v", err)
			} else {
				fmt.Printf("  %s Recyclarr config generated\n", ui.Ok("✓"))
				r.fix()
			}
		}
	}

	// Step 3: Run Recyclarr sync
	if rt.Method != "none" {
		syncRecyclarr(rt, &r)
	} else {
		fmt.Printf("  %s Recyclarr not available %s\n", ui.Dim("—"),
			ui.Dim("(optional — syncs TRaSH Guides quality profiles)"))
	}

	// Step 4: Ensure all items use the configured quality profile
	profile := config.QualityProfile()
	if profile == "" {
		fmt.Printf("  %s quality_profile not set in config, skipping profile assignment\n", ui.Dim("—"))
		if r.Passed == 0 && r.Fixed == 0 && len(r.Errors) == 0 {
			r.skip()
		}
		return r
	}

	fmt.Printf("\n  %s\n", ui.Bold("Quality Profile: "+profile))

	// Sync all reachable *Arr services
	for _, svcName := range []string{"radarr", "sonarr", "lidarr", "readarr", "whisparr"} {
		svc := state.Services[svcName]
		if svc == nil || !svc.Reachable {
			continue
		}
		switch svcName {
		case "radarr":
			syncRadarrQuality(profile, &r)
		case "sonarr":
			syncSonarrQuality(profile, &r)
		case "lidarr", "readarr", "whisparr":
			// These use the same quality profile model as radarr
			syncArrQuality(svcName, profile, &r)
		}
	}

	return r
}

func syncRecyclarr(rt recyclarr.Runtime, r *StepResult) {
	fmt.Printf("  %s Recyclarr detected (%s)\n", ui.Ok("●"), rt.Method)
	var output string
	var err error
	ui.SpinWhile("Deploying Recyclarr", func() error {
		output, err = recyclarr.Sync(rt, "")
		return err
	})
	if err != nil {
		r.errf("Recyclarr sync failed: %v", err)
		lines := strings.Split(strings.TrimSpace(output), "\n")
		start := 0
		if len(lines) > 5 {
			start = len(lines) - 5
		}
		for _, line := range lines[start:] {
			fmt.Printf("    %s\n", ui.Dim(line))
		}
	} else {
		r.fix()
		fmt.Printf("  %s Recyclarr sync complete\n", ui.Ok("✓"))
		results := recyclarr.Verify("radarr", "sonarr")
		for _, v := range results {
			if len(v.Issues) == 0 {
				fmt.Printf("  %s %s → %d profiles, %d custom formats\n",
					ui.Ok("✓"), titleCase(v.Service), v.QualityProfiles, v.CustomFormats)
			}
		}
	}
}

func syncRadarrQuality(profile string, r *StepResult) {
	client := arr.New("radarr")

	profileID := resolveProfileID(client, profile)
	if profileID == 0 {
		r.errf("Radarr → quality profile %q not found", profile)
		return
	}

	movies, err := client.Movies()
	if err != nil {
		r.errf("Radarr → cannot fetch movies: %v", err)
		return
	}

	changed := 0
	for _, m := range movies {
		if m.QualityProfileID == profileID {
			continue
		}
		full, err := client.GetMovieByID(m.ID)
		if err != nil {
			continue
		}
		full["qualityProfileId"] = profileID
		if err := client.UpdateMovie(m.ID, full); err != nil {
			r.errf("Radarr → failed to update %s: %v", m.Title, err)
			continue
		}
		changed++
	}

	if changed > 0 {
		fmt.Printf("  %s Radarr → updated %d movies to %s\n", ui.Ok("✓"), changed, profile)
		r.fix()
	} else {
		fmt.Printf("  %s Radarr → all %d movies already on %s\n", ui.Ok("✓"), len(movies), profile)
		r.pass()
	}
}

func syncSonarrQuality(profile string, r *StepResult) {
	client := arr.New("sonarr")

	profileID := resolveProfileID(client, profile)
	if profileID == 0 {
		r.errf("Sonarr → quality profile %q not found", profile)
		return
	}

	series, err := client.Series()
	if err != nil {
		r.errf("Sonarr → cannot fetch series: %v", err)
		return
	}

	changed := 0
	for _, s := range series {
		if s.QualityProfileID == profileID {
			continue
		}
		full, err := client.GetSeriesByID(s.ID)
		if err != nil {
			continue
		}
		full["qualityProfileId"] = profileID
		if err := client.UpdateSeries(s.ID, full); err != nil {
			r.errf("Sonarr → failed to update %s: %v", s.Title, err)
			continue
		}
		changed++
	}

	if changed > 0 {
		fmt.Printf("  %s Sonarr → updated %d series to %s\n", ui.Ok("✓"), changed, profile)
		r.fix()
	} else {
		fmt.Printf("  %s Sonarr → all %d series already on %s\n", ui.Ok("✓"), len(series), profile)
		r.pass()
	}
}

// syncArrQuality handles quality profile sync for optional *Arr services
// (Lidarr, Readarr, Whisparr) which share the same API shape.
func syncArrQuality(service, profile string, r *StepResult) {
	client := arr.New(service)

	profileID := resolveProfileID(client, profile)
	if profileID == 0 {
		// Not an error — optional services may not have the profile
		fmt.Printf("  %s %s → quality profile %q not found, skipping\n",
			ui.Dim("—"), titleCase(service), profile)
		r.skip()
		return
	}

	fmt.Printf("  %s %s → quality profile %q found (id=%d)\n",
		ui.Ok("✓"), titleCase(service), profile, profileID)
	r.pass()
}

func resolveProfileID(client *arr.Client, name string) int {
	profiles, err := client.QualityProfiles()
	if err != nil {
		return 0
	}
	for _, p := range profiles {
		if strings.EqualFold(p.Name, name) {
			return p.ID
		}
	}
	return 0
}
