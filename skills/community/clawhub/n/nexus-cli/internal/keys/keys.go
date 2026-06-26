package keys

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"sync"
	"time"

	"github.com/maxtechera/admirarr/internal/config"
)

var (
	cache   = make(map[string]string)
	cacheMu sync.Mutex

	xmlKeyRe = regexp.MustCompile(`<ApiKey>([^<]+)</ApiKey>`)
)

// Get returns the API key for a service, using cache and auto-discovery.
func Get(service string) string {
	if key := config.ManualKey(service); key != "" {
		return key
	}

	cacheMu.Lock()
	if key, ok := cache[service]; ok {
		cacheMu.Unlock()
		return key
	}
	cacheMu.Unlock()

	key := discover(service)
	if key != "" {
		cacheMu.Lock()
		cache[service] = key
		cacheMu.Unlock()
	}
	return key
}

func discover(service string) string {
	def, ok := config.GetServiceDef(service)
	if !ok {
		return ""
	}

	rt := config.DetectRuntime(service)

	switch rt.Type {
	case config.TypeDocker:
		// Read config from inside containers
		switch def.KeySource {
		case "config.xml":
			return readConfigXML(config.ContainerName(service))
		case "settings.json":
			return readSeerrKey(config.ContainerName(service))
		case "config.ini":
			return readConfigINI(config.ContainerName(service), service)
		case "config.yaml":
			return readConfigYAML(config.ContainerName(service), service)
		default:
			return ""
		}
	default:
		// Native or remote: try native filesystem paths (works on WSL where
		// the remote host is the Windows machine with /mnt/c accessible).
		return discoverNative(service, def)
	}
}

// discoverNative reads API keys from native service config files.
// Checks platform-appropriate paths: Linux ~/.config, macOS ~/Library,
// WSL /mnt/c/Users/.../AppData.
func discoverNative(service string, def config.ServiceDef) string {
	switch def.KeySource {
	case "config.xml":
		return readNativeConfigXML(service)
	case "config.ini":
		return readNativeConfigINI(service)
	case "config.yaml":
		return readNativeConfigYAML(service)
	default:
		return ""
	}
}

// readNativeConfigXML reads config.xml from platform-appropriate paths.
func readNativeConfigXML(service string) string {
	paths := nativeConfigPaths(service, "config.xml")
	for _, p := range paths {
		data, err := os.ReadFile(p)
		if err != nil {
			continue
		}
		m := xmlKeyRe.FindSubmatch(data)
		if m != nil {
			return string(m[1])
		}
	}
	return ""
}

// readNativeConfigINI reads an INI-style config from platform-appropriate paths.
func readNativeConfigINI(service string) string {
	var filename string
	switch service {
	case "bazarr":
		filename = "config/config.ini"
	case "sabnzbd":
		filename = "sabnzbd.ini"
	default:
		filename = "config.ini"
	}
	paths := nativeConfigPaths(service, filename)

	for _, p := range paths {
		data, err := os.ReadFile(p)
		if err != nil {
			continue
		}
		for _, line := range strings.Split(string(data), "\n") {
			line = strings.TrimSpace(line)
			if strings.HasPrefix(line, "api_key") || strings.HasPrefix(line, "apikey") {
				parts := strings.SplitN(line, "=", 2)
				if len(parts) == 2 {
					key := strings.TrimSpace(parts[1])
					if key != "" {
						return key
					}
				}
			}
		}
	}
	return ""
}

// nativeConfigPaths returns candidate config file paths for a service
// on the current platform.
func nativeConfigPaths(service, filename string) []string {
	title := strings.Title(service) //nolint:staticcheck
	home := os.Getenv("HOME")
	var paths []string

	// WSL: check Windows paths via /mnt/c
	if isWSL() {
		paths = append(paths, wslConfigPaths(title, filename)...)
	}

	switch runtime.GOOS {
	case "darwin":
		// macOS: ~/Library/Application Support/{Service}/
		paths = append(paths,
			filepath.Join(home, "Library", "Application Support", title, filename),
		)
	default:
		// Linux: ~/.config/{service}/ and /var/lib/{service}/
		paths = append(paths,
			filepath.Join(home, ".config", title, filename),
			filepath.Join(home, ".config", strings.ToLower(service), filename),
			filepath.Join("/var/lib", strings.ToLower(service), filename),
		)
	}

	return paths
}

// wslConfigPaths returns candidate paths for a service's config file
// on Windows, accessible via WSL mount points.
func wslConfigPaths(serviceTitle, filename string) []string {
	var paths []string

	entries, _ := os.ReadDir("/mnt/c/Users")
	for _, e := range entries {
		if !e.IsDir() {
			continue
		}
		name := e.Name()
		if name == "Public" || name == "Default" || name == "Default User" || name == "All Users" {
			continue
		}
		paths = append(paths,
			fmt.Sprintf("/mnt/c/Users/%s/AppData/Roaming/%s/%s", name, serviceTitle, filename),
			fmt.Sprintf("/mnt/c/Users/%s/AppData/Local/%s/%s", name, serviceTitle, filename),
		)
	}

	paths = append(paths,
		fmt.Sprintf("/mnt/c/ProgramData/%s/%s", serviceTitle, filename),
	)

	return paths
}

// isWSL returns true if running inside Windows Subsystem for Linux.
func isWSL() bool {
	_, err := os.Stat("/mnt/c/Windows")
	return err == nil
}

// readConfigXML reads an API key from config.xml inside a Docker container.
func readConfigXML(container string) string {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	out, err := exec.CommandContext(ctx, "docker", "exec", container, "cat", "/config/config.xml").Output()
	if err != nil {
		return ""
	}
	m := xmlKeyRe.FindSubmatch(out)
	if m == nil {
		return ""
	}
	return string(m[1])
}

// readSeerrKey reads the API key from Overseerr's settings.json inside Docker.
func readSeerrKey(container string) string {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	out, err := exec.CommandContext(ctx, "docker", "exec", container, "cat", "/app/config/settings.json").Output()
	if err != nil {
		return ""
	}
	var result struct {
		Main struct {
			APIKey string `json:"apiKey"`
		} `json:"main"`
	}
	if err := json.Unmarshal(out, &result); err != nil {
		return ""
	}
	return result.Main.APIKey
}

// readConfigINI reads an API key from an INI-style config inside Docker.
func readConfigINI(container, service string) string {
	configPath := "/config/config.ini"
	switch service {
	case "bazarr":
		configPath = "/config/config/config.ini"
	case "sabnzbd":
		configPath = "/config/sabnzbd.ini"
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	out, err := exec.CommandContext(ctx, "docker", "exec", container, "cat", configPath).Output()
	if err != nil {
		return ""
	}

	for _, line := range strings.Split(string(out), "\n") {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(line, "api_key") || strings.HasPrefix(line, "apikey") {
			parts := strings.SplitN(line, "=", 2)
			if len(parts) == 2 {
				key := strings.TrimSpace(parts[1])
				if key != "" {
					return key
				}
			}
		}
	}
	return ""
}

// readConfigYAML reads an API key from a YAML config inside a Docker container.
// Used by bazarr which stores its key at auth.apikey in config/config.yaml.
func readConfigYAML(container, service string) string {
	configPath := "/config/config/config.yaml"
	switch service {
	case "bazarr":
		configPath = "/config/config/config.yaml"
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	out, err := exec.CommandContext(ctx, "docker", "exec", container, "cat", configPath).Output()
	if err != nil {
		return ""
	}

	return parseYAMLApiKey(string(out))
}

// readNativeConfigYAML reads an API key from a YAML config on the native filesystem.
func readNativeConfigYAML(service string) string {
	var filename string
	switch service {
	case "bazarr":
		filename = "config/config.yaml"
	default:
		filename = "config.yaml"
	}
	paths := nativeConfigPaths(service, filename)
	for _, p := range paths {
		data, err := os.ReadFile(p)
		if err != nil {
			continue
		}
		if key := parseYAMLApiKey(string(data)); key != "" {
			return key
		}
	}
	return ""
}

// parseYAMLApiKey extracts an API key from YAML content.
// Handles bazarr format: auth:\n  apikey: <key>
// Also handles flat format: apikey: <key> or api_key: <key>
func parseYAMLApiKey(content string) string {
	inAuth := false
	for _, line := range strings.Split(content, "\n") {
		trimmed := strings.TrimSpace(line)

		// Check for auth: section
		if trimmed == "auth:" {
			inAuth = true
			continue
		}

		// If we're in the auth section, look for apikey
		if inAuth && strings.HasPrefix(trimmed, "apikey:") {
			parts := strings.SplitN(trimmed, ":", 2)
			if len(parts) == 2 {
				return strings.TrimSpace(parts[1])
			}
		}

		// If we hit a non-indented line, we've left the auth section
		if inAuth && len(line) > 0 && line[0] != ' ' && line[0] != '\t' {
			inAuth = false
		}

		// Also check flat format
		if strings.HasPrefix(trimmed, "api_key:") || strings.HasPrefix(trimmed, "apikey:") {
			parts := strings.SplitN(trimmed, ":", 2)
			if len(parts) == 2 {
				key := strings.TrimSpace(parts[1])
				if key != "" {
					return key
				}
			}
		}
	}
	return ""
}
