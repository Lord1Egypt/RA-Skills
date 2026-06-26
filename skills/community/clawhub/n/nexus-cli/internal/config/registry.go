package config

import "sort"

// ServiceDef defines metadata for a known service.
type ServiceDef struct {
	ContainerName string // docker container name
	Port          int    // default port
	APIVer        string // e.g., "v3", "v1", ""
	HasAPI        bool   // whether it exposes an API we query
	KeySource     string // "config.xml", "settings.json", "config.ini", "none", "manual"
	Tier          string // "core" or "optional"
	Category      string // "media", "download", "indexer", "management", "vpn"
}

// DefaultServices defines all known services and their metadata.
// Core = included in the default Admirarr stack. Optional = user selects during setup.
var DefaultServices = map[string]ServiceDef{
	// ── Media Servers ──
	"jellyfin": {ContainerName: "jellyfin", Port: 8096, HasAPI: true, KeySource: "manual", Tier: "core", Category: "media"},
	"plex":     {ContainerName: "plex", Port: 32400, HasAPI: true, KeySource: "manual", Tier: "optional", Category: "media"},

	// ── *Arr Management (all use config.xml for API keys) ──
	"radarr":   {ContainerName: "radarr", Port: 7878, APIVer: "v3", HasAPI: true, KeySource: "config.xml", Tier: "core", Category: "management"},
	"sonarr":   {ContainerName: "sonarr", Port: 8989, APIVer: "v3", HasAPI: true, KeySource: "config.xml", Tier: "core", Category: "management"},
	"lidarr":   {ContainerName: "lidarr", Port: 8686, APIVer: "v1", HasAPI: true, KeySource: "config.xml", Tier: "optional", Category: "management"},
	"readarr":  {ContainerName: "readarr", Port: 8787, APIVer: "v1", HasAPI: true, KeySource: "config.xml", Tier: "optional", Category: "management"},
	"whisparr": {ContainerName: "whisparr", Port: 6969, APIVer: "v3", HasAPI: true, KeySource: "config.xml", Tier: "optional", Category: "management"},
	"bazarr":   {ContainerName: "bazarr", Port: 6767, HasAPI: true, KeySource: "config.yaml", Tier: "core", Category: "management"},

	// ── Indexer ──
	"prowlarr":     {ContainerName: "prowlarr", Port: 9696, APIVer: "v1", HasAPI: true, KeySource: "config.xml", Tier: "core", Category: "indexer"},
	"flaresolverr": {ContainerName: "flaresolverr", Port: 8191, HasAPI: true, KeySource: "none", Tier: "core", Category: "indexer"},

	// ── Download ──
	"qbittorrent": {ContainerName: "qbittorrent", Port: 8080, HasAPI: true, KeySource: "none", Tier: "core", Category: "download"},
	"sabnzbd":     {ContainerName: "sabnzbd", Port: 8080, HasAPI: true, KeySource: "config.ini", Tier: "optional", Category: "download"},
	"autobrr":     {ContainerName: "autobrr", Port: 7474, HasAPI: true, KeySource: "manual", Tier: "optional", Category: "download"},
	"unpackerr":   {ContainerName: "unpackerr", Port: 0, HasAPI: false, KeySource: "none", Tier: "optional", Category: "download"},

	// ── VPN ──
	"gluetun": {ContainerName: "gluetun", Port: 8888, HasAPI: false, KeySource: "none", Tier: "core", Category: "vpn"},

	// ── Automation & Quality ──
	// Recyclarr is a CLI tool (not a server) — syncs TRaSH Guides quality profiles
	// and custom formats to *Arr services. Port 0 is correct; it runs on-demand.
	"recyclarr":  {ContainerName: "recyclarr", Port: 0, HasAPI: false, KeySource: "none", Tier: "optional", Category: "automation"},
	"profilarr":  {ContainerName: "profilarr", Port: 6868, HasAPI: true, KeySource: "none", Tier: "optional", Category: "automation"},
	"watchtower": {ContainerName: "watchtower", Port: 0, HasAPI: false, KeySource: "none", Tier: "core", Category: "infrastructure"},

	// ── Requests & Management ──
	"seerr":       {ContainerName: "seerr", Port: 5055, HasAPI: true, KeySource: "settings.json", Tier: "core", Category: "requests"},
	"maintainerr": {ContainerName: "maintainerr", Port: 6246, HasAPI: true, KeySource: "none", Tier: "optional", Category: "management"},

	// ── Transcoding ──
	"tdarr": {ContainerName: "tdarr", Port: 8265, HasAPI: true, KeySource: "none", Tier: "optional", Category: "transcoding"},

	// ── Monitoring & Analytics ──
	"tautulli":  {ContainerName: "tautulli", Port: 8181, HasAPI: true, KeySource: "config.ini", Tier: "optional", Category: "monitoring"},
	"jellystat": {ContainerName: "jellystat", Port: 3000, HasAPI: true, KeySource: "none", Tier: "optional", Category: "monitoring"},
	"notifiarr": {ContainerName: "notifiarr", Port: 5454, HasAPI: true, KeySource: "manual", Tier: "optional", Category: "monitoring"},
}

// customServices holds user-registered services at runtime.
var customServices = make(map[string]ServiceDef)

// RegisterService adds a custom service definition at runtime.
func RegisterService(name string, def ServiceDef) {
	customServices[name] = def
}

// GetServiceDef returns the definition for a service, checking custom then default.
func GetServiceDef(name string) (ServiceDef, bool) {
	if def, ok := customServices[name]; ok {
		return def, true
	}
	if def, ok := DefaultServices[name]; ok {
		return def, true
	}
	return ServiceDef{}, false
}

// ServicesByTier returns sorted service names filtered by tier ("core" or "optional").
func ServicesByTier(tier string) []string {
	var names []string
	for name, def := range DefaultServices {
		if def.Tier == tier {
			names = append(names, name)
		}
	}
	for name, def := range customServices {
		if def.Tier == tier {
			names = append(names, name)
		}
	}
	sort.Strings(names)
	return names
}

// ServicesByCategory returns sorted service names filtered by category.
func ServicesByCategory(category string) []string {
	var names []string
	for name, def := range DefaultServices {
		if def.Category == category {
			names = append(names, name)
		}
	}
	for name, def := range customServices {
		if def.Category == category {
			names = append(names, name)
		}
	}
	sort.Strings(names)
	return names
}

// AllRegisteredNames returns all known service names, sorted: core first, then optional, alphabetical within tier.
func AllRegisteredNames() []string {
	core := ServicesByTier("core")
	optional := ServicesByTier("optional")
	return append(core, optional...)
}

// ContainerName returns the Docker container name for a service.
func ContainerName(service string) string {
	if def, ok := GetServiceDef(service); ok {
		return def.ContainerName
	}
	return service
}

// ResetCustomServices clears any runtime-registered services (for testing).
func ResetCustomServices() {
	customServices = make(map[string]ServiceDef)
}
