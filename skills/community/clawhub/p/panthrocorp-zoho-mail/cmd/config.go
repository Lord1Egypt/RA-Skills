package cmd

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"

	"github.com/spf13/cobra"
)

const configFileName = "config.json"

// mailConfig holds the persisted skill configuration.
type mailConfig struct {
	Email string `json:"email"`
}

func loadConfig(dir string) (mailConfig, error) {
	path := filepath.Join(dir, configFileName)
	data, err := os.ReadFile(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return mailConfig{}, nil
		}
		return mailConfig{}, fmt.Errorf("reading config: %w", err)
	}

	var cfg mailConfig
	if err := json.Unmarshal(data, &cfg); err != nil {
		return mailConfig{}, fmt.Errorf("parsing config: %w", err)
	}

	return cfg, nil
}

func saveConfig(dir string, cfg mailConfig) error {
	if err := os.MkdirAll(dir, 0o700); err != nil {
		return fmt.Errorf("creating config directory: %w", err)
	}

	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return fmt.Errorf("marshalling config: %w", err)
	}

	data = append(data, '\n')
	path := filepath.Join(dir, configFileName)
	return os.WriteFile(path, data, 0o600)
}

var configCmd = &cobra.Command{
	Use:   "config",
	Short: "Manage skill configuration",
}

var configShowCmd = &cobra.Command{
	Use:   "show",
	Short: "Display current configuration",
	Run: func(cmd *cobra.Command, args []string) {
		cfg, err := loadConfig(configDir)
		if err != nil {
			exitf("loading config: %v", err)
		}
		printJSON(cfg)
	},
}

var setEmail string

var configSetCmd = &cobra.Command{
	Use:   "set",
	Short: "Update skill configuration",
	Long:  "Set the email address for the Zoho Mail account. Re-run 'zoho-mail auth login' after changing this value.",
	Run: func(cmd *cobra.Command, args []string) {
		cfg, err := loadConfig(configDir)
		if err != nil {
			exitf("loading config: %v", err)
		}

		if cmd.Flags().Changed("email") {
			cfg.Email = setEmail
		}

		if cfg.Email == "" {
			exitf("--email is required")
		}

		if err := saveConfig(configDir, cfg); err != nil {
			exitf("saving config: %v", err)
		}

		printJSON(cfg)
		fmt.Println("\nConfig saved. Run 'zoho-mail auth login' if this is a new account.")
	},
}

func init() {
	configSetCmd.Flags().StringVar(&setEmail, "email", "", "Zoho Mail email address for this account")

	configCmd.AddCommand(configShowCmd, configSetCmd)
	rootCmd.AddCommand(configCmd)
}
