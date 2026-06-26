package skills

import (
	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
)

// HealthResult represents a health check result for a service.
type HealthResult struct {
	Service string `json:"service"`
	Type    string `json:"type"`
	Message string `json:"message"`
}

// CheckHealth fetches health from Jellyfin + *Arr services.
func CheckHealth() ([]HealthResult, error) {
	var results []HealthResult

	// Jellyfin health check
	if api.CheckReachable("jellyfin") {
		results = append(results, HealthResult{Service: "jellyfin", Type: "ok", Message: "Healthy"})
	} else {
		results = append(results, HealthResult{Service: "jellyfin", Type: "error", Message: "unreachable"})
	}

	// *Arr health checks
	for _, svc := range []string{"radarr", "sonarr", "prowlarr"} {
		items, err := arr.New(svc).Health()
		if err != nil || len(items) == 0 {
			results = append(results, HealthResult{Service: svc, Type: "ok", Message: "Healthy"})
			continue
		}
		for _, item := range items {
			results = append(results, HealthResult{Service: svc, Type: item.Type, Message: item.Message})
		}
	}

	return results, nil
}
