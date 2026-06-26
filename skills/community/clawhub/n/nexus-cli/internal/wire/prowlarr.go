package wire

import (
	"fmt"
	"strings"

	"github.com/maxtechera/admirarr/internal/arr"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/keys"
)

// CheckSyncTargets checks if Radarr/Sonarr are configured as Prowlarr sync targets.
func CheckSyncTargets() []WireResult {
	client := arr.New("prowlarr")
	apps, err := client.Applications()
	if err != nil {
		return []WireResult{{
			Service: "prowlarr",
			Target:  "sync-targets",
			Action:  "failed",
			Detail:  fmt.Sprintf("cannot query Prowlarr applications: %v", err),
			Err:     err,
		}}
	}

	var results []WireResult
	for _, service := range []string{"radarr", "sonarr"} {
		found := false
		for _, app := range apps {
			if strings.EqualFold(app.Implementation, service) ||
				strings.EqualFold(app.Name, service) {
				found = true
				results = append(results, WireResult{
					Service: "prowlarr",
					Target:  service,
					Action:  "ok",
					Detail:  fmt.Sprintf("sync target exists (sync: %s)", app.SyncLevel),
				})
				break
			}
		}
		if !found {
			results = append(results, WireResult{
				Service: "prowlarr",
				Target:  service,
				Action:  "failed",
				Detail:  "sync target not configured",
			})
		}
	}

	return results
}

// EnsureSyncTarget creates a Prowlarr sync target for a service if missing.
// prowlarrURL, serviceURL: inter-container URLs (e.g. http://prowlarr:9696)
// apiKey: the target service's API key
func EnsureSyncTarget(service, prowlarrURL, serviceURL, apiKey string) WireResult {
	client := arr.New("prowlarr")
	apps, err := client.Applications()
	if err != nil {
		return WireResult{
			Service: "prowlarr",
			Target:  service,
			Action:  "failed",
			Detail:  fmt.Sprintf("cannot query Prowlarr applications: %v", err),
			Err:     err,
		}
	}

	// Check if already exists
	for _, app := range apps {
		if strings.EqualFold(app.Implementation, service) ||
			strings.EqualFold(app.Name, service) {
			return WireResult{
				Service: "prowlarr",
				Target:  service,
				Action:  "ok",
				Detail:  fmt.Sprintf("sync target already exists (sync: %s)", app.SyncLevel),
			}
		}
	}

	// Create sync target
	impl := strings.ToUpper(service[:1]) + service[1:]
	contract := impl + "Settings"

	payload := map[string]interface{}{
		"name":           impl,
		"syncLevel":      "fullSync",
		"implementation": impl,
		"configContract": contract,
		"fields": []map[string]interface{}{
			{"name": "prowlarrUrl", "value": prowlarrURL},
			{"name": "baseUrl", "value": serviceURL},
			{"name": "apiKey", "value": apiKey},
		},
		"tags": []int{},
	}

	_, err = client.Post("api/v1/applications", payload, nil)
	if err != nil {
		return WireResult{
			Service: "prowlarr",
			Target:  service,
			Action:  "failed",
			Detail:  fmt.Sprintf("failed to create sync target: %v", err),
			Err:     err,
		}
	}

	return WireResult{
		Service: "prowlarr",
		Target:  service,
		Action:  "created",
		Detail:  fmt.Sprintf("sync target created (baseUrl=%s)", serviceURL),
	}
}

// CheckFlareProxy checks if FlareSolverr proxy exists in Prowlarr.
func CheckFlareProxy() WireResult {
	client := arr.New("prowlarr")
	proxies, err := client.IndexerProxies()
	if err != nil {
		return WireResult{
			Service: "prowlarr",
			Target:  "flaresolverr",
			Action:  "failed",
			Detail:  fmt.Sprintf("cannot query indexer proxies: %v", err),
			Err:     err,
		}
	}

	for _, p := range proxies {
		if len(p.Tags) > 0 {
			return WireResult{
				Service: "prowlarr",
				Target:  "flaresolverr",
				Action:  "ok",
				Detail:  fmt.Sprintf("proxy exists (tag %d)", p.Tags[0]),
			}
		}
	}

	return WireResult{
		Service: "prowlarr",
		Target:  "flaresolverr",
		Action:  "failed",
		Detail:  "FlareSolverr proxy not configured",
	}
}

// EnsureFlareProxy creates FlareSolverr proxy in Prowlarr if missing.
// flareURL: inter-container URL of FlareSolverr (e.g. http://flaresolverr:8191)
func EnsureFlareProxy(flareURL string) WireResult {
	client := arr.New("prowlarr")

	// Check if proxy already exists
	proxies, err := client.IndexerProxies()
	if err == nil {
		for _, p := range proxies {
			if len(p.Tags) > 0 {
				return WireResult{
					Service: "prowlarr",
					Target:  "flaresolverr",
					Action:  "ok",
					Detail:  fmt.Sprintf("proxy already exists (tag %d)", p.Tags[0]),
				}
			}
		}
	}

	// Create tag
	_, err = client.Post("api/v1/tag", map[string]interface{}{"label": "flaresolverr"}, nil)
	if err != nil {
		return WireResult{
			Service: "prowlarr",
			Target:  "flaresolverr",
			Action:  "failed",
			Detail:  fmt.Sprintf("failed to create FlareSolverr tag: %v", err),
			Err:     err,
		}
	}

	// Fetch tag to get ID
	var tags []struct {
		ID    int    `json:"id"`
		Label string `json:"label"`
	}
	tagID := 0
	if err := client.GetJSON("api/v1/tag", nil, &tags); err == nil {
		for _, t := range tags {
			if t.Label == "flaresolverr" {
				tagID = t.ID
				break
			}
		}
	}

	if tagID == 0 {
		return WireResult{
			Service: "prowlarr",
			Target:  "flaresolverr",
			Action:  "failed",
			Detail:  "created tag but failed to retrieve its ID",
		}
	}

	// Create proxy
	proxyPayload := map[string]interface{}{
		"name":           "FlareSolverr",
		"implementation": "FlareSolverr",
		"configContract": "FlareSolverrSettings",
		"fields": []map[string]interface{}{
			{"name": "host", "value": flareURL},
			{"name": "requestTimeout", "value": 60},
		},
		"tags": []int{tagID},
	}

	_, err = client.Post("api/v1/indexerProxy", proxyPayload, nil)
	if err != nil {
		return WireResult{
			Service: "prowlarr",
			Target:  "flaresolverr",
			Action:  "failed",
			Detail:  fmt.Sprintf("failed to create proxy: %v", err),
			Err:     err,
		}
	}

	return WireResult{
		Service: "prowlarr",
		Target:  "flaresolverr",
		Action:  "created",
		Detail:  fmt.Sprintf("proxy created (tag %d, url=%s)", tagID, flareURL),
	}
}

// GetFlareTag returns the FlareSolverr tag ID from Prowlarr, or 0 if not found.
func GetFlareTag() int {
	client := arr.New("prowlarr")
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

// DefaultSyncTargets creates sync targets for both Radarr and Sonarr using
// config-derived URLs and auto-discovered API keys.
func DefaultSyncTargets() []WireResult {
	prowlarrURL := config.ServiceURL("prowlarr")
	var results []WireResult
	for _, service := range []string{"radarr", "sonarr"} {
		apiKey := keys.Get(service)
		if apiKey == "" {
			results = append(results, WireResult{
				Service: "prowlarr",
				Target:  service,
				Action:  "skipped",
				Detail:  "API key not available",
			})
			continue
		}
		serviceURL := config.ServiceURL(service)
		results = append(results, EnsureSyncTarget(service, prowlarrURL, serviceURL, apiKey))
	}
	return results
}
