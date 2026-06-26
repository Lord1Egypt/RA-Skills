// Package deploy provides on-demand Docker container deployment for individual
// services. Used by commands that need a tool (e.g. Recyclarr) and can deploy
// it automatically when missing.
package deploy

import (
	"context"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/migrate"
)

// Result describes the outcome of a deploy operation.
type Result struct {
	Deployed  bool
	Container string
	Error     error
}

// Service deploys a single service as a Docker container. It generates a
// minimal compose file, runs `docker compose up -d`, and waits for the
// container to start.
//
// composePath is the directory where docker-compose files live. If empty,
// it uses the configured compose_path or ~/docker.
func Service(service string) Result {
	container := config.ContainerName(service)

	// Check Docker is available
	if err := exec.Command("docker", "version").Run(); err != nil {
		return Result{Error: fmt.Errorf("Docker not available: %v", err)}
	}

	// Check if container already exists
	out, err := exec.CommandContext(
		contextTimeout(10*time.Second),
		"docker", "inspect", "-f", "{{.State.Status}}", container,
	).Output()
	if err == nil {
		state := strings.TrimSpace(string(out))
		if state == "running" {
			return Result{Deployed: true, Container: container}
		}
		// Container exists but not running — start it
		if state != "" {
			if err := exec.Command("docker", "start", container).Run(); err != nil {
				return Result{Error: fmt.Errorf("container exists but failed to start: %v", err)}
			}
			return Result{Deployed: true, Container: container}
		}
	}

	// Generate a standalone compose snippet for this service
	cfg := config.Get()
	opts := migrate.ComposeOpts{
		DataDir:   cfg.DataPath,
		ConfigDir: filepath.Join(filepath.Dir(cfg.ComposePath), "config"),
		TZ:        "UTC",
		PUID:      fmt.Sprintf("%d", os.Getuid()),
		PGID:      fmt.Sprintf("%d", os.Getgid()),
	}

	composeDir := filepath.Dir(cfg.ComposePath)
	if composeDir == "." || composeDir == "" {
		home, _ := os.UserHomeDir()
		composeDir = filepath.Join(home, "docker")
	}

	// Ensure config dir exists for this service
	configDir := filepath.Join(composeDir, "config", container)
	if err := os.MkdirAll(configDir, 0755); err != nil {
		// Parent may be root-owned (created by Docker) — use a Docker container to create the dir
		mkdirCmd := exec.Command("docker", "run", "--rm",
			"-v", filepath.Dir(configDir)+":/mnt",
			"alpine", "sh", "-c",
			fmt.Sprintf("mkdir -p /mnt/%s && chown -R %d:%d /mnt/%s", container, os.Getuid(), os.Getgid(), container))
		if mkdirErr := mkdirCmd.Run(); mkdirErr != nil {
			return Result{Error: fmt.Errorf("cannot create config dir %s: %v", configDir, err)}
		}
	}

	// Generate compose for just this one service
	content := migrate.GenerateCompose([]string{service}, opts)

	// Write to a temp compose file to avoid clobbering the main one
	tmpCompose := filepath.Join(composeDir, fmt.Sprintf("docker-compose.%s.yml", service))
	if err := os.MkdirAll(composeDir, 0755); err != nil {
		return Result{Error: fmt.Errorf("cannot create compose dir: %v", err)}
	}

	// Also ensure .env exists
	envPath := filepath.Join(composeDir, ".env")
	if _, err := os.Stat(envPath); os.IsNotExist(err) {
		envContent := migrate.GenerateEnvFile(opts, envPath)
		_ = os.WriteFile(envPath, []byte(envContent), 0644)
	}

	if err := os.WriteFile(tmpCompose, []byte(content), 0644); err != nil {
		return Result{Error: fmt.Errorf("cannot write compose file: %v", err)}
	}
	defer os.Remove(tmpCompose)

	// Docker compose up
	cmd := exec.CommandContext(
		contextTimeout(2*time.Minute),
		"docker", "compose", "-f", tmpCompose, "up", "-d",
	)
	cmd.Dir = composeDir
	out, err = cmd.CombinedOutput()
	if err != nil {
		// Try V1
		cmd2 := exec.CommandContext(
			contextTimeout(2*time.Minute),
			"docker-compose", "-f", tmpCompose, "up", "-d",
		)
		cmd2.Dir = composeDir
		out2, err2 := cmd2.CombinedOutput()
		if err2 != nil {
			return Result{Error: fmt.Errorf("docker compose up failed: %s\n%s",
				strings.TrimSpace(string(out)), strings.TrimSpace(string(out2)))}
		}
	}

	// Wait for container to be running (30s max)
	deadline := time.Now().Add(30 * time.Second)
	for time.Now().Before(deadline) {
		out, err := exec.Command("docker", "inspect", "-f", "{{.State.Status}}", container).Output()
		if err == nil && strings.TrimSpace(string(out)) == "running" {
			return Result{Deployed: true, Container: container}
		}
		time.Sleep(2 * time.Second)
	}

	return Result{Error: fmt.Errorf("container %s did not start within 30s", container)}
}

func contextTimeout(d time.Duration) context.Context {
	ctx, _ := context.WithTimeout(context.Background(), d)
	return ctx
}
