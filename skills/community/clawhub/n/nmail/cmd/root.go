package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

var (
	jsonOutput   bool
	prettyOutput bool
)

var rootCmd = &cobra.Command{
	Use:   "nmail",
	Short: "Korean email CLI for agents and humans",
	Long: `nmail — CLI for Korean email services (Naver, Daum, Kakao).
Designed for OpenClaw agents. JSON output by default.

Examples:
  nmail config add --provider naver
  nmail inbox --limit 10
  nmail read 42
  nmail send --to foo@naver.com --subject "Hi" --body "Hello"`,
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().BoolVar(&jsonOutput, "json", true, "output as JSON (default for agents)")
	rootCmd.PersistentFlags().BoolVar(&prettyOutput, "pretty", false, "output human-readable text")

	rootCmd.AddCommand(versionCmd)
	rootCmd.AddCommand(configCmd)
	rootCmd.AddCommand(inboxCmd)
	rootCmd.AddCommand(readCmd)
	rootCmd.AddCommand(searchCmd)
	rootCmd.AddCommand(watchCmd)
	rootCmd.AddCommand(sendCmd)
}
