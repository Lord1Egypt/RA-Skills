package config

import (
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/spf13/viper"
)

// Service deployment types.
const (
	TypeDocker = "docker" // container on localhost
	TypeNative = "native" // local process on same machine
	TypeRemote = "remote" // service on another IP (e.g. Windows host via WSL)
)

// ServiceConfig holds the configuration for a single service.
type ServiceConfig struct {
	Host          string `mapstructure:"host"`
	Port          int    `mapstructure:"port"`
	APIVer        string `mapstructure:"api_ver"`
	ContainerName string `mapstructure:"container_name"`
	LocalhostOnly bool   `mapstructure:"localhost_only"` // binds to localhost on remote host, needs WSL gateway
}

// IndexerConfig holds declarative config for a single Prowlarr indexer.
type IndexerConfig struct {
	Enabled     *bool                  `mapstructure:"enabled"`
	Flare       bool                   `mapstructure:"flare"`
	BaseURL     string                 `mapstructure:"base_url"`
	ExtraFields map[string]interface{} `mapstructure:"extra_fields"`
}

// IsEnabled returns whether the indexer is enabled (defaults to true).
func (ic IndexerConfig) IsEnabled() bool {
	if ic.Enabled == nil {
		return true
	}
	return *ic.Enabled
}

// Config holds the full application configuration.
type Config struct {
	Host           string                   `mapstructure:"host"`           // global host IP for remote services
	WSLGateway     string                   `mapstructure:"wsl_gateway"`    // WSL gateway for localhost_only services
	DataPath       string                   `mapstructure:"data_path"`
	ComposePath    string                   `mapstructure:"compose_path"`
	Services       map[string]ServiceConfig `mapstructure:"services"`
	Keys           map[string]string        `mapstructure:"keys"`
	QualityProfile string                   `mapstructure:"quality_profile"`
	Indexers       map[string]IndexerConfig `mapstructure:"indexers"`
}

var cfg *Config

// Load initializes the configuration from file and defaults.
func Load() {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")

	configDir := filepath.Join(os.Getenv("HOME"), ".config", "admirarr")
	viper.AddConfigPath(configDir)
	viper.AddConfigPath(".")

	// Set defaults
	viper.SetDefault("data_path", "/data")
	viper.SetDefault("compose_path", filepath.Join(os.Getenv("HOME"), "docker", "docker-compose.yml"))

	_ = viper.ReadInConfig() // OK if missing

	cfg = &Config{
		Host:           viper.GetString("host"),
		WSLGateway:     viper.GetString("wsl_gateway"),
		DataPath:       viper.GetString("data_path"),
		ComposePath:    viper.GetString("compose_path"),
		Services:       make(map[string]ServiceConfig),
		Keys:           make(map[string]string),
		QualityProfile: viper.GetString("quality_profile"),
		Indexers:       make(map[string]IndexerConfig),
	}

	// Load services from config (overrides)
	if viper.IsSet("services") {
		svcMap := viper.GetStringMap("services")
		for name := range svcMap {
			var svc ServiceConfig
			sub := viper.Sub("services." + name)
			if sub != nil {
				_ = sub.Unmarshal(&svc)
			}
			cfg.Services[name] = svc
		}
	}

	// Resolve WSL gateway if set to "auto"
	if cfg.WSLGateway == "auto" {
		cfg.WSLGateway = detectWSLGateway()
	}

	// Ensure all default services exist with registry defaults
	for name, def := range DefaultServices {
		if _, exists := cfg.Services[name]; !exists {
			cfg.Services[name] = ServiceConfig{
				Host:          "localhost",
				Port:          def.Port,
				APIVer:        def.APIVer,
				ContainerName: def.ContainerName,
			}
		} else {
			// Fill in missing fields from defaults
			svc := cfg.Services[name]
			if svc.Host == "" {
				svc.Host = resolveHost()
			}
			if svc.Port == 0 {
				svc.Port = def.Port
			}
			if svc.APIVer == "" {
				svc.APIVer = def.APIVer
			}
			if svc.ContainerName == "" {
				svc.ContainerName = def.ContainerName
			}
			cfg.Services[name] = svc
		}
	}

	// Load manual keys
	if viper.IsSet("keys") {
		keyMap := viper.GetStringMapString("keys")
		for k, v := range keyMap {
			if v != "" {
				cfg.Keys[k] = v
			}
		}
	}

	// Load indexer config
	if viper.IsSet("indexers") {
		idxMap := viper.GetStringMap("indexers")
		for name := range idxMap {
			var ic IndexerConfig
			sub := viper.Sub("indexers." + name)
			if sub != nil {
				_ = sub.Unmarshal(&ic)
			}
			cfg.Indexers[name] = ic
		}
	}
}

// Get returns the current configuration.
func Get() *Config {
	if cfg == nil {
		Load()
	}
	return cfg
}

// SetGlobalHost updates the global host IP at runtime.
func SetGlobalHost(host string) {
	Get().Host = host
}

// ServiceURL returns the base URL for a service.
func ServiceURL(name string) string {
	svc := Get().Services[name]
	return fmt.Sprintf("http://%s:%d", svc.Host, svc.Port)
}

// ServiceHost returns the host for a service.
func ServiceHost(name string) string {
	return Get().Services[name].Host
}

// ServicePort returns the port for a service.
func ServicePort(name string) int {
	return Get().Services[name].Port
}

// ServiceAPIVer returns the API version for a service.
func ServiceAPIVer(name string) string {
	return Get().Services[name].APIVer
}

// DataPath returns the configured data path (Docker volume root).
func DataPath() string {
	return Get().DataPath
}

// ManualKey returns a manually configured API key, or empty string.
func ManualKey(service string) string {
	return Get().Keys[service]
}

// AllServiceNames returns all service names derived from the registry.
// Core services first (sorted), then optional (sorted).
func AllServiceNames() []string {
	return AllRegisteredNames()
}

// QualityProfile returns the configured quality profile name.
func QualityProfile() string {
	return Get().QualityProfile
}

// GetIndexers returns the declarative indexer config.
func GetIndexers() map[string]IndexerConfig {
	return Get().Indexers
}

// Host returns the global host for the stack (from config, or "localhost").
func Host() string {
	h := Get().Host
	if h == "" {
		return "localhost"
	}
	return h
}

// resolveHost returns "localhost" as the default host for a service.
func resolveHost() string {
	return "localhost"
}

// SetServiceHost updates a service's host in memory (does not write to disk).
func SetServiceHost(name, host string) {
	c := Get()
	svc := c.Services[name]
	svc.Host = host
	c.Services[name] = svc
}

// CandidateHosts returns deduplicated hosts to probe for a service, in priority order.
// Order: configured host, global host, WSL gateway, localhost.
func CandidateHosts(name string) []string {
	c := Get()
	svc := c.Services[name]
	seen := make(map[string]bool)
	var hosts []string

	add := func(h string) {
		if h != "" && !seen[h] {
			seen[h] = true
			hosts = append(hosts, h)
		}
	}

	add(svc.Host)      // configured host first
	add(c.Host)        // global host
	add(c.WSLGateway)  // WSL gateway
	add("localhost")   // always try localhost
	add("127.0.0.1")   // in case localhost doesn't resolve

	return hosts
}

// detectWSLGateway reads the default gateway from /etc/resolv.conf (WSL2).
func detectWSLGateway() string {
	data, err := os.ReadFile("/etc/resolv.conf")
	if err != nil {
		return ""
	}
	for _, line := range strings.Split(string(data), "\n") {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(line, "nameserver ") {
			return strings.TrimSpace(strings.TrimPrefix(line, "nameserver "))
		}
	}
	return ""
}

// IsConfigured returns true if a service is explicitly listed in the user's config file.
// Services only in the registry (not in config) are discovered but not required.
func IsConfigured(name string) bool {
	return viper.IsSet("services." + name)
}

// ConfiguredServiceNames returns only services explicitly listed in the config file.
func ConfiguredServiceNames() []string {
	var names []string
	if !viper.IsSet("services") {
		return names
	}
	svcMap := viper.GetStringMap("services")
	for name := range svcMap {
		names = append(names, name)
	}
	return names
}

// MediaPathWSL returns the media/data path (Docker volume root).
func MediaPathWSL() string {
	return Get().DataPath
}

// MediaPathWin returns the media/data path (same as WSL in Docker setups).
func MediaPathWin() string {
	return Get().DataPath
}
