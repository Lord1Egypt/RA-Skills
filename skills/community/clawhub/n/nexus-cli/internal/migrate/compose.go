package migrate

import (
	"fmt"
	"os"
	"strings"

	"github.com/maxtechera/admirarr/internal/config"
)

// ComposeOpts configures compose file generation.
type ComposeOpts struct {
	DataDir     string
	ConfigDir   string
	TZ          string
	PUID        string
	PGID        string
	VPNProvider string
	VPNType     string
	VPNCreds    map[string]string
}

// GenerateCompose builds a docker-compose.yml from selected services.
func GenerateCompose(services []string, opts ComposeOpts) string {
	var b strings.Builder

	b.WriteString(composeHeader)

	// Ensure gluetun comes before qbittorrent (dependency order)
	ordered := orderServices(services)

	for _, name := range ordered {
		snippet, ok := serviceSnippets[name]
		if !ok {
			continue
		}
		b.WriteString(snippet)
		b.WriteString("\n")
	}

	// Write .env hint as comment at end
	b.WriteString("# ─── Environment variables (create a .env file alongside this compose) ───\n")
	b.WriteString(fmt.Sprintf("# DATA_DIR=%s\n", opts.DataDir))
	b.WriteString(fmt.Sprintf("# CONFIG_DIR=%s\n", opts.ConfigDir))
	b.WriteString(fmt.Sprintf("# TZ=%s\n", opts.TZ))
	b.WriteString(fmt.Sprintf("# PUID=%s\n", opts.PUID))
	b.WriteString(fmt.Sprintf("# PGID=%s\n", opts.PGID))
	if opts.VPNProvider != "" {
		b.WriteString(fmt.Sprintf("# VPN_PROVIDER=%s\n", opts.VPNProvider))
		b.WriteString(fmt.Sprintf("# VPN_TYPE=%s\n", opts.VPNType))
	}

	return b.String()
}

// GenerateEnvFile creates the .env file content for docker-compose.
// If envPath is non-empty and exists, existing values are preserved as
// defaults — new opts values take precedence.
func GenerateEnvFile(opts ComposeOpts, envPath string) string {
	existing := parseEnvFile(envPath)

	// Build the desired state: opts values win, existing values fill gaps
	env := map[string]string{
		"DATA_DIR":   opts.DataDir,
		"CONFIG_DIR": opts.ConfigDir,
		"TZ":         opts.TZ,
		"PUID":       opts.PUID,
		"PGID":       opts.PGID,
	}
	if opts.VPNProvider != "" {
		env["VPN_PROVIDER"] = opts.VPNProvider
		env["VPN_TYPE"] = opts.VPNType
	}
	// VPN credentials from prompts
	for _, key := range []string{
		"WIREGUARD_PRIVATE_KEY", "WIREGUARD_ADDRESSES",
		"OPENVPN_USER", "OPENVPN_PASSWORD",
		"SERVER_COUNTRIES",
	} {
		if val, ok := opts.VPNCreds[key]; ok && val != "" {
			env[key] = val
		}
	}

	// Merge: existing values fill gaps (don't overwrite what we just set)
	for k, v := range existing {
		if _, set := env[k]; !set {
			env[k] = v
		}
	}

	// Write in stable order
	var b strings.Builder
	orderedKeys := []string{
		"DATA_DIR", "CONFIG_DIR", "TZ", "PUID", "PGID",
		"VPN_PROVIDER", "VPN_TYPE",
		"WIREGUARD_PRIVATE_KEY", "WIREGUARD_ADDRESSES",
		"OPENVPN_USER", "OPENVPN_PASSWORD",
		"SERVER_COUNTRIES",
	}
	written := make(map[string]bool)
	for _, key := range orderedKeys {
		if val, ok := env[key]; ok && val != "" {
			b.WriteString(fmt.Sprintf("%s=%s\n", key, val))
			written[key] = true
		}
	}
	// Append any extra keys from the existing .env (custom user vars)
	for k, v := range env {
		if !written[k] && v != "" {
			b.WriteString(fmt.Sprintf("%s=%s\n", k, v))
		}
	}
	return b.String()
}

// parseEnvFile reads key=value pairs from an existing .env file.
func parseEnvFile(path string) map[string]string {
	result := make(map[string]string)
	if path == "" {
		return result
	}
	data, err := os.ReadFile(path)
	if err != nil {
		return result
	}
	for _, line := range strings.Split(string(data), "\n") {
		line = strings.TrimSpace(line)
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		parts := strings.SplitN(line, "=", 2)
		if len(parts) == 2 {
			result[parts[0]] = parts[1]
		}
	}
	return result
}

// orderServices ensures dependency order (gluetun before qbittorrent).
func orderServices(services []string) []string {
	// Separate into priority tiers
	has := make(map[string]bool)
	for _, s := range services {
		has[s] = true
	}

	// If qbittorrent is selected but gluetun is not, add gluetun
	if has["qbittorrent"] && !has["gluetun"] {
		has["gluetun"] = true
	}

	// Build ordered list: gluetun first (if present), then core, then optional
	var result []string
	if has["gluetun"] {
		result = append(result, "gluetun")
		delete(has, "gluetun")
	}

	// Add remaining in registry order
	for _, name := range config.AllRegisteredNames() {
		if has[name] {
			result = append(result, name)
		}
	}

	return result
}
