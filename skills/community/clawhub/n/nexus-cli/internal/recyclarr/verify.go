package recyclarr

import (
	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/arr"
)

// Verify checks that quality profiles and custom formats are configured
// in the target *Arr services. This validates the end result of Recyclarr
// without requiring Recyclarr to be installed — it queries the APIs directly.
func Verify(services ...string) []VerifyResult {
	if len(services) == 0 {
		services = []string{"radarr", "sonarr"}
	}

	var results []VerifyResult
	for _, svc := range services {
		results = append(results, verifyService(svc))
	}
	return results
}

func verifyService(service string) VerifyResult {
	result := VerifyResult{Service: service}

	if !api.CheckReachable(service) {
		result.Issues = append(result.Issues, "service unreachable")
		return result
	}

	client := arr.New(service)

	// Check quality profiles
	profiles, err := client.QualityProfiles()
	if err != nil {
		result.Issues = append(result.Issues, "cannot query quality profiles: "+err.Error())
	} else {
		result.QualityProfiles = len(profiles)
		if len(profiles) == 0 {
			result.Issues = append(result.Issues, "no quality profiles configured")
		} else {
			result.ProfilesApplied = true
		}
	}

	// Check custom formats
	formats, err := client.CustomFormats()
	if err != nil {
		result.Issues = append(result.Issues, "cannot query custom formats: "+err.Error())
	} else {
		result.CustomFormats = len(formats)
		if len(formats) > 0 {
			result.FormatsApplied = true
		}
		// Having 0 custom formats isn't necessarily an error — some users don't use them.
		// But if Recyclarr is supposed to be managing them, it might indicate a problem.
	}

	return result
}
