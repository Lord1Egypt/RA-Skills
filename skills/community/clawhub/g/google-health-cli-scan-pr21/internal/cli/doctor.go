package cli

import (
	"strings"

	"github.com/spf13/cobra"

	"github.com/stozo04/google-health-cli/internal/auth"
	"github.com/stozo04/google-health-cli/internal/config"
	"github.com/stozo04/google-health-cli/internal/version"
)

// doctorReport is the doctor JSON shape (GOAL.md §10). The old Python doctor was
// a passthrough of `ghealth doctor`; this is our own shape but keeps the
// tokenValid boolean so existing checks keep working. Existing keys keep their
// order and meaning; configFound/clientIdLoaded were added (issue #6) so doctor
// can diagnose a missing/credential-less config instead of staying silent.
type doctorReport struct {
	TokenValid     bool     `json:"tokenValid"`
	BaseURL        string   `json:"baseURL"`
	User           string   `json:"user"`
	TokenPath      string   `json:"tokenPath"`
	ConfigPath     string   `json:"configPath"`
	ConfigFound    bool     `json:"configFound"`
	ClientIDLoaded bool     `json:"clientIdLoaded"`
	Scopes         []string `json:"scopes"`
	Version        string   `json:"version"`
}

// newDoctorCmd implements `doctor` (GOAL.md §6, §10): print config + token
// validity as indent-2 JSON; exit 2 (with a stderr hint) when not authenticated.
//
// Privacy: the JSON reports local environment metadata — token-cache and config
// paths, the configured account (user), and the base URL. These are intentionally
// surfaced because diagnosing the user's own setup is the whole point of doctor;
// they are not redacted. The caller is warned in SKILL.md (guarded by
// TestSkillDocWarnsAboutSensitiveOutput) that this output is local filesystem
// layout / account info an agent may log or forward — see
// .claude/CLAWHUB_STANDARDS.md (warn about sensitive output).
func newDoctorCmd(app *App) *cobra.Command {
	return &cobra.Command{
		Use:   "doctor",
		Short: "Check config + token validity",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			cfg, err := app.resolveConfig()
			if err != nil {
				return err
			}

			// Confirm a usable token can be obtained (refresh if needed),
			// without requiring daily_log — doctor is a diagnostic and should
			// report token state even before the log path is wired (GOAL.md §8).
			tokenValid := false
			if tok, lerr := auth.LoadToken(cfg.TokenCache); lerr != nil {
				app.logger.Warn("token cache unreadable", "path", cfg.TokenCache, "err", lerr)
			} else if tok != nil {
				client := app.buildAuthClient(cmd.Context(), cfg, tok)
				if _, terr := client.CurrentToken(); terr != nil {
					app.logger.Debug("token check failed", "err", terr)
				} else {
					tokenValid = true
				}
			}

			report := doctorReport{
				TokenValid:     tokenValid,
				BaseURL:        cfg.BaseURL,
				User:           cfg.User,
				TokenPath:      cfg.TokenCache,
				ConfigPath:     cfg.ConfigPath,
				ConfigFound:    cfg.ConfigExists,
				ClientIDLoaded: cfg.ClientID != "",
				Scopes:         cfg.Scopes,
				Version:        version.Info().Version,
			}
			if err := writeJSON(cmd.OutOrStdout(), report); err != nil {
				return err
			}

			// Diagnose config/credential problems first: a missing or
			// credential-less config is the root cause of the cryptic
			// "Could not determine client ID" refresh failure (issue #6), and
			// it is exactly what users run doctor to find. Report it loudly and
			// exit non-zero instead of leaving a relative configPath as the only
			// (silent) tell.
			stderr := cmd.ErrOrStderr()
			if !cfg.HasOAuthClient() {
				if !cfg.ConfigExists {
					fprintf(stderr, "\nNo config found. Looked at: %s\n", strings.Join(cfg.SearchedPaths, ", "))
				} else {
					fprintf(stderr, "\nConfig %s is missing client_id/client_secret.\n", cfg.ConfigPath)
				}
				fprintf(stderr, "Set %s or pass --config <path> to a config.json with client_id and client_secret.\n", config.EnvConfig)
				fprintln(stderr, "Without OAuth client credentials, an expired token cannot be refreshed.")
				return silentExit(ExitConfig)
			}

			if !tokenValid {
				fprintln(stderr, "\nNot authenticated yet. Run:  google-health-cli auth login")
				return silentExit(ExitAuth)
			}
			return nil
		},
	}
}
