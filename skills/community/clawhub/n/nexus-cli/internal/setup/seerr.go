package setup

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/cookiejar"
	"net/url"
	"time"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/ui"
)

// seerrArrEntry represents a Seerr Radarr/Sonarr server config entry.
type seerrArrEntry struct {
	ID                int    `json:"id"`
	Name              string `json:"name"`
	Hostname          string `json:"hostname"`
	Port              int    `json:"port"`
	APIKey            string `json:"apiKey"`
	IsDefault         bool   `json:"isDefault"`
	ActiveProfileID   int    `json:"activeProfileId"`
	ActiveDirectory   string `json:"activeDirectory"`
}

// WireSeerr runs Phase 8: connect Seerr to Radarr/Sonarr/media server.
func WireSeerr(state *SetupState) StepResult {
	r := StepResult{Name: "Seerr Wiring"}

	svc := state.Services["seerr"]
	if svc == nil || !svc.Reachable {
		fmt.Printf("  %s Seerr %s\n", ui.Dim("—"), ui.Dim("skipped (not in stack or unreachable)"))
		r.skip()
		return r
	}

	// Try to initialize Seerr if it has no API key yet
	if state.Keys["seerr"] == "" {
		initSeerr(state, svc, &r)
	}

	if state.Keys["seerr"] == "" {
		fmt.Printf("  %s Seerr %s\n", ui.Dim("—"), ui.Dim("skipped (no API key)"))
		r.skip()
		return r
	}

	// Wire Radarr → Seerr
	if radarrSvc := state.Services["radarr"]; radarrSvc != nil && radarrSvc.Reachable && state.Keys["radarr"] != "" {
		wireArrToSeerr(state, &r, "radarr")
	} else {
		fmt.Printf("  %s Radarr %s\n", ui.Dim("—"), ui.Dim("skipped (not reachable)"))
	}

	// Wire Sonarr → Seerr
	if sonarrSvc := state.Services["sonarr"]; sonarrSvc != nil && sonarrSvc.Reachable && state.Keys["sonarr"] != "" {
		wireArrToSeerr(state, &r, "sonarr")
	} else {
		fmt.Printf("  %s Sonarr %s\n", ui.Dim("—"), ui.Dim("skipped (not reachable)"))
	}

	// Check media server wiring (Jellyfin/Plex)
	checkSeerrMediaServer(state, &r)

	return r
}

func wireArrToSeerr(state *SetupState, r *StepResult, service string) {
	endpoint := fmt.Sprintf("api/v1/settings/%s", service)

	// Check existing
	var existing []seerrArrEntry
	if err := api.GetJSON("seerr", endpoint, nil, &existing); err == nil {
		for _, entry := range existing {
			if entry.APIKey == state.Keys[service] {
				fmt.Printf("  %s Seerr → %s connected\n", ui.Ok("✓"), service)
				r.pass()
				return
			}
		}
	}

	// Get metadata from the service
	client := arr.New(service)

	profiles, err := client.QualityProfiles()
	if err != nil || len(profiles) == 0 {
		r.errf("Seerr: cannot get %s quality profiles: %v", service, err)
		return
	}

	roots, err := client.RootFolders()
	if err != nil || len(roots) == 0 {
		r.errf("Seerr: cannot get %s root folders: %v", service, err)
		return
	}

	// Parse hostname from internal URL
	internalURL := state.InternalURL(service)
	parsed, _ := url.Parse(internalURL)
	hostname := parsed.Hostname()
	port := config.ServicePort(service)

	// Build payload
	payload := map[string]interface{}{
		"name":              service,
		"hostname":          hostname,
		"port":              port,
		"apiKey":            state.Keys[service],
		"useSsl":            false,
		"activeProfileId":   profiles[0].ID,
		"activeDirectory":   roots[0].Path,
		"is4k":              false,
		"isDefault":         true,
		"syncEnabled":       false,
		"preventSearch":     false,
	}

	// Sonarr needs extra fields
	if service == "sonarr" {
		payload["activeAnimeProfileId"] = profiles[0].ID
		payload["activeAnimeDirectory"] = roots[0].Path
		payload["enableSeasonFolders"] = true
	}

	_, err = api.Post("seerr", endpoint, payload, nil)
	if err != nil {
		r.errf("Seerr: failed to add %s: %v", service, err)
		return
	}

	fmt.Printf("  %s Seerr → %s configured\n", ui.Ok("✓"), service)
	r.fix()
}

func checkSeerrMediaServer(state *SetupState, r *StepResult) {
	// If Seerr was initialized via Jellyfin auth, media server is already connected
	if state.SeerrInitialized {
		fmt.Printf("  %s Seerr → Jellyfin connected (via init)\n", ui.Ok("✓"))
		r.pass()
		return
	}

	// Check if Jellyfin is configured in Seerr
	var jellySettings map[string]interface{}
	err := api.GetJSON("seerr", "api/v1/settings/jellyfin", nil, &jellySettings)
	if err == nil && jellySettings != nil {
		// Check if it has meaningful config
		if host, ok := jellySettings["hostname"]; ok && host != nil && fmt.Sprintf("%v", host) != "" {
			fmt.Printf("  %s Seerr → media server connected\n", ui.Ok("✓"))
			r.pass()
			return
		}
	}

	fmt.Printf("  %s Complete media server → Seerr at %s\n", ui.Warn("!"),
		ui.CyanText("http://localhost:5055/settings"))
	r.skip()
}

// initSeerr initializes a fresh Seerr instance by authenticating via Jellyfin.
func initSeerr(state *SetupState, svc *ServiceState, r *StepResult) {
	// Need Jellyfin credentials from Phase 4
	if state.JellyfinUser == "" || state.JellyfinPassword == "" {
		if state.AutoMode {
			fmt.Printf("  %s Seerr init skipped — no Jellyfin credentials available\n", ui.Dim("—"))
			return
		}
		// Interactive: prompt for Jellyfin credentials
		var user, pass string
		form := huh.NewForm(huh.NewGroup(
			huh.NewInput().
				Title("Jellyfin admin username (for Seerr login)").
				Value(&user).
				Placeholder("admin"),
			huh.NewInput().
				Title("Jellyfin admin password").
				EchoMode(huh.EchoModePassword).
				Value(&pass),
		))
		if err := form.Run(); err != nil || pass == "" {
			fmt.Printf("  %s Seerr init skipped — no Jellyfin credentials provided\n", ui.Dim("—"))
			return
		}
		if user == "" {
			user = "admin"
		}
		state.JellyfinUser = user
		state.JellyfinPassword = pass
	}

	base := fmt.Sprintf("http://%s:%d", svc.Host, svc.Port)

	// Check if already initialized via public settings endpoint
	c := &http.Client{Timeout: 10 * time.Second}
	pubResp, err := c.Get(base + "/api/v1/settings/public")
	if err != nil {
		fmt.Printf("  %s Seerr init skipped — cannot reach public settings: %v\n", ui.Dim("—"), err)
		return
	}
	pubBody, _ := io.ReadAll(pubResp.Body)
	pubResp.Body.Close()

	var pubSettings struct {
		Initialized bool `json:"initialized"`
	}
	if err := json.Unmarshal(pubBody, &pubSettings); err != nil {
		fmt.Printf("  %s Seerr init skipped — cannot parse public settings\n", ui.Dim("—"))
		return
	}
	if pubSettings.Initialized {
		fmt.Printf("  %s Seerr already initialized — enter API key manually or check Settings\n", ui.Dim("—"))
		return
	}

	// Build Jellyfin internal URL for Seerr to reach Jellyfin
	jellyURL := state.InternalURL("jellyfin")
	parsed, _ := url.Parse(jellyURL)
	jellyHost := parsed.Hostname()
	jellyPort := 8096
	if parsed.Port() != "" {
		fmt.Sscanf(parsed.Port(), "%d", &jellyPort)
	}

	// Step 1: Auth via Jellyfin
	authPayload, _ := json.Marshal(map[string]interface{}{
		"username": state.JellyfinUser,
		"password": state.JellyfinPassword,
		"hostname": jellyHost,
		"port":     jellyPort,
		"useSsl":   false,
	})

	jar, _ := cookiejar.New(nil)
	cc := &http.Client{Timeout: 15 * time.Second, Jar: jar}

	authResp, err := cc.Post(base+"/api/v1/auth/jellyfin", "application/json", bytes.NewReader(authPayload))
	if err != nil {
		fmt.Printf("  %s Seerr Jellyfin auth failed: %v\n", ui.Err("✗"), err)
		return
	}
	io.ReadAll(authResp.Body)
	authResp.Body.Close()

	if authResp.StatusCode != 200 {
		fmt.Printf("  %s Seerr Jellyfin auth returned %d\n", ui.Err("✗"), authResp.StatusCode)
		return
	}

	fmt.Printf("  %s Seerr authenticated via Jellyfin\n", ui.Ok("✓"))

	// Step 2: Initialize
	initResp, err := cc.Post(base+"/api/v1/settings/initialize", "application/json", bytes.NewReader([]byte("{}")))
	if err != nil {
		fmt.Printf("  %s Seerr initialization failed: %v\n", ui.Err("✗"), err)
		return
	}
	initResp.Body.Close()

	// Step 3: Get API key from main settings
	settingsResp, err := cc.Get(base + "/api/v1/settings/main")
	if err != nil {
		fmt.Printf("  %s Seerr: cannot retrieve settings: %v\n", ui.Err("✗"), err)
		return
	}
	settingsBody, _ := io.ReadAll(settingsResp.Body)
	settingsResp.Body.Close()

	var mainSettings struct {
		APIKey string `json:"apiKey"`
	}
	if err := json.Unmarshal(settingsBody, &mainSettings); err != nil || mainSettings.APIKey == "" {
		fmt.Printf("  %s Seerr: could not extract API key from settings\n", ui.Err("✗"))
		return
	}

	svc.APIKey = mainSettings.APIKey
	state.Keys["seerr"] = mainSettings.APIKey
	state.SeerrInitialized = true

	masked := maskKey(mainSettings.APIKey)
	fmt.Printf("  %s Seerr initialized %s\n", ui.Ok("✓"), ui.Dim(masked))
	r.fix()
}
