package cmd

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	"github.com/spf13/cobra"
)

var (
	version   = "dev"
	configDir string
	outputFmt string
)

// SetVersion sets the version string displayed by --version.
func SetVersion(v string) {
	version = v
}

func defaultConfigDir() string {
	if v := os.Getenv("ZOHO_MAIL_CONFIG_DIR"); v != "" {
		return v
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return filepath.Join(".", ".zoho-mail")
	}
	return filepath.Join(home, ".openclaw", "credentials", "zoho-mail")
}

var rootCmd = &cobra.Command{
	Use:     "zoho-mail",
	Short:   "Full read/write Zoho Mail access for OpenClaw agents",
	Version: version,
}

func init() {
	rootCmd.PersistentFlags().StringVar(&configDir, "config-dir", defaultConfigDir(), "path to config and credential directory")
	rootCmd.PersistentFlags().StringVar(&outputFmt, "output", "json", "output format: json or text")
}

// Execute runs the root command.
func Execute() error {
	return rootCmd.Execute()
}

func encryptionKey() string {
	return os.Getenv("ZOHO_MAIL_TOKEN_KEY")
}

func clientID() string {
	return os.Getenv("ZOHO_CLIENT_ID")
}

func clientSecret() string {
	return os.Getenv("ZOHO_CLIENT_SECRET")
}

func exitf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "error: "+format+"\n", args...)
	os.Exit(1)
}

func printJSON(v any) {
	data, _ := json.MarshalIndent(v, "", "  ")
	fmt.Println(string(data))
}
