package cli

import (
	"github.com/spf13/cobra"
)

// configView is the stable shape emitted by `config show --json`. Key order:
// token_path, export_url, login_url, email, password_set, config_path. The
// password is never emitted — only a boolean that it is set; email is the user's
// own account id and is shown as-is.
type configView struct {
	TokenPath   string `json:"token_path"`
	ExportURL   string `json:"export_url"`
	LoginURL    string `json:"login_url"`
	Email       string `json:"email"`
	PasswordSet bool   `json:"password_set"`
	ConfigPath  string `json:"config_path"`
}

// newConfigCmd implements `config [show|path]`, a convenience for inspecting the
// resolved configuration without hand-reading config.json.
func newConfigCmd(app *App) *cobra.Command {
	cmd := &cobra.Command{
		Use:   "config",
		Short: "Inspect configuration (show/path)",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			return cmd.Help()
		},
	}
	cmd.AddCommand(newConfigShowCmd(app), newConfigPathCmd(app))
	return cmd
}

func newConfigShowCmd(app *App) *cobra.Command {
	var asJSON bool
	cmd := &cobra.Command{
		Use:   "show",
		Short: "Print the resolved effective config",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			cfg, err := app.resolveConfig()
			if err != nil {
				return err
			}
			out := cmd.OutOrStdout()
			if asJSON {
				return writeJSON(out, configView{
					TokenPath:   cfg.TokenPath,
					ExportURL:   cfg.ExportURL,
					LoginURL:    cfg.LoginURL,
					Email:       cfg.Email,
					PasswordSet: cfg.Password != "",
					ConfigPath:  cfg.ConfigPath,
				})
			}
			pw := "<unset>"
			if cfg.Password != "" {
				pw = "<set>"
			}
			fprintf(out, "token_path:  %s\n", cfg.TokenPath)
			fprintf(out, "export_url:  %s\n", cfg.ExportURL)
			fprintf(out, "login_url:   %s\n", cfg.LoginURL)
			fprintf(out, "email:       %s\n", cfg.Email)
			fprintf(out, "password:    %s\n", pw)
			fprintf(out, "config_path: %s\n", cfg.ConfigPath)
			return nil
		},
	}
	cmd.Flags().BoolVar(&asJSON, "json", false, "machine-readable output")
	return cmd
}

func newConfigPathCmd(app *App) *cobra.Command {
	return &cobra.Command{
		Use:   "path",
		Short: "Print the config.json path in use",
		Args:  cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			cfg, err := app.resolveConfig()
			if err != nil {
				return err
			}
			fprintln(cmd.OutOrStdout(), cfg.ConfigPath)
			return nil
		},
	}
}
