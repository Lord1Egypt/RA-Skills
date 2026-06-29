package cli

import (
	"fmt"
	"time"

	"github.com/spf13/cobra"

	"github.com/stozo04/google-health-cli/internal/auth"
)

// newAuthCmd implements the new `auth` surface (GOAL.md §6, §8): login | logout |
// status. These are additive — the Python tool had none (ghealth owned auth).
func newAuthCmd(app *App) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "auth",
		Short: "Manage OAuth2 login (login/logout/status)",
		Args:  cobra.NoArgs,
		RunE: func(c *cobra.Command, _ []string) error {
			return c.Help()
		},
	}
	cmd.AddCommand(newAuthLoginCmd(app), newAuthLogoutCmd(app), newAuthStatusCmd(app))
	return cmd
}

// newAuthLoginCmd runs the loopback OAuth2 + PKCE flow and caches the token
// (GOAL.md §8). Read-only scopes only — there is intentionally no --write flag.
func newAuthLoginCmd(app *App) *cobra.Command {
	return &cobra.Command{
		Use:   "login",
		Short: "Authorize read-only Google Health access and cache a token",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			cfg, err := app.resolveConfig()
			if err != nil {
				return err
			}
			if !cfg.HasOAuthClient() {
				return withCode(ExitConfig, fmt.Errorf(
					"missing OAuth client: set client_id and client_secret in %s (or via %s / %s). See OAUTH_SETUP.md",
					cfg.ConfigPath, "GOOGLE_HEALTH_CLIENT_ID", "GOOGLE_HEALTH_CLIENT_SECRET",
				))
			}

			oauthCfg := auth.OAuthConfig(cfg.ClientID, cfg.ClientSecret, cfg.Scopes)
			stderr := cmd.ErrOrStderr()
			open := func(url string) error {
				fprintln(stderr, "Opening your browser to authorize read-only Google Health access.")
				fprintln(stderr, "If it doesn't open automatically, visit:\n  "+url)
				return auth.OpenBrowser(url)
			}

			res, err := auth.Login(cmd.Context(), oauthCfg, open, app.logger)
			if err != nil {
				return withCode(ExitAuth, fmt.Errorf("login failed: %w", err))
			}
			if err := auth.SaveToken(cfg.TokenCache, res.Token); err != nil {
				return withCode(ExitFailure, fmt.Errorf("cache token: %w", err))
			}

			fprintf(cmd.OutOrStdout(), "Logged in. Token cached to %s\n", cfg.TokenCache)
			fprintln(stderr, "Keep this file private — it grants read-only access to your Google Health data.")
			return nil
		},
	}
}

// newAuthLogoutCmd deletes the token cache (GOAL.md §8).
func newAuthLogoutCmd(app *App) *cobra.Command {
	return &cobra.Command{
		Use:   "logout",
		Short: "Delete the cached token",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			cfg, err := app.resolveConfig()
			if err != nil {
				return err
			}
			if err := auth.DeleteToken(cfg.TokenCache); err != nil {
				return withCode(ExitFailure, err)
			}
			fprintf(cmd.OutOrStdout(), "Logged out. Token cache removed: %s\n", cfg.TokenCache)
			return nil
		},
	}
}

// authStatusReport is the `auth status --json` shape. It reports presence,
// expiry and non-expired validity WITHOUT a network call (GOAL.md §8).
type authStatusReport struct {
	Present   bool   `json:"present"`
	Valid     bool   `json:"valid"`
	Expiry    string `json:"expiry"`
	TokenPath string `json:"token_path"`
}

// newAuthStatusCmd reports the cached token's presence/validity/expiry without
// hitting the API (GOAL.md §8).
func newAuthStatusCmd(app *App) *cobra.Command {
	var asJSON bool
	cmd := &cobra.Command{
		Use:   "status",
		Short: "Show cached token presence/validity/expiry (no network)",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			cfg, err := app.resolveConfig()
			if err != nil {
				return err
			}
			tok, lerr := auth.LoadToken(cfg.TokenCache)
			if lerr != nil {
				app.logger.Warn("token cache unreadable", "path", cfg.TokenCache, "err", lerr)
			}

			report := authStatusReport{TokenPath: cfg.TokenCache}
			if tok != nil {
				report.Present = true
				report.Valid = tok.Valid() // non-empty access token AND not expired.
				if !tok.Expiry.IsZero() {
					report.Expiry = tok.Expiry.UTC().Format(time.RFC3339)
				}
			}

			out := cmd.OutOrStdout()
			if asJSON {
				return writeJSON(out, report)
			}
			if !report.Present {
				fprintln(out, "No cached token. Run:  google-health-cli auth login")
				return nil
			}
			state := "valid"
			if !report.Valid {
				state = "expired or unusable (run: google-health-cli auth login, or it will refresh on next use)"
			}
			fprintf(out, "Token: present, %s\n", state)
			if report.Expiry != "" {
				fprintf(out, "Expiry: %s\n", report.Expiry)
			}
			fprintf(out, "Path: %s\n", report.TokenPath)
			return nil
		},
	}
	cmd.Flags().BoolVar(&asJSON, "json", false, "machine-readable output")
	return cmd
}
