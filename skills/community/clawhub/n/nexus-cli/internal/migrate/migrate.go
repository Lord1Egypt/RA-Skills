package migrate

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/maxtechera/admirarr/internal/api"
	"github.com/maxtechera/admirarr/internal/config"
	"github.com/maxtechera/admirarr/internal/keys"
	"github.com/maxtechera/admirarr/internal/ui"
)

// Options configures the migration.
type Options struct {
	ComposeDir string
	DataDir    string
	ConfigDir  string
	DryRun     bool
	Services   []string
	TZ         string
	PUID       string
	PGID       string
}

// Result tracks what the migration did.
type Result struct {
	ComposePath string
	EnvPath     string
	DirsCreated []string
	KeysFound   map[string]string
	Errors      []string
}

// Run executes the full migration.
func Run(opts Options) *Result {
	r := &Result{
		KeysFound: make(map[string]string),
	}

	// Defaults
	if opts.TZ == "" {
		opts.TZ = "UTC"
	}
	if opts.PUID == "" {
		opts.PUID = fmt.Sprintf("%d", os.Getuid())
	}
	if opts.PGID == "" {
		opts.PGID = fmt.Sprintf("%d", os.Getgid())
	}
	if opts.ConfigDir == "" {
		opts.ConfigDir = filepath.Join(opts.ComposeDir, "config")
	}
	if len(opts.Services) == 0 {
		opts.Services = config.ServicesByTier("core")
	}

	// Phase 1: Detect existing services
	fmt.Println(ui.Bold("\n  Phase 1 — Detect Running Services"))
	fmt.Println(ui.Separator())
	detectExisting(r, opts)

	// Phase 2: Harvest API keys
	fmt.Println(ui.Bold("\n  Phase 2 — Harvest API Keys"))
	fmt.Println(ui.Separator())
	harvestKeys(r)

	// Phase 3: Create directory structure
	fmt.Println(ui.Bold("\n  Phase 3 — Directory Structure"))
	fmt.Println(ui.Separator())
	createDirs(r, opts)

	// Phase 4: Generate docker-compose.yml
	fmt.Println(ui.Bold("\n  Phase 4 — Generate Docker Compose"))
	fmt.Println(ui.Separator())
	generateCompose(r, opts)

	// Phase 5: Generate .env
	fmt.Println(ui.Bold("\n  Phase 5 — Generate .env"))
	fmt.Println(ui.Separator())
	generateEnv(r, opts)

	return r
}

func detectExisting(r *Result, opts Options) {
	for _, name := range config.AllRegisteredNames() {
		def, ok := config.GetServiceDef(name)
		if !ok || def.Port == 0 {
			continue
		}
		if api.CheckReachable(name) {
			fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.Ok(fmt.Sprintf("running on :%d", def.Port)))
		} else {
			// Try Docker
			container := config.ContainerName(name)
			out, err := exec.Command("docker", "inspect", "-f", "{{.State.Status}}", container).Output()
			state := strings.TrimSpace(string(out))
			if err == nil && state != "" {
				fmt.Printf("  %s %-15s %s\n", ui.Dim("—"), name, ui.Dim(fmt.Sprintf("container %s", state)))
			} else {
				fmt.Printf("  %s %-15s %s\n", ui.Dim("—"), name, ui.Dim("not found"))
			}
		}
	}
}

func harvestKeys(r *Result) {
	for _, name := range config.AllRegisteredNames() {
		def, ok := config.GetServiceDef(name)
		if !ok || def.KeySource == "none" || !def.HasAPI {
			continue
		}
		key := keys.Get(name)
		if key != "" {
			r.KeysFound[name] = key
			masked := key[:4] + "…" + key[len(key)-4:]
			if len(key) <= 8 {
				masked = "****"
			}
			fmt.Printf("  %s %-15s %s\n", ui.Ok("✓"), name, ui.Dim(masked))
		} else {
			fmt.Printf("  %s %-15s %s\n", ui.Dim("—"), name, ui.Dim("no key found"))
		}
	}
}

func createDirs(r *Result, opts Options) {
	dirs := []string{
		opts.DataDir,
		filepath.Join(opts.DataDir, "torrents"),
		filepath.Join(opts.DataDir, "torrents", "movies"),
		filepath.Join(opts.DataDir, "torrents", "tv"),
		filepath.Join(opts.DataDir, "torrents", "music"),
		filepath.Join(opts.DataDir, "torrents", "books"),
		filepath.Join(opts.DataDir, "usenet"),
		filepath.Join(opts.DataDir, "usenet", "movies"),
		filepath.Join(opts.DataDir, "usenet", "tv"),
		filepath.Join(opts.DataDir, "usenet", "music"),
		filepath.Join(opts.DataDir, "usenet", "books"),
		filepath.Join(opts.DataDir, "media"),
		filepath.Join(opts.DataDir, "media", "movies"),
		filepath.Join(opts.DataDir, "media", "tv"),
		filepath.Join(opts.DataDir, "media", "music"),
		filepath.Join(opts.DataDir, "media", "books"),
		opts.ConfigDir,
	}

	// Add per-service config directories
	for _, name := range opts.Services {
		container := config.ContainerName(name)
		dirs = append(dirs, filepath.Join(opts.ConfigDir, container))
	}

	for _, dir := range dirs {
		if opts.DryRun {
			fmt.Printf("  %s mkdir -p %s\n", ui.Dim("→"), dir)
			r.DirsCreated = append(r.DirsCreated, dir)
			continue
		}
		if err := os.MkdirAll(dir, 0755); err != nil {
			r.Errors = append(r.Errors, fmt.Sprintf("cannot create %s: %v", dir, err))
			fmt.Printf("  %s %s %s\n", ui.Err("✗"), dir, ui.Err(err.Error()))
		} else {
			r.DirsCreated = append(r.DirsCreated, dir)
			fmt.Printf("  %s %s\n", ui.Ok("✓"), dir)
		}
	}
}

func generateCompose(r *Result, opts Options) {
	composePath := filepath.Join(opts.ComposeDir, "docker-compose.yml")
	r.ComposePath = composePath

	content := GenerateCompose(opts.Services, ComposeOpts{
		DataDir:   opts.DataDir,
		ConfigDir: opts.ConfigDir,
		TZ:        opts.TZ,
		PUID:      opts.PUID,
		PGID:      opts.PGID,
	})

	if opts.DryRun {
		fmt.Printf("  %s Would write %s (%d bytes)\n", ui.Dim("→"), composePath, len(content))
		fmt.Printf("\n%s\n", content)
		return
	}

	if err := os.MkdirAll(opts.ComposeDir, 0755); err != nil {
		r.Errors = append(r.Errors, fmt.Sprintf("cannot create compose dir: %v", err))
		fmt.Printf("  %s %s\n", ui.Err("✗"), err.Error())
		return
	}

	// Back up existing file
	if _, err := os.Stat(composePath); err == nil {
		backup := composePath + fmt.Sprintf(".bak.%s", time.Now().Format("20060102-150405"))
		if err := os.Rename(composePath, backup); err == nil {
			fmt.Printf("  %s Backed up existing compose to %s\n", ui.Dim("→"), filepath.Base(backup))
		}
	}

	if err := os.WriteFile(composePath, []byte(content), 0644); err != nil {
		r.Errors = append(r.Errors, fmt.Sprintf("cannot write compose: %v", err))
		fmt.Printf("  %s %s\n", ui.Err("✗"), err.Error())
		return
	}

	fmt.Printf("  %s Written to %s\n", ui.Ok("✓"), composePath)
}

func generateEnv(r *Result, opts Options) {
	envPath := filepath.Join(opts.ComposeDir, ".env")
	r.EnvPath = envPath

	content := GenerateEnvFile(ComposeOpts{
		DataDir:   opts.DataDir,
		ConfigDir: opts.ConfigDir,
		TZ:        opts.TZ,
		PUID:      opts.PUID,
		PGID:      opts.PGID,
	}, envPath)

	if opts.DryRun {
		fmt.Printf("  %s Would write %s\n", ui.Dim("→"), envPath)
		fmt.Printf("\n%s\n", content)
		return
	}

	if err := os.WriteFile(envPath, []byte(content), 0644); err != nil {
		r.Errors = append(r.Errors, fmt.Sprintf("cannot write .env: %v", err))
		fmt.Printf("  %s %s\n", ui.Err("✗"), err.Error())
		return
	}

	fmt.Printf("  %s Written to %s\n", ui.Ok("✓"), envPath)
}
