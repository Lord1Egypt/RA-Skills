package cmd

import (
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
	if v := os.Getenv("GOOGLE_WORKSPACE_CONFIG_DIR"); v != "" {
		return v
	}
	home, err := os.UserHomeDir()
	if err != nil {
		return filepath.Join(".", ".google-workspace")
	}
	return filepath.Join(home, ".openclaw", "credentials", "google-workspace")
}

var rootCmd = &cobra.Command{
	Use:     "google-workspace",
	Short:   "Gmail, Calendar, Contacts, Drive, Docs, and Sheets for OpenClaw agents",
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
	return os.Getenv("GOOGLE_WORKSPACE_TOKEN_KEY")
}

func clientID() string {
	return os.Getenv("GOOGLE_CLIENT_ID")
}

func clientSecret() string {
	return os.Getenv("GOOGLE_CLIENT_SECRET")
}

func exitf(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "error: "+format+"\n", args...)
	os.Exit(1)
}
