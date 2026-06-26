package doctor

import (
	"fmt"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
	"github.com/maxtechera/admirarr/internal/wire"
)

// checkCrossService validates wiring between services:
// Prowlarr sync targets, FlareSolverr proxy, Bazarr connections, Seerr connections.
func checkCrossService(r *Result) {
	fmt.Println(ui.Bold("\n  Cross-Service Wiring"))
	fmt.Println(ui.Separator())

	// 1. Prowlarr sync targets (Radarr + Sonarr)
	if api.CheckReachable("prowlarr") {
		syncResults := wire.CheckSyncTargets()
		for _, res := range syncResults {
			switch res.Action {
			case "ok":
				r.ChecksPassed++
				fmt.Printf("  %s [prowlarr → %s] %s\n", ui.Ok("✓"), res.Target, res.Detail)
			case "failed":
				r.Issues = append(r.Issues, Issue{Description:
					fmt.Sprintf("PROWLARR SYNC: %s sync target — %s. Run admirarr setup to fix.", res.Target, res.Detail),
				})
				fmt.Printf("  %s [prowlarr → %s] %s\n", ui.Err("✗"), res.Target, ui.Err(res.Detail))
			}
		}

		// 2. FlareSolverr proxy
		if config.IsConfigured("flaresolverr") {
			flareResult := wire.CheckFlareProxy()
			switch flareResult.Action {
			case "ok":
				r.ChecksPassed++
				fmt.Printf("  %s [prowlarr → flaresolverr] %s\n", ui.Ok("✓"), flareResult.Detail)
			case "failed":
				r.Issues = append(r.Issues, Issue{Description:
					fmt.Sprintf("FLARESOLVERR: %s. Run admirarr setup to configure.", flareResult.Detail),
				})
				fmt.Printf("  %s [prowlarr → flaresolverr] %s\n", ui.Err("✗"), ui.Err(flareResult.Detail))
			}
		}
	} else {
		fmt.Printf("  %s %s\n", ui.Dim("—"), ui.Dim("Prowlarr not reachable (skipping sync target checks)"))
	}

	// 3. Bazarr → Radarr/Sonarr connections
	if api.CheckReachable("bazarr") {
		checkBazarrConnections(r)
	} else if config.IsConfigured("bazarr") {
		fmt.Printf("  %s [bazarr] %s\n", ui.Dim("—"), ui.Dim("not reachable"))
	}

	// 4. Seerr → media server + *Arr connections
	if api.CheckReachable("seerr") {
		checkSeerrConnections(r)
	} else if config.IsConfigured("seerr") {
		fmt.Printf("  %s [seerr] %s\n", ui.Dim("—"), ui.Dim("not reachable"))
	}
}

// checkBazarrConnections validates Bazarr's connections to Radarr and Sonarr
// via the Bazarr system status API.
func checkBazarrConnections(r *Result) {
	client := api.NewClient("bazarr")

	var status struct {
		Data struct {
			RadarrVersion string `json:"radarr_version"`
			SonarrVersion string `json:"sonarr_version"`
		} `json:"data"`
	}

	err := client.GetJSON("api/system/status", nil, &status)
	if err != nil {
		fmt.Printf("  %s [bazarr] %s\n", ui.Dim("—"), ui.Dim("cannot query status"))
		return
	}

	if status.Data.RadarrVersion != "" {
		r.ChecksPassed++
		fmt.Printf("  %s [bazarr → radarr] connected\n", ui.Ok("✓"))
	} else if config.IsConfigured("radarr") {
		r.Issues = append(r.Issues, Issue{Description:
			"BAZARR: Not connected to Radarr. Configure in Bazarr Settings → Radarr.",
		})
		fmt.Printf("  %s [bazarr → radarr] %s\n", ui.Err("✗"), ui.Err("not connected"))
	}

	if status.Data.SonarrVersion != "" {
		r.ChecksPassed++
		fmt.Printf("  %s [bazarr → sonarr] connected\n", ui.Ok("✓"))
	} else if config.IsConfigured("sonarr") {
		r.Issues = append(r.Issues, Issue{Description:
			"BAZARR: Not connected to Sonarr. Configure in Bazarr Settings → Sonarr.",
		})
		fmt.Printf("  %s [bazarr → sonarr] %s\n", ui.Err("✗"), ui.Err("not connected"))
	}
}

// checkSeerrConnections validates Seerr has a media server and *Arr services configured.
func checkSeerrConnections(r *Result) {
	client := api.NewClient("seerr")

	var settings struct {
		Initialized bool `json:"initialized"`
	}

	err := client.GetJSON("api/v1/settings/main", nil, &settings)
	if err != nil {
		fmt.Printf("  %s [seerr] %s\n", ui.Dim("—"), ui.Dim("cannot query settings"))
		return
	}

	if settings.Initialized {
		r.ChecksPassed++
		fmt.Printf("  %s [seerr] initialized and configured\n", ui.Ok("✓"))
	} else {
		r.Issues = append(r.Issues, Issue{Description:
			"SEERR: Not initialized. Complete setup at the Seerr web UI.",
		})
		fmt.Printf("  %s [seerr] %s\n", ui.Err("✗"), ui.Err("not initialized"))
	}
}
