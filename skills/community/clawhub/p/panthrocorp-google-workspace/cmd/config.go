package cmd

import (
	"encoding/json"
	"fmt"

	"github.com/PanthroCorp-Limited/openclaw-skills/google-workspace/internal/config"
	"github.com/spf13/cobra"
)

var configCmd = &cobra.Command{
	Use:   "config",
	Short: "Manage service scope configuration",
}

var configShowCmd = &cobra.Command{
	Use:   "show",
	Short: "Display current configuration",
	Run: func(cmd *cobra.Command, args []string) {
		cfg, err := config.Load(configDir)
		if err != nil {
			exitf("loading config: %v", err)
		}

		data, _ := json.MarshalIndent(cfg, "", "  ")
		fmt.Println(string(data))
		fmt.Printf("\nOAuth scopes: %v\n", cfg.OAuthScopes())
	},
}

var (
	setGmail    *bool
	setCalendar string
	setContacts *bool
	setDrive    string
	setDocs     string
	setSheets   string
)

var configSetCmd = &cobra.Command{
	Use:   "set",
	Short: "Update service scope configuration",
	Long:  "Update which Google services are enabled and their access level.\nAfter changing scopes, re-run 'google-workspace auth login' for the change to take effect.",
	Run: func(cmd *cobra.Command, args []string) {
		cfg, err := config.Load(configDir)
		if err != nil {
			exitf("loading config: %v", err)
		}

		if cmd.Flags().Changed("gmail") {
			cfg.Gmail = *setGmail
		}
		if cmd.Flags().Changed("calendar") {
			cfg.Calendar = config.CalendarMode(setCalendar)
		}
		if cmd.Flags().Changed("contacts") {
			cfg.Contacts = *setContacts
		}
		if cmd.Flags().Changed("drive") {
			cfg.Drive = config.ServiceMode(setDrive)
		}
		if cmd.Flags().Changed("docs") {
			cfg.Docs = config.ServiceMode(setDocs)
		}
		if cmd.Flags().Changed("sheets") {
			cfg.Sheets = config.ServiceMode(setSheets)
		}

		if err := config.Save(configDir, cfg); err != nil {
			exitf("saving config: %v", err)
		}

		data, _ := json.MarshalIndent(cfg, "", "  ")
		fmt.Println(string(data))
		fmt.Println("\nConfig saved. Run 'google-workspace auth login' if scopes have changed.")
	},
}

func init() {
	setGmail = configSetCmd.Flags().Bool("gmail", true, "enable Gmail read-only access")
	configSetCmd.Flags().StringVar(&setCalendar, "calendar", "readonly", "calendar mode: off, readonly, or readwrite")
	setContacts = configSetCmd.Flags().Bool("contacts", true, "enable Contacts read-only access")
	configSetCmd.Flags().StringVar(&setDrive, "drive", "readonly", "drive mode: off, readonly, or readwrite")
	configSetCmd.Flags().StringVar(&setDocs, "docs", "off", "docs mode: off, readonly, or readwrite")
	configSetCmd.Flags().StringVar(&setSheets, "sheets", "off", "sheets mode: off, readonly, or readwrite")

	configCmd.AddCommand(configShowCmd, configSetCmd)
	rootCmd.AddCommand(configCmd)
}
