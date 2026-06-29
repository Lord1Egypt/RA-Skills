package cli

import (
	"github.com/spf13/cobra"

	"github.com/stozo04/loseit-cli/internal/config"
	"github.com/stozo04/loseit-cli/internal/export"
	"github.com/stozo04/loseit-cli/internal/version"
)

// doctorReport is the doctor JSON shape. Key order frozen: tokenPresent,
// exportURL, tokenPath, configPath, version. There is no network check — Lose It
// has no OAuth to validate, and tokenPresent is a local file/env presence test
// that never reveals the cookie value.
type doctorReport struct {
	TokenPresent       bool   `json:"tokenPresent"`
	CredentialsPresent bool   `json:"credentialsPresent"`
	ExportURL          string `json:"exportURL"`
	LoginURL           string `json:"loginURL"`
	TokenPath          string `json:"tokenPath"`
	ConfigPath         string `json:"configPath"`
	Version            string `json:"version"`
}

// newDoctorCmd implements `doctor`: print config + whether a token is present as
// indent-2 JSON. No network. Lacking a token is not a failure — the --zip path
// needs none — so doctor always exits 0; it just hints when a token is missing.
func newDoctorCmd(app *App) *cobra.Command {
	return &cobra.Command{
		Use:   "doctor",
		Short: "Report config + whether a Lose It token is present (no network)",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			cfg, err := app.resolveConfig()
			if err != nil {
				return err
			}

			present := export.HasToken(cfg)
			creds := cfg.HasCredentials()
			report := doctorReport{
				TokenPresent:       present,
				CredentialsPresent: creds,
				ExportURL:          cfg.ExportURL,
				LoginURL:           cfg.LoginURL,
				TokenPath:          cfg.TokenPath,
				ConfigPath:         cfg.ConfigPath,
				Version:            version.Info().Version,
			}
			if err := writeJSON(cmd.OutOrStdout(), report); err != nil {
				return err
			}

			switch {
			case present:
				// All set — a saved token is present.
			case creds:
				fprintf(cmd.ErrOrStderr(),
					"\nNo saved token yet, but credentials are set — `loseit-cli login` "+
						"(or `days` on its own) will log in and save one.\n")
			default:
				fprintf(cmd.ErrOrStderr(),
					"\nNo Lose It token or credentials. Set %s/%s (or email/password in config.json) "+
						"then run `loseit-cli login`, or pass --zip <export.zip>.\n",
					config.EnvEmail, config.EnvPassword)
			}
			return nil
		},
	}
}
