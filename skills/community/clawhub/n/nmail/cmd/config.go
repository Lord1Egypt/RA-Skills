package cmd

import (
	"fmt"

	"github.com/harlock/nmail/internal/config"
	"github.com/harlock/nmail/internal/output"
	"github.com/spf13/cobra"
)

var configCmd = &cobra.Command{
	Use:   "config",
	Short: "Manage email account configuration",
	Long:  `Add, list, or remove email accounts from ~/.nmail/config.yaml`,
}

var configAddCmd = &cobra.Command{
	Use:   "add",
	Short: "Add an email account",
	RunE: func(cmd *cobra.Command, args []string) error {
		provider, _ := cmd.Flags().GetString("provider")
		email, _ := cmd.Flags().GetString("email")
		password, _ := cmd.Flags().GetString("password")

		if email == "" {
			return fmt.Errorf("--email is required")
		}
		if password == "" {
			return fmt.Errorf("--password is required")
		}

		cfg, err := config.Load()
		if err != nil {
			output.Error(err.Error())
			return nil
		}

		p := config.Provider(provider)
		account := config.Account{
			Email:    email,
			Password: password,
			Provider: p,
		}

		// Apply provider preset
		if preset, ok := config.ProviderPresets[p]; ok {
			account.IMAPHost = preset.IMAPHost
			account.IMAPPort = preset.IMAPPort
			account.IMAPTLS = preset.IMAPTLS
			account.SMTPHost = preset.SMTPHost
			account.SMTPPort = preset.SMTPPort
		}

		cfg.Add(account)
		if err := config.Save(cfg); err != nil {
			output.Error(err.Error())
			return nil
		}

		if prettyOutput {
			output.Pretty("Account added: %s (%s)", email, provider)
		} else {
			output.JSON(map[string]string{"status": "added", "email": email, "provider": provider})
		}
		return nil
	},
}

var configListCmd = &cobra.Command{
	Use:   "list",
	Short: "List configured accounts",
	RunE: func(cmd *cobra.Command, args []string) error {
		cfg, err := config.Load()
		if err != nil {
			output.Error(err.Error())
			return nil
		}

		type accountView struct {
			Email    string `json:"email"`
			Provider string `json:"provider"`
			Default  bool   `json:"default"`
			IMAPHost string `json:"imap_host"`
			SMTPHost string `json:"smtp_host"`
		}
		var views []accountView
		for _, a := range cfg.Accounts {
			views = append(views, accountView{
				Email:    a.Email,
				Provider: string(a.Provider),
				Default:  a.Email == cfg.DefaultAccount,
				IMAPHost: a.IMAPHost,
				SMTPHost: a.SMTPHost,
			})
		}
		if views == nil {
			views = []accountView{}
		}

		if prettyOutput {
			if len(views) == 0 {
				output.Pretty("No accounts configured.")
			}
			for _, v := range views {
				def := ""
				if v.Default {
					def = " (default)"
				}
				output.Pretty("%s [%s]%s — IMAP: %s", v.Email, v.Provider, def, v.IMAPHost)
			}
		} else {
			output.JSON(views)
		}
		return nil
	},
}

var configRemoveCmd = &cobra.Command{
	Use:   "remove",
	Short: "Remove an email account",
	RunE: func(cmd *cobra.Command, args []string) error {
		email, _ := cmd.Flags().GetString("email")
		if email == "" {
			return fmt.Errorf("--email is required")
		}

		cfg, err := config.Load()
		if err != nil {
			output.Error(err.Error())
			return nil
		}

		if !cfg.Remove(email) {
			output.Error("account not found: " + email)
			return nil
		}
		if err := config.Save(cfg); err != nil {
			output.Error(err.Error())
			return nil
		}

		if prettyOutput {
			output.Pretty("Removed: %s", email)
		} else {
			output.JSON(map[string]string{"status": "removed", "email": email})
		}
		return nil
	},
}

func init() {
	configAddCmd.Flags().String("provider", "naver", "email provider (naver, daum, kakao, custom)")
	configAddCmd.Flags().String("email", "", "email address")
	configAddCmd.Flags().String("password", "", "app password")
	configAddCmd.MarkFlagRequired("email")
	configAddCmd.MarkFlagRequired("password")

	configRemoveCmd.Flags().String("email", "", "email address to remove")
	configRemoveCmd.MarkFlagRequired("email")

	configCmd.AddCommand(configAddCmd)
	configCmd.AddCommand(configListCmd)
	configCmd.AddCommand(configRemoveCmd)
}
