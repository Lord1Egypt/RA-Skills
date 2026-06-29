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

	"github.com/stozo04/loseit-cli/internal/config"
	"github.com/stozo04/loseit-cli/internal/version"
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
// App and command tree per call keeps tests isolated from sticky global flags.
func NewRootCmd() *cobra.Command {
	app := &App{}

	root := &cobra.Command{
		Use:   "loseit-cli",
		Short: "Read-only Lose It! nutrition extractor (export → per-day JSON)",
		Long: "loseit-cli is a self-contained, read-only nutrition extractor for the Lose It!\n" +
			"data export. It obtains the export (a downloaded ZIP or a cookie fetch), parses\n" +
			"the food log, and emits per-day nutrition as JSON. It never modifies your Lose It\n" +
			"account and does no application storage (no daily log, no sync; the consuming\n" +
			"agent stores nutrition); the only file it writes locally is its 0600 session-token\n" +
			"cache.\n\n" +
			"  days                  parse the export and print per-day nutrition\n" +
			"  login                 log in (email/password) and save a session token\n" +
			"  config show|path      inspect the resolved configuration\n" +
			"  doctor                report config + whether a token/credentials are present\n" +
			"  version               build metadata (also --version)\n" +
			"  completion <shell>    shell completion script",
		// Runtime failures print one error line to stderr ourselves; never dump
		// usage on them, and never let cobra also print the error.
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

	// Root --version: short one-liner, no subcommand needed.
	root.Version = version.Info().String()
	root.SetVersionTemplate("{{.Version}}\n")

	addCommands(app, root)
	return root
}

// addCommands registers every subcommand on root. Each command lives in its own
// file and exposes a newXxxCmd(app) constructor.
func addCommands(app *App, root *cobra.Command) {
	root.AddCommand(
		newDaysCmd(app),
		newLoginCmd(app),
		newDoctorCmd(app),
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
	a.cfg = cfg
	return cfg, nil
}

// newLogger returns a slog text logger writing to w (stderr). Default level is
// Warn; --verbose drops to Debug; LOG_LEVEL overrides either.
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
