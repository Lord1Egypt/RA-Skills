// Package recyclarr provides integration with Recyclarr, the community tool
// that syncs TRaSH Guides quality profiles and custom formats to *Arr services.
//
// Recyclarr is a CLI tool — it runs on-demand, not as a persistent server.
// It can be installed natively, run via Docker, or invoked from a schedule.
//
// Admirarr uses this package to:
//   - Detect how Recyclarr is installed (Docker, native, not found)
//   - Run Recyclarr sync operations
//   - Verify that quality profiles and custom formats are applied
package recyclarr

import (
	"context"
	"fmt"
	"os/exec"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/config"
)

// Runtime describes how Recyclarr is available.
type Runtime struct {
	Method  string // "docker", "native", "none"
	Version string // version string if detected
	Path    string // binary path (native) or container name (docker)
}

// Detect finds how Recyclarr is installed.
func Detect() Runtime {
	// 1. Check native install
	if path, err := exec.LookPath("recyclarr"); err == nil {
		ver := nativeVersion(path)
		return Runtime{Method: "native", Version: ver, Path: path}
	}

	// 2. Check Docker container
	container := config.ContainerName("recyclarr")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	out, err := exec.CommandContext(ctx, "docker", "inspect", "-f", "{{.State.Status}}", container).Output()
	if err == nil {
		state := strings.TrimSpace(string(out))
		ver := dockerVersion(container)
		if state != "" {
			return Runtime{Method: "docker", Version: ver, Path: container}
		}
	}

	return Runtime{Method: "none"}
}

// Sync runs Recyclarr sync for the specified instance (or all if empty).
// Returns the combined stdout+stderr output and any error.
func Sync(rt Runtime, instance string) (string, error) {
	args := buildArgs(rt, "sync")
	if instance != "" {
		args = append(args, instance)
	}

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()

	cmd := exec.CommandContext(ctx, args[0], args[1:]...)
	out, err := cmd.CombinedOutput()
	return string(out), err
}

// ListInstances returns configured Recyclarr instances.
func ListInstances(rt Runtime) ([]string, error) {
	args := buildArgs(rt, "list", "instances")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	out, err := exec.CommandContext(ctx, args[0], args[1:]...).Output()
	if err != nil {
		return nil, err
	}

	var instances []string
	for _, line := range strings.Split(strings.TrimSpace(string(out)), "\n") {
		line = strings.TrimSpace(line)
		if line != "" && !strings.HasPrefix(line, "=") && !strings.Contains(line, "Instance") {
			instances = append(instances, line)
		}
	}
	return instances, nil
}

// buildArgs constructs the command + args based on runtime method.
func buildArgs(rt Runtime, subcmd ...string) []string {
	switch rt.Method {
	case "docker":
		// docker exec recyclarr recyclarr <subcmd>
		args := []string{"docker", "exec", rt.Path, "recyclarr"}
		return append(args, subcmd...)
	case "native":
		return append([]string{rt.Path}, subcmd...)
	default:
		return append([]string{"recyclarr"}, subcmd...)
	}
}

func nativeVersion(path string) string {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	out, err := exec.CommandContext(ctx, path, "--version").Output()
	if err != nil {
		return ""
	}
	return strings.TrimSpace(string(out))
}

func dockerVersion(container string) string {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	out, err := exec.CommandContext(ctx, "docker", "exec", container, "recyclarr", "--version").Output()
	if err != nil {
		return ""
	}
	return strings.TrimSpace(string(out))
}

// VerifyResult holds the result of verifying Recyclarr's applied config.
type VerifyResult struct {
	Service          string
	QualityProfiles  int
	CustomFormats    int
	ProfilesApplied  bool
	FormatsApplied   bool
	Issues           []string
}

func (v VerifyResult) String() string {
	status := "OK"
	if len(v.Issues) > 0 {
		status = fmt.Sprintf("%d issues", len(v.Issues))
	}
	return fmt.Sprintf("[%s] %d profiles, %d custom formats — %s", v.Service, v.QualityProfiles, v.CustomFormats, status)
}
