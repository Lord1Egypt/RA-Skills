package setup

import (
	"bytes"
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/charmbracelet/huh"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/keys"
	"github.com/maxtechera/admirarr/internal/ui"
)

// keyedServices that require API key validation (driven by registry KeySource).
var keyedServices = []string{"jellyfin", "sonarr", "radarr", "prowlarr", "lidarr", "readarr", "whisparr", "seerr", "bazarr", "tautulli"}

// ValidateAPIKeys runs Phase 4: API key discovery and validation.
// Two-pass approach: silent auto-discovery first, manual prompt only if needed.
func ValidateAPIKeys(state *SetupState) StepResult {
	r := StepResult{Name: "API Key Discovery"}

	// Pass 1: Silent auto-discovery
	var needManual []string

	for _, name := range keyedServices {
		svc := state.Services[name]
		if svc == nil || !svc.Reachable {
			fmt.Printf("  %s %-15s %s\n", ui.Dim("—"), name, ui.Dim("skipped (not reachable)"))
			r.skip()
			continue
		}

		// Check if service needs a key
		def, ok := config.GetServiceDef(name)
		if ok && def.KeySource == "none" {
			r.pass()
			continue
		}

		// Try auto-discovery (via docker exec)
		key := keys.Get(name)
		if key != "" && validateKey(name, key, svc) {
			svc.APIKey = key
			state.Keys[name] = key
			masked := maskKey(key)
			fmt.Printf("  %s %-15s %s %s\n", ui.Ok("✓"), name, ui.Ok("found"), ui.Dim(masked))
			r.pass()
			continue
		}

		needManual = append(needManual, name)
	}

	// Pass 2: Interactive prompt for missing keys (only if needed)
	if len(needManual) == 0 {
		return r
	}

	fmt.Printf("\n  %s %d service(s) need manual API key entry:\n", ui.Warn("!"), len(needManual))

	for _, name := range needManual {
		svc := state.Services[name]
		if svc == nil {
			continue
		}

		// Try Jellyfin startup wizard API (works for Docker, native, or remote)
		if name == "jellyfin" {
			if initJellyfin(state, svc, &r) {
				continue
			}
			// initJellyfin returned false — wizard already done or failed.
			// Fall through to manual prompt for API key.
		}

		// Auto mode: skip manual prompts, just report missing
		if state.AutoMode {
			fmt.Printf("  %s %-15s %s\n", ui.Warn("!"), name, ui.Warn("key not found (auto mode)"))
			r.skip()
			continue
		}

		port := config.ServicePort(name)
		host := config.ServiceHost(name)

		var manualKey string
		form := huh.NewForm(
			huh.NewGroup(
				huh.NewInput().
					Title(fmt.Sprintf("API key for %s (find at http://%s:%d → Settings → General)", name, host, port)).
					Value(&manualKey),
			),
		)
		if err := form.Run(); err != nil || manualKey == "" {
			r.errf("%s: no API key available", name)
			continue
		}

		if validateKey(name, manualKey, svc) {
			svc.APIKey = manualKey
			state.Keys[name] = manualKey
			state.ManualKeys[name] = manualKey
			fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.GoldText("key accepted"))
			r.fix()
		} else {
			r.errf("%s: entered key failed validation", name)
		}
	}

	return r
}

func validateKey(service, key string, svc *ServiceState) bool {
	c := &http.Client{Timeout: 5 * time.Second}

	var url string
	switch service {
	case "sonarr", "radarr":
		ver := config.ServiceAPIVer(service)
		url = fmt.Sprintf("http://%s:%d/api/%s/system/status?apikey=%s", svc.Host, svc.Port, ver, key)
	case "prowlarr":
		url = fmt.Sprintf("http://%s:%d/api/v1/system/status?apikey=%s", svc.Host, svc.Port, key)
	case "jellyfin":
		req, err := http.NewRequest("GET", fmt.Sprintf("http://%s:%d/System/Info", svc.Host, svc.Port), nil)
		if err != nil {
			return false
		}
		req.Header.Set("X-Emby-Token", key)
		resp, err := c.Do(req)
		if err != nil {
			return false
		}
		resp.Body.Close()
		return resp.StatusCode == 200
	case "tautulli":
		url = fmt.Sprintf("http://%s:%d/api/v2?apikey=%s&cmd=status", svc.Host, svc.Port, key)
	case "seerr":
		req, err := http.NewRequest("GET", fmt.Sprintf("http://%s:%d/api/v1/status", svc.Host, svc.Port), nil)
		if err != nil {
			return false
		}
		req.Header.Set("X-Api-Key", key)
		resp, err := c.Do(req)
		if err != nil {
			return false
		}
		resp.Body.Close()
		return resp.StatusCode == 200
	case "bazarr":
		req, err := http.NewRequest("GET", fmt.Sprintf("http://%s:%d/api/system/status", svc.Host, svc.Port), nil)
		if err != nil {
			return false
		}
		req.Header.Set("X-API-KEY", key)
		resp, err := c.Do(req)
		if err != nil {
			return false
		}
		resp.Body.Close()
		return resp.StatusCode == 200
	default:
		return key != ""
	}

	resp, err := c.Get(url)
	if err != nil {
		return false
	}
	resp.Body.Close()
	return resp.StatusCode == 200
}

func maskKey(key string) string {
	if len(key) <= 8 {
		return "****"
	}
	return key[:4] + "…" + key[len(key)-4:]
}

// initJellyfin runs the Jellyfin startup wizard via API, creates a user, and
// obtains a permanent API key. Returns true if it handled the key (pass or fix).
func initJellyfin(state *SetupState, svc *ServiceState, r *StepResult) bool {
	c := &http.Client{Timeout: 10 * time.Second}
	base := fmt.Sprintf("http://%s:%d", svc.Host, svc.Port)

	// Check if startup wizard is needed
	pubResp, err := c.Get(base + "/System/Info/Public")
	if err != nil {
		return false
	}
	pubBody, _ := io.ReadAll(pubResp.Body)
	pubResp.Body.Close()

	var pubInfo struct {
		StartupWizardCompleted bool `json:"StartupWizardCompleted"`
	}
	if err := json.Unmarshal(pubBody, &pubInfo); err != nil {
		return false
	}

	if pubInfo.StartupWizardCompleted {
		// Wizard already done — try to recover existing admirarr API key
		// using credentials stored from a previous init
		if state.JellyfinUser != "" && state.JellyfinPassword != "" {
			if key := recoverJellyfinKey(c, base, state.JellyfinUser, state.JellyfinPassword); key != "" {
				svc.APIKey = key
				state.Keys["jellyfin"] = key
				masked := maskKey(key)
				fmt.Printf("  %s %-15s %s %s\n", ui.Ok("✓"), "jellyfin", ui.Ok("recovered"), ui.Dim(masked))
				r.pass()
				return true
			}
		}
		return false
	}

	// Determine username/password
	username := "admin"
	password := ""
	if state.AutoMode {
		b := make([]byte, 16)
		rand.Read(b)
		password = hex.EncodeToString(b)
	} else {
		var user, pass string
		form := huh.NewForm(huh.NewGroup(
			huh.NewInput().
				Title("Jellyfin admin username").
				Value(&user).
				Placeholder("admin"),
			huh.NewInput().
				Title("Jellyfin admin password").
				EchoMode(huh.EchoModePassword).
				Value(&pass),
		))
		if err := form.Run(); err != nil {
			return false
		}
		if user != "" {
			username = user
		}
		if pass == "" {
			return false
		}
		password = pass
	}

	// Step 1: POST /Startup/Configuration
	configPayload, _ := json.Marshal(map[string]string{
		"UICulture":                 "en-US",
		"MetadataCountryCode":       "US",
		"PreferredMetadataLanguage": "en",
	})
	cfgResp, err := c.Post(base+"/Startup/Configuration", "application/json", bytes.NewReader(configPayload))
	if err != nil {
		r.errf("jellyfin: startup config failed: %v", err)
		return false
	}
	cfgResp.Body.Close()
	if cfgResp.StatusCode >= 400 {
		r.errf("jellyfin: startup config returned %d", cfgResp.StatusCode)
		return false
	}

	// Step 2: POST /Startup/User
	userPayload, _ := json.Marshal(map[string]string{
		"Name":     username,
		"Password": password,
	})
	userResp, err := c.Post(base+"/Startup/User", "application/json", bytes.NewReader(userPayload))
	if err != nil {
		r.errf("jellyfin: startup user creation failed: %v", err)
		return false
	}
	userResp.Body.Close()
	if userResp.StatusCode >= 400 {
		r.errf("jellyfin: startup user creation returned %d", userResp.StatusCode)
		return false
	}

	// Step 3: POST /Startup/Complete
	completeResp, err := c.Post(base+"/Startup/Complete", "application/json", bytes.NewReader([]byte("{}")))
	if err != nil {
		r.errf("jellyfin: startup complete failed: %v", err)
		return false
	}
	completeResp.Body.Close()
	if completeResp.StatusCode >= 400 {
		r.errf("jellyfin: startup complete returned %d", completeResp.StatusCode)
		return false
	}

	// Step 4: Authenticate to get a session token
	authPayload, _ := json.Marshal(map[string]string{
		"Username": username,
		"Pw":       password,
	})
	req, _ := http.NewRequest("POST", base+"/Users/AuthenticateByName", bytes.NewReader(authPayload))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Emby-Authorization",
		`MediaBrowser Client="Admirarr", Device="CLI", DeviceId="admirarr-setup", Version="1.0.0"`)
	authHTTPResp, err := c.Do(req)
	if err != nil {
		r.errf("jellyfin: authentication failed: %v", err)
		return false
	}
	authBody, _ := io.ReadAll(authHTTPResp.Body)
	authHTTPResp.Body.Close()

	var authResp struct {
		AccessToken string `json:"AccessToken"`
	}
	if err := json.Unmarshal(authBody, &authResp); err != nil || authResp.AccessToken == "" {
		r.errf("jellyfin: could not get access token")
		return false
	}

	// Step 5: Check for existing admirarr key, create if missing
	apiKey := findOrCreateJellyfinKey(c, base, authResp.AccessToken)
	if apiKey == "" {
		r.errf("jellyfin: API key creation failed")
		return false
	}

	// Store everything
	svc.APIKey = apiKey
	state.Keys["jellyfin"] = apiKey
	state.JellyfinUser = username
	state.JellyfinPassword = password

	masked := maskKey(apiKey)
	fmt.Printf("  %s %-15s %s %s\n", ui.Ok("✓"), "jellyfin", ui.GoldText("initialized"), ui.Dim(masked))
	r.fix()
	return true
}

// findOrCreateJellyfinKey checks for an existing "admirarr" API key and
// creates one if it doesn't exist. Returns the key or empty string on failure.
func findOrCreateJellyfinKey(c *http.Client, base, sessionToken string) string {
	// List existing keys
	req, _ := http.NewRequest("GET", base+"/Auth/Keys", nil)
	req.Header.Set("Authorization", "MediaBrowser Token="+sessionToken)
	resp, err := c.Do(req)
	if err != nil {
		return ""
	}
	body, _ := io.ReadAll(resp.Body)
	resp.Body.Close()

	var keysResp struct {
		Items []struct {
			AccessToken string `json:"AccessToken"`
			AppName     string `json:"AppName"`
		} `json:"Items"`
	}
	if err := json.Unmarshal(body, &keysResp); err != nil {
		return ""
	}

	// Check if admirarr key already exists
	for _, item := range keysResp.Items {
		if item.AppName == "admirarr" {
			return item.AccessToken
		}
	}

	// Create new key
	req, _ = http.NewRequest("POST", base+"/Auth/Keys?app=admirarr", nil)
	req.Header.Set("Authorization", "MediaBrowser Token="+sessionToken)
	resp, err = c.Do(req)
	if err != nil {
		return ""
	}
	resp.Body.Close()

	// Re-fetch to get the new key
	req, _ = http.NewRequest("GET", base+"/Auth/Keys", nil)
	req.Header.Set("Authorization", "MediaBrowser Token="+sessionToken)
	resp, err = c.Do(req)
	if err != nil {
		return ""
	}
	body, _ = io.ReadAll(resp.Body)
	resp.Body.Close()

	if err := json.Unmarshal(body, &keysResp); err != nil {
		return ""
	}
	for _, item := range keysResp.Items {
		if item.AppName == "admirarr" {
			return item.AccessToken
		}
	}
	return ""
}

// recoverJellyfinKey authenticates with known credentials and retrieves
// an existing admirarr API key. Used when wizard is already complete.
func recoverJellyfinKey(c *http.Client, base, username, password string) string {
	authPayload, _ := json.Marshal(map[string]string{
		"Username": username,
		"Pw":       password,
	})
	req, _ := http.NewRequest("POST", base+"/Users/AuthenticateByName", bytes.NewReader(authPayload))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("X-Emby-Authorization",
		`MediaBrowser Client="Admirarr", Device="CLI", DeviceId="admirarr-setup", Version="1.0.0"`)
	resp, err := c.Do(req)
	if err != nil {
		return ""
	}
	body, _ := io.ReadAll(resp.Body)
	resp.Body.Close()

	var authResp struct {
		AccessToken string `json:"AccessToken"`
	}
	if err := json.Unmarshal(body, &authResp); err != nil || authResp.AccessToken == "" {
		return ""
	}

	return findOrCreateJellyfinKey(c, base, authResp.AccessToken)
}
