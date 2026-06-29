package cli

import (
	"github.com/spf13/cobra"

	"github.com/stozo04/loseit-cli/internal/export"
)

// newLoginCmd implements `login`: authenticate with the configured Lose It
// email/password, obtain a fresh liauth session cookie, and save it to
// token_path. The only network call is the login POST; the token value is never
// printed. `days --json` also logs in on its own when needed, so this command is
// mainly for an explicit refresh or to verify credentials.
func newLoginCmd(app *App) *cobra.Command {
	return &cobra.Command{
		Use:   "login",
		Short: "Log in with email/password and save a fresh session token",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			cfg, err := app.resolveConfig()
			if err != nil {
				return err
			}
			token, err := export.Login(cmd.Context(), cfg)
			if err != nil {
				return withCode(ExitExport, err)
			}
			if err := export.SaveToken(cfg, token); err != nil {
				return withCode(ExitExport, err)
			}
			fprintf(cmd.OutOrStdout(),
				"Logged in as %s — session token saved to %s\n", cfg.Email, cfg.TokenPath)
			return nil
		},
	}
}
