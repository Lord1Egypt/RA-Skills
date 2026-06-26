package config

import (
	"fmt"
	"net/http"
	"os/exec"
	"strings"
	"sync"
	"time"
)

// RuntimeInfo describes where a service is running.
type RuntimeInfo struct {
	Type  string // "docker", "native", "remote"
	Label string // human-readable, e.g. "docker (radarr)", "remote", "native"
}

// ServiceStatus holds the result of probing a service.
type ServiceStatus struct {
	Up        bool
	Host      string // resolved host where the service was found
	LatencyMs int64
	Runtime   RuntimeInfo
}

// ProbeAll probes all services with ports across all candidate hosts in parallel.
// Updates in-memory config hosts to match where services were actually found.
// Returns status for every service checked.
func ProbeAll() map[string]ServiceStatus {
	names := AllServiceNames()
	dockerContainers := listDockerContainers()
	result := make(map[string]ServiceStatus, len(names))
	var mu sync.Mutex
	var wg sync.WaitGroup

	for _, name := range names {
		def, ok := GetServiceDef(name)
		if !ok || def.Port == 0 {
			continue
		}
		wg.Add(1)
		go func(n string) {
			defer wg.Done()
			ss := probeService(n, dockerContainers)
			mu.Lock()
			result[n] = ss
			// Update in-memory host so subsequent API calls use the resolved host
			if ss.Up && ss.Host != ServiceHost(n) {
				SetServiceHost(n, ss.Host)
			}
			mu.Unlock()
		}(name)
	}
	wg.Wait()
	return result
}

// probeService tries all candidate hosts for a service and returns the first that responds.
func probeService(name string, dockerContainers map[string]bool) ServiceStatus {
	port := ServicePort(name)
	candidates := CandidateHosts(name)

	for _, host := range candidates {
		t0 := time.Now()
		if httpProbe(host, port) {
			ms := time.Since(t0).Milliseconds()
			rt := detectRuntime(name, host, dockerContainers)
			return ServiceStatus{
				Up:        true,
				Host:      host,
				LatencyMs: ms,
				Runtime:   rt,
			}
		}
	}

	// Not reachable at any host — return with configured host and best-guess runtime
	configuredHost := Get().Services[name].Host
	rt := detectRuntime(name, configuredHost, dockerContainers)
	return ServiceStatus{
		Up:      false,
		Host:    configuredHost,
		Runtime: rt,
	}
}

// httpProbe does a quick HTTP GET to check if a service is listening.
func httpProbe(host string, port int) bool {
	c := &http.Client{Timeout: 2 * time.Second}
	resp, err := c.Get(fmt.Sprintf("http://%s:%d/", host, port))
	if err != nil {
		return false
	}
	resp.Body.Close()
	return resp.StatusCode < 500
}

// DetectRuntime determines how a single service is deployed using a fresh Docker check.
func DetectRuntime(name string) RuntimeInfo {
	host := ServiceHost(name)
	return detectRuntime(name, host, listDockerContainers())
}

// DetectAllRuntimes detects runtime info for all services with ports.
func DetectAllRuntimes() map[string]RuntimeInfo {
	names := AllServiceNames()
	result := make(map[string]RuntimeInfo, len(names))
	dockerContainers := listDockerContainers()

	for _, name := range names {
		def, ok := GetServiceDef(name)
		if !ok || def.Port == 0 {
			continue
		}
		host := ServiceHost(name)
		result[name] = detectRuntime(name, host, dockerContainers)
	}
	return result
}

// detectRuntime auto-detects deployment type:
//  1. Non-localhost host → remote
//  2. Docker container running → docker
//  3. Otherwise → native
func detectRuntime(name, host string, dockerContainers map[string]bool) RuntimeInfo {
	// Non-localhost → remote
	if host != "" && host != "localhost" && host != "127.0.0.1" {
		return RuntimeInfo{Type: TypeRemote, Label: "remote"}
	}

	// Check Docker
	container := ContainerName(name)
	svc := Get().Services[name]
	if svc.ContainerName != "" {
		container = svc.ContainerName
	}
	if container != "" && dockerContainers[container] {
		return RuntimeInfo{Type: TypeDocker, Label: fmt.Sprintf("docker (%s)", container)}
	}

	return RuntimeInfo{Type: TypeNative, Label: "native"}
}

// listDockerContainers returns a set of all running Docker container names.
func listDockerContainers() map[string]bool {
	out, err := exec.Command("docker", "ps", "--format", "{{.Names}}").Output()
	if err != nil {
		return make(map[string]bool)
	}
	result := make(map[string]bool)
	for _, line := range strings.Split(strings.TrimSpace(string(out)), "\n") {
		name := strings.TrimSpace(line)
		if name != "" {
			result[name] = true
		}
	}
	return result
}
