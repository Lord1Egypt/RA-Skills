// Package cli wires the cobra command tree. One file per command; this file
// holds the root command, the shared App state, and global flag handling.
package cli

import (
	"fmt"
	"io"
	"log/slog"
	"os"
	"strings"

	"github.com/spf13/cobra"

	"github.com/stozo04/google-health-cli/internal/auth"
	"github.com/stozo04/google-health-cli/internal/config"
	"github.com/stozo04/google-health-cli/internal/version"
)

// App holds process-wide state shared by every command: resolved config, a
// stderr logger, and the values of the global persistent flags. Config is
// resolved lazily so commands that need no config (version, completion) never
// fail on a malformed config.json.
type App struct {
	configPath string // --config
	verbose    bool   // --verbose/-v

	cfg    *config.Config
	logger *slog.Logger
}

// NewRootCmd builds the root command and registers every subcommand. A fresh
// App and command tree per call keeps tests isolated from sticky global flags
// (GOAL.md §14).
func NewRootCmd() *cobra.Command {
	app := &App{}

	root := &cobra.Command{
		Use:   "google-health-cli",
		Short: "Read-only Google Health data extractor (auth + all data types as JSON)",
		Long: "google-health-cli is a self-contained, read-only client for the Google Health\n" +
			"API. It owns OAuth2 login and the v4 REST wire, and emits your health data as\n" +
			"JSON for any agent or script to consume. It does no filtering or derivation —\n" +
			"callers get the data and parse whatever they care about.\n\n" +
			"  types list|describe   discover the data types you can read\n" +
			"  data list <type>      read data points (heart-rate, sleep, steps, exercise, …)\n" +
			"  rollup daily <type>   server-side daily totals (steps, active-minutes, …)\n" +
			"  sessions              parsed exercise sessions (convenience)\n" +
			"  api get <path>        raw read-only GET for anything else (profile, settings, …)",
		// Runtime failures print one error line to stderr ourselves; never dump
		// usage on them, and never let cobra also print the error (GOAL.md §12).
		SilenceUsage:  true,
		SilenceErrors: true,
		// Default action with no subcommand: show help (exit 0).
		RunE: func(cmd *cobra.Command, _ []string) error {
			return cmd.Help()
		},
		// Initialize the stderr logger before any command body runs.
		PersistentPreRunE: func(cmd *cobra.Command, _ []string) error {
			app.logger = newLogger(cmd.ErrOrStderr(), app.verbose)
			return nil
		},
	}

	root.PersistentFlags().StringVar(&app.configPath, "config", "",
		"path to config.json (overrides discovery and "+config.EnvConfig+")")
	root.PersistentFlags().BoolVarP(&app.verbose, "verbose", "v", false,
		"verbose logging to stderr")

	// Root --version: short one-liner, no subcommand needed (GOAL.md §6).
	root.Version = version.Info().String()
	root.SetVersionTemplate("{{.Version}}\n")

	addCommands(app, root)
	return root
}

// addCommands registers every subcommand on root. Each command lives in its own
// file and exposes a newXxxCmd(app) constructor.
func addCommands(app *App, root *cobra.Command) {
	root.AddCommand(
		newDoctorCmd(app),
		newTypesCmd(app),
		newDataCmd(app),
		newRollupCmd(app),
		newSessionsCmd(app),
		newAPICmd(app),
		newAuthCmd(app),
		newConfigCmd(app),
		newVersionCmd(app),
		newCompletionCmd(),
	)
}

// resolveConfig loads configuration once and caches it on the App. Errors are
// tagged with the config exit code so main reports them consistently.
func (a *App) resolveConfig() (*config.Config, error) {
	if a.cfg != nil {
		return a.cfg, nil
	}
	cfg, err := config.Load(config.Options{ConfigPath: a.configPath})
	if err != nil {
		return nil, withCode(ExitConfig, err)
	}

	// When the token cache fell through to the default (non-roaming cache dir),
	// relocate a token left at the previous default (the roaming config dir) so
	// upgrading users keep their session without re-authenticating. Conservative
	// and best-effort (CLI conventions §7); a failure just means a fresh login.
	if cfg.TokenCacheIsDefault {
		if moved, merr := auth.MigrateLegacyToken(cfg.TokenCache, config.LegacyTokenCachePath()); merr != nil {
			a.logger.Warn("could not migrate token cache out of the roaming dir", "err", merr)
		} else if moved {
			a.logger.Warn("relocated token cache to the non-roaming user cache dir", "path", cfg.TokenCache)
		}
	}

	a.cfg = cfg
	return cfg, nil
}

// newLogger returns a slog text logger writing to w (stderr). Default level is
// Warn; --verbose drops to Debug; LOG_LEVEL overrides either (GOAL.md §13).
func newLogger(w io.Writer, verbose bool) *slog.Logger {
	level := slog.LevelWarn
	if verbose {
		level = slog.LevelDebug
	}
	if v, ok := os.LookupEnv("LOG_LEVEL"); ok {
		if parsed, ok := parseLevel(v); ok {
			level = parsed
		}
	}
	h := slog.NewTextHandler(w, &slog.HandlerOptions{Level: level})
	return slog.New(h)
}

func parseLevel(s string) (slog.Level, bool) {
	switch strings.ToLower(strings.TrimSpace(s)) {
	case "debug":
		return slog.LevelDebug, true
	case "info":
		return slog.LevelInfo, true
	case "warn", "warning":
		return slog.LevelWarn, true
	case "error":
		return slog.LevelError, true
	default:
		return slog.LevelWarn, false
	}
}

// fprintln writes a human line to the given writer, ignoring write errors (a
// broken stdout/stderr pipe is not actionable at the CLI layer).
func fprintln(w io.Writer, args ...any) {
	_, _ = fmt.Fprintln(w, args...)
}

// fprintf is the Printf-style sibling of fprintln.
func fprintf(w io.Writer, format string, args ...any) {
	_, _ = fmt.Fprintf(w, format, args...)
}
